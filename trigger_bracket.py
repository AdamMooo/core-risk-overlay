"""What fraction of the clairvoyant prize does a real trigger actually capture?

hedge_economics.py produced a bracket with nothing in it: always-on at the
bottom, perfect foresight at the top, and every possible overlay somewhere
between. This puts real points in it.

THE ASYMMETRY IS THE POINT, AND IT CHANGES THE METRIC. A put payoff is convex
-- lose a little often, win a lot rarely. Always-on eats every small loss to
reach the rare wins, and what it pays for that is the variance risk premium.
Clairvoyance eats none of them. So a trigger is NOT scored on how often it is
right. It is scored on

    payoff captured / premium spent

which is why a rule can be wrong most of the time and still win. This is a
distributional and economic property, not a directional one, so it does not
reimport the crash-prediction yardstick README 2 rejects.

Every rule is strictly point-in-time. Level rules need no estimation at all
(VIX 20 is VIX 20). Percentile rules use an EXPANDING window with a 104-week
burn-in, so no quantile is ever computed from the future.

THE DIAGNOSTIC THAT MATTERS MOST is not any rule's score. It is the entry-VIX
distribution of the blocks the clairvoyant program chooses, printed first. High
implied vol means insurance is EXPENSIVE, so:

  clairvoyant blocks have HIGH entry VIX  ->  "hedge when VIX is high" can work
  clairvoyant blocks have LOW entry VIX   ->  the payoff is bought BEFORE the
                                              market reprices, every reactive
                                              rule is structurally too late,
                                              and the whole lag thesis is
                                              confirmed rather than argued

--- protocol 0 stub -----------------------------------------------------------

1. CLAIM TUPLE   weekly * 4- and 13-week blocks * CAGR and max drawdown *
                 SPY 1993-2026. Descriptive placement inside a bracket. No
                 significance is tested and none is claimed.

2. PREDICTION    Reactive VIX rules capture a MINORITY of the ceiling, because
                 VIX rises on the same information the payoff needs and the
                 premium reprices with it. The cheap-vol rule is the interesting
                 one precisely because it inverts that.

3. LITERATURE    The variance risk premium (Carr & Wu 2009; Bollerslev, Tauchen
                 & Zhou 2009) is why always-on loses. Not re-derived here.

4. MECHANISM     Not a two-estimator comparison, so 0.4 does not bind. The
                 bracket is the comparison and every rule is placed in it.

5. SURPRISE      A rule capturing a large fraction of the ceiling would justify
                 an overlay outright. Near-zero capture across every rule says
                 the prize is real but unreachable by anything reactive, which
                 is a decision to stop.

MULTIPLE COMPARISONS, STATED NOT HIDDEN. Eight rules are run and ALL are
reported -- no winner is selected. The whole sample rests on roughly five
systemic episodes (1998, 2000-02, 2008, 2020, 2022) whatever the block count
says, so any apparent winner here is one of eight picked on an effective n
near five. This is a bracket-placement exercise, not evidence.

Run: .venv\\Scripts\\python.exe trigger_bracket.py [SPY]
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

import numpy as np
import pandas as pd

from hedge_economics import (
    SUBSAMPLE_START,
    load_inputs,
    simulate,
    summarize,
)

SKEW_SLOPE = 0.60
SPREAD = 0.05
BURN_IN = 104
CONFIGS = ((0.05, 4), (0.10, 13))


def level_trigger(vix, threshold):
    return (vix * 100.0) > threshold


def percentile_trigger(vix, quantile, above=True):
    rank = vix.expanding(min_periods=BURN_IN).apply(
        lambda window: float((window[-1] >= window).mean()), raw=True
    )
    fires = rank >= quantile if above else rank <= quantile
    return fires.fillna(False)


def build_rules(vix):
    rules = {}
    for threshold in (15, 20, 25, 30):
        rules[f"VIX > {threshold}"] = level_trigger(vix, threshold)
    for quantile in (0.50, 0.75, 0.90):
        rules[f"VIX top {1 - quantile:.0%} expanding"] = percentile_trigger(
            vix, quantile
        )
    rules["VIX bottom 50% (cheap vol)"] = percentile_trigger(vix, 0.50, above=False)
    return rules


def clairvoyant_entry_vix(spot, vix, moneyness, tenor):
    """Entry VIX of blocks the clairvoyant program buys, versus all blocks."""
    curve, _, _ = simulate(
        spot, vix, 1.00, moneyness, tenor, SKEW_SLOPE, SPREAD, foresight=True
    )
    prices = spot.to_numpy()
    chosen, every = [], []
    start = 0
    n = len(prices)
    while start < n - 1:
        end = min(start + tenor, n - 1)
        strike = prices[start] * (1.0 - moneyness)
        every.append(vix.iloc[start] * 100.0)
        if max(strike - prices[end], 0.0) > 0.0:
            chosen.append(vix.iloc[start] * 100.0)
        start = end
    return np.array(chosen), np.array(every), curve


def report(ticker: str = "SPY") -> None:
    spot, vix = load_inputs(ticker)

    for label, (s, v) in {
        f"FULL SAMPLE {spot.index[0].date()} to {spot.index[-1].date()}": (spot, vix),
        f"SUBSAMPLE {SUBSAMPLE_START} onward": (
            spot[SUBSAMPLE_START:],
            vix[SUBSAMPLE_START:],
        ),
    }.items():
        rules = build_rules(v)
        print(f"\n{'=' * 96}\n{label}   |   skew slope {SKEW_SLOPE}, offer = mid + {SPREAD:.0%}")
        print(f"{'=' * 96}")

        for moneyness, tenor in CONFIGS:
            naked_curve, _, _ = simulate(s, v, 0.0, moneyness, tenor, SKEW_SLOPE, SPREAD)
            naked = summarize(naked_curve, 0.0, 0.0)

            chosen, every, _ = clairvoyant_entry_vix(s, v, moneyness, tenor)
            print(f"\n{moneyness:.0%} OTM, {tenor}-week roll")
            print(
                f"  DIAGNOSTIC -- entry VIX where the put finished in the money:"
                f" median {np.median(chosen):.1f} over {len(chosen)} blocks"
            )
            print(
                f"              entry VIX across all blocks:"
                f" median {np.median(every):.1f} over {len(every)} blocks"
            )

            rows = []
            for name, trigger in (
                ("always on", None),
                *rules.items(),
                ("CLAIRVOYANT", "foresight"),
            ):
                foresight = isinstance(trigger, str)
                curve, premium, payoff = simulate(
                    s, v, 1.00, moneyness, tenor, SKEW_SLOPE, SPREAD,
                    foresight=foresight,
                    trigger=None if foresight else trigger,
                )
                stats = summarize(curve, premium, payoff)
                stats["name"] = name
                stats["hedged_pct"] = (
                    curve.attrs["blocks_hedged"] / curve.attrs["blocks_total"]
                )
                stats["capture"] = (
                    payoff / premium if premium > 1e-9 else float("nan")
                )
                rows.append(stats)

            table = pd.DataFrame(rows).set_index("name")
            floor = table.loc["always on"]
            ceiling = table.loc["CLAIRVOYANT"]
            span_cagr = ceiling["cagr"] - floor["cagr"]
            span_dd = ceiling["max_drawdown"] - floor["max_drawdown"]

            print(
                f"\n  {'rule':<28s} {'CAGR':>7s} {'maxDD':>7s} {'on%':>5s} "
                f"{'pay/prem':>9s} {'EVPI captured':>16s}"
            )
            print(f"  {'naked (no hedge)':<28s} {naked['cagr']:+7.2%} "
                  f"{naked['max_drawdown']:+7.1%} {'--':>5s} {'--':>9s} {'--':>16s}")
            for name, row in table.iterrows():
                pos_cagr = (row["cagr"] - floor["cagr"]) / span_cagr
                pos_dd = (row["max_drawdown"] - floor["max_drawdown"]) / span_dd
                marker = "  <--" if name == "CLAIRVOYANT" else ""
                print(
                    f"  {name:<28s} {row['cagr']:+7.2%} {row['max_drawdown']:+7.1%} "
                    f"{row['hedged_pct']:5.0%} {row['capture']:9.2f} "
                    f"  {pos_cagr:5.0%} ret {pos_dd:5.0%} dd{marker}"
                )

    print(f"\n{'=' * 96}")
    print("pay/prem: dollars of payoff per dollar of premium. Above 1.00 the hedge")
    print("made money outright. EVPI captured: position in the bracket, 0% = always")
    print("on, 100% = perfect foresight, separately for return and for drawdown.")


def main() -> None:
    report(sys.argv[1].upper() if len(sys.argv) > 1 else "SPY")


if __name__ == "__main__":
    main()
