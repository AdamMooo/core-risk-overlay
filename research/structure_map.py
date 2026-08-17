r"""The structure grid: what a put program buys, given no signal at all.

ACTIVE. Charter: ../CHARTER.md. Sweeps tenor x strike x outright/spread with
NO timing anywhere in the design, and reports outcomes against the naked book.

WHAT IT ESTABLISHED (2026-08-15), and it reordered the project:
  E9   0 of 40 structures beat the naked book on CAGR, in both samples. The
       founding inequality -- "premium drag smaller than the drawdown avoided"
       -- fails on average at every point in this grid. The overlay is a
       PURCHASE of drawdown reduction at a price, not a positive-carry device.
  E10  Tenor dominates: extending 10% OTM outrights from 4w to 52w buys 3-4x
       the drawdown at flat-to-falling cost.
  F6   Deep OTM refuted -- 30% OTM at 4w/13w buys NEGATIVE drawdown.
  F7   Efficiency is not a usable metric; its denominator goes to zero.
  F12  Put spreads cap the payoff exactly in the tail the program exists for.

WHAT IT DOES NOT ESTABLISH, and this is the correction of 2026-08-17. The stub
below already said the benefit side has ~10 observations. It has fewer. Ranking
is on `max_drawdown`, a single `.min()` set by one episode (Oct 2007 - Mar
2009) which BOTH samples share entirely. So:

  - the ORDERING (long tenor spans a multi-month drawdown, short tenor
    re-strikes downward through it) is a structural mechanism and is probably
    robust -- it is arithmetic about where the strike sits;
  - the MAGNITUDES (+16.8, +19.9, +24.3pp) are one draw of one statistic at one
    arbitrary roll phase, and are NOT identified. Do not quote them as effects.

Three further conditions on every row, none of them swept here:
  - ROLL PHASE. Blocks walk a fixed grid from index 0; at 52w that is 33
    decisions in 33 years. E1 sweeps it.
  - M3. Ranking is on MARKED wealth including the put's mark, under no
    monetisation rule. E0 decomposes it.
  - M2. Cost rests on skewed_vol's sqrt(4/tenor), an assumption favouring the
    conclusion, and on a tenor-flat offer spread. Neither is verifiable on this
    sample.

--- protocol 0 stub, fixed before the original run ----------------------------

1. CLAIM TUPLE   weekly marks * full holding period * geometric return and max
                 drawdown * SPY 1993-2026, subsample 2003-2026 * ALWAYS-ON,
                 h=1.00, NO signal and NO timing anywhere in the design.

2. PREDICTION    (a) NO structure beats the naked book on CAGR. CONFIRMED.
                 (b) Efficiency maximised at long tenor AND deep strike. SPLIT
                 -- long tenor confirmed, deep strike refuted.
                 (c) Put spreads look good on premium, bad on drawdown bought.
                 CONFIRMED.

3. LITERATURE    Ilmanen (2012) on the cost of index put protection. Israelov
                 (2017), "Pathetic Protection", on rolled-put drag. Both
                 [UNREAD] and recorded as such.

4. MECHANISM     Not a comparison of estimators. A cost characterisation of a
                 DECISION whose cost side has ~1700 weekly observations and
                 whose benefit side has ~10 -- in fact one, see above.

5. SURPRISE      A structure beating naked on CAGR would have ended the signal
                 program outright. None did.

Run: .venv\Scripts\python.exe research/structure_map.py [SPY] [--slope 0.6]
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

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
    print("drawdown avoided.  eff = ddBought per pp of cost and is REFUTED as a")
    print("selection metric (F7): its denominator goes to zero, so a structure")
    print("protecting nothing scores best.  Rank on ddBought at a stated cost.")


if __name__ == "__main__":
    main()
