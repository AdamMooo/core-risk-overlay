# Core-Risk-Overlay — Operating Manual

Last updated: 2026-08-27. **Read this before reading any code.** Companion to [[README]] (what is
established), [[docs/RESEARCH-PROTOCOL]] (what has to be true before a run) and
[[docs/POINT-IN-TIME-DISCIPLINE]] (time basis).

## 1. What this repository is

A **research laboratory** for questions about systematic market and portfolio risk. It is not a
product, not a detector, and not a model awaiting improvement.

Six things at once, and none of them is "the regime system":

| purpose | what it means here |
|---|---|
| research laboratory | a question is specified, gated, run, and closed |
| literature-reproduction environment | published results rebuilt on public data before being believed |
| measurement laboratory | quantities constructed and validated *as measurements* |
| falsification engine | its principal product is closures |
| methodological archive | three closed programmes, preserved and reproducible |
| risk-intelligence environment | description of risk, explicitly not alpha |

**There is no active research programme.** Three have run and all three are closed. That is a fact
about the queue, not about the repository's purpose. A fourth requires a new charter, argued from the
question — never from the code that happens to be here.

**The repository name is historical.** It names a programme that no longer runs, and it does not
describe the scope of admissible questions.

## 2. The order of work

```
real-world risk question -> literature -> mechanism -> observable data
    -> mathematical formulation -> empirical test -> falsification
    -> extension -> implementation
```

**Code is the last step, not the first.** A sophisticated model applied to a poorly motivated target
is still poor research. The repository comes after the research question.

## 3. Repository gravity — the failure mode this file exists to prevent

**Repository gravity** is treating what is already here — code, models, features, labels, datasets,
tests, abstractions — as the definition of the research problem.

It sounds like this, and every one of these is wrong:

- "There is state-model machinery here, so the task is to improve it."
- "These are the existing features, so the question must concern these features."
- "This direction was pursued before, so it defines what comes next."
- "We have K-means / an HMM / a jump model, so which one should we use?"

The correct relationship is a containment, and it is never reversed:

```
research universe  >  literature  >  candidate mechanisms
                   >  publicly measurable phenomena  >  repository experiments
```

**Existing code is evidence of what has been attempted. It is not evidence of what to attempt.**
When a new question opens, the first move is *outward* — to the field — not *inward* to `src/`.

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
14. **A direction having been pursued does not make it the project's future.**
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
| [[docs/PROBLEM-MAP]] | **frozen evidence** — the closed programmes' findings and lessons |
| [[CHARTER]] | **historical** — the third programme's charter, terminated at §11 |
| [[core-risk-overlay]] | **historical** — chronological log |
| `closed-research/` | **historical, reproducible** — three programmes, own charters and check suites |

Change the authoritative documents first, and never edit [[CHARTER]] or `closed-research/` to make the
past look tidier than it was.

**No document outside this repository has authority over it.** The charter in
`regime-detection/governance/` governs three other repositories; this one is not in that stack, is not
audited against it, and owes it no reconciliation. If a rule is meant to bind work here, it is written
here.

## 8. Run commands

```powershell
.venv\Scripts\python.exe checks.py                               # 72 active checks
.venv\Scripts\python.exe d4_crosscheck.py                        # 28 vs authors' jumpmodels pkg
.venv\Scripts\python.exe closed-research\checks.py               # 81 frozen
.venv\Scripts\python.exe closed-research\intervention\checks.py  # 17 frozen
.venv\Scripts\python.exe closed-research\return-states\checks.py # 180 frozen
```

`data/` is gitignored; `data/MANIFEST.md` is tracked and is what makes reproduction checkable rather
than asserted.

## 9. What a future agent's job is

Not this:

> "My job is to improve the existing regime detector."

This:

> **"My job is to investigate meaningful, testable questions about systematic market and portfolio
> risk, using the repository as a laboratory and the broader quantitative-finance literature as the
> starting point."**

The project does not need to find something. It needs to determine what is true. If the answer is
already known, reproduce it or move on. If it is false, close it. If there is a real unresolved
phenomenon, establish it carefully — and only then ask whether it is useful.

## Related

- [[README]] · [[docs/RESEARCH-PROTOCOL]] · [[docs/POINT-IN-TIME-DISCIPLINE]] · [[PARKED]]
- [[docs/PROBLEM-MAP]] — frozen evidence · [[core-risk-overlay]] — chronological log
