"""What is the best hedge STRUCTURE, given no signal at all?

This is the first experiment written for the LIVE HEDGE rather than for the
research question, and the scope boundary in README 2 -- "the model answers
when, never what to buy or how much" -- is deliberately set aside. The reason is
arithmetic, not preference. Everything inside that boundary has now been
measured as nearly worthless: a CLAIRVOYANT trigger is worth ~+3pp/yr, real VIX
rules capture 4-7% of that, and no rule beat simply not hedging on return.
Everything that moved the numbers was outside it -- correcting the equity skew
alone took hedge efficiency from 17.58 to 3.6.

THE ASYMMETRY THAT MOTIVATES THE WHOLE DESIGN. Premium drag is measurable to
high precision: it is paid every roll, thousands of times, over thirty years.
Timing benefit depends on ~10-15 systemic drawdowns in all of SPY history and is
structurally unmeasurable -- the wall this repo has now hit from three unrelated
directions (containment, the trigger bracket, and the absorption ratio's
effective sample size of ~6). So build the side that can be measured. That means
holding the signal FIXED and sweeping structure, which is the exact opposite of
everything attempted here so far.

--- protocol 0 stub, fixed before the run -------------------------------------

1. CLAIM TUPLE   weekly marks * full holding period * geometric return and max
                 drawdown * SPY 1993-2026, subsample 2003-2026 * ALWAYS-ON,
                 h=1.00, NO signal and NO timing anywhere in the design. No
                 claim is made about any measure, indicator or regime state.

2. PREDICTION    (a) NO structure beats the naked book on CAGR. README 2's
                 inequality fails on average at every point in this grid;
                 Ilmanen (2012) is the skeptical prior and the repo has already
                 measured h=0 winning on return.
                 (b) Efficiency is maximised at LONG tenor and DEEP strike --
                 52 weeks, 20-30% OTM. Skew scales as sqrt(4/tenor) in
                 `skewed_vol`, so long-dated is far cheaper per unit of calendar
                 time, and deep OTM is where tail insurance actually lives.
                 (c) PUT SPREADS cut cost more than a flat surface implies,
                 because the short leg sits deeper on the skew and is sold rich.
                 But they cap the payoff exactly in the deep tail the program
                 exists for, so they should look good on premium and bad on
                 drawdown bought -- efficiency a wash or worse.

3. LITERATURE    Ilmanen (2012) on the cost of index put protection. Israelov
                 (2017), "Pathetic Protection", on rolled-put drag specifically.
                 Both [UNREAD] and recorded as such -- the 2026-08-14 lesson is
                 that an [UNREAD] tag on the paper whose construction you need
                 is itself the defect.

4. MECHANISM     Not a comparison of estimators. A cost characterisation of a
                 DECISION whose cost side has ~1700 weekly observations and
                 whose benefit side has ~10. Only the first is being measured.

5. SURPRISE      A structure beating naked on CAGR ends the signal program
                 outright -- buy it and stop. Efficiency flat across the grid
                 means structure does not matter either, and the honest answer
                 for real money becomes "do not hedge with options". A strong
                 interior optimum is the first actionable result in the repo.

WHAT THIS RUN DOES NOT COVER, stated so it is not mistaken for complete:
  - RECYCLING. README 1 monetises the hedge in a crash and buys the core back
    lower. `simulate` reinvests the payoff at the next roll, which is a passive
    version of that. Sizing the buyback deliberately is untested and may matter
    more than any strike choice here.
  - THE HONEST COMPETITORS. A trend-following sleeve or long duration are what a
    real book would use instead of puts, and they carry positive or neutral
    carry rather than bleed. Not compared. Doing so needs data this repo lacks.

Run: .venv\\Scripts\\python.exe structure_map.py [SPY] [--slope 0.6]
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

import pandas as pd

import hedge_economics as he

TENORS = (4, 13, 26, 52)
MONEYNESS = (0.05, 0.10, 0.15, 0.20, 0.30)
SPREAD_WIDTH = 0.10
PRIMARY_SLOPE = 0.6
SLOPE_SENSITIVITY = (0.0, 0.4, 0.8)
SUBSAMPLE_START = "2003-01-24"


def grid(spot, vix, slope, spread, hedge_ratio=1.00):
    naked, _, _ = he.simulate(spot, vix, 0.0, 0.10, 4, 0.0, spread)
    base = he.summarize(naked, 0.0, 0.0)

    rows = []
    for tenor in TENORS:
        for moneyness in MONEYNESS:
            for short in (0.0, moneyness + SPREAD_WIDTH):
                curve, premium, payoff = he.simulate(
                    spot, vix, hedge_ratio, moneyness, tenor, slope, spread,
                    short_moneyness=short,
                )
                row = he.summarize(curve, premium, payoff)
                cost = (base["cagr"] - row["cagr"]) * 100
                bought = (row["max_drawdown"] - base["max_drawdown"]) * 100
                rows.append({
                    "tenor": tenor,
                    "otm": moneyness,
                    "structure": f"spread/{short:.0%}" if short else "outright",
                    "cagr": row["cagr"],
                    "maxdd": row["max_drawdown"],
                    "cost_pp": cost,
                    "dd_bought_pp": bought,
                    "efficiency": bought / cost if cost > 1e-9 else float("nan"),
                    "drag_pa": row["premium_drag_pa"],
                })
    return pd.DataFrame(rows), base


def show(frame, base, label):
    print(f"\n{'=' * 100}\n{label}")
    print(f"naked book: CAGR {base['cagr']:+.2%}   maxDD {base['max_drawdown']:+.1%}")
    print(f"{'=' * 100}")
    print(f"  {'tenor':>5s} {'OTM':>5s} {'structure':<13s} {'CAGR':>8s} "
          f"{'maxDD':>8s} {'cost':>7s} {'ddBought':>9s} {'eff':>7s}")
    for _, r in frame.sort_values("efficiency", ascending=False).iterrows():
        print(f"  {r['tenor']:5.0f}w {r['otm']:5.0%} {r['structure']:<13s} "
              f"{r['cagr']:+8.2%} {r['maxdd']:+8.1%} {r['cost_pp']:7.2f} "
              f"{r['dd_bought_pp']:+9.1f} {r['efficiency']:7.2f}")

    beats = frame[frame["cagr"] > base["cagr"]]
    print(f"\n  structures beating the naked book on CAGR: {len(beats)} of {len(frame)}")
    if len(beats):
        for _, r in beats.iterrows():
            print(f"    {r['tenor']:.0f}w {r['otm']:.0%} {r['structure']} "
                  f"-> {r['cagr']:+.2%} vs naked {base['cagr']:+.2%}")

    print("\n  RANKED BY DRAWDOWN ACTUALLY BOUGHT -- read this table, not the one above.")
    print("  Efficiency is a ratio and its denominator goes to zero: a structure costing")
    print("  0.03pp/yr and buying 6pp of drawdown scores 218 and protects nothing. The")
    print("  ratio is only meaningful BETWEEN structures of comparable cost, so the")
    print("  question for a real book is how much drawdown got bought and at what price.")
    print(f"  {'tenor':>5s} {'OTM':>5s} {'structure':<13s} {'CAGR':>8s} "
          f"{'maxDD':>8s} {'cost':>7s} {'ddBought':>9s} {'eff':>7s}")
    for _, r in frame.sort_values("dd_bought_pp", ascending=False).head(8).iterrows():
        print(f"  {r['tenor']:5.0f}w {r['otm']:5.0%} {r['structure']:<13s} "
              f"{r['cagr']:+8.2%} {r['maxdd']:+8.1%} {r['cost_pp']:7.2f} "
              f"{r['dd_bought_pp']:+9.1f} {r['efficiency']:7.2f}")

    print("\n  TENOR AT MATCHED STRIKE -- the cleanest contrast in the grid.")
    for moneyness in (0.10, 0.15):
        legs = frame[(frame["otm"] == moneyness) & (frame["structure"] == "outright")]
        cells = "   ".join(
            f"{r['tenor']:.0f}w {r['dd_bought_pp']:+5.1f}pp @ {r['cost_pp']:4.2f}"
            for _, r in legs.sort_values("tenor").iterrows()
        )
        print(f"    {moneyness:.0%} OTM outright:  {cells}")


def main() -> None:
    args = list(sys.argv[1:])
    slope = PRIMARY_SLOPE
    if "--slope" in args:
        i = args.index("--slope")
        slope = float(args[i + 1])
        del args[i:i + 2]
    ticker = args[0].upper() if args else "SPY"

    spot, vix = he.load_inputs(ticker)
    spread = 0.05

    frame, base = grid(spot, vix, slope, spread)
    show(frame, base, f"{ticker} FULL SAMPLE {spot.index[0].date()} to "
                      f"{spot.index[-1].date()}   skew slope {slope}, h=1.00")

    sub_spot, sub_vix = spot[SUBSAMPLE_START:], vix[SUBSAMPLE_START:]
    sub_frame, sub_base = grid(sub_spot, sub_vix, slope, spread)
    show(sub_frame, sub_base, f"{ticker} SUBSAMPLE {SUBSAMPLE_START} onward   "
                              f"skew slope {slope}, h=1.00")

    print(f"\n{'=' * 100}\nSKEW SENSITIVITY -- best efficiency in the grid, by slope")
    print(f"{'=' * 100}")
    for test in (PRIMARY_SLOPE,) + SLOPE_SENSITIVITY:
        f, b = grid(spot, vix, test, spread)
        best = f.loc[f["efficiency"].idxmax()]
        tag = "  <- primary" if test == PRIMARY_SLOPE else ""
        print(f"  slope {test:4.2f}   best = {best['tenor']:.0f}w "
              f"{best['otm']:.0%} {best['structure']:<13s} "
              f"eff {best['efficiency']:6.2f}   cost {best['cost_pp']:5.2f}pp/yr"
              f"{tag}")

    print("\ncost = pp/yr of CAGR given up vs the naked book.  ddBought = pp of max")
    print("drawdown avoided.  eff = ddBought per pp of cost, and is roughly invariant")
    print("to h, which is why it is the right metric for comparing STRUCTURES.")


if __name__ == "__main__":
    main()
