# §0 Stub — does discrete regime structure add anything to smooth mean reversion?

Last updated: 2026-08-14 · **Status: PREREGISTERED, NOT IMPLEMENTED. Still blocked — see §14.2.**

**Gate status after the 2026-08-14 search:** Marcucci (2005) **INFORMS** (four axis mismatches;
three design changes taken, §14.2). Hamilton & Susmel (1994) **UNRESOLVED and blocking** — weekly
US stock returns, exact frequency match, forecast comparison not obtainable without institutional
access.

Written under `RESEARCH-PROTOCOL.md` §0: no experiment runs until its stub is committed, and the
stub is committed before the commit carrying its results. This document moves into the module
docstring of the implementing file when implementation starts, exactly as
`dynamics_test.py`, `systemic_state.py` and `state_character.py` carry theirs.

---

## 1. The research question

> **Does the discrete regime structure provide information about future conditional variance that
> is not already captured by a smooth mean-reverting variance model?**

Not "is the Markov-switching model better than GARCH." That is a horse race and
`RESEARCH-PROTOCOL.md` forbids it in its header. **This is an encompassing question** — does one
forecast carry information the other lacks — and the repo already owns the validated apparatus for
it (`encompassing.py`, with adversarial alignment verification).

## 2. Claim tuple

**The objective, narrowly, and nothing may be concluded outside this sentence:**

> **Does the plain MS model contain incremental information about the multi-step predictive return
> density relative to smooth GARCH dynamics, under the pre-specified horizons, functional and
> evaluation protocol?**

Anything beyond that requires a separate experiment with its own stub.

```
frequency   weekly
horizon     h = 13 primary; h = 4 and h = 26 as declared brackets (see 5)
functional  h-step predictive DENSITY of the aggregate return (primary)
            h-period integrated variance (secondary, see 3 for why it is secondary)
sample      SPY, walk-forward OOS 2003-2026; QQQ 2009-2026 as weak replication
```

## 3. The structural distinction — and the trap inside it

### 3.1 Both models are "long-run level plus geometric decay". This is the finding that shapes the design.

**GARCH(1,1)**, with `sigma_bar^2 = omega / (1 - alpha - beta)` and `alpha + beta < 1`:

```
sigma2[t+1]        = omega + alpha*eps[t]^2 + beta*sigma2[t]
E_t[ sigma2[t+h] ] = sigma_bar^2 + (alpha+beta)^(h-1) * ( sigma2[t+1] - sigma_bar^2 )
```

**Markov-switching**, with regime variances `v`, stationary weights `pi`, filtered state `xi[t]`,
and `lam = p00 + p11 - 1` the non-unit eigenvalue of `P`:

```
w[t+h|t]           = xi[t]' P^h
w[t+h|t] - pi      = lam^h * ( xi[t] - pi )
E_t[ sigma2[t+h] ] = pi.v + lam^h * ( xi[t] - pi ).v
```

**Read these two side by side.** Both are:

```
E_t[ variance at t+h ] = (long-run level) + (geometric rate)^h * (current deviation)
```

**identical functional form, with a single state-independent decay rate in each.** They differ only
in (a) the rate — `alpha+beta` versus `lam` — and (b) how the current deviation is inferred from
the return history.

**The consequence, and it is the whole reason this stub exists.** A comparison of **h-step point
forecasts of conditional variance** is a comparison of two parameterisations of the *same*
two-parameter curve. Under §0 rule 2, that outcome is largely derivable in advance and the run
would carry little information — **structurally the same mistake as the h=1 EWMA comparison, one
level deeper.** Moving from h=1 to h>1 is necessary and **not sufficient**. Point-forecast
variance comparison is therefore **secondary and reported as a descriptive rung, never as the
answer.**

### 3.2 What genuinely differs: the shape of the h-step density

Let `R[t,t+h] = sum_{i=1..h} r[t+i]`.

- **Under GARCH(1,1)**, `R` is a sum of scaled innovations with a smoothly evolving scale. It is
  unimodal and, aggregated over `h` periods, approaches Gaussian; its excess kurtosis comes only
  from vol-of-vol and is modest.
- **Under Markov switching**, `R` is a genuine finite mixture over the `2^h` regime *paths*.
  Conditional on the path, `R` is Gaussian with mean `sum mu[s_i]` and variance `sum v[s_i]`, so
  the density of `R` is a mixture indexed by **`N_h` = the number of wide weeks in the window**,
  with weights given by the distribution of `N_h` under the chain started at `xi[t]`.

**This is a difference in shape that no single-regime GARCH can reproduce**, and it is the
model class's actual claim. It is also why the density and not the variance is the primary
functional — the same argument `RESEARCH-PROTOCOL.md` §1 already makes about scoring on every
observation rather than on breaches.

### 3.3 A second, sharper difference: boundedness

```
MS     E_t[sigma2[t+h]] lies in the convex hull of v  ->  CANNOT exceed max_j v[j]
GARCH  sigma2[t+1] is LINEAR in eps[t]^2             ->  unbounded above
```

The MS state update is a Bayesian likelihood-ratio update on a probability vector and therefore
**saturates**; GARCH's is linear in the squared innovation and does not. This is the documented
source of the blocky VaR path and of EWMA reaching −16% in 2008 where the model stopped at −10%.
It yields a directional, falsifiable prediction (§13) rather than a hope.

## 4. The exact quantity being forecast

| | definition |
|---|---|
| **primary** | `f(R[t,t+h] \| F_t)` — the h-step predictive density of the aggregate log return, formed strictly before `r[t+1]` exists |
| **secondary** | `IV[t,t+h] = sum_{i=1..h} r[t+i]^2` — realized h-period integrated variance, forecast by `E_t[IV]` |

Both models emit both objects in closed or near-closed form. **No simulation is used for the MS
density if the mixture over `N_h` is computed exactly** — the distribution of the number of wide
weeks is a linear recursion on the chain, so the exact mixture is available in `O(h^2)` and Monte
Carlo would introduce avoidable noise into a comparison this close.

## 5. The horizon, justified from the mechanism and fixed before implementation

**The argument is about mixing time, not about fitted convenience.**

The mixture non-Gaussianity in §3.2 is governed by the dispersion of `N_h`:

- **h ≪ mixing time** — the chain barely moves, `N_h` is nearly degenerate, the mixture collapses
  toward a single component. The models converge. *This is the h=1 failure, generalised.*
- **h ≫ mixing time** — `N_h / h` concentrates on `pi[wide]` by the ergodic theorem, the mixture
  is smoothed by the CLT and returns to approximate Gaussianity. The models converge again.
- **h ≈ mixing time** — path uncertainty is maximal and the mixture is furthest from Gaussian.
  **This is the only region where the mechanisms are distinguishable.**

The chain's mixing time is `1 / (1 - lam)`. The repo has already measured `lam` across 95
walk-forward vintages: **median 0.9126, range [0.8921, 0.9929]** (`memory_diagnostic.py`), giving a
mixing time of **≈ 11.4 weeks** at the median.

```
h = 13   PRIMARY    ~ mixing time; also the existing refit cadence
h =  4              lower bracket; the horizon encompassing.py and dynamics_test.py already use
h = 26              upper bracket; where the CLT should be visibly reabsorbing the difference
```

**Two disciplines on this choice.** (a) `lam` is a *previously published* repo measurement, not a
quantity estimated inside this experiment, so using it does not select the horizon on this
experiment's outcome. (b) h=4 and h=26 are the repo's existing horizons, so no new degree of
freedom is introduced. **The three horizons are fixed here and are reported together, always. A
result at one horizon only is not reportable.**

**Preregistered shape prediction, which is itself a test:** any incremental information should be
**largest at h=13 and smaller at both h=4 and h=26**. A monotone-in-h result, or one that appears
only at h=26, contradicts the stated mechanism and must be reported as such rather than accepted
as a win.

## 6. Loss functions

**For the density (primary):** the **logarithmic score** and **CRPS**. Both are strictly proper, so
neither can be gamed by a mis-stated forecast. Log score is sensitive to the tail; CRPS is more
robust to it. Reporting both separates "the density is better everywhere" from "the density is
better in the tail", and those are different claims.

**For the variance (secondary):** **QLIKE** as headline, MSE alongside.

```
QLIKE:  L = IV/F - log(IV/F) - 1
MSE:    L = (IV - F)^2
```

Patton (2011) proves MSE and QLIKE are the **only** losses in the relevant class that are robust to
noise in the volatility proxy — that is, that rank forecasts consistently even though `IV` is a
noisy estimate of true integrated variance. Using anything else here would let proxy noise pick the
winner. **QLIKE is headline because it is far less dominated by a handful of crisis observations
than MSE**, and with ~10-15 systemic episodes in the whole sample, an MSE ranking is effectively an
opinion about 2008.

## 7. Out-of-sample protocol

Identical to the existing walk-forward path, because reusing it is what makes the result comparable
to everything already in the repo:

```
parameters   both models refit every 13 weeks on data through the refit point only
state        MS from filtered[t]; GARCH from sigma2[t] recursion through t
density       formed before r[t+1] exists
scored on    the realized window r[t+1 .. t+h]
alignment    verified adversarially -- a leaky variant (window starts at t) must
             score BETTER and a stale variant (starts at t+2) WORSE, monotonically
```

The adversarial alignment check is **mandatory and blocking**. Both prior encompassing runs used it
and it is the only reason an off-by-one would not have invalidated them silently.

**Innovation distribution is held FIXED AND IDENTICAL across both models** — Gaussian in the
primary, Student-*t* for both as a declared sensitivity. This is what makes any observed difference
attributable to the **variance dynamics** rather than to the tail assumption, and it is the direct
implementation of the tail requirement in §11.

## 8. The comparison metric and the null

**Primary — encompassing regression**, which asks the §1 question directly rather than asking which
model wins:

```
L[t](GARCH) - L[t](MS)  regressed on a constant, HAC standard errors
```

and, in the repo's established form on the variance side:

```
IV[t,t+h] = a + b * F_GARCH[t] + c * F_MS[t]
```

```
H0 (the null):     c = 0   -- the MS forecast is nested inside GARCH's
                              information, as it was inside VIX's
H1:                c != 0  -- discrete regime structure carries incremental
                              information about forward variance
```

**Secondary — Giacomini-White (2006) conditional predictive ability**, not plain Diebold-Mariano.
GW is the correct test when parameters are re-estimated in a rolling scheme, which is exactly this
design; DM's null concerns population-optimal forecasts and is not what a walk-forward comparison
delivers. DM with the Harvey-Leybourne-Newbold small-sample correction is reported alongside for
continuity with `baselines.py`.

**Overlapping windows are used, with HAC (Newey-West) covariance at lag ≥ h−1.** See §9.

## 9. Effective sample size, stated before the run because it may kill the experiment

This is the constraint that has stopped three previous strands in this repo and it is checked
here in advance rather than discovered afterwards.

```
non-overlapping blocks   h=4  -> n ~ 307     h=13 -> n ~ 94     h=26 -> n ~ 47
overlapping + HAC        h=4  -> n ~ 1226    h=13 -> n ~ 1217   h=26 -> n ~ 1204
```

**At h=13 non-overlapping, n ≈ 94 has almost no power against a small effect.** Overlapping windows
with HAC recover nominal observations but not independent information; the honest count is closer
to the non-overlapping figure, and HAC only fixes the standard error, not the information content.

**Therefore the density score is the primary functional for a power reason as well as a structural
one:** a proper scoring rule evaluates the whole distribution at every `t`, which is the largest
source of power available here — the same argument `RESEARCH-PROTOCOL.md` §1 makes for scoring
densities over breaches.

**Blocking requirement:** the implementing run reports a **power statement** — the effect size
detectable at 80% with the realised HAC standard error — *before* interpreting any p-value. A null
without a power statement is not reportable as a null. `dynamics_test.py` set this precedent by
demonstrating power rather than assuming it, and that is why its negative was strong.

## 10. What would constitute evidence FOR incremental regime information

All four required together:

1. `c != 0` in the encompassing regression at **h=13**, with joint R² materially above
   GARCH-alone — not matching to four decimals as VIX-alone did in D3.
2. The density log score and CRPS both favour MS at h=13, i.e. the gain is not a
   tail-only artifact of one scoring rule.
3. The effect is **largest at h=13** and smaller at h=4 and h=26, matching the §5 mechanism.
4. It survives on QQQ, with QQQ's weakness (§12) stated.
5. **It survives the common-mean MS variant of §11.3.** Without this the result is not
   interpretable as a statement about regime *variance* structure, because the switching mean is an
   alternative explanation the GARCH benchmark also cannot reproduce.

## 11. What would constitute a null

`c ≈ 0` with a **demonstrated** power to detect a meaningful effect, at all three horizons.

### 11.1 A null here is CONFOUNDED, and this is the weakest point in the design

Raised 2026-08-14 under §0.2 P9, against my own stub. The sentence originally here — *"a null closes
the specification question"* — **overstated what a null could carry, and is retracted.**

**The base specification is already known to be misspecified in the exact dimension being tested.**
ARCH-LM on standardized residuals rejects at **55.6 (p = 2.4e-11) *after* regime switching**:
volatility keeps moving *within* regimes. So this experiment compares a **known-misspecified**
regime model against a smooth model that handles the very dynamics the regime model is known to
miss. Interpretation is therefore **asymmetric**:

- **A positive result is clean and strong.** A model with a documented within-regime defect that
  *still* carries incremental density information is good evidence that discrete regime structure
  contributes something real — it cleared the bar carrying a known handicap.
- **A null is confounded and cannot be read as "discrete regimes add nothing".** It is equally
  consistent with *"the base spec's within-regime defect masks whatever the regimes contribute"*.
  These two explanations are not separated by this design and **no sample size separates them.**

**The literature makes this sharper, not softer.** Under §0.2 P6, both blocking papers fit the
**S3 rung** — SWARCH and MS-GARCH both put ARCH inside the regimes. The literature largely *skipped*
the rung this repo actually occupies, and skipped it **because plain MS was already understood to be
inadequate.** That cuts both ways and both must be recorded: it is why this experiment is **not
redundant**, and it is why its **null would be uninformative**.

**Consequence, binding on the write-up.** A null is reported as *"the base specification adds no
incremental density information beyond GARCH(1,1) at these horizons"* — a claim about **this
specification**, never about **regime structure as such**. Extending it to the model class would
require S3, which is the separating experiment and is not this one.

**This does not cancel the run.** A confounded null is still worth having: it is the honest terminal
result for the specification this repo has actually built and validated, and P4 says a null is a
successful outcome. It does mean the §10 evidence-for criteria carry far more weight than the §11
evidence-against ones, and the run should be understood as **asymmetric by construction** rather
than as a two-sided test.

### 11.2 The two hypotheses, which are not the same hypothesis

```
H0_spec    plain MS provides no incremental density information relative to GARCH
           -> THIS experiment tests this

H0_struct  discrete regime structure provides no useful information beyond smooth
           volatility models
           -> THIS experiment CANNOT establish this. Ever. At any sample size.
```

```
plain MS beats GARCH      =>  evidence that discrete regime structure carries
                              incremental density information  (strong: it cleared
                              the bar carrying a documented handicap)

plain MS does NOT beat    =/=> regime structure is useless
GARCH                          -- compatible with (1) no incremental regime
                                  information, OR (2) real regime information
                                  masked by the known within-regime defect
```

**Permitted wording for a null, verbatim:** *"No incremental information was detected from this
particular plain-MS specification relative to the tested GARCH benchmark."* **Forbidden:** *"regime
switching provides no useful information"* — or any sentence of that shape.

### 11.3 A confound on the POSITIVE branch too, which §11.2 does not cover

Raised 2026-08-14 against the amendment itself. `src/markov_switching.py:168-170` fits
`trend="c", switching_trend=True, switching_variance=True` — the mean switches **as well as** the
variance. The GARCH(1,1) benchmark carries a **constant** mean.

So a positive result is confounded between:

1. **discrete regime structure in the variance** — the intended finding; and
2. **a two-component mixture in the mean**, which GARCH(1,1) also cannot reproduce, and which is a
   different claim.

Not hypothetical: the fitted regime means are **+0.36%/wk (calm) and −0.26%/wk (wide)**, and the
repo has already measured the switching mean moving the up/down probability ratio from 1.0000 to
0.9279.

**Declared sensitivity, fixed here before the run: refit MS with a COMMON mean
(`switching_trend=False`) and score it identically.** If the positive survives, it is attributable
to the regime *variance* structure. If it vanishes, the finding was the mixture mean and must be
reported as such. **Without this variant a positive result is not interpretable**, and §10's
criteria are amended to require it.

### 11.4 No retroactive repair

**Do not replace the base MS model with SWARCH or MS-GARCH in response to a null.** That is a
different experiment, and running it *because* the first one failed converts a specification ladder
into a search for a version that passes.

```
FORBIDDEN  experiment -> null -> richer model -> rerun -> report the rerun
REQUIRED   experiment -> result -> diagnosis -> NEW STUB -> next specification
```

If this experiment returns a null, the **next** research question — a separate stub, separately
preregistered — is:

> **Does within-regime ARCH recover information that plain MS fails to express?**

That is S3, it is the experiment that separates the two explanations in §11.1, and it does not
retroactively rescue this one.

**Note on GJR-GARCH (§14.2), so it is not later mistaken for a violation of this rule.** GJR was
added on the **opponent** side, before any run, from the literature. It makes a positive result
*harder* to obtain. Strengthening the benchmark against yourself is the opposite of a retroactive
rescue; the rule bars strengthening the *model* after seeing it lose.

### 11.5 Verdict classification — assigned BEFORE any conclusion is written

Every result is classified as exactly one of three. **Inconclusive is a first-class outcome, not a
soft null:**

| verdict | meaning |
|---|---|
| **POSITIVE** | Evidence that the tested discrete-state specification carries incremental density information. Requires all §10 criteria **including the common-mean variant of §11.3**. |
| **NULL** | No detectable incremental information *from this plain-MS specification against this benchmark*. Requires the §9 power statement. |
| **INCONCLUSIVE** | Insufficient power, a failed protocol condition (alignment check, convergence, clip counter), or another identified limitation. |

**Binding:** a result failing the §9 power requirement is **INCONCLUSIVE, never NULL.** The
distinction is the whole reason §9 is blocking — at h=13 non-overlapping, n ≈ 94, and an
underpowered test that finds nothing has found nothing about the world.

**Never upgrade a NULL into a structural conclusion about regime switching. Never upgrade a
POSITIVE into a trading rule.**

## 12. Tail caveat, preregistered

**Every candidate model shares the Gaussian conditional assumption, and at α=0.01 they already
breach ~2x uniformly** — MS 1.79%, constant 1.87%, EWMA 0.97 2.03%, EWMA 0.94 2.36%. That is a
property of the **data**, not of any model's variance dynamics.

**Consequence, binding:** no tail result from this experiment may be read as evidence about regime
structure while the innovation distribution is shared. The separation of *model-specific
information* from *shared distributional assumption* is achieved by §7's fixed-and-identical
innovation distribution plus the Student-*t* sensitivity: if the MS-vs-GARCH gap is stable across
Gaussian and Student-*t* innovations, it is attributable to the variance dynamics; if it moves, it
was the tail assumption.

**QQQ is a weak replication** — its 520-week burn-in pushes the OOS window to 2009, excluding the
GFC entirely, and it correlates 0.87 with SPY weekly.

## 13. Predicted outcome, recorded before any code (§0 rule 2)

- **Point-forecast variance, all horizons: NULL, and largely derivable** from §3.1. Recorded rather
  than discovered. This is why it is secondary.
- **Density at h=13: the only place a difference is plausible.** Genuinely uncertain — I do not know
  whether the mixture shape survives parameter estimation error at n≈94 independent windows.
- **Extreme episodes: MS loses to GARCH**, from the boundedness argument in §3.3. MS's forecast
  cannot exceed `max_j v[j]`; GARCH's can. 2008 should show this plainly.
- **Overall: I expect a null**, for the containment reason that killed D3 and the dynamics test —
  though note containment applied to *VIX*, which observes more than returns. GARCH sees **exactly
  the same information set** as the MS model, so containment does **not** apply here. This is a
  genuine estimator comparison on a fixed information set, which is why it is worth running at all
  and why it is not simply D3 again.

## 14. Literature gate — THIS BLOCKS IMPLEMENTATION

`RESEARCH-PROTOCOL.md` §0 rule 3: name the paper that already settles this, or state in writing
that none does. **I cannot honestly state that none does.**

| paper | why it may already settle this | status |
|---|---|---|
| **Marcucci (2005)**, *Forecasting stock market volatility with regime-switching GARCH models* | Compares Markov-switching against GARCH for volatility and VaR at multiple horizons. This is close to the present design. | **[UNREAD] — BLOCKING** |
| **Hamilton & Susmel (1994)**, *Autoregressive conditional heteroskedasticity and changes in regime* | Already cited in `RESEARCH-PROTOCOL.md` §11 as answering the specification question. SWARCH exists precisely because pure regime-switching does not absorb the volatility dynamics. | **[UNREAD] — BLOCKING** |
| **Klaassen (2002)**, *Improving GARCH volatility forecasts with regime-switching GARCH* | Directly on multi-step MS-GARCH forecasting. | **[UNREAD]** |
| Patton (2011), *Volatility forecast comparison using imperfect volatility proxies* | Source of the §6 loss-function restriction. | **[UNREAD]** |
| Giacomini & White (2006), *Tests of conditional predictive ability* | Source of the §8 test choice. | **[UNREAD]** |

**These two must be read before implementation, not after.** The repo's own lesson, recorded
2026-08-14 in `systemic_state.py`: *an `[UNREAD]` tag on the paper whose construction you need is
itself the defect* — the absorption-ratio strand was refuted precisely because Kritzman's published
construction went unread. `RESEARCH-PROTOCOL.md` §11 records that **S3 was rediscovered
empirically instead of read**, and calls that the failure §0 exists to stop.

**If Marcucci or Hamilton & Susmel already answers §1 for weekly equity index returns, §0 rule 2
says the run carries no information and must not happen** — the finding gets recorded with its
citation instead.

### 14.1 Adjudication rule — "similar" does not mean "settled"

Added 2026-08-14, binding, because the failure mode runs in **both** directions. §0 rule 3 exists to
stop a finding being rediscovered instead of read; it must not become a way to cancel experiments
by gesturing at an adjacent paper. A paper cancels this run **only** if it answers *this* estimand.

Check each axis explicitly and record the answer per paper. **Any material mismatch means the paper
informs the design and does not settle it:**

| axis | this experiment |
|---|---|
| estimand | incremental information in the **h-step predictive density**, not a point variance forecast |
| frequency | weekly |
| horizon | h = 13 primary, mechanism-derived from mixing time |
| model structure | MS with **switching mean and variance**, no within-regime ARCH, against **plain GARCH(1,1)** |
| evaluation | encompassing regression + Giacomini-White, strict walk-forward with vintage parameters, adversarial alignment check |
| asset / sample | SPY weekly 2003-2026 |

**Three distinct verdicts, and the middle one is the likely and most useful outcome:**

- **SETTLED** — the paper answers §1 on a matching estimand at a comparable frequency and horizon.
  Record the citation and the number; **do not run.**
- **INFORMS** — the paper addresses the substantive question with materially different
  specification, data, frequency, horizon or loss. **Document the distinction explicitly in this
  stub, adopt whatever construction it settles, and run the remainder.** A near-miss makes the
  experiment *narrower and better specified*, not unnecessary.
- **ORTHOGONAL** — different question. Note and move on.

**A verdict of SETTLED requires reading the paper's actual results section, not its abstract.**
An abstract states what was compared; it does not state at what horizon, on what functional, or
with what power. Recording "settled" from an abstract would be the same defect as recording
`[UNREAD]` and proceeding — the failure this gate exists to prevent, wearing the opposite mask.

**The asymmetry that makes this gate operable without full-text access:** a *stated mismatch* on
any axis is dispositive and can be read off an abstract, so an abstract **can** establish INFORMS.
A *stated match* is not dispositive, because the axes that decide it — horizon, functional, power —
live in the results. So an abstract can **never** establish SETTLED. Verdicts below are recorded at
the level the available access actually supports.

### 14.2 Adjudication performed 2026-08-14

**Marcucci (2005) — verdict: INFORMS. Does not settle. Access: abstract and headline result from
two independent sources; results section NOT read.**

| axis | Marcucci (2005) | this experiment | match |
|---|---|---|---|
| frequency | **daily** | weekly | no |
| horizons | **1 day to 1 month** (~1-22 trading days) | h = 4, 13, 26 **weeks** | no — his *longest* ≈ our *shortest* |
| regime model | **MRS-GARCH** — GARCH dynamics *inside* each regime | plain MS, constant variance within regime | no — his MS side is this repo's **S3** |
| opponent | standard GARCH family incl. EGARCH, GJR | plain GARCH(1,1) | partial |
| functional | point volatility forecasts, statistical + risk-management (VaR) loss | **h-step predictive density**, log score / CRPS | no on primary, yes on secondary |
| test | loss-function comparison | encompassing + Giacomini-White | no |

**Three consequences, all recorded BEFORE any code — which is what makes them legitimate:**

1. **The predicted shape in §13 is weakened by the empirical record and §5's prediction is amended
   in tone, not in content.** Marcucci reports MRS-GARCH beating standard GARCH at **short**
   horizons under statistical loss, with **standard asymmetric GARCH (EGARCH, GJR) with non-normal
   innovations best at longer horizons (beyond about a week)**. That is regime advantage **decaying**
   with horizon — the opposite trend to this stub's "maximum near the mixing horizon". It is **not a
   direct contradiction**: different functional (point variance, which §3.1 already predicts is
   non-discriminating), different frequency, and horizon ranges that do not overlap. But the prior
   now leans harder toward a null at h=13, and §5's falsifiable prediction stands **with that leaning
   recorded against it.** A confirmatory result would now be more surprising, which raises rather
   than lowers its value.
2. **Plain GARCH(1,1) is a weak opponent, and a win against it would not establish much.** If
   EGARCH/GJR with non-normal innovations dominate at longer horizons, then beating GARCH(1,1) at
   h=13 does not show that discrete regimes beat *smooth mean reversion* — only that they beat the
   weakest smooth model. **Added as a declared second rung: GJR-GARCH(1,1).** Its purpose is stated
   narrowly — *is the plain-GARCH bar too low?* — and it is **not** the mechanism test, because
   swapping it in would confound "discrete vs smooth" with "symmetric vs asymmetric". GARCH(1,1)
   remains the mechanism-isolating primary opponent.
3. **Marcucci's MS side is this repo's S3, not its base specification.** MRS-GARCH carries ARCH
   inside each regime. So the paper is evidence about **S3**, and is not evidence about the plain
   two-state switching-variance model this repo actually fits.

**Hamilton & Susmel (1994) — verdict: UNRESOLVED. STILL BLOCKING.**

Confirmed: it uses **U.S. weekly stock returns** — this repo's exact frequency, which is the single
strongest match on any axis of any paper here — and it introduces **SWARCH**, i.e. ARCH *within*
regimes, which again is this repo's **S3** rather than its base specification. Secondary sources
agree it shows ARCH/GARCH impute spurious persistence that regime switching removes.

**Its out-of-sample forecast comparison could not be obtained.** Journal of Econometrics is
paywalled, and no legitimate open copy was found. Nothing below abstract level is recorded here.

**Why this one genuinely blocks.** If H&S establishes that pure regime switching is inadequate
*without* within-regime ARCH, that is not a fact about the horizon — it is a fact about whether this
repo's **base specification is the right object to test at all**, and it would redirect the
experiment rather than refine it. `RESEARCH-PROTOCOL.md` §11 already cites this paper as answering
the specification question, and §11 also records that **S3 was rediscovered empirically instead of
read.** Running before resolving it risks a third instance of exactly that.

**Acquisition is a manual step through institutional access and is not routed around.**

### 14.3 Gate reassigned to Timmermann (2000), and Timmermann READ — 2026-08-14

**Why the blocker moved, recorded so it is not mistaken for gate-shopping.** A fact changed, not a
preference: reading Kandji & Misko established that **SWARCH is MS-*ARCH*** — ARCH inside the
regimes, chosen to avoid path dependence in the likelihood — so Hamilton & Susmel sits at **rung 4**
while this experiment tests **rung 3**. Under §14.1 a rung-4 paper returns INFORMS, not SETTLED.
Timmermann's model **(1)**, `y_t = mu[S_t] + sigma[S_t] eps_t` with iid innovations and no
within-regime dynamics, **is exactly this repo's specification.** H&S remains an open row at lower
priority; it was not dismissed.

**Read in full** from the LSE Financial Markets Group working paper (DP 323, May 1999), the
author's own institutional copy of what became *J. Econometrics* 96(1), 75-111. **Version caveat:**
this is the working paper, not the published article; they may differ.

**Verdict: INFORMS. Does not settle — and does not kill the experiment.** Timmermann derives
*unconditional* moments and the autocovariance function. He never compares MS against GARCH on
forecast performance, and never treats *conditional* h-step predictive densities, which is our
functional. The §3.2 mechanism — a mixture over `2^h` regime paths **conditional on `xi[t]`** — is
untouched by anything in the paper.

**Three findings that change what this experiment should expect.**

**(a) Skewness requires switching MEANS. Variance switching alone cannot produce it — ever.**
Corollary 1, stated by Timmermann as a necessary condition: *"a necessary condition for the Markov
switching process to generate skewness is that the means in the states differ, and differences in
the variances of the states alone are insufficient to generate skewness."* His footnote adds that
this parallels Bollerslev (1986): **standard GARCH without leverage has zero skewness.**

This is the sharpest structural difference yet identified between our model and the benchmark, and
it was invisible before reading the paper:

```
plain MS, switching means   ->  CAN generate skewness
GARCH(1,1), no leverage     ->  skewness identically ZERO, always
```

It is also consistent with a measurement the repo already has and could not explain: **the PIT QQ
panel is asymmetric — the left tail falls off the 45-degree line while the right sits on it.**
That is a skewness signature.

**(b) Consequence for the §11.3 common-mean control, which is heavier than it looked.** Setting
`switching_trend=False` forces skewness to **exactly zero, analytically**. Since GARCH(1,1) also
has zero skewness, the common-mean variant **removes the entire asymmetry axis from the
comparison**, leaving only kurtosis and state-dependent conditional shape — and GARCH generates
excess kurtosis too. §11.3 is therefore not merely a confound control; it is the variant on which a
positive result is *hardest*. Both must still be run and reported together, and the interpretation
in §11.3 stands. **GJR-GARCH (§14.2), which has leverage and therefore can produce skewness, is the
correct opponent for axis (a)** — it was added for an unrelated reason and turns out to be the
right control here.

**(c) Timmermann's own warning lands on our parameters.** He notes that MS models *"fitted to
high-frequency financial data whose means are often very small in all states may have trouble
replicating successfully the skewness found in these data."* Our weekly means are **+0.36% and
−0.26%** — small. So the skewness advantage in (a) may be structurally real and numerically tiny.

**This is computable in advance and it is not a new control.** §9 already makes a power statement
**blocking** before any p-value is interpreted. Corollary 1 gives skewness and excess kurtosis in
closed form from `pi_1, mu_1, mu_2, sigma_1, sigma_2` — all of which are already fitted at 95
walk-forward vintages. **Evaluating it analytically discharges an existing §9 obligation earlier
and more cheaply than the run would**, and could show the experiment is underpowered by
construction before any code is written, which is the outcome §0 rule 2 most wants. Recommended,
not performed — the design is frozen and this is the owner's call.

## 15. What this experiment does NOT license, whatever it returns

- **No directional claim.** A variance result says nothing about direction. `wide` never implies
  `bearish`, `short`, or `to cash`. `TRANSLATION-LAYER.md` is binding.
- **No sizing rule.** A better variance forecast can *support* variance targeting or risk
  budgeting; it cannot establish directional alpha. Any future sizing rule must state in writing
  whether its justification is **variance control** or **directional prediction** — different
  claims, different evidence.
- **No economic claim.** `RESEARCH-PROTOCOL.md` §0 firewall: a loss-function number may not appear
  in the same sentence as a cost-benefit judgement. Economic value is gated on D5 and unmeasured.
- **No tail claim about regime structure** while the innovation distribution is shared (§12).
- **No verdict beyond the claim tuple.** Weekly, these three horizons, these two assets, variance
  and density only.
