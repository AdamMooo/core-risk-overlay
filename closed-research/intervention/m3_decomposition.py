r"""E0 -- the M3 decomposition: is the drawdown reduction cash, or a mark?

ACTIVE. Charter: ../CHARTER.md, experiment E0, which heads the queue and which
nothing else may precede. Preregistration: ../docs/STUB-E0-M3-DECOMPOSITION.md,
committed 2026-08-18 before this file existed. Read it first; every parameter
below was fixed there.

THE EXPERIMENT IS ONE ACCOUNTING DIFFERENCE. Same path, same parameters, same
contracts, same cash flows:

    W_marked(t) = shares * S_t + contracts * P(S_t, K, tau - t, sigma_t)
    W_cash(t)   = shares * S_t                            inside a block
                = shares * S_t + contracts * (K - S_T)+   at expiry

`simulate(..., mark_hedge=False)` is the whole implementation. The design's one
virtue is that it cannot be confounded: the two curves are EQUAL at every roll
boundary, so premium, payoff, terminal wealth and CAGR are identical to the last
bit and the entire difference lives in the drawdown coordinates. Section 1 of
the output verifies that identity rather than assuming it -- if it fails, the
implementation is broken and no number below means anything.

WHAT THIS DOES NOT DO. It adds no monetisation rule and assumes none. `W_cash`
is not a claim that the hedge is worthless mid-life; it is the accounting under
which the program's cash flows are exactly what `simulate` already transacts.
Any real rule `rho` lands between the two curves, and E6 is where one gets
specified. E0 measures the width of the interval rho has to live in.

WHAT IT CANNOT DO. It does not add an observation. The benefit side still has
effective n = 1 -- one crisis, at one roll phase -- and the *share* reported
here is an accounting fact about this path, not an effect size. The sign and the
tenor-ordering are structural and travel; the numbers do not.

Run: .venv\Scripts\python.exe research/m3_decomposition.py [SPY]
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import numpy as np
import pandas as pd

import hedge_economics as he
import pathfunctionals as pf

# All six fixed in the stub, section 1. Changing one after seeing the output is
# selection on outcome (POINT-IN-TIME-DISCIPLINE rows 10-11).
TENORS = (4, 13, 26, 52)
PRIMARY_MONEYNESS = 0.10
SENSITIVITY_MONEYNESS = (0.05, 0.15)
SLOPE = 0.6
SPREAD = 0.05
ALPHAS = (0.01, 0.05, 0.10, 0.25, 0.50, 1.00)
EXCURSION_THRESHOLD = 0.10

# Stub section 8. Both are verdict rules, not display choices.
DOMINANCE = 0.5
DENOMINATOR_FLOOR = 0.01

SUBSAMPLE_START = he.SUBSAMPLE_START


def curves(spot, vix, moneyness, tenor):
    """The two accountings of one program, plus the unhedged book."""
    naked, _, _ = he.simulate(spot, vix, 0.0, moneyness, tenor, SLOPE, SPREAD)
    marked, prem, pay = he.simulate(spot, vix, 1.00, moneyness, tenor, SLOPE, SPREAD)
    cash, prem_c, pay_c = he.simulate(
        spot, vix, 1.00, moneyness, tenor, SLOPE, SPREAD, mark_hedge=False
    )
    return naked, marked, cash, (prem, pay), (prem_c, pay_c)


def identity_check(spot, vix):
    """Section 1: the design's own precondition, verified not assumed.

    The two curves must agree at every roll boundary and at the terminal date,
    and must transact identical premium and payoff. A failure here means the
    switch changed the position rather than the accounting.
    """
    print(f"\n{'=' * 92}")
    print("1. IDENTITY CHECK -- the decomposition's precondition")
    print(f"{'=' * 92}")
    print("   marked and cash must agree at every roll boundary and on all cash flows.")
    print(f"\n   {'tenor':>6}  {'boundary max|diff|':>19}  {'terminal max|diff|':>19}"
          f"  {'premium':>10}  {'payoff':>9}")

    ok = True
    for tenor in TENORS:
        _, marked, cash, (prem, pay), (prem_c, pay_c) = curves(
            spot, vix, PRIMARY_MONEYNESS, tenor
        )
        n = len(marked)
        bounds = list(range(0, n - 1, tenor)) + [n - 1]
        diff = np.abs(marked.to_numpy()[bounds] - cash.to_numpy()[bounds]).max()
        term = abs(marked.iloc[-1] - cash.iloc[-1])
        flows = abs(prem - prem_c) + abs(pay - pay_c)
        ok &= diff < 1e-12 and term < 1e-12 and flows < 1e-12
        print(f"   {tenor:>6}  {diff:>19.2e}  {term:>19.2e}"
              f"  {abs(prem - prem_c):>10.2e}  {abs(pay - pay_c):>9.2e}")

    print(f"\n   {'PASS -- the difference is interior only' if ok else 'FAIL -- STOP'}")
    return ok


def decompose(spot, vix, moneyness, tenor):
    """One row: what the two accountings say the program bought."""
    naked, marked, cash, (prem, pay), _ = curves(spot, vix, moneyness, tenor)
    years = (naked.index[-1] - naked.index[0]).days / 365.25

    dd = {k: pf.drawdown(c).max() for k, c in
          (("naked", naked), ("marked", marked), ("cash", cash))}
    red_marked = dd["naked"] - dd["marked"]
    red_cash = dd["naked"] - dd["cash"]

    row = {
        "tenor": tenor,
        "cagr_naked": naked.iloc[-1] ** (1 / years) - 1,
        "cagr_hedged": marked.iloc[-1] ** (1 / years) - 1,
        "premium_pa": prem / years,
        "dd_naked": dd["naked"],
        "dd_marked": dd["marked"],
        "dd_cash": dd["cash"],
        "red_marked": red_marked,
        "red_cash": red_cash,
    }
    row["gap"] = red_marked - red_cash
    # F7 before the fact: the ratio is only reportable above the declared floor.
    row["gap_share"] = (
        row["gap"] / red_marked if red_marked >= DENOMINATOR_FLOOR else np.nan
    )
    row["verdict"] = (
        "INDETERMINATE" if np.isnan(row["gap_share"])
        else "H3 REJECTED" if row["gap_share"] > DOMINANCE
        else "H3 survives"
    )
    row["curves"] = (naked, marked, cash)
    return row


def report_maxdd(spot, vix, moneyness, label):
    print(f"\n{'-' * 92}")
    print(f"   max drawdown, {moneyness:.0%} OTM, h=1.00 -- DIAGNOSTIC COORDINATE ONLY")
    print(f"   (effective n = 1; reported because it is the coordinate the "
          f"headline numbers were made in)")
    print(f"{'-' * 92}")
    print(f"   {'tenor':>5} {'naked':>8} {'marked':>8} {'cash':>8} |"
          f" {'bought(mk)':>11} {'bought(cash)':>13} {'gap':>7} {'share':>7}  verdict")

    rows = []
    for tenor in TENORS:
        r = decompose(spot, vix, moneyness, tenor)
        share = "  n/a" if np.isnan(r["gap_share"]) else f"{r['gap_share']:6.0%}"
        print(f"   {r['tenor']:>5} {r['dd_naked']:>8.1%} {r['dd_marked']:>8.1%}"
              f" {r['dd_cash']:>8.1%} | {r['red_marked'] * 100:>+11.1f}"
              f" {r['red_cash'] * 100:>+13.1f} {r['gap'] * 100:>+7.1f} {share:>7}"
              f"  {r['verdict']}")
        rows.append(r)
    return rows


def report_cdar(rows, moneyness):
    """The same decomposition in the coordinate the charter actually ranks on.

    CDaR is computed from the whole occupation measure of D, so its effective
    sample is the number of distinct excursions rather than one. If the gap is a
    max-drawdown artifact it shrinks as alpha rises; if it is a property of the
    whole path it does not.
    """
    print(f"\n{'-' * 92}")
    print(f"   CDaR_alpha reduction, {moneyness:.0%} OTM -- pp bought, marked vs cash")
    print(f"   alpha -> 0 is max drawdown (n=1); alpha = 1 is average drawdown "
          f"(well sampled)")
    print(f"{'-' * 92}")
    header = "".join(f"{a:>13.2f}" for a in ALPHAS)
    print(f"   {'tenor':>5} {'acct':>7}{header}")

    for r in rows:
        naked, marked, cash = r["curves"]
        base = pf.cdar_curve(naked, ALPHAS)
        red = {
            "marked": base - pf.cdar_curve(marked, ALPHAS),
            "cash": base - pf.cdar_curve(cash, ALPHAS),
        }
        for name in ("marked", "cash"):
            cells = "".join(f"{v * 100:>+13.1f}" for v in red[name])
            print(f"   {r['tenor'] if name == 'marked' else '':>5} {name:>7}{cells}")
        shares = []
        for a in ALPHAS:
            m, c = red["marked"][a], red["cash"][a]
            shares.append("      n/a" if m < DENOMINATOR_FLOOR
                          else f"{(m - c) / m:>12.0%}")
        print(f"   {'':>5} {'share':>7}" + "".join(f"{s:>13}" for s in shares))


def report_excursions(rows, moneyness):
    """Per-excursion depths and time under water. Psi travels with Phi."""
    print(f"\n{'-' * 92}")
    print(f"   excursions deeper than {EXCURSION_THRESHOLD:.0%}, and time under water,"
          f" {moneyness:.0%} OTM")
    print(f"{'-' * 92}")
    print(f"   {'tenor':>5} {'acct':>7} {'n>=thr':>7} {'deepest three':>26}"
          f" {'U(10%)':>8} {'mean depth':>11}")

    for r in rows:
        for name, curve in zip(("naked", "marked", "cash"), r["curves"]):
            if name == "naked" and r["tenor"] != TENORS[0]:
                continue
            exc = pf.excursions(curve, EXCURSION_THRESHOLD)
            depths = sorted((e.depth for e in exc), reverse=True)
            top = " ".join(f"{d:>7.1%}" for d in depths[:3]) or "-"
            mean = np.mean(depths) if depths else float("nan")
            tag = r["tenor"] if name != "naked" else "  --"
            print(f"   {tag:>5} {name:>7} {len(exc):>7} {top:>26}"
                  f" {pf.time_under_water(curve, EXCURSION_THRESHOLD):>8.1%}"
                  f" {mean:>11.1%}")


def report(ticker: str = "SPY") -> None:
    spot, vix = he.load_inputs(ticker)

    print(f"\n{'=' * 92}")
    print(f"E0 -- M3 DECOMPOSITION.  {ticker}, weekly, slope {SLOPE}, "
          f"offer +{SPREAD:.0%}, h=1.00, roll phase 0")
    print(f"preregistered: docs/STUB-E0-M3-DECOMPOSITION.md")
    print(f"{'=' * 92}")

    if not identity_check(spot, vix):
        sys.exit(1)

    samples = {
        f"FULL SAMPLE {spot.index[0].date()} to {spot.index[-1].date()}": (spot, vix),
        f"SUBSAMPLE {SUBSAMPLE_START} onward (inherited, unchanged -- PARKED)": (
            spot[SUBSAMPLE_START:], vix[SUBSAMPLE_START:]
        ),
    }

    section = 2
    for label, (s, v) in samples.items():
        print(f"\n\n{'=' * 92}")
        print(f"{section}. {label}")
        print(f"{'=' * 92}")
        rows = report_maxdd(s, v, PRIMARY_MONEYNESS, label)
        report_cdar(rows, PRIMARY_MONEYNESS)
        report_excursions(rows, PRIMARY_MONEYNESS)
        section += 1

    print(f"\n\n{'=' * 92}")
    print(f"{section}. MONEYNESS SENSITIVITY, full sample -- does the share depend on "
          f"the strike?")
    print(f"{'=' * 92}")
    for moneyness in SENSITIVITY_MONEYNESS:
        report_maxdd(spot, vix, moneyness, "full")

    print(f"\n{'=' * 92}")
    print("bought = pp of drawdown the accounting says the program removed.")
    print("gap    = pp visible in marks and absent from cash.  share = gap / bought.")
    print(f"H3 REJECTED where share > {DOMINANCE:.0%}: M3 IS the dominant source there.")
    print(f"INDETERMINATE where bought < {DENOMINATOR_FLOOR:.0%} -- declared before the "
          f"run, F7.")
    print("No magnitude here is identified. One path, one crisis, one roll phase.")


def main() -> None:
    args = sys.argv[1:]
    report(args[0].upper() if args else "SPY")


if __name__ == "__main__":
    main()
