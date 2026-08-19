r"""E4 -- strike anchoring (M1) as pure path geometry, across markets and eras.

ACTIVE. Charter: ../CHARTER.md, experiment E4. Preregistration:
../docs/STUB-E4-STRIKE-ANCHORING.md, committed 2026-08-18 before this file
existed, and amended once -- also before any run -- to record that the verdict
rule is biased toward M1 surviving.

THIS IS NOT AN ATTEMPT TO RESCUE THE PUT OVERLAY. The economic hypothesis for
rolled outright puts is provisionally NEGATIVE: E9 (0 of 40 structures beat the
naked book on CAGR), E0 (82-85% of the measured reduction is unrealised mark),
E1 (the magnitude is smaller than the spread from an arbitrary roll offset), E2
(no tenor ordering survives in cash anywhere on the drawdown path). Nothing here
can revise any of that, because NOTHING HERE IS PRICED and no premium is paid.

WHAT IS TESTED. Gross intrinsic payoff only, at matched notional:

    anchored     P_A = max( (1-m)*S[t]                  - S[t+H], 0 )
    re-striking  P_R = SUM_i max( (1-m)*S[t+i*s] - S[t+(i+1)*s], 0 )

No option pricing, no implied vol, no monetisation, no signal, no conditioning.

THE MECHANISM IS THE DEDUCTIBLE, AND IT IS DERIVABLE. With a_i the decline over
sub-period i, SUM a_i = S[t] - S[t+H], and at m = 0:

    P_R = SUM max(a_i, 0)  >=  max(SUM a_i, 0) = P_A

the positive part of a sum never exceeds the sum of positive parts. So WITHOUT a
deductible the re-striking leg weakly dominates on every path, always. M1 is not
"long contracts protect better"; it is "a deductible charged once beats the same
deductible charged H/s times, when the decline is persistent enough that both
legs would have paid anyway". Block 5 verifies the m=0 dominance as a control:
if it ever fails, the implementation is wrong.

WHAT THIS CANNOT SAY. A gross-payoff comparison omits the anchored leg's higher
cost by construction, which is exactly the comparison that flatters it. E4
establishes nothing about whether any overlay is worth buying at any tenor.

Run: .venv\Scripts\python.exe research/anchoring.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import numpy as np
import pandas as pd

import data_loader as dl
import pathfunctionals as pf

DATA_DIR = Path(__file__).parent.parent.parent / "data"

# Stub §2. Fixed before the run.
MARKETS = (
    ("^GSPC", "1927-01-01", "S&P 500"),
    ("^N225", "1965-01-01", "Nikkei 225"),
    ("^FTSE", "1984-01-01", "FTSE 100"),
    ("^GDAXI", "1988-01-01", "DAX"),
)
PRIMARY_H, HORIZONS = 52, (52, 104)
PRIMARY_S, SUBS = 4, (4, 13, 26)
PRIMARY_M, MONEYNESS = 0.10, (0.05, 0.10, 0.15)
PRIMARY_THR, THRESHOLDS = 0.20, (0.20, 0.10)

# Stub §8. The kill condition, unchanged from CHARTER H1.
KILL_FRACTION = 1.0 / 3.0


def payoffs(prices, horizon: int, sub: int, moneyness: float):
    """Gross intrinsic payoff of both legs at every start with a full horizon.

    The only new arithmetic in E4, and the only thing in it with tests.
    Vectorised over starts: element t is the payoff of a programme begun at t.
    """
    prices = np.asarray(prices, dtype="float64")
    last = len(prices) - horizon
    if last <= 0:
        raise ValueError(f"horizon {horizon} exceeds the {len(prices)}-week sample")

    strike_ratio = 1.0 - moneyness
    anchored = np.maximum(strike_ratio * prices[:last] - prices[horizon:horizon + last], 0.0)

    restriking = np.zeros(last)
    for i in range(0, horizon, sub):
        j = min(i + sub, horizon)
        restriking += np.maximum(
            strike_ratio * prices[i:i + last] - prices[j:j + last], 0.0
        )
    return anchored, restriking


def load_prices(ticker: str, start: str):
    """Weekly W-FRI closes, cached locally. data/ is gitignored by policy."""
    path = DATA_DIR / f"{ticker.strip('^').lower()}_e4_weekly.csv"
    if path.exists():
        return pd.read_csv(path, index_col=0, parse_dates=True).iloc[:, 0].astype("float64")
    prices = dl.download_weekly_prices(ticker=ticker, start=start)
    prices.to_frame().to_csv(path)
    return prices


def episodes_of(prices, threshold):
    """Declines of the INDEX ITSELF. Positions, so starts can be matched to them."""
    out = []
    for e in pf.excursions(prices, threshold):
        out.append({
            "start": prices.index.get_loc(e.start),
            "end": prices.index.get_loc(e.end),
            "trough": e.trough,
            "depth": e.depth,
            "label": f"{e.start.date()}..{e.end.date()}",
            "year": e.trough.year,
        })
    return out


def vote(anchored, restriking, episode, horizon):
    """Starts whose horizon intersects the episode window, and how they vote.

    Membership is [t0, t0+H] intersecting [peak, recovery] -- declared in the
    stub. Episode structure GROUPS starts; it never places one. No start sits at
    a peak, because knowing a peak is a peak is clairvoyant.
    """
    lo = max(0, episode["start"] - horizon)
    hi = min(len(anchored) - 1, episode["end"])
    if hi < lo:
        return None

    a, r = anchored[lo:hi + 1], restriking[lo:hi + 1]
    informative = (a > 0) | (r > 0)
    return {
        "n": len(a),
        "for": int(np.sum(a >= r)),
        "n_info": int(np.sum(informative)),
        "for_info": int(np.sum(a[informative] >= r[informative])),
    }


def tally(prices, episodes, horizon, sub, moneyness):
    anchored, restriking = payoffs(prices, horizon, sub, moneyness)
    rows = []
    for ep in episodes:
        v = vote(anchored, restriking, ep, horizon)
        if v is not None:
            rows.append((ep, v))
    return rows


def block_1(loaded):
    print("\n1  THE GRID -- four markets, deliberately non-contemporaneous")
    print(f"   {'market':>12} {'ticker':>8} {'from':>12} {'to':>12} {'weeks':>7}"
          f" {'eps@20%':>8} {'eps@10%':>8}")
    for ticker, name, prices, eps in loaded:
        print(f"   {name:>12} {ticker:>8} {str(prices.index[0].date()):>12}"
              f" {str(prices.index[-1].date()):>12} {len(prices):>7}"
              f" {len(eps[0.20]):>8} {len(eps[0.10]):>8}")


def block_2(loaded):
    print(f"\n2  PER-EPISODE VOTES at the primary grid"
          f" (H={PRIMARY_H}w, s={PRIMARY_S}w, m={PRIMARY_M:.0%}, threshold {PRIMARY_THR:.0%})")
    print("   FOR = anchored >= re-striking.  'info' excludes starts where BOTH legs pay zero;")
    print("   the preregistered rule counts those ties as FOR, so it is biased toward M1.")
    print(f"   {'market':>12} {'episode':>24} {'depth':>7} {'starts':>7} {'FOR':>7}"
          f" {'vote':>6} {'info':>6} {'FOR/info':>9} {'diag':>6}")

    flips = kept = 0
    for ticker, name, prices, eps in loaded:
        for ep, v in tally(prices, eps[PRIMARY_THR], PRIMARY_H, PRIMARY_S, PRIMARY_M):
            share = v["for"] / v["n"]
            voted = share >= 0.5
            flips += not voted
            kept += voted
            info = f"{v['for_info']}/{v['n_info']}" if v["n_info"] else "-"
            diag = ("n/a" if not v["n_info"]
                    else "FOR" if v["for_info"] / v["n_info"] >= 0.5 else "AGAINST")
            print(f"   {name:>12} {ep['label']:>24} {ep['depth']:>7.1%} {v['n']:>7}"
                  f" {v['for']:>7} {'FOR' if voted else 'AGAINST':>6}"
                  f" {v['n_info']:>6} {info:>9} {diag:>6}")
    return flips, kept


def block_3(flips, kept):
    total = flips + kept
    share = flips / total if total else float("nan")
    print(f"\n3  THE KILL CONDITION (CHARTER H1, unchanged): flips in >= 1/3 of episodes")
    print(f"   episodes: {total}   voting FOR M1: {kept}   flipped: {flips}"
          f"   flip share: {share:.1%}")
    verdict = "KILLED" if share >= KILL_FRACTION else "SURVIVES"
    print(f"   verdict on the preregistered rule: **M1 {verdict}**")
    return verdict


def block_4(loaded):
    print("\n4  ROBUSTNESS -- the same flip count across the declared grid")
    print(f"   {'H':>5} {'s':>4} {'m':>6} {'thr':>5} {'episodes':>9} {'flips':>6}"
          f" {'flip share':>11} {'informative flips':>18}")
    for horizon in HORIZONS:
        for sub in SUBS:
            for moneyness in MONEYNESS:
                for thr in THRESHOLDS:
                    if sub >= horizon:
                        continue
                    flips = kept = iflips = ikept = 0
                    for _, _, prices, eps in loaded:
                        for _, v in tally(prices, eps[thr], horizon, sub, moneyness):
                            voted = v["for"] / v["n"] >= 0.5
                            flips += not voted
                            kept += voted
                            if v["n_info"]:
                                ivoted = v["for_info"] / v["n_info"] >= 0.5
                                iflips += not ivoted
                                ikept += ivoted
                    n, ni = flips + kept, iflips + ikept
                    print(f"   {horizon:>5} {sub:>4} {moneyness:>6.0%} {thr:>5.0%} {n:>9}"
                          f" {flips:>6} {flips / n:>10.1%}  {f'{iflips}/{ni} = {iflips / ni:.0%}' if ni else '-':>18}")


def block_5(loaded):
    """The control. At m=0 re-striking must weakly dominate on every start."""
    print("\n5  THE m=0 CONTROL -- re-striking must weakly dominate everywhere")
    print("   sum of positive parts >= positive part of the sum. A failure here is a bug,")
    print("   not a finding, and it would invalidate every row above.")
    ok = True
    for ticker, name, prices, _ in loaded:
        worst = 0.0
        for horizon in HORIZONS:
            for sub in SUBS:
                if sub >= horizon:
                    continue
                a, r = payoffs(prices, horizon, sub, 0.0)
                worst = max(worst, float(np.max(a - r)))
        ok &= worst <= 1e-9
        print(f"   {name:>12}  max(anchored - restriking) at m=0 = {worst:.2e}")
    print(f"   {'PASS' if ok else 'FAIL -- STOP'}")
    return ok


def block_6(loaded):
    print("\n6  PSI -- what the episode count is and is not")
    windows = []
    for ticker, name, prices, eps in loaded:
        for ep in eps[PRIMARY_THR]:
            windows.append((name, ep, prices.index[ep["start"]], prices.index[ep["end"]]))

    print("   calendar overlap between markets: episodes sharing a window are NOT")
    print("   independent replications -- they are one event reported more than once.")
    print(f"   {'market':>12} {'episode':>24} {'overlaps with':>44}")
    for name, ep, start, end in windows:
        others = sorted({
            other for other, _, s2, e2 in windows
            if other != name and s2 <= end and e2 >= start
        })
        print(f"   {name:>12} {ep['label']:>24} {(', '.join(others) or 'NONE -- independent'):>44}")

    spans = {name: (prices.index[0].year, prices.index[-1].year)
             for _, name, prices, _ in loaded}
    print(f"\n   spans: " + ";  ".join(f"{k} {v[0]}-{v[1]}" for k, v in spans.items()))
    print("   the genuinely independent content is where calendars do NOT overlap:")
    print("   US 1929-1954 and Japan 1990-2003. Everything post-1990 is shared.")
    print("   Starts overlap almost completely: n_starts is NOT a sample size, and no")
    print("   standard error, test statistic or population magnitude is computed anywhere.")


def block_7(verdict, loaded):
    print("\n7  VERDICT")
    print(f"   M1 {verdict} on the preregistered rule.")
    print("   Asymmetry declared before the run (stub §8.1): the rule counts ties as votes")
    print("   FOR M1, so a KILL is strong evidence and a SURVIVAL is weak. Read block 2's")
    print("   'diag' column before quoting block 3.")
    print("\n   E4 measured payoff geometry with no premium. It says nothing about whether")
    print("   any overlay is worth buying. CHARTER §9.1's forbidden sentences still apply.")


def report() -> None:
    print(f"\n{'=' * 96}")
    print("E4 -- STRIKE ANCHORING AS PURE PATH GEOMETRY.  No pricing, no IV, no premium,")
    print("no monetisation, no signal.  preregistered: docs/STUB-E4-STRIKE-ANCHORING.md")
    print(f"{'=' * 96}")

    loaded = []
    for ticker, start, name in MARKETS:
        prices = load_prices(ticker, start)
        eps = {thr: episodes_of(prices, thr) for thr in THRESHOLDS}
        loaded.append((ticker, name, prices, eps))

    block_1(loaded)
    flips, kept = block_2(loaded)
    verdict = block_3(flips, kept)
    block_4(loaded)
    if not block_5(loaded):
        sys.exit(1)
    block_6(loaded)
    block_7(verdict, loaded)


if __name__ == "__main__":
    report()
