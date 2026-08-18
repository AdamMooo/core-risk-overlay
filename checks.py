"""Regression checks for active infrastructure.

Covers src/data_loader.py, research/pathfunctionals.py, and the two invariants
of research/hedge_economics.py:simulate that E0 and E1 rest on -- the accounting
switch and the roll-phase grid. The prediction program's checks live in
closed-research/checks.py and are frozen there.

Plain-script smoke test (no pytest). Synthetic data, no network, deterministic.
Exits non-zero on failure.

Run: .venv\Scripts\python.exe checks.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))
sys.path.insert(0, str(Path(__file__).parent / "research"))

import numpy as np
import pandas as pd

import data_loader as dl
import hedge_economics as he
import pathfunctionals as pf

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


def check_pathfunctionals() -> None:
    # Hand-built curve with two known excursions, the second still open.
    #   W        1.0   1.2   0.9    1.0     1.3   1.1     1.4    1.0
    #   cummax   1.0   1.2   1.2    1.2     1.3   1.3     1.4    1.4
    #   D        0     0     0.25   0.1667  0     0.1538  0      0.2857
    index = pd.date_range("2024-01-05", periods=8, freq="W-FRI")
    wealth = pd.Series([1.0, 1.2, 0.9, 1.0, 1.3, 1.1, 1.4, 1.0], index=index)

    d = pf.drawdown(wealth)
    check("pathfunctionals: drawdown is zero at a running peak", d.iloc[0] == 0.0 and d.iloc[4] == 0.0)
    check("pathfunctionals: drawdown depth matches 1 - W/M", np.isclose(d.iloc[2], 0.25))
    check("pathfunctionals: drawdown is positive-signed", bool((d >= 0).all()))

    for bad, label in [(pd.Series(dtype="float64"), "an empty curve"),
                       (pd.Series([1.0, 0.0]), "a non-positive curve")]:
        try:
            pf.drawdown(bad)
            check(f"pathfunctionals: drawdown rejects {label}", False)
        except ValueError:
            check(f"pathfunctionals: drawdown rejects {label}", True)

    ex = pf.excursions(wealth)
    check("pathfunctionals: finds every excursion", len(ex) == 3)
    check("pathfunctionals: excursion depth is its trough", np.isclose(ex[0].depth, 0.25))
    check("pathfunctionals: trough is dated, not just measured", ex[0].trough == index[2])
    check("pathfunctionals: duration is peak to trough", ex[0].duration == 1)
    check("pathfunctionals: recovery is trough to new high", ex[0].recovery == 1)
    check("pathfunctionals: a closed excursion is marked recovered", ex[0].recovered)
    # The censored one is the trap: it is still under water at the sample end,
    # so its recovery is a lower bound and must never be averaged in as a duration.
    check("pathfunctionals: an open excursion is marked NOT recovered", not ex[-1].recovered)

    deep = pf.excursions(wealth, threshold=0.20)
    check("pathfunctionals: threshold filters on depth", len(deep) == 2)

    # alpha=1 is the mean of the whole drawdown process; small alpha is max DD.
    check("pathfunctionals: CDaR at alpha=1 is the average drawdown",
          np.isclose(pf.cdar(wealth, 1.0), d.mean()))
    check("pathfunctionals: CDaR at small alpha is the max drawdown",
          np.isclose(pf.cdar(wealth, 0.01), d.max()))
    curve = pf.cdar_curve(wealth)
    check("pathfunctionals: CDaR is monotone non-increasing in alpha",
          bool((curve.to_numpy()[:-1] >= curve.to_numpy()[1:] - 1e-12).all()))
    check("pathfunctionals: CDaR rejects alpha outside (0, 1]", _raises(lambda: pf.cdar(wealth, 0.0)))

    check("pathfunctionals: time under water counts observations, not episodes",
          np.isclose(pf.time_under_water(wealth, 0.0), 4 / 8))
    check("pathfunctionals: time under water respects the threshold",
          np.isclose(pf.time_under_water(wealth, 0.20), 2 / 8))


def check_mark_hedge_accounting() -> None:
    """The E0 invariant: mark_hedge switches the ACCOUNTING, not the position.

    Everything E0 concludes rests on this. If the switch also moved contracts,
    premium or expiry payoff, the marked-versus-cash gap would be a difference
    between two programs rather than two views of one, and the decomposition
    would be a comparison instead.
    """
    # A path that falls hard mid-block, so the put is deep in the money between
    # roll dates -- exactly where the two accountings are meant to diverge.
    index = pd.date_range("2024-01-05", periods=41, freq="W-FRI")
    shock = np.concatenate([np.full(12, 0.004), np.full(10, -0.045), np.full(18, 0.010)])
    spot = pd.Series(100.0 * np.exp(np.concatenate([[0.0], shock.cumsum()])), index=index)
    vix = pd.Series(0.20, index=index)
    tenor = 8

    marked, prem_m, pay_m = he.simulate(spot, vix, 1.0, 0.10, tenor, 0.6, 0.05)
    cash, prem_c, pay_c = he.simulate(
        spot, vix, 1.0, 0.10, tenor, 0.6, 0.05, mark_hedge=False
    )

    bounds = list(range(0, len(spot) - 1, tenor)) + [len(spot) - 1]
    check(
        "hedge_economics: the two accountings agree at every roll boundary",
        bool(np.allclose(marked.to_numpy()[bounds], cash.to_numpy()[bounds], atol=1e-12)),
    )
    check(
        "hedge_economics: cash accounting leaves terminal wealth untouched",
        np.isclose(marked.iloc[-1], cash.iloc[-1], atol=1e-12),
    )
    check(
        "hedge_economics: cash accounting transacts identical premium and payoff",
        np.isclose(prem_m, prem_c, atol=1e-12) and np.isclose(pay_m, pay_c, atol=1e-12),
    )
    # A switch that silently did nothing would pass every check above.
    check(
        "hedge_economics: the two accountings DO differ inside a block",
        float((marked - cash).abs().max()) > 1e-6,
    )
    check(
        "hedge_economics: a mark is never negative, so cash never exceeds marked",
        bool((cash <= marked + 1e-12).all()),
    )
    unhedged_marked, _, _ = he.simulate(spot, vix, 0.0, 0.10, tenor, 0.6, 0.05)
    unhedged_cash, _, _ = he.simulate(
        spot, vix, 0.0, 0.10, tenor, 0.6, 0.05, mark_hedge=False
    )
    check(
        "hedge_economics: with no hedge the two accountings coincide everywhere",
        bool(np.allclose(unhedged_marked, unhedged_cash, atol=1e-12)),
    )


def check_roll_phase() -> None:
    """The E1 invariant: phase moves the ROLL GRID and nothing else.

    If phase also moved the sample, the start date or the naked baseline, the
    spread it produces would be a mixture of alignment and sample and would
    answer no question at all.
    """
    index = pd.date_range("2024-01-05", periods=41, freq="W-FRI")
    shock = np.concatenate([np.full(12, 0.004), np.full(10, -0.045), np.full(18, 0.010)])
    spot = pd.Series(100.0 * np.exp(np.concatenate([[0.0], shock.cumsum()])), index=index)
    vix = pd.Series(0.20, index=index)
    tenor = 8

    base, prem, pay = he.simulate(spot, vix, 1.0, 0.10, tenor, 0.6, 0.05)
    zero, prem0, pay0 = he.simulate(spot, vix, 1.0, 0.10, tenor, 0.6, 0.05, phase=0)
    check(
        "hedge_economics: phase=0 reproduces the unphased curve exactly",
        base.equals(zero) and prem == prem0 and pay == pay0,
    )
    wrapped, _, _ = he.simulate(spot, vix, 1.0, 0.10, tenor, 0.6, 0.05, phase=tenor)
    check("hedge_economics: phase=tenor is phase=0", base.equals(wrapped))

    shifted, _, _ = he.simulate(spot, vix, 1.0, 0.10, tenor, 0.6, 0.05, phase=3)
    # A phase parameter that silently did nothing would pass every other check.
    check(
        "hedge_economics: a non-zero phase DOES move the curve",
        float((base - shifted).abs().max()) > 1e-6,
    )

    # The design's precondition: the sample does not move, so the baseline the
    # sweep measures against is one baseline. Equality is to double precision --
    # re-basing shares at different boundaries reorders the rounding, nothing more.
    naked = [
        he.simulate(spot, vix, 0.0, 0.10, tenor, 0.6, 0.05, phase=p)[0]
        for p in range(tenor)
    ]
    check(
        "hedge_economics: the naked book is invariant to phase",
        all(bool(np.allclose(naked[0], n, atol=1e-12)) for n in naked[1:]),
    )

    # Rolls must land ON the phase. E0 proved the two accountings coincide only
    # at roll boundaries, so their agreement is a direct read of the grid.
    cash, _, _ = he.simulate(
        spot, vix, 1.0, 0.10, tenor, 0.6, 0.05, mark_hedge=False, phase=3
    )
    interior = (shifted.iloc[1:3] - cash.iloc[1:3]).abs().max()
    check(
        "hedge_economics: the first roll lands on the phase, not on the tenor",
        np.isclose(shifted.iloc[3], cash.iloc[3], atol=1e-12) and interior > 1e-9,
    )


def _raises(call) -> bool:
    try:
        call()
    except ValueError:
        return True
    return False


def main() -> None:
    check_data_loader()
    check_vix_alignment()
    check_pathfunctionals()
    check_mark_hedge_accounting()
    check_roll_phase()

    print()
    if FAILURES:
        print(f"{len(FAILURES)} check(s) FAILED:")
        for failure in FAILURES:
            print(f"  - {failure}")
        sys.exit(1)

    print("All checks passed.")


if __name__ == "__main__":
    main()
