# Q1 decision note — what claim is supported, and whether Q1 is licensed

Written 2026-08-19, **before Q1 is designed**, at the claim level rather than the design level.
Companion to [[docs/IDENTIFICATION-UNDER-N1]], which established that Davies' problem does not apply
and that the *alternative* is what goes unidentified.

**Nothing in S0 is altered by this note.** Its result, its four reported anomalies and its record stand
exactly as committed.

---

## 0. The recommendation, stated first

**Q1 IS NOT LICENSED AS FRAMED, and the reason is stronger than the one flagged in the report.** It is
not merely that other DGP classes could produce the same rejection. It is that **S0's matching leaves
free precisely the quantity T3 measures**, so the separation S0 found is, to first order, the residual
mismatch re-expressed at a 21-day scale — and the market's value of that quantity is **already known
from this repository's own evidence**.

**One narrowly scoped gate is required first (§4).** It is cheap, it uses the machinery S0 already
has, and it can end the programme.

This is not the safest claim available. The safest claim would be to run Q1 as a necessary-condition
test and report "the data are not N1". §1.3 shows why that sentence is **predictable in advance**, and
therefore forbidden by [[docs/RESEARCH-PROTOCOL]] §0 rule 2.

---

## 1. What Q1 can establish

### 1.1 The exact proposition

Q1 computes T3 on the observed daily series and compares it against T3's distribution simulated from
a GARCH(1,1) with Gaussian innovations fitted to that series. A rejection supports exactly:

> **P1.** *The dispersion of 21-day integrated variance in the observed series is greater than a
> GARCH(1,1) with Gaussian innovations can produce, given that model's fitted unconditional variance
> and its fitted squared-return autocorrelation.*

That is a well-defined, testable, falsifiable proposition about a **scalar feature of the volatility
process**. It is not a proposition about states, discreteness, persistence, or the number of regimes.

### 1.2 The algebra that pins this down, and it is exact

For any process `r_t = sigma_t z_t` with `z ~ iid N(0,1)` and `E[sigma_t^2] = 1`:

```
    kurtosis  K = 3 E[sigma^4]        =>      Var(sigma^2) = K/3 - 1
```

**This holds identically for both classes S0 compared.** So the residual kurtosis mismatch that
survived S0's matching *is* a mismatch in the dispersion of the variance process — not a correlate of
one, not a proxy for one. **The same quantity, exactly.**

S0 matched the unconditional variance and the entire squared-return ACF. Because
`Cov(r_t^2, r_{t-k}^2) = Cov(sigma_t^2, sigma_{t-k}^2)` for `k >= 1`, matching the ACF matches the
variance process's autocorrelation **in shape but not in scale** — the scale is `Var(sigma^2)`, and
that is exactly what was left free. From S0's own printed Block 1, using `Var(sigma^2) = K/3 - 1`:

| κ | π₂ | λ | `Var(σ²)` switching | `Var(σ²)` null | ratio |
|---|---|---|---|---|---|
| 2.0 | 0.15 | 0.950 | 0.097 | 0.020 | 4.8x |
| 4.0 | 0.30 | 0.950 | 0.523 | 0.163 | 3.2x |
| 6.5 | 0.15 | 0.950 | 1.157 | 0.323 | 3.6x |
| 6.5 | 0.30 | 0.950 | 0.903 | 0.267 | **3.4x** |
| 6.5 | 0.30 | 0.980 | 0.903 | 0.400 | **2.3x** |
| 6.5 | 0.30 | 0.995 | 0.903 | 0.583 | **1.6x** |

**T3 is a measure of variance-process dispersion at the 21-day scale.** Block realized variance is
integrated variance plus estimation noise; the sd of its log is, to first order, the coefficient of
variation of integrated variance, and the within-block aggregation factor is common to both classes
*because the ACF was matched*. So T3 and the mismatch are two estimators of one quantity at two
aggregation scales.

**The void rule does not orthogonalise them.** Requiring `d'(T3) > d'(T2 at h=1)` compares two
estimators of the same difference; T3 wins because it is the **more efficient estimator** — sample
kurtosis on 8,300 observations has enormous sampling variance, sd of log block variance on 395 blocks
does not. The report flagged the rule as "not demonstrably orthogonal". It is now demonstrably **not
orthogonal**, and that flag is upgraded rather than resolved.

### 1.3 Why P1's answer is already known, which is the decisive point

Equity returns are well established to carry more kurtosis than a Gaussian-innovation GARCH(1,1)
implies — it is why the t-innovation variant exists at all. **And this repository measured it
directly.** From [[docs/PROBLEM-MAP]] §1, result **E5**: at `alpha = 0.01` every method breaches at
roughly twice its nominal rate — constant 1.87%, EWMA 2.03–2.36%, MS 1.79% — and the recorded
diagnosis is that *"what they share is the Gaussian assumption"* and that **the tail failure belongs to
the data, not the model.**

So P1's expected answer on SPY is **reject**, and it is derivable before the run from evidence already
in this repository.

> [[docs/RESEARCH-PROTOCOL]] §0 rule 2: *"If the prediction is confident and derivable from theory or
> a citable paper, the run carries no information — do not run it. Record the prediction and its
> source instead."*

**That rule applies to Q1 as framed, and it is the reason Q1 is not licensed.** The rule has been
invoked twice before in this repository's history to stop work; it applies here to work the programme
wants to do, which is the only circumstance in which such a rule is worth anything.

## 2. What Q1 cannot establish

Stated as the propositions a rejection does **not** support, in decreasing order of how tempting each
one will be:

> **Not-P2.** *Return states exist.* The rejection is of one parametric null; it identifies no
> alternative.
>
> **Not-P3.** *The volatility process is discrete rather than continuous.* T3 measures dispersion, and
> dispersion is a property of every conditional-variance process. **Discreteness leaves no fingerprint
> in a dispersion statistic** — this is the specific gap, and §4 is built around it.
>
> **Not-P4.** *There is persistence beyond what the null carries.* The ACF was matched by
> construction, so Q1 carries no information about persistence whatever.
>
> **Not-P5.** *Anything about the conditional return distribution `F_{s,h}`.* Q1 conditions on nothing.
> It is an unconditional specification test, and [[CHARTER]] §1's object is a conditional law.

Not-P5 deserves emphasis because it is structural: **the charter's research object is
`F_{s,h} = law of R_{t:t+h} given S_t = s`, and Q1 never forms a conditional distribution at all.**
Q1 as designed is one step further from the charter's object than the queue's wording suggests.

## 3. Competing DGP classes that produce the same rejection

Given §1.2 — the matching leaves `Var(sigma^2)` free — the competing set is not a list of exotic
possibilities. It is **every process whose variance is more dispersed than the matched null's**:

| class | produces the rejection? | why it matters here |
|---|---|---|
| **GARCH with fat-tailed (t) innovations** | **Yes, and it is the banal explanation** | Same ACF, same unconditional variance, higher kurtosis, hence higher `Var(sigma^2)` by the §1.2 identity. **This is the single most likely generator of a Q1 rejection and it contains no states at all** |
| **Long-memory volatility (FIGARCH, and the hyperbolic-decay literature)** | Yes | Also breaks the ACF match, so it would be rejected for a second reason. Note Rydén, Teräsvirta & Åsbrink report slow ACF decay as precisely what HMMs **fail** to reproduce — so this alternative is favoured by evidence that runs *against* the switching story |
| **Structural breaks in unconditional variance** | Yes, strongly | A level shift inflates block-variance dispersion directly. And a break is not a recurrent state |
| **Stochastic volatility with high vol-of-vol** | Yes | Continuous latent state, i.e. the charter's N2, which is explicitly *not* the claim under test |
| **Jumps in returns** | Yes | Inflates both kurtosis and block-variance dispersion |
| **A two-state persistent switching process** | Yes | The one the programme cares about, and **it is one of six** |

**None of these can be separated from the others by T3**, because T3 responds to the one scalar they
all move. The first row is the decisive one: it is the *default* econometric specification for equity
returns, and it would produce Q1's rejection while containing no state structure whatsoever.

## 4. Does this need another gate? Yes — and it is a sharper question than S0 asked

**A necessary-condition framing does not rescue Q1**, because a necessary condition whose outcome is
known in advance is not a test. So the answer to the question as posed is: **another narrowly scoped
synthetic gate is required, and it is a better experiment than Q1 was going to be.**

### 4.1 What the gate must ask

S0 matched three quantities: unconditional variance, `rho(1)`, and the ACF decay rate. Three
parameters, three constraints, and `Var(sigma^2)` left free — which turned out to be the thing being
measured. **The fix is to close that degree of freedom and ask what, if anything, survives.**

A null with **four** free parameters — a GARCH with standardized-t innovations, `(omega, alpha, beta,
nu)` — can match unconditional variance, `rho(1)`, decay rate, **and kurtosis**, i.e. `Var(sigma^2)`
as well. With all four matched:

```
    matched: the unconditional variance
             the entire squared-return ACF
             Var(sigma^2)  -- the dispersion of the variance process

    free:    the SHAPE of the variance process's distribution.
             A two-state chain puts its mass at two points.
             A GARCH-t spreads it continuously.
```

> **The gate's question: with the dispersion of the variance process matched as well, does any
> functional still separate a two-state chain from a continuous-variance null at n = 8,300 — and if
> so, is it a functional of the SHAPE of the variance distribution rather than its spread?**

That is a test of **discreteness**, which is what [[CHARTER]] §2 says the claim under test actually is
("discreteness is the claim under test; persistence is not"). S0, in retrospect, did not test it.

### 4.2 Why this is the right size

- **It reuses S0's machinery**: the same simulator, the same `d'`, the same sweep, the same void rule,
  the same seed discipline. One additional distribution and one additional matching equation.
- **It can end the programme.** If nothing separates once dispersion is matched, then discreteness is
  not identifiable at this sample size, and [[CHARTER]] §6 gives **INDETERMINATE** — the cheapest
  possible ending, still with no market data touched.
- **It is falsifiable in the direction that hurts.** The programme wants a survivor; the honest prior
  after §1.2 is that most candidates die.
- **It inherits S0's negatives unchanged**: drawdown geometry stays foreclosed, aggregate kurtosis
  stays below its own floor, the sample ACF stays forbidden.

### 4.3 What it is not

It is **not** a redesign of the programme, not a new null in the charter's sense (N1 remains "a
continuous smoothly-reverting conditional-scale process"; a t-innovation GARCH is a member of that
class, not a new class), and **not a licence to keep adding nulls until something survives.** If this
gate returns nothing, the programme ends. That must be written into its stub before it runs.

## 5. What [[CHARTER]] §6 licenses under each Q1 outcome

Answered for Q1 **as currently framed**, because that is what was asked — and the answer is itself an
argument for §4.

| Q1 outcome | what it means | §6 licence |
|---|---|---|
| **Rejects N1** (the predicted outcome, §1.3) | the observed variance process is more dispersed than a Gaussian-innovation GARCH implies | **Nothing.** It matches no stopping rule. It does not satisfy S5, and it is not evidence for states — six DGP classes produce it, one of which is the standard specification for equity returns. **The programme would be exactly where it started, having spent its first market-data experiment** |
| **Fails to reject** | the observed dispersion is consistent with the null | **S1 only if power is demonstrated** — and power against a switching alternative requires knowing the market's state contrast, which is unmeasurable without assuming the alternative. Absent that, [[CHARTER]] §6's fourth outcome applies: **INCONCLUSIVE, never NULL** |
| **Rejects in the *other* direction** (less dispersed than the null) | almost certainly a fitting or specification artefact | not a finding; a defect report |

**Both principal outcomes are uninformative for the programme's question.** One licenses nothing, the
other licenses an ending that cannot be reached without assuming what is under test. Under the gate's
own field 5 — *what would surprise me, and what does it change about what we claim to know* — Q1 as
framed has no answer, and an experiment with no answer to field 5 does not run.

## 6. The strongest claim genuinely supported, stated plainly

Not the weakest. The strongest the identification structure carries:

> **This programme can, today, measure whether the dispersion of the equity market's variance process
> exceeds what a Gaussian-innovation GARCH implies. It already knows the answer is yes (E5). It cannot
> yet measure whether that variance process is discrete, and discreteness is the claim
> [[CHARTER]] §2 put under test.**

The gap between those two sentences is the gate in §4, and closing it is the whole of what should
happen next.

## 6b. R1 — the result S0 actually produced, entered into the record

**S0 is not an abandoned experiment and must never be described as one.** It produced a determinate,
citable negative, and it is the first established result of the return-state programme. It is given an
identifier here so that later documents cite it rather than re-deriving it.

> ### R1 (2026-08-18, deductive + measured)
>
> **T3 — the dispersion of log realized variance over 21-day blocks — is not evidence of
> discreteness. Its separation between a two-state chain and a matched GARCH(1,1) is algebraically
> reducible to a difference in variance-process dispersion, which S0's matching left free.**
>
> The reduction is exact, not approximate: with `E[sigma^2] = 1`, kurtosis `K = 3 E[sigma^4]` gives
> `Var(sigma^2) = K/3 - 1` for both classes, so the residual kurtosis mismatch S0 declared **is** the
> unmatched variance-process dispersion, and T3 measures that dispersion at a 21-day scale. S0's
> surviving functional and S0's declared mismatch are two estimators of one quantity; T3 won on
> efficiency, not on content.
>
> **Kind:** `[D]` for the reduction, `[I]` for the `d'` magnitudes that motivated looking.
> **Evidence:** [[docs/STUB-S0-WHAT-COUNTS-AS-EVIDENCE]] sections 6-8 for the measurement, section 1.2
> above for the algebra. **Effective n:** 400 replications x 18 cells, synthetic; the reduction itself
> needs none.

**What R1 establishes, and it is a methodological result rather than a fact about markets:**

1. **Matching two moments of a variance process does not isolate its shape.** Matching the level and
   the autocorrelation of `sigma^2` leaves its *scale* free, and a great many natural functionals
   respond to scale. A matching argument must state which moment each functional reads.
2. **A void rule built from a second statistic of the same quantity is not a control.** S0's rule
   required `d'(T3)` to exceed `d'(kurtosis)`; both estimate `Var(sigma^2)`, so the rule compared two
   estimators of one difference and rewarded the more efficient one. **The rule was not wrong to be
   there — it was wrong to be trusted**, and the way it failed is only visible because the rule was
   declared in advance.
3. **The functional that survives a synthetic gate is not thereby the functional the programme wants.**
   S0 asked *what separates these classes* and got an honest answer to that question. The programme's
   question was *what identifies discreteness*, and those turned out to be different questions.

**R1 is why S0b exists**, and it is the reason S0b's control functional is T3 itself.

## 7. Carried forward unchanged

- **S0's four anomalies stand exactly as reported.** `d'` falling with persistence remains **recorded
  as unexplained**; §1.2 offers a candidate — within each (κ, π₂) row the variance-dispersion ratio
  falls monotonically with λ (3.4x → 2.3x → 1.6x) exactly as `d'` does (10.22 → 6.66 → 3.24) — but the
  correspondence **fails across rows** (ρ = 0.18 over the full sweep), because occupancy also drives
  the estimator's sampling noise. **A partial, post-hoc, unpreregistered hypothesis. Not a finding,
  and it does not amend S0.**
- Occupancy dominance at π₂ = 0.30, systematic kurtosis mismatch, and the non-orthogonality of the
  void rule all stand. The last is **upgraded from "not demonstrably orthogonal" to "demonstrably not
  orthogonal"** by §1.2.
- **The 9.7% smoothed/filtered issue remains a Q2/Q3 state-construction constraint.** Neither Q1 nor
  the §4 gate infers a state path, so neither must solve it.
- **The reading gaps remain explicit.** Garcia (1998) and Carter & Steigerwald (2012) were not
  obtained. **No argument here rests on the Cho–White QLR**, and none may until Carter & Steigerwald
  is read.

## Related

- [[CHARTER]] §2 — the null and what discreteness means · §6 — stopping rules · §9.1 — what S0 fixed
- [[docs/IDENTIFICATION-UNDER-N1]] — the identification gate this note builds on
- [[docs/STUB-S0-WHAT-COUNTS-AS-EVIDENCE]] — the experiment, unaltered
- [[docs/PROBLEM-MAP]] §1 E5 — the measured Gaussian-tail failure that makes P1's answer predictable
