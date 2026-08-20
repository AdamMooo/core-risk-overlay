# §0 Stub — E2, the drawdown path: CDaR curve and per-excursion depths

> **CLOSED BRANCH — PRESERVED AS EVIDENCE, NOT AS A DESIGN.** This preregistration belongs to the
> rolled-put / tenor intervention program, closed 2026-08-18
> ([[closed-research/intervention/README]]). It is kept intact because its result is evidence and
> because a stub edited after the fact is worthless. **Nothing in it is a queued experiment, and its
> code now lives at `closed-research/intervention/`.** The active program is [[CHARTER]].


Committed 2026-08-18, **before any code**, under [[docs/RESEARCH-PROTOCOL]] §0 and [[closed-research/intervention/CHARTER-INTERVENTION|CHARTER-INTERVENTION]] §8.
Status: preregistration. Results are appended below in a later commit, and nothing above the results
rule may be edited once they exist.

**E2 does exactly one thing: it determines whether any tenor ordering survives when the outcome is
measured across the drawdown path rather than by a single maximum.** No new objective, no new
intervention class, no pricing, no monetisation, no optimisation. The prediction program stays
closed.

**The estimand problem E2 exists to repair, exposed by E1.** `max(D)` on the hedged path and `max(D)`
on the naked path need not describe the same episode. E1's `Psi` column showed they usually do not:
on the full sample, at 26w and 52w in marks, the hedged book's maximum is set in **2003** in 25 of 26
and 51 of 52 alignments while the naked book's is set in **2009**. "Drawdown bought" was therefore a
difference between two different events, and protection beyond the second-deepest episode was
invisible in the coordinate — **max drawdown is censored from below by the next-deepest episode.**

**Two repairs, and they are the whole experiment.**

```
1. CDaR(worst q%)   the occupation-measure tail mean of D. It integrates over the
                    WHOLE path, so it cannot be pinned to a single event, and its
                    dependence on q is itself the measurement of how much rests
                    on one episode.

2. EPISODE-MATCHED   episodes are defined ONCE, on the NAKED book, and both books
   PER-EXCURSION     are measured inside the SAME calendar windows, each from its
   DEPTHS            own within-window peak. The comparison is then guaranteed to
                     be about one event at a time.
```

Defining episodes on the naked book is the load-bearing choice: if the windows were derived from the
hedged path they would move with the intervention, and the estimand would be broken in a new way
rather than repaired.

**Gate closed before the run, not after.** Chekhlov, Uryasev & Zabarankin read 2026-08-18 —
[[docs/MATH-REFERENCE]] §4.1. It found a convention collision (**their `alpha` is a confidence level and
ours is the fraction averaged**), confirmed our estimator as the upper CDaR with a bounded gap, and
established that their convexity result is in the portfolio weights and licenses nothing here. Every
CDaR number below is written as **`CDaR(worst q%)`** for that reason.

---

## 1. Claim tuple

```
frequency   weekly marks
horizon     the full holding period, and per-episode windows within it
functional  (a) CDaR(worst q%) reduction versus the naked book, as a CURVE in q
            (b) episode-matched depth reduction, per naked-defined episode
            NEITHER reduces to max drawdown, and max drawdown is NOT the primary
            statistic anywhere in E2. It appears only as the q -> 0 limit's label
            and as the censoring diagnostic carried from E1
sample      SPY weekly, 1993-02-05 to 2026-08-14, and the inherited 2003-01-24
            subsample. ONE path
design      ALWAYS-ON, h = 1.00, 10% OTM, slope 0.60, 5% offer. No signal, no
            timing, no conditioning
```

**Declared before the run. Every one of these is a researcher degree of freedom and is fixed here,
never selected from a result ([[POINT-IN-TIME-DISCIPLINE]] rows 10-11).**

```
q grid          (0.01, 0.05, 0.10, 0.25, 0.50, 1.00) -- pathfunctionals' default,
                unchanged since E0. q is the FRACTION AVERAGED (ours), so
                q = 0.05 is CUZ's 0.95-CDaR
episodes        defined on the NAKED book, threshold 0.10 primary (E0's, inherited
                and not re-chosen) and 0.20 as a declared robustness column
tenors          (4, 13, 26, 52) weeks
phases          every offset 0..tau-1, as E1 -- carried forward into both verdicts
accountings     marked AND cash, always both, neither standing in for the other
```

## 2. Predicted outcome, with its reason

**Derivable or already measured, therefore carrying no information — recorded, not tested.**

- At `q = 1.00` the coordinate is the average drawdown and is dominated by premium drag, which is
  continuous. E0 already measured it: −0.8pp at 52w cash on the full sample. Nothing to learn.
- The 4-week programme is negative at every `q` in both accountings (E0, phase 0). So a *phase-0*
  ordering test is nearly guaranteed to favour long tenor and is not the question. **The question is
  whether it survives once alignment is swept**, which is why every verdict below is phase-robust.

**The informative part, predicted in advance.**

> **Prediction: under marked accounting the tenor ordering survives at small `q` and is at risk at
> large `q`; under cash accounting it fails at every `q`.**

Reason, and it is M1 again: the ordering is a claim about a long contract *spanning* a deep multi-
month decline, so it should live in the deep tail of the occupation measure and fade as `q` grows to
include ordinary shallow drawdowns where premium drag dominates and nothing is being spanned. The
cash prediction follows from E0 and E1 jointly: the cash reduction at 52w is small (~+3pp at phase 0)
while the phase spread is 12–14pp, so the minimum over alignments should fall below the 4-week
maximum, exactly as it did on max drawdown in E1 (−9.0pp and −7.5pp).

**Secondary prediction, on episodes.** Sign-consistency of `52w >= 4w` across (episode × phase)
pairs: **>= 2/3 under marked**, **< 1/2 under cash**.

**Genuinely uncertain, and this is why the run carries information:** whether the marked ordering
holds at `q = 0.50` and `q = 1.00`, where the gap between tenors is a few points and the phase spread
is comparable to it.

## 3. Literature

**Chekhlov, Uryasev & Zabarankin — `[skim]`, read before this run**, which is what the register
required and what E0 failed to do. Its three consequences are recorded in [[docs/MATH-REFERENCE]] §4.1 and
are already applied in this stub. **Its most useful sentence for us is its own scope caveat:** the
authors define CDaR as a risk function *on a sample-path*, explicitly leaving the definition on a
*set* of sample-paths to future research. The source therefore agrees with this repository's
identification stance — computing CDaR carefully does not turn one path into a population.

No paper settles the episode-matching question, which is a defect of this repository's own estimand
rather than a question about markets. Israelov (2017) measures drawdowns over rolling fixed-length
windows, which sidesteps episode identity instead of resolving it, and its remedy remains
inadmissible under [[closed-research/intervention/CHARTER-INTERVENTION|CHARTER-INTERVENTION]] §2 C2.

## 4. Mechanism for a difference

**Structural difference.** `max(D)` reports one number from one instant; `CDaR(worst q%)` averages
the drawdown process over the fraction of time it is deepest, and per-episode depth reports one
number per event. A long-dated contract that spans one decline changes the *shape* of `D` over
months, so it must be visible in the occupation measure and in the depth of that episode, and it need
not be visible in a maximum that has moved to a different year.

**Horizon at which it is observable:** months, within an episode.

**Functional on which it is observable:** the CDaR curve at small `q`, and the matched depth of the
episodes the contract actually spans. **Invisible at `q = 1.00`** if the mechanism is spanning rather
than carry — which is itself the prediction being tested.

## 5. What would surprise me, and what it changes

- **The ordering surviving at every `q` in CASH** would surprise me and would be the strongest
  positive result the intervention side has produced. It would establish a structural claim in the
  accounting the investor can bank, which E0 and E1 jointly suggest does not exist.
- **The ordering failing at small `q` in MARKS** would mean nothing survives at all, and the tenor
  claim would be withdrawn in full rather than preserved as structure ([[closed-research/intervention/CHARTER-INTERVENTION|CHARTER-INTERVENTION]] §9.1).
- **Sign consistency near 1/2** would mean the tenor choice is a coin flip per episode, which no
  amount of averaging repairs.

**Decision changed:** whether [[closed-research/intervention/CHARTER-INTERVENTION|CHARTER-INTERVENTION]] §9.1's preserved structural ordering keeps its "at every
alignment tested" clause, gains a `q`-range qualifier, or is withdrawn.

## 6. Boundary

**Identification**, primarily — E2 replaces a broken estimand with two that are well defined on the
object we have. **Robustness**, secondarily, since both verdicts are evaluated across every alignment.

It moves neither economic comparability nor the frontier: no outlay is matched, no structure is
ranked for selection, no preference is used.

## 7. Identification status, per coordinate, before the run

**This section is the reason E2 exists, so it is stated per coordinate rather than in one paragraph.**

| coordinate | what is identified | effective n | what is NOT identified |
|---|---|---|---|
| `CDaR(worst q%)`, `q >= 0.25` | the functional on this path, exactly | the number of distinct episodes contributing to the tail — reported as `Psi`, expected ~5-9 | any population magnitude; the episodes are not draws from a superpopulation |
| `CDaR(worst q%)`, `q <= 0.05` | same | approaches **1** as `q` falls — this is the coordinate's known failure mode, not a surprise | anything at all beyond the one episode it collapses onto |
| episode-matched depth reduction | the sign and size *on that episode*, exactly | **1 per episode**, 9 (1993–) and 6 (2003–) expected | that the episodes are exchangeable. 1987, 2000-02, 2008-09, 2020 and 2022 differ in structure, monetary regime and options-market depth |
| sign consistency over (episode × phase) | a **count of a deterministic sensitivity** | not a sample size at all | **no proportion test, no p-value, no confidence interval.** Phases are not independent (E1 §7) and episodes are not exchangeable. The count is descriptive |

**Forbidden in advance, on all four rows:** any standard error, any test statistic, any "mean across
episodes" quoted as an effect, and any use of the phase dimension as replication. **E2 does not add
an observation. Effective n on the benefit side remains 1 for anything resembling a population
claim**, and every number below is a description of one realized path.

## 8. Verdict rules, fixed in advance

**V1 — CDaR ordering, phase-robust.** For each `q`, and separately per accounting and sample:

```
separation(q) = min over phases of bought(52w, q)  -  max over phases of bought(4w, q)

SURVIVES at q     separation(q) > 0
FAILS at q        separation(q) <= 0
```

Reported as the **set of `q` at which the ordering survives**, not as a single verdict.

**V2 — episode sign-consistency ([[closed-research/intervention/CHARTER-INTERVENTION|CHARTER-INTERVENTION]] H2's excursion clause).** Over all (episode × phase)
pairs, the fraction with `reduction(52w) >= reduction(4w)`:

```
SURVIVES    >= 2/3
MARGINAL    (1/2, 2/3)
KILLED      <= 1/2
```

**V3 — does the long-tenor intervention reduce depth at all, per episode.** The fraction of
(episode × phase) pairs with `reduction(52w) > 0`. **Sign only.** No magnitude is quoted from this
row, and it is not a verdict on H2 — it is the context V2's ordering needs in order not to be read as
"52w is good".

Every verdict is reported **separately for marked and for cash**, at both episode thresholds.

## 9. Exact outputs

```
1  q grid, episode set, and phase grid, with the naked book's own excursion depths
2  CDaR(worst q%) reduction curve, per tenor, per accounting, at phase 0
3  V1 -- separation(q) across all phases, per accounting: the surviving q set
4  episode-matched depth reduction, per episode, per tenor, per accounting, phase 0
5  V2 and V3 -- sign-consistency counts across (episode x phase)
6  Psi for every Phi above: episodes contributing to each q-tail, episode count,
   censored/uncovered excursions, phase count, and the E1 censoring flag
7  verdicts against §8
```

New code: `research/path_outcomes.py`, and one function in `pathfunctionals` —
`depth_in_window` — because measuring a book inside someone else's episode window is a genuinely new
mechanic. Both get tests. Nothing else is added, and **no experiment is triggered automatically when
E2 finishes.**

---
--- RESULTS RULE. Everything above was committed 2026-08-18 in cfa4ad2, before
--- `research/path_outcomes.py` existed. Nothing above it has been edited since.
---

# §10 Results — 2026-08-18

Run: `.venv\Scripts\python.exe research/path_outcomes.py SPY`.
New code: `research/path_outcomes.py` and `pathfunctionals.depth_in_window`. Checks: **46 passing**,
four of them new and specific to window-matched depth. Run before and after.

## 10.1 The answer

> **In marks, a tenor ordering survives per-episode and survives on the drawdown curve only in the
> region where that curve has collapsed onto one or two episodes. In cash, no tenor ordering survives
> anywhere on the path, at any `q`, in either sample.**

## 10.2 V1 — the CDaR ordering, phase-robust

`separation(q) = min over phases of bought(52w, q) − max over phases of bought(4w, q)`, in pp.
Positive means the ordering holds at *every* alignment tested.

| sample | acct | worst 1% | 5% | 10% | 25% | 50% | 100% |
|---|---|---|---|---|---|---|---|
| 1993– | marked | **+2.0** | **+0.5** | **+0.2** | **+0.2** | −0.2 | −0.1 |
| 1993– | cash | −8.0 | −7.4 | −5.6 | −3.8 | −3.4 | −2.0 |
| 2003– | marked | **+8.9** | **+4.0** | −0.2 | −3.1 | −2.7 | −1.5 |
| 2003– | cash | −9.3 | −8.7 | −7.6 | −7.2 | −5.6 | −3.1 |

**Surviving set: `q <= 25%` marked (1993–), `q <= 5%` marked (2003–), and NOWHERE in cash, both
samples.**

**Two honest qualifications on the marked row, neither of which changes the verdict.**

1. **The margins at 5%, 10% and 25% on the full sample are +0.5, +0.2 and +0.2pp**, on a coordinate
   whose values run to 10pp. That is survival by the letter of a rule fixed in advance, and it is not
   a robust ordering in any other sense. The rule stands as preregistered; the margin is reported
   beside it.
2. **V1 is deliberately asymmetric and its asymmetry grows with tenor.** It takes the worst of 52
   alignments against the best of 4, so the long tenor is given 52 chances to fail and the short one
   4 chances to succeed. This is the conservative direction, it was chosen before the run, and it
   means a *failure* at some `q` is weaker evidence than a *survival* at that `q`.

## 10.3 The `Psi` column, which is what the CDaR curve was built to produce

Distinct naked episodes contributing observations to the worst `q%` of the hedged book's drawdown
process, phase 0. This is the effective `n` of the coordinate, measured rather than argued.

| curve | 1% | 5% | 10% | 25% | 50% | 100% |
|---|---|---|---|---|---|---|
| naked, 1993– | 2 | 2 | 3 | 7 | 9+ | 9+ |
| 52w marked, 1993– | **1** | **2** | **2** | 5 | 9+ | 9+ |
| naked, 2003– | **1** | 2 | 3 | 6+ | 6+ | 6+ |
| 52w marked, 2003– | **1** | **1** | 2 | 6+ | 6+ | 6+ |

> **Line these up against §10.2 and the result reads itself: the ordering survives exactly where the
> coordinate rests on one or two episodes, and fails exactly where the coordinate is well sampled.**
> On the 2003– sample the two surviving points (`q` = 1%, 5%) are the two points where the marked
> tail collapses onto a **single episode**. At `q >= 50%`, where all nine episodes and the time
> between them contribute, the separation is negative in every sample and both accountings.

This is the sample-size problem converted into an output, which is the entire reason `CDaR_q` was
specified as a curve rather than a point. It did not need to be argued from the outside; the
coordinate reported it about itself.

## 10.4 V2 and V3 — the episode-matched coordinate

Episodes defined once on the **naked** book; both books measured inside the same windows, each from
its own peak within the window. Counts over (episode × 52w-phase × 4w-phase) triples.

| sample | thr | acct | **V2** `52w >= 4w` | verdict | **V3** `52w reduces depth at all` |
|---|---|---|---|---|---|
| 1993– | 10% | marked | 1758/1872 = **93.9%** | **SURVIVES** | 450/468 = **96.2%** |
| 1993– | 10% | cash | 1139/1872 = **60.8%** | MARGINAL | 77/468 = **16.5%** |
| 1993– | 20% | marked | 771/832 = **92.7%** | **SURVIVES** | 206/208 = **99.0%** |
| 1993– | 20% | cash | 460/832 = **55.3%** | MARGINAL | 58/208 = **27.9%** |
| 2003– | 10% | marked | 1146/1248 = **91.8%** | **SURVIVES** | 299/312 = **95.8%** |
| 2003– | 10% | cash | 670/1248 = **53.7%** | MARGINAL | 76/312 = **24.4%** |
| 2003– | 20% | marked | 563/624 = **90.2%** | **SURVIVES** | 154/156 = **98.7%** |
| 2003– | 20% | cash | 299/624 = **47.9%** | **KILLED** | 31/156 = **19.9%** |

**H2's excursion clause survives in marks and does not in cash.** Marked sign-consistency is 90–94%
across both thresholds and both samples — genuinely consistent, and it is the strongest positive
result the intervention side of this repository has produced.

**V3 is the number that stops V2 from being read as good news.** In cash the 52-week programme
reduces episode depth in **16.5% to 27.9%** of pairs — which is to say **it deepens the episode
between roughly three-quarters and five-sixths of the time.** V2's cash figure of 53–61% is
therefore an ordering *between two harms*: 52w is less bad than 4w about as often as a coin, and both
are usually negative.

**Why V1 and V2 diverge, since both are phase-aware.** V1 is a worst-case test (min over one grid
against max over another); V2 is a count over all pairs. A coordinate can be consistently ordered in
92% of pairs and still have its worst alignment fall below the other tenor's best. Both were
preregistered, both are reported, and neither is a correction of the other.

## 10.5 The episodes themselves, phase 0, threshold 10%, full sample

Depth reduction in pp, each book measured inside the naked book's window:

| episode | naked depth | 4w marked | 4w cash | 52w marked | **52w cash** |
|---|---|---|---|---|---|
| 1998-07 → 1998-11 | 17.6% | −1.0 | −1.0 | +5.0 | **−0.0** |
| 1999-07 → 1999-11 | 11.7% | +0.4 | −0.9 | +2.2 | **−0.0** |
| 2000-03 → 2006-11 | 45.7% | −8.3 | −8.5 | +7.9 | **−2.0** |
| 2007-10 → 2012-08 | 54.6% | +5.1 | +1.1 | +19.9 | **+3.0** |
| 2015-07 → 2016-05 | 11.2% | −2.1 | −2.4 | −0.7 | **−6.1** |
| 2018-09 → 2019-04 | 17.1% | +0.6 | −0.7 | +2.1 | **+0.0** |
| 2020-02 → 2020-07 | 31.8% | +6.6 | −1.0 | +24.9 | **−0.0** |
| 2021-12 → 2023-12 | 23.9% | −3.2 | −3.7 | +11.2 | **−2.6** |
| 2025-02 → 2025-06 | 16.9% | +2.8 | −0.3 | +11.3 | **−0.0** |

**In marks the 52-week column is positive in 8 of 9 episodes** — that is V2's consistency, visible.
**In cash the same column is one episode.** 2008 gives +3.0pp; 2020, the second-deepest event in the
sample and the one a put programme is imagined for, gives **−0.0pp**; three episodes are negative.
The 2020 row is the clearest single statement of E0's finding in episode form: **+24.9pp of marked
protection through February–March 2020 converted to nothing in cash**, because the option's value was
never realized before the market recovered past it.

## 10.6 Predictions, scored

- **"Marked survives at small `q`, at risk at large `q`" — CONFIRMED**, and more sharply than
  predicted: it fails from `q >= 50%` (1993–) and from `q >= 10%` (2003–).
- **"Cash fails at every `q`" — CONFIRMED**, both samples, all six points, with no margin close to
  zero.
- **"Episode sign-consistency `>= 2/3` marked, `< 1/2` cash" — SPLIT.** Marked confirmed (90–94%).
  Cash came in at 47.9–60.8%: below the SURVIVES line everywhere, but only *at* the KILLED line at
  one of four cells. **Recorded as MARGINAL where the rule says marginal.** The prediction was
  directionally right and too strong.
- **The genuinely uncertain case named in §2 — whether the marked ordering holds at `q` = 50% and
  100% — resolved NO in both samples.** That is where the run carried its information, and it is the
  half of the curve that is well sampled.

## 10.7 What E2 establishes, and what it does not

**Establishes.**

- **The estimand is repaired.** Both coordinates compare like with like: `CDaR_q` integrates one
  path's own process, and episode-matched depths put both books inside the same windows. Neither can
  silently change which event it describes, which `max(D)` did in 51 of 52 alignments.
- **No tenor ordering survives in cash anywhere on the drawdown path**, at any `q`, in either sample,
  at either episode threshold — and in cash the long-tenor programme *deepens* episodes in 72–84% of
  pairs.
- **In marks, the ordering survives per-episode (90–94%)** and, on the CDaR curve, only where `Psi`
  shows the coordinate resting on one or two episodes.
- **Therefore the structural ordering preserved in [[closed-research/intervention/CHARTER-INTERVENTION|CHARTER-INTERVENTION]] §9.1 needs a qualifier it did not
  have.** It is an episode-level, marked-accounting regularity. It is not a property of the drawdown
  path as a whole, and where the path is well sampled it is absent.

**Does not establish.**

- **No magnitude, and no population claim.** One path. Episodes are not exchangeable — 1998, 2008,
  2020 and 2022 differ in structure, monetary regime and options-market depth — and phases are not
  independent. The V2/V3 fractions are counts of a deterministic sensitivity, exactly as declared in
  §7: **no standard error, no test statistic, and none may be derived from them.** Effective n on the
  benefit side is still 1.
- **Nothing about whether the intervention is worth its cost.** E2 measured depth only. Cost, outlay
  matching and monetisation are E6 and E7 and are untouched.
- **Nothing about instruments other than the rolled outright put**, and nothing about timing: no rule
  here conditions on anything.
- **Nothing that promotes `q = 1%` to a preferred coordinate.** The surviving points are the
  *least* identified ones on the curve; that is the finding, not a selection criterion.

## 10.8 Consequences booked

1. [[closed-research/intervention/CHARTER-INTERVENTION|CHARTER-INTERVENTION]] §9.1 — the preserved structural ordering gains its qualifier: episode-level, marked
   only, absent where the coordinate is well sampled.
2. [[closed-research/intervention/CHARTER-INTERVENTION|CHARTER-INTERVENTION]] §4 — H2 resolved on both clauses: **excursion clause SURVIVES in marks, KILLED/MARGINAL
   in cash; phase clause already killed by E1.**
3. [[PROBLEM-MAP]] — E14 recorded; §1.1's rider extended to say the ordering does not hold on the
   well-sampled part of the path.
4. **No experiment is triggered.** E3 is not started. The queue decision is recorded as open.

## Related

- [[closed-research/intervention/CHARTER-INTERVENTION|CHARTER-INTERVENTION]] §4 H2 — the excursion clause · §9 E2 — the queue entry · §9.1 — the claim's split status
- [[closed-research/intervention/STUB-E1-ROLL-PHASE]] — the estimand problem this repairs · [[closed-research/intervention/STUB-E0-M3-DECOMPOSITION]] — the accounting
- [[docs/MATH-REFERENCE]] §4.1 — the CDaR convention, confirmed against the source
- [[docs/RESEARCH-PROTOCOL]] §0 — the gate · [[POINT-IN-TIME-DISCIPLINE]] — the leak register
