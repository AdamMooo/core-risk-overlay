"""Regression checks for active infrastructure.

Covers src/data_loader.py -- the only module shared by the active
intervention-design program. The prediction program's checks live in
closed-research/checks.py and are frozen there.

Plain-script smoke test (no pytest). Synthetic data, no network, deterministic.
Exits non-zero on failure.

Run: .venv\Scripts\python.exe checks.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

import numpy as np
import pandas as pd

import data_loader as dl

FAILURES: list[str] = []


def check(description: str, condition: bool) -> None:
    status = "PASS" if condition else "FAIL"
    print(f"[{status}] {description}")
    if not condition:
        FAILURES.append(description)


def check_data_loader() -> None:
    prices = pd.Series(
        [100.0, 102.0, 101.0, 105.0],
        index=pd.date_range("2024-01-01", periods=4, freq="W-MON"),
    )
    returns = dl.compute_weekly_log_returns(prices)
    check("data_loader: log-return count is prices - 1", len(returns) == len(prices) - 1)
    check(
        "data_loader: log-return math matches np.log(p1/p0)",
        np.isclose(returns.iloc[0], np.log(102.0 / 100.0)),
    )

    for bad_prices in [pd.Series(dtype="float64"), pd.Series([1.0]), pd.Series([1.0, -1.0])]:
        try:
            dl.compute_weekly_log_returns(bad_prices)
            check(f"data_loader: rejects invalid input {bad_prices.tolist()}", False)
        except ValueError:
            check(f"data_loader: rejects invalid input {bad_prices.tolist()}", True)


def check_vix_alignment() -> None:
    index = pd.date_range("2024-01-01", periods=6, freq="W-MON")
    vix = pd.Series([13.0, 14.5, 22.0, 31.5, 18.0, 15.0], index=index)
    returns = pd.Series(np.linspace(-0.02, 0.02, 6), index=index)

    aligned = dl.align_vix_to_returns(vix, returns)
    check("data_loader: VIX aligns on an exact index match", aligned.index.equals(returns.index))
    check("data_loader: VIX alignment preserves values", bool(np.allclose(aligned, vix)))

    # The whole point of the exact join: a missing week must surface, never be
    # papered over with a stale carried-forward quote.
    for label, gap in [
        ("a missing week", vix.drop(index[2])),
        ("a shifted index", pd.Series(vix.to_numpy(), index=index + pd.Timedelta(days=1))),
    ]:
        try:
            dl.align_vix_to_returns(gap, returns)
            check(f"data_loader: VIX alignment rejects {label}", False)
        except ValueError:
            check(f"data_loader: VIX alignment rejects {label}", True)

    try:
        dl.align_vix_to_returns(vix.copy().mask(vix > 30, -1.0), returns)
        check("data_loader: VIX alignment rejects non-positive values", False)
    except ValueError:
        check("data_loader: VIX alignment rejects non-positive values", True)

    log_vix = dl.to_log_vix(aligned)
    check(
        "data_loader: to_log_vix matches np.log",
        bool(np.allclose(log_vix, np.log(vix))),
    )
    try:
        dl.to_log_vix(pd.Series([10.0, 0.0], index=index[:2]))
        check("data_loader: to_log_vix rejects non-positive values", False)
    except ValueError:
        check("data_loader: to_log_vix rejects non-positive values", True)


def main() -> None:
    check_data_loader()
    check_vix_alignment()

    print()
    if FAILURES:
        print(f"{len(FAILURES)} check(s) FAILED:")
        for failure in FAILURES:
            print(f"  - {failure}")
        sys.exit(1)

    print("All checks passed.")


if __name__ == "__main__":
    main()
