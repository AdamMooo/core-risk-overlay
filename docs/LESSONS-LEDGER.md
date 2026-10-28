# Lessons Ledger — what the three closures teach

Last updated: 2026-10-25. **Status: synthesis, not evidence.** Written after the 2026-10-25 policy
change in [[CLAUDE]] re-opened the repository to continuing enquiry. This document distils what the
three closed programmes established about *the data, the estimators, and the method class* — so a
new question can be argued with that evidence in hand, rather than rediscovering it.

Nothing here is new measurement. Every row cites the frozen source. The ledger is organised by
*what was learned*, not by programme.

## 1. What the data will and will not support

| # | fact | source | binding on what |
|---|---|---|---|
| L1 | **Public return-volatility estimators are five smoothings of one quantity.** Realized vol, EWMA, GARCH, MS state, absorption ratio all nest inside `F_returns ⊆ F_market`; AR built explicitly to escape this came back +0.4965 correlated with VIX. | PROBLEM-MAP §0.4, F5 | Any new feature family built from the return series alone — needs an argument that it sees something these five do not. |
| L2 | **Systemic episodes have effective n ≈ 10–15 across all of SPY history.** This is the common cause of F9–F11 and F4 and is not fixable by better estimators. | PROBLEM-MAP F9–F11 | Any claim whose statistic is dominated by crisis-count: block bootstrap required, point estimates not quotable as effect sizes. |
| L3 | **A reproduction's edge can live in a single decade.** SJM-2024 reproduces path dominance across the whole CDaR curve, but the entire CAGR advantage is the 2000s (+8.3pp/yr); every other decade loses. | REPRO-SJM2024 §Findings, point 3 | Any claim about regime-based strategies: decade-wise subperiod analysis is mandatory before the headline. |
| L4 | **Daily resolves memory to lag 212 (~10 months); weekly hides all of it inside a ±0.0469 band.** | PROBLEM-MAP E8 | Sampling frequency is a design decision, not a convenience: weekly loses the memory signal entirely. |
| L5 | **Marked PnL and cash PnL are not the same object.** Same simulation, one accounting change: 82–85% of the headline drawdown reduction is unrealised mark. In cash the full-sample tenor reduction at 52w is ~0 to slightly negative. | PROBLEM-MAP §0, E12 | Every path-functional comparison needs the accounting rule written down *before* the run. No magnitude is interpretable without it. |
| L6 | **Roll phase / calendar alignment is a hidden hyperparameter.** The 52w cash cell ranges −6.3 to +7.8pp as the roll offset moves. Phase spread 1.85–6.82× the effect in cash. | PROBLEM-MAP E13 | Any calendar-grid intervention: sweep all phases, no selection — single-alignment results are one draw of a highly variable statistic. |
| L7 | **E2's estimand repair.** Using `CDaR(worst q%)` with episodes matched on the naked book kills the tenor ordering in cash at every q; max-drawdown comparisons between different peaks are between different episodes. | PROBLEM-MAP E14 | Max-drawdown is n=1; whole-curve CDaR with matched episodes is the minimum acceptable path-functional. |

## 2. What the method class predicts, independent of fit quality

| # | fact | source | binding on what |
|---|---|---|---|
| M1 | **Unsupervised compression of return-based features recovers a volatility meter.** Dominant-variance direction of return-magnitude inputs is vol level; the recovered state is near-monotone in trailing realized volatility. SJM-2024 lambda sweep: state-vs-RV AUC rises from 0.762 (k-means) to 0.947 (lambda=150), climbing *with* performance. | PROBLEM-MAP §0.9, REPRO-SJM2024 §Sweep | K-means, GMM, HMM, HSMM, SJM, change-point: all the same family on this input. Free check: regress labels on trailing RV before anything else. |
| M2 | **The jump penalty adds persistence, not information.** At lambda=0: Sharpe 0.04, 1503% turnover. At lambda=70: Sharpe 0.44, 144% turnover. Same features. | REPRO-SJM2024 §Sweep | Any persistence-regularised state model: separate the persistence contribution from any claimed information contribution before attributing performance. |
| M3 | **Squared-return ACF of any MS model decays geometrically.** For any k, any parameters — Timmermann (2000) Prop. 5. | PROBLEM-MAP E6 | MS/HMM cannot match power-law memory as a matter of theorem, not fit; feature. |
| M4 | **Finite Gaussian mixtures are Gaussian in the far tail.** For any k, any weight — algebra. | PROBLEM-MAP E7 | More regimes cannot fix a tail; a tail claim needs non-mixture structure (jumps, EVT, heavy-tailed innovations). |
| M5 | **The jump penalty changes which local optimum coordinate descent finds.** At lambda_ours=30 on synthetic 18%-bear data, 10 restarts land in a 73%-bear local optimum. CV sweeps over lambda are sweeps over qualitatively different fits. | REPRO-SJM2024 §D4 | Any CV over a persistence hyperparameter: report the fitted-regime proportions per fold, not just the loss. |
| M6 | **Feature halflife bounds regime resolvability.** EWM Sortino halflife 60d cannot resolve a 25-day bear segment. | REPRO-SJM2024 §D4 | Feature halflives are a resolution floor on claimed regime durations; a shorter regime claim requires faster features. |

## 3. What the closures teach about *framing*

| # | lesson | source | the error it names |
|---|---|---|---|
| F1 | **Alignment of the model to the target matters more than within-family model choice.** The unsupervised family returns a vol meter whether you fit K-means, HMM, or SJM; the right correction is to ask whether the research object fits the method, not to swap methods. | PROBLEM-MAP §0.9 → PROTOCOL P12 | "Try a different model" after a null result. |
| F2 | **Signal economics vs protection economics are separate questions.** Timing a structure cannot be evaluated unless the structure itself has been evaluated against the base case. Item 5 (variance targeting on equity weight) proposed signal economics without ever measuring the base case. | PROBLEM-MAP §5.0 | Running a timing experiment with no measured passive comparator. |
| F3 | **Fixing by assumption what later turns out to dominate.** The prediction programme held tenor constant and researched the probability estimate; tenor turned out to be the dominant structural variable. | PROBLEM-MAP §0.4 | Pre-committing design parameters that have never been measured. |
| F4 | **"Not identified" is a legitimate reportable result.** Every magnitude in the intervention branch collapsed under accounting (E0), phase (E1), and estimand (E2) scrutiny. The ordering survived in marks only where Psi showed 1–2 episodes carrying the coordinate. | PROBLEM-MAP §1.1, intervention README | Treating a point estimate as an effect size when the underlying population is one or two episodes. |
| F5 | **Rediscovering published results is a process failure.** The tenor ordering was derived empirically here; Israelov (2017) *Pathetic Protection* reports it. Row 1 of the reading list, `[UNREAD]`. | PROBLEM-MAP §1.1 | Literature check deferred until after the run. Now PROTOCOL §0 field 3. |
| F6 | **Reproducing the paper means reproducing the code, not the prose.** SJM-2024's `preprocess.py::DataClipperStd` (3σ winsorization) and `base.py::init_centers()` (warm-start from prior fit) are absent from the paper's text. | REPRO-SJM2024 §Fidelity audit, D7/D8 | Trusting the methods section as a complete specification. |
| F7 | **Benchmarks must contain a reactive incumbent.** SJM-2024's comparison set was buy-and-hold + a deliberately-noisy HMM; adding a 200d MA and a 10% vol target cuts the JM margin substantially and reveals the state is a slow volatility threshold. | REPRO-SJM2024 §Fidelity audit, point 4 | Comparing against a straw man. |

## 4. Methodology gates these lessons produced

These are now binding in [[docs/RESEARCH-PROTOCOL]]:

- Claim tuple `(frequency, horizon, functional, sample, null)` committed before any code — one-step marginals cannot support path-functional claims (from L5, L7).
- Literature check as a committed field — a result rediscovered from an unread paper logs as a process failure (from F5).
- Mechanism and horizon stated as a gate, not a courtesy — invisible at the horizon ⇒ comparison is void (from F3).
- "Not identified" as a permitted written-before-run answer (from F4).
- No magnitude without identification: orderings, signs and falsifications only when the population is thin (from L2, F4).
- P12: "the correct response to a negative result is to ask whether the research object and representation are appropriate — not to substitute another model" (from F1).

## 5. What the lessons *do not* say

- They do not forbid reuse of any closed estimator. A jump model, an HMM, an EVPI construction may be
  used *if the question requires them*. The question picks the model (CLAUDE §6.13).
- They do not say "prediction from public data is impossible." They say *one family* was closed on
  *one target* at *two horizons* on *SPY* against *VIX*. Credit, funding, breadth, positioning,
  cross-asset structure were never tested (PROBLEM-MAP §0.3).
- They do not say the intervention branch is dead. They say the magnitudes are not identified under
  current accounting and phase assumptions, and the ordering survives in marks only where Psi
  collapses. A reformulated question — e.g., *cash-recognised* path properties with a declared
  monetisation rule — would be admissible.

## 6. Candidate directions these lessons point toward

**Not a queue.** These are the directions the evidence makes most legible. Each still requires a
charter and the PROTOCOL §0 gate before any code.

| direction | what the lessons suggest | principal risk |
|---|---|---|
| **Non-return observables.** Credit spreads, funding (TED, SOFR–IOER), breadth, cross-asset structure — anything *not* in `F_returns`. | L1 says return-based features saturate; the escape is new information, not a new estimator. | Many of these are also VIX-correlated; the mechanism-for-difference gate (PROTOCOL §0 field 4) must be argued. |
| **Jumps and heavy tails as the primitive, not regimes.** | M3+M4 say mixtures of Gaussians cannot match either long memory or far-tail mass. A jump-diffusion or EVT formulation addresses both as a matter of theorem. | Identifiability of jump intensity on finite samples; see MATH-AUDIT-JUMPMODEL for what lambda is actually estimating. |
| **Path-functional claims with declared monetisation.** | L5+L7 say every path-functional comparison in this repo prior to 2026-08-18 was in marks; cash recognition kills most of them. A path claim committed with monetisation up front is still open. | Requires an *admissible* monetisation rule — this is the U3 question the intervention branch left unanswered. |
| **Measurement, not prediction.** | A valid result (CLAUDE §4) is "current conditions imply elevated exposure to form-X risk" — no asset named, no path implied. The data supports this far more cleanly than it supports a decision rule. | Must resist the drift from measurement to intervention; see F2. |

## Related

- [[CLAUDE]] — the operating manual, updated 2026-10-25
- [[docs/PROBLEM-MAP]] — frozen evidence from the two closed programmes
- [[docs/REPRO-SJM2024-FINDINGS]] — the reproduction's full record
- [[docs/RESEARCH-PROTOCOL]] — the gate every new question passes
- [[closed-research/intervention/README]] — the intervention programme's closure
