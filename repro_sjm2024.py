"""Reproduction of Shu, Yu & Mulvey (2024), J. Asset Management 25(5).

VERIFICATION RUN, NOT A STRATEGY. The 0/1 exposure rule is F9, permanently
closed in PARKED §4; it is reconstructed here only because reproducing the
paper's claim requires reproducing the paper's rule. The output is a
verification result. There is no live path and none is designed.

What this adds to the paper: the two reactive incumbents its comparison set
omits -- a 200-day moving average and a capped volatility target -- plus the
PROBLEM-MAP §0.9 diagnostic (is the fitted state a trailing-volatility meter?).

Scoring note. Sharpe divides by total volatility and cannot see the path, so it
is the wrong scorecard for a downside-risk claim. The path metrics below are the
ones the paper's claim lives on, and the CDaR curve is reported whole rather than
at one alpha -- leak-register row 11.

Declared deviations from the paper, before any number is read:
  D1  Fixed jump penalty. The paper reselects lambda monthly by trailing
      8-year validation Sharpe. This run holds lambda fixed, so it reproduces
      the model but not the selection procedure.
  D2  Price index, not total return. ^GSPC carries no dividends, so levels of
      return are understated by roughly the dividend yield.
  D3  The online window start is frozen within each 6-month block rather than
      rolling daily. The state at t is still a function of data up to t only.
  D4  The implementation is not yet verified against the authors' package or
      against synthetic regimes with known states. Until it is, a null here is
      not evidence.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))

from src.caching import cached_series
from src.data_loader import download_daily_prices
from src.jumpmodel import fit_jump_model, online_states, order_states_by
from src.pathfunctionals import cdar_curve, depth_in_window, time_under_water
from src.sjm_features import DOWNSIDE_FEATURE, build_features

TRAIN_DAYS = 3000
REFIT_DAYS = 126
LAMBDA = 50.0
COST_ONE_WAY = 0.0010
EXECUTION_LAG = 2  # signal at t executes at t+1, holds from t+2
TRADING_DAYS = 252
SMA_WINDOW = 200
VOL_TARGET = 0.10
VOL_WINDOW = 60
CDAR_ALPHAS = (0.01, 0.05, 0.10, 0.25, 0.50, 1.00)
UNDERWATER = (0.10, 0.20)
ROOT = Path(__file__).resolve().parent
CACHE = ROOT / "data"

EPISODES = {
    "Gulf war 1990": ("1990-07-16", "1990-10-11"),
    "LTCM 1998": ("1998-07-17", "1998-10-08"),
    "Dot-com 2000-02": ("2000-03-24", "2002-10-09"),
    "GFC 2007-09": ("2007-10-09", "2009-03-09"),
    "COVID 2020": ("2020-02-19", "2020-03-23"),
    "Inflation 2022": ("2022-01-03", "2022-10-12"),
}


def _cached(name: str, build):
    return cached_series(CACHE, name, build)


def load_prices(ticker: str, start: str) -> pd.Series:
    key = ticker.replace("^", "").lower()
    return _cached(f"sjm_{key}_daily.csv", lambda: download_daily_prices(ticker, start=start))


def load_riskfree() -> pd.Series:
    def build():
        url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=DTB3"
        raw = pd.read_csv(url)
        raw.columns = ["date", "rate"]
        raw["date"] = pd.to_datetime(raw["date"])
        raw["rate"] = pd.to_numeric(raw["rate"], errors="coerce")
        return raw.dropna().set_index("date")["rate"]

    return _cached("sjm_dtb3.csv", build)


def daily_riskfree(annual_percent: pd.Series, index: pd.DatetimeIndex) -> pd.Series:
    aligned = annual_percent.reindex(index.union(annual_percent.index)).ffill().reindex(index)
    return ((1.0 + aligned.bfill() / 100.0) ** (1.0 / TRADING_DAYS) - 1.0)


def run_jump_model(features: pd.DataFrame, oos_start: pd.Timestamp, lam: float) -> pd.Series:
    X = features.to_numpy()
    dates = features.index
    first = max(int(dates.searchsorted(oos_start)), TRAIN_DAYS)
    signal = pd.Series(np.nan, index=dates, dtype="float64")

    for block_start in range(first, len(dates), REFIT_DAYS):
        train = X[block_start - TRAIN_DAYS : block_start]
        mean = train.mean(axis=0)
        scale = train.std(axis=0)
        scale[scale == 0] = 1.0

        _, centroids, _ = fit_jump_model(
            (train - mean) / scale, k=2, jump_penalty=lam, n_init=10, seed=0
        )
        centroids = centroids[order_states_by(centroids, DOWNSIDE_FEATURE)]  # 0 = bull

        block_end = min(block_start + REFIT_DAYS, len(dates))
        window = (X[block_start - TRAIN_DAYS : block_end] - mean) / scale
        signal.iloc[block_start:block_end] = 1.0 - online_states(window, centroids, lam)[TRAIN_DAYS:]

    return signal


def backtest(returns: pd.Series, position: pd.Series, rf: pd.Series) -> dict:
    held = position.shift(EXECUTION_LAG).fillna(0.0)
    traded = held.diff().abs().fillna(held.abs())
    net = held * returns + (1.0 - held) * rf - traded * COST_ONE_WAY

    curve = (1.0 + net).cumprod()
    years = len(net) / TRADING_DAYS
    excess = net - rf
    downside = excess.clip(upper=0.0)

    return {
        "CAGR": curve.iloc[-1] ** (1.0 / years) - 1.0,
        "Vol": net.std() * np.sqrt(TRADING_DAYS),
        "Sharpe": excess.mean() / excess.std() * np.sqrt(TRADING_DAYS),
        "Sortino": excess.mean() / np.sqrt((downside**2).mean()) * np.sqrt(TRADING_DAYS),
        "MaxDD": (curve / curve.cummax() - 1.0).min(),
        "Turnover": traded.sum() / years,
        "TimeIn": held.mean(),
        "curve": curve,
        "net": net,
    }


def build_positions(ticker: str, start: str, oos_start: str, end: str | None, lam: float):
    prices = load_prices(ticker, start)
    returns = prices.pct_change().dropna()
    rf = daily_riskfree(load_riskfree(), returns.index)
    features = build_features((returns - rf).dropna())

    returns = returns.reindex(features.index)
    rf = rf.reindex(features.index)
    if end:
        keep = features.index <= pd.Timestamp(end)
        features, returns, rf = features[keep], returns[keep], rf[keep]
        prices = prices[prices.index <= pd.Timestamp(end)]

    signal = run_jump_model(features, pd.Timestamp(oos_start), lam)
    oos = signal.dropna().index
    if len(oos) == 0:
        raise SystemExit("Not enough history for the training window.")

    sma = prices.rolling(SMA_WINDOW).mean().reindex(oos)
    realized = returns.rolling(VOL_WINDOW).std().mul(np.sqrt(TRADING_DAYS)).reindex(oos)

    positions = {
        "Buy & hold": pd.Series(1.0, index=oos),
        "Jump model (0/1)": signal.reindex(oos),
        "200d moving average": (prices.reindex(oos) > sma).astype("float64"),
        "Vol target 10% cap": (VOL_TARGET / realized).clip(upper=1.0).fillna(0.0),
    }
    return positions, returns.reindex(oos), rf.reindex(oos), signal.reindex(oos), realized


def plot(results: dict, ticker: str, out: Path) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, (top, bottom) = plt.subplots(
        2, 1, figsize=(12, 8), sharex=True, gridspec_kw={"height_ratios": [2, 1]}
    )
    for name, stats in results.items():
        curve = stats["curve"]
        top.plot(curve.index, curve.to_numpy(), label=name, linewidth=1.2)
        bottom.fill_between(
            curve.index, (curve / curve.cummax() - 1.0).to_numpy() * 100, 0, alpha=0.35
        )
    top.set_yscale("log")
    top.set_ylabel("wealth (log scale, 1.0 at start)")
    top.set_title(f"{ticker}: jump-model reproduction against reactive incumbents")
    top.legend(loc="upper left", fontsize=9)
    top.grid(alpha=0.25)
    bottom.set_ylabel("drawdown (%)")
    bottom.grid(alpha=0.25)
    fig.tight_layout()
    out.parent.mkdir(exist_ok=True)
    fig.savefig(out, dpi=130)
    plt.close(fig)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ticker", default="^GSPC")
    parser.add_argument("--start", default="1970-01-01")
    parser.add_argument("--oos-start", default="1990-01-01")
    parser.add_argument("--end", default=None)
    parser.add_argument("--lam", type=float, default=LAMBDA)
    parser.add_argument("--no-plot", action="store_true")
    args = parser.parse_args()

    positions, r_oos, rf_oos, signal, realized = build_positions(
        args.ticker, args.start, args.oos_start, args.end, args.lam
    )
    oos = r_oos.index
    results = {name: backtest(r_oos, pos, rf_oos) for name, pos in positions.items()}

    print(f"\n{args.ticker}  out-of-sample {oos[0].date()} to {oos[-1].date()}  "
          f"({len(oos)} days, {len(oos)/TRADING_DAYS:.1f} years)")
    print(f"jump penalty {args.lam:g} (fixed, D1) | cost {COST_ONE_WAY*1e4:.0f}bp one-way "
          f"| execution lag {EXECUTION_LAG}d | 0/1 exposure\n")

    names = list(results)
    width = max(len(n) for n in names) + 2

    def row(label, values, fmt):
        print(f"{label:<22s}" + "".join(format(v, fmt).rjust(width) for v in values))

    print(f"{'':<22s}" + "".join(n.rjust(width) for n in names))
    print("-" * (22 + width * len(names)))
    row("CAGR", [results[n]["CAGR"] for n in names], ".1%")
    row("Volatility", [results[n]["Vol"] for n in names], ".1%")
    row("Sharpe", [results[n]["Sharpe"] for n in names], ".2f")
    row("Sortino", [results[n]["Sortino"] for n in names], ".2f")
    row("Max drawdown", [results[n]["MaxDD"] for n in names], ".1%")
    row("Turnover / yr", [results[n]["Turnover"] for n in names], ".0%")
    row("Time invested", [results[n]["TimeIn"] for n in names], ".0%")

    print("\nCDaR -- mean of the worst q% of drawdown days (whole curve, row 11)")
    for alpha in CDAR_ALPHAS:
        label = f"  worst {alpha:.0%}" if alpha < 1 else "  average (pain)"
        row(label, [cdar_curve(results[n]["curve"], (alpha,)).iloc[0] for n in names], ".1%")

    print("\nTime under water -- fraction of days below the running peak by more than")
    for threshold in UNDERWATER:
        row(f"  {threshold:.0%}", [time_under_water(results[n]["curve"], threshold) for n in names], ".1%")

    print("\nDrawdown within each episode, each strategy from its own peak inside the window")
    for label, (lo, hi) in EPISODES.items():
        if pd.Timestamp(lo) < oos[0] or pd.Timestamp(hi) > oos[-1]:
            continue
        row(f"  {label}", [depth_in_window(results[n]["curve"], lo, hi) for n in names], ".1%")

    print("\nCAGR by decade")
    decades = sorted({d.year // 10 * 10 for d in oos})
    for decade in decades:
        mask = (oos.year >= decade) & (oos.year < decade + 10)
        if mask.sum() < TRADING_DAYS // 2:
            continue
        values = []
        for n in names:
            seg = results[n]["net"][mask]
            values.append((1.0 + seg).prod() ** (TRADING_DAYS / len(seg)) - 1.0)
        row(f"  {decade}s ({mask.sum()//TRADING_DAYS}y)", values, ".1%")

    state = 1.0 - signal
    switches = int((state.diff().abs() > 0).sum())
    years = len(oos) / TRADING_DAYS
    print(f"\nregime switches {switches} over {years:.0f}y ({switches/years:.2f}/yr), "
          f"bear {state.mean():.1%} of days")

    rv = realized.dropna()
    common = state.dropna().index.intersection(rv.index)
    bear = rv.loc[common][state.loc[common] == 1.0].to_numpy()
    bull = rv.loc[common][state.loc[common] == 0.0].to_numpy()
    auc = float(np.mean([(bull < b).mean() + 0.5 * (bull == b).mean() for b in bear]))
    print(f"state vs trailing {VOL_WINDOW}d realized vol: bear {bear.mean():.1%}, "
          f"bull {bull.mean():.1%}, separation AUC {auc:.3f}")
    print("AUC near 1.0 means the state is a volatility meter (PROBLEM-MAP 0.9)\n")

    if not args.no_plot:
        out = ROOT / "figures" / f"sjm2024_{args.ticker.replace('^','').lower()}.png"
        plot(results, args.ticker, out)
        print(f"figure written: {out.relative_to(ROOT)}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
