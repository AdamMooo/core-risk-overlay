r"""E2 -- the drawdown path: does any tenor ordering survive off the maximum?

ACTIVE. Charter: ../CHARTER.md, experiment E2. Preregistration:
../docs/STUB-E2-DRAWDOWN-PATH.md, committed 2026-08-18 before this file existed.
Every coordinate, threshold, grid and verdict rule below was fixed there.

THE ESTIMAND PROBLEM THIS REPAIRS. E1 showed that `max(D)` on the hedged path and
`max(D)` on the naked path routinely describe DIFFERENT EPISODES -- at 52w on the
full sample, 2003 versus 2009, in 51 of 52 alignments. "Drawdown bought" was a
difference between two unrelated events, and protection past the second-deepest
episode was invisible. Max drawdown is censored from below by the next-deepest
episode.

TWO REPAIRS, AND THEY ARE THE WHOLE EXPERIMENT.

  CDaR(worst q%)      the occupation-measure tail mean of D. It integrates over
                      the whole path, so it cannot be pinned to one instant, and
                      its dependence on q measures how much rests on one episode.

  EPISODE-MATCHED     episodes are defined ONCE, on the NAKED book, and both
  DEPTHS              books are measured inside the SAME calendar windows, each
                      from its own peak within the window.

Defining episodes on the naked book is load-bearing: windows derived from the
hedged path would move with the intervention, breaking the estimand in a new way
rather than repairing it.

CONVENTION. `q` is OURS -- the fraction of the process averaged. Chekhlov,
Uryasev & Zabarankin parameterise by a confidence level, so our q=0.05 is their
0.95-CDaR. Read before this run, not after: MATH-REFERENCE §4.1. Every label
below says `worst q%` for that reason.

WHAT THE COUNTS ARE NOT. Phases are not independent and episodes are not
exchangeable. The sign-consistency fractions are counts of a deterministic
sensitivity, not proportions with standard errors. No test statistic is computed
here and none may be derived from these numbers.

Run: .venv\Scripts\python.exe research/path_outcomes.py [SPY]
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import numpy as np

import hedge_economics as he
import pathfunctionals as pf

# Stub §1. Fixed before the run.
Q_GRID = (0.01, 0.05, 0.10, 0.25, 0.50, 1.00)
EPISODE_THRESHOLDS = (0.10, 0.20)
PRIMARY_THRESHOLD = 0.10
TENORS = (4, 13, 26, 52)
MONEYNESS = 0.10
SLOPE = 0.6
SPREAD = 0.05

# Stub §8. Verdict rules.
V2_SURVIVES = 2.0 / 3.0
V2_KILLED = 0.5

SUBSAMPLE_START = he.SUBSAMPLE_START
ACCOUNTINGS = (("marked", True), ("cash", False))


def episode_of(date, windows):
    """Index of the naked episode containing `date`, or None."""
    for i, (start, end) in enumerate(windows):
        if start <= date <= end:
            return i
    return None


def tail_episodes(curve, q, windows):
    """Psi: how many distinct naked episodes the worst q% of D falls inside."""
    d = pf.drawdown(curve)
    k = max(1, int(np.ceil(q * len(d))))
    dates = d.sort_values(ascending=False).index[:k]
    hits = {episode_of(t, windows) for t in dates}
    outside = None in hits
    return len(hits - {None}), outside


def measure(curve, naked_cdar, naked_depths, windows):
    """One hedged curve reduced to E2's two coordinates, in pp."""
    return {
        "cdar": {q: (naked_cdar[q] - pf.cdar(curve, q)) * 100.0 for q in Q_GRID},
        "episodes": {
            thr: [
                (naked_depths[thr][i] - pf.depth_in_window(curve, start, end)) * 100.0
                for i, (start, end) in enumerate(windows[thr])
            ]
            for thr in EPISODE_THRESHOLDS
        },
    }


def build(spot, vix):
    naked, _, _ = he.simulate(spot, vix, 0.0, MONEYNESS, TENORS[0], SLOPE, SPREAD)
    naked_cdar = {q: pf.cdar(naked, q) for q in Q_GRID}
    excursions = {thr: pf.excursions(naked, thr) for thr in EPISODE_THRESHOLDS}
    windows = {thr: [(e.start, e.end) for e in excursions[thr]] for thr in EPISODE_THRESHOLDS}
    naked_depths = {thr: [e.depth for e in excursions[thr]] for thr in EPISODE_THRESHOLDS}

    grid, curves0 = {}, {}
    for tenor in TENORS:
        for acct, mark in ACCOUNTINGS:
            rows = []
            for p in range(tenor):
                curve, _, _ = he.simulate(
                    spot, vix, 1.00, MONEYNESS, tenor, SLOPE, SPREAD,
                    mark_hedge=mark, phase=p,
                )
                if p == 0:
                    curves0[(tenor, acct)] = curve
                rows.append(measure(curve, naked_cdar, naked_depths, windows))
            grid[(tenor, acct)] = rows
    return grid, naked, naked_cdar, excursions, windows, curves0


def block_1(naked, naked_cdar, excursions):
    print("\n   1  THE MEASURING APPARATUS, all of it declared in the stub")
    print(f"      q grid (fraction of the process averaged; CUZ's alpha is 1-q):"
          f" {', '.join(f'{q:.2f}' for q in Q_GRID)}")
    print(f"      naked CDaR(worst q%):  "
          + "  ".join(f"{q:.0%}={naked_cdar[q]:.1%}" for q in Q_GRID))
    print(f"      phases: every offset 0..tau-1 for tau in {TENORS}")
    for thr in EPISODE_THRESHOLDS:
        eps = excursions[thr]
        print(f"\n      episodes on the NAKED book, threshold {thr:.0%}: n = {len(eps)}")
        for i, e in enumerate(eps):
            flag = "" if e.recovered else "   [CENSORED: still under water at sample end]"
            print(f"        {i}  {e.start.date()} -> {e.end.date()}"
                  f"   trough {e.trough.date()}  depth {e.depth:>5.1%}{flag}")


def block_2(grid):
    print("\n   2  CDaR(worst q%) REDUCTION vs the naked book (pp), phase 0")
    print(f"      {'tenor':>5} {'acct':>7}" + "".join(f"{q:>10.0%}" for q in Q_GRID))
    for tenor in TENORS:
        for acct, _ in ACCOUNTINGS:
            row = grid[(tenor, acct)][0]["cdar"]
            print(f"      {tenor:>4}w {acct:>7}"
                  + "".join(f"{row[q]:>+10.1f}" for q in Q_GRID))


def block_3(grid):
    """V1: does the ordering survive at q, at EVERY alignment?"""
    print("\n   3  V1 -- separation(q) = min over phases of 52w  -  max over phases of 4w")
    print("      positive means the ordering survives that q at every alignment tested")
    print(f"      {'acct':>7}" + "".join(f"{q:>10.0%}" for q in Q_GRID))

    surviving = {}
    for acct, _ in ACCOUNTINGS:
        cells, ok = [], []
        for q in Q_GRID:
            lo = min(r["cdar"][q] for r in grid[(52, acct)])
            hi = max(r["cdar"][q] for r in grid[(4, acct)])
            cells.append(f"{lo - hi:>+10.1f}")
            if lo - hi > 0:
                ok.append(q)
        surviving[acct] = ok
        print(f"      {acct:>7}" + "".join(cells))
    for acct, _ in ACCOUNTINGS:
        got = surviving[acct]
        print(f"      ordering survives, {acct:>6}:  "
              + (", ".join(f"q={q:.0%}" for q in got) if got else "NOWHERE"))
    return surviving


def block_4(grid, excursions, thr):
    print(f"\n   4  EPISODE-MATCHED DEPTH REDUCTION (pp), phase 0, threshold {thr:.0%}")
    print("      each book measured inside the NAKED book's window, from its own peak in it")
    eps = excursions[thr]
    print(f"      {'episode':>26} {'naked':>7}" +
          "".join(f"{f'{t}w {a}':>13}" for t in (4, 52) for a, _ in ACCOUNTINGS))
    for i, e in enumerate(eps):
        cells = "".join(
            f"{grid[(t, a)][0]['episodes'][thr][i]:>+13.1f}"
            for t in (4, 52) for a, _ in ACCOUNTINGS
        )
        print(f"      {f'{e.start.date()}..{e.end.date()}':>26} {e.depth:>7.1%}{cells}")


def block_5(grid, thr):
    """V2 and V3, across every alignment of both tenors."""
    print(f"\n   5  V2 / V3 -- sign consistency over (episode x 52w-phase x 4w-phase),"
          f" threshold {thr:.0%}")
    print("      counts of a deterministic sensitivity. NOT proportions, no standard errors.")

    out = {}
    for acct, _ in ACCOUNTINGS:
        long_rows = [r["episodes"][thr] for r in grid[(52, acct)]]
        short_rows = [r["episodes"][thr] for r in grid[(4, acct)]]
        n_ep = len(long_rows[0])

        wins = total = 0
        for i in range(n_ep):
            for a in long_rows:
                for b in short_rows:
                    wins += a[i] >= b[i]
                    total += 1
        v2 = wins / total

        positive = sum(a[i] > 0 for i in range(n_ep) for a in long_rows)
        v3 = positive / (n_ep * len(long_rows))

        out[acct] = (v2, v3)
        print(f"      {acct:>7}:  V2  52w >= 4w in {wins}/{total} = {v2:>5.1%}"
              f"     V3  52w reduces depth at all in "
              f"{positive}/{n_ep * len(long_rows)} = {v3:>5.1%}")
    return out


def block_6(curves0, naked, windows, excursions):
    print("\n   6  PSI attached to every Phi above")
    thr = PRIMARY_THRESHOLD
    print(f"      episodes contributing to the worst q% of the drawdown process, phase 0")
    print(f"      (effective n of the CDaR coordinate: 1 means it has collapsed onto one event)")
    print(f"      {'curve':>14}" + "".join(f"{q:>10.0%}" for q in Q_GRID))
    rows = [("naked", naked)] + [
        (f"{t}w {a}", curves0[(t, a)]) for t in (26, 52) for a, _ in ACCOUNTINGS
    ]
    for label, curve in rows:
        cells = []
        for q in Q_GRID:
            n, outside = tail_episodes(curve, q, windows[thr])
            cells.append(f"{n}{'+' if outside else '':>1}".rjust(10))
        print(f"      {label:>14}" + "".join(cells))
    print("      ('+' means part of the tail lies outside every episode window)")
    print(f"      episodes: n = {len(excursions[thr])} at {thr:.0%},"
          f" {len(excursions[EPISODE_THRESHOLDS[1]])} at {EPISODE_THRESHOLDS[1]:.0%};"
          f" censored = {sum(not e.recovered for e in excursions[thr])}")
    print(f"      phases: {sum(TENORS)} alignments per accounting."
          f"  Effective n on the benefit side: still 1.")


def block_7(surviving, v_counts):
    print("\n   7  VERDICTS against the preregistered rules (stub §8)")
    for acct, _ in ACCOUNTINGS:
        got = surviving[acct]
        where = ", ".join(f"{q:.0%}" for q in got) if got else "no q"
        print(f"      V1  ordering, {acct:>6}:  survives at {where}"
              f"  ({len(got)}/{len(Q_GRID)} of the curve)")
    for thr in EPISODE_THRESHOLDS:
        for acct, _ in ACCOUNTINGS:
            v2, v3 = v_counts[thr][acct]
            verdict = ("SURVIVES" if v2 >= V2_SURVIVES
                       else "KILLED" if v2 <= V2_KILLED else "MARGINAL")
            print(f"      V2  episodes @{thr:.0%}, {acct:>6}:  {v2:>5.1%}  {verdict}"
                  f"     V3 depth reduced in {v3:.1%} of pairs")


def report(ticker: str = "SPY") -> None:
    spot, vix = he.load_inputs(ticker)

    print(f"\n{'=' * 96}")
    print(f"E2 -- THE DRAWDOWN PATH.  {ticker}, {MONEYNESS:.0%} OTM, slope {SLOPE}, "
          f"offer +{SPREAD:.0%}, h=1.00")
    print("preregistered: docs/STUB-E2-DRAWDOWN-PATH.md.  One question: does ANY tenor")
    print("ordering survive when the outcome is measured across the drawdown path?")
    print(f"{'=' * 96}")

    samples = {
        f"FULL SAMPLE {spot.index[0].date()} to {spot.index[-1].date()}": (spot, vix),
        f"SUBSAMPLE {SUBSAMPLE_START} onward (inherited, unchanged)": (
            spot[SUBSAMPLE_START:], vix[SUBSAMPLE_START:]
        ),
    }

    for i, (label, (s, v)) in enumerate(samples.items(), start=2):
        grid, naked, naked_cdar, excursions, windows, curves0 = build(s, v)
        print(f"\n\n{'=' * 96}")
        print(f"{i}. {label}")
        print(f"{'=' * 96}")
        block_1(naked, naked_cdar, excursions)
        block_2(grid)
        surviving = block_3(grid)
        block_4(grid, excursions, PRIMARY_THRESHOLD)
        v_counts = {thr: block_5(grid, thr) for thr in EPISODE_THRESHOLDS}
        block_6(curves0, naked, windows, excursions)
        block_7(surviving, v_counts)

    print(f"\n{'=' * 96}")
    print("Max drawdown is not the primary statistic anywhere above. Every number is a")
    print("description of ONE realized path: no standard errors, no population claim.")


def main() -> None:
    args = sys.argv[1:]
    report(args[0].upper() if args else "SPY")


if __name__ == "__main__":
    main()
