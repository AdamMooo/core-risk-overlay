"""Regression checks for the CLOSED intervention program.

Frozen with the code they guard. These are the invariants E0, E1 and E4 rest
on -- the accounting switch, the roll-phase grid, and E4's payoff arithmetic.
They are kept runnable so the archived negatives stay reproducible; they are
not part of the active program's suite.

Plain-script smoke test (no pytest). Synthetic data, no network, deterministic.
Exits non-zero on failure.

Run from the repository root:
    .venv\Scripts\python.exe closed-research/intervention/checks.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import numpy as np
import pandas as pd

import anchoring as an
import hedge_economics as he

FAILURES: list[str] = []


def check(description: str, condition: bool) -> None:
    status = "PASS" if condition else "FAIL"
    print(f"[{status}] {description}")
    if not condition:
        FAILURES.append(description)


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


def check_anchoring_payoffs() -> None:
    """E4's payoff arithmetic. The only new arithmetic in the experiment.

    Every claim E4 makes reduces to the sign of these two numbers, so the
    identities they must satisfy are tested rather than assumed.
    """
    # 1. The m=0 dominance identity. sum of positive parts >= positive part of
    #    the sum, so WITHOUT a deductible the re-striking leg always wins. This
    #    is the whole mechanism: M1 exists only because of the deductible.
    path = np.array([100.0, 92.0, 97.0, 85.0, 80.0, 88.0, 91.0, 76.0, 70.0])
    anchored, restriking = an.payoffs(path, horizon=4, sub=1, moneyness=0.0)
    check(
        "anchoring: at m=0 the re-striking leg weakly dominates on every start",
        bool(np.all(restriking >= anchored - 1e-12)),
    )

    # 2. When every leg finishes in the money the difference is exactly the
    #    extra deductibles: P_A - P_R = m * (sum of re-strike levels - S_0).
    steep = np.array([100.0, 80.0, 64.0, 51.2, 40.96])
    anchored, restriking = an.payoffs(steep, horizon=4, sub=1, moneyness=0.10)
    expected = 0.10 * (steep[:4].sum() - steep[0])
    check(
        "anchoring: the payoff gap is exactly the extra deductibles",
        np.isclose(float(anchored[0] - restriking[0]), expected),
    )

    # 3. One sub-period IS the anchored contract. A degenerate case that would
    #    catch an off-by-one in the block loop.
    anchored, restriking = an.payoffs(path, horizon=4, sub=4, moneyness=0.10)
    check(
        "anchoring: sub == horizon makes the two legs identical",
        bool(np.allclose(anchored, restriking)),
    )

    # 4. The reversal case, and it is the reason E4 is an empirical question:
    #    a V-shape pays the short legs and expires the anchored one worthless.
    vshape = np.array([100.0, 70.0, 100.0, 100.0, 100.0])
    anchored, restriking = an.payoffs(vshape, horizon=4, sub=1, moneyness=0.10)
    check(
        "anchoring: a V-shape reverses the ordering (anchored pays nothing)",
        anchored[0] == 0.0 and restriking[0] > 0.0,
    )

    # 5. Nothing to insure, nothing paid.
    rising = np.array([100.0, 101.0, 102.0, 103.0, 104.0])
    anchored, restriking = an.payoffs(rising, horizon=4, sub=1, moneyness=0.10)
    check(
        "anchoring: a rising path pays zero on both legs",
        anchored[0] == 0.0 and restriking[0] == 0.0,
    )

    check(
        "anchoring: rejects a horizon longer than the sample",
        _raises(lambda: an.payoffs(rising, horizon=99, sub=4, moneyness=0.10)),
    )


def _raises(call) -> bool:
    try:
        call()
    except ValueError:
        return True
    return False


def main() -> None:
    check_mark_hedge_accounting()
    check_roll_phase()
    check_anchoring_payoffs()

    print()
    if FAILURES:
        print(f"{len(FAILURES)} check(s) FAILED:")
        for failure in FAILURES:
            print(f"  - {failure}")
        sys.exit(1)

    print("All checks passed.")


if __name__ == "__main__":
    main()
