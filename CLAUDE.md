# Core-Risk-Overlay — Operating Manual

Last updated: 2026-10-25. **Read this before reading any code.** Companion to [[README]] (what is
established), [[docs/RESEARCH-PROTOCOL]] (what has to be true before a run) and
[[docs/POINT-IN-TIME-DISCIPLINE]] (time basis).

**Policy change, 2026-10-25.** Prior versions of this file declared the repository had no active
research programme and that further work required a new charter arguing from scratch. That stance is
rescinded. Three closed programmes exist; their lessons are **inputs** to continued work, not an
endpoint. The repository is active. The methodology gates below (literature-first, mechanism-first,
cheap-falsification-first, no leakage, honest identifiability) still bind every new run.

## 1. What this repository is

A **research laboratory** for questions about systematic market and portfolio risk, and more broadly
about the statistical structure of market dynamics. It is not a product and not a model awaiting
cosmetic improvement — but it *is* an ongoing programme that learns from its closures.

Seven things at once:

| purpose | what it means here |
|---|---|
| research laboratory | a question is specified, gated, run, and either closed or extended |
| literature-reproduction environment | published results rebuilt on public data before being believed |
| measurement laboratory | quantities constructed and validated *as measurements* |
| falsification engine | its principal product is closures that teach the next question |
| methodological archive | three closed programmes, preserved and reproducible |
| risk-intelligence environment | description of risk, explicitly not alpha |
| continuing enquiry | closures are inputs to the next question, not the end of the queue |

**There is an active programme of enquiry.** The three closures (`return-states`, `intervention`,
`reproduction-sjm2024`) are **evidence** — about what the data can and cannot support, what estimators
are identified at this sample size, which targets are mis-specified. A fourth question is admissible,
and it may legitimately reuse closed methods *when the question asks for them* — not because the code
happens to be here.

**The repository name is historical** and does not restrict the scope of admissible questions.

## 2. The order of work

```
real-world risk question -> literature -> mechanism -> observable data
    -> mathematical formulation -> empirical test -> falsification
    -> extension -> implementation
```

**Code is the last step, not the first.** A sophisticated model applied to a poorly motivated target
is still poor research. The repository comes after the research question.

## 3. Repository gravity — the failure mode to watch

**Repository gravity** is treating what is already here — code, models, features, labels, datasets,
tests, abstractions — as the *definition* of the research problem rather than as prior evidence
about it. The distinction matters because the lessons of the three closures are legitimately
load-bearing on what comes next; the error is letting the shape of `src/` substitute for a question.

Still wrong:

- "There is state-model machinery here, so the task is to improve it" (improvement is not a question).
- "These are the existing features, so the question must concern these features" (features follow
  mechanism, not the other way round).
- "We have K-means / an HMM / a jump model, so which one should we use?" (the question picks the
  model; §6.13 still binds).

Legitimate, and newly explicit:

- "Programme Z closed because estimator X was unidentified at this T; a reformulated question
  asking a different quantity of the same data is admissible."
- "The reproduction established that published result P does not survive on public data at this
  window; the next question is what weaker claim *does* survive."
- "A method that failed on target A is not disqualified from target B — but it must be re-argued
  for B, not inherited."

The correct containment is still:

```
research universe  >  literature  >  candidate mechanisms
                   >  publicly measurable phenomena  >  repository experiments
```

**Existing code is evidence of what has been attempted and what it taught us.** When a new question
opens, the first move is still *outward* — to the literature and to the closed programmes' lessons —
before any `src/` edit.

**Cross-repository gravity is the same defect, pointed sideways.** This repository stands alone. It has
no upstream, no downstream, no sibling it must reconcile with, and no governing document outside its own
tree (§7). It shares the `systematic-investing-research/` directory with three governed repositories and
is **not one of them**. `regime-detection` is not a predecessor, and this repository is neither its
extension nor its successor. Nothing here imports from another repository and nothing there imports from
here.

It sounds like this, and every one of these is wrong too:

- "This continues what `regime-detection` was doing."
- "Another repository has that dataset, so that is the question to ask."
- "The systematic-investing charter governs this, so the question has to fit the stack."
- "This repository needs to be reconciled with / migrated into / justified against that one."

A dataset held in another repository is a fact about the world, not a research question. If a question
argued *here* turns out to need data that exists elsewhere, that is an acquisition decision taken after
the question stands on its own — never a reason to choose the question.

## 4. Risk intelligence is not alpha

Three distinct problems. This repository works on the second and third, and is not required to solve
the first:

| | object | question |
|---|---|---|
| alpha prediction | `X_t -> E[R_{t+h}]` | what should I buy? |
| **risk prediction** | `X_t -> P(adverse outcome given X_t)` | what risk is the portfolio carrying? |
| **risk intervention** | risk information -> risk posture | what should the posture be? |

A valid result is *"current conditions imply materially elevated exposure to this form of systematic
risk."* It does not have to name an asset, and profitability is not the definition of success — see
[[README]] §6 for what does count. **Never claim to know what will outperform unless the evidence
supports that specific claim.**

## 5. Public data is a constraint, stated honestly

Institutional researchers may hold proprietary data, positioning, order flow, execution records,
alternative datasets, deeper option histories and better infrastructure. We do not, and acquiring them
is not this project.

So the question is usually: **what mathematically defensible risk information can be extracted from
publicly accessible data?** A phenomenon that is theoretically meaningful, statistically robust,
reproducible and useful for risk monitoring — but not directly tradable — is an acceptable result. Do
not pretend public data can answer every question, and do not use the constraint as an excuse for a
weak test.

## 6. Standing requirements

1. **Look outward before inward.** New question, literature first, repository second.
2. **Search the literature before selecting a model.** [[docs/RESEARCH-PROTOCOL]] §0 field 3 makes
   this a gate, not a courtesy.
3. **Distinguish established fact, established regularity, theoretical possibility, unresolved
   question, and speculation.** Say which one every claim is.
4. **Identify the mechanism before choosing features.**
5. **Prefer independent reproduction** of a useful published finding over citing it.
6. **Use public data honestly** and state its limits.
7. **Treat existing code as prior experimental history**, never as the boundary of possible research.
8. **Do not force an existing model onto a new question.**
9. **Find the cheapest falsification first.** Before a model, a pipeline, a feature family, a state
   taxonomy or a backtest, ask: *what is the cheapest experiment that would make this whole programme
   unnecessary?* Run that one.
10. **Preserve failed approaches as methodological knowledge.** Closures are outputs.
11. **Separate risk measurement from return prediction.**
12. **Separate risk intelligence from trading and alpha.**
13. **A model existing here is not a reason to use it again** — and a programme having failed with a
    model is not a reason to exclude it. **The question chooses the model.**
14. **A direction having been pursued does not make it the project's future, but neither does it
    disqualify it.** Closures teach; they do not forbid. Reuse requires a fresh argument from the
    question, not inheritance.
15. **Stop when the evidence closes a branch.** "Not identified" and "indeterminate on the available
    history" are legitimate, reportable results.
16. **This repository stands alone.** Never relate a question, a model, a result or a justification to
    another repository — §3, cross-repository gravity.

## 7. Where authority lives

| document | status |
|---|---|
| this file | **authoritative** — repository purpose and agent behaviour |
| [[README]] | **authoritative** — what is established, what is closed, what counts as a result |
| [[docs/RESEARCH-PROTOCOL]] | **authoritative** — the gate and the standing principles |
| [[docs/POINT-IN-TIME-DISCIPLINE]] | **authoritative** — time basis and leak register |
| [[PARKED]] | **authoritative** — what is excluded, and the condition that would unpark it |
| [[docs/MATH-REFERENCE]] | **authoritative** — live conventions for the drawdown process and the CDaR family; cited from source code, binds every published CDaR number |
| [[docs/MATH-AUDIT-JUMPMODEL]] | **evidence** — the jump model's mathematical audit: what the estimator is and what lambda means |
| [[docs/PROBLEM-MAP]] | **frozen evidence** — the closed programmes' findings and lessons |
| [[CHARTER]] | **historical** — the third programme's charter, terminated at §11 |
| [[core-risk-overlay]] | **historical** — chronological status log, with a navigation map of every document |
| `closed-research/` | **historical, reproducible** — three programmes, self-contained with their preregistrations and check suites; [[closed-research/HUB-RECORD]] is the hub's pre-closure working record |

Change the authoritative documents first, and never edit [[CHARTER]] or `closed-research/` to make the
past look tidier than it was.

**No document outside this repository has authority over it.** The charter in
`regime-detection/governance/` governs three other repositories; this one is not in that stack, is not
audited against it, and owes it no reconciliation. If a rule is meant to bind work here, it is written
here.

## 8. Run commands

```powershell
.venv\Scripts\python.exe checks.py                                             # 37 active checks
.venv\Scripts\python.exe closed-research\checks.py                             # 81 frozen
.venv\Scripts\python.exe closed-research\intervention\checks.py                # 17 frozen
.venv\Scripts\python.exe closed-research\return-states\checks.py               # 180 frozen
.venv\Scripts\python.exe closed-research\reproduction-sjm2024\checks.py        # 35 frozen
.venv\Scripts\python.exe closed-research\reproduction-sjm2024\d4_crosscheck.py # 28 vs authors' jumpmodels pkg
```

`data/` is gitignored; `data/MANIFEST.md` is tracked and is what makes reproduction checkable rather
than asserted.

## 9. What a future agent's job is

Not this:

> "My job is to improve the existing regime detector."

This:

> **"My job is to investigate meaningful, testable questions about systematic market and portfolio
> risk — and more broadly the statistical structure of market dynamics — using the repository as a
> laboratory, the three closed programmes as evidence of what the data will and will not support,
> and the broader quantitative-finance literature as the starting point."**

The project does not need to find something. It needs to determine what is true. If the answer is
already known, reproduce it. If it is false, close it. If a closure teaches a sharper question,
pursue it. If there is a real unresolved phenomenon, establish it carefully — and only then ask
whether it is useful.

**Continuing from closures is encouraged and governed.** A new question may reuse a closed
programme's data, estimator, or framing — provided the reuse is argued from the new question, the
old failure mode is explicitly addressed (identifiability, power, leakage, target mis-specification,
whichever applied), and the gate in [[docs/RESEARCH-PROTOCOL]] is passed before any code is written.

## Related

- [[README]] · [[docs/RESEARCH-PROTOCOL]] · [[docs/POINT-IN-TIME-DISCIPLINE]] · [[PARKED]]
- [[docs/PROBLEM-MAP]] — frozen evidence · [[core-risk-overlay]] — chronological log
