"""The persistence-matched volatility-threshold incumbent -- the baseline the paper never ran.

VERIFICATION RUN, NOT A STRATEGY (the 0/1 rule is F9, PARKED section 4).

Design preregistered in docs/REPRO-SJM2024-FINDINGS.md ("Preregistered for the
volatility-threshold incumbent") before first execution. Exit to cash when
trailing 60d realized vol crosses above its trailing-3000d percentile p_exit;
re-enter when it falls below percentile p_reenter. The two-sided band is the
hysteresis that supplies persistence. Percentiles refit on the same 126-day
block schedule the jump model uses; same 10bp cost, execution lag, risk-free
leg. Three parameter pairs, all reported, none selected: (80,60), (75,55),
(85,65). The strategy starts invested.

Comparison set: buy & hold; the JM at fixed paper-25 (the headline run) and
fixed paper-35 (the sweep's best pain index); the three threshold variants.
The CV row is excluded until the D6 naming question is settled.

Run: .venv\\Scripts\\python.exe volthreshold.py
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))

from repro_sjm2024 import (
    REFIT_DAYS,
    TRADING_DAYS,
    TRAIN_DAYS,
    VOL_WINDOW,
    backtest,
    daily_riskfree,
    load_prices,
    load_riskfree,
    run_jump_model,
)
from src.pathfunctionals import cdar_curve, time_under_water
from src.sjm_features import build_features

PAIRS = ((80, 60), (75, 55), (85, 65))
JM_LAMBDAS_PAPER = (25.0, 35.0)
CDAR_ALPHAS = (0.01, 0.05, 0.10, 0.25, 0.50, 1.00)
ROOT = Path(__file__).resolve().parent


def threshold_signal(rv: pd.Series, oos_index: pd.DatetimeIndex,
                     p_exit: float, p_reenter: float) -> pd.Series:
    """0/1 hysteresis band on trailing realized vol, thresholds refit per block.

    The state at t uses rv through t and thresholds from data before the
    block -- the same information timing as the jump model's online state.
    """
    rv = rv.dropna()
    signal = pd.Series(np.nan, index=oos_index)
    invested = True
    positions = rv.index.get_indexer(oos_index)
    if (positions < 0).any():
        raise ValueError("OOS dates missing from the realized-vol series.")

    thr_hi = thr_lo = None
    for k, (date, pos) in enumerate(zip(oos_index, positions)):
        if k % REFIT_DAYS == 0:
            train = rv.iloc[max(0, pos - TRAIN_DAYS): pos]
            thr_hi = float(np.percentile(train, p_exit))
            thr_lo = float(np.percentile(train, p_reenter))
        level = rv.iloc[pos]
        if invested and level > thr_hi:
            invested = False
        elif not invested and level < thr_lo:
            invested = True
        signal.iloc[k] = 1.0 if invested else 0.0
    return signal


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ticker", default="^GSPC")
    parser.add_argument("--start", default="1970-01-01")
    parser.add_argument("--oos-start", default="1990-01-01")
    args = parser.parse_args()

    prices = load_prices(args.ticker, args.start)
    returns = prices.pct_change().dropna()
    rf = daily_riskfree(load_riskfree(), returns.index)
    features = build_features((returns - rf).dropna())
    returns = returns.reindex(features.index)
    rf = rf.reindex(features.index)

    rv = returns.rolling(VOL_WINDOW).std().mul(np.sqrt(TRADING_DAYS))

    jm_signals = {}
    for lam_paper in JM_LAMBDAS_PAPER:
        jm_signals[lam_paper] = run_jump_model(
            features, pd.Timestamp(args.oos_start), 2.0 * lam_paper
        ).dropna()
    oos_full = jm_signals[JM_LAMBDAS_PAPER[0]].index

    windows = {
        "paper window (to 2023-12-29)": oos_full[oos_full <= pd.Timestamp("2023-12-29")],
        "full sample": oos_full,
    }
    for label, oos in windows.items():
        rows = {"Buy & hold": pd.Series(1.0, index=oos)}
        for lam_paper in JM_LAMBDAS_PAPER:
            rows[f"JM fixed paper-{lam_paper:g}"] = jm_signals[lam_paper].reindex(oos)
        for p_exit, p_reenter in PAIRS:
            rows[f"RV band ({p_exit},{p_reenter})"] = threshold_signal(rv, oos, p_exit, p_reenter)

        r_oos, rf_oos = returns.reindex(oos), rf.reindex(oos)
        results = {name: backtest(r_oos, pos, rf_oos) for name, pos in rows.items()}

        print(f"\n{label}: {oos[0].date()} to {oos[-1].date()} "
              f"({len(oos)} days, {len(oos)/TRADING_DAYS:.1f} years)")
        header = f"{'':<22s}" + "".join(
            f"{c:>10s}" for c in ["CAGR", "Vol", "Sharpe", "MaxDD", "Turnover", "TimeIn", "TuW10%"]
        )
        print(header)
        print("-" * len(header))
        for name, stats in results.items():
            tuw = time_under_water(stats["curve"], 0.10)
            print(f"{name:<22s}"
                  f"{stats['CAGR']:>10.1%}{stats['Vol']:>10.1%}{stats['Sharpe']:>10.2f}"
                  f"{stats['MaxDD']:>10.1%}{stats['Turnover']:>10.0%}{stats['TimeIn']:>10.0%}"
                  f"{tuw:>10.1%}")

        print("\nCDaR -- mean of the worst q% of drawdown days (whole curve, row 11)")
        print(f"{'':<22s}" + "".join(
            (f"{a:>9.0%}" if a < 1 else f"{'pain':>9s}") for a in CDAR_ALPHAS))
        for name, stats in results.items():
            curve = cdar_curve(stats["curve"], CDAR_ALPHAS)
            print(f"{name:<22s}" + "".join(f"{v:>9.1%}" for v in curve))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
