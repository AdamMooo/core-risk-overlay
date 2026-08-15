---
type: project
---

# Core-Risk-Overlay

Last updated: 2026-08-14

Tail-risk hedge overlay for a permanently long global equity book. **Problem statement, and the gate
on what is worth building: [[docs/PROBLEM-MAP]] — read it first.** Mandate in [[README]]. Protocol in
[[docs/RESEARCH-PROTOCOL]]. Mathematics in [[docs/MATH-REFERENCE]]. Time-basis rules in
[[docs/POINT-IN-TIME-DISCIPLINE]]. **Width/direction separation, binding, in
[[docs/TRANSLATION-LAYER]].**

## Status — 2026-08-15

> **SCOPE RESET 2026-08-15. This repo is no longer a signal-discovery engine.** Its job is to state
> the hedging problem — what is established, what is falsified, what is unknown and *why*, what the
> decision actually is, and what research would change it. **No signal, measure or estimator is added
> unless the decision it improves is named first, with a size.** The standing answer lives in
> **[[docs/PROBLEM-MAP]]** — read that before anything below. This file remains the chronological log.
>
> **The objective above all of it is unchanged: build an economically valuable tool.** The problem map
> is the route and the four-step board is the current best-supported path — **evidence, not
> commitment.** If a better path to economic value appears, the board changes ([[docs/PROBLEM-MAP]]
> §0.0). "Follow the four steps" is not the goal.

**The structure map ran (2026-08-15) and it reordered the project.** Tenor is the dominant variable:
extending 10% OTM outrights from 4w to 52w buys **3-4x the drawdown protection at equal or lower
cost**. Always-on 52w 5% OTM buys **+24.3pp** of drawdown (2003+) against a *clairvoyant* 4w bound of
+24.7pp — so the protection axis is close to saturated by structure alone, with no signal. Perfect
foresight at matched structure adds **+1.4pp of drawdown and +8.5pp/yr of premium**: a signal is a
**cost-reduction device, not a protection device**. Full decomposition and its limits in
[[docs/PROBLEM-MAP]] §5.

**Both axes of the model question are closed. The model adds nothing to VIX on levels (D3) or on
dynamics, for SPY.**
Two directions were held open on structural grounds — **multi-asset** (a different *information set*)
and the **GARCH specification question** (a different *estimator* on the same set, so containment
does not apply). Both remain structurally valid and **both are now off the decision path**: the
structure map bounded what any signal can be worth, and neither is scored against that bound.
Retained as research items if the paper is written — [[docs/PROBLEM-MAP]] §6.

**What the model IS, now measured rather than assumed** (`state_character.py`, below): a **width
meter** that separates volatility by ~2.4x out of sample, carries **no direction content**, and
reads "wide" when the book is already ~13% below its peak. That description is the honest product
of this repo to date. It is not a forecast and it is not incremental to VIX.

Prior session (2026-08-13): the encompassing regression against VIX, the hedge-economics bracket,
the trigger bracket, and the memory diagnostic — the last of which **refuted a confident claim made
earlier the same day** and is recorded as such.

## Governing frame — read this before proposing any experiment

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
status of every "beyond simpler measures" comparison: [[docs/TRANSLATION-LAYER]].

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

## Next

**Read [[docs/PROBLEM-MAP]] first.** It is the standing statement of the problem and §6 is the gate
that decides whether anything below is worth running. Then [[README]] §§1-5 and the **Governing
frame** above.

**The gate, in one line: no signal, measure or estimator is built unless it is scored as *premium
avoided per unit of protection retained*, at 26-52 week tenor, against the §5.1 decomposition.**

### Superseded by the scope reset — retained as record, not as plan

Everything from here to the end of this section was the plan as of 2026-08-14, when the signal
program was still believed to be where the value was. The design work is sound and the reasoning is
worth keeping — particularly the horizon argument and the asymmetry amendment, which are the two
best pieces of experimental design in the repo. **None of it is on the decision path**
([[docs/PROBLEM-MAP]] §6). Do not treat the items below as next actions.

**The stated next research question (2026-08-14), and the constraint that makes it answerable:**

> **Does this representation of width contain information beyond simpler volatility measurements?**

Status of every rung, so none is re-run by accident: **constant — run**, model wins tick loss, DM
significant at 10% and 5%. **EWMA — run at h=1 and VOID at h=1.** **VIX levels — run, null (D3).**
**VIX dynamics — run, null.** **GARCH(1,1) — never built, not implemented anywhere in this repo.**
**ATR / Parkinson / Garman-Klass / Rogers-Satchell / Yang-Zhang — never built**, needs daily OHLC.

**The horizon is the whole design and §0 rule 4 will void the run without it.** EWMA is IGARCH: its
multi-step variance forecast is a martingale and never reverts. MS reverts toward the stationary
regime mix at a rate set by the second eigenvalue of `P`. That is the entire structural difference
and it is **exactly zero at h=1** — so an h=1 rerun measures nothing, whatever it returns. Any
"beyond simpler measures" test runs at **h > 1** and states the reverting-vs-martingale mechanism in
its stub. **GARCH(1,1) is the sharper opponent than EWMA**, because GARCH also reverts (toward
unconditional variance, at rate `alpha + beta`), which isolates the real question: do **discrete
regimes** add anything over **smooth mean reversion**? Full table in [[docs/TRANSLATION-LAYER]] §5.

**The §0 stub is written and the experiment is BLOCKED, deliberately:
[[docs/STUB-GARCH-ENCOMPASSING]].** Two findings from writing it, both of which would have wasted
the run:

- **h > 1 is necessary and not sufficient.** `E_t[sigma2(t+h)]` is *the same functional form* in
  both models — `long-run level + (geometric rate)^h × current deviation`, with a single
  state-independent rate in each (`alpha+beta` vs `lam`). A point-forecast variance comparison at
  any horizon compares two parameterisations of one two-parameter curve: **structurally the h=1
  EWMA mistake, one level deeper.** The discriminating functional is the **h-step density**, whose
  shape under MS is a mixture over `2^h` regime paths that no single-regime GARCH can reproduce.
- **The horizon follows from mixing time, not from taste.** Mixture non-Gaussianity vanishes for
  h ≪ mixing time (chain barely moves) *and* for h ≫ it (CLT reabsorbs it). Mixing time is
  `1/(1-lam)` ≈ **11.4 weeks** at the already-published median `lam` = 0.9126 — hence **h=13
  primary**, with h=4 and h=26 as brackets and a preregistered prediction that any effect is
  *largest at 13*, which is itself a test of the stated mechanism.

**A third finding, raised against my own stub (§11.1): a null would be CONFOUNDED.** ARCH-LM
rejects at 55.6 *after* regime switching, so the base specification is known-misspecified in the
exact dimension under test. A positive result is therefore clean and strong; a null is equally
consistent with *"the within-regime defect masks what the regimes contribute"* and **no sample size
separates those.** The literature sharpens this rather than softening it — SWARCH and MS-GARCH both
put ARCH inside the regimes, so the field largely **skipped this rung because plain MS was already
understood to be inadequate.** That is simultaneously why the run is not redundant and why its null
is uninformative. The run is still worth having, as an **asymmetric** test, and a null is reportable
only as a claim about *this specification*, never about regime structure as such.

**The experiment is now formally ASYMMETRIC** ([[docs/RESEARCH-PROTOCOL]] amendment 2026-08-14,
stub §11.1-§11.5). `H0_spec` (plain MS adds nothing over GARCH) is testable; `H0_struct` (regime
structure adds nothing) **is not, at any sample size**. Verdicts are POSITIVE / NULL /
**INCONCLUSIVE**, assigned before any conclusion is written, and a result failing the power
requirement is INCONCLUSIVE rather than NULL. **No retroactive repair:** a null does not license
swapping in SWARCH and rerunning — S3 is a separate stub. And the **positive** branch is confounded
too: the model switches its **mean** as well as its variance while GARCH's mean is constant, so a
**common-mean MS variant is required** or a positive is uninterpretable.

**Literature gate — 2026-08-14. Timmermann (2000) READ IN FULL; verdict INFORMS; the run is not
killed.** The blocker moved from Hamilton & Susmel because a *fact* changed: SWARCH is MS-**ARCH**
(rung 4), while Timmermann's model (1) is **exactly this repo's specification** (rung 3). Obtained
free as LSE FMG DP 323. Three consequences, in [[docs/STUB-GARCH-ENCOMPASSING]] §14.3:

- **Skewness requires switching MEANS** — variance switching alone cannot produce it, at any `P`.
  And standard GARCH without leverage has **zero** skewness (Bollerslev 1986). So plain MS can do
  something GARCH(1,1) structurally cannot, which is the sharpest mechanism found so far — and it
  explains the asymmetric PIT QQ panel the repo already had and could not account for.
- **The §11.3 common-mean control is heavier than it looked:** it forces skewness to exactly zero,
  removing that entire axis and making a positive result *hardest* on that variant. GJR-GARCH,
  added earlier for an unrelated reason, is the right opponent for the skewness axis.
- **Timmermann's own warning lands on our parameters** — MS with small means in all states "may have
  trouble replicating the skewness found in these data." Ours are +0.36% / −0.26%. **Corollary 1
  makes this computable in closed form from parameters already fitted at 95 vintages**, which would
  discharge §9's blocking power requirement before any code exists. Recommended, not done.

**A §0 rule 3 PROCESS FAILURE came out of it, logged in [[docs/RESEARCH-PROTOCOL]] §Amendments.**
`memory_diagnostic.py`'s 2026-08-13 "deductive result" is Timmermann's Proposition 5 — published
1999, sitting `[UNREAD]` as row 2 of the reading list, whose own reading-order note already said
what it contained. The repo's version omits the mean terms and overstates the autocovariance by
**1.00%** at fitted parameters: negligible numerically, wrong formally, now corrected.

**Still open:** Hamilton & Susmel (1994), lower priority, and Marcucci (2005) full text. §0 rule 3 requires naming the paper that settles it; if one does, rule 2 says
the run carries no information and must not happen. Containment does **not** apply here — GARCH sees
exactly the same information set as the MS model — which is why this is a real experiment and not
D3 again.

**The direction that was open on 2026-08-14 — structurally valid, and now off the decision path.**
The containment argument against everything else still stands, and multi-asset still escapes it. What
changed is the *denominator*: the structure map bounded what any signal can be worth, and a
cross-asset width measure is not scored against that bound. It returns only under the §6 gate.

3. **Multi-asset.** [[README]] §1 says *systemic* is the operative word and the model has only ever
   seen SPY. VIX is SPY-only implied volatility, so a cross-asset measure is a genuinely different
   **information set** rather than a better estimator on the same one — the single argument that
   survives D3 and the dynamics test. Cheapest first probe is not a multivariate Markov model but the
   **absorption ratio** (Kritzman, Li, Page & Rigobon 2010): rolling PCA over a small asset panel,
   fraction of variance in the top eigenvectors, point-in-time. One new column through
   `encompassing.py`, which already exists and is already validated. If a cheap joint measure adds
   nothing to VIX, an expensive one almost certainly will not either.

   **`state_character.py` now gives this probe a bar to clear that is not a regression.** The
   single-asset state reads "wide" when the book is already ~13% below its peak at the median, on
   both SPY and QQQ. A cross-asset measure that fires at the same depth is not worth building
   whatever its encompassing coefficient does, and that comparison is descriptive, cheap, and
   available before any regression is run. Note `systemic_state.py` currently threatens this route
   independently: the expanding-percentile trigger it used is refuted, and the fix (Kritzman's own
   standardised shift) is unbuilt.

4. **Fit the model on daily** and re-measure `RELIABLE_MIN_OBSERVATIONS` (§1.3) — the 520-week figure
   is weekly and does not transfer. Worth doing for the **memory** question only. It cannot reopen
   the encompassing question: containment is frequency-invariant, and treating it as a route back in
   would be exactly the goalpost-moving this repo keeps catching.

**Deprioritized, not deleted.** S3 (within-regime ARCH), S4 (Student-t regime densities), DQ, the ES
breach bootstrap and R1-R10 all address **marginal / level** properties. D3 closed the level-based
case, so none of them speaks to the untested question. They remain valid research items if the paper
is written; they are not the path.

**MSM and HAR are parked, not adopted.** They were proposed on a long-memory argument the daily run
did not support. They come back only if step 1 or 2 shows a power law.

Not planned: statistical jump models, intraday data, Hawkes processes, K-means, binary classifiers.
*"Economic backtesting" was on this list until 2026-08-15; the structure map is exactly that, and it
produced the largest effect size in the repo. Removed.*

### The actual next actions (2026-08-15)

In order, and each qualifies under [[docs/PROBLEM-MAP]] §6 because a plausible outcome changes an
action:

1. **Fit the real skew surface from `options-quant`'s archived SPY chains** and replace
   `skewed_vol`'s swept slope. The `sqrt(4/tenor)` term is load-bearing *in the direction of the
   conclusion*; if real 52-week skew is steeper than assumed, the tenor result shrinks or inverts.
   **This can overturn the largest finding in the repo, which is why it goes first.** Data only —
   no import, no code dependency, and `options-quant` is not governed by the charter either.
2. **Extend the clairvoyant grid to 26w and 52w** in `hedge_economics.py`. One line. Until it exists,
   "timing is worth ~3pp/yr" is a claim about 4w and 13w only, and §5.2 of the problem map stays
   suggestive rather than settled.
3. **Decide the objective: options, or drawdown reduction?** If the second, a trend sleeve is the
   honest competitor and the whole options program is one branch of a comparison never run. A
   decision for Adam, not a measurement — and it gates how much of the rest is worth doing.
4. **Specify the recycling rule, then measure it.** README §1 claims monetize-and-rebuy as a source of
   value; it has never been written as a rule, so it has never been measured.

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
