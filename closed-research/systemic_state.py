"""Is it systemic? A cross-asset state indicator against SPY-only implied vol.

README 1: "SPY wobbling alone is noise. SPY, QQQ and international falling
together is the event worth insuring." VIX is SPY-only implied volatility. It
measures SPY wobbling. It CANNOT distinguish the noise case from the event case
-- not badly, but structurally, at any sample size, with any model. That is a
COVERAGE gap, and it is the one thing every result in this repo leaves untouched.

So this is not an information test. D3 and dynamics_test.py were information
tests and they are finished: no returns-based estimator adds anything to VIX for
SPY risk, on level or on dynamics. This asks a different question -- when does
each indicator say the market is under systemic stress, how often, for how long,
and WHERE DO THEY DISAGREE.

--- protocol 0 stub, fixed before the run -------------------------------------

1. CLAIM TUPLE   weekly decisions * contemporaneous state * operational
                 properties (frequency, duration, whipsaw, agreement) *
                 SPY/QQQ/EFA/EEM 2003-2026. NO forward return is regressed and
                 no predictive claim is made or implied.

2. PREDICTION    The two agree in the large events -- 2008 and 2020 are both a
                 SPY volatility shock AND a correlation shock, so nothing
                 distinguishes them there. The interesting cell is small and
                 lives in the quiet periods: AR elevated while VIX is calm.
                 I expect that cell to be non-empty and to be the whole finding.

3. LITERATURE    Kritzman, Li, Page & Rigobon (2010), "Principal Components as a
                 Measure of Systemic Risk" -- the absorption ratio. Standard,
                 not invented here. [UNREAD], recorded as such.

4. MECHANISM     VIX is a WIDTH measure on one asset. The absorption ratio is a
                 COUPLING measure across four. Cross-asset covariance structure
                 is information a single-asset option price cannot contain, at
                 any quality. This is the only mechanism argument in the repo
                 that survives the containment result.

5. SURPRISE      An empty disagreement cell would mean coupling adds nothing
                 observable beyond SPY vol, and the systemic question is closed
                 along with everything else. A populated one is the first
                 measured thing VIX cannot say.

TWO DESIGN CHOICES THAT REMOVE THE TUNING KNOBS, both fixed before running:

  CORRELATION, not covariance. Kritzman uses the covariance matrix. On a
  covariance matrix the absorption ratio rises mechanically when SPY vol spikes,
  which would make it a volatility measure in disguise -- exactly the failure the
  scale-free construction in dynamics_test.py was designed to avoid. The
  correlation matrix isolates COUPLING from LEVEL, which is the entire reason to
  add a cross-asset measure to a volatility measure. Covariance is reported as a
  DECLARED sensitivity, not as an alternative to pick from.

  EQUAL ON-TIME. Threshold choice is where a result gets manufactured, so it is
  removed: both indicators are calibrated to fire the SAME fraction of weeks, via
  an EXPANDING percentile with a 104-week burn-in (point-in-time, no look-ahead).
  Frequency is therefore held equal BY CONSTRUCTION and cannot be tuned. What is
  compared is how that identical on-time is DISTRIBUTED -- few long episodes or
  many short ones -- which is what duration and whipsaw measure. Primary target
  10% of weeks; 5% and 20% are declared sensitivities.

--- AMENDMENT 2026-08-14, after the first run --------------------------------

THE EQUAL-ON-TIME CONSTRUCTION ABOVE DID NOT DELIVER ITS STATED PROPERTY, and
this is logged rather than quietly patched. First run, single expanding
percentile:

    target 10%   ->   AR fired 16.2%,  VIX fired 11.9%
    target  5%   ->   AR fired 13.1%,  VIX fired  5.6%

So a share of the headline "AR only 8.9% of weeks" was nothing but "AR is on
more often". The comparison was not at equal on-time and the protocol said it
would be.

WHY IT FAILED. Firing when x[t] exceeds the (1 - a) quantile of its own history
has unconditional rate a only if x[t] is EXCHANGEABLE with that history. The
absorption ratio drifts upward across 2003-2026, so its accumulated history is
stale and it clears its own bar far too often. Mean-reverting VIX is close to
exchangeable and landed near target. The bug was in the calibrator, not in the
indicator.

WHY AMENDING IS LEGITIMATE HERE. The change restores a property this stub
preregistered and failed to implement; it is not selected on the outcome, and
the pre-fix numbers are preserved above. Under D4 that is a repair, not a
degree of freedom. The direction of the effect on the finding is stated in
advance: equalising on-time can only SHRINK the AR-only cell, so this makes the
result harder to obtain, not easier.

FOUR REPAIRS TRIED, ALL WORSE. Realised on-time, AR / VIX, 10% target:

    raw expanding rank      16.2% / 11.9%    overshoots on AR (the known bug)
    double rank              0.0% /  2.7%    degenerate, see below
    de-mean                  4.2% /  6.1%    undershoots BOTH
    de-median                3.9% /  5.8%    undershoots BOTH
    z-score                  0.0% /  2.6%    degenerate

  Double rank failed on TIES. 6.6% of AR ranks are exactly 1.0 -- every week the
  AR sets a new all-time high -- so the rank series has a mass point at 1.0. The
  meta-rank's 90th percentile is only 0.552 and it jumps from 0.742 straight to
  1.0, so the 10% and 5% thresholds both land in that gap and select nothing but
  the mass point. The trigger degenerated into "fires at all-time highs", which
  is why it returned an identical 3.0% at both targets. It also doubled the
  burn-in to 208 weeks, which pushes the sample start to 2008-04 and swallows
  the 2006-2007 stretch the first run was interesting for.

  De-meaning failed in the OPPOSITE direction, and the reason generalises. The
  expanding mean LAGS a trending series, so d[t] = x[t] - mean starts large and
  positive and shrinks as the mean catches up: rank mean 0.32, not 0.50. It does
  not remove the drift, it replaces an upward drift with a downward one. The
  ranker itself is sound -- on iid normal it gives rank mean 0.4946 and fires
  8.1% at a 10% target.

THE PREMISE, NOT THE IMPLEMENTATION, IS WHAT BROKE. On a persistent and
structurally drifting series there is no point-in-time normalisation that
returns an exchangeable residual, because exchangeability is exactly what the
drift destroys and any estimate of the drift is itself backward-looking. Equal
on-time BY CONSTRUCTION and point-in-time discipline cannot both hold without a
knob. This stub promised both.

--- AND THEN THE INDICATOR ITSELF FAILED ------------------------------------

Matching VIX to the absorption ratio's own realised rate was tried next. It
handed VIX a 33% budget against the AR's 9%, which looked like a third bug and
was not. It was the matcher faithfully propagating a broken rate. AR's firing
rate under the expanding-percentile rule, BY ERA:

    2004-2006     76.9% of weeks
    2006-2008     72.7%
    2008-2012     31.8%
    2012-2018      2.7%
    2018-2026      4.0%

THE 16.2% HEADLINE WAS AN AVERAGE OF 77% AND 3%. Early in the sample the
history is short and the series trends up, so the AR sets a new running high
almost every week and fires three weeks in four. Twenty years later the history
contains the 2008 and 2020 peaks and it almost never sets a new high, so it
fires one week in twenty-five. The firing rate is governed by HOW MUCH HISTORY
HAS ACCUMULATED, not by the market.

THIS RETRACTS THE FIRST RUN'S HEADLINE. The 2006-07-28 -> 2007-01-05 stretch
was read as coupling elevated through the lowest VIX regime on record. It sits
inside an era where the AR was firing 72.7% of ALL weeks. It was not detecting
anything; it was simply on, as it was on for most of that period regardless of
what markets did. The disagreement cell was an artifact of the calibration era,
and none of the three "AR only" runs survives.

WHAT IS AND IS NOT DAMAGED. The AR LEVEL is still a legitimate measurement --
an eigenvalue share of a realised correlation matrix, and README 1's coupling
argument is untouched. What is refuted is thresholding it with an expanding
percentile, and every result above that rests on one.

THE FIX IS IN THE PAPER WE DID NOT READ. Protocol item 3 records Kritzman, Li,
Page & Rigobon (2010) as [UNREAD]. Kritzman does not threshold the raw ratio.
The paper's own statistic is a STANDARDISED SHIFT -- a short-window average of
the AR minus a long-window average, divided by the long-window standard
deviation -- which is stationary by construction and immune to exactly this
failure. Adopting it is not a knob chosen after seeing results; it is using the
published construction as specified, and the 2026-08-14 lesson is that the
[UNREAD] tag was itself the defect.

TWO FURTHER RESULTS FROM THE FIRST RUN, reported and NOT designed away:

  The correlation-vs-covariance choice was INERT. corr(AR_corr, AR_cov) =
  +0.9825. The design decision billed above as the one that isolates coupling
  from level did essentially nothing, and corr(AR_corr, VIX) = +0.4965 -- the
  absorption ratio is still half VIX. Both stay in the output as findings.

  WINDOW MEMORY is a live confound. A 252-day window keeps the AR mechanically
  elevated for a year after any crash, so an "AR only" stretch following a
  selloff may be the window remembering rather than coupling now. The
  descriptive listing therefore annotates each stretch with the worst single
  SPY day inside its own trailing window. This is an annotation, not an
  exclusion rule.

NO EPISODE SCORING. README 3 permanently excludes crisis-detection hit rates,
lead time, and accuracy on hand-selected episodes. Every metric below is
distributional over the whole sample. Disagreement DATES are printed because
they are the useful output, but they are DESCRIPTIVE -- they are not a scorecard
and must never become one.

Run: .venv\\Scripts\\python.exe systemic_state.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

import numpy as np
import pandas as pd

import data_loader as dl

ROOT = Path(__file__).parent.parent
DATA_DIR = ROOT / "data"

PANEL = ("SPY", "QQQ", "EFA", "EEM")
WINDOW = 252
BURN_IN = 104
TRIGGER_BURN_IN = 2 * BURN_IN
PRIMARY_ON_TIME = 0.10
SENSITIVITIES = (0.05, 0.20)
WEEKS_PER_YEAR = 52.0


def load_panel() -> pd.DataFrame:
    path = DATA_DIR / "panel_daily.csv"
    if path.exists():
        return pd.read_csv(path, index_col=0, parse_dates=True)

    series = {}
    for ticker in PANEL:
        prices = dl.download_daily_prices(ticker=ticker, start=dl.DEFAULT_START)
        series[ticker] = np.log(prices / prices.shift(1))

    panel = pd.DataFrame(series).dropna()
    panel.to_csv(path)
    return panel


def load_weekly_vix() -> pd.Series:
    path = DATA_DIR / "vix_weekly.csv"
    if path.exists():
        return pd.read_csv(path, index_col=0, parse_dates=True).iloc[:, 0]
    vix = dl.download_weekly_vix()
    vix.to_frame().to_csv(path)
    return vix


def absorption_ratio(panel: pd.DataFrame, window: int, use_correlation: bool) -> pd.Series:
    """Fraction of cross-asset variation held by the first eigenvector.

    High means the panel is tightly coupled and a shock propagates instead of
    diversifying away. Strictly point-in-time: the window at t ends at t.
    """
    values = panel.to_numpy()
    out = np.full(len(panel), np.nan)

    for i in range(window, len(panel) + 1):
        block = values[i - window : i]
        matrix = np.corrcoef(block, rowvar=False) if use_correlation else np.cov(
            block, rowvar=False
        )
        eigenvalues = np.linalg.eigvalsh(matrix)
        out[i - 1] = eigenvalues[-1] / eigenvalues.sum()

    return pd.Series(out, index=panel.index, name="absorption_ratio").dropna()


def _expanding_rank(series: pd.Series) -> pd.Series:
    """Position of each value within its own history. Point-in-time."""
    return series.expanding(min_periods=BURN_IN).apply(
        lambda w: float((w[-1] >= w).mean()), raw=True
    )


def expanding_trigger(series: pd.Series, on_time: float) -> pd.Series:
    """Fires above the expanding (1 - on_time) quantile. No look-ahead.

    KNOWN NOT TO DELIVER EQUAL ON-TIME. See the AMENDMENT block in the module
    docstring: this undershoots on VIX and overshoots badly on the absorption
    ratio, and the four repairs tried on 2026-08-14 were all worse. Left as the
    original until the protocol question above is settled, because it is the
    only candidate whose failure is understood and monotone.
    """
    rank = _expanding_rank(series)
    return (rank >= 1.0 - on_time).fillna(False)


def matched_trigger(reference: pd.Series, on_time: float, series: pd.Series) -> pd.Series:
    """Fires at the REFERENCE indicator's own realised on-time through t-1.

    The resolution to the amendment above. No absolute rate is targeted, so
    nothing has to be exchangeable for the construction to hold: whatever rate
    the absorption ratio happens to run at, VIX is held to that same rate. What
    the claim tuple needs is the two equal to EACH OTHER, and the 10% figure was
    only ever a preference. Strictly point-in-time -- the rate applied at t is
    computed from fires up to t-1 only, and the burn-in weeks are masked out
    rather than counted as non-fires.

    The absolute rate now floats and is REPORTED. VIX is close to exchangeable,
    so its percentile rule tracks the requested rate closely but not exactly;
    the residual is printed rather than assumed away.
    """
    ref_rank = _expanding_rank(reference)
    ref_fires = (ref_rank >= 1.0 - on_time).where(ref_rank.notna())
    rate = ref_fires.shift(1).expanding(min_periods=BURN_IN).mean()
    rank = _expanding_rank(series)
    return (rank >= 1.0 - rate).fillna(False)


def trailing_worst_day(panel: pd.DataFrame, window: int) -> pd.Series:
    """Worst single SPY log return inside the same window the AR is built on."""
    return panel["SPY"].rolling(window).min()


def episodes(fires: pd.Series) -> list[int]:
    """Lengths of contiguous fired runs, in weeks."""
    lengths, run = [], 0
    for value in fires.to_numpy():
        if value:
            run += 1
        elif run:
            lengths.append(run)
            run = 0
    if run:
        lengths.append(run)
    return lengths


def describe(name: str, fires: pd.Series, years: float) -> dict:
    lengths = episodes(fires)
    return {
        "name": name,
        "on_time": fires.mean(),
        "episodes_per_year": len(lengths) / years,
        "median_weeks": float(np.median(lengths)) if lengths else float("nan"),
        "max_weeks": max(lengths) if lengths else 0,
        "whipsaw": sum(1 for x in lengths if x == 1) / len(lengths) if lengths else float("nan"),
    }


def run_comparison(ar: pd.Series, vix: pd.Series, on_time: float, label: str,
                   worst_day: pd.Series | None = None) -> None:
    common = ar.index.intersection(vix.index)
    ar, vix = ar.reindex(common), vix.reindex(common)

    ar_fires = expanding_trigger(ar, on_time)
    vix_fires = matched_trigger(ar, on_time, vix)
    valid = ar_fires.index[TRIGGER_BURN_IN:]
    ar_fires, vix_fires = ar_fires.loc[valid], vix_fires.loc[valid]
    years = (valid[-1] - valid[0]).days / 365.25

    print(f"\n{'=' * 84}\n{label}   |   AR seed {on_time:.0%}, VIX matched to AR, "
          f"{len(valid)} weeks, {years:.1f} years")
    print(f"{'=' * 84}")
    print(f"  on-time is MATCHED, not targeted. Residual "
          f"{ar_fires.mean() - vix_fires.mean():+.1%} "
          f"(AR {ar_fires.mean():.1%} vs VIX {vix_fires.mean():.1%}).")

    print(f"\n  {'indicator':<22s} {'on%':>6s} {'ep/yr':>7s} {'med wks':>8s} "
          f"{'max wks':>8s} {'whipsaw':>8s}")
    for name, fires in (("absorption ratio", ar_fires), ("VIX", vix_fires)):
        row = describe(name, fires, years)
        print(f"  {row['name']:<22s} {row['on_time']:6.1%} "
              f"{row['episodes_per_year']:7.2f} {row['median_weeks']:8.1f} "
              f"{row['max_weeks']:8d} {row['whipsaw']:8.1%}")

    both = (ar_fires & vix_fires).sum()
    ar_only = (ar_fires & ~vix_fires).sum()
    vix_only = (~ar_fires & vix_fires).sum()
    neither = (~ar_fires & ~vix_fires).sum()
    total = len(valid)

    print(f"\n  AGREEMENT over {total} weeks")
    print(f"    both fire        {both:5d}  ({both/total:5.1%})")
    print(f"    AR only          {ar_only:5d}  ({ar_only/total:5.1%})"
          f"   <- coupling without a SPY vol shock")
    print(f"    VIX only         {vix_only:5d}  ({vix_only/total:5.1%})")
    print(f"    neither          {neither:5d}  ({neither/total:5.1%})")

    fired = ar_fires | vix_fires
    overlap = both / fired.sum() if fired.sum() else float("nan")
    print(f"    Jaccard overlap  {overlap:5.1%}   "
          f"(1.0 would mean the two are the same indicator)")

    if on_time == PRIMARY_ON_TIME and ar_only:
        only = ar_fires & ~vix_fires
        runs, start = [], None
        for date, value in only.items():
            if value and start is None:
                start = date
            elif not value and start is not None:
                runs.append((start, date))
                start = None
        if start is not None:
            runs.append((start, only.index[-1]))
        runs = [r for r in runs if (r[1] - r[0]).days >= 21]
        print(f"\n  DESCRIPTIVE ONLY -- AR-only stretches of 3+ weeks "
              f"({len(runs)} of {len(episodes(only))} runs).")
        print("  README 3 forbids scoring on selected episodes. This is a listing,")
        print("  not evidence, and must not become a scorecard.")
        print("  'worst day in window' is the worst single SPY return inside the")
        print("  252-day window the AR is built on. Large and negative means the")
        print("  window still remembers a crash, and the stretch may be memory")
        print("  rather than live coupling.")
        for start, end in runs[:12]:
            note = ""
            if worst_day is not None:
                value = worst_day.reindex([start], method="ffill").iloc[0]
                flag = "  <- window holds a crash" if value <= -0.05 else ""
                note = f"   worst day in window {value:+.2%}{flag}"
            print(f"    {start.date()} -> {end.date()}{note}")


def main() -> None:
    panel = load_panel()
    vix_daily = load_weekly_vix()

    print(f"PANEL {', '.join(PANEL)}   {panel.index[0].date()} to "
          f"{panel.index[-1].date()}   {len(panel)} daily observations")
    print(f"rolling window {WINDOW} days, first AR at "
          f"{panel.index[WINDOW - 1].date()}")

    ar_daily = absorption_ratio(panel, WINDOW, use_correlation=True)
    ar_weekly = ar_daily.resample(dl.WEEKLY_RULE).last().dropna()
    vix_weekly = vix_daily.resample(dl.WEEKLY_RULE).last().dropna()
    worst = trailing_worst_day(panel, WINDOW).resample(dl.WEEKLY_RULE).last().dropna()

    run_comparison(ar_weekly, vix_weekly, PRIMARY_ON_TIME,
                   "PRIMARY -- correlation matrix", worst)
    for on_time in SENSITIVITIES:
        run_comparison(ar_weekly, vix_weekly, on_time,
                       f"declared sensitivity -- correlation, {on_time:.0%}", worst)

    cov_daily = absorption_ratio(panel, WINDOW, use_correlation=False)
    cov_weekly = cov_daily.resample(dl.WEEKLY_RULE).last().dropna()
    run_comparison(cov_weekly, vix_weekly, PRIMARY_ON_TIME,
                   "declared sensitivity -- COVARIANCE matrix (Kritzman's form)", worst)
    print(f"\n  corr(AR_correlation, AR_covariance) = "
          f"{ar_weekly.corr(cov_weekly):+.4f}")
    print(f"  corr(AR_correlation, VIX)            = "
          f"{ar_weekly.corr(vix_weekly.reindex(ar_weekly.index)):+.4f}")
    print(f"  corr(AR_covariance,  VIX)            = "
          f"{cov_weekly.corr(vix_weekly.reindex(cov_weekly.index)):+.4f}")


if __name__ == "__main__":
    main()
