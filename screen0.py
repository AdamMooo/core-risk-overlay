"""Screen 0 of the present-state assessment: the redundancy / disagreement map.

Six candidate present-state risk coordinates, one elevated-state definition
each (preregistered in docs/ASSESSMENT-PRESENT-STATE-RISK.md section 7b before
this script existed -- no parameter here may change without a new
preregistration block). The deliverable is the DISAGREEMENT structure: if the
elevated states never disagree beyond episode noise, the coordinates are one
axis wearing six names, the family closes as redundant, and the honest monitor
is a citation to the OFR FSI.

DESCRIPTION ONLY. No posture, no trigger, no rule (F9 stays closed). The
backwardation tabulation re-derives a blog-grade claim from primary data with
its base rate attached.

Run: .venv\\Scripts\\python.exe screen0.py
"""
from __future__ import annotations

import io
import sys
import urllib.request
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))

from src.caching import cached_series
from src.data_loader import download_daily_prices

ROOT = Path(__file__).resolve().parent
CACHE = ROOT / "data"

# Inlined from repro_sjm2024.py at its archive move (2026-08-27) so this Thread B
# screen does not import across the closed-research boundary. Same cache keys,
# byte-identical series.
TRADING_DAYS = 252


def load_prices(ticker: str, start: str) -> pd.Series:
    key = ticker.replace("^", "").lower()
    return cached_series(CACHE, f"sjm_{key}_daily.csv",
                         lambda: download_daily_prices(ticker, start=start))

RV_WINDOW = 60
VRP_RV_WINDOW = 21
PCT_WINDOW = 1000
TURB_COV_WINDOW = 500
REFIT_DAYS = 126
BAND = (75, 55)
VRP_BAND = (25, 45)  # stress = LOW vrp, so exit below p25, re-enter above p45
PANEL = ("SPY", "EFA", "TLT", "GLD")
EPISODE_GAP = 5
FWD_DAYS = 21
DD_LEVEL = 0.05
SOLO_MIN_DAYS = 10

OFR_URL = "https://www.financialresearch.gov/financial-stress-index/data/fsi.csv"
VIX3M_URL = "https://cdn.cboe.com/api/global/us_indices/daily_prices/VIX3M_History.csv"


def _cached_csv(name: str, build) -> pd.Series:
    return cached_series(CACHE, name, build)


def load_ofr() -> pd.Series:
    def build():
        with urllib.request.urlopen(OFR_URL, timeout=60) as response:
            raw = pd.read_csv(io.StringIO(response.read().decode()))
        raw["Date"] = pd.to_datetime(raw["Date"])
        return raw.set_index("Date")["OFR FSI"].astype("float64").dropna()

    return _cached_csv("ofr_fsi.csv", build)


def load_vix3m() -> pd.Series:
    def build():
        with urllib.request.urlopen(VIX3M_URL, timeout=60) as response:
            raw = pd.read_csv(io.StringIO(response.read().decode()))
        raw["DATE"] = pd.to_datetime(raw["DATE"])
        return raw.set_index("DATE")["CLOSE"].astype("float64").dropna()

    return _cached_csv("vix3m_cboe.csv", build)


def hysteresis_band(level: pd.Series, p_exit: float, p_reenter: float,
                    low_is_stress: bool = False) -> pd.Series:
    """Elevated-state 0/1 with thresholds from trailing PCT_WINDOW percentiles,
    refit every REFIT_DAYS. `low_is_stress` flips the band for the VRP."""
    level = level.dropna()
    state = pd.Series(np.nan, index=level.index)
    elevated = False
    thr_exit = thr_reenter = None
    for k in range(PCT_WINDOW, len(level)):
        if (k - PCT_WINDOW) % REFIT_DAYS == 0:
            train = level.iloc[k - PCT_WINDOW: k]
            thr_exit = float(np.percentile(train, p_exit))
            thr_reenter = float(np.percentile(train, p_reenter))
        x = level.iloc[k]
        if not low_is_stress:
            if not elevated and x > thr_exit:
                elevated = True
            elif elevated and x < thr_reenter:
                elevated = False
        else:
            if not elevated and x < thr_exit:
                elevated = True
            elif elevated and x > thr_reenter:
                elevated = False
        state.iloc[k] = 1.0 if elevated else 0.0
    return state.dropna()


def turbulence(panel: pd.DataFrame) -> pd.Series:
    returns = panel.pct_change().dropna()
    values = pd.Series(np.nan, index=returns.index)
    X = returns.to_numpy()
    for k in range(TURB_COV_WINDOW, len(X)):
        train = X[k - TURB_COV_WINDOW: k]
        mu = train.mean(axis=0)
        cov = np.cov(train, rowvar=False)
        diff = X[k] - mu
        values.iloc[k] = float(diff @ np.linalg.solve(cov, diff))
    return values.dropna()


def spells(state: pd.Series) -> list[int]:
    runs, count = [], 0
    for v in state.to_numpy():
        if v == 1.0:
            count += 1
        elif count:
            runs.append(count)
            count = 0
    if count:
        runs.append(count)
    return runs


def solo_episodes(a: pd.Series, b: pd.Series) -> int:
    solo = ((a == 1.0) & (b == 0.0)).to_numpy()
    return sum(1 for run in spells(pd.Series(solo.astype(float))) if run >= SOLO_MIN_DAYS)


def main() -> int:
    gspc = load_prices("^GSPC", "1970-01-01")
    returns = gspc.pct_change().dropna()
    # Cache names carry an s0_ prefix: data/spy_daily.csv already belongs to the
    # closed programme and holds log RETURNS, not prices -- a silent collision.
    vix = _cached_csv("s0_vix_daily.csv", lambda: download_daily_prices("^VIX", start="1990-01-01"))
    vix3m = load_vix3m()
    ofr = load_ofr()
    panel = pd.DataFrame({t: _cached_csv(f"s0_{t.lower()}_daily.csv",
                                         lambda t=t: download_daily_prices(t, start="2001-01-01"))
                          for t in PANEL}).dropna()

    rv = returns.rolling(RV_WINDOW).std().mul(np.sqrt(TRADING_DAYS)).dropna()
    implied_var = (vix / 100.0) ** 2
    realized_var = returns.rolling(VRP_RV_WINDOW).var().mul(TRADING_DAYS)
    vrp = (implied_var - realized_var).dropna()
    slope = (vix / vix3m).dropna()
    turb = turbulence(panel)

    levels = {"RV": rv, "VIX": vix, "slope": slope, "VRP": vrp,
              "turb": turb, "OFR": ofr}
    states = {
        "RV": hysteresis_band(rv, *BAND),
        "VIX": hysteresis_band(vix, *BAND),
        "slope": (slope > 1.0).astype(float),
        "VRP": hysteresis_band(vrp, *VRP_BAND, low_is_stress=True),
        "turb": hysteresis_band(turb, *BAND),
        "OFR": (ofr > 0.0).astype(float),
    }

    S = pd.DataFrame(states).dropna()
    L = pd.DataFrame(levels).reindex(S.index)
    names = list(S.columns)
    print(f"joint sample: {S.index[0].date()} to {S.index[-1].date()} "
          f"({len(S)} days, {len(S)/TRADING_DAYS:.1f} years) -- no GFC (VIX3M starts 2009-09)")

    print("\nlevel correlations (Pearson, joint sample)")
    print(L.corr().round(2).to_string())

    def jaccard_table(frame: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame(index=names, columns=names, dtype=float)
        for a, b in combinations(names, 2):
            both = float(((frame[a] == 1) & (frame[b] == 1)).sum())
            either = float(((frame[a] == 1) | (frame[b] == 1)).sum())
            out.loc[a, b] = out.loc[b, a] = both / either if either else np.nan
        return out

    print("\nelevated-state Jaccard (days both / days either)")
    print(jaccard_table(S).round(2).to_string(na_rep="--"))

    half = len(S) // 2
    print("\nJaccard, first half / second half")
    j1, j2 = jaccard_table(S.iloc[:half]), jaccard_table(S.iloc[half:])
    for a, b in combinations(names, 2):
        print(f"  {a:>5s} vs {b:<5s}: {j1.loc[a, b]:.2f} / {j2.loc[a, b]:.2f}")

    print("\noccupancy and spells")
    print(f"{'':<7s}{'elevated':>10s}{'spells':>8s}{'median d':>10s}{'mean d':>8s}")
    for n in names:
        runs = spells(S[n])
        med = float(np.median(runs)) if runs else 0.0
        avg = float(np.mean(runs)) if runs else 0.0
        print(f"{n:<7s}{S[n].mean():>10.1%}{len(runs):>8d}{med:>10.0f}{avg:>8.1f}")

    print(f"\nsolo episodes (one elevated >= {SOLO_MIN_DAYS}d while the other is not)")
    print(f"{'':<7s}" + "".join(f"{n:>7s}" for n in names))
    for a in names:
        row = "".join(
            f"{solo_episodes(S[a], S[b]):>7d}" if a != b else f"{'--':>7s}" for b in names
        )
        print(f"{a:<7s}{row}")

    # Backwardation tabulation, re-derived from primary data with its base rate.
    inv = (slope > 1.0)
    idx = inv.index
    episodes = []
    start = None
    gap = 0
    for i, flag in enumerate(inv.to_numpy()):
        if flag:
            if start is None:
                start = i
            gap = 0
        elif start is not None:
            gap += 1
            if gap > EPISODE_GAP:
                episodes.append((start, i - gap))
                start, gap = None, 0
    if start is not None:
        episodes.append((start, len(idx) - 1))

    px = gspc.reindex(idx).ffill()
    fwd_dd = pd.Series(np.nan, index=idx)
    values = px.to_numpy()
    for i in range(len(values) - 1):
        window = values[i: i + FWD_DAYS + 1]
        fwd_dd.iloc[i] = 1.0 - window.min() / window[0]
    base = float((fwd_dd > DD_LEVEL).mean())

    hits = sum(1 for s, _ in episodes if fwd_dd.iloc[s] > DD_LEVEL)
    print(f"\nbackwardation episodes (VIX/VIX3M > 1, gaps <= {EPISODE_GAP}d merged), "
          f"sample {idx[0].date()} to {idx[-1].date()}:")
    print(f"  episodes: {len(episodes)}   with >{DD_LEVEL:.0%} drawdown within {FWD_DAYS}d "
          f"of onset: {hits}   base rate on all days: {base:.1%}")
    long_eps = [(s, e) for s, e in episodes if e - s + 1 >= 5]
    long_hits = sum(1 for s, _ in long_eps if fwd_dd.iloc[s] > DD_LEVEL)
    print(f"  EXPLORATORY, post-hoc (not preregistered): episodes lasting >= 5 days: "
          f"{len(long_eps)}, of which {long_hits} hit")
    for s, e in episodes:
        print(f"    {idx[s].date()} to {idx[e].date()}  fwd {FWD_DAYS}d dd from onset: "
              f"{fwd_dd.iloc[s]:.1%}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
