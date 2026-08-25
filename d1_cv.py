"""D1 + D6 discharge run for the Shu-Yu-Mulvey (2024) reproduction.

VERIFICATION RUN, NOT A STRATEGY (the 0/1 rule is F9, PARKED section 4). One pass
over the refit blocks fits every candidate lambda, then:

  1. D6 -- both state-naming rules recorded per (block, lambda): rule A (this
     repo, bull = lower downside-deviation centroid) vs rule B (the paper,
     bull = higher cumulative training return). Disagreements are counted.
  2. The fixed-lambda sweep on the paper's ACTUAL grid, in this repo's units:
     paper {0, 5, 15, 35, 70, 150} x2 = {0, 10, 30, 70, 140, 300}.
  3. D1 -- the paper's monthly CV: at each selection date, for each candidate,
     the trailing 8-year validation Sharpe of that candidate's online strategy
     (net of costs, same execution convention), pick the argmax. The lambda-hat
     series is a required output (the paper never reports its own).

Choices the paper leaves unstated are preregistered in
docs/REPRO-SJM2024-FINDINGS.md ("Preregistered for the D1/D6 run") before this
was first executed: costs inside validation, 21-day reselection, ties to the
larger lambda, rule B on raw returns, effective OOS start = first date with a
full 8-year signal history.

Run: .venv\\Scripts\\python.exe d1_cv.py [--ticker ^GSPC] [--start 1970-01-01]
     [--oos-start 1990-01-01]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))

from repro_sjm2024 import (
    COST_ONE_WAY,
    EXECUTION_LAG,
    REFIT_DAYS,
    TRADING_DAYS,
    TRAIN_DAYS,
    VOL_WINDOW,
    backtest,
    daily_riskfree,
    load_prices,
    load_riskfree,
)
from src.jumpmodel import fit_jump_model, online_states, order_states_by
from src.pathfunctionals import cdar_curve
from src.sjm_features import DOWNSIDE_FEATURE, build_features

PAPER_GRID = (0.0, 5.0, 15.0, 35.0, 70.0, 150.0)
OUR_GRID = tuple(2.0 * lam for lam in PAPER_GRID)
VALIDATION_DAYS = 8 * TRADING_DAYS
SELECT_EVERY = 21
ROOT = Path(__file__).resolve().parent


def signals_for_grid(features: pd.DataFrame, returns: pd.Series, naming: str = "dd"):
    """One pass over the blocks; every candidate fit on the same training data.

    Returns the 0/1 bull signal per lambda and the D6 record: for each
    (block, lambda), whether rule A and rule B name the same bull state.
    `naming` picks which rule drives the signal -- "dd" (rule A, this repo:
    bull = lower downside-deviation centroid) or "cumret" (rule B, the paper:
    bull = higher cumulative training return). Both rules are recorded either way.
    """
    X = features.to_numpy()
    dates = features.index
    r = returns.to_numpy()
    signals = pd.DataFrame(np.nan, index=dates, columns=list(OUR_GRID))
    records = []

    for block_start in range(TRAIN_DAYS, len(dates), REFIT_DAYS):
        train = X[block_start - TRAIN_DAYS : block_start]
        mean = train.mean(axis=0)
        scale = train.std(axis=0)
        scale[scale == 0] = 1.0
        train_s = (train - mean) / scale
        block_end = min(block_start + REFIT_DAYS, len(dates))
        window = (X[block_start - TRAIN_DAYS : block_end] - mean) / scale
        r_train = r[block_start - TRAIN_DAYS : block_start]

        for lam in OUR_GRID:
            states, centroids, _ = fit_jump_model(
                train_s, k=2, jump_penalty=lam, n_init=10, seed=0
            )
            order = order_states_by(centroids, DOWNSIDE_FEATURE)
            bull_a = int(order[0])
            cumret = [r_train[states == j].sum() for j in range(2)]
            bull_b = int(np.argmax(cumret))
            records.append(
                {"block": dates[block_start], "lam": lam, "agree": bull_a == bull_b}
            )
            bull = bull_a if naming == "dd" else bull_b
            ordered = centroids[[bull, 1 - bull]]
            signals.iloc[block_start:block_end, signals.columns.get_loc(lam)] = (
                1.0 - online_states(window, ordered, lam)[TRAIN_DAYS:]
            )

    return signals, pd.DataFrame(records)


def state_vs_rv_auc(signal: pd.Series, returns: pd.Series) -> float:
    rv = returns.rolling(VOL_WINDOW).std().mul(np.sqrt(TRADING_DAYS))
    state = (1.0 - signal).dropna()
    common = state.index.intersection(rv.dropna().index)
    bear = rv.loc[common][state.loc[common] == 1.0].to_numpy()
    bull = rv.loc[common][state.loc[common] == 0.0].to_numpy()
    if len(bear) == 0 or len(bull) == 0:
        return float("nan")
    return float(np.mean([(bull < b).mean() + 0.5 * (bull == b).mean() for b in bear]))


def cv_select(signals: pd.DataFrame, returns: pd.Series, rf: pd.Series, oos_start: pd.Timestamp):
    """The paper's monthly selector, on precomputed candidate signal tracks."""
    net = {}
    for lam in OUR_GRID:
        held = signals[lam].shift(EXECUTION_LAG).fillna(0.0)
        traded = held.diff().abs().fillna(held.abs())
        net[lam] = held * returns + (1.0 - held) * rf - traded * COST_ONE_WAY
    excess = pd.DataFrame(net).sub(rf, axis=0)

    dates = signals.index
    first_signal = TRAIN_DAYS
    earliest = first_signal + VALIDATION_DAYS
    start = max(int(dates.searchsorted(oos_start)), earliest)

    chosen = pd.Series(np.nan, index=dates)
    lam_hat = {}
    for i in range(start, len(dates), SELECT_EVERY):
        window = excess.iloc[i - VALIDATION_DAYS : i]
        sharpe = window.mean() / window.std() * np.sqrt(TRADING_DAYS)
        best = sharpe.iloc[::-1].idxmax()  # ties break to the larger lambda
        lam_hat[dates[i]] = best
        stop = min(i + SELECT_EVERY, len(dates))
        chosen.iloc[i:stop] = signals[best].iloc[i:stop]

    return chosen.dropna(), pd.Series(lam_hat, name="lambda_ours")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ticker", default="^GSPC")
    parser.add_argument("--start", default="1970-01-01")
    parser.add_argument("--oos-start", default="1990-01-01")
    parser.add_argument("--naming", choices=("dd", "cumret"), default="dd",
                        help="state naming driving the signal: dd = rule A (this repo), "
                             "cumret = rule B (the paper)")
    args = parser.parse_args()

    prices = load_prices(args.ticker, args.start)
    returns = prices.pct_change().dropna()
    rf = daily_riskfree(load_riskfree(), returns.index)
    features = build_features((returns - rf).dropna())
    returns = returns.reindex(features.index)
    rf = rf.reindex(features.index)

    signals, naming = signals_for_grid(features, returns, naming=args.naming)
    print(f"\nsignal naming rule: {args.naming} "
          f"({'rule A, this repo' if args.naming == 'dd' else 'rule B, the paper'})")

    # --- D6 ---
    print("\nD6 -- naming-rule agreement per lambda (rule A: downside-dev centroid;"
          " rule B: training cumret)")
    for lam in OUR_GRID:
        sub = naming[naming["lam"] == lam]
        n_dis = int((~sub["agree"]).sum())
        flag = "" if n_dis == 0 else "  <-- DISAGREEMENTS"
        print(f"  lambda {lam:>5g} (paper {lam/2:>5g}): "
              f"{int(sub['agree'].sum())}/{len(sub)} blocks agree{flag}")
        if n_dis:
            for _, row in sub[~sub["agree"]].iterrows():
                print(f"      block starting {row['block'].date()}")

    # --- fixed-lambda sweep on the paper's grid ---
    chosen, lam_hat = cv_select(signals, returns, rf, pd.Timestamp(args.oos_start))
    full = chosen.index

    # Every signal and every lambda-hat selection is causal, so truncating the
    # scoring window needs no refit: the sub-window result is exactly what a
    # run ending there would have produced.
    windows = {
        "paper window (to 2023-12-29)": full[full <= pd.Timestamp("2023-12-29")],
        "full sample": full,
    }
    results = {}
    for label, oos in windows.items():
        print(f"\n{label}: {oos[0].date()} to {oos[-1].date()} "
              f"({len(oos)} days, {len(oos)/TRADING_DAYS:.1f} years)")
        rows = {"Buy & hold": pd.Series(1.0, index=oos)}
        for lam in OUR_GRID:
            rows[f"lam {lam:g} (paper {lam/2:g})"] = signals[lam].reindex(oos)
        rows["CV monthly (D1)"] = chosen.reindex(oos)

        r_oos, rf_oos = returns.reindex(oos), rf.reindex(oos)
        results = {name: backtest(r_oos, pos, rf_oos) for name, pos in rows.items()}

        header = f"{'':<26s}" + "".join(
            f"{c:>10s}" for c in ["CAGR", "Vol", "Sharpe", "MaxDD", "Turnover", "TimeIn", "pain", "AUC"]
        )
        print(header)
        print("-" * len(header))
        for name, stats in results.items():
            pain = cdar_curve(stats["curve"], (1.0,)).iloc[0]
            auc = state_vs_rv_auc(rows[name], returns.reindex(oos)) if name != "Buy & hold" else float("nan")
            print(f"{name:<26s}"
                  f"{stats['CAGR']:>10.1%}{stats['Vol']:>10.1%}{stats['Sharpe']:>10.2f}"
                  f"{stats['MaxDD']:>10.1%}{stats['Turnover']:>10.0%}{stats['TimeIn']:>10.0%}"
                  f"{pain:>10.1%}{auc:>10.3f}")

        gap = results["Buy & hold"]["CAGR"] - results["CV monthly (D1)"]["CAGR"]
        frac = results["CV monthly (D1)"]["TimeIn"]
        penalty = 0.018 * (1.0 - frac)
        print(f"X4 on this window: CAGR gap CV vs B&H = {gap:+.2%}/yr vs dividend penalty "
              f"~{penalty:.2%}/yr -> "
              f"{'return claim CONSISTENT with replication on TR data' if gap <= penalty else 'NOT closed by dividends'}")

    # --- lambda-hat, the required output ---
    in_paper_units = (lam_hat / 2.0).astype(float)
    print("\nlambda-hat distribution (paper units), monthly selections "
          f"n={len(lam_hat)}:")
    counts = in_paper_units.value_counts().sort_index()
    for value, count in counts.items():
        print(f"  {value:>5g}: {count:>4d}  ({count/len(lam_hat):.0%})")
    print(f"  median {in_paper_units.median():g}, "
          f"switches of lambda-hat itself: {int((in_paper_units.diff() != 0).sum() - 1)}")

    suffix = "" if args.naming == "dd" else f"_{args.naming}"
    out = ROOT / "figures" / f"sjm2024_lambda_hat{suffix}.csv"
    out.parent.mkdir(exist_ok=True)
    in_paper_units.rename("lambda_hat_paper_units").to_csv(out)
    print(f"\nlambda-hat series written: {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
