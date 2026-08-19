# §5 Stub — S0, what would constitute evidence that the return-generating environment has changed

Committed 2026-08-18, **before any code**, under [[CHARTER]] §5 and [[docs/RESEARCH-PROTOCOL]] §0.
Status: preregistration. Results are appended below the results rule in a later commit, and nothing
above that rule may be edited once they exist.

**This is the first item in the return-state queue and currently the only one.** [[CHARTER]] Q1 is
not designable until S0 returns, because S0 is what fixes Q1's functional, horizon and falsification
threshold. S0 is deliberately the smallest thing that can be wrong.

---

## 1. The question

> **What observation would constitute evidence that the return-generating environment has changed —
> as opposed to evidence that returns are, as everyone already knows, heteroskedastic?**

Stated as the thing that must be produced: a **discriminating functional** `T` and a **horizon** `h`
such that a discrete persistent state structure and the charter's null N1 make *different* claims
about `T` at `h`, together with a demonstration on synthetic data that the difference is large enough
to be seen with the history that exists.

**Why this is an experiment and not a memo.** The claim "these two model classes differ at horizon
`h` on functional `T`" is checkable, and it is checkable **without touching market data at all** —
simulate from each class at known parameters and measure. That is the whole of S0. It is a power and
identification study, and it can fail.

## 2. The nine fields

**1. QUESTION.** **(A) Existence** — S0 does not test whether states exist; it establishes what a
test of existence would have to measure, and whether such a test is possible on this history at all.
It is the identification precondition for A.

**2. CLAIM TUPLE.** `(frequency = daily; horizon = h in {1, 5, 21, 63} trading days; functional =
candidate set below; sample = SYNTHETIC ONLY, generated under each class at stated parameters; null =
N1)`.

**No market data is used in S0.** That is not a limitation, it is the design: a power study run on
the real series would let the answer be chosen by looking at the data.

**3. HYPOTHESIS AND PREDICTED OUTCOME.**

The hypothesis:

```
H(S0)  There exists a functional T and a horizon h > 1 at which a two-state
       persistent switching process and a smoothly-reverting continuous-scale
       process (N1), CALIBRATED TO MATCH ON THE UNCONDITIONAL DISTRIBUTION AND
       ON THE FIRST-ORDER PERSISTENCE OF SQUARED RETURNS, produce different
       expected values of T -- by a margin detectable at n = one daily equity
       history.
```

The matching clause is the entire content of the hypothesis. Two models that differ in unconditional
variance or in raw volatility persistence are trivially distinguishable and the comparison would be
uninformative — that is the mistake [[docs/PROBLEM-MAP]] F10 records, where MS and EWMA were raced at
h=1 where they are structurally identical.

**Predicted outcome, written before any code, with its reason.** Split, because the fields differ:

- **`T` = h-step conditional variance: PREDICTED NULL, and therefore forbidden as Q1's functional.**
  Both classes have the point-forecast form `long-run level + geometric^h x current deviation`. This
  is derivable and is already recorded in [[closed-research/docs/TRANSLATION-LAYER]] §5. **If S0's
  measurement contradicts this, the implementation is wrong, not the theory** — that is the
  correctness check, not the finding.
- **`T` = h-step predictive **density** score: PREDICTED DIFFERENT, weakly, and the margin is the
  open question.** A switching process's h-step density is a *mixture* over state paths; N1's is a
  scaled innovation. They differ in shape even when they agree in variance. **The prediction is that
  the difference exists and is small**, and the useful output of S0 is the size, not the sign.
- **`T` = persistence-of-persistence — the variability of realized variance over blocks, at
  a scale longer than N1's mean-reversion time: PREDICTED DIFFERENT, and this is the coordinate
  most likely to survive.** A switching process holds a level for a geometrically-distributed
  sojourn; a mean-reverting scale process pulls back continuously. **But E6 constrains it: a Markov
  chain's squared-return ACF decays geometrically, and so does a GARCH-type model's. If the two decay
  rates can be matched by construction, this coordinate dies at the matching step**, and that is a
  legitimate S0 outcome.
- **`T` = a drawdown functional (excursion depth distribution, CDaR curve): PREDICTED DIFFERENT AND
  UNUSABLE.** Path functionals are where a switching process should show its sojourn structure most
  visibly — and they are where effective n collapses to the number of excursions. **The prediction is
  that this coordinate separates the classes in expectation and cannot be estimated on one history.**
  If that prediction is right it is worth more than a positive result, because it forecloses a route
  the program would otherwise take.

**Literature check.** Named, and none of them settles S0:

- **Hansen (1992), Garcia (1998), Cho & White (2007)** — testing the number of regimes by likelihood
  ratio is invalid because the transition parameters are **unidentified nuisance parameters under
  the one-state null**, so the LR statistic has no chi-square limit (*Davies' problem*). **This is
  why S0 exists and why Q1 will not be an LR test.** These papers state the problem; they do not
  supply this program's functional.
- **Diebold & Mariano (1995), Giacomini & White (2006)** — out-of-sample predictive comparison,
  which sidesteps the identification problem by asking a predictive rather than a parametric
  question. The machinery is already implemented in `closed-research/src/evaluation.py`. They supply
  the *test*, not the *functional*.
- **Rydén, Teräsvirta & Åsbrink (1998)** — hidden Markov models reproduce most stylized facts of
  daily returns **except the slow decay of squared-return autocorrelation**. Closest prior art to
  S0's third coordinate, and the reason its prediction is hedged.
- **Timmermann (2000) Prop. 5** — the geometric-decay result, `[D]`, already in this repository as
  E6. **It constrains coordinate three before it is measured.**
- **No paper found that states which functional discriminates a persistent discrete state structure
  from a smooth-reverting one at a given horizon on a single equity history, with power.** If one
  exists, S0 is redundant and should not run. Searching for it is part of S0 and the search is
  reported.

**4. WHY IT MATTERS.** Without S0, Q1 is unfalsifiable in the specific way this repository has failed
twice: a functional gets chosen, a difference gets measured, and it is not knowable afterwards
whether the difference was a property of the market or of the model class
([[docs/RESEARCH-PROTOCOL]] P8). S0 also carries a real chance of ending the program before any
market data is touched, which is the cheapest possible ending.

**5. DATA.** None. Synthetic paths generated under both classes at stated parameters, with a stated
seed, at sample lengths matching what exists: `n ~ 8,300` daily observations (SPY 1993–2026) and
`n ~ 25,000` (^GSPC 1927–2026). **Effective n per coordinate is the output, not an input** — for the
drawdown coordinate it is the excursion count, roughly 10–15 at systemic depth, and S0's job is to
say so numerically rather than by argument.

**6. IDENTIFICATION.**

- **The population is the model classes, not the market.** S0 establishes what is *measurable*; it
  establishes nothing about equities.
- **Identified in magnitude:** the separation between classes at stated parameters, and the sampling
  variability of each candidate `T` at the stated `n`. Both are simulation quantities and are as
  identified as the number of replications.
- **NOT identified, and not identifiable by S0:** whether any real market resembles either class;
  whether the parameters chosen for the switching process are the ones a market would have; the
  behaviour of either class under misspecification. **Parameter choice is the soft spot** — a
  switching process with far-apart regimes and long sojourns will separate on everything. So the
  parameters are declared in advance (§3 of the eventual implementation) and swept, and **the
  reported result is the whole sweep, never its most favourable point** ([[docs/POINT-IN-TIME-DISCIPLINE]],
  the standing rule against quoting an assumption at its primary value).

**7. FALSIFICATION.** Declared numerically, before the run:

```
H(S0) is FALSIFIED if, after matching on the unconditional distribution and on
first-order squared-return persistence, NO candidate functional achieves a
separation between the two classes exceeding 2 standard errors of its own
sampling distribution at n = 8,300, at any h in {1, 5, 21, 63}, anywhere in the
declared parameter sweep.
```

**And the second, more likely failure mode is declared with equal force:** if a functional separates
the classes **only** at parameter settings where the two are already distinguishable by eye — regimes
far apart, sojourns long — then the functional is measuring the parameters, not the structure, and it
is reported as **not discriminating**, not as a success.

**8. IF IT SUCCEEDS / IF IT FAILS.**

- **Succeeds** (at least one functional separates the classes with adequate power under matching):
  Q1 becomes designable. Its functional, horizon and falsification threshold are **taken from S0's
  output and are not re-chosen**. That is the whole of what success licenses.
- **Fails** (no functional separates them under matching, at this `n`): **the program ends under
  [[CHARTER]] §6 as INDETERMINATE — cannot be settled on the available history.** Not S1, because S1
  requires a measurement on the market. This is the stronger and cheaper ending: it says the question
  cannot be asked, not that the answer is no. **It does not license a search for a better functional
  after the fact.**
- **Settles nothing** (results depend entirely on the parameter sweep, with no stable region): report
  as INCONCLUSIVE, and the program ends the same way. A functional that discriminates only where you
  did not need it is not a functional.

**9. WHAT IT MAY MOTIVATE NEXT.** **Exactly one thing: the design of Q1**, and only under the success
branch, and only with the functional and horizon S0 returns.

**It may not motivate:** a second synthetic study; a third model class; a search for a functional
that works after one has failed; the collection of new data; any measurement on market data; or any
statement whatever about equity returns. **S0 touches no market data and therefore cannot produce a
finding about markets.** If its result feels like one, that feeling is the error.

## 3. What this experiment cannot establish

Stated plainly because the temptation will be to read more into it:

- **Nothing about whether return states exist.** S0 measures instruments, not the market.
- **Nothing about whether a state would be detectable in real time.** That is question (D) and is
  untouched.
- **Nothing about which model class is right.** Both are wrong; the question is only whether they are
  *distinguishable*, and on what.
- **Nothing that survives a change of parameterisation** beyond the declared sweep.

## 4. The one thing to watch while running it

**The matching step is where this experiment can be quietly ruined.** If the two classes are
calibrated to match on the unconditional distribution and on squared-return persistence and the
matching is imperfect, every downstream separation is contaminated by the mismatch, and it will look
like a finding. **The matching quality is therefore reported as a first-class output, before any
separation number**, and a separation smaller than the mismatch is reported as **void**, not as
small.

This is the same defect class as E0's: the closed program spent three days quoting a drawdown
reduction that was 82% an accounting artifact, because the thing being compared was not what it
appeared to be.

## 5. Operationalisation — AMENDMENT, committed 2026-08-18 before any code

§2 field 6 said the parameters are declared in advance and swept. This is that declaration. It is an
amendment rather than part of the original stub because it was written second; it is committed
**before** the implementation and before any result exists.

### 5.1 The two classes

**Switching (the claim).** `r_t = sigma(S_t) * z_t`, `z ~ iid N(0,1)`, `S_t` a two-state Markov chain
with transition matrix `P`. Parameterised by the three quantities that actually matter, rather than by
`P` directly:

```
    kappa  = v2 / v1      variance ratio between states
    pi2                   stationary occupancy of the wide state
    lambda = p11+p22-1    second eigenvalue of P -- the persistence

    p11 = 1 - pi2 (1 - lambda)          pi1 = 1 - pi2
    p22 = lambda + pi2 (1 - lambda)     vbar = pi1 v1 + pi2 v2 = 1 (scale normalised)
```

**N1 (the null).** GARCH(1,1) with Gaussian innovations —
`sigma2_t = omega + alpha r2_{t-1} + beta sigma2_{t-1}`, persistence `psi = alpha + beta`.

### 5.2 The matching, and it is exact on more than the stub promised

The moments, both standard:

```
  SWITCHING     E[r^4] = 3 (pi1 v1^2 + pi2 v2^2)                    = K_MS
                Cov(r2_t, r2_{t-k}) = pi1 pi2 (v1-v2)^2 lambda^k
                rho_MS(k) = pi1 pi2 (v1-v2)^2 lambda^k / (K_MS - 1)

  GARCH(1,1)    omega = 1 - psi
                rho_G(1) = alpha (1 - beta psi) / (1 - 2 alpha beta - beta^2)
                rho_G(k) = psi^(k-1) rho_G(1)
                K_G = 3 (1 - psi^2) / (1 - psi^2 - 2 alpha^2)
```

**Both squared-return ACFs are geometric from lag 1** — the switching one by Timmermann (2000)
Prop. 5, which is E6 in this repository. So setting `psi = lambda` and then solving for the single
`alpha` that gives `rho_G(1) = rho_MS(1)` matches **the entire squared-return autocorrelation
function at every lag, exactly**, on top of the unconditional variance.

**This is a stronger match than §2 required, and it is a substantive finding in itself:** the
stub predicted that coordinate three would "die at the matching step" if the two decay rates could be
matched by construction. They can, exactly, and E6 is the reason. **That prediction is therefore
resolved before the run, deductively.** It is recorded here rather than presented later as a result.

**The residual mismatch is kurtosis**, and it is the matching-quality number reported first. Three
free GARCH parameters cannot also match a fourth moment.

**Feasibility is checked and reported, never silently skipped.** A cell is infeasible if no
`alpha in (0, lambda)` attains `rho_MS(1)`, or if GARCH's fourth moment does not exist
(`3 alpha^2 + 2 alpha beta + beta^2 >= 1`). Infeasible cells are counted in the report.

### 5.3 The functionals, and what each is for

All computed on one simulated path of `n = 8,300` daily observations, zero drift.

| | functional | horizons | what it is for | prediction |
|---|---|---|---|---|
| **T1** | sample ACF of squared returns at lag `h` | 1, 5, 21, 63 | **correctness check on the matching.** Matched exactly at every lag by construction | `d' ≈ 0`. A non-zero `d'` means the implementation is wrong, not the theory |
| **T2** | excess kurtosis of `h`-day aggregated returns | 1, 5, 21, 63 | distributional shape at horizon — the mixture-over-state-paths versus scaled-innovation difference | differs; **T2 at h=1 IS the residual mismatch**, so T2 at h>1 is informative only in excess of T2(1) |
| **T3** | sd of log realized variance over non-overlapping blocks of length `B` | B = 21, 63 | persistence-of-persistence, at a scale longer than the mean-reversion time | predicted to die at matching (§5.2) |
| **T4** | max drawdown; `CDaR(worst 5%)` of the cumulative path | — | sojourn structure in path geometry, where a switching process should show most | separates in expectation, **not estimable on one history** |

**T2(1) doing double duty is deliberate.** It makes the stub's rule — *a separation smaller than the
mismatch is void* — exact rather than a matter of judgement: any `d'` on T2 at `h > 1` must exceed
the `d'` on T2 at `h = 1` to count at all.

### 5.4 Discriminability, and the falsification threshold

The question is whether **one** history of length `n` can tell the classes apart, so the statistic is
the standardised separation of the two sampling distributions of `T` at that `n`:

```
    d'(T) = | mean_MS(T) - mean_G(T) |  /  sqrt( (var_MS(T) + var_G(T)) / 2 )
```

`d' >= 2` is the preregistered threshold, which is §2 field 7's "2 standard errors of its own
sampling distribution at n = 8,300".

### 5.5 The sweep, declared in full

```
    kappa   in {2, 4, 6.5}         6.5 ~ (3.84/1.50)^2, this repo's own fitted regime ratio
    pi2     in {0.15, 0.30}
    lambda  in {0.95, 0.98, 0.995}

    18 cells. n = 8,300 (SPY daily 1993-2026). R = 400 replications per class per cell.
    seed = 20260818.
```

**The whole sweep is reported, never its most favourable cell.** And the anti-flattery rule from §2
field 7 is made mechanical: if the surviving cells are only the extreme corner
(`kappa = 6.5` and `lambda = 0.995`), the functional is reported as **measuring the parameters, not
the structure** — which is a failure, not a partial success.

### 5.6 Scale — AMENDMENT, committed 2026-08-18 after the checks, before any separation number

`vbar = 1` normalises the unconditional variance for the algebra. **T1, T2 and T3 are scale-invariant
and are unaffected by it** — an autocorrelation of squared returns, an excess kurtosis, and the sd of
*log* realized variance all cancel a constant factor. **T4 is not.** Drawdown geometry depends on the
actual volatility level, and at unit variance a single "day" is a 100% standard-deviation move: every
path drops far enough that `1 - W/M` saturates at exactly 1.0 in floating point and the functional
cannot discriminate anything, for reasons of units rather than structure.

**Declared: `DAILY_SD = 0.01`**, applied at generation so every functional sees the same series.
1% per day is ~16% annualised, the right order for a broad equity index. The choice is a *units*
choice; it changes nothing about T1–T3 and it makes T4 computable at all.

**How this was found, recorded because the sequence is the point.** The preregistered check
`max drawdown lies in [0, 1)` failed on the first run of the test suite — **before a single
discriminability number had been computed.** That is the check doing its job: the defect was in the
units of a functional, it was caught by an invariant declared in advance, and the fix is a declared
constant rather than a re-specification. Had the sweep been run first, T4 would have returned
`d' ~ 0` everywhere and it would have been reported as "path geometry does not discriminate" — a
false negative that looks exactly like a real one.

---

*Results rule — nothing above this line may be edited once results exist below it.*

---

## Results

**RAN 2026-08-18.** `states/s0_discriminating_functional.py`, seed 20260818, 400 replications per
class per cell, 18 cells, all feasible. No market data. Full console output reproduced by re-running
the module.

### 6. Matching quality, reported first

Matched **exactly**: unconditional variance, and the squared-return autocorrelation at every lag
(`|rho_MS(1) - rho_G(1)| <= 1.8e-15` across the sweep). Residual mismatch is kurtosis, and it is
**large** — GARCH sits 3.6% below the switching model at `kappa = 2` and **38.6% below at
`kappa = 6.5`**. Three GARCH parameters cannot also match a fourth moment, as declared.

That mismatch is the floor every separation has to clear, and §4's void rule is applied to **every**
functional rather than only to T2. *(The first implementation applied it to T2 alone; applying it
everywhere is strictly more stringent and can only remove survivors. Recorded because it is a change
to the analysis, made before the verdict was read.)*

### 7. The four functionals

| | prediction | result | verdict |
|---|---|---|---|
| **T1** squared-return ACF | `d' ~ 0` — correctness check | max `d' = 1.035` | **matching confirmed in simulation.** Below threshold, but not zero — see §7.1 |
| **T2** kurtosis of `h`-day sums | different but small | max `d'` at `h>1` is **1.59** against a mismatch floor reaching **6.80**. **0 surviving cells** | **PREDICTION HELD.** Aggregation washes it out. The size is: too small to use |
| **T3** dispersion of block realized variance | **dies at the matching step** | max `d' = 10.22`. **9 surviving cell x block pairs** | **PREDICTION WRONG — and this is the finding.** See §7.2 |
| **T4** max drawdown, CDaR(5%) | separates in expectation, unestimable at `n` | `d' = 0.151` and `0.136`. Mean max drawdown **0.645 switching vs 0.647 null**. **6.1 excursions past 10% per 8,300-day path** | **PREDICTION HELD**, and it is the most useful negative here. See §7.3 |

#### 7.1 The T1 residue, which is a caveat rather than a failure

`d'` reaches 1.035 at `kappa = 6.5`, `lambda = 0.995` — below the threshold, so the correctness check
passes, but it is not zero and the reason matters. **The population ACF is identical by
construction.** What differs is the *sampling distribution* of the estimator: the sample ACF of
squared returns is a ratio of fourth-moment quantities, and the two classes' fourth moments differ.
**A sample ACF is therefore not a clean discriminating statistic even when the population ACFs are
provably equal**, and any future experiment proposing one inherits this caveat.

#### 7.2 T3, and why the deductive prediction was wrong

§5.2 argued deductively that matching the whole squared-return ACF would kill this coordinate. It
did not, and the error is instructive:

> **Matching the autocovariance function of squared returns is not matching the distribution of the
> latent variance process.** The ACF is a second-order object. The dispersion of block realized
> variance depends on the *shape* of the variance process — a two-state chain makes a 21-day block
> mostly-one-state or mostly-the-other, while a GARCH variance drifts smoothly through a continuum.
> Identical autocovariance at every lag; different distribution. **Second-order equality is not
> equality.**

The §5.2 amendment claimed this coordinate was resolved *before the run, deductively*. **That claim
was wrong and is withdrawn.** It is left standing above the results rule, as written, because a stub
edited after the fact is worthless — and because the whole point of preregistering a deduction is
that it can be caught being wrong.

#### 7.3 T4, and the route it forecloses

Path geometry does not discriminate: `d' = 0.15` at best, and the mean max drawdown differs by
**0.2 percentage points between the two classes** — 0.645 against 0.647. With **6.1 excursions past
10% per simulated 33-year history**, the effective n of this coordinate is single digits, exactly as
[[docs/PROBLEM-MAP]]'s standing sample-size result implies.

**This closes drawdown geometry as a coordinate for a state-existence claim, and it does so on
synthetic data where the states are known to exist by construction.** That is a stronger foreclosure
than any market measurement could give: if the coordinate cannot see states that are *there*, its
silence on real data would have meant nothing.

### 8. Verdict

**H(S0) SURVIVES, conditionally, on T3.**

Best: `T3` at block 21, `d' = 10.22`, at `kappa = 6.5`, `pi2 = 0.30`, `lambda = 0.950`. Five of
eighteen parameter cells carry at least one surviving functional.

**The anti-flattery rule (§5.5) does not fire** — survival is not confined to the extreme corner, and
in fact `d'` on T3 *falls* as `lambda` rises. **But the survival is conditional, and the condition
travels with Q1:**

```
    survives at kappa  in {4.0, 6.5}          NEVER at kappa = 2.0
    survives at pi2    in {0.15, 0.30}        but 8 of 9 surviving pairs are at pi2 = 0.30
    survives at lambda in {0.95, 0.98, 0.995}
```

**Whether a real equity market has a state contrast that large is not known, is not something S0 can
establish, and is precisely what Q1 would be measuring.** If the market's states are separated by a
variance ratio of 2 rather than 4, this functional cannot see them at `n = 8,300` and Q1 will return
INCONCLUSIVE rather than a negative — which must be written into Q1's stub in advance.

### 9. What this licenses, and what it does not

Under §2 field 9, exactly one thing: **the design of Q1**, with the functional and horizon S0
returned and not re-chosen.

```
  Q1's functional      T3 -- sd of log realized variance over non-overlapping
                       blocks. Block length 21 primary, 63 as the declared
                       sensitivity. Both survived; 21 is stronger in 4 of 5 cells.

  Q1's horizon         daily returns, 21-day blocks. NOT h in {1, 5, 63}.

  FORBIDDEN in Q1      the sample squared-return ACF (T1 -- matched by
                       construction, and see 7.1); aggregate kurtosis (T2 --
                       below its own mismatch floor everywhere); ANY drawdown
                       or path-geometry functional (T4 -- d' = 0.15 where the
                       states are known to exist).

  Q1's floor           any separation Q1 reports must clear the kurtosis-
                       mismatch floor in the same way, and the floor must be
                       computed and reported before the separation.
```

**It does not license:** a second synthetic study; a third model class; a search for a functional
that works better than T3; any change to the null or the frequency; or any statement about equity
returns. **S0 touched no market data and has said nothing about markets.**

**And one thing it explicitly does not license, because it is the obvious next thought:** T3 is not a
state detector. It is a statistic that distinguishes two *model classes* on synthetic data. Using it
to label periods would be [[CHARTER]] §1's questions (A) and (D) collapsed into one, which §1
forbids.

## Related

- [[CHARTER]] §2 — the null · §5 — the gate · §6 — the stopping rules · §9 — the queue
- [[docs/RESEARCH-PROTOCOL]] §0 — the gate's fields · P8 — data versus representation
- [[docs/POINT-IN-TIME-DISCIPLINE]] — the leak register and the pre-flight checklist
- [[closed-research/docs/TRANSLATION-LAYER]] §5 — why h=1 is void, and the reverting-versus-martingale
  mechanism this stub inherits
