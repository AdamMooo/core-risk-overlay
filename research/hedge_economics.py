r"""Engine of the intervention-design program: priced put programs on a real path.

ACTIVE. Charter: ../CHARTER.md. This file owns `simulate` -- the self-financing,
weekly-marked equity curve for a continuously rolled put program -- and
`summarize`, which reduces that curve to outcomes. Everything the active program
measures runs through here.

It was written on 2026-08-13 to answer a question that is now closed ("how good
would a trigger have to be?"). The machinery survived the program that
commissioned it; the framing did not. What follows is the current reading.

THREE MECHANISMS, AND THEY ARE NOT ONE EFFECT. The measured tenor result is a
composite of three separable claims with completely different assumption costs.
Do not quote it undifferentiated.

  M1  STRIKE ANCHORING.  `simulate` re-strikes to the NEW spot at every roll, so
      short-tenor protection chases the market down and never spans the full
      peak-to-trough distance. A long-dated put struck at the peak spans it.
      Depends on the price path ALONE -- no option pricing. Testable on any
      index, any history, with no option data.

  M2  ROLL-COST AVOIDANCE.  Not repurchasing at elevated IV after the first
      shock. Depends entirely on `skewed_vol`'s sqrt(4/tenor) term, which is an
      ASSUMPTION and one that favours the conclusion. The SPY chain archive
      begins 2026-08-14 and cannot cover 2008, so M2 is NOT VERIFIABLE on the
      historical sample -- a surface fit can reject the shape, never confirm the
      cost. Formally asymmetric.

  M3  MARK-TO-MARKET.  `equity[t]` includes the put's mark, so a long-dated
      put's rising mark mechanically reduces measured `max_drawdown`. Depends on
      pricing AND on a monetisation policy. MEASURED 2026-08-18 by E0: it is the
      DOMINANT term. 82% of the 52w reduction on the full sample, 85% on the
      2003- subsample, and the +16.8pp headline becomes +3.0pp in cash. Use
      `mark_hedge=False` to see it. No output of this file is a drawdown
      reduction until its accounting is named.

CORRECTION, 2026-08-17. This docstring previously claimed: "Monetisation is
automatic ... the payoff lands in the portfolio at expiry and is reinvested at
the next roll -- which is exactly 'sell the inflated puts and buy the core at
the discount'". THAT IS FALSE, and it is the single sentence that kept the gap
invisible. The payoff lands at EXPIRY. Selling into the peak of implied
volatility is a different action, at a different time, for a different amount.
`simulate` implements NO monetisation rule. The mandate's value story requires
one. Measuring the difference was E0; it ran on 2026-08-18 and the answer is that
the gap is WIDER than the effect it sits inside -- 13.9pp of gap within a 16.8pp
claim. E6 (specify rho, measure kappa) is therefore a PRECONDITION for quoting any
magnitude from this file, not a later refinement of one.

EFFECTIVE SAMPLE. `summarize` returns `max_drawdown` as a single `.min()` of the
drawdown series. On this sample that statistic is set by one episode
(Oct 2007 - Mar 2009), and the 1993- and 2003- "samples" share it entirely. The
cost side is well sampled -- premium is paid ~1700 times. THE BENEFIT SIDE HAS
EFFECTIVE n = 1. No hypothesis may assert a magnitude from it.

ROLL PHASE IS A HIDDEN PARAMETER. Blocks walk a fixed calendar grid from index
0, so a 52-week program makes 33 decisions in 33 years and the phase of every
roll relative to the crisis is set by the sample's first date. Unswept. E1.

PRICING IS DELIBERATELY OPTIMISTIC FOR THE HEDGE. Puts are priced Black-Scholes
off VIX, a ~30-day at-the-money-ish variance rate; OTM index puts trade richer.
Pricing off VIX therefore UNDERSTATES cost, and the bias is chosen so that a
hedge which loses at an optimistically cheap price loses by more in reality.
`--skew` adds vol points back. A flat 5% offer spread is applied at every tenor,
which is a second optimistic assumption: 52-week SPY puts are thinner than
4-week, so the true spread rises with tenor and points the same way as skew.

r = 0. Over these tenors the rate effect is small next to the skew error above.

The book is marked WEEKLY with the outstanding put revalued at the current spot
and VIX, so max drawdown reflects the hedge's mid-life mark rather than only its
value at expiry -- see M3, which is precisely what that choice creates.

TWO CONSTANTS CARRY PROVENANCE FROM THE CLOSED PROGRAM. Neither is changed here;
changing them is an experiment, not a migration.
  SUBSAMPLE_START = 2003-01-24 is the closed model's 520-week burn-in. The
    active program has no burn-in and no reason to inherit it. Open, E1/E2.
  TENOR_WEEKS = (4, 13) is why the clairvoyant ceiling exists only at the
    tenors the structure map says are dominated. Extending it is E3.

Run: .venv\Scripts\python.exe research/hedge_economics.py [SPY] [--skew 4]
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import numpy as np
import pandas as pd
from scipy import stats

import data_loader as dl

ROOT = Path(__file__).parent.parent
DATA_DIR = ROOT / "data"

WEEKS_PER_YEAR = 52.0
HEDGE_RATIOS = np.round(np.arange(0.0, 1.0001, 0.05), 4)
MONEYNESS = (0.05, 0.10, 0.15)
SKEW_SLOPES = (0.0, 0.4, 0.6, 0.8)
TENOR_WEEKS = (4, 13)
REPORT_RATIOS = (0.0, 0.05, 0.10, 0.25, 0.50, 1.00)
SUBSAMPLE_START = "2003-01-24"


def black_scholes_put(spot, strike, years, sigma):
    """European put, r=0. Vectorised; years=0 returns intrinsic value."""
    spot = np.asarray(spot, dtype="float64")
    years = np.asarray(years, dtype="float64")
    sigma = np.asarray(sigma, dtype="float64")

    intrinsic = np.maximum(strike - spot, 0.0)
    alive = (years > 0) & (sigma > 0)
    if not np.any(alive):
        return intrinsic

    vol_time = np.where(alive, sigma * np.sqrt(np.maximum(years, 0.0)), 1.0)
    d1 = np.where(alive, (np.log(spot / strike) + 0.5 * vol_time**2) / vol_time, 0.0)
    d2 = d1 - vol_time
    priced = strike * stats.norm.cdf(-d2) - spot * stats.norm.cdf(-d1)
    return np.where(alive, priced, intrinsic)


def load_inputs(ticker: str):
    returns_path = DATA_DIR / f"{ticker.lower()}_weekly.csv"
    if not returns_path.exists():
        raise FileNotFoundError(f"{returns_path} missing. Run walkforward.py first.")
    returns = (
        pd.read_csv(returns_path, index_col=0, parse_dates=True)
        .iloc[:, 0]
        .astype("float64")
    )

    vix_path = DATA_DIR / "vix_weekly.csv"
    if vix_path.exists():
        raw_vix = pd.read_csv(vix_path, index_col=0, parse_dates=True).iloc[:, 0]
    else:
        raw_vix = dl.download_weekly_vix()
        raw_vix.to_frame().to_csv(vix_path)

    vix = dl.align_vix_to_returns(raw_vix, returns) / 100.0
    spot = 100.0 * np.exp(returns.cumsum())
    return spot, vix


def skewed_vol(base_vix, strike, spot_now, tenor_weeks, slope):
    """Implied vol for a put, with an equity skew that steepens with moneyness.

    A FLAT skew premium is wrong and it flatters deep strikes specifically --
    the exact strikes the first run made look best. Real index skew rises
    roughly linearly in percent out-of-the-money, so a 15% OTM put carries far
    more than a 5% OTM one, and short tenors are steeper than long ones.

        IV = VIX + slope * (percent OTM) * sqrt(4 / tenor_weeks)

    slope is vol points per 1% OTM at a 4-week tenor. SPX sits near 0.5-0.8 for
    short-dated puts. THIS IS A PARAMETERISED GUESS, not fitted to option data.
    The repo has no option chain, so the honest move is to sweep slope and see
    whether the conclusion depends on it. If it does, the conclusion is about
    the parameter, not the market.
    """
    otm_pct = np.maximum(0.0, (1.0 - strike / spot_now) * 100.0)
    tenor_scale = np.sqrt(4.0 / tenor_weeks)
    return base_vix + slope * otm_pct * tenor_scale / 100.0


def simulate(spot, vix, hedge_ratio, moneyness, tenor, skew_slope=0.0,
             spread=0.0, foresight=False, trigger=None, short_moneyness=0.0,
             mark_hedge=True, phase=0):
    """Weekly-marked equity curve for a continuously rolled put program.

    Self-financing: premium is paid out of the book at each roll, the remainder
    is held in the index, and the payoff lands back in the book at expiry.

    short_moneyness > moneyness turns the outright put into a PUT SPREAD: long
    at (1 - moneyness), short at (1 - short_moneyness). The short leg is deeper
    OTM, so under a skew it carries a HIGHER implied vol than the long leg and
    recoups disproportionately more premium than a flat surface would suggest.
    That is the whole reason a spread is worth testing in a skewed market. The
    cost is that the payoff is capped at the distance between the strikes --
    precisely in the deep tail the program exists to insure. Both legs cross the
    bid-ask, so `spread` is paid on the long leg and given up on the short.

    phase moves the roll grid and nothing else: at phase p the first block is a
    stub of p weeks, so rolls land at {p, p+tenor, ...} while the sample, the
    naked book and the price path are untouched. p = 0 is the historical
    behaviour exactly. It exists because the alignment of rolls against the one
    episode that sets every drawdown number was never chosen -- it fell out of
    the sample's first date. E1.

    mark_hedge=False switches the ACCOUNTING, not the position. The book then
    carries the hedge at zero inside a block and recognises it only at expiry,
    when it becomes a cash flow -- which is the only moment `simulate` has ever
    actually transacted it. Premium, contracts, payoff, terminal wealth and CAGR
    are UNCHANGED; the two curves coincide at every roll boundary and differ only
    in a block's interior. That is M3, isolated. E0.

    foresight=True is CLAIRVOYANT and not implementable: it looks at the expiry
    price before deciding to buy, and skips any block where the structure would
    expire worth less than it cost. It is the strict upper bound on what ANY
    trigger can achieve at this instrument, strike and tenor -- no signal,
    however good, beats knowing the answer. Its only purpose is to bound others.
    """
    prices = spot.to_numpy()
    base_vix = vix.to_numpy()
    fires = None if trigger is None else trigger.reindex(spot.index).fillna(False).to_numpy()
    n = len(prices)
    blocks_total = 0
    blocks_hedged = 0

    equity = np.empty(n)
    equity[0] = 1.0
    premium_paid = 0.0
    payoff_received = 0.0

    # E1. `phase` moves the ROLL GRID without moving the sample: the first block
    # is a stub of `phase` weeks, so rolls land at {phase, phase+tenor, ...} and
    # the naked book is identical across every phase. phase == tenor is phase 0,
    # which is why the modulo is the definition rather than a guard.
    stub = phase % tenor
    block_start = 0
    while block_start < n - 1:
        is_stub = bool(stub) and block_start == 0
        span = stub if is_stub else tenor
        block_end = min(block_start + span, n - 1)
        # The stub is genuinely a shorter-dated option and is priced as one. A
        # TRUNCATED FINAL block is not -- it keeps the nominal tenor's skew
        # scaling, which is the pre-existing convention and is left alone.
        skew_tenor = span if is_stub else tenor
        entry_spot = prices[block_start]
        value = equity[block_start]

        strike = entry_spot * (1.0 - moneyness)
        short_strike = entry_spot * (1.0 - short_moneyness) if short_moneyness else 0.0
        entry_years = (block_end - block_start) / WEEKS_PER_YEAR
        entry_vol = skewed_vol(
            base_vix[block_start], strike, entry_spot, skew_tenor, skew_slope
        )
        # Bought at the offer, not the mid.
        unit_cost = float(
            black_scholes_put(entry_spot, strike, entry_years, entry_vol)
        ) * (1.0 + spread)
        if short_strike:
            short_vol = skewed_vol(
                base_vix[block_start], short_strike, entry_spot, skew_tenor, skew_slope
            )
            unit_cost -= float(
                black_scholes_put(entry_spot, short_strike, entry_years, short_vol)
            ) * (1.0 - spread)

        contracts = hedge_ratio * value / entry_spot
        expiry_payoff = max(strike - prices[block_end], 0.0)
        if short_strike:
            expiry_payoff -= max(short_strike - prices[block_end], 0.0)
        if foresight and expiry_payoff <= unit_cost:
            contracts = 0.0
        if fires is not None and not fires[block_start]:
            contracts = 0.0
        blocks_total += 1
        blocks_hedged += int(contracts > 0.0)
        cost = contracts * unit_cost
        premium_paid += cost
        shares = (value - cost) / entry_spot

        for t in range(block_start + 1, block_end + 1):
            remaining = (block_end - t) / WEEKS_PER_YEAR
            mark_vol = skewed_vol(base_vix[t], strike, prices[t], skew_tenor, skew_slope)
            put_value = float(
                black_scholes_put(prices[t], strike, remaining, mark_vol)
            )
            if short_strike:
                short_mark_vol = skewed_vol(
                    base_vix[t], short_strike, prices[t], skew_tenor, skew_slope
                )
                put_value -= float(
                    black_scholes_put(prices[t], short_strike, remaining, short_mark_vol)
                )
            # E0. mark_hedge=False switches the ACCOUNTING, not the position:
            # the hedge is recognised only when it becomes a cash flow, which is
            # at expiry. t == block_end is that moment and `remaining` is zero
            # there, so put_value is already the intrinsic payoff and must stay.
            # Both curves therefore coincide at every roll boundary and differ
            # only in a block's interior -- see docs/STUB-E0-M3-DECOMPOSITION.
            if not mark_hedge and t < block_end:
                put_value = 0.0
            equity[t] = shares * prices[t] + contracts * put_value

        payoff_received += contracts * expiry_payoff
        block_start = block_end

    curve = pd.Series(equity, index=spot.index)
    curve.attrs["blocks_total"] = blocks_total
    curve.attrs["blocks_hedged"] = blocks_hedged
    return curve, premium_paid, payoff_received


def summarize(curve, premium_paid, payoff_received):
    years = (curve.index[-1] - curve.index[0]).days / 365.25
    cagr = curve.iloc[-1] ** (1.0 / years) - 1.0
    drawdown = (curve / curve.cummax() - 1.0).min()
    weekly = np.log(curve).diff().dropna()
    return {
        "cagr": cagr,
        "max_drawdown": drawdown,
        "vol_annual": weekly.std() * np.sqrt(WEEKS_PER_YEAR),
        "premium_drag_pa": premium_paid / years,
        "payoff_pa": payoff_received / years,
    }


def sweep(spot, vix, moneyness, tenor, skew_slope, spread):
    rows = []
    for ratio in HEDGE_RATIOS:
        curve, premium, payoff = simulate(
            spot, vix, ratio, moneyness, tenor, skew_slope, spread
        )
        row = summarize(curve, premium, payoff)
        row["hedge_ratio"] = ratio
        rows.append(row)
    return pd.DataFrame(rows).set_index("hedge_ratio")


def report(ticker: str = "SPY", spread: float = 0.05) -> None:
    spot, vix = load_inputs(ticker)

    samples = {
        f"FULL SAMPLE {spot.index[0].date()} to {spot.index[-1].date()}": (spot, vix),
        f"SUBSAMPLE {SUBSAMPLE_START} onward": (
            spot[SUBSAMPLE_START:],
            vix[SUBSAMPLE_START:],
        ),
    }

    for label, (s, v) in samples.items():
        naked_curve, _, _ = simulate(s, v, 0.0, 0.10, 4, 0.0, spread)
        base = summarize(naked_curve, 0.0, 0.0)
        print(f"\n{'=' * 92}\n{label}")
        print(
            f"naked book: CAGR {base['cagr']:+.2%}   maxDD {base['max_drawdown']:+.1%}"
            f"   |   offer = mid + {spread:.0%}"
        )
        print(f"{'=' * 92}")

        for tenor in TENOR_WEEKS:
            print(f"\n{tenor}-WEEK ROLL, full notional (h=1.00)")
            print("             " + "".join(f"{m:>10.0%} OTM" for m in MONEYNESS))
            print("  slope      " + "  cost    dd  eff" * len(MONEYNESS))
            for slope in SKEW_SLOPES:
                cells = []
                for moneyness in MONEYNESS:
                    curve, prem, pay = simulate(
                        s, v, 1.00, moneyness, tenor, slope, spread
                    )
                    row = summarize(curve, prem, pay)
                    cost = (base["cagr"] - row["cagr"]) * 100
                    bought = (row["max_drawdown"] - base["max_drawdown"]) * 100
                    eff = bought / cost if cost > 1e-9 else float("nan")
                    cells.append(f" {cost:6.2f} {bought:+5.1f} {eff:5.1f}")
                print(f"  {slope:4.2f}       " + "".join(cells))

            print(f"\n  clairvoyant ceiling (EVPI), {tenor}-week roll")
            print("  slope      " + "".join(f"{m:>10.0%} OTM" for m in MONEYNESS))
            print("             " + "  dCAGR   dDD    " * len(MONEYNESS))
            for slope in SKEW_SLOPES:
                cells = []
                for moneyness in MONEYNESS:
                    curve, prem, pay = simulate(
                        s, v, 1.00, moneyness, tenor, slope, spread, foresight=True
                    )
                    row = summarize(curve, prem, pay)
                    d_cagr = (row["cagr"] - base["cagr"]) * 100
                    d_dd = (row["max_drawdown"] - base["max_drawdown"]) * 100
                    cells.append(f"  {d_cagr:+6.2f} {d_dd:+6.1f}   ")
                print(f"  {slope:4.2f}       " + "".join(cells))

    print(f"\n{'=' * 92}")
    print("cost = pp/yr of CAGR given up.  dd = pp of max drawdown bought (+ is less")
    print("drawdown).  eff = dd per unit cost.  slope = vol points of skew per 1% OTM")
    print("at 4 weeks; 0.00 is the naive flat-VIX pricing of the first run.")
    print("dCAGR/dDD are the CLAIRVOYANT bound -- unachievable, and the ceiling on")
    print("what any trigger at that strike and tenor could ever be worth.")


def main() -> None:
    args = list(sys.argv[1:])
    spread = 0.05
    if "--spread" in args:
        i = args.index("--spread")
        spread = float(args[i + 1])
        del args[i : i + 2]
    report(args[0].upper() if args else "SPY", spread)


if __name__ == "__main__":
    main()
