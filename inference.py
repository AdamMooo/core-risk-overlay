r"""Inference for the SJM reproduction -- the SHALLOW half.

VERIFICATION RUN, NOT A STRATEGY (the 0/1 rule is F9, PARKED section 4).

Design preregistered in docs/REPRO-SJM2024-FINDINGS.md ("Preregistered for the
inference run", 2026-08-26) before first execution, and nothing here may be
changed after a number is seen.

The split this file implements one side of: block machinery for functionals that
AVERAGE OVER MANY DAYS spread across the sample -- Sharpe, the pain index, CDaR
at shallow alpha -- and nothing else. MaxDD and CDaR at 1-5% are produced by two
episodes (2000-02, 2007-09); the resample-to-resample variation of a maximum
drawdown is dominated by how often the resampler concatenates blocks drawn from
those two episodes, which is a property of the block length b and not of the
market. Those go to deeptail_mc.py, under explicit simulated nulls. Nothing
crosses.

  Sharpe difference     Ledoit-Wolf (2008) studentized circular block bootstrap,
                        prewhitened-QS HAC standard error. src/ledoitwolf.py.
  pain, CDaR(25%,50%)   same resampler, but PERCENTILE intervals -- they are not
                        smooth functions of means, so there is no delta-method
                        standard error to studentize with, and the interval is
                        reported as the weaker object it is.

Block size is DECLARED, not calibrated: the grid is run in full, every p-value is
reported, and the largest is the headline. Politis-White is printed as a
reference point and is never the selector.

Run: .venv\Scripts\python.exe inference.py
     .venv\Scripts\python.exe inference.py --refresh    rebuild the net-return cache
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

import ledoitwolf as lw
from repro_sjm2024 import (
    CACHE,
    TRADING_DAYS,
    VOL_WINDOW,
    backtest,
    daily_riskfree,
    load_prices,
    load_riskfree,
    run_jump_model,
)
from src.pathfunctionals import cdar
from src.sjm_features import build_features
from volthreshold import JM_LAMBDAS_PAPER, PAIRS, threshold_signal

BLOCK_GRID = (5, 10, 21, 42, 63, 126)
N_BOOT = 4999
N_BOOT_PERCENTILE = 999
ALPHA = 0.05
DELTA_SHARPE = 0.10
DELTA_PAIN = 0.010
SHALLOW_ALPHAS = (0.25, 0.50, 1.00)
BENCHMARK = "JM fixed paper-25"
PAPER_END = "2023-12-29"
NETS_CACHE = CACHE / "infer_nets_gspc.csv"

# Preregistered as calendar windows, deliberately wider than the peak-to-trough
# spans in repro_sjm2024.EPISODES, which they contain.
LEAVE_OUT = {
    "no dot-com": (("2000-01-01", "2002-12-31"),),
    "no GFC": (("2007-07-01", "2009-06-30"),),
    "neither": (("2000-01-01", "2002-12-31"), ("2007-07-01", "2009-06-30")),
}


def build_nets(ticker: str, start: str, oos_start: str, refresh: bool) -> pd.DataFrame:
    """Daily NET returns of every rule, plus the risk-free leg. Cached: the refit loop is slow.

    DERIVED artifact -- registered in src/manifest.py PROVENANCE. Costs a full
    jump-model refit loop to regenerate, which is why --refresh is explicit.
    """
    if NETS_CACHE.exists() and not refresh:
        return pd.read_csv(NETS_CACHE, index_col=0, parse_dates=True)

    prices = load_prices(ticker, start)
    returns = prices.pct_change().dropna()
    rf = daily_riskfree(load_riskfree(), returns.index)
    features = build_features((returns - rf).dropna())
    returns, rf = returns.reindex(features.index), rf.reindex(features.index)
    realized = returns.rolling(VOL_WINDOW).std().mul(np.sqrt(TRADING_DAYS))

    signals = {
        f"JM fixed paper-{lam:g}": run_jump_model(
            features, pd.Timestamp(oos_start), 2.0 * lam
        ).dropna()
        for lam in JM_LAMBDAS_PAPER
    }
    oos = signals[BENCHMARK].index
    signals["Buy & hold"] = pd.Series(1.0, index=oos)
    for p_exit, p_reenter in PAIRS:
        signals[f"RV band ({p_exit},{p_reenter})"] = threshold_signal(
            realized, oos, p_exit, p_reenter
        )

    r_oos, rf_oos = returns.reindex(oos), rf.reindex(oos)
    frame = pd.DataFrame(
        {name: backtest(r_oos, sig.reindex(oos), rf_oos)["net"] for name, sig in signals.items()}
    )
    frame["rf"] = rf_oos
    frame.to_csv(NETS_CACHE)
    return frame


def excess(nets: pd.DataFrame, name: str) -> np.ndarray:
    return (nets[name] - nets["rf"]).to_numpy(dtype=float)


def annual_sharpe(r: np.ndarray) -> float:
    return float(r.mean() / r.std(ddof=0) * np.sqrt(TRADING_DAYS))


def wealth(r: np.ndarray) -> pd.Series:
    return pd.Series(np.cumprod(1.0 + r))


def pain(r: np.ndarray) -> float:
    return float(cdar(wealth(r), 1.0))


def sharpe_test(r_i: np.ndarray, r_n: np.ndarray, seed: int) -> pd.DataFrame:
    """The Ledoit-Wolf test across the declared block grid. One row per b, all reported."""
    psi = lw.hac_psi(lw.moment_conditions(r_i, r_n, lw.moments(r_i, r_n)))
    rows = []
    for block in BLOCK_GRID:
        out = lw.studentized_pvalue(
            r_i, r_n, block=block, n_boot=N_BOOT, rng=np.random.default_rng(seed), psi_hat=psi
        )
        scale = np.sqrt(TRADING_DAYS)
        rows.append(
            {
                "b": block,
                "delta": out["delta"] * scale,
                "se": out["se"] * scale,
                "d": out["d"],
                "p": out["pvalue"],
                "lo": out["ci"][0] * scale,
                "hi": out["ci"][1] * scale,
            }
        )
    return pd.DataFrame(rows).set_index("b")


def percentile_test(r_i: np.ndarray, r_n: np.ndarray, statistic, seed: int) -> pd.DataFrame:
    """Circular block bootstrap percentile interval for a path functional's difference.

    Weaker than the studentized interval by construction and labelled as such:
    a path functional is not a smooth function of means, so there is no
    delta-method standard error to studentize with. The wealth curve is rebuilt
    from each resample, which is exactly the step that stops being defensible at
    deep alpha -- hence SHALLOW_ALPHAS only.
    """
    observed = statistic(r_i) - statistic(r_n)
    rows = []
    for block in BLOCK_GRID:
        rng = np.random.default_rng(seed)
        n_obs = len(r_i)
        draws = np.empty(N_BOOT_PERCENTILE)
        for m in range(N_BOOT_PERCENTILE):
            idx = lw.circular_block_indices(n_obs, block, rng)
            draws[m] = statistic(r_i[idx]) - statistic(r_n[idx])
        lo, hi = np.percentile(draws, [100 * ALPHA / 2, 100 * (1 - ALPHA / 2)])
        rows.append({"b": block, "diff": observed, "lo": lo, "hi": hi,
                     "p_zero_in": float(lo <= 0.0 <= hi)})
    return pd.DataFrame(rows).set_index("b")


def report_sharpe(nets: pd.DataFrame, names: list[str]) -> None:
    r_jm = excess(nets, BENCHMARK)
    print(f"\n{'='*78}\nSHARPE -- Ledoit-Wolf studentized circular block bootstrap, "
          f"M={N_BOOT}\n{'='*78}")
    print(f"reference block length (Politis-White 2004, NOT the selector): "
          f"{lw.politis_white_block(r_jm):.1f}")
    print(f"\n{BENCHMARK}: annualised Sharpe {annual_sharpe(r_jm):.3f}")

    for name in names:
        r_band = excess(nets, name)
        table = sharpe_test(r_band, r_jm, seed=20260826)
        headline = table["p"].max()
        equivalent = bool((table["lo"] > -DELTA_SHARPE).all())
        print(f"\n{name}: annualised Sharpe {annual_sharpe(r_band):.3f}   "
              f"(band - JM, both annualised)")
        print(table.to_string(float_format=lambda v: f"{v: .4f}"))
        print(f"  headline p (max over the declared grid): {headline:.4f}   "
              f"-> {'NOT distinguishable' if headline > ALPHA else 'DISTINGUISHABLE'} at alpha={ALPHA}")
        print(f"  Z2 equivalence at delta={DELTA_SHARPE}: every interval above -{DELTA_SHARPE}? "
              f"{'YES -- not materially worse' if equivalent else 'NO'}")


def report_paths(nets: pd.DataFrame, names: list[str]) -> None:
    r_jm = excess(nets, BENCHMARK)
    print(f"\n{'='*78}\nSHALLOW PATH FUNCTIONALS -- percentile intervals, weaker by construction, "
          f"M={N_BOOT_PERCENTILE}\n{'='*78}")
    statistics = {"pain index": pain}
    for a in SHALLOW_ALPHAS:
        if a < 1.0:
            statistics[f"CDaR({a:.0%})"] = lambda r, a=a: float(cdar(wealth(r), a))

    for label, statistic in statistics.items():
        print(f"\n{label}   {BENCHMARK}: {statistic(r_jm):.2%}")
        for name in names:
            r_band = excess(nets, name)
            table = percentile_test(r_band, r_jm, statistic, seed=20260826)
            widest = table.loc[(table["hi"] - table["lo"]).idxmax()]
            zero_in = bool(table["p_zero_in"].max() > 0)
            print(f"  {name}: {statistic(r_band):.2%}   diff {widest['diff']:+.2%}   "
                  f"widest 95% CI [{widest['lo']:+.2%}, {widest['hi']:+.2%}]   "
                  f"{'contains 0' if zero_in else 'excludes 0'}")
            if label == "pain index":
                print(f"    Z2 equivalence at delta={DELTA_PAIN:.1%}: "
                      f"{'YES' if (table['lo'] > -DELTA_PAIN).all() else 'NO'}")


def report_episodes(nets: pd.DataFrame, names: list[str]) -> None:
    """Leave-one-episode-out. DESCRIPTIVE. No p-value is computed or implied.

    Dropping days splices the return series across the gap, so the wealth curve
    is a synthetic path, not a counterfactual history. It answers one question
    only -- how much of each number is those two episodes -- and that is the
    question the deep tail's effective sample size of 2 makes worth asking.
    """
    print(f"\n{'='*78}\nLEAVE-ONE-EPISODE-OUT -- descriptive, not inference\n{'='*78}")
    columns = [BENCHMARK] + names
    header = f"{'':<16s}" + "".join(f"{c:>22s}" for c in columns)
    for label, windows in {"full sample": (), **LEAVE_OUT}.items():
        keep = pd.Series(True, index=nets.index)
        for lo, hi in windows:
            keep &= ~((nets.index >= pd.Timestamp(lo)) & (nets.index <= pd.Timestamp(hi)))
        trimmed = nets[keep]
        if label == "full sample":
            print(header)
            print("-" * len(header))
        cells = []
        for name in columns:
            r = excess(trimmed, name)
            cells.append(f"{annual_sharpe(r):>10.2f}{pain(r):>12.2%}")
        print(f"{label:<16s}" + "".join(cells))
    print("                    (Sharpe, pain index) per rule")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ticker", default="^GSPC")
    parser.add_argument("--start", default="1970-01-01")
    parser.add_argument("--oos-start", default="1990-01-01")
    parser.add_argument("--refresh", action="store_true", help="rebuild the net-return cache")
    args = parser.parse_args()

    nets = build_nets(args.ticker, args.start, args.oos_start, args.refresh)
    nets = nets[nets.index <= pd.Timestamp(PAPER_END)]
    names = [f"RV band ({p_exit},{p_reenter})" for p_exit, p_reenter in PAIRS]

    print(f"paper window: {nets.index[0].date()} to {nets.index[-1].date()}   "
          f"T = {len(nets)} days ({len(nets)/TRADING_DAYS:.1f} years)")
    print(f"claim tuple: (daily, whole out-of-sample path, "
          f"{{Sharpe, pain, CDaR(shallow)}}, ^GSPC {nets.index[0].date()}-{nets.index[-1].date()}, "
          f"equal value of the functional)")

    report_sharpe(nets, names)
    report_paths(nets, names)
    report_episodes(nets, names)

    print(f"\n{'='*78}")
    print("Y2's intersection-union test lives in deeptail_mc.py: the claim is that the")
    print("jump model beats EVERY band, so its null is a union and the statistic is the")
    print("MAXIMUM of the three p-values, at exactly alpha with no correction.")
    print("Nothing above may be carried to the deep tail, at any confidence.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
