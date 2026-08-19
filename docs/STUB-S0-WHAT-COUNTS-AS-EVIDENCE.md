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

---

*Results rule — nothing above this line may be edited once results exist below it.*

---

## Results

Not yet run.

## Related

- [[CHARTER]] §2 — the null · §5 — the gate · §6 — the stopping rules · §9 — the queue
- [[docs/RESEARCH-PROTOCOL]] §0 — the gate's fields · P8 — data versus representation
- [[docs/POINT-IN-TIME-DISCIPLINE]] — the leak register and the pre-flight checklist
- [[closed-research/docs/TRANSLATION-LAYER]] §5 — why h=1 is void, and the reverting-versus-martingale
  mechanism this stub inherits
