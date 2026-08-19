r"""E1 -- the roll-phase sweep: is the tenor result an artifact of calendar alignment?

ACTIVE. Charter: ../CHARTER.md, experiment E1. Preregistration:
../docs/STUB-E1-ROLL-PHASE.md, committed 2026-08-18 before this file existed.
Every parameter, coordinate, threshold and verdict rule below was fixed there.

E1 DOES EXACTLY ONE THING. It varies the alignment of the roll grid against the
price path and reports how large the resulting spread is RELATIVE TO the tenor
effect it is supposed to qualify. It adds no hypothesis, no intervention class,
no data source and no criterion. It is a robustness test of an intervention
result, not a reopening of timing research: nothing here conditions on anything.

`simulate(..., phase=p)` is the whole implementation -- the first block is a stub
of p weeks, so rolls land at {p, p+tenor, ...} while the sample, the price path
and the naked book stay put. The naked baseline is therefore computed ONCE per
sample and shared by every phase.

WHY THE SPREAD IS NOT AN ERROR BAR, AND THIS IS THE POINT OF THE EXPERIMENT.
The 52 phases are 52 overlapping views of ONE crisis, deterministic functions of
one path. The spread is the sensitivity of a single-path statistic to an
arbitrary implementation choice -- NOT a sampling distribution. No standard
error, no confidence interval, no mean-across-phases quoted as an estimate. A
wide spread does not make the published number uncertain; it makes it ARBITRARY,
which is worse. Effective n on the benefit side is still 1.

Run: .venv\Scripts\python.exe research/phase_sweep.py [SPY]
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import numpy as np

import hedge_economics as he
import pathfunctionals as pf

# Stub §1. Fixed before the run; changing one now is selection on outcome.
TENORS = (4, 13, 26, 52)
MONEYNESS = 0.10
SLOPE = 0.6
SPREAD = 0.05
ALPHA = 0.05

# Stub §8. Verdict rules, not display choices.
SURVIVES = 1.0 / 3.0
KILLED = 1.0
EFFECT_FLOOR = 1.0  # pp

SUBSAMPLE_START = he.SUBSAMPLE_START


def bought(naked_dd, naked_cdar, spot, vix, tenor, phase, mark_hedge):
    """Drawdown bought versus the naked book, in both declared coordinates (pp).

    The third element is Psi, not Phi: the year the hedged book's max drawdown
    is set in. CHARTER §2 forbids reporting a Phi row without one, and here it
    is load-bearing -- if the hedged book's deepest episode is not the naked
    book's, then "bought" is a difference between two different episodes.
    """
    curve, _, _ = he.simulate(
        spot, vix, 1.00, MONEYNESS, tenor, SLOPE, SPREAD,
        mark_hedge=mark_hedge, phase=phase,
    )
    drawdown = pf.drawdown(curve)
    return (
        (naked_dd - drawdown.max()) * 100.0,
        (naked_cdar - pf.cdar(curve, ALPHA)) * 100.0,
        drawdown.idxmax().year,
    )


def sweep(spot, vix):
    """{(tenor, accounting): [(maxdd_pp, cdar_pp)] indexed by phase}."""
    naked, _, _ = he.simulate(spot, vix, 0.0, MONEYNESS, TENORS[0], SLOPE, SPREAD)
    naked_drawdown = pf.drawdown(naked)
    naked_dd = naked_drawdown.max()
    naked_cdar = pf.cdar(naked, ALPHA)
    naked_year = naked_drawdown.idxmax().year

    grid = {}
    for tenor in TENORS:
        for acct, mark in (("marked", True), ("cash", False)):
            grid[(tenor, acct)] = [
                bought(naked_dd, naked_cdar, spot, vix, tenor, p, mark)
                for p in range(tenor)
            ]
    return grid, naked_dd, naked_cdar, naked_year


def _col(grid, tenor, acct, coord):
    return np.array([row[coord] for row in grid[(tenor, acct)]])


def block_1_phase_grid():
    print("\n   1  PHASE GRID -- every offset, no selection")
    for tenor in TENORS:
        print(f"      {tenor:>2}w  offsets 0..{tenor - 1}   ({tenor} alignments)")


def block_23_by_phase(grid, acct, number):
    print(f"\n   {number}  {acct.upper()} -- drawdown bought (pp) at every phase")
    for tenor in TENORS:
        values = _col(grid, tenor, acct, 0)
        head = f"      {tenor:>2}w "
        for start in range(0, len(values), 13):
            chunk = "".join(f"{v:+7.1f}" for v in values[start:start + 13])
            print(f"{head if start == 0 else ' ' * len(head)}{chunk}")


def block_4_spread(grid):
    print("\n   4  PHASE RANGE AND SPREAD (pp).  median is a locator, NOT an estimate")
    print("      episode is Psi: the year the HEDGED book's max drawdown is set in,")
    print("      modal across phases. Where it is not the naked book's year, `bought`")
    print("      is a difference between two DIFFERENT episodes.")
    print(f"      {'tenor':>5} {'acct':>7} {'min':>8} {'median':>8} {'max':>8} {'spread':>8}"
          f"  {'episode':>14}")
    for tenor in TENORS:
        for acct in ("marked", "cash"):
            v = _col(grid, tenor, acct, 0)
            years = [row[2] for row in grid[(tenor, acct)]]
            top = max(set(years), key=years.count)
            print(f"      {tenor:>4}w {acct:>7} {v.min():>+8.1f} {np.median(v):>+8.1f}"
                  f" {v.max():>+8.1f} {v.max() - v.min():>8.1f}"
                  f"  {f'{top} ({years.count(top)}/{len(years)})':>14}")


def block_5_vs_effect(grid):
    """The one number E1 exists to produce, in both coordinates."""
    print("\n   5  SPREAD vs THE EFFECT.  effect = bought(52w) - bought(4w) at phase 0,")
    print("      the alignment E10 was published at.  R = spread(52w) / effect")
    print(f"      {'coord':>10} {'acct':>7} {'effect':>9} {'spread52':>9} {'R':>8}")

    out = {}
    for coord, label in ((0, "max DD"), (1, f"CDaR_{ALPHA:.2f}")):
        for acct in ("marked", "cash"):
            effect = (_col(grid, 52, acct, coord)[0] - _col(grid, 4, acct, coord)[0])
            col = _col(grid, 52, acct, coord)
            spread = col.max() - col.min()
            ratio = np.nan if abs(effect) < EFFECT_FLOOR else spread / effect
            shown = "     n/a" if np.isnan(ratio) else f"{ratio:8.2f}"
            print(f"      {label:>10} {acct:>7} {effect:>+9.1f} {spread:>9.1f} {shown}")
            out[(coord, acct)] = (effect, spread, ratio)
    return out


def block_6_verdict(grid, ratios):
    print("\n   6  VERDICT against the preregistered rule (stub §8)")
    for acct in ("marked", "cash"):
        effect, spread, ratio = ratios[(0, acct)]
        if np.isnan(ratio):
            verdict = f"INDETERMINATE -- |effect| {abs(effect):.1f}pp < {EFFECT_FLOOR:.1f}pp floor"
        elif ratio > KILLED:
            verdict = f"KILLED -- the phase spread EXCEEDS the whole tenor effect (R={ratio:.2f})"
        elif ratio <= SURVIVES:
            verdict = f"SURVIVES -- spread is small relative to the effect (R={ratio:.2f})"
        else:
            verdict = f"MARGINAL -- reported as marginal, not rounded (R={ratio:.2f})"
        print(f"      H2 phase clause, {acct:>6}:  {verdict}")

    print()
    for acct in ("marked", "cash"):
        lo52 = _col(grid, 52, acct, 0).min()
        hi4 = _col(grid, 4, acct, 0).max()
        sep = lo52 - hi4
        state = ("survives every alignment tested" if sep > 0
                 else "IS PHASE-DEPENDENT -- worst 52w does not beat best 4w")
        print(f"      ordering,      {acct:>6}:  separation {sep:+.1f}pp"
              f"  (min 52w {lo52:+.1f} vs max 4w {hi4:+.1f})  -- {state}")


def report(ticker: str = "SPY") -> None:
    spot, vix = he.load_inputs(ticker)

    print(f"\n{'=' * 92}")
    print(f"E1 -- ROLL-PHASE SWEEP.  {ticker}, {MONEYNESS:.0%} OTM, slope {SLOPE}, "
          f"offer +{SPREAD:.0%}, h=1.00")
    print("preregistered: docs/STUB-E1-ROLL-PHASE.md.  One question: is the tenor result")
    print("materially dependent on an arbitrary roll-calendar alignment?")
    print(f"{'=' * 92}")

    samples = {
        f"FULL SAMPLE {spot.index[0].date()} to {spot.index[-1].date()}": (spot, vix),
        f"SUBSAMPLE {SUBSAMPLE_START} onward (inherited, unchanged -- PARKED)": (
            spot[SUBSAMPLE_START:], vix[SUBSAMPLE_START:]
        ),
    }

    for i, (label, (s, v)) in enumerate(samples.items(), start=2):
        grid, naked_dd, naked_cdar, naked_year = sweep(s, v)
        print(f"\n\n{'=' * 92}")
        print(f"{i}. {label}")
        print(f"   naked book: maxDD {naked_dd:.1%} (set in {naked_year})"
              f"   CDaR_{ALPHA:.2f} {naked_cdar:.1%}")
        print(f"{'=' * 92}")
        block_1_phase_grid()
        block_23_by_phase(grid, "marked", 2)
        block_23_by_phase(grid, "cash", 3)
        block_4_spread(grid)
        ratios = block_5_vs_effect(grid)
        block_6_verdict(grid, ratios)

    print(f"\n{'=' * 92}")
    print("The spread is a SENSITIVITY of one path's statistic to an arbitrary choice.")
    print("It is not a sampling distribution: no standard error, no confidence interval,")
    print("no mean quoted as an estimate. Effective n on the benefit side is still 1.")


def main() -> None:
    args = sys.argv[1:]
    report(args[0].upper() if args else "SPY")


if __name__ == "__main__":
    main()
