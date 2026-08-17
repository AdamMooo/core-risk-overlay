# Research Protocol

Last updated: 2026-08-17. **Binding on everything in the active program.**

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

## 0. The gate — seven fields, committed before any code

**No experiment runs until its stub is committed.** If any field cannot be filled honestly, the
experiment does not run. The stub is committed *before* the commit carrying its results. The
canonical field list is [[CHARTER]] §8; what follows is what each field is for.

1. **Claim tuple — `(frequency, horizon, functional, sample)`.** A test of a one-step *marginal*
   cannot support a claim about a *path* functional, at any sample size. Drawdown depth is a path
   functional. The tuple appears in the heading of every section reporting the result, so no reader
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

5. **What would surprise me, and what decision it changes.** If no outcome moves a decision, the run
   is decoration and does not run.

6. **Boundary.** Which of the six does this move — identification, mechanism validity, robustness,
   realizability, economic comparability, or the admissible frontier? **`BOUNDARY` empty ⇒ do not run.
   It goes in [[PARKED]].** This field is what makes the scope discipline mechanical rather than
   aspirational.

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

These govern *what to work on and why*, where §0 governs *whether a given run may happen*. P1-P7 and
P10 are carried from the closed protocol essentially unchanged — they were never specific to
forecasting. P8 and P9 are restated for a program about contracts rather than estimators.

**P1 — The governing question, asked at every stage.**

> **What does this intervention change that the cheaper alternative does not — and is that change
> identified?**

Answerable and convincing → build on it. Not answerable → stop.

**P2 — Identifiability before implementation.** Ask *what mathematical object actually differs* before
asking what to run. Two objects producing the same functional on the available sample do not become
distinguishable by collecting more of the same sample. **The response to an uninformative experiment
is to redesign it, not to enlarge it.**

**P3 — Four questions, never collapsed.** (A) What does the intervention change? (B) Is that change
identified in magnitude? (C) Is it realizable in cash rather than in marks? (D) Is it worth it?
**A → D directly is forbidden.** Current state: A partially measured, B the live question, C untouched
until E6, D is the decision layer's and not research's at all.

**P4 — Do not optimise toward usefulness.** "This intervention changes nothing" and "it changes
something" are both successful outcomes. **This principle was enforced rigorously on individual runs
in the closed program and never once applied to the program itself** — the board's stated purpose
became recovering a question the evidence had closed. Apply it at both scales.

**P5 — Mechanism first, then test.** `mechanism → observable consequence → test → falsification
criterion`. Never start from "what backtest should we run"; start from *what would have to be true*,
then build the **smallest** experiment separating the possibilities. E0 is the model of this: same
simulation, same parameters, same path, one accounting difference.

**P6 — Literature is part of the model, not a citation duty.** It supplies mechanisms, prior
measurements, and alternative explanations requiring control. And do not collapse distinct objects into
one name: **a mark is not a cash flow, an ordering is not a magnitude, and a bound is not an estimate.**

**P7 — The reason for the code is the hypothesis, not the code.** Identical lines carry different
claims and need different evidence. **The reason is written next to the line, always.** Be most
suspicious when a result is attractive: ask whether it measures what it appears to. The single worst
defect found in this repo was a docstring asserting that an expiry payoff *was* a monetisation at the
volatility peak. The code was right; the sentence beside it was wrong, and the sentence is what people
read.

**P8 — Ask whether a difference is about the contract or about an assumption.** The closed program's
version asked whether a comparison was about information sets or estimator quality. The analogue here:
if two structures differ because of what the *contract* specifies (M1, strike anchoring), the result is
robust and needs no pricing. If they differ because of what we *assumed about prices* (M2), the result
is only as good as the assumption — and `skewed_vol`'s shape is an assumption that favours the
conclusion. Say which one every number is.

**P9 — Complexity does not count as evidence.** Each rung earns its place by identified difference:

```
no intervention -> fixed structure -> fixed structure + monetisation rule -> conditioned structure
```

The closed program established that the last rung is worth at most ~3pp/yr at the tested tenors. Do not
climb the ladder because a rung exists.

**P10 — Enforce these against whoever proposes the violation, including the person directing the
work.** Push back, in writing, on: quoting a magnitude from an unidentified population; ranking on max
drawdown; adding a coordinate to `Phi` that belongs in `Psi`; selecting a phase, threshold or `alpha`
after seeing the result; treating a mark as realizable; comparing interventions at unmatched outlay;
adding an experiment outside [[CHARTER]] §9; and reopening anything in [[PARKED]]'s permanently-closed
list without meeting its stated condition.

## 2. Reporting

- Every reported number carries its **claim tuple** and its **effective n**, per coordinate.
- Every row of `Phi` is accompanied by its row of `Psi`. A `Phi` without a `Psi` is not reportable.
- **Overlapping windows are permitted for description and never for inference.** Inflating n by
  overlap is the most available way to fake a result here.
- A result failing its power or identification requirement is **INCONCLUSIVE, never NULL**.
- Preregistered third outcome, accepted in advance so the pressure to manufacture n has no purchase:
  **"indeterminate — cannot be settled on the available history"** is a legitimate, reportable finding.

## Amendments

Every change to this document after a result exists is logged here with date and reason.

**2026-08-17 — program transition. §0 extended from five fields to seven; §1 P8/P9 restated; §2
added.** Not selected on a result: no experiment in the active queue has been run. The transition
itself, its evidence and its reasoning are recorded as a first-class amendment in
[[docs/PROBLEM-MAP]], not here — this file records changes to *process*, that one records changes to
*program*.

## Related

- [[CHARTER]] — the active program · [[PARKED]] — deliberately excluded
- [[docs/POINT-IN-TIME-DISCIPLINE]] — leak register · [[docs/MATH-REFERENCE]] — path functionals
- [[closed-research/docs/PROTOCOL-PREDICTION-PROGRAM]] — the closed program's protocol, intact
