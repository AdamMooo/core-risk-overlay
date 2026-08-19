# Research Protocol

Last updated: 2026-08-18. **Binding on everything in the active program.**

Companion to [[CHARTER]] (the question, the space, the queue) and
[[docs/POINT-IN-TIME-DISCIPLINE]] (time basis and the leak register).

This document is **process**: what has to be true before a run may happen, and what may be said about
its result afterwards. It says nothing about which experiment is next — that is [[CHARTER]] §9, and
there is exactly one such list.

Its §0 and §1 are carried forward, with adaptation, from the closed program's protocol. That program's
substantive sections did not transfer; they are preserved at
[[closed-research/docs/PROTOCOL-PREDICTION-PROGRAM]]. **The process survived the program that
produced it, and it survived because it worked** — every hard negative in this repo's history was
produced under these rules, and the two experiments that wasted effort were the two that ran before
the rules did.

---

## 0. The gate — nine fields, committed before any code

**No experiment runs until its stub is committed.** If any field cannot be filled honestly, the
experiment does not run. The stub is committed *before* the commit carrying its results. The
canonical field list is [[CHARTER]] §5; what follows is what the load-bearing fields are for. The
seven below map onto the nine there — the charter splits *what it establishes* and *what it may
motivate next* into their own fields, because the second is the anti-sprawl clause and it was
previously implicit.

1. **Claim tuple — `(frequency, horizon, functional, sample, null)`.** A test of a one-step
   *marginal* cannot support a claim about a *path* functional, at any sample size. Drawdown depth is
   a path functional. **The null joined the tuple on 2026-08-18**: a distributional difference is only
   a finding relative to what it is a difference *from* ([[CHARTER]] §2). The tuple appears in the heading of every section reporting the result, so no reader
   inherits a wider claim than was measured.

2. **Predicted outcome, with its reason, before any code.** If the prediction is confident and
   derivable from theory or a citable paper, **the run carries no information — do not run it.**
   Record the prediction and its source instead.

3. **Literature check.** Name the paper that already settles this, or state in writing that none does.
   A finding rediscovered empirically that was already in a cited paper is a process failure and gets
   logged as one. This has happened here once, and the paper was sitting `[UNREAD]` as row 2 of the
   list at the time.

4. **Mechanism for a difference.** State the structural difference between the two objects, **the
   horizon at which it becomes observable, and the functional on which it becomes observable.**
   Invisible at the proposed horizon *or* in the proposed functional → the comparison is void and does
   not run. Both clauses earned their place by catching a different mistake.

5. **What would surprise me, and what it changes about what we claim to know.** If no outcome
   changes the state of knowledge, the run is decoration and does not run. **Restated 2026-08-18** —
   it previously read "what decision it changes", which presumed a decision layer the active program
   does not have and must not acquire by wording.

6. **Question.** Which of the four does this move — **existence**, **characterisation**,
   **transition**, or **identification** ([[CHARTER]] §1 A/B/C/D)? **Empty ⇒ do not run. It goes in
   [[PARKED]].** This field is what makes the scope discipline mechanical rather than aspirational,
   and **its enumeration was replaced on 2026-08-18**: it previously read *identification / mechanism
   validity / robustness / realizability / economic comparability / frontier*, three of which are
   intervention concepts. Left in place it would have licensed exactly the work the transition
   closed — through the mechanism built to prevent it.

7. **Identification.** What population the claim addresses, what is identified in magnitude, and what
   is not. **"Not identified" is a permitted answer and is written before the run, not after.**

### 0.1 Three firewalls, absolute

- **A verdict may not exceed its claim tuple.** Absent a horizon and functional at which two objects
  differ, the only sayable sentence is "indistinguishable at horizon h on functional f, as predicted" —
  never "does not beat", never any word implying a fair chance to differ was given.

- **Statistical loss never licenses an economic claim, and no economic claim rests on a loss
  function.** No sentence may contain both a loss-function number and a cost-benefit judgement.

- **No magnitude without identification.** **No active hypothesis may assert a numerical effect
  magnitude as though it were identified when the underlying population is not identified.** Orderings,
  signs and falsifications only. This is the rule that would have stopped a single-episode statistic
  from reordering the whole project, and it is the most important line in this document.

## 1. Standing principles

These govern *what to work on and why*, where §0 governs *whether a given run may happen*. P2, P4-P7
are carried across both closed programs essentially unchanged — they were never specific to
forecasting or to contracts. P1, P3, P8, P9 and P10 are restated for a program about distributions.

**P1 — The governing question, asked at every stage.**

> **What does this state structure make different about the return distribution that the null
> does not — and is that difference identified?**

Answerable and convincing → build on it. Not answerable → stop.

**P2 — Identifiability before implementation.** Ask *what mathematical object actually differs* before
asking what to run. Two objects producing the same functional on the available sample do not become
distinguishable by collecting more of the same sample. **The response to an uninformative experiment
is to redesign it, not to enlarge it.**

**P3 — Four questions, never collapsed.** (A) What differs across states? (B) Is the difference
identified, and on what population? (C) Is it persistent, and does it survive out of sample and
across markets? (D) Is the state observable at time `t` from `I_t`? **A → D directly is forbidden**,
and so is any fifth question about what to do with the answer — that is a different charter
([[CHARTER]] §7). Current state: A is the live question, B–D untouched.

**P4 — Do not optimise toward usefulness.** "There is no state structure here" and "there is" are
both successful outcomes. **This principle was enforced rigorously on individual runs
in the closed program and never once applied to the program itself** — the board's stated purpose
became recovering a question the evidence had closed. Apply it at both scales.

**P5 — Mechanism first, then test.** `mechanism → observable consequence → test → falsification
criterion`. Never start from "what backtest should we run"; start from *what would have to be true*,
then build the **smallest** experiment separating the possibilities. E0 remains the model of this
across both closed programs: same simulation, same parameters, same path, one accounting difference —
and it removed 82% of a headline number.

**P6 — Literature is part of the model, not a citation duty.** It supplies mechanisms, prior
measurements, and alternative explanations requiring control. And do not collapse distinct objects into
one name: **a mark is not a cash flow, an ordering is not a magnitude, and a bound is not an estimate.**

**P7 — The reason for the code is the hypothesis, not the code.** Identical lines carry different
claims and need different evidence. **The reason is written next to the line, always.** Be most
suspicious when a result is attractive: ask whether it measures what it appears to. The single worst
defect found in this repo was a docstring asserting that an expiry payoff *was* a monetisation at the
volatility peak. The code was right; the sentence beside it was wrong, and the sentence is what people
read.

**P8 — Ask whether a difference is about the data or about the representation.** Two earlier
versions of this principle asked whether a comparison was about information sets or estimator
quality, then whether it was about the contract or the pricing assumption. The analogue here: if two
states differ because the *returns* in them differ, the result is about the world. If they differ
because of what the *model class* imposes — a mixture is Gaussian in the far tail for any `k`, a
Markov chain's squared-return ACF decays geometrically for any `k` — the result is about the
representation and would appear on data that had no states at all. **Say which one every number is**,
and prefer the comparison that could come out the other way.

**P9 — Complexity does not count as evidence.** Each rung earns its place by identified
difference, and the ladder is now one of representations rather than of interventions:

```
one unconditional distribution  ->  a continuous conditional-scale process
                                ->  a discrete persistent state structure
                                ->  states with more than two values, or with
                                    time-varying transitions
```

**The second rung is the null ([[CHARTER]] D1), not a rung we are climbing.** Do not climb because a
rung exists, and do not climb to escape a negative result — that is [[CHARTER]] §6 S1, which ends the
program rather than motivating the next model.

**P10 — Enforce these against whoever proposes the violation, including the person directing the
work.** Push back, in writing, on: quoting a magnitude from an unidentified population; reporting a
statistic whose effective n was never stated; selecting a threshold, window, horizon or sample after
seeing the result; changing the null or the frequency once a result exists; calling a fitted label a
regime without showing the return distribution differs; using portfolio outcomes to define, validate
or tune a state; adding an experiment outside [[CHARTER]] §9; and reopening anything in [[PARKED]]'s
permanently-closed list without meeting its stated condition.

## 2. Reporting

- Every reported number carries its **claim tuple** and its **effective n**, per coordinate.
- **Every estimate is accompanied by how well it is known.** The closed program's form of this was
  `Phi` (how good is this) beside `Psi` (how well do we know it), and the separation is retained even
  though those objects are gone: a distributional difference is reported beside its effective n, its
  sensitivity to the sample, and what it rests on. An estimate without that row is not reportable.
- **Overlapping windows are permitted for description and never for inference.** Inflating n by
  overlap is the most available way to fake a result here.
- A result failing its power or identification requirement is **INCONCLUSIVE, never NULL**.
- Preregistered third outcome, accepted in advance so the pressure to manufacture n has no purchase:
  **"indeterminate — cannot be settled on the available history"** is a legitimate, reportable finding.

## Amendments

Every change to this document after a result exists is logged here with date and reason.

**2026-08-18 — program transition to return states. §0 field 6 re-enumerated to the charter's
A/B/C/D; the null added to the claim tuple; field 5 restated off "decision"; P1, P3, P8, P9 and P10
restated for a program about distributions rather than contracts; §2's `Phi`/`Psi` clause
generalised.** Not selected on a result: no experiment in the return-state queue has been run. **The
field-6 change is the load-bearing one** — its previous enumeration named three intervention
boundaries, so the mechanism built to prevent sprawl would have licensed the work the transition
closed. The transition's reasoning is recorded in [[CHARTER]] and
[[closed-research/intervention/README]], not here.

**2026-08-17 — program transition. §0 extended from five fields to seven; §1 P8/P9 restated; §2
added.** Not selected on a result: no experiment in the active queue has been run. The transition
itself, its evidence and its reasoning are recorded as a first-class amendment in
[[docs/PROBLEM-MAP]], not here — this file records changes to *process*, that one records changes to
*program*.

## Related

- [[CHARTER]] — the active program · [[PARKED]] — deliberately excluded
- [[docs/POINT-IN-TIME-DISCIPLINE]] — leak register · [[docs/MATH-REFERENCE]] — path functionals
- [[closed-research/docs/PROTOCOL-PREDICTION-PROGRAM]] — the closed program's protocol, intact
