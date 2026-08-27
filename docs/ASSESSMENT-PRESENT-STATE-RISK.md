# Assessment — present-state risk description: which public coordinates say something distinct about the risk the book is carrying *now*?

Last updated: 2026-08-27. **STATUS: PROPOSAL. Not a charter, not a programme, not a queue.** The written
assessment [[CLAUDE]] §6 and [[docs/RESEARCH-PROTOCOL]] P11/P13 require before a programme may be argued.
Nothing here authorises a run beyond Screen 0 and Screen 1, both preregistered below.

**Where it came from.** The Shu-Yu-Mulvey reproduction ([[docs/REPRO-SJM2024-FINDINGS]]) ended with: the
jump model's state is a persistence-regularised volatility threshold, and the honest present-state
statement it supports is one a percentile band can make. The follow-up question — *is that statement
worth anything for risk management?* — was first answered from inside the repository ("it's a percentile,
you don't need a model"). This assessment is the outward correction: the literature holds several
present-state coordinates that are **not** trailing-vol percentiles, and at least one free, daily,
professionally maintained incumbent already exists.

---

## 1. Question

> Of the publicly observable, point-in-time coordinates that plausibly describe the **current systemic
> risk state** of a permanently long equity book, which carry **distinct** information, which are
> redundant with each other, and what **calibrated, well-sampled descriptive statements** does each
> support?

Description, not prediction: the object is `X_t -> P(adverse outcome | X_t)` stated as *conditional
base rates with effective-n honesty*, never a forecast, never a posture. Direction is excluded by
[[CLAUDE]] §4 and the width-not-direction result.

## 2. Why it matters, and why it is not already answered here

The prediction closure ([[README]] §3) says public **return-volatility estimators** add nothing to VIX
about forward downside on SPY, on levels and dynamics. It does **not** cover:

- **the shape of the volatility term structure** (VIX vs 3-month VIX) — a statement about the *term
  structure of fear*, not the level;
- **the variance risk premium** (implied minus realized variance) — a *decomposition* of VIX into
  delivered risk and priced fear, which uses a return-vol estimator to split the incumbent, not to beat
  it;
- **cross-asset covariance structure** (turbulence / Mahalanobis distance) — the closure's own text
  names covariance structure as the one information set a single-asset option price cannot contain;
- **composite stress indices maintained by others** (OFR FSI) — an incumbent to test against, not a
  candidate to build.

## 3. What the literature already knows — searched 2026-08-24, PROVISIONAL

Four searches is a scope check. [[docs/RESEARCH-PROTOCOL]] §0 field 3 is not discharged until a proper
review is done; no run beyond Screen 0 before that.

| status | finding |
|---|---|
| **established** | Volatility management of the *equity market* factor raises Sharpe (Moreira & Muir, JF 2017). The SJM paper is one entry in this family — and our reproduction's "the state is a vol threshold" is the family's own mainstream mechanism, not an insult |
| **established** | The out-of-sample, real-time version of vol management **largely fails**: across 103 strategies the implementable versions generally earn lower Sharpe/certainty-equivalent than unmanaged (Cederburg, O'Doherty, Wang & Yan, JFE 2020); costs bite further (Barroso & Detzel). Our bootstrap scepticism about the SJM margins is the literature's out-of-sample position |
| **established** | The variance risk premium — implied minus realized variance — is on average negative (variance risk is priced) and time-varying, and predicts aggregate returns at quarterly horizons (Bollerslev, Tauchen & Zhou, RFS 2009). It is a *different object* from the VIX level |
| **established regularity, primary source needed** | VIX term-structure inversion (VIX/VIX3M > 1, "backwardation") is rare (~5% of days) and clusters at stress onsets; one practitioner tabulation claims 21 of 22 inversion episodes since 2004 preceded a >5% S&P drawdown within a month. **Blog-grade claim, must be re-derived from primary data before any use — and note the base-rate trap: drawdowns are common enough that this may be less impressive than it sounds** |
| **established** | Turbulence (Mahalanobis distance; Chow-Jacquier-Kritzman-Lowrey 1999, Kritzman & Li 2010) and the absorption ratio (Kritzman-Li-Page-Rigobon 2010) are documented cross-asset state descriptors; OFR replicated absorption-ratio behaviour around crises |
| **established, and the strongest "do not build" fact** | The **OFR Financial Stress Index** is free, daily, 33 variables across credit / equity valuation / funding / safe assets / volatility, published after each U.S. trading day. A general "is the market stressed" readout is a solved, maintained, public product. Any monitor built here must state what it adds over the OFR FSI, or not exist |
| **unresolved, as far as four searches show** | The *redundancy structure* of these coordinates as present-state descriptors — which of {RV percentile, VIX level, VIX/VIX3M slope, VRP, turbulence, OFR FSI} are distinct axes and which are one axis wearing six names — stated point-in-time with honest inference. The pieces are all studied; the joint descriptive map with effective-n per coordinate is what I could not find |

## 4. Counter-arguments to this repository's own recent framing, stated fairly

1. **"It's just a vol percentile" is too quick.** True of the jump model's *state*; not true of the
   candidate space. Term-structure slope, VRP and turbulence are not functions of trailing SPY returns,
   so the nesting argument (`F^returns ⊆ F^market`) does not dispose of them — two of them are *made
   from* the option market's own prices.
2. **"Nested in VIX" does not mean "VIX is the last word."** VIX = delivered-vol expectation + variance
   risk premium. Splitting the level into its parts is informative even when the level nests your
   estimator — the split says *why* VIX is high (delivered turbulence vs priced fear), which is a
   present-state distinction a risk manager can use descriptively.
3. **"Description doesn't need incrementality" is half-right.** For a *monitor*, synthesis has value even
   without new information — but then the honest deliverable is presentation of the OFR FSI plus a few
   local coordinates, and the build is a page, not a programme. The research content, if any, is the
   redundancy map and the calibrated base rates, not the dashboard.

## 5. What public data can observe

| coordinate | source, span | PIT status | note |
|---|---|---|---|
| trailing RV percentile band | own data, 1970- | clean | built today (`volthreshold.py`) |
| VIX level | `^VIX` 1990- | clean | incumbent within-repo |
| VIX/VIX3M slope | `^VIX3M` (ex-VXV) 2007- | clean | **short history: one GFC tail, effective n on inversions ~20** |
| VRP = VIX² − realized var | both in repo | clean | construction choices (window, horizon) must be preregistered |
| turbulence (Mahalanobis) | cross-asset ETF panel 2004- | clean | needs a small fixed panel; **absorption ratio only as fixed-window characteristic — [[PARKED]] §2 forbids the percentile trigger** |
| OFR FSI | financialresearch.gov, 2000-, daily CSV | published next day; methodology revisions must be checked | **the external incumbent** |

## 6. Effective sample size, stated before anything runs

Backwardation episodes since 2004: ~22. Systemic drawdowns in the whole SPY history: ~10-15
([[systemic-events-are-too-rare-to-calibrate|systemic events are too rare to calibrate on]]). **Any claim conditioned on rare states is
episode-counted, not day-counted.** Well-sampled statements live at the *shallow* end (occupancy, spell
lengths, co-movement of coordinates); tail-conditional statements are curve endpoints, not estimates.

## 7. The cheapest first experiment — Screen 0

One script, no model, block-bootstrap errors. On the common sample (2007-, set by VIX3M):

1. The 6x6 dependence map of the coordinates (levels and a debounced state for each), full sample and
   halves.
2. Occupancy and spell statistics per coordinate: how often "elevated", how long, how often they
   disagree — **the disagreement matrix is the deliverable**: if the coordinates never disagree, the
   answer is "one axis, six names, use the OFR FSI and stop."
3. Re-derive the backwardation-episode tabulation from primary data with the base rate stated.

**Preregistered reading:** if pairwise dependence is so high that disagreement states are episode-rare,
the family closes as redundant and the honest output is a citation to the OFR FSI. That is a
publishable-quality closure for a day's work, and it is the expected-value case for running Screen 0.

## 7b. Screen 0 construction choices — preregistered 2026-08-24, before the script exists

Data realities found first: CBOE's VIX3M history begins **2009-09-18** (Yahoo's `^VIX3M` is unusable),
so the **joint sample starts there and contains no GFC**; pairwise statistics are additionally reported
on each pair's own maximal sample. OFR FSI runs 2000-01-03 to present, daily, zero-mean by construction.
The equity leg is `^GSPC` (already cached); the turbulence panel is fixed as [SPY, EFA, TLT, GLD].

Elevated-state definitions, one per coordinate, none tuned:

| coordinate | elevated when | notes |
|---|---|---|
| RV | 60d realized vol above its trailing-1000d p75, re-enter below p55 | hysteresis band as `volthreshold.py`, window 1000d (not 3000d) so the short joint sample is not consumed — declared deviation |
| VIX level | same (75,55) band on the level | |
| slope | VIX/VIX3M > 1.0 | canonical inversion threshold, literature-defined, no percentile |
| VRP | implied var (VIX/100)^2 minus trailing-21d realized var (annualized) **below** its trailing-1000d p25, re-enter above p45 | stress direction = realized overwhelming implied; the high-premium direction is a different object, noted and not used |
| turbulence | Mahalanobis distance of daily panel returns vs trailing-500d mean/cov, above its trailing-1000d p75 / re-enter p55 | fixed panel, fixed window — [[PARKED]] §2's percentile-trigger failure was an *expanding* window; these are rolling and declared |
| OFR FSI | index > 0 | the publisher's own above-average-stress convention |

Metrics: Pearson correlation of levels; pairwise Jaccard of elevated states (days both / days either);
days-A-only and days-B-only; **solo episodes** = runs of >= 10 consecutive days where one coordinate is
elevated and the other is not; occupancy, spell count, median spell length per coordinate; all repeated
on sample halves. Backwardation tabulation: episodes = runs of inversion merged across gaps <= 5 trading
days; per episode, `^GSPC` max drawdown within 21 trading days of episode start; base rate = fraction of
all sample days whose forward-21d drawdown exceeds 5%. Bands refit every 126 days. No parameter in this
table may be changed after the first run; a change requires a new preregistration block.

## 8. Clearance against PARKED

| boundary | why this is outside it |
|---|---|
| **F9 — all trigger rules, permanently closed** | the output is descriptive statements and base rates. No posture, no threshold-to-action mapping, no tier. **A hysteresis state may be *described* (occupancy, spells); the moment its only use is "so de-risk when it fires", it is F9 and it stops** |
| **[[PARKED]] §2 — absorption ratio as trigger** | enters only as a fixed-window characteristic if at all; the percentile trigger stays dead |
| **prediction closure (F1/F2)** | no forecast is made; the three new coordinates are outside the closed input family in any case |
| **the mandate, §0** | nothing here buys, sells, or sizes anything |

## 9. Predicted outcome, before any code

- RV percentile, VIX level and OFR FSI: **highly redundant** as states (high confidence). The monitor
  case survives on presentation only.
- VIX/VIX3M and VRP: **genuinely uncertain** whether their disagreement states with the level are more
  than episode-noise on 18 years. My prior: the slope's inversions are real but too rare to support more
  than "inversion is rare and bad"; the VRP's descriptive split is the likeliest to carry a
  well-sampled, distinct statement.
- Turbulence: distinct by construction (covariance axis); whether its *incremental* descriptive content
  over the OFR FSI (which already holds 33 series) is non-trivial is the open question.
- **What would change minds:** a coordinate whose elevated state disagrees with the OFR FSI's more than
  episodically *and* whose disagreement periods have distinct outcome base rates at well-sampled alphas.

## 10. Screen 0 ran — 2026-08-24, scored against §7/§9

Run: `.venv\Scripts\python.exe screen0.py`. Joint sample 2010-11-04 to 2026-08-20 (15.7 years, no GFC
— set by VIX3M plus the percentile burn-in). One execution note for the record: the first run silently
collided with the closed programme's `data/spy_daily.csv` (log returns, not prices) and produced garbage;
screen-0 caches now carry an `s0_` prefix and all files are manifest-registered.

**The redundancy closure does NOT fire. The coordinates are not one axis.** The largest elevated-state
Jaccard is RV-vs-VIX at 0.54; every other pair sits between 0.06 and 0.36 — and the matrix is strikingly
stable across sample halves (RV-VIX 0.55/0.53, VRP-turb 0.22/0.22; largest drift VIX-slope 0.27/0.18).
The disagreement structure is persistent, not episode noise.

The structure, read off the matrices:

- **The vol family {RV, VIX, OFR} clusters moderately (0.29-0.54) but is far from identical** — my §9
  "highly redundant" prediction was wrong in degree.
- **The VRP is the most independent axis**, as §9 predicted: Jaccard <= 0.24 against everything, and
  35-47 solo episodes (>= 10 consecutive days elevated alone) against every other coordinate, in both
  directions. Realized-overwhelming-implied is genuinely a different state than high-vol.
- **The slope is a subset flag, not an axis**: it almost never elevates alone (at most 1 solo episode
  against any coordinate). Inversion happens inside someone else's elevated state.
- **The coordinates differ in clock as much as in content**: median spell 102 days (RV band), 12 (VIX),
  9 (VRP), 5 (OFR), 2 (turbulence). Turbulence chatters (512 spells) — comparing it fairly needs its own
  debounce, which is a design gap recorded here, not a parameter to retune post hoc.

**The backwardation claim is refuted as stated.** Under the preregistered definition: 63 episodes since
2009, 13 followed by a >5% drawdown within 21 days (21%) against a 15.4% base rate on all days — nothing
like "21 of 22". EXPLORATORY and post-hoc: restricting to episodes lasting >= 5 days gives 24 episodes,
10 hits (42%, ~2.7x base) — suggestive, n=24, not preregistered, and would need its own confirmation
under a definition fixed in advance.

**Where this leaves the assessment.** The interesting branch fired: disagreement states exist in bulk
and are stable. The question that would justify going further — do the disagreement states carry
*distinct, well-sampled outcome base rates* (e.g., VRP-only stress vs vol-only stress) — is beyond
Screen 0's license and would need its own preregistered screen. That screen is also where F9 binds
hardest: base rates may be described; the moment the output is "so do X when the state fires," it stops.

## 11. Screen 1 — duration/hazard, preregistered 2026-08-25, before any code

> **WITHDRAWN 2026-08-25, same day, before any code — and the reason is a standing directive this
> preregistration violated.** The 2026-08-24 session closed with: *persistence is real, states are
> not; the honest object is continuous ranks and trajectories on multiple clocks, never binarized
> elevated/quiet — Screen 1 must be redesigned continuous-conditional or not at all* (recorded in
> `_daily/2026-08-24`, carried into `_daily/2026-08-25` Focus). Both 11a and 11b below are hazards of
> a **binarized** state's exit — the exact framing the directive rejects: the (75,55) band's spell
> structure is a property of the band's own hysteresis at least as much as of the market, and "9
> spells" is what discretization does to 15.7 years of continuous information. **The text is kept,
> struck in spirit, per this repository's precedent for a superseded preregistration ([[CHARTER]]
> §9.3, Q1). Nothing below may run.** A continuous-conditional redesign — the conditional decay
> profile of the RV *rank trajectory* given its current level and path, on multiple clocks, with the
> term-structure slope as a continuous covariate rather than an inversion flag — requires its own
> preregistration block, written against the directive, before any code exists.

**Where this came from.** The SJM reproduction's own diagnostic (state-vs-RV AUC 0.85-0.95) reduces the
jump model's state to a persistence-regularised volatility threshold; the honest present-state question
raised by that closure was not "is the state elevated" (Screen 0's object) but **"is it elevated and
about to leave, or elevated and going to stay"** — duration, not level. The jump model itself is **not**
added as a seventh coordinate here: Screen 0's RV band already stands in for that class (the reproduction's
own Y1/Y2 verdicts showed the two are near-equivalent outside the deepest tail), and reaching for the jump
model because it happens to be built in this repository is exactly the P12 defect. RV is the vehicle.

**Literature — one source [UNREAD], stated rather than hidden.** Chen Xie, "Asset Pricing Implications of
Volatility Term Structure Risk" (SSRN 2517868, 2014) proposes a regime-switching rare-disaster model in
which the VIX term-structure *slope* is a market-implied statement about expected disaster **length** — a
downward-sloping curve prices a longer disaster. **The full text could not be obtained**: SSRN returns 403
to both direct fetch and its citeseerx mirror, and the mirror's own fallback (web.archive.org) is also
unreachable from here. Only the abstract-level mechanism is used below, corroborated by two independent
search summaries; **no quantitative claim in this document rests on unread material**, matching this
repository's own precedent for an uncited source (`CHARTER.md` §9.2, Garcia 1998 / Carter & Steigerwald
2012). Lunde & Timmermann (2004, *JBES* 22(3):253-273) independently establishes the general mechanism —
bull/bear regime hazard depends on age — on Bry-Boschan-style directional regimes, without any VIX
comparison. No paper testing the specific comparison below was found.

**Two stages, cheapest first (P13).** Stage 1a needs no VIX3M data and gets far more history; only if it
clears does stage 1b spend the short joint window on the Xie-flavoured comparison.

### 11a. Screen 1a — does RV's own age predict its own exit?

**Claim tuple.** (daily, hazard of RV-elevated-state exit within `n in {5, 21, 63}` trading days, functional
= empirical hazard by spell-age bucket, sample = `^GSPC` 1970-2026 full history, null = constant hazard
i.e. spell age carries no information — the memoryless / geometric-duration case).

**Mechanism.** If the RV band's exit hazard is flat in age, "here to stay vs. leaving soon" has no content
beyond "currently elevated," and duration is not a describable coordinate at all — the question closes
before slope ever enters. If hazard varies with age (Lunde-Timmermann's finding, on a different regime
definition), age itself is informative and stage 1b becomes worth running.

**Effective n, measured before the run, not asserted.** Computed directly from the existing `(75,55)` RV
band (`screen0.py::hysteresis_band`, `BAND`): **27 spells over the full 1970-2026 history (56.4y)**, median
147d / mean 184d; **15 spells over 1990-2026 (36.6y)**, median 151d / mean 214d. This is the same
effective-n wall this repository's README §4 already names for systemic-episode counting (~10-15). **A
hazard curve fit on 15-27 spells is a description of a handful of episodes, not an estimated function** —
stated now so a later result cannot be over-read.

**Predicted outcome, before code.** Age-dependence is very likely present in *some* direction (long
elevated spells statistically must show declining raw exit-count density late in life simply from
survivorship of the ones that dodged early exit) — the informative question is whether it is large relative
to the sampling noise from ~20 spells, not whether a point estimate moves. **My prior: any age-hazard curve
will be visually suggestive and statistically unresolvable at this n** — a plausible INCONCLUSIVE, not a
NULL, and that distinction must be preserved in the writeup.

**What would surprise me.** A hazard pattern that survives a block-bootstrap or spell-permutation null
(shuffle spell order, not spell content) at conventional confidence — that would be a real, reportable
description of RV persistence structure, independent of anything below.

**Construction.** Kaplan-Meier-style empirical survival function over spell age (no parametric hazard
form imposed); non-overlapping spells only; sensitivity to the `(75,55)` band already fixed by Screen 0
(not reselected here — reselecting a band after seeing a duration result would be selection on outcome).

### 11b. Screen 1b — conditional on RV's own age, does the VIX/VIX3M slope add anything?

**Only runs if 1a's hazard-vs-age pattern survives its own null.** Skipping stage 1a and going straight
to slope would let slope absorb what is really just RV's own age effect.

**Claim tuple.** (daily, hazard of RV-exit within `n in {5, 21, 63}` days | RV state + RV spell-age,
functional = added hazard-model term for VIX/VIX3M slope, sample = joint window 2010-2026 set by VIX3M's
2009-09-18 start, null = slope adds nothing once RV's own age is already in the model).

**Effective n, measured, not asserted.** In the joint window: RV has **9 spells** (median 102d, mean
129.8d); the slope's own elevated state has **95 spells but median dwell 1 day, mean 3.2 days**
(`screen0.py` output, 2026-08-25 run) — it is closer to a same-day co-movement flag than an independent
persistence signal. **Predicted outcome, before code: INCONCLUSIVE by construction is the likely honest
result**, not a discovery either way — 9 RV spells cannot support a second covariate's coefficient with
any power, and this is written down now specifically so a null here is read as underpowered rather than
as evidence slope carries nothing.

**What would surprise me.** If slope's coefficient is large, consistently signed across both halves of
the joint sample, and survives even with 9 spells — an effect that big would be worth a dedicated,
longer-history proxy for the term structure (VIX vs. VIX futures rather than VIX3M) before any charter is
argued, since 9 spells alone could never license the claim on its own.

**Construction.** Cox-type proportional-hazards form, RV spell-age as the baseline and slope-at-onset
(and slope's own trailing state) as the added covariate; report the coefficient, its confidence interval
at the honest n, and a likelihood-ratio test against 1a's baseline-only model. No new coordinate, no new
band; slope's definition is the one Screen 0 already fixed (`VIX/VIX3M > 1.0`).

### 11c. Clearance against PARKED, restated for the duration functional specifically

| boundary | why this is outside it |
|---|---|
| **F9 — all trigger rules** | the output is a survival/hazard curve and a coefficient with a confidence interval, never a threshold or an action. **If the only sayable sentence becomes "so de-risk when the hazard is low," it is F9 and stops there** — identical to §8's rule for Screen 0 |
| **the jump-model reproduction, `PARKED` note in `repro_sjm2024.py`** | the jump model is not used, run, or refit anywhere in Screen 1; RV stands in for the whole persistence-regularised-threshold class, per the reproduction's own Y1 finding |

### 11d. What it may motivate next — exactly one thing, or nothing

If 1a survives and 1b's coefficient is real despite the small n: the one licensed next step is sourcing a
**longer-history term-structure proxy** (VIX futures curve, not VIX3M, to escape the 2009 floor) before
any duration claim is asserted with confidence. Nothing else. If 1a fails its own null: this whole branch
closes, and the closure is itself the reportable result — "present-state duration is not resolvable from
this coordinate at this sample size," same shape as the closed return-state programme's ending.

## 12. The Screen 1 redesign — corrected 2026-08-25, still not preregistered, no code exists

**This section is not a preregistration.** It records what the redesign's object must be, and one
correction to the object named on 2026-08-25 morning, so that the preregistration written next is
written against the right thing. Nothing here authorises a run.

### 12a. The correction: the *unconditional* decay profile is nearly information-free

The object named after Screen 1's withdrawal was the **local-projection decay profile** — for
`x_t = log(range-based vol_t)`, one OLS per horizon:

```
x_{t+h} = a_h + b_h * x_t + e_{t+h}          h = 1 ... 120
```

with the curve `b_h` versus `h` as the deliverable. That is model-free and it does respect the
filtration-not-states directive. But with a single regressor its population value is

```
b_h = Cov(x_{t+h}, x_t) / Var(x_t) = rho(h)
```

— **the autocorrelation function of log volatility, estimated horizon by horizon.** And the log-vol
ACF of equity indices is already established in print: slow, near-hyperbolic decay with `d` around
0.4 (Andersen, Bollerslev, Diebold & Ebens 2001; Andersen et al. 2003 *Econometrica*). The
unconditional profile will reproduce a published result.

**Disposition: the unconditional curve is demoted to a calibration check, and labelled as one.** Its
value is that it verifies our *measurement* — that Parkinson (or Garman-Klass) volatility on daily
OHLC recovers a known shape despite its five documented defects (discretization bias downward,
missing overnight gaps, jump contamination, drift sensitivity, non-synchronous index highs). Passing
it licenses the measurement. It is not a finding about markets and may not be reported as one.

### 12b. The informative object: the *level-conditional* profile

The question in §1, and in the directive, is whether **currently** elevated risk is staying or
leaving. A single `b_h` per horizon assumes the decay rate is the same from a high starting point as
from a low one — **which is the question itself, assumed away.**

There is strong prior reason to think that assumption is false, and it is priced rather than
estimated: **the VIX term structure inverts when spot VIX is high** and slopes upward when it is low.
That is the options market stating in a tradeable instrument that mean reversion from elevated levels
is faster than from quiet ones. A single-slope local projection averages the two and reports a number
belonging to neither.

So the object becomes decay as a continuous function of the **starting rank**, not of a state:

```
b_h(u) = d/dx E[ x_{t+h} | x_t = F^{-1}(u) ]        u in (0,1)
```

Read down a column and the answer is "from the 90th percentile, at what rate does it come back." No
binarization, no spell, no hazard, no elevated/quiet panel — the directive is satisfied by
construction, because the conditioning variable is a continuous rank and the output is a rate.

**Literature terms for the preregistration to cite:** state-dependent local projections (Ramey &
Zubairy 2018 *JPE* — the threshold version), quantile autoregression (Koenker & Xiao 2006 *JASA*),
nonlinear/nonparametric local-projection validity (Goncalves, Herrera, Kilian & Pesavento — read for
the caveats before choosing the form), and in the volatility literature the phenomenon itself is
**level-dependent mean reversion in variance**.

**Claim status, per [[CLAUDE]] §6.3.** That reversion is faster from high volatility is an
**established regularity** in the options-pricing and volatility-targeting literatures and is visible
in the VIX curve. Whether it is present, and how large, in *daily range-based volatility on this
sample under honest overlapping-horizon inference* is an **unresolved question**. That gap is the only
reason to run anything.

### 12c. The kill condition, to be preregistered verbatim

Two ways this thread dies, and both are cheap:

1. **`b_h(u)` is flat in `u`.** Decay from the 90th percentile matches decay from the 50th. Then "is
   current elevated risk staying" has the answer *"the same as always — there is nothing conditional
   to know"*, the present-state description collapses to the unconditional ACF, and the thread closes
   on one afternoon's measurement.
2. **`b_h(u)` slopes, but says nothing the VIX/VIX3M slope does not already say.** The slope is free,
   forward-looking, and available daily since 2009-09-18. Its known defect is that it is a Q-measure
   object contaminated by the variance risk premium (Dew-Becker, Giglio, Le & Rodriguez 2017 *JFE*:
   only ~1-2 months of variance-shock persistence is actually priced). **If our physical-measure
   profile is redundant against it, the thread closes.** This comparison is preregistered as the kill
   condition, not bolted on after a favourable result.

Survival requires slope *beyond* what the curve already prices. That would be a continuous, stateless,
public-data risk-description result — and it would name the model family to fit next rather than
authorising one.

### 12d. Inference constraints, inherited and non-negotiable

Named now so the preregistration cannot quietly omit them:

- **Overlapping horizons.** `e_{t+h}` is serially correlated by construction for `h > 1`. HAC
  (Newey-West at lag ~`h`, or Hansen-Hodrick) is mandatory; plain OLS standard errors are wrong by a
  factor growing in `h`.
- **Persistent regressor.** Long-horizon regression `t`-statistics diverge when `h/T` does not vanish
  (Valkanov 2003), and `R^2` has a nonstandard limit. No significance claim at the far end of the
  curve; the profile is reported as description.
- **Effective sample at the tail.** Roughly `T/h` non-overlapping blocks — order 66 at `h = 120` on a
  full daily history. That number is written on the figure.
- **Logs, not levels.** Log realized/range volatility is approximately Gaussian (Andersen, Bollerslev,
  Diebold & Ebens 2001); a levels regression would be a statement about 2008 and 2020.
- **Attenuation.** Parkinson carries relative variance ~0.41 — real errors-in-variables in the
  regressor. In the unconditional form this shrinks every `b_h` by a common factor, so the *level* of
  the curve is biased down and the *shape* survives. **Whether that clean separation holds in the
  conditional form, where the noisy regressor enters twice, is an open question to settle before the
  form is chosen.**
- **Form not yet chosen.** Interacted/threshold (few lines, one summary number) versus full quantile
  surface (own HAC treatment, over-resolution risk at long `h`). Given the effective-sample figure
  above, the interaction is the form the data plausibly supports. **Decided in the preregistration,
  before code, and not revisited after seeing a result.**

**The attenuation question above was settled 2026-08-27, by synthetic design study**
(`screen1_design_eiv.py`, no market data), and the clean separation does NOT hold — in a direction
worse than attenuation:

- With a level-dependent truth calibrated to what the VIX curve prices (persistence 0.99 quiet ->
  0.97 stressed) and Parkinson-magnitude noise (`s_u = 0.32` on log vol), the quadratic-summary
  coefficient `c_h` is **detectable at T = 14000**: |c|/MC-sd ~ 3.4 at h = 1-21, falling to 1.7 at
  h = 63 — the far end is description only, as already stated above.
- **Noise does not attenuate the curvature — at short horizons it inflates it** (x11 at h = 1, x3 at
  h = 5, x1.3 at h = 21). Mechanism: with a non-Gaussian marginal, `E[x_t | x*_t]` is itself
  nonlinear in the observed value, so curvature is injected by the *distribution's shape* under
  noise, not by the dynamics. It happened to share the true effect's sign here; its magnitude is an
  artifact. **No magnitude of `c_h` may be interpreted; only detection against a calibrated null.**
- The flat-truth simulation false-fired at ~0% — but only because its marginal was Gaussian by
  construction. A level-independent null on real data can still be skewed, which would inject
  spurious curvature through the same mechanism.

**Consequences for the preregistration, binding when it is written:** (1) the form is the
quadratic/interacted summary `c_h` — the surface is over-resolution at this effective sample;
(2) the flatness test is scored against a **simulation-calibrated null** — a level-independent
process fitted to the data, with the measured noise added, never against `c_h = 0` — the same
discipline the deep-tail run used and for the same reason; (3) informative horizons are the middle
of the curve (h ~ 5-21), where true dynamics dominate the injection artifact; (4) the kill
condition's "flat" reads "indistinguishable from the calibrated level-independent null", not
"c_h ~ 0".

### 12e. Sequencing

**Thread A's inference step runs first** (decided 2026-08-25 — see [[docs/REPRO-SJM2024-FINDINGS]]
scope decision). This section waits behind it. That ordering is deliberate: Thread A is one run from
closing, and this repository's queue is capped at two live threads.

## Related

- [[docs/REPRO-SJM2024-FINDINGS]] — where the question came from · [[docs/ASSESSMENT-RETURN-AT-RISK]] —
  the sibling proposal · [[CLAUDE]] §4, §6 · [[docs/RESEARCH-PROTOCOL]] §0, P11, P13 · [[PARKED]] §2, §4
