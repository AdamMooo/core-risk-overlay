# §0 Stub — E2, the drawdown path: CDaR curve and per-excursion depths

Committed 2026-08-18, **before any code**, under [[RESEARCH-PROTOCOL]] §0 and [[CHARTER]] §8.
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
[[MATH-REFERENCE]] §4.1. It found a convention collision (**their `alpha` is a confidence level and
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
required and what E0 failed to do. Its three consequences are recorded in [[MATH-REFERENCE]] §4.1 and
are already applied in this stub. **Its most useful sentence for us is its own scope caveat:** the
authors define CDaR as a risk function *on a sample-path*, explicitly leaving the definition on a
*set* of sample-paths to future research. The source therefore agrees with this repository's
identification stance — computing CDaR carefully does not turn one path into a population.

No paper settles the episode-matching question, which is a defect of this repository's own estimand
rather than a question about markets. Israelov (2017) measures drawdowns over rolling fixed-length
windows, which sidesteps episode identity instead of resolving it, and its remedy remains
inadmissible under [[CHARTER]] §2 C2.

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
  claim would be withdrawn in full rather than preserved as structure ([[CHARTER]] §9.1).
- **Sign consistency near 1/2** would mean the tenor choice is a coin flip per episode, which no
  amount of averaging repairs.

**Decision changed:** whether [[CHARTER]] §9.1's preserved structural ordering keeps its "at every
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

**V2 — episode sign-consistency ([[CHARTER]] H2's excursion clause).** Over all (episode × phase)
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

## Related

- [[CHARTER]] §4 H2 — the excursion clause · §9 E2 — the queue entry · §9.1 — the claim's split status
- [[STUB-E1-ROLL-PHASE]] — the estimand problem this repairs · [[STUB-E0-M3-DECOMPOSITION]] — the accounting
- [[MATH-REFERENCE]] §4.1 — the CDaR convention, confirmed against the source
- [[RESEARCH-PROTOCOL]] §0 — the gate · [[POINT-IN-TIME-DISCIPLINE]] — the leak register
