# §5 Stub — S0b, the discreteness gate

> **CLOSED PROGRAMME — PRESERVED AS EVIDENCE.** The return-state programme terminated 2026-08-19 as
> INDETERMINATE ([[CHARTER]] §11). This document is kept intact because the reasoning is the asset;
> nothing in it is a live instruction, and no experiment it describes is queued. **The code moved to
> `closed-research/return-states/`** — path references inside the results sections below record where
> it was when it ran. Full record: [[closed-research/return-states/README]].


Committed 2026-08-19, **before any code**, under [[CHARTER]] §5 and [[docs/RESEARCH-PROTOCOL]] §0.
Status: preregistration. Results are appended below the results rule in a later commit, and nothing
above that rule may be edited once they exist.

> ## S0b IS THE FINAL SYNTHETIC IDENTIFICATION GATE.
>
> **There is no S0c.** The null family is not expanded again. If S0b returns no determinate result,
> the programme terminates as INDETERMINATE under [[CHARTER]] §6 — it does not acquire another
> objection to test. **No market data is touched until S0b has returned a determinate result**, and
> S0b itself touches none.
>
> This condition is authored into the preregistration rather than promised alongside it, because a
> scope condition that lives outside the document it constrains is not a constraint.

**Why this gate exists and S0's did not suffice.** S0 matched the unconditional variance and the whole
squared-return ACF and found a surviving functional, T3. [[docs/DECISION-Q1-CLAIM]] §1.2 then showed
by exact algebra that **S0's matching left free precisely the quantity T3 measures** — the dispersion
of the variance process — so T3's separation carried no information about discreteness. S0b closes
that degree of freedom and asks what, if anything, is left.

---

## 1. The question

> **With the dispersion of the variance process matched as well as its level and its autocorrelation,
> does any functional still separate a discrete two-state variance from a continuous one at
> `n = 8,300` — and is it a functional of the variance distribution's SHAPE rather than its spread?**

[[CHARTER]] §2 states that "discreteness is the claim under test; persistence is not." **S0 tested
neither.** It tested spread. S0b tests discreteness, which is the last dimension the charter's claim
rests on that has not been examined.

## 2. The nine fields

### 1. QUESTION

**(A) Existence**, and specifically its identification precondition. S0b does not test whether states
exist. It establishes whether *discreteness* is distinguishable from *continuity* at all, once every
easier difference has been matched away.

### 2. CLAIM TUPLE

```
  frequency   daily
  horizon     block lengths B in {21, 63} trading days
  functional  the shape functionals of section 3 below
  sample      SYNTHETIC ONLY, both classes at declared parameters
  null        N1', a GARCH(1,1) with standardized Student-t innovations,
              matched on THREE constraints (section 2.4)
```

**N1' is inside [[CHARTER]] §2's N1 and is not a new null class.** N1 is "one continuous,
smoothly-reverting conditional-scale process with iid standardized innovations." A t-innovation GARCH
is a member of that class. **No charter amendment is required and none is made.** Changing the
innovation law is what makes the third matching constraint solvable; it is not a widening of the
family.

### 2.4 THE NULL AND THE MATCHING, EXACTLY SPECIFIED

**The alternative (unchanged from S0).** `r_t = sigma(S_t) z_t`, `z ~ iid N(0,1)`, `S_t` a two-state
Markov chain, parameterised by `(kappa, pi2, lambda)` exactly as in
[[docs/STUB-S0-WHAT-COUNTS-AS-EVIDENCE]] §5.1, unconditional variance normalised to 1, returns scaled
by `DAILY_SD = 0.01`.

**The null.**

```
  r_t = sigma_t z_t          z ~ iid standardized t(nu), E[z^2] = 1, E[z^4] = k
  sigma2_t = omega + alpha r2_{t-1} + beta sigma2_{t-1}
  psi = alpha + beta

  k = 3(nu - 2)/(nu - 4)     for nu > 4;   nu = (4k - 6)/(k - 3)
```

**Three matching constraints, fixed here and not revisited:**

```
  (M1) UNCONDITIONAL VARIANCE       omega = 1 - psi        =>  E[sigma2] = 1

  (M2) VARIANCE-PROCESS ACF         psi = lambda           matches the decay ratio
       and                          rho(1) = rho_MS(1)     matches the level

       rho(1) = alpha (1 - psi beta) / (1 - 2 psi beta + beta^2)

       ** and this expression does NOT depend on k **, because it is a ratio of
       two autocovariances that both carry the same innovation-kurtosis factor.
       So alpha and beta come out IDENTICAL to the values S0 solved, and the
       squared-return ACF is matched at every lag exactly as it was there.

  (M3) VARIANCE-PROCESS DISPERSION  E[sigma^4] equal across classes,
       equivalently Var(sigma^2) equal, since Var(sigma^2) = E[sigma^4] - 1
       when E[sigma^2] = 1.

       null:         E[sigma^4] = (1 - psi^2) / (1 - alpha^2 k - 2 alpha beta - beta^2)
       alternative:  E[sigma^4] = pi1 v1^2 + pi2 v2^2

       Solved for the one remaining free parameter:

           k = [ 1 - 2 alpha beta - beta^2 - (1 - psi^2)/m ] / alpha^2
                where m = E[sigma^4] of the alternative
```

**Feasibility, checked and reported per cell, never silently skipped.** A cell is infeasible if the
required `k <= 3` (no t distribution has less kurtosis than a normal), if `nu <= 4` (no fourth
moment), or if `alpha^2 k + 2 alpha beta + beta^2 >= 1` (the null's fourth moment does not exist).
Infeasible cells are counted and listed, and **a sweep with many infeasible cells is itself a
result** — it would say the null family cannot reach the alternative's variance dispersion.

### 2.5 What the matching deliberately UNMATCHES, declared before the run

Matching `Var(sigma^2)` while letting innovation kurtosis absorb the difference **unmatches the
return kurtosis, in the opposite direction from S0**:

```
    K_alternative = 3 m            (Gaussian innovations)
    K_null        = k m            with k > 3   =>  K_null > K_alternative
```

**This is the intended trade and it is the point of the gate.** Return kurtosis mixes two things —
how dispersed the variance process is, and how fat the innovation tails are. S0 held the innovations
fixed and let the variance dispersion absorb everything, which is why its functional measured
dispersion. S0b holds the variance dispersion fixed and lets the innovations absorb the difference,
so that anything still separating the classes must come from the **shape** of the variance
distribution.

**The residual mismatch is therefore return kurtosis with its sign flipped**, and the void rule of
§2.7 applies to its absolute value.

### 3. HYPOTHESIS AND PREDICTED OUTCOME

```
H(S0b)  With (M1), (M2) and (M3) all imposed, there exists a functional of the
        SHAPE of the block-variance distribution that separates a two-state
        chain from N1' by d' >= 2 at n = 8,300, in a region of the declared
        sweep that is not the extreme corner.
```

**The functionals, and a prediction for each, written before any code.**

All are computed on `log RV_B`, the log realized variance over non-overlapping blocks of length `B`,
for `B` in `{21, 63}`.

| | functional | why it is a shape measure | **prediction, and its reason** |
|---|---|---|---|
| **T3** *(control)* | sd of `log RV_B` — S0's survivor | spread, not shape | **PREDICTED NULL.** `Var(sigma^2)` is matched by (M3), so the quantity T3 measures is now equal by construction. **This is S0b's correctness check: a non-zero `d'` means the matching is broken, not that a difference was found** |
| **T5** | excess kurtosis of `log RV_B` | a two-point mixture with long sojourns is **bimodal**, hence **platykurtic**; a continuous variance process is unimodal | **PREDICTED DIFFERENT, with the alternative NEGATIVE relative to the null.** The most direct consequence of two mass points |
| **T6** | skewness of `log RV_B` | occupancy asymmetry — at `pi2 = 0.15` the alternative sits mostly in one state with excursions into the other | **PREDICTED WEAKLY DIFFERENT and asymmetric in `pi2`. Low confidence**, recorded so a null here is not read as a surprise |
| **T7** | Sarle's bimodality coefficient of `log RV_B`, `(g1^2 + 1)/(g2 + 3)` | the direct measure of the thing under test | **PREDICTED DIFFERENT and the most likely survivor**, since it is built to detect exactly two-mass-point structure |

**And one structural prediction that the sweep will test, which S0's anomaly makes worth stating:**

> **Discreteness should be HARDEST to see at low `lambda` and EASIEST at high `lambda`** — the
> opposite of S0's T3 behaviour. A 21-day block under short sojourns averages across many switches and
> washes the two-point structure out; under long sojourns a block sits inside one state and the two
> masses survive aggregation. **If S0b's surviving functional instead strengthens as `lambda` falls,
> it is behaving like S0's T3 and should be suspected of measuring dispersion again.**

**Literature check.** Sarle's bimodality coefficient is a standard descriptive statistic (SAS
documentation; discussed in Pfister et al. 2013 on bimodality detection) and carries no distributional
theory here — it is used as a *statistic whose null distribution is simulated*, which needs no theory.
**No paper is known to state which functional distinguishes a discrete-variance process from a
continuous one matched on variance, ACF and `Var(sigma^2)`**; if one exists, S0b is redundant and must
not run. The search is part of S0b and is reported. **The Cho–White QLR is not used and no argument
here rests on it**, per the standing block pending Carter & Steigerwald (2012)
([[docs/IDENTIFICATION-UNDER-N1]] §2).

### 4. WHY IT MATTERS

Because [[CHARTER]] §2 rests the entire programme on discreteness, and after S0 the repository has
**no evidence that discreteness is detectable at all.** S0b either supplies that evidence or ends the
programme, and it does so without market data. It is the cheapest remaining question that can
terminate the charter.

### 5. DATA

None. Synthetic paths under both classes at declared parameters, stated seed. `n = 8,300` daily
observations (SPY 1993–2026), 400 replications per class per cell, **the same sweep as S0**:

```
    kappa   in {2, 4, 6.5}
    pi2     in {0.15, 0.30}
    lambda  in {0.95, 0.98, 0.995}
    n = 8300, REPLICATIONS = 400, seed = 20260819, DAILY_SD = 0.01
```

**The sweep is not re-chosen.** It is S0's, so the two gates are comparable cell by cell.

**Effective n per coordinate is an output.** At `B = 21` a path yields 395 blocks; at `B = 63`, 131.
The shape functionals are third- and fourth-moment statistics of those blocks, so their sampling
variance is large and **the `B = 63` column is expected to be noisier per replication even where the
signal is cleaner** — see §2.7.

### 6. IDENTIFICATION

- **The population is the model classes, not the market.** S0b establishes what is measurable and
  says nothing whatever about equities.
- **Identified in magnitude:** the separation between the classes at declared parameters, and each
  functional's sampling distribution at `n = 8,300`. Both are simulation quantities.
- **NOT identified, and not identifiable by S0b:** whether any market resembles either class; whether
  the alternative's parameters are ones a market would have; the behaviour of either class under
  misspecification.
- **NOT addressed, and named so it is not forgotten:** structural breaks in unconditional variance and
  long-memory volatility are **outside both classes**. S0b cannot separate a two-state chain from
  either. That limitation is carried forward into §8 and is the principal thing a pass does *not* buy.

### 2.7 THE VOID RULE, and the aggregation diagnostic

**The void rule, carried from S0 and applied to every functional.** A separation counts only if it
clears **both** the preregistered threshold **and** the residual mismatch, the latter measured as
`d'` on the return kurtosis in the same cell, in absolute value. Declared here rather than discovered:
this is a **heuristic control, not an orthogonalisation** — exactly the criticism that
[[docs/DECISION-Q1-CLAIM]] §1.2 upgraded against S0's void rule, stated in advance this time.

**The aggregation diagnostic, which is S0b's specific defence against repeating S0's error.** Fatter
innovation tails in the null inflate the estimation noise in realized variance, which reshapes
`log RV` for a reason that has nothing to do with discreteness. The declared discriminator:

> **If a functional's separation STRENGTHENS from `B = 21` to `B = 63`**, it is reading the shape of
> integrated variance, because longer blocks average estimation noise away while preserving the
> underlying variance distribution. **If it WEAKENS**, it is more likely reading estimation noise, and
> is reported as such.

This is declared before the run and is not a post-hoc interpretation.

### 7. FALSIFICATION

```
H(S0b) IS FALSIFIED if, with (M1)-(M3) imposed, NO shape functional (T5, T6, T7)
attains d' >= 2 while also clearing its own return-kurtosis mismatch floor, at
either block length, anywhere in the declared sweep.
```

**Three further conditions under which a nominal survivor is reported as NOT DISCRIMINATING**, all
declared in advance:

1. **The anti-flattery rule**, carried from S0: survival confined to the extreme corner
   (`kappa = 6.5` and `lambda = 0.995`) means the functional measures the parameters, not the
   structure.
2. **The dispersion tell**: a functional whose `d'` *rises as `lambda` falls* is behaving like S0's
   T3 (§3) and is reported as suspected of measuring dispersion again.
3. **The noise tell**: a functional that survives only at `B = 21` and weakens at `B = 63` (§2.7) is
   reported as reading estimation noise.

### 8. IF IT SUCCEEDS / IF IT FAILS — and "success" is not "we found a difference"

#### 8.1 PASS — what it licenses, exactly

A pass requires a shape functional clearing threshold **and** floor, in a non-corner region, surviving
all three tells of §7.

**A pass licenses exactly one thing: THE DESIGN OF Q1. Not its execution.** Q1's stub returns for
approval before any market data is read.

**And Q1 inherits S0b's design rather than reopening the identification question:**

```
    Q1's null          N1', GARCH-t matched under (M1)-(M3). NOT re-chosen.
    Q1's functional    whichever shape functional S0b returns. NOT re-chosen.
    Q1's block length  whichever B it survived at. NOT re-chosen.
    Q1's void rule     the return-kurtosis floor, computed and reported
                       BEFORE the separation.
    Q1's power clause  a negative is INCONCLUSIVE, not S1, unless Q1
                       demonstrates power against the contrast the market
                       actually appears to have.
```

**The exact proposition a passing S0b would license Q1 to test:**

> *The shape of the market's block-variance distribution is inconsistent with a continuous-variance
> process matched to it on unconditional variance, on the squared-return autocorrelation at every lag,
> and on the dispersion of the variance process itself.*

**What that still would not establish, declared now so it cannot be quietly widened later.** Structural
breaks in unconditional variance and long-memory volatility remain outside the null. A Q1 rejection
would be evidence **against a continuous-variance GARCH-t and for two-mass-point structure among the
alternatives considered** — it would not exclude a break process. **Q1's stub must handle that by a
declared robustness check (subsample stability of the functional), not by commissioning another
gate**, because there is no gate after this one.

#### 8.2 FAIL — what it terminates, exactly

**The programme terminates.** [[CHARTER]] §6, outcome INDETERMINATE: *the question cannot be settled
on the available history*, which is not the same as the answer being no.

Concretely, and this is the whole content of the scope condition at the top of this file:

- **No S0c.** The null family is not widened again, the functional set is not extended, the sweep is
  not enlarged, and the sample size is not increased to chase a marginal cell.
- **No market-data experiment.** Q1 is not written. Q2 and Q3 never existed.
- **`CHARTER`, `README` and the hub record the termination**, and the repository becomes what
  `closed-research/` already is: preserved, reproducible, and closed.
- **The negative is worth having and is stated as such.** It would say: *the discreteness of the
  equity return-generating environment is not identifiable from a single daily history at this sample
  size, once every easier difference is matched away.* That is a real result about what can be known,
  established without ever fitting a model to market data.

#### 8.3 INDETERMINATE-BY-INSTABILITY

If results depend entirely on the sweep with no stable region — survivors scattered without pattern,
or contradicting each other between `B = 21` and `B = 63` — the verdict is **INCONCLUSIVE and the
programme terminates under §8.2.** A functional that discriminates only where it was not needed is not
a functional.

### 9. WHAT IT MAY MOTIVATE NEXT

**Exactly one thing, and only on the pass branch: the design of Q1**, under §8.1's inherited
constraints.

**It may not motivate:** a third synthetic gate; a fourth matching constraint; another innovation
distribution; a longer sample; a different alternative class; or any statement whatever about equity
returns. **S0b touches no market data and therefore cannot produce a finding about markets.**

## 3. What this experiment cannot establish

- **Nothing about whether return states exist.** It measures instruments.
- **Nothing about detectability in real time.** That is question (D), untouched, and neither S0 nor
  S0b infers a state path — so the smoothed-versus-filtered constraint
  ([[docs/POINT-IN-TIME-DISCIPLINE]] row 1) does not bind here and remains a **Q2/Q3**
  state-construction constraint.
- **Nothing about structural breaks or long memory.** §6 and §8.1.
- **Nothing that survives a change of parameterisation** beyond the declared sweep.

## 4. The one thing to watch while running it

**The matching step, again, and for a new reason.** S0's matching was exact on its two constraints and
the failure was that it matched the wrong things. S0b's third constraint (M3) is solved through a
kurtosis parameter, so **an error in the fourth-moment algebra would silently leave `Var(sigma^2)`
unmatched and reproduce S0's defect exactly.**

`T3` is in the functional list as the control for precisely this. **`d'` on T3 must come back near
zero. If it does not, the run is void** — not interesting.

---

*Results rule — nothing above this line may be edited once results exist below it.*

---

## Results

**RAN 2026-08-19.** `closed-research/return-states/s0b_discreteness_gate.py` (at `states/` pre-archive), seed 20260819, 400 replications per class per
cell, 18 cells. No market data.

> # THE RUN IS VOID.
>
> **The control failed.** T3 was included in the functional list under §4 precisely so that a broken
> (M3) would announce itself, and the preregistered instruction was: *"`d'` on T3 must come back near
> zero. If it does not, the run is void — not interesting."*
>
> **Max `d'` on T3 across every cell and block: 7.416.** The threshold is 2.0.
>
> Under the frozen criteria this is neither PASS nor FAIL. The shape functionals are reported below
> for the record and **none of them is interpretable.**

### 6. Feasibility and matching quality

**All 18 cells feasible; none skipped.** Required innovation kurtosis `k` ran 3.56 to 9.91, i.e. `nu`
from 14.80 down to **4.87** — to reach a switching model's variance dispersion, a GARCH needs
genuinely fat innovations.

| constraint | residual |
|---|---|
| **(M1)** unconditional variance | exact by construction |
| **(M2)** squared-return ACF at every lag | `<= 1.8e-15` |
| **(M3)** `Var(sigma^2)` | `<= 3.4e-14`, and independently checked to `1e-10` in `checks.py` |

**The declared unmatching of return kurtosis is large and rises as `Var(sigma^2)` falls:** +18.5% at
`kappa = 6.5, lambda = 0.995`, and **+230.2%** at `kappa = 2.0, lambda = 0.95`.

### 7. Why the control failed — diagnosis, not repair

**(M3) is holding.** `Var(sigma^2)` is matched to 3.4e-14 and the check asserts 1e-10 independently.
The matching is not broken. **What was wrong is the control's premise.**

The stub asserted, via R1, that T3 measures variance-process dispersion, so matching `Var(sigma^2)`
would drive its `d'` to zero. **That is true only when both classes share an innovation law**, which
was S0's situation and is not S0b's. Two channels were missed, and both are structural:

```
  (i)  RV_block = SUM sigma2_t z2_t, so its dispersion carries the ESTIMATION
       NOISE of z2, whose size is set by E[z^4] = k.
       And k IS THE INSTRUMENT (M3) USES.
       Matching Var(sigma^2) therefore necessarily unmatches the noise in every
       realized-variance statistic.

  (ii) sd(log RV) is not a function of Var(sigma^2) alone. The variance of a LOG
       depends on the whole distribution of the level, not just its second
       moment -- so T3 was never a pure spread statistic on the log scale.
```

**Channel (i) is visible directly in the numbers, and it is monotone in the right direction:**

| | `Var(sigma^2)` | required `k` | `d'` on T3 at B=21 |
|---|---|---|---|
| `kappa = 2.0`, `pi2 = 0.15` | 0.096 | 9.91 / 6.29 / 4.28 | **7.42 / 5.86 / 2.92** |
| `kappa = 4.0`, `pi2 = 0.15` | 0.546 | 5.87 / 4.51 / 3.65 | 2.92 / 2.17 / 1.09 |
| `kappa = 6.5`, `pi2 = 0.15` | 1.158 | 5.38 / 4.27 / 3.56 | **0.08 / 0.02 / 0.22** |

Where the true variance dispersion is small, RV is dominated by estimation noise and the noise
mismatch shows up at `d' = 7.4`. Where it is large, the true signal dominates and the control behaves
as intended, `d' = 0.02`. **The control is not failing at random; it is failing exactly where the
matching instrument bites hardest.**

**This is not a coding defect.** It is an obstruction: **matching the variance process's dispersion
requires an instrument that contaminates every realized-variance functional used to read its shape.**

### 8. The other frozen criteria, reported mechanically and NOT interpretable

Recorded because they were preregistered and because a void run should not be able to hide its
numbers.

**Surviving cells.** 45 cell x functional pairs clear the threshold; 43 also clear their own mismatch
floor, across 13 of 18 parameter cells. By functional: `T7_b63` 13, `T7_b21` 12, `T6_b21` 6, `T6_b63`
5, `T5_b21` 4, `T5_b63` 3. Largest: **`T7` (Sarle's bimodality coefficient) at `d' = 11.74`**, B=21,
`kappa = 6.5, pi2 = 0.30, lambda = 0.980`.

**Tell 1 — anti-flattery.** Does **not** fire. Survival spans `kappa` in {2.0, 4.0, 6.5} and `lambda`
in {0.95, 0.98, 0.995}.

**Tell 2 — the dispersion tell**, and the `lambda`-direction prediction of §3. Predicted: `d'` **rises**
with `lambda`.

| | rises | falls | flat | verdict |
|---|---|---|---|---|
| `T5_b21` | 2 | 4 | 0 | **CONTRADICTED** — behaves like S0's T3 |
| `T6_b21` | 3 | 2 | 1 | HELD |
| `T7_b21` | 1 | 3 | 2 | **CONTRADICTED** — behaves like S0's T3 |
| `T5_b63` | 2 | 4 | 0 | **CONTRADICTED** |
| `T6_b63` | 3 | 3 | 0 | INDETERMINATE |
| `T7_b63` | **5** | **0** | 1 | **HELD**, and cleanly |

**Tell 3 — the noise tell.** Stronger at B=63 in: `T5` 5/18, `T6` 5/18, **`T7` 10/18**. And `T7` splits
by regime contrast — stronger at B=63 in **5 of 6** cells at `kappa = 2.0`, but only **2 of 6** at
`kappa = 6.5`.

**The one pattern worth recording, and it is a hypothesis rather than a finding.** `T7` at B=63 is the
only column that satisfies the `lambda` prediction cleanly (5 rises, 0 falls) *and* strengthens with
aggregation in the majority of cells. That is what a genuine shape signal was predicted to look like.
**It is not a result, because the control voided the run**, and it may be an artifact of the very noise
channel §7 identifies. It is written down so that it is neither lost nor promoted.

### 9. What the preregistration does NOT say, and this is a gap

§4 names the void state — *"the run is void, not interesting"* — but **§8's outcome list has three
branches (PASS, FAIL, INDETERMINATE-BY-INSTABILITY) and a void control is none of them.** No licence
is attached to this outcome anywhere in the stub.

**That gap is flagged and is not filled here.** Filling it after seeing the result is exactly the
move the programme's rules exist to prevent. The two readings are:

```
  (a) VOID means the gate never ran. Repairing the control and re-running is
      completing S0b, not commissioning S0c.
      RISK: this is indistinguishable, from the outside, from adjusting an
      experiment until it works.

  (b) VOID means the DESIGN was wrong, and S0b was the final gate. The
      programme terminates as INDETERMINATE under CHARTER section 6.
      RISK: it discards an obstruction that is arguably itself the answer to
      the identification question.
```

**And the obvious repair is precisely what the scope condition forbids.** The natural fix is a null
whose variance dispersion is a free parameter *of the variance process* rather than of the innovation
law — a lognormal stochastic-volatility null with Gaussian innovations, say — which would leave the
RV estimation noise matched. **That is a different null family, i.e. S0c**, ruled out in advance by
this stub's own header and by [[CHARTER]] §9.4.

**The decision is the author's and is deliberately not taken inside the experiment.**

## Related

- [[CHARTER]] §2 — the null and what discreteness means · §6 — stopping rules · §9.3 — why Q1 was not
  licensed
- [[docs/DECISION-Q1-CLAIM]] — the identity that made this gate necessary, and **R1**, the negative
  result S0 actually produced
- [[docs/STUB-S0-WHAT-COUNTS-AS-EVIDENCE]] — S0, unaltered, whose sweep and machinery this reuses
- [[docs/IDENTIFICATION-UNDER-N1]] — why Davies' problem does not apply, and the two reading gaps
