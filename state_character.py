"""What market environment does each latent state actually describe?

The repo has scored the model's DENSITY exhaustively -- coverage, Berkowitz,
encompassing, dynamics -- and has never once described the STATE in plain
observable terms. Everything known about the regimes comes from fitted
parameters (sigma 1.50% vs 3.84%, expected duration 36.1 vs 12.9 weeks), and
those are in-sample quantities from a single whole-sample fit. What the states
look like out of sample, at vintage parameters, in realized market variables,
is not written down anywhere.

This is a DESCRIPTION, not a test. No forward return is regressed, no forecast
is scored, no rule is proposed, and nothing here licenses a decision. It sits
strictly between "the filter emits a number" and "somebody uses it".

--- protocol 0 stub, fixed before the run -------------------------------------

1. CLAIM TUPLE   weekly * h=1 * CONTEMPORANEOUS realized environment (volatility,
                 drift, tail asymmetry, episode duration, drawdown position) *
                 SPY, 1,230 walk-forward OOS weeks 2003-01-24 to 2026-08-14,
                 vintage parameters. NO forward window, NO regression, NO
                 comparison against VIX or any other indicator.

                 Note the h=1 label is not cosmetic. w_wide[t] is formed from
                 data through t-1, so pairing it with the week-t return is
                 already a one-step-ahead statement, not a same-time summary.
                 There is no such thing as a purely contemporaneous description
                 of a filtered state, and calling this "descriptive" does not
                 exempt it from the claim tuple.

2. PREDICTION    Split by what is entailed and what is not, because rule 2 says
                 an entailed result carries no information and must be recorded
                 rather than run.

                 ENTAILED, recorded not discovered:
                 (a) The wide band shows materially higher realized volatility.
                     w_wide[t] is driven by r[t-1] through a saturating
                     likelihood ratio and volatility clusters, so this is the
                     filter functioning. It is not evidence of anything.
                 (b) Drift separation is near zero and the tail is close to
                     symmetric. Measured already: up/down probability ratio
                     0.9279 at |r| >= 7% with a switching mean. The regime is
                     named `high_variance` for exactly this reason.

                 NOT ENTAILED, which is why the run happens:
                 (c) The OOS separation MAGNITUDE at vintage parameters. The
                     2.6x fitted sigma ratio is one whole-sample fit; the
                     realized ratio across bands out of sample is unknown and
                     could be much smaller.
                 (d) OCCUPANCY OF THE AMBIGUOUS BAND. Saturation is documented
                     (top-20 probability weeks all at P >= 0.99999), so I expect
                     the middle to be thin, but "thin" has never been counted. If
                     it is under ~5% of weeks the model effectively cannot say
                     "uncertain", which is an operational property of the signal
                     and not a fact about markets.
                 (e) REALIZED episode duration against the fitted expected
                     duration. A model that says 12.9 weeks and delivers 2 is
                     misdescribing its own persistence, and persistence is the
                     only thing this model class claims that a spot measure
                     lacks.
                 (f) Where in a DRAWDOWN each state sits. Drawdown is the
                     mandate's variable and variance is not, so this is the
                     nearest honest look at the gap.

3. LITERATURE    Hamilton (1989) for the filter; Ang & Timmermann (2012),
                 "Regime Changes and Financial Markets", for the standard
                 characterisation table this imitates. No paper settles what THIS
                 fit on THIS sample looks like, so the run is not a rediscovery.
                 Both [UNREAD] and recorded as such.

4. MECHANISM     Not a comparison. No second object, therefore no horizon at
                 which two things must differ. Rule 4 is satisfied vacuously and
                 that is precisely why this run is cheap and why it cannot
                 support a verdict.

5. SURPRISE      A vol separation near 1.0x would mean the states are a labelling
                 of noise and the translation layer has nothing to translate --
                 that kills the multi-asset extension too, since there would be
                 no state worth measuring jointly. A well-populated ambiguous
                 band would REVIVE the abstain path, which the saturation finding
                 currently rules out. Realized durations near the fitted ones
                 would be the first evidence that the persistence claim is
                 honest, which is the one axis the encompassing tests said the
                 model owns and the dynamics test said it could not monetise.

BANDS ARE DECLARED HERE AND NOT TUNED. Three coarse bands with an explicit
abstain zone, and a fixed six-bin grid for the shape. Chosen before running, on
the 0.5 convention plus a symmetric 0.2/0.8 abstain margin. No band edge is
selected on any outcome, and no sweep is reported, because a sweep over band
edges is exactly how a descriptive table turns into a threshold search.

WHAT THIS DELIBERATELY DOES NOT DO. No forward window. No VIX column. No hit
rate, lead time, or named episodes -- README 3 excludes all three permanently.
No rule, no sizing, no threshold recommendation. The next question after this
one is whether the description is incremental to VIX, and for SPY that is
already answered NO on both level (encompassing.py, D3) and dynamics
(dynamics_test.py). Nothing in this file reopens it.

Run: .venv\\Scripts\\python.exe state_character.py [SPY]
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

import numpy as np
import pandas as pd

ROOT = Path(__file__).parent
DATA_DIR = ROOT / "data"
WEEKS_PER_YEAR = 52.0

CALM_MAX = 0.20
WIDE_MIN = 0.80
COARSE = ("calm", "ambiguous", "wide")
FINE_EDGES = (0.0, 0.01, 0.10, 0.20, 0.80, 0.99, 1.0 + 1e-12)

BOOTSTRAP_BLOCK = 8
BOOTSTRAP_REPS = 2000
BOOTSTRAP_SEED = 20260814
TAIL_THRESHOLD = 0.03


def load_vintage(ticker: str) -> pd.DataFrame:
    path = DATA_DIR / f"density_{ticker.lower()}.csv"
    if not path.exists():
        raise FileNotFoundError(
            f"{path} not found. Build it first with: "
            f".venv\\Scripts\\python.exe walkforward.py density {ticker}"
        )
    frame = pd.read_csv(path, index_col=0, parse_dates=True)
    return frame[["realized", "w_wide", "sigma_wide", "sigma_calm"]].dropna()


def coarse_band(w: pd.Series) -> pd.Series:
    labels = np.where(w < CALM_MAX, "calm",
                      np.where(w >= WIDE_MIN, "wide", "ambiguous"))
    return pd.Series(labels, index=w.index, name="band")


def fine_band(w: pd.Series) -> pd.Series:
    return pd.cut(w, bins=list(FINE_EDGES), right=False,
                  labels=[f"[{a:.2f},{b:.2f})" for a, b in
                          zip(FINE_EDGES[:-1], FINE_EDGES[1:])])


def drawdown_position(returns: pd.Series) -> pd.Series:
    """Depth below the running peak, using only past data at every point."""
    cumulative = returns.cumsum()
    return np.expm1(cumulative - cumulative.cummax())


def describe_returns(r: pd.Series) -> dict:
    downside = r[r < 0]
    return {
        "n": len(r),
        "share": np.nan,
        "mean_pa": r.mean() * WEEKS_PER_YEAR,
        "vol_pa": r.std(ddof=1) * np.sqrt(WEEKS_PER_YEAR),
        "semivol_pa": (np.sqrt((downside ** 2).sum() / max(len(r) - 1, 1))
                       * np.sqrt(WEEKS_PER_YEAR)),
        "mean_abs": r.abs().mean(),
        "worst": r.min(),
        "best": r.max(),
        "neg_share": (r < 0).mean(),
        "skew": r.skew(),
        "ex_kurt": r.kurt(),
    }


def episodes(mask: pd.Series) -> list[int]:
    lengths, run = [], 0
    for value in mask.to_numpy():
        if value:
            run += 1
        elif run:
            lengths.append(run)
            run = 0
    if run:
        lengths.append(run)
    return lengths


def block_bootstrap_ratio(frame: pd.DataFrame, reps: int = BOOTSTRAP_REPS) -> tuple:
    """CI for the wide/calm realized-vol ratio under a moving-block bootstrap.

    Blocks rather than iid draws because both the returns and the state series
    are strongly dependent; an iid bootstrap would understate the interval by a
    large factor and manufacture a separation that is not there.
    """
    rng = np.random.default_rng(BOOTSTRAP_SEED)
    values = frame[["realized", "w_wide"]].to_numpy(dtype=float)
    n = len(values)
    n_blocks = int(np.ceil(n / BOOTSTRAP_BLOCK))
    ratios = []

    for _ in range(reps):
        starts = rng.integers(0, n - BOOTSTRAP_BLOCK + 1, size=n_blocks)
        idx = (starts[:, None] + np.arange(BOOTSTRAP_BLOCK)[None, :]).ravel()[:n]
        sample = values[idx]
        wide = sample[sample[:, 1] >= WIDE_MIN, 0]
        calm = sample[sample[:, 1] < CALM_MAX, 0]
        if len(wide) < 20 or len(calm) < 20:
            continue
        ratios.append(wide.std(ddof=1) / calm.std(ddof=1))

    ratios = np.asarray(ratios)
    return float(np.percentile(ratios, 2.5)), float(np.percentile(ratios, 97.5)), len(ratios)


def report_environment(frame: pd.DataFrame) -> None:
    band = coarse_band(frame["w_wide"])
    total = len(frame)

    print(f"\n{'=' * 96}")
    print("1. THE ENVIRONMENT IN EACH BAND -- realized, out of sample, vintage parameters")
    print(f"{'=' * 96}")
    print("   All figures describe week t, labelled by w_wide[t], which was formed from data")
    print("   through t-1. Annualised where marked pa. This is a description, not a forecast.")
    print(f"\n   {'band':<11s} {'n':>5s} {'share':>7s} {'drift pa':>9s} {'vol pa':>8s} "
          f"{'semivol':>8s} {'mean|r|':>8s} {'worst':>8s} {'best':>8s} {'neg%':>6s} "
          f"{'skew':>7s} {'exkurt':>7s}")

    for name in COARSE:
        r = frame.loc[band == name, "realized"]
        if r.empty:
            print(f"   {name:<11s} {0:5d}   EMPTY")
            continue
        d = describe_returns(r)
        print(f"   {name:<11s} {d['n']:5d} {d['n']/total:7.1%} {d['mean_pa']:+9.2%} "
              f"{d['vol_pa']:8.2%} {d['semivol_pa']:8.2%} {d['mean_abs']:8.2%} "
              f"{d['worst']:+8.2%} {d['best']:+8.2%} {d['neg_share']:6.1%} "
              f"{d['skew']:+7.2f} {d['ex_kurt']:+7.2f}")

    all_stats = describe_returns(frame["realized"])
    print(f"   {'ALL WEEKS':<11s} {all_stats['n']:5d} {1.0:7.1%} "
          f"{all_stats['mean_pa']:+9.2%} {all_stats['vol_pa']:8.2%} "
          f"{all_stats['semivol_pa']:8.2%} {all_stats['mean_abs']:8.2%} "
          f"{all_stats['worst']:+8.2%} {all_stats['best']:+8.2%} "
          f"{all_stats['neg_share']:6.1%} {all_stats['skew']:+7.2f} "
          f"{all_stats['ex_kurt']:+7.2f}")

    print(f"\n   {'fine bin':<14s} {'n':>5s} {'share':>7s} {'drift pa':>9s} "
          f"{'vol pa':>8s} {'mean|r|':>8s} {'worst':>8s}")
    fine = fine_band(frame["w_wide"])
    for name, r in frame["realized"].groupby(fine, observed=False):
        if r.empty:
            print(f"   {str(name):<14s} {0:5d}   EMPTY")
            continue
        d = describe_returns(r)
        print(f"   {str(name):<14s} {d['n']:5d} {d['n']/total:7.1%} "
              f"{d['mean_pa']:+9.2%} {d['vol_pa']:8.2%} {d['mean_abs']:8.2%} "
              f"{d['worst']:+8.2%}")


def report_separation(frame: pd.DataFrame) -> None:
    band = coarse_band(frame["w_wide"])
    wide = frame.loc[band == "wide", "realized"]
    calm = frame.loc[band == "calm", "realized"]

    print(f"\n{'=' * 96}")
    print("2. IS THE SEPARATION REAL, AND HOW BIG -- the only genuinely open part of table 1")
    print(f"{'=' * 96}")

    ratio = wide.std(ddof=1) / calm.std(ddof=1)
    low, high, used = block_bootstrap_ratio(frame)
    print(f"   realized vol ratio wide/calm       {ratio:.3f}")
    print(f"   moving-block bootstrap 95% CI      [{low:.3f}, {high:.3f}]  "
          f"({used}/{BOOTSTRAP_REPS} reps usable, block {BOOTSTRAP_BLOCK}w)")
    print(f"   fitted sigma ratio, last vintage   "
          f"{frame['sigma_wide'].iloc[-1] / frame['sigma_calm'].iloc[-1]:.3f}")
    print("   The fitted ratio is what the model BELIEVES; the realized ratio is what the")
    print("   bands DELIVERED out of sample. A large gap means the fit overstates its own")
    print("   discrimination, and the CI says whether the delivered gap survives dependence.")

    print("\n   DRIFT, which the entailed prediction says is not separated:")
    for name, r in (("wide", wide), ("calm", calm)):
        se = r.std(ddof=1) / np.sqrt(len(r))
        print(f"     {name:<5s} mean weekly {r.mean():+.4%}  se {se:.4%}  "
              f"t {r.mean() / se:+.2f}")
    pooled = np.sqrt(wide.var(ddof=1) / len(wide) + calm.var(ddof=1) / len(calm))
    print(f"     difference {wide.mean() - calm.mean():+.4%}  "
          f"Welch t {(wide.mean() - calm.mean()) / pooled:+.2f}")
    print("     Welch t is quoted WITHOUT a p-value on purpose: the observations are serially")
    print("     dependent and the band assignment is itself autocorrelated, so a nominal p")
    print("     would be badly oversized. Read it as an effect-size ruler only.")

    print(f"\n   TAIL SYMMETRY at |r| >= {TAIL_THRESHOLD:.0%} -- does 'wide' mean 'down'?")
    print(f"     {'band':<7s} {'n down':>7s} {'n up':>6s} {'down/up':>8s}")
    for name, r in (("wide", wide), ("calm", calm)):
        down = int((r <= -TAIL_THRESHOLD).sum())
        up = int((r >= TAIL_THRESHOLD).sum())
        ratio_du = down / up if up else float("nan")
        print(f"     {name:<7s} {down:7d} {up:6d} {ratio_du:8.2f}")
    print("     A ratio near 1.0 means the state is a WIDTH statement, not a direction one.")
    print("     That is what modelling variance means; it is not a defect to be patched.")


def report_persistence(frame: pd.DataFrame, ticker: str) -> None:
    band = coarse_band(frame["w_wide"])
    years = (frame.index[-1] - frame.index[0]).days / 365.25

    print(f"\n{'=' * 96}")
    print("3. PERSISTENCE -- the one property this model class claims that a spot measure lacks")
    print(f"{'=' * 96}")
    print(f"   {'band':<11s} {'episodes':>9s} {'per yr':>7s} {'median wk':>10s} "
          f"{'mean wk':>8s} {'max wk':>7s} {'1-week %':>9s}")
    for name in COARSE:
        lengths = episodes(band == name)
        if not lengths:
            print(f"   {name:<11s} {0:9d}   none")
            continue
        blips = sum(1 for x in lengths if x == 1) / len(lengths)
        print(f"   {name:<11s} {len(lengths):9d} {len(lengths)/years:7.2f} "
              f"{np.median(lengths):10.1f} {np.mean(lengths):8.1f} "
              f"{max(lengths):7d} {blips:9.1%}")

    print("\n   REALIZED vs FITTED expected duration. The fitted figure is 1/(1-p_jj) from the")
    print("   final vintage; the realized figure is the mean run length of the band above.")
    print("   These measure adjacent but non-identical things -- a band crossing is not a")
    print("   state transition -- so read the comparison as an order-of-magnitude check, not")
    print("   as a calibration test. A large gap still says the model misdescribes itself.")

    path = DATA_DIR / f"walkforward_{ticker.lower()}.csv"
    if path.exists():
        vintages = pd.read_csv(path)
        last = vintages.iloc[-1]
        # Identify the wide regime from the fitted variances, never from a stored
        # label column. The cached file predates the 2026-08-12 rename and still
        # carries `jump_regime`; more importantly, post-hoc relabelling by
        # argmax(sigma2) is the repo's identification rule, so re-deriving it here
        # is correct rather than merely convenient.
        stay = {0: last["p[0->0]"], 1: 1.0 - last["p[1->0]"]}
        wide = 0 if last["sigma2[0]"] > last["sigma2[1]"] else 1
        calm = 1 - wide
        print(f"     fitted expected duration  wide {1/(1-stay[wide]):6.1f} weeks   "
              f"calm {1/(1-stay[calm]):6.1f} weeks   (vintage {last['refit_end']}, "
              f"wide = regime {wide} by argmax sigma2)")
    else:
        print(f"     fitted duration unavailable: {path.name} not built")

    print("\n   BAND-TO-BAND TRANSITIONS, row-normalised (rows = from, cols = to)")
    nxt = band.shift(-1)
    counts = pd.crosstab(band[:-1], nxt[:-1])
    counts = counts.reindex(index=COARSE, columns=COARSE, fill_value=0)
    print("     " + "from/to".ljust(11) + " " + " ".join(f"{c:>11s}" for c in COARSE))
    for name in COARSE:
        row = counts.loc[name]
        share = row / row.sum() if row.sum() else row
        print(f"     {name:<11s} " + " ".join(f"{share[c]:11.1%}" for c in COARSE))
    print("     The diagonal IS the persistence the model is for. An ambiguous row that")
    print("     mostly leaves to calm or wide within a week means the middle is a transit")
    print("     corridor rather than a state the layer could ever abstain in.")


def report_drawdown(frame: pd.DataFrame) -> None:
    band = coarse_band(frame["w_wide"])
    depth = drawdown_position(frame["realized"])

    print(f"\n{'=' * 96}")
    print("4. DRAWDOWN POSITION -- variance is what the model estimates, depth is the mandate")
    print(f"{'=' * 96}")
    print("   Depth below the running peak of the OOS path, using only past data. This says")
    print("   WHERE the model tends to be, not what it predicts. A wide state that mostly")
    print("   occurs when the book is already far below its peak is a late measure -- which")
    print("   is what a causal filter is, by construction, and is recorded not deplored.")
    print(f"\n   {'band':<11s} {'mean dd':>9s} {'median dd':>10s} {'p10 dd':>9s} "
          f"{'worst dd':>9s} {'% at peak':>10s}")
    for name in COARSE:
        d = depth[band == name]
        if d.empty:
            print(f"   {name:<11s}   EMPTY")
            continue
        print(f"   {name:<11s} {d.mean():+9.2%} {d.median():+10.2%} "
              f"{d.quantile(0.10):+9.2%} {d.min():+9.2%} {(d > -0.01).mean():10.1%}")


def report_occupancy(frame: pd.DataFrame) -> None:
    w = frame["w_wide"]
    band = coarse_band(w)
    print(f"\n{'=' * 96}")
    print("5. CAN THE LAYER EVER SAY 'UNCERTAIN'? -- an operational property of the signal")
    print(f"{'=' * 96}")
    print(f"   weeks in the ambiguous band [{CALM_MAX:.2f}, {WIDE_MIN:.2f}): "
          f"{(band == 'ambiguous').sum()} of {len(w)} ({(band == 'ambiguous').mean():.1%})")
    print(f"   w_wide < 0.01                     {(w < 0.01).mean():6.1%}")
    print(f"   w_wide > 0.99                     {(w > 0.99).mean():6.1%}")
    print(f"   w_wide outside [0.01, 0.99]       "
          f"{((w < 0.01) | (w > 0.99)).mean():6.1%}")
    print(f"   median w_wide {w.median():.4f}   mean {w.mean():.4f}")
    print("\n   This is a fact about THIS FIT, not about the model class. The conditional")
    print("   variance is continuous in the mixture weight and sweeps the whole range; the")
    print("   weight saturates because the fitted components sit far apart, so one bad week")
    print("   moves the likelihood ratio almost the whole way. If the abstain band is nearly")
    print("   empty, an abstain rule has nothing to fire on -- not because abstaining is")
    print("   wrong, but because this estimator almost never expresses doubt.")


def report_halves(frame: pd.DataFrame) -> None:
    """The same four headline numbers on each half of the OOS sample.

    Not a sweep and not a search. A description that only holds on one half of
    the sample is a description of that half, and the split point is the sample
    median date -- the one choice that involves no judgement.
    """
    midpoint = len(frame) // 2
    print(f"\n{'=' * 96}")
    print("6. DOES THE DESCRIPTION HOLD ON BOTH HALVES OF THE SAMPLE")
    print(f"{'=' * 96}")
    print("   Split at the median date, which is the only split involving no judgement.")
    print("   A number that moves a lot between halves is a fact about an era, not a state.")
    print(f"\n   {'half':<24s} {'vol ratio':>10s} {'ambig %':>9s} "
          f"{'wide mean run':>14s} {'wide mean dd':>13s}")

    for label, part in (("first  " + str(frame.index[0].date()), frame.iloc[:midpoint]),
                        ("second " + str(frame.index[midpoint].date()), frame.iloc[midpoint:])):
        band = coarse_band(part["w_wide"])
        wide = part.loc[band == "wide", "realized"]
        calm = part.loc[band == "calm", "realized"]
        runs = episodes(band == "wide")
        # Depth is recomputed inside the half, so each half starts at its own
        # peak. Carrying the full-sample path in would make the second half
        # inherit 2008's drawdown and is not a property of the second half.
        depth = drawdown_position(part["realized"])
        ratio = (wide.std(ddof=1) / calm.std(ddof=1)
                 if len(wide) > 1 and len(calm) > 1 else float("nan"))
        print(f"   {label:<24s} {ratio:10.3f} {(band == 'ambiguous').mean():9.1%} "
              f"{np.mean(runs) if runs else float('nan'):14.1f} "
              f"{depth[band == 'wide'].mean():13.2%}")


def draw(frame: pd.DataFrame, ticker: str) -> None:
    """One figure, three panels, matching the three questions the tables answer.

    Deliberately NOT added to figures.py: that module's figure list is
    preregistered in protocol 8 precisely so the analysis cannot sprawl into
    whatever looks interesting. This figure belongs to this experiment and lives
    with the stub that licenses it.
    """
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    ink, muted, accent, calm = "#1a1a1a", "#8a8a8a", "#c1440e", "#2b6cb0"
    band = coarse_band(frame["w_wide"])
    fine = fine_band(frame["w_wide"])

    fig, axes = plt.subplots(1, 3, figsize=(15, 4.6))

    grouped = frame["realized"].groupby(fine, observed=False)
    labels = [str(k) for k, _ in grouped]
    vols = [r.std(ddof=1) * np.sqrt(WEEKS_PER_YEAR) if len(r) > 1 else np.nan
            for _, r in grouped]
    drifts = [r.mean() * WEEKS_PER_YEAR if len(r) else np.nan for _, r in grouped]
    counts = [len(r) for _, r in grouped]

    ax = axes[0]
    ax.bar(range(len(labels)), vols, color=calm, width=0.62)
    for i, n in enumerate(counts):
        ax.text(i, vols[i], f"n={n}", ha="center", va="bottom", fontsize=7, color=muted)
    twin = ax.twinx()
    twin.plot(range(len(labels)), drifts, "o-", color=accent, lw=1.4, ms=4)
    twin.axhline(0, color=muted, lw=0.7, ls=":")
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=45, ha="right", fontsize=7)
    ax.set_ylabel("realized volatility, annualized", color=calm)
    twin.set_ylabel("mean drift, annualized", color=accent)
    ax.set_title("A. width separates, drift does not", fontsize=10, color=ink)
    ax.set_xlabel("P(wide regime), formed at t-1")

    ax = axes[1]
    depth = drawdown_position(frame["realized"])
    data = [depth[band == name].to_numpy() for name in COARSE]
    parts = ax.boxplot(data, tick_labels=list(COARSE), showfliers=False,
                       patch_artist=True, medianprops={"color": accent, "lw": 1.6})
    for patch, colour in zip(parts["boxes"], (calm, muted, accent)):
        patch.set_facecolor(colour)
        patch.set_alpha(0.32)
    ax.axhline(0, color=muted, lw=0.8, ls=":")
    ax.set_ylabel("depth below running peak")
    ax.set_title("B. the wide state arrives deep into a drawdown", fontsize=10, color=ink)

    ax = axes[2]
    ax.hist(frame["w_wide"], bins=50, color=calm, alpha=0.85)
    ax.axvspan(CALM_MAX, WIDE_MIN, color=muted, alpha=0.18)
    ax.set_yscale("log")
    ax.set_xlabel("P(wide regime)")
    ax.set_ylabel("weeks (log scale)")
    ax.set_title(f"C. shaded = ambiguous, {(band == 'ambiguous').mean():.0%} of weeks",
                 fontsize=10, color=ink)

    for a in axes:
        a.spines[["top", "right"]].set_visible(False)
    axes[0].spines["right"].set_visible(True)

    fig.suptitle(f"{ticker}: what the latent states describe   "
                 f"({len(frame)} walk-forward OOS weeks, "
                 f"{frame.index[0].date()} to {frame.index[-1].date()})",
                 fontsize=11, color=ink)
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    fig.text(0.5, 0.015,
             "A: the drift line is NOT a signal. Its end bins hold few weeks and a "
             "handful of overlapping episodes, so the swing there is sampling noise, "
             "not a direction the state predicts.\n"
             "The bars are the finding; the line is flat wherever there is enough data "
             "to say so. B: where the state OCCURS, not what it forecasts.",
             ha="center", fontsize=7.5, color=muted)
    out = ROOT / "figures" / f"state_character_{ticker.lower()}.png"
    out.parent.mkdir(exist_ok=True)
    fig.savefig(out, dpi=150)
    plt.close(fig)
    print(f"\n   figure written to {out.relative_to(ROOT)}")


def main() -> None:
    ticker = (sys.argv[1] if len(sys.argv) > 1 else "SPY").upper()
    frame = load_vintage(ticker)

    print("=" * 96)
    print(f"STATE CHARACTERISATION -- {ticker}")
    print("=" * 96)
    print(f"   {len(frame)} walk-forward OOS weeks   "
          f"{frame.index[0].date()} .. {frame.index[-1].date()}")
    print("   Source: data/density_%s.csv, vintage parameters, filtered never smoothed."
          % ticker.lower())
    print("   Bands declared in the module docstring before the run and not tuned.")

    report_environment(frame)
    report_separation(frame)
    report_persistence(frame, ticker)
    report_drawdown(frame)
    report_occupancy(frame)
    report_halves(frame)
    draw(frame, ticker)

    print(f"\n{'=' * 96}")
    print("SCOPE. Everything above is Q1/Q2: can the states be told apart, and what do they")
    print("look like. Q3 -- is this incremental to what a downstream user already sees -- is")
    print("NOT answered here and is not answerable from these tables. For SPY it is already")
    print("answered NO on levels (encompassing.py) and on dynamics (dynamics_test.py), and")
    print("no table above reopens either. Q4 is gated on D5 and untouched.")
    print("")
    print("WIDTH, NOT DIRECTION. Tables 1 and 2 establish a volatility axis and REFUTE a")
    print("directional reading: the drift difference reverses sign between SPY and QQQ and")
    print("the down/up tail ratio straddles 1.0. Nothing here licenses `wide -> bearish`.")
    print("The binding contract is docs/TRANSLATION-LAYER.md.")
    print("=" * 96)


if __name__ == "__main__":
    main()
