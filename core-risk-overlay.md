---
type: project
---

# Core-Risk-Overlay

Last updated: 2026-08-18

**Return-state research.** Whether the equity return distribution enters distinguishable, persistent,
identifiable states. **The active program is [[CHARTER]] — read it first.** Process in
[[docs/RESEARCH-PROTOCOL]]. Time-basis rules in [[docs/POINT-IN-TIME-DISCIPLINE]]. Frozen evidence in
[[docs/PROBLEM-MAP]]. Excluded, including the hedging mandate, in [[PARKED]].

**The repository name is historical.** It names a program that no longer runs.

## Status — 2026-08-18, second entry: THE RETURN-STATE TRANSITION

> **The rolled-put / tenor intervention program is CLOSED**, preserved and reproducible at
> [[closed-research/intervention/README]] with its own charter, its four preregistrations, its code
> and its 17 checks. **The active program is [[CHARTER]] — return states.**
>
> **Why it closed, and it is not fatigue.** E0 removed 82–85% of the measured drawdown reduction as
> unrealised mark. E1 showed the remainder is smaller than the spread an arbitrary roll-calendar
> offset produces, and that in cash the *sign* flips with the calendar. E2 repaired the estimand and
> no tenor ordering survived anywhere on the drawdown path in cash. E4 took the last surviving
> structural claim from unconditional to conditional — M1 is a deductible-count effect that wins
> grinds and loses V-shapes — **and the condition is a forecast the prediction program had already
> closed.** The two programs closed each other.
>
> **What the new program studies.** The conditional law of the forward return path,
> `F_{s,h} = law of R_{t:t+h} given S_t = s`. Four questions in order: existence, characterisation,
> transition, identification. **It terminates at identification.** No allocation, no instrument, no
> trigger, no exposure — those need a new charter, not an amendment ([[CHARTER]] §3, §7).
>
> **Two decisions were fixed before the first experiment so neither can be selected on a result
> later.** The null is **N1**, a smoothly-reverting continuous-scale process — the honest opponent,
> and never built in this repository. The frequency is **daily** — E8 established weekly cannot
> resolve the memory any persistence claim depends on.
>
> **The queue holds one item: S0, the identification problem itself**
> ([[docs/STUB-S0-WHAT-COUNTS-AS-EVIDENCE]]). Q1 is not designable until S0 fixes the functional and
> the horizon. Q2 and Q3 do not exist as experiments.

## Status - 2026-08-18 — first entry, E0


> **E0 RAN 2026-08-18 AND IT IS THE LARGEST CORRECTION IN THE REPO.** The measured drawdown
> reduction is **mostly an unrealised mark**: 82% of the 52-week figure on the full sample, 85% on
> 2003-. **+16.8pp and +19.9pp both become +3.0pp in cash**, the cash reduction is flat from 26w to
> 52w, and at 4w/13w it is *negative* -- the program deepens the worst drawdown. In the well-sampled
> `CDaR_alpha` coordinate the full-sample cash reduction at 52w is zero to slightly negative at every
> alpha. E10's tenor ordering survives in **sign** and not in **magnitude**. Section below;
> preregistration and full result in [[closed-research/intervention/STUB-E0-M3-DECOMPOSITION]].
> **PROGRAM TRANSITION 2026-08-17. The prediction/regime program is CLOSED.** It is preserved,
> self-contained and reproducible, at [[closed-research/README]] -- completed research, not obsolete
> code, and not an active branch. The active program is **drawdown intervention design**: [[CHARTER]],
> which is the only research question and the only experiment queue in this repository.
>
> **Why.** The model's forward-downside information is nested inside VIX on levels (D3) and dynamics
> (F2); the clairvoyant ceiling bounds any timing rule near +3pp/yr where it has been measured; and
> the variable that dominated outcomes -- option tenor -- had been fixed by assumption while the
> variable that did not got the research. *The old program's failure was in what it held constant,
> never in how carefully it measured.* Full amendment, including the precise scope of the closure and
> what is prohibited from reopening: [[docs/PROBLEM-MAP]] Part I.
>
> **The closure is scoped, not universal.** It covers public return-volatility estimators, for
> decision purposes, on SPY, against VIX, at h=4 and h=13. Credit, funding, breadth and positioning
> were never tested -- out of scope, not refuted. And the EVPI ceiling exists only at 4w/13w, the
> tenors the structure map says are dominated; [[CHARTER]] E3 closes that corner or shows it
> undecidable.
>
> **The founding arithmetic is withdrawn.** [[README]] §2 held that premium drag would be smaller than
> the drawdown avoided. E9 measured it: 0 of 40 structures beat the naked book on CAGR, both samples.
> The overlay is a **purchase** of a different outcome path at a cost in compound return. That is
> price discovery, and it moves preference explicitly downstream of research.

## Governing frame — HISTORICAL, superseded by [[CHARTER]]

> **Everything from here to the "Next" section is the chronological record of two closed programs and
> stands as written.** It is not the active frame and does not govern anything. Rules 1-4 below were
> the prediction program's; rule 4 (width is not direction) survives verbatim into [[CHARTER]] §4,
> and rule 3 (check the data and the frequency first) is why the active program is daily. The rest is
> history.

Rules 1-3 have each been broken by this repo at least once. They exist because the documents kept
asserting the right principle while the practice reverted. Rule 4 is the one rule added *before* it
was broken, and it is now binding architecture rather than a preference.

**1. The model's content is `P`, not a level.** A Markov-switching model's claim is about
*persistence* — how long a state lasts, how belief decays, how the forecast reverts. Every test
run through 2026-08-13, including D3, collapsed it to a **scalar** (a VaR or ES number) and raced
that against VIX's scalar. VIX is a spot price with no memory structure, so a level-vs-level test
**structurally cannot see** what this model knows. Protocol §1.2 already said this and every
subsequent experiment scored levels anyway. Before proposing a test: *what does the model claim to
know that the comparison object does not?* If a test could be passed by a constant rescaling of
VIX, it is not testing this model.

**2. The model never decides what, where or how to trade.** It reports risk. Strikes, tenors, roll
schedules, hedge ratios, premium and P&L are not the working surface — [[README]] §5 has said so
from the start, and on 2026-08-13 three consecutive runs drifted into option mechanics anyway
before being stopped. Economic viability is the long-run goal, not the near-term reasoning surface.

**3. Check the data and the frequency before reasoning about model shape.** The weekly series
cannot resolve volatility memory at all — at n=1750 the ACF band is ±0.0469 and the empirical
squared-return ACF is inside it by lag 8. A year of argument about regime counts and tail shapes
happened on a series that could not have settled any of it.

**4. The model measures WIDTH. Direction is a separate layer that does not exist.** Established
empirically, not assumed: volatility separates 2.4x (SPY) / 1.8x (QQQ) across probability bins and
replicates, while the drift difference **reverses sign between the two assets** and the down/up
tail ratio straddles 1.0. So `wide` never licenses `bearish`, `short`, or `to cash`. Sizing on
width is legitimate **only** as variance targeting, and the reason must be written next to the
line — identical code, different research obligation. Full contract, forbidden patterns, and the
status of every "beyond simpler measures" comparison: [[closed-research/docs/TRANSLATION-LAYER]].

The question is unchanged ([[README]] §3): *how well does a Markov-switching model provide
real-time information about Value at Risk and the tail risk of equity assets?* **Real-time**
excludes smoothed probabilities by definition.

[[docs/RESEARCH-PROTOCOL]] is preregistered. `src/evaluation.py` scores whatever it is handed and
knows nothing about which model produced it, which is what turns the specification argument into
an experiment.

## Target

> Each week: is there a real, **systemic** threat to a long global equity book, large enough that
> paying for a hedge is worth it?

The book is permanently long SPY / QQQ / international and is never sold. The hedge is a small USD
sleeve buying SPY puts, monetized in a crash and recycled into the core at lower prices. Goals:
smooth the ride, cut drawdown depth, stay invested.

Two properties this implies that the current model lacks:

- **Systemic, not single-asset.** SPY alone wobbling is noise; SPY + QQQ + international falling
  together is the event. Those correlate 0.77-0.87 weekly.
- **Continuous in principle, saturated in practice.** *Not* near-binary by construction — the
  conditional variance is continuous in the mixture weight and sweeps the whole range between the two
  regime variances. It saturates because the fitted components are far apart ($\sigma$ 1.50% vs
  3.84%, a 2.6x ratio), so one bad week moves the likelihood ratio almost all the way: the top-20
  probability weeks all sit at P ≥ 0.99999. A property of the fit, not of the model class.

## Open questions

Positions stated, not hedged. None is a tuning question.

1. **Is the target variable right?** *Probably not.* The model estimates the latent state of return
   *variance*; the mandate is about forward *drawdown* over weeks to months. These diverge badly —
   2022 was -24% over 39 weeks at unremarkable weekly volatility, while a single -8% week that
   recovers is high-variance and harmless. Subsumes most of the others. The protocol's answer is to
   score the predictive density directly rather than argue about the target.
2. **Is a discrete-regime model the right class?** *Not alone.* ARCH-LM on standardized residuals
   rejects at 55.6 (p = 2.4e-11) *after* regime-switching — volatility keeps moving within regimes.
   Not because MS(2) has "only two conditional variances" — it has a continuum, via the mixture
   weight. The binding limits are that the weight is driven only by returns through a saturating
   likelihood ratio, and that **the tail decay rate is fixed by the largest regime $\sigma$ alone**:
   a finite Gaussian mixture is Gaussian in the far tail for any $k$ and any weight. That is algebra,
   and it means **more regimes cannot fix a tail.** Within-regime ARCH and Student-$t$ regime
   densities are S3/S4 in the protocol; S4 is the one aimed at the measured defect. Known in the
   literature since Rydén, Teräsvirta & Åsbrink (1998) — see protocol §11.
3. **How many regimes?** Corrected AIC *and* BIC both prefer **k=3** decisively (ΔAIC 66, ΔBIC 44) on
   real data. k=2 persisted only because [[README]] said so. But k=3 does not fix question 2.
4. **Returns only?** *No.* VIX is free, forward-looking, aligns 1750/1750 weeks. It is the **price**
   side — what acting costs — not a benchmark to beat. Loaded in `data_loader.py`, used by nothing.
5. **Sign-blindness.** Not a bug to patch — it is what modelling variance *means*. Up/down probability
   ratio **1.0000** at |return| ≥ 7% with a common mean; **0.9279** with a switching mean. Follows
   from question 1, and it is why the regime is named `high_variance` rather than anything
   directional.

## Settled by evidence

- **Filtered, never smoothed.** Kim-smoothed probabilities condition on the entire sample including
  the future. Filtered and smoothed disagree at the 0.5 threshold in **9.7%** of real weeks. Guarded
  by two checks.
- **520-week (10-year) minimum history, weekly.** At 260 weeks, walk-forward fits produced degenerate
  parameters (`p[0->0]` to 0.163, `p[1->0]` pinned at 0.999999, a variance collapsing to zero), 6
  label flips across SPY and QQQ, 2-3% convergence failures. At 520: 1 flip, 0-1 failures, 7.3-7.8%
  revision, no degenerate values. **Does not transfer to daily by multiplying by 5** — must be
  re-measured.
- **Post-hoc relabelling is load-bearing.** The high-variance index flips across refits on real data —
  SPY at 2009-01-09, a genuine GFC transition. Any hardcoded index inverts the signal.
- **The data loader must resample daily onto a fixed weekly grid.** `yfinance`'s `interval="1wk"`
  anchors on each series' first observation: SPY from 1993 came back Monday-anchored, from 2010
  Friday-anchored, sharing zero bars. `start=None` silently returned a short window. Both fixed.
- **The 2006-2011 "persistence pathology"** the original constraints existed to prevent **does not
  occur.** The unconstrained high-variance regime is *less* persistent (17.2 vs 44.7 weeks). Those
  constraints were removed.
- **Mixture VaR and ES closed forms verified** against a 40M-draw Monte Carlo to ~1e-5. The
  moment-matched normal approximation errs by 11% of the VaR level at $w=[0.85,0.15]$ — it is wrong,
  not merely imprecise.
- **The primary test has a blind spot, and it is the one this project cares about.** Berkowitz's
  $\rho$ tests autocorrelation in the *level* of $z$. A stochastic-volatility series scored at
  constant volatility passes the full LR at $p=0.07$ while the Ljung-Box on $(u_t-0.5)^2$ rejects at
  $p<10^{-16}$. Unabsorbed volatility dynamics are a $z^2$ phenomenon. A passing Berkowitz is
  meaningless without the companion statistic — enforced by a check, documented in both the
  docstring and protocol §5.1.
- **The censored Berkowitz separates from the full one on exactly the case it is for.** Standardized
  $t(4)$ scored as $N(0,1)$ — zero mean, unit variance, no dependence, wrong only in the tail — gives
  full $p=0.89$, censored $p=4\times10^{-37}$. Measured, not asserted.

## Known defects

| what | where | severity |
|---|---|---|
| **No dynamics test exists** — every experiment scores levels | whole repo | **the live gap** |
| Daily minimum history still unmeasured; 520 is a weekly figure | `RELIABLE_MIN_OBSERVATIONS` | blocks any daily model fit |
| Squared daily returns are a noisy variance proxy; attenuates long-lag ACF | `memory_diagnostic.py` | blocks the shape question |
| DQ, tick loss, ES bootstrap unbuilt | `src/evaluation.py` | deprioritized — level-based (D3) |
| ~~No vintage-parameter VaR path~~ | ~~`walkforward.py`~~ | **fixed 2026-08-13**, `walkforward.py density` |
| Base specification's tail is ~2.8x too narrow at $\alpha$=0.05 | model class | the finding, not a bug — S3/S4 exist for it |
| Parameter look-ahead in the convenience path | `markov_switching.estimate_high_variance_probability` | documented in the docstring; walk-forward path is the honest one |
| ~7.5% of weeks have their state revised by later refits | model class | reliability number, protocol R4 |
| ~1-2% of refits fail to converge | `markov_switching.py` | policy fixed in protocol §4.5, not yet coded |
| Signal timing unresolved — no weekly close exists at Friday 3:30pm | operational | leak register #3 |
| Daily minimum history unmeasured | `RELIABLE_MIN_OBSERVATIONS` | blocks quoting any daily result |

## Working lesson from 2026-08-12

**Most of this repo was analysis apparatus built while the base was unsettled, and it did active harm
rather than merely wasting effort.** 2065 lines documenting a 2-regime model made k=2 feel decided
when the repo's own diagnostics said k=3. A 764-line diagnostics suite nobody had read produced
numbers that entered permanent documents as fact — including a QQ standardization bug found the first
time it was actually reviewed. That suite is deleted; the documents that cited its line numbers had to
be rewritten.

Two rules that came out of it:

- Sort findings into **deductive** (code does X, math implies Y — solid as stated) and **inductive**
  (this beat that on these episodes — needs a rule-based test bed and honest effective-n, which is
  episodes, not configuration rows). They were being quoted with equal confidence.
- **Fix the design and the kill thresholds before running.** That is now
  [[docs/RESEARCH-PROTOCOL]] §7.

A third, from the naming sweep: **a wrong name is a load-bearing defect.** `jump_model.py` implemented
a Markov-switching model while "statistical jump model" is an established name for a different method.
Every document inherited the confusion.

## Possible output: a paper

A **long-run** goal, not a near-term deliverable — but recording it disciplines the work rather than
adding to it. A paper audience will not accept metrics invented after seeing the data, hand-picked
crisis windows, or economic results without a calibration test. That is exactly the standard
[[docs/RESEARCH-PROTOCOL]] sets, and it is stricter than what this project was applying to itself.

The natural shape, if results support one: *does a conditional regime model carry information about
downside risk that is incremental to implied volatility?* Open in the literature, genuinely uncertain,
and a well-executed negative result is publishable and useful. It is also exactly the question that
decides whether this system should exist.

## First honest result — 2026-08-13

**Walk-forward, no look-ahead.** 1,230 out-of-sample weekly SPY forecasts, 2003-01-24 to 2026-08-14.
Parameters refit every 13 weeks on data through the refit point only; state from `filtered[t-1]`;
density formed before $r_t$ exists. Run: `.venv\Scripts\python.exe walkforward.py density SPY`.

**Alignment verified adversarially**, because an off-by-one would invalidate everything: shifting the
realized series so a forecast is scored against a return its own filter already absorbed collapses
coverage to $p=0.0000$. Only the true alignment and the harmless staler direction are sane.

**The body is calibrated. The tail is not, and it degrades monotonically with depth.**

| $\alpha$ | breach rate | Kupiec $p$ | independence $p$ | CC $p$ |
|---|---|---|---|---|
| 0.10 | 0.1049 | 0.571 | 0.657 | 0.772 |
| 0.05 | 0.0528 | 0.650 | 0.384 | 0.617 |
| 0.01 | **0.0179** | **0.012** | **0.006** | **0.001** |

| measure | $\alpha$=0.10 | $\alpha$=0.05 | $\alpha$=0.01 |
|---|---|---|---|
| censored Berkowitz $\sigma^2$ | 1.89 ($p<10^{-4}$) | 2.80 ($p<10^{-4}$) | — |
| ES ratio realized ÷ predicted | 1.108 | 1.171 | 1.216 |

Full Berkowitz LR 8.66, $p=0.034$ — $\mu=-0.008$, $\rho=-0.076$, $\sigma^2=1.044$. PIT uniformity
$p=0.033$. Ljung-Box on $u$ quiet at every lag count (0.06-0.42).

**Ljung-Box on $(u-0.5)^2$ is lag-dependent and must be quoted as a sweep, not a number:**

| lags | 5 | 10 | 15 | 20 | 26 | 52 |
|---|---|---|---|---|---|---|
| $p$ | 0.0004 | 0.0075 | 0.045 | 0.062 | 0.099 | 0.108 |

The dependence is concentrated at lags 1-4 and dilutes as uninformative lags are added. Unabsorbed
volatility dynamics are therefore a **short-horizon** finding, not a general one. **The protocol never
preregistered a lag count** — a real gap, recorded rather than closed by picking one after seeing the
sweep.

**Worst week, and the whole story in one line:** 2008-10-10, SPY $-22.1\%$ against a 1% VaR of
$-6.4\%$. PIT $= 6\times10^{-16}$: the density called it impossible. That is the sample's one clipped
observation, surfaced by the clip counter rather than swallowed.

### The diagnosis: thin tails INSIDE each regime, not bad regime detection

Found 2026-08-13 by looking at Figure 2 and asking why ordinary weeks were breaching.
**16 of the 22 breaches happen while the model believes it is calm**, most at $P(\text{wide}) < 0.10$:

| date | realized | its 1% VaR | $P$(wide) |
|---|---|---|---|
| 2007-03-02 | −4.67% | −3.00% | 0.005 |
| 2005-04-15 | −3.32% | −3.03% | 0.008 |
| 2004-03-12 | −3.32% | −2.93% | 0.008 |
| 2007-07-27 | −5.62% | −3.04% | 0.007 |

2004 and 2005 are not crises. The calm regime has $\sigma \approx 1.5\%$/week, so a Gaussian puts the
1% worst week at $-3.5\%$; real quiet markets deliver $-4\%$ and $-5\%$ weeks far more often.

| model state | weeks | breaches | rate | vs promised |
|---|---|---|---|---|
| believes calm | 929 | 16 | 1.72% | 1.7x |
| believes wide | 301 | 6 | 1.99% | 2.0x |

**Both states are broken by roughly the same factor** — the tell that this is the conditional
*density*, not the regime *classifier*. Three separable failures:

1. **Thin tails** — small breaches ($-3\%$ to $-5.7\%$) in genuinely quiet markets. Majority of cases.
   Also explains 2008-10-10: $P(\text{wide})=0.995$, VaR $-6.4\%$, realized $-22.1\%$. Fix: fat-tailed
   regime densities (S4).
2. **Lateness** — *large* breaches at low $P$(wide) at crisis onset, before the filter switches:
   2020-02-28 ($-11.8\%$ vs $-4.8\%$, $P=0.10$), 2025-04-04 ($-9.5\%$ vs $-6.1\%$, $P=0.16$).
   Fix: daily cadence, or a leading input (VIX).
3. **Neither is fixed by more regimes.** k=3 walk-forward threw `Invalid regime transition
   probabilities` across the run — numerically fragile, and aimed at the wrong defect anyway.

**Read.** The failure is exactly the one open question 2 predicts — ARCH-LM rejects *after*
regime-switching, and two conditional variances cannot track scale in the far tail. Three independent
measures (breach rate, censored $\sigma^2$, ES ratio) agree and all worsen with depth, which is the
signature of a tail that is too thin rather than a level that is mis-set.

**The censored test earned itself immediately.** The full Berkowitz alone reads as borderline
($p=0.034$); the censored version is $p<10^{-4}$ — body-correct, tail-wrong, on real data the same day
the discriminating case was demonstrated on simulated $t(4)$.

**The figures say two things the tables do not.**

- **The QQ panel of the PIT is asymmetric.** The *left* tail falls off the 45-degree line; the right
  tail sits on it. The density is too thin on the downside specifically, not symmetrically fat-tailed.
  That argues for a **skewed** heavy-tailed regime density, not just Student-$t$ — and it is a
  distributional-width finding, not a directional one, so it stays inside the mandate.
- **A 20-bin PIT histogram cannot resolve the failure.** The whole $\alpha=0.01$ story lives inside
  the leftmost bin. Figure 1's histogram looks unremarkable ($\chi^2 p = 0.033$) while the QQ panel
  and the censored LR show the defect plainly. Do not read the histogram as the tail check.

**Figure 2 makes the causal-filter lag concrete.** Through Feb 2020 the 1% VaR sits flat near $-5\%$;
the $-11.8\%$, $-10.0\%$ and $-15.7\%$ weeks all arrive *before* it widens to $-9\%$. Same shape in
2008. This is protocol §7's recorded threat to D5, now visible rather than argued.

**Not a verdict.** D1 requires Berkowitz *and* DQ rejecting across R8 subsamples for *every* §3
specification. DQ is unbuilt, subsamples unrun, and S3 (within-regime ARCH) and S4 (Student-$t$
regime densities) — preregistered precisely for this failure — do not exist yet. **This is the base
specification only**, and it fails where the protocol said to look.

## Context rungs — one-step coverage, harness shakeout (2026-08-13)

**Claim tuple: weekly · $h=1$ · marginal quantile and density · SPY, 1,230 OOS weeks 2003-2026.**
Nothing in this section supports any claim outside that tuple (protocol §0.1).

Protocol step 3, `baselines.py`. Constant (expanding mean/sd) and EWMA
($\sigma^2_t = \lambda\sigma^2_{t-1} + (1-\lambda)r^2_{t-1}$, $\lambda$ reported as a sweep, never
tuned) scored by the identical battery on the identical 1,230-week sample.

**Ranking, mean tick loss $\times 10^4$ — lower better:**

| | 10% | 5% | 1% |
|---|---|---|---|
| MS model | **42.71** | **27.73** | **9.92** |
| EWMA 0.94 | 43.77 | 28.54 | 10.77 |
| constant | 46.38 | 30.20 | 11.10 |

The model wins at every level and **Diebold-Mariano finds none of it significant** (vs EWMA 0.94:
$p$ = 0.24, 0.30, 0.077). It beats the *constant* significantly at 10% ($p<0.001$) and 5%
($p=0.011$) — so conditioning on something helps; conditioning on *regimes* specifically is not
demonstrated.

**Density calibration — EWMA 0.97 beats the model:**

| | Berkowitz $p$ |
|---|---|
| EWMA 0.97 | **0.237** passes |
| EWMA 0.94 | 0.070 |
| MS model | 0.034 fails |
| constant | 0.027 fails |

**No verdict is available here, and none ever was.** At $h=1$ the MS model and a tuned EWMA have
near-identical conditional variances by construction, so a DM null is what theory *predicts* rather
than information about the model. RiskMetrics EWMA is IGARCH — its multi-step variance forecast is a
martingale and never reverts; MS(2) reverts toward the stationary regime mix at a rate set by the
second eigenvalue of $P$. That is the entire structural difference between the two, and it is exactly
zero one step ahead. **D2 may not be evaluated against this comparison** (protocol §0, standing
consequence).

**Recorded because the rule came from it.** This section was previously headed *"the model does not
beat a moving average"* and called the outcome *"a thin return on a Hamilton filter."* The first
exceeded the claim tuple; the second inferred an economic judgement from a loss function, when
economic value is gated on D5 and has never been measured here. The protocol already forbade all of
it — the header says "Not a horse race," §3 requires a preregistered expectation, and §11 cited the
paper that answers the specification question. Protocol §0 is the gate that now runs before code.

### The most important number on this page

**Every method breaches ~2x at $\alpha=0.01$:** MS 1.79%, constant 1.87%, EWMA 0.97 2.03%,
EWMA 0.94 2.36%. What they share is the **Gaussian assumption**. The 1% failure is therefore a
property of the *data*, not a defect of the regime model, and **no Gaussian-based estimator of any
complexity can fix it**. This is the strongest evidence yet for fat-tailed conditional densities —
and it means the fix applies to EWMA too, without a custom Hamilton filter.

### From `figures/rungs_paths_spy.png`

- The model's VaR path is **blocky** — snaps between levels and sits flat, while EWMA glides.
  Saturation of the mixture weight, visible; not a structural binary (see open question 2). This is
  also the whipsaw source: 10 of 36 elevated-risk episodes are single-week blips. Whether blocky is a
  *defect* is undetermined at $h=1$ — a model that holds a level because it believes the state
  persists is doing what a regime model is for. That question lives at horizon.
- **In 2008 and 2020 EWMA went deeper and faster** — reaching $-16\%$ at the 2008 trough against the
  model's $-10\%$.

## Earlier smoke reading — NOT a result

`src/predictive.py` landed 2026-08-12 and the full path runs. On weekly SPY (1,749 forecasts), fitted
**once on the whole sample**, so this carries parameter look-ahead and is not reportable — it is a
smoke test that the plumbing produces sane numbers:

| $\alpha$ | breach rate | Kupiec $p$ | independence $p$ |
|---|---|---|---|
| 0.10 | 0.1109 | 0.134 | 0.724 |
| 0.05 | 0.0555 | 0.303 | 0.782 |
| 0.01 | 0.0114 | 0.555 | **0.020** |

Regimes: high-variance $\sigma$ 3.84%/week, mean -0.26%, expected duration 12.9 weeks; calm $\sigma$
1.50%, mean +0.36%, 36.1 weeks.

**The pattern worth noting:** rates are right at every level, but at $\alpha=0.01$ the breaches
*cluster* — the independence test rejects while Kupiec passes comfortably. That is precisely the
failure Kupiec cannot see and the reason [[README]] §3 calls independence the discriminating test. It
is also what the ARCH-LM rejection predicts: two conditional variance values cannot track scale in
the far tail. Expect the honest walk-forward version to be worse, not better, since look-ahead
flatters.

## D3 FIRED — the model is nested inside VIX on levels (2026-08-13)

**Claim tuple: weekly · h=4 and h=13 · forward downside semivolatility · SPY 2003-2026, 1,230
walk-forward OOS forecasts.** Run: `.venv\Scripts\python.exe encompassing.py SPY`.

`RV[t,t+h] = a + b·IV[t] + c·X[t]`, with RV the forward downside semi-volatility
`sqrt(SUM min(r,0)^2)`, IV log VIX at the same information time, and X the model's own
`-ES(0.05)` from the walk-forward vintage path.

| h=4, non-overlapping n=307 | coefficient | p |
|---|---|---|
| VIX | +0.3616 | 0.0026 |
| model (−ES 0.05) | **+0.0009** | **0.9935** |

| R² | value |
|---|---|
| both together | **0.1015** |
| VIX alone | **0.1015** |
| model alone | 0.0471 |

Joint and VIX-alone are **identical to four decimal places**. h=13 agrees: c = −0.0232 (p=0.9277),
joint 0.1173 against VIX-alone 0.1172.

**Alignment verified adversarially**, because an off-by-one would invalidate it: leaky (window
starts d−1) R²=0.2488 > true (starts d) 0.1015 > stale (starts d+1) 0.0769. Monotone in the right
direction; the leak more than doubles R².

**The null arrives in its strong form.** Low power shows up as a large-but-insignificant
coefficient. c = +0.0009 with p = 0.99 is a coefficient that is actually zero. The model carries
real downside information (R²=0.047 alone) and it is **strictly nested** inside VIX's.

**Preregistered consequence (§7 D3): no capital is committed.** The result is reported.

**The load-bearing caveat.** X was a *level*. This is a level-vs-level test and it is exactly what
governing-frame rule 1 warns about. D3 closes the level-based case; it says nothing about
persistence, which remains untested.

## Memory diagnostic — and a claim of mine that it refuted (2026-08-13)

Run: `.venv\Scripts\python.exe memory_diagnostic.py SPY [--daily]`.

**Deductive result first.** For a two-state switching-variance model with regime variances `v[j]`,
stationary weights `pi`, and `lam = p00 + p11 − 1`:

```
Cov(r[t]^2, r[t+k]^2) = pi_0 * pi_1 * (v_0 - v_1)^2 * lam^k
```

The squared-return ACF decays **geometrically — for any k, any number of regimes, any parameters**.
That is algebra, not a fitted claim, and it holds at all 95 vintages (λ₂ ∈ [0.8921, 0.9929]).

**Weekly (n=1750, band ±0.0469):** median λ₂ = 0.9126, half-life 7.6 weeks. Model lag-1 ACF 0.1754
against empirical 0.2776 — the model captures **63% of the one autocorrelation weekly data can
measure reliably**. Shape test inconclusive: exponential R² 0.4094 against power-law 0.4283, both
poor, H = 0.524. Empirical ACF falls inside the noise band by lag 8, so **decay shape is not
identifiable at weekly frequency at all.**

**Daily built and cached** (`data_loader.download_daily_prices` / `load_daily_log_returns`;
`data/spy_daily.csv`). All 64 checks still pass. n = 8,441, band ±0.0213.

| | weekly | daily |
|---|---|---|
| ACF significant to | ~4-7 weeks (20-35 days) | **lag 212 (~10 months)** |
| fraction of lags significant | — | 54% of lags 1-250 |

Weekly hid ten months of memory behind its noise band. That gain alone justified the frequency
change.

**But the shape claim was refuted.** I asserted confidently that volatility has power-law memory a
Markov chain structurally cannot match, and that MSM or HAR was therefore required. At daily
frequency:

```
lags 1-250   exponential R2 = 0.7192   power law R2 = 0.6219   H = 0.423
lags 1- 63   exponential R2 = 0.8644   power law R2 = 0.7719
lags 1-126   exponential R2 = 0.8094   power law R2 = 0.8264
```

**Exponential wins**, and H = 0.423 is *below* 0.5 — anti-persistent, the opposite of long memory.
The gap is one of **duration, not shape**: the model's implied memory reaches ~138 trading days
against the data's 212, roughly 35% short.

**Three reasons the refutation is itself weak, recorded so neither claim is over-read:**

1. **It flips with the window** — exp / power / exp across 1-63, 1-126, 1-250. Under D4 a verdict
   that flips on window choice is not reportable as stated. This one flips.
2. **The ACF is non-monotone at short lags** — 0.2638 at lag 1 *rising* to 0.2858 at lag 5. Neither
   functional form fits a hump, at exactly the lags carrying the most signal.
3. **An R² race on log-ACF is not a long-memory test.** GPH log-periodogram regression or local
   Whittle estimate the fractional integration order `d` *with a standard error*. A proxy was used
   in place of the test.

**Most likely cause, and it is fixable in scope.** Squared daily returns are a single-draw estimate
of that day's variance — unbiased but very noisy — and measurement error **attenuates the ACF
toward zero at exactly the long lags where long memory would appear**. Andersen & Bollerslev (1998),
already `[skim]` in the reading list. The literature's long-memory results are mostly on realized
volatility from intraday data, which protocol §9 excludes.

## THE DYNAMICS TEST — the model class is closed on both axes (2026-08-14)

**Claim tuple: weekly · h=4 · forward downside semivolatility · SPY 2003-2026, n=307
non-overlapping. One preregistered input, no sweep.** Run:
`.venv\Scripts\python.exe dynamics_test.py SPY`.

The first experiment whose **input matches what the model claims to know**. Scale-free by
construction, so it cannot be passed by a rescaling of VIX:

```
X[t] = Var_4(t) / Var_1(t)        w_1 = xi[t]' P ,  w_h = w_1 P^(h-1)
```

X > 1 means the model expects risk to rise; X < 1 means it expects reversion. Pure `P`.

| | coefficient | p |
|---|---|---|
| VIX | +0.3473 | 0.0003 |
| model (Var₄/Var₁) | **−0.0047** | **0.6255** |

R² both 0.1019 · VIX alone 0.1015 · **X alone 0.0339**. Alignment verified adversarially
(leaky 0.2481 > true 0.1019 > stale 0.0768); c stays insignificant even in the leaky variant.

**Power was reported, not assumed — and it rules out "undetected".** X ranges 0.8019 to 1.3144,
sd 0.1422, coefficient of variation 0.131; 69.8% of weeks have X > 1. Correlation with VIX is
only **−0.5324**, the expected mean-reversion signature, so X is not VIX in disguise. A genuinely
independent, well-varying input with real standalone content that adds **0.0004 of R²**.

**Result, stated absolutely as [[README]] §3 requires.** A two-state Markov-switching model on
weekly SPY returns provides **no information about forward downside risk beyond what implied
volatility already prices — on either level (D3) or dynamics (here)**. Predicted in advance,
both times.

**Why this is a strong negative rather than a weak one:** the prediction was registered before the
run, the alignment was verified adversarially, power was demonstrated rather than assumed, the
input was scale-free by construction, and both axes were tested.

**The structural reason, and it is why more modelling cannot fix it.** `F^returns ⊆ F^market`. The
option market observes the same return path plus everything else. That containment is a property
of the information set, not of the estimator, so no filter, tail shape, regime count, memory
structure or frequency escapes it.

**What this does NOT close.** VIX is **SPY-only** implied volatility. A cross-asset measure is a
genuinely different information set — covariance structure is information a single-asset option
price cannot contain. That argument is structural and survives every result in this file. It is the
only thing that does.

**Daily would sharpen these estimates and cannot change them.** The containment argument is
frequency-invariant. Daily is worth building for the *memory* question; it is not a route back into
this one, and proposing it as one would be the goalpost-moving this repo keeps catching itself at.

## STATE CHARACTERISATION — what the states actually describe (2026-08-14)

**Claim tuple: weekly · h=1 · contemporaneous realized environment (volatility, drift, tail
asymmetry, episode duration, drawdown position) · SPY 1,230 OOS weeks 2003-2026 and QQQ 898 OOS
weeks 2009-2026, vintage parameters.** Run: `.venv\Scripts\python.exe state_character.py [SPY|QQQ]`.
Figure: `figures/state_character_<ticker>.png`.

The first description of the **state** in observable market terms. Everything prior scored the
**density**; everything known about the regimes came from fitted parameters on a single whole-sample
fit. No forward window, no regression, no VIX column, no rule.

**Q1 — can the states be told apart? Yes, on width, and it replicates.** Realized volatility is
monotone across all six probability bins on both assets.

| | realized vol ratio wide/calm | block-bootstrap 95% CI | fitted σ ratio |
|---|---|---|---|
| SPY | 2.446 | [1.823, 3.124] | 2.560 |
| QQQ | 1.791 | [1.316, 2.184] | 2.477 |

Stable across sample halves (SPY 2.559 / 2.372; QQQ 1.714 / 1.638). **The direction was entailed** —
`w_wide[t]` is driven by `r[t-1]` through the likelihood ratio and volatility clusters — and is
recorded rather than claimed. The magnitude and the monotonicity were not.

**One thing does not replicate.** On SPY the fitted ratio (2.560) nearly equals the delivered one
(2.446); on QQQ the fit overstates its own discrimination by 38% (2.477 vs 1.791). "The fit does not
exaggerate its separation" is a **SPY fact, not a model fact.**

**Q2 — what do they look like? A width axis with no direction content.** This is the sign-blindness
finding reappearing out-of-sample on the state bands rather than on the fitted parameters:

| | drift, wide − calm | Welch t | down/up at \|r\|≥3%, wide | calm |
|---|---|---|---|---|
| SPY | −0.24%/wk | −0.78 | 1.12 | 1.00 |
| QQQ | +0.46%/wk | +0.91 | 0.83 | 0.90 |

**The two assets disagree on the sign of the drift difference and the down/up ratio straddles 1.0.**
That is as clean a demonstration as this sample can give that the state is a statement about
**width, not direction.** The Welch *t* is quoted without a *p*-value on purpose — the observations
and the band assignment are both autocorrelated, so a nominal *p* would be badly oversized.

**The trap, flagged because the figure makes it inviting.** SPY's `[0.99,1.00)` bin shows −60.9%/yr
drift on **n=28 weeks**, a handful of overlapping episodes. QQQ's same bin shows **+131%/yr on n=5**.
Reading either as a directional signal is exactly the error [[README]] §4 names. The figure carries
a footnote saying so.

**Persistence — the model misdescribes its own.** The one property this model class claims that a
spot measure lacks:

| | fitted expected duration, wide | realized mean band run | median | 1-week blips |
|---|---|---|---|---|
| SPY | 12.9 weeks | 5.1 | 2 | 34.2% |
| QQQ | 26.7 weeks | 4.3 | 3 | 23.5% |

**The realized run lengths are stable across assets (5.1, 4.3) while the fitted duration parameter is
not (12.9, 26.7).** SPY's second half is worse than its first (3.2 vs 7.6 weeks). **Caveat that keeps
this from being a test:** a band crossing is not a state transition, so a threshold on a continuous
probability necessarily crosses more often than the latent state switches. Part of the gap is
mechanical and this is an order-of-magnitude reading, not a calibration result.

**Drawdown position — the cleanest replication in the run, and the most decision-relevant table.**
Depth below the running peak, past data only:

| | mean dd when wide | median | % of wide weeks at a peak | mean dd when calm |
|---|---|---|---|---|
| SPY | −15.90% | −13.08% | 10.4% | −3.04% |
| QQQ | −15.52% | −13.54% | 12.3% | −2.75% |

**By the time the model says "wide", the book is already ~13% below its peak at the median.** This
is the causal-filter lag of §"Figure 2 makes the causal-filter lag concrete" expressed for the first
time in the **mandate's own variable** — depth, not variance. Partly mechanical in direction (a wide
state follows bad returns, which put you below peak); the magnitude is not entailed, and it lands
within 0.4pp across two assets.

**A prediction of mine, refuted.** I predicted from the saturation finding that the ambiguous band
would be nearly empty and an abstain path would have nothing to fire on. **It is 17.6% of SPY weeks
and 13.8% of QQQ weeks**, with only 9.0% / 5.5% of weeks outside `[0.01, 0.99]` and median `w_wide`
0.073 / 0.030. It is a *state*, not a transit corridor — its transition diagonal is 66.7% / 65.3%,
median run 3 / 2 weeks. The saturation claim above is about the **extreme top** (top-20 weeks at
P ≥ 0.99999) and the blocky VaR path, and both stand; what does not stand is the natural reading
that the signal is effectively binary. Recorded as a correction of a plausible misreading, not of a
stated claim.

**Stated precisely, because the loose version jumps A→C** (protocol §0.2 P3): what is measured is
**occupancy** — the ambiguous band is populated and persistent rather than empty. That an abstain
branch would have something to fire on is **not** evidence that abstaining is useful, which is a
question C and untouched. An earlier phrasing here — *"the abstain path is available"* — elided the
two and is retracted.

**QQQ is a weak replication and must not be quoted as an independent one.** Its OOS window starts
2009-03-06 — the 520-week burn-in swallows the GFC entirely — and QQQ correlates 0.87 with SPY
weekly. Effective sample is far below 1,230 + 898.

**Scope.** All of the above is measurement and interpretation. Whether the description is
*incremental* to what a downstream user already observes is **not** asked here and is not answerable
from these tables; for SPY it is already answered **no** on levels (D3) and dynamics, and nothing
above reopens either. No rule, threshold, sizing or action is proposed.

## Hedge economics — measured before the strand was legitimised (2026-08-13)

Two runs happened while the measure-vs-instrument boundary still applied to everything. That boundary
was scoped to the research strand on 2026-08-14 and the scope reset of 2026-08-15 makes **this the
main strand**. The line that used to head this section — *"nothing should be built on this strand"* —
is **retracted**. It was written when the signal program still looked like the source of value.

- `hedge_economics.py` — [[README]] §2's inequality (*"premium drag smaller than the drawdown
  avoided"*) measured for the first time. Naked SPY 1993-2026: **+10.82% CAGR, −54.6% maxDD**.
- **A correction is logged inside it.** A first pass priced puts off flat VIX and reported an
  efficiency of 17.58 for 15% OTM. That was an artifact of ignoring the equity skew. With a
  strike-dependent skew (0.60 vol points per 1% OTM) it is **3.6**, and at 5-10% OTM the drawdown
  benefit turns *negative* on the full sample.
- **The robust half:** the clairvoyant ceiling (expected value of perfect information, Howard 1966)
  barely moves with pricing — +2.8 to +3.2pp/yr and +18 to +22pp of drawdown across every skew
  assumption. **Cost of always-on is highly pricing-sensitive; value of timing is not.**
- `trigger_bracket.py` — payoff per dollar of premium: always-on 0.34, best VIX rule (VIX>30) 0.44,
  clairvoyant 2.98. Real VIX rules capture **4% (full sample) to 7% (2003+)** of available selection
  skill, and **no rule beats simply not hedging** on return. Eight rules on ~5 systemic episodes:
  **power to kill, not to confirm.**

## THE STRUCTURE MAP — tenor dominates, and it reorders the project (2026-08-15)

**Claim tuple: weekly marks · full holding period · geometric return and max drawdown · SPY
1993-2026 and 2003-2026 · ALWAYS-ON, h=1.00, NO signal and NO timing anywhere in the design.**
Run: `.venv\Scripts\python.exe structure_map.py SPY`. Grid: 4 tenors × 5 strikes × outright/spread,
skew slope 0.60 primary, 5% offer spread.

**All three registered predictions resolved, and one of them was wrong in a useful direction.**

- **(a) CONFIRMED, unanimously.** **0 of 40** structures beat the naked book on CAGR, in *both*
  samples. README §2's inequality — "premium drag smaller than the drawdown avoided" — **fails on
  average at every point in this grid.** The mandate's founding arithmetic does not hold as stated.
- **(b) SPLIT.** *Long tenor* confirmed decisively. *Deep strike* **refuted** — 30% OTM at 4w and 13w
  buys **negative** drawdown, and the drawdown-bought table is dominated by *shallow* strikes at long
  tenor. "Deep OTM is where tail insurance lives" was wrong.
- **(c) CONFIRMED.** Put spreads top the efficiency table (13.90) and buy 3.3-6.8pp of drawdown
  against outright's 16.8-24.3pp. Cheap, and capped exactly in the tail the program exists for.

**The result — drawdown bought (pp) @ cost (pp/yr), outright, slope 0.60:**

| strike | sample | 4w | 13w | 26w | 52w |
|---|---|---|---|---|---|
| 10% OTM | 1993-2026 | −1.1 @ 3.28 | +1.1 @ 3.39 | **+10.8 @ 2.74** | **+16.8 @ 2.36** |
| 10% OTM | 2003-2026 | +5.1 @ 2.85 | +5.7 @ 2.98 | **+17.8 @ 2.51** | **+19.9 @ 2.49** |
| 15% OTM | 2003-2026 | +4.1 @ 0.94 | +3.3 @ 1.64 | +12.5 @ 1.42 | +16.0 @ 1.70 |

**Cost is flat to falling across the row while protection triples.** This is a dominated region of the
design space, not a trade-off — and the repo sat in it for two years without measuring it.

**Against the clairvoyant bound (2003+, slope 0.60), which is what makes it a project-level finding.**
Always-on 52w 5% OTM buys **+24.3pp @ 3.74**. The *clairvoyant* 4w 5% bound is **+24.7pp**; the
clairvoyant 13w 5% bound is **+14.5pp**. **Choosing the tenor correctly with no signal at all delivers
as much drawdown reduction as perfect foresight at the tenors previously tested.** The apparent value
of timing was substantially an artifact of holding structure at 4-13 weeks.

At matched structure (13w 5%), perfect foresight adds **+1.4pp of drawdown and +8.46pp/yr of
premium**. **A signal is a cost-reduction device, not a protection device** — the first statement of
what a signal is *for* that this repo has derived from the decision rather than from statistics.

**Two things this run refutes about its own predecessor.**

- **Efficiency is not a usable selection metric.** Its denominator goes to zero: at slope 0.00 the
  grid's best efficiency is **218.23 at a cost of 0.03pp/yr** — a structure that protects nothing.
  The script's own warning was right and its footer ("eff … is the right metric for comparing
  STRUCTURES") contradicts it. **Rank on drawdown bought at a stated cost.**
- **The whole grid is conditional on an unverified skew parameterization**, and it favours the
  conclusion. `skewed_vol` scales skew as `sqrt(4/tenor)`, so long tenors are assumed to carry far
  less skew per point of moneyness. The repo has no option chain. Best-efficiency structure swings
  from 4w to 26w and from eff 218 to 9.22 across slope 0.00→0.80. **This is the single largest
  caveat on the finding and it now has a cheap fix** — `options-quant` has archived point-in-time SPY
  chains since 2026-08-14 with 25Δ skew per expiry.

**Not covered, stated so the run is not read as complete:** recycling (`simulate` reinvests passively
at the next roll; never sized deliberately), the honest competitors (trend sleeve, long duration),
and the 26w/52w clairvoyant columns, which do not exist.

## E0 — THE DRAWDOWN REDUCTION IS MOSTLY A MARK (2026-08-18)

**Claim tuple: weekly marks · full holding period · the drawdown process D(t) and its functionals
(CDaR_alpha curve, per-excursion depths, time under water; max drawdown as a labelled diagnostic) ·
SPY 1993-2026 and 2003-2026, one path · ALWAYS-ON h=1.00, no signal, roll phase 0.**
Preregistered in [[closed-research/intervention/STUB-E0-M3-DECOMPOSITION]], committed before the code existed.
Run: `.venv\Scripts\python.exe research/m3_decomposition.py SPY`.

**The experiment is one accounting difference**, and that is the whole design. Same path, same
parameters, same contracts, same cash flows; the only change is *when the hedge is recognised as
wealth*. `W_marked` carries the put's model value continuously — which is what every drawdown number
in this repo has always been computed from. `W_cash` carries it only when it becomes a cash flow, at
expiry, which is the only moment `simulate` has ever actually transacted it.

**The precondition held exactly.** The two curves agree to `0.00e+00` at every roll boundary, at the
terminal date, and on premium and payoff, at all four tenors. Not "close" — zero. So the difference
is entirely interior, CAGR is untouched, and the result is a decomposition rather than a comparison
of two programs.

**H3 is REJECTED**, in fifteen of the sixteen cells where the ratio is reportable, in both samples and
at all three strikes. Drawdown bought, 10% OTM:

| sample | | 4w | 13w | 26w | 52w |
|---|---|---|---|---|---|
| 1993- | marked | −1.1 | +1.1 | +10.8 | **+16.8** |
| 1993- | **cash** | **−4.7** | **−4.8** | **+3.2** | **+3.0** |
| 2003- | marked | +5.1 | +5.7 | +17.8 | **+19.9** |
| 2003- | **cash** | +1.1 | −0.9 | **+4.4** | **+3.0** |

> **+16.8pp becomes +3.0pp. +19.9pp becomes +3.0pp. The best cell in the repo, +24.3pp, has never
> been quoted in cash at all.**

**What this does to E10, the largest measured effect in the repo.** The *sign* of the tenor ordering
survives — long tenor beats short, which is M1, strike anchoring, and it is arithmetic about where the
strike sits rather than anything about pricing. Everything else about the row changes. The cash
reduction is **flat from 26w to 52w**, it is *larger at 26w* on the 2003- sample, and at 4w and 13w it
is **negative on the full sample**: the program makes the worst drawdown about 5pp deeper than never
hedging, because premium is paid continuously and the payoff lands after the trough. The monotone
climb across the marked row is a mark that grows with the length of the block interior — 51
unrecognised weeks at 52w against three at 4w. **Read the marked row as the ordering and the cash row
as the size.**

**In the well-sampled coordinate the cash reduction is approximately zero.** CDaR_alpha, full sample,
52w: cash reduction is −0.5 / +0.0 / −0.2 / −0.6 / −1.0 / −0.8 across alpha 0.01 → 1.00, against a
marked +10.0 → +1.0. The 2003- subsample does show a real cash benefit concentrated at the extreme
end (+0.6 / +3.5 / +2.9 at alpha 0.01 / 0.05 / 0.10), and 26w is stronger there than 52w. This is
exactly the job CDaR was built for: the marked effect decays smoothly in alpha, the signature of a
statistic resting on the deepest part of one episode, and the cash effect has almost nothing to decay
from.

**The mark erases excursions the investor still lives through.** Full sample, excursions deeper than
10%: naked 9, 52w marked **6**, 52w cash **9** — the same nine the unhedged book has. Time under water
at 10%: naked 31.7%, 52w marked 29.1%, 52w cash **34.1%**. **In cash, the hedged book spends more time
under water than if it had never hedged**, because premium drag is continuous and the offset is not.
"Smooth the ride" is one of the mandate's three stated goals, and on this path, at this phase,
measured in cash, the 52-week program did the opposite of it.

**What it does NOT establish, and this matters as much as the rest.** Not that the marked number is
wrong — cash accounting is not the truth either, since a real investor can sell mid-life. The
realizable path under any stated rule lies *between* the two curves. What E0 establishes is that
**the accounting interval is wider than the effect inside it** — 13.9pp of gap within a 16.8pp claim —
so no point in it can be quoted. And it adds **no observation**: one path, one crisis, one unswept
roll phase, effective n = 1 on the benefit side still. The 82% is an accounting fact about this path,
not an effect size.

**Consequences, booked the same day.** E6 (`specify rho, measure kappa`) is reclassified from queued
experiment to **precondition** — no drawdown magnitude in this repository is interpretable until it
runs. E1 (roll-phase sweep) is **promoted**, because how much of a crisis falls inside a block
interior is exactly what phase sets, and that is what the size of the mark depends on. And no number
here may be quoted as a drawdown reduction without naming its accounting.

**One process note, recorded against myself.** The stub declared a denominator floor for `gap_share`
because the denominator was known to approach zero, and then predicted the *ratio* at precisely the
tenors where that floor binds. The floor did its job — those cells print INDETERMINATE instead of
531% — but the prediction should have been stated in pp of gap. F7, twice in one document, in
opposite directions.

**And a second, larger one: the literature gate was skipped.** [[docs/literature/README]] lists
Israelov (2017), *Pathetic Protection*, as **blocking on E0**, and yesterday's carry-over note said
so in as many words. E0 ran first; the paper was read afterwards, on the same day. The verdict is
mixed and worth having in full:

- **E0's design survives.** The paper never distinguishes marked from realized value — zero
  occurrences of *mark-to-market*, *unrealised* or *monetise* in the text, and every drawdown it
  reports is computed on a marked NAV. **The decomposition is not in the literature.** Honouring
  the gate would have changed nothing about the run.
- **But E10 was a rediscovery.** The paper sweeps 20 / 63 / 250 business-day maturities — our 4w /
  13w / 52w — and concludes that *"longer-dated options do a less bad job of protecting a portfolio
  against long-term drawdowns than shorter-dated options. Less bad, but not good."* That is E10's
  ordering and, in cash, roughly E0's magnitude, in a paper sitting `[UNREAD]` as **row 1** of the
  reading list while both were derived from scratch. Second §0-rule-3 failure in this repo's
  history; the first was Timmermann's Proposition 5, also row 2 of a list at the time.
- **E1 is respecified by it.** The paper's central mechanism is expiration-cycle misalignment:
  *"equity drawdowns have lives of their own that may not conveniently coincide with option
  expiration cycles."* That phase matters is therefore **citable, not testable**, and a run showing
  it carries no information. E1 now measures the quantity the paper does not supply — the **phase
  spread relative to the effect**, which is what H2 actually turns on.
- **Its remedy is inadmissible here, and that is the load-bearing difference.** The paper's
  comparison alternative throughout is static divestment — 36.5% equity, 63.5% cash, matched to
  PPUT's realized return. [[CHARTER]] §2's C2 excludes exactly that. **Its verdict does not bind
  this mandate; its mechanisms bind it completely.** The permanent-long constraint is what makes
  the paper's recommendation unavailable and its evidence entirely relevant — which is the worst
  possible combination to have skipped.


## E1 — THE TENOR MAGNITUDE IS ALIGNMENT-DEPENDENT (2026-08-18)

**Claim tuple: weekly marks · full holding period · drawdown bought versus the naked book, on max
drawdown and on `CDaR_0.05` · SPY 1993-2026 and 2003-2026, one path · ALWAYS-ON h=1.00, 10% OTM, no
signal and no conditioning of any kind.** Preregistered in [[closed-research/intervention/STUB-E1-ROLL-PHASE]], committed
before the code existed. Run: `.venv\Scripts\python.exe research/phase_sweep.py SPY`.

**E1 asked one question and answered it.** `simulate` walked blocks from index 0, so the alignment of
every roll against the 2007-09 decline was set by the sample's first date and nothing else. The sweep
moves the roll grid without moving the sample -- at phase `p` the first block is a stub of `p` weeks
-- and reports the resulting spread **relative to the tenor effect it is supposed to qualify**. Every
offset, no selection: 4 + 13 + 26 + 52 alignments per accounting per sample.

**Verdicts against the rule fixed before the run:**

| sample | acct | effect | spread at 52w | R | verdict |
|---|---|---|---|---|---|
| 1993- | marked | +18.0 | 12.7 | 0.71 | MARGINAL |
| 1993- | **cash** | +7.6 | 14.1 | **1.85** | **KILLED** |
| 2003- | marked | +14.7 | 12.5 | 0.85 | MARGINAL |
| 2003- | **cash** | +1.8 | 12.6 | **6.82** | **KILLED** |

Nothing anywhere reached the preregistered SURVIVES threshold of `R <= 1/3`. In `CDaR_0.05`, the
declared artifact check, the ratios are 0.79 / 1.41 and 1.14 / 4.10 -- **the sensitivity is not a
max-drawdown artifact**, and on the 2003- marked cell the CDaR ratio would have flipped MARGINAL to
KILLED. The rule keyed on max drawdown, so the recorded verdict stands and the CDaR number is
reported beside it.

> **In cash, the sign of the 52-week result is set by the roll calendar.** Same program, same path,
> same contracts: at one arbitrary offset it removes 7.8pp of drawdown, at another it adds 6.3pp.
> Published cell: +3.0.

**The ordering, which is the part that survives.** `separation = min_p bought(52w) - max_p
bought(4w)`: **+6.0pp** (1993-) and **+13.1pp** (2003-) in marks -- long tenor beats short at **56 of
56 alignments tested**. In cash it is **-9.0pp** and **-7.5pp**: there are alignments at which a
4-week program buys more than a 52-week one. **Combined with E0, the only claim left standing about
tenor is a marked-accounting ordering. Every magnitude, in both accountings, is gone.**

**The published number was never cherry-picked -- it was arbitrary.** On the 2003- sample `p = 0`
gives +19.9, the *second lowest of 52* alignments.

**One diagnostic that changes how the marked column should be read.** The naked book's max drawdown
is set in 2009. The hedged book's, on the full sample at 26w and 52w in marks, is set in **2003** --
in 25 of 26 and 51 of 52 phases. So `+16.8pp` never meant "the 2008 drawdown was 16.8pp shallower".
It meant the 2008 trough was pushed below the 2003 trough, after which the statistic stopped
measuring 2008 at all: **max drawdown is censored from below by the next-deepest episode.** The 2003-
subsample is the control -- it excludes the dot-com decline, its episodes match, and its marked ratio
is still 0.85. The phase sensitivity is real and is not an artifact of episode switching. The
coordinate problem itself is parked to E2, which exists to replace this coordinate.

**Predictions, scored.** `R(52w) > 1` in marks on the full sample: **REFUTED** at 0.71, and the
post-hoc reason is the censoring above -- the prediction was about the 2008 window, and the
coordinate had stopped reporting on it. `separation > 0` marked and `<= 0` cash: **CONFIRMED**, both
samples. And a claim the stub called *derivable* -- that spread grows with tenor -- is **REFUTED**:
full-sample marked spreads run 11.8 (4w), 12.6 (13w), **14.1 (26w)**, 12.7 (52w). A four-week program
has an 11.8pp spread over four alignments. Block length bounds how far an alignment can slip; it does
not determine how much the outcome moves, because that depends on whether a given window happens to
contain October 2008. Filed as an error in the stub's §2, not as a finding.

**What it does not establish.** Nothing about a second crisis: the 52 phases are 52 overlapping views
of one episode, no standard error was computed and none may be, and **effective n on the benefit side
is still 1**. Nothing about timing or signals -- the phase is swept exhaustively, never selected, and
the prediction program stays closed. And no new magnitude: E1 produces no quotable number. It removes
one.

**E1 triggered nothing automatically.** E2 and E3 stand where they were; what runs next is an open
decision, deliberately not taken inside the experiment that preceded it.


## E2 — THE ESTIMAND REPAIRED, AND THE ORDERING DOES NOT SURVIVE THE REPAIR (2026-08-18)

**Claim tuple: weekly marks · full holding period and per-episode windows within it ·
`CDaR(worst q%)` reduction as a curve, and episode-matched depth reduction · SPY 1993-2026 and
2003-2026, one path · ALWAYS-ON h=1.00, 10% OTM, no signal and no conditioning.** Preregistered in
[[closed-research/intervention/STUB-E2-DRAWDOWN-PATH]], with the identification status of each coordinate written **before**
the run. Run: `.venv\Scripts\python.exe research/path_outcomes.py SPY`.

**The gate was closed first this time.** Chekhlov, Uryasev & Zabarankin read before the run, not
after, and it found a real defect: **their `alpha` is a confidence level and ours is the fraction
averaged**, so our `CDaR_0.05` is their `0.95`-CDaR and a bare label reads as its own opposite. Also
recorded: our estimator is the *upper* CDaR with a bounded gap, and their convexity result is in the
portfolio weights and licenses nothing here. [[docs/MATH-REFERENCE]] §4.1.

**What E2 repaired.** E1 showed `max(D)` on the hedged and naked paths describing *different
episodes* — 2003 versus 2009, in 51 of 52 alignments. E2 replaced it with two coordinates that cannot
do that: `CDaR(worst q%)`, which integrates the whole path, and **episode-matched depths**, where
episodes are defined once on the **naked** book and both books are measured inside the same calendar
windows from their own peak within each. Defining the windows on the naked book is the load-bearing
choice; windows taken from the hedged path would move with the intervention.

**V1 — the ordering, phase-robust, at every `q`:**

| sample | acct | worst 1% | 5% | 10% | 25% | 50% | 100% |
|---|---|---|---|---|---|---|---|
| 1993- | marked | **+2.0** | **+0.5** | **+0.2** | **+0.2** | -0.2 | -0.1 |
| 1993- | cash | -8.0 | -7.4 | -5.6 | -3.8 | -3.4 | -2.0 |
| 2003- | marked | **+8.9** | **+4.0** | -0.2 | -3.1 | -2.7 | -1.5 |
| 2003- | cash | -9.3 | -8.7 | -7.6 | -7.2 | -5.6 | -3.1 |

**In cash the ordering survives NOWHERE, at any `q`, in either sample.** In marks it survives at
`q <= 25%` (1993-) and `q <= 5%` (2003-) — and the full-sample margins at 5%, 10% and 25% are +0.5,
+0.2 and +0.2pp, which is survival by the letter of a preregistered rule and by nothing else.

**And then the `Psi` column, which is what the whole curve was built to produce.** Distinct episodes
contributing to the worst `q%` of the process: at `q = 1%` and `5%` the marked tail rests on **one or
two episodes**; at `q >= 50%` all nine contribute.

> **The ordering survives exactly where the coordinate has collapsed onto one or two episodes, and
> fails exactly where the coordinate is well sampled.** The sample-size problem was converted into an
> output rather than argued about, which is the entire reason CDaR was specified as a curve.

**V2 / V3 — the episode-matched coordinate.** Over (episode x 52w-phase x 4w-phase) triples:

- **marked: 52w >= 4w in 90-94%** of pairs, both thresholds, both samples. **SURVIVES** — and this is
  the strongest positive result the intervention side of this repo has produced.
- **cash: 48-61%**, MARGINAL to KILLED. And **V3 is the number that stops V2 being read as good
  news**: in cash the 52-week programme reduces episode depth in only **16.5-27.9%** of pairs, so it
  **deepens** the episode three-quarters to five-sixths of the time. The cash ordering is between two
  harms.

**The episodes, phase 0, full sample, in cash.** 2008: **+3.0pp**. Everything else: -0.0, -0.0, -2.0,
-6.1, +0.0, **-0.0**, -2.6, -0.0. **The entire cash-side benefit in thirty-three years is one
episode.** The 2020 row is E0's finding in episode form: **+24.9pp of marked protection through
February-March 2020, and -0.0pp in cash** -- the option was never sold, and the market recovered past
it.

**Predictions.** "Marked survives at small `q`, at risk at large `q`" and "cash fails at every `q`":
both **CONFIRMED**, the second with no margin close to zero. "Episode sign-consistency >= 2/3 marked,
< 1/2 cash": **SPLIT** — marked confirmed, cash came in at 48-61%, below SURVIVES everywhere but only
*at* KILLED in one of four cells. Directionally right and too strong, recorded as the rule says.

**What it does not establish.** No magnitude and no population claim: one path, episodes that are not
exchangeable, phases that are not independent. The V2/V3 fractions are counts of a deterministic
sensitivity and **no standard error or test statistic may be derived from them** — that was written
into the stub before the run. Nothing about cost, outlay or monetisation, which are E6 and E7.
Nothing that promotes `q = 1%` to a preferred coordinate: the surviving points are the *least*
identified ones on the curve, which is the finding rather than a selection criterion.

**Consequence for the one claim still standing.** [[CHARTER]] §9.1's preserved structural ordering
keeps its status but gains a qualifier it cannot be quoted without: it is an **episode-level,
marked-accounting regularity about deep episodes**, and it is absent on the well-sampled part of the
drawdown path.

**E2 triggered nothing. E3 was not started.**


## E4 — M1 IS A DEDUCTIBLE-COUNT EFFECT, AND IT IS CONDITIONAL (2026-08-18)

**Claim tuple: weekly W-FRI closes · H = 52 weeks primary, 104 robustness · the SIGN of the gross
intrinsic payoff difference, no magnitude reported anywhere · ^GSPC 1927-2026, ^N225 1965-, ^FTSE
1984-, ^GDAXI 1988- (12,601 weekly observations, 29 episodes at 20%) · every week with a complete
horizon is a start, and NO start is placed at a peak.** Preregistered in
[[closed-research/intervention/STUB-E4-STRIKE-ANCHORING]], amended once — also before any run — to record that the verdict
rule is biased toward M1. Run: `.venv\Scripts\python.exe research/anchoring.py`.

**Not a rescue attempt, and it could not have been one.** Nothing in E4 is priced and no premium is
paid anywhere in it. E9, E0, E1 and E2 stand unchanged and the economic hypothesis for rolled
outright puts remains provisionally negative.

**What M1 actually is, derived before the run and confirmed by it.** With `a_i` the decline over
sub-period `i`, at `m = 0`:

```
    P_restriking = SUM max(a_i, 0)  >=  max(SUM a_i, 0) = P_anchored
```

the positive part of a sum never exceeds the sum of positive parts — so **without a deductible the
re-striking leg weakly dominates on every path, always.** M1 is therefore not "long contracts protect
better". It is **a deductible charged once versus the same deductible charged `H/s` times**, and when
every leg finishes in the money the difference is exactly `m · (SUM of re-strike levels − S_0)`. The
`m = 0` control reproduced this to the bit: `max(anchored − restriking) = 0.00e+00` in all four
markets.

**The verdict, in the order the stub requires.**

| | |
|---|---|
| preregistered rule | **M1 SURVIVES** — 4 of 29 episodes flip = 13.8%, against a 1/3 kill line |
| diagnostic declared before the run | **CONTRADICTED** — excluding starts where both legs pay zero, **15 of 28 = 54%** flip |
| therefore | *survival on a biased rule, contradicted on the diagnostic* — **not to be quoted as M1 holding** |

The whole gap is ties: starts whose horizon sits in flat or rising prices, where both legs pay zero
and the preregistered rule scores that as a vote *for* M1. **Had the amendment not been written
before the run, 13.8% would have been the headline.**

**The deductible sweep, and it is decisive.** Flip share on the diagnostic, `H = 52` — higher is
worse for M1:

| `m` | s=4 | s=13 | s=26 |
|---|---|---|---|
| **5%** | **100%** | **100%** | 83-90% |
| 10% | 54-61% | 76-77% | 76% |
| 15% | 40-45% | 59-70% | 69-74% |

> **At a 5% deductible M1 fails in every single episode, in every market.** The effect is a property
> of large deductibles, not of long tenor, exactly as the identity says.

**The shape split is the finding.** Anchoring wins persistent grinds — S&P 1973-80 (65%), S&P 2000-07
(72%), Nikkei 1989-2024 (56%), FTSE 1999-2015 (57%) — and loses V-shaped crashes: **2020 at 0/53 in
both the S&P and the DAX**, 1987 at 5/54 and 8/62, DAX 1998 at 0/69, Nikkei 1970 at 1/94. A contract
struck in February 2020 expired in February 2021 above its strike having paid nothing, while
four-week legs collected March as it happened.

**And that routes straight into the closed programme.** The condition deciding M1 is whether the
coming decline grinds or V-bottoms — **a property not observable at the moment the contract must be
bought.** Forecasting it is the problem [[docs/PROBLEM-MAP]] Part I closed. **M1 is real, conditional,
and unusable without the one capability this programme has established it does not have.** Parked as
*unavailable* rather than queued, in [[PARKED]].

**Predictions.** "Failures concentrated in V-shapes, 2020 and 1987 against": **CONFIRMED sharply.**
"More favourable at larger `m`": **CONFIRMED**, monotonically. "More favourable at `H = 104`":
**REFUTED** — the diagnostic flip share rises to 89-98%, because the §3 reasoning counted the extra
deductibles and forgot that a two-year contract has two years in which to expire out of the money.
Half a mechanism asserted as the whole one.

**`Psi`.** 29 episodes is not 29 observations: 2000-07, 2008, 2020 and 2022 appear in three or four
markets each and are one event reported several times. Only five episodes have no cross-market
calendar overlap, and **the genuinely independent content is US 1929-1954 and Japan 1990-2003** —
perhaps 12-15 distinct events, not 29. Two mega-episodes (S&P 1929-54, Nikkei 1989-2024) carry 42% of
all starts, a known limitation of the inherited peak-to-recovery definition that was **not** re-tuned
after seeing the result. Starts overlap almost completely, so `n_starts` is not a sample size and no
standard error, test statistic or population magnitude appears anywhere in E4.

**E4 stopped where its stub said it would.** No pricing, no monetisation, no additional structures,
no progression to E5/E6/E7. The outcome is neither the clean failure that closes the rolled-put/tenor
branch nor the clean survival that triggers a reassessment, so **the branch decision is recorded as
open and was not taken inside the experiment.**


## Next

**There is no queue in this file.** [[CHARTER]] §9 is the single experiment queue, and two documents
proposing next steps is how a second research program starts.

**PROGRAM TRANSITION 2026-08-18 — the second one.** Both the prediction/regime program (closed
2026-08-17) and the rolled-put/tenor intervention program (closed 2026-08-18) are preserved,
reproducible, in `closed-research/`. The active program is **return states**: [[CHARTER]]. What is
queued is **S0 only** — the identification problem, worked before anything is measured.

**Nothing from the intervention queue carries forward.** E3, E5, E6 and E7 are closed with the
programme, not parked as future work; they were downstream of a claim that no longer stands. See
[[PARKED]] §1.

Everything above this line is the chronological record and stands as written, with one standing
caveat that attaches to the structure-map entry and to every number derived from it:

> **The benefit side has effective n = 1.** `summarize` returns `max_drawdown` as a single `.min()`,
> and on both reported samples that statistic is set by the same episode (Oct 2007 - Mar 2009). The
> **orderings** are probably robust; the **magnitudes** are one draw at one unswept roll phase and are
> not identified. [[CHARTER]] E1 and E2 test exactly this. **E0 has now run (2026-08-18) and the
> answer is that the reduction is mostly a mark** — 82% of it at 52w on the full sample — which makes
> the caveat above stronger, not weaker: the magnitudes are one draw at one phase *and* they are
> quoted in an accounting the investor cannot bank.

The four "actual next actions" previously listed here — fit the real skew surface, extend the
clairvoyant grid, decide the objective, specify recycling — were written on 2026-08-15 under the
framing this transition replaces. They are not deleted from the project: the clairvoyant extension is
[[CHARTER]] E3, the surface is E5 (reclassified as procurement, never prediction), and recycling is
E6. The objective question is answered by [[CHARTER]] §1.

## Registration

Not in [[INDEX]] nor the repo table in [[CLAUDE]] — worth adding when convenient, not a blocker.

**`regime-detection` is not this repo's problem and is not to be raised here.** It was a learning
ground — jump models, k-means, lag experiments — it lives on `AdamMooo/regime-detection`, and it will
be revisited on its own terms. This repo is an extension, not a successor, and owes it no
reconciliation. Raised three times on 2026-08-15 as a "migration risk"; that was wrong each time and
is exactly the reflex [[docs/PROBLEM-MAP]] standing rule 5 now forbids.

## Related

- [[README]] · [[docs/RESEARCH-PROTOCOL]] · [[docs/MATH-REFERENCE]] · [[docs/POINT-IN-TIME-DISCIPLINE]]
- [[look-ahead-bias-is-self-concealing]] — vault lesson from this work
- [[INDEX|Home]]
