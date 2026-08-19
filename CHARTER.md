# Charter — Return States

Adopted 2026-08-18. **This is the only active research program in this repository.**

Two programs are closed and preserved, reproducible, in `closed-research/`: the prediction/regime
program ([[closed-research/README]], closed 2026-08-17) and the rolled-put / tenor intervention
program ([[closed-research/intervention/README]], closed 2026-08-18). Neither is a branch, a
dependency, or a backlog. The reasoning that closed the first is a dated amendment in
[[docs/PROBLEM-MAP]] Part I; the reasoning that closed the second is in its own README and in §9
below.

**The repository name is historical.** `core-risk-overlay` names a program that no longer runs.

---

## 0. The sentence

> **We are not trying to win the pricing game. We are trying to determine whether the return
> distribution itself enters distinguishable states, how those states transition, and whether the
> change in distribution is real, persistent, and identifiable.**

And the first principle, which the last two programs each violated in a different way:

> **We study changes in the distribution and dynamics of returns. We do not begin by selecting an
> intervention.**

## 1. The research object

Let `r_t` be returns on a stated frequency, `I_t` the information available at time `t`, and `h` a
stated horizon. The object is the conditional law of the forward return path:

```
    F_{s,h}(.)  =  law of  R_{t:t+h}  given  S_t = s
```

The program asks four questions, in this order and no other:

```
  (A) EXISTENCE         is there a partition {s} with F_{s,h} != F_{j,h} for
                        some s != j, against a STATED null, on a functional
                        and horizon declared in advance?

  (B) CHARACTERISATION  if so, WHICH properties of the distribution differ --
                        and, equally reportable, which do not?

  (C) TRANSITION        how does S_t move? persistence, transition structure,
                        and the distribution conditional on a transition
                        having just occurred.

  (D) IDENTIFICATION    is {s} recoverable from the sample -- and separately,
                        is S_t measurable with respect to I_t, using no
                        future information?
```

**The active program terminates at (D).** Nothing downstream of (D) is in scope.

**A, B, C and D are never collapsed.** "This state looks risky, therefore reduce exposure" is not a
finding; it is four unstated inferences wearing one sentence, and it is the exact reasoning this
charter exists to prevent.

## 2. The null — the load-bearing definition

`F_{s,h} != F_{j,h}` is satisfied trivially. Any conditional-variance process produces a different
conditional distribution at every `t` with no states, no discreteness and no transition matrix. **A
bare existence test therefore carries no information and is forbidden under §5 field 3.**

The program's content is exactly whatever a state structure has that the null does not.

```
  N0   iid draws from one fixed distribution
       -> rejected a priori. NOT a permitted null; a run against it is decoration.

  N1   one continuous, smoothly-reverting conditional-scale process with iid
       standardized innovations
       -> the honest opponent. Conditional distributions differ at every t;
          there is no state.

  N2   a continuous, slowly-varying latent state
       -> discreteness is the claim under test; persistence is not.
```

**DECISION D1, fixed 2026-08-18: the null is N1.** Reasons: it is the honest opponent rather than a
strawman; [[closed-research/docs/TRANSLATION-LAYER]] §5 identifies it as the sharper comparison than
EWMA and records that it was **never built in this repository**; and it makes the claim under test
*discreteness and persistence structure* rather than "the conditional distribution varies", which is
not in doubt and has not been since the 1980s.

**DECISION D2, fixed 2026-08-18: the frequency is daily.** E8 is decisive — the weekly series cannot
resolve volatility memory at all: at n=1750 the ACF band is +/-0.0469 and the empirical
squared-return ACF is inside it by lag 8, while daily resolves it to lag 212. Any persistence claim
made on weekly data is unfalsifiable on this repository's own evidence. Carried cost, declared:
`RELIABLE_MIN_OBSERVATIONS = 520` is a weekly figure and does not transfer (U5), and daily brings
microstructure and non-synchronous-close issues weekly did not have.

**Both decisions are fixed BEFORE the first experiment and are not revisited after seeing a result.**
Changing the null or the frequency once a result exists is selection on outcome at the level of the
whole program, and it is the leak this program is most exposed to.

## 3. What this program may and may not investigate

**MAY.** Return observations at stated frequency and horizon. Unconditional and conditional return
distributions. Candidate partitions and their conditional laws. Distributional distance, divergence
and density scoring. Persistence and transition structure. Distributions conditional on a recent
transition. Which distributional properties differ across states and which do not. Sensitivity of
all of the above to frequency, sample, market, horizon and representation class. **What is not
identified.**

**MAY NOT.** Allocation. Exposure. Position sizing. Instrument selection. Hedging. Options in any
role — pricing, implied volatility, skew, surface, chains, tenor, strike, roll, monetisation.
Trigger construction. Threshold tuning against portfolio performance. Trading. Alpha. Sharpe. Return
maximisation. Drawdown *reduction*. Economic capture. Whether anything is worth doing.

**Portfolio P&L may never define, select, validate or tune a state.** A state definition chosen
because it produced better historical portfolio outcomes is not a state definition; it is a backtest
with a latent variable in it.

**Three boundary cases, ruled in advance because they will otherwise be argued case by case:**

- **Drawdown geometry is IN as a characteristic, OUT as an objective.** `D(t) = 1 - W(t)/M(t)` is a
  functional of the return path and a legitimate coordinate on which `F_s` may differ. The moment a
  number is reported as drawdown *bought*, *reduced* or *avoided*, the boundary has been crossed.
- **Ex-ante observability is question (D), not a signal question.** *Is `S_t` measurable with respect
  to `I_t`* is in scope. *Does knowing `S_t` help* is not. The test: if the answer would be reported
  as a return, a Sharpe, a hit rate, a capture fraction or an exposure, it is out.
- **Comparison against a public benchmark is IN as identification, OUT as competition.** Whether a
  state representation's content is nested inside a cheaper public measurement is a question about
  what has been identified — and the closed program's D3/F2 answered exactly that for one
  representation. Whether it *beats* that measurement is not this program's question.

**Crossing this boundary requires a NEW CHARTER** — its own question, its own admissible space, its
own gate. Not an amendment. Not an experiment. Not a section added here.

## 4. Naming discipline

States are named by what distinguishes them, never by what one would do about them.

```
  FORBIDDEN as a state label:  bull / bear / neutral - risk-on / risk-off
                               crisis / panic / calm-vs-danger
                               buy / hold / sell - hedge / no-hedge
  FORBIDDEN as an identifier:  signal, trigger, regime_score, exposure, hedge,
                               allocation, position, alpha, edge
```

The precedent is retained because it worked. The closed program's state was named `high_variance`
and never "crisis", because a model of variance is blind to sign by construction — and the measured
drift difference between states **reversed sign between SPY and QQQ** while the down/up tail ratio
straddled 1.0. The naming rule is what stopped a width measurement from being read as a directional
one. Full contract: [[closed-research/docs/TRANSLATION-LAYER]].

**And a model that emits discrete labels has not thereby found a regime.** A label is evidence of a
fitted partition, not of a difference in the return-generating environment. The burden is on the
distribution.

## 5. The gate — nine fields, and no code before they are committed

**No experiment runs until its stub is committed.** The stub is committed *before* the commit
carrying its results. If any field cannot be filled honestly, the experiment does not run.

```
  1. QUESTION           which of A / B / C / D does this move?
                        EMPTY => DO NOT RUN. It goes in PARKED.md.

  2. CLAIM TUPLE        (frequency, horizon, functional, sample, null)
                        A test of a one-step marginal cannot support a claim
                        about a path functional, at any sample size.

  3. HYPOTHESIS         and the PREDICTED OUTCOME with its reason, before any
                        code. Confidently derivable from theory or a citable
                        paper => the run carries no information; record the
                        prediction instead. Includes the LITERATURE check:
                        name the paper that settles this, or state in writing
                        that none does.

  4. WHY IT MATTERS     what it establishes about return states. Not
                        "interesting". Not "we have the data".

  5. DATA               series, frequency, span, provenance, and the
                        EFFECTIVE n PER COORDINATE.

  6. IDENTIFICATION     what population the claim addresses, what is identified
                        in magnitude, and what is NOT. "Not identified" is a
                        permitted answer and is written BEFORE the run.

  7. FALSIFICATION      the observation that kills the hypothesis, stated
                        numerically, declared in advance.

  8. IF IT SUCCEEDS /   both branches written before the run, including the
     IF IT FAILS        branch where it settles nothing.

  9. WHAT IT MAY        exactly one thing, or nothing. NOTHING IS THE DEFAULT
     MOTIVATE NEXT      and the most common correct answer.
```

### 5.1 Per-experiment discipline

```
  STUB -> PREDICTION -> IMPLEMENTATION -> TESTS -> RESULT -> VERDICT
       -> GOVERNANCE UPDATE -> STOP
```

No metric is added after a result is seen. No threshold, window, horizon, sample boundary or
representation is selected on outcome. When the preregistered question is answered the experiment is
over — **including when the answer is interesting.**

**On an interesting result:** `STOP -> RECORD -> INTERPRET -> TEST THE PREREGISTERED IMPLICATION ->
STOP AGAIN.` An interesting result licenses at most the one thing field 9 named. A result that
suggests five new experiments has produced zero; all five are written into [[PARKED]] and none runs.

**If an experiment changes the research question, STOP and ask.** That is a charter amendment, not a
finding.

## 6. Stopping rules — program level

The program **ends, successfully**, on any of:

```
  S1  the state structure is not distinguishable from N1 on the declared
      functional, with power DEMONSTRATED rather than assumed
  S2  it is distinguishable in sample and does not survive out of sample or
      across independent markets
  S3  it is distinguishable but its content is nested inside a measurement
      already available, so nothing new is identified
  S4  it is distinguishable and real, but S_t is not measurable with respect
      to I_t -- states exist and cannot be located in real time
  S5  A, B, C and D are all answered
```

**S1 through S4 are findings, not failures.** Each **ends the program** rather than motivating a
search for a representation that avoids it.

This clause is here because [[docs/RESEARCH-PROTOCOL]] P4 records that "do not optimise toward
usefulness" was enforced rigorously on individual runs and **never once applied to the program
itself**. Two programs have now closed. The pressure at this moment is to make the third produce
something.

A fourth outcome is preregistered and legitimate: **indeterminate — cannot be settled on the
available history.** A result failing its power or identification requirement is INCONCLUSIVE, never
NULL.

**The research is allowed to end without producing a trading strategy. That is a successful result.**

## 7. The research / decision firewall

**Research may establish:** that states exist or do not; what distinguishes them; how they persist
and transition; what is identified and what is not; whether the state is observable in real time.

**Research may not establish:** that anything should be done about it.

There is no `decision/` directory and none will be created empty — an empty directory is an
invitation to fill it. If a decision layer is ever built it begins with its own charter and inherits
from this one only the *findings*: never the code, never the framing, and never an implicit
obligation created by a phrase like "this could be used to".

**The motivation is recorded in [[PARKED]], not here.** The reason anyone cares whether return states
exist is that the risk/reward of remaining fully exposed might change across them. That sentence
contains an exposure decision. If it sits in the charter, every experiment gets read against it — and
reading experiments against an intended intervention is precisely how the last two programs ended up
where they did.

## 8. The first phase is an observatory, not a controller

There is no allocation engine, hedge engine, trigger engine, optimizer or portfolio decision rule,
and none is designed. What the program is trying to become able to say at time `t` is:

```
    STATE                          = ?
    IDENTIFICATION QUALITY         = ?
    WHAT CHANGED IN THE            = ?
      RETURN DISTRIBUTION
    HOW PERSISTENT IS IT           = ?
    WHAT EVIDENCE SUPPORTS THIS    = ?
    WHAT REMAINS UNKNOWN           = ?
```

The last two lines are not decoration. They are the columns the closed programs kept omitting.

## 9. The queue

**One queue. One experiment at a time. Each must be capable of killing the next.**

Nothing is listed here without a committed stub or a stated dependency on one. Q2 and Q3 are **not
queued** — they are recorded so the sequence is visible, and neither exists as an experiment until
its predecessor returns.

| | question | status |
|---|---|---|
| **S0** | ~~What would constitute evidence that the return-generating environment has changed?~~ **RAN 2026-08-18. H(S0) SURVIVES, CONDITIONALLY.** One functional discriminates the classes after exact matching on the unconditional variance and the whole squared-return ACF: **T3, the dispersion of block realized variance**, `d'` up to 10.2 at 21-day blocks. Two candidates are **eliminated** and one deductive prediction was **wrong** — see §9.1. [[docs/STUB-S0-WHAT-COUNTS-AS-EVIDENCE]] | **CLOSED** |
| **Q1** | **(A) Existence.** Does a discrete, persistent state structure produce forward return distributions that N1 does not — measured on **T3 at 21-day blocks**, the functional S0 returned? | **EXISTS, not yet designed.** Its functional, horizon and mismatch floor are fixed by S0 and are not re-chosen. **Kills the program under S1** |
| **Q2** | **(B) Characterisation.** Which properties of `F_{s,h}` differ, and which do not? | **does not exist** until Q1 returns |
| **Q3** | **(C) Transition.** Is the distribution conditional on a recent transition different from the distribution conditional on occupying the state? | **does not exist** until Q2 returns |

### 9.1 What S0 fixed, and what it eliminated

Recorded here because Q1 inherits all of it and may not re-open any of it.

**Q1's functional is fixed: `T3`** — the standard deviation of log realized variance over
non-overlapping blocks, block length **21** primary with **63** as the declared sensitivity. Not
chosen; returned.

**Three candidates are eliminated and are forbidden in Q1:**

| | why it is out |
|---|---|
| the sample **squared-return ACF** | matched by construction, so it cannot discriminate — and its residual `d' = 1.03` comes from the *sampling distribution* of the estimator rather than the population ACF, a fourth-moment effect. **A sample ACF is not a clean discriminating statistic even where the population ACFs are provably equal** |
| **aggregate kurtosis** at `h > 1` | max `d' = 1.59` against a kurtosis-mismatch floor reaching 6.80. Below its own floor in every cell. Aggregation washes the difference out |
| **any drawdown or path-geometry functional** | `d' = 0.15` on max drawdown, `0.14` on CDaR(5%); mean max drawdown 0.645 versus 0.647; **6.1 excursions past 10% per simulated 33-year history.** Measured on synthetic data where the states exist *by construction*, so this is a foreclosure no market measurement could have given |

**One preregistered deduction was wrong, and the correction is load-bearing.** §5.2 of the stub argued
that matching the whole squared-return ACF would kill T3 deductively. It did not. **Matching the
autocovariance function of squared returns is not matching the distribution of the latent variance
process** — the ACF is second-order; the dispersion of block realized variance depends on the shape
of the variance process. Identical autocovariance at every lag, different distribution. **Second-order
equality is not equality**, and that sentence now constrains every future matching argument here.

**Q1 inherits a condition it must state in advance.** T3 survives at variance ratios of 4 and 6.5 and
**never at 2**, and 8 of its 9 surviving cells have the wide state occupying 30% of the time. Whether
a real market's state contrast is that large is unknown and is not something S0 could establish. **So
a negative from Q1 is INCONCLUSIVE rather than S1** unless Q1 also demonstrates power against the
contrast the market actually appears to have — and that requirement goes in Q1's stub before it runs,
not after it returns.

**Two deductive results already constrain Q2 and bind before it is designed.** A finite Gaussian
mixture is Gaussian in the far tail for any `k` and any weight (E7, algebra); and the squared-return
ACF of any Markov-switching model decays geometrically for any `k` and any parameters (E6,
Timmermann 2000 Prop. 5). **If tail thickness or non-geometric memory is proposed as a
distinguishing property, the mixture class is disqualified a priori and the comparison does not run
against it.**

**And the warning that attaches to Q2 and Q3 in advance.** The characteristics most likely to
distinguish states interestingly — tail probability, downside concentration, drawdown geometry — are
exactly the ones with effective n ~ 10-15 in all of SPY history. The characteristics with large
effective n — dispersion, serial dependence — are the ones the closed program established are
measurable, are a **width meter with no direction content**, and are **nested inside VIX**. That is
not a reason to skip Q2. It is why §5 field 5 demands effective n *per coordinate*, and it is a live
route to an S3 ending.

## 10. Scope discipline

**The codebase must make scope creep harder, not easier.**

- Everything in this repository is **ACTIVE**, **ARCHIVED**, or **PARKED**. Nothing is ambiguous.
- No "maybe useful later", no "next experiment", no "future signal", no "we could also test", no
  "interesting extension". Those go in [[PARKED]] or they do not exist.
- A new idea passes the §5 gate **before** it gets code. Field 1 empty means parked, not queued.
- A closed idea does not return without meeting its own stated reopening condition.
- An experiment appears in **exactly one** queue — §9 above.
- No orphan TODOs. No speculative branches. No "while we're here" refactors. No utilities
  accumulated without a current research need. No empty directories.
- **Do not inherit an old assumption because it already has code.** The question is always: does this
  help identify or characterise a return state? If not, it is archived, not retrofitted.

## Related

- [[README]] — what the project is · [[PARKED]] — deliberately excluded, including the mandate
- [[docs/RESEARCH-PROTOCOL]] — the gate and the standing principles
- [[docs/POINT-IN-TIME-DISCIPLINE]] — the leak register
- [[docs/PROBLEM-MAP]] — the evidence base, frozen · [[core-risk-overlay]] — chronological log
- [[closed-research/README]] — the prediction program · [[closed-research/intervention/README]] — the
  intervention program
