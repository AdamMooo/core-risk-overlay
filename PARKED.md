# Parked

Last updated: 2026-08-17

**Ideas deliberately excluded from the active program, written down rather than built around.**

This file exists so that an interesting thought has somewhere to go that is not the codebase. Under
[[CHARTER]] §8, an experiment whose `BOUNDARY` field is empty does not run — it lands here. Under §10,
this is the only place a non-queued idea may live.

**Being parked is not a queue position.** Nothing moves from here to [[CHARTER]] §9 without meeting
the seven-field gate, including a reopening condition where one is stated.

---

## Parked from the transition (2026-08-17)

| item | why parked | what would unpark it |
|---|---|---|
| **Sample definition.** `SUBSAMPLE_START = 2003-01-24` is the closed model's 520-week burn-in, inherited by `research/hedge_economics.py` and `research/structure_map.py` for no active reason | changing it is an experiment, not a migration, and it changes every published number | E1/E2 must state the sample they use and why. Candidates: full history; a split on options-market depth rather than on a filter's burn-in |
| **Matched-budget comparison.** The grid compares structures at equal *notional* (`hedge_ratio=1.00`), not equal premium spend | a real methodological improvement, and it would reorder the grid — so it is an experiment | fold into E7, where `I_opt` and `I_sleeve` must be compared at matched outlay anyway |
| **Ladders.** Overlapping tenors rather than one block at a time | not in `simulate`; adding it is new machinery before E0 has said what the existing machinery measures | after E0-E2, if tenor survives as a live axis |
| **Optimal tenor as a convex program.** CDaR is convex in the position (Chekhlov, Uryasev & Zabarankin), so tenor/notional choice under a premium budget is plausibly a convex optimization | this is optimization, and the charter puts identification first | after the frontier's coordinates are identified, i.e. after E2 and E5 |
| **Monetisation as optimal stopping.** When to sell the put and convert to shares is a genuine stochastic-control problem | E6 specifies *a* rule and measures it. Optimising over rules is a different and much larger question, and optimising a rule against the realized trough is clairvoyant | after E6 establishes that `kappa` is materially non-zero under a simple stated rule |
| **Tax modelling.** Monetisation realizes income while the core's loss stays unrealized; the sign is known, the magnitude is not | it is a decision-layer input and depends on account structure, which is not a research fact | when the decision layer exists and the account structure is stated |
| **Currency.** A USD put's CAD value rises in a crisis — an unmodelled term pointing *for* the hedge | same: it changes magnitudes nobody is entitled to quote yet | when a magnitude becomes identified enough to be worth correcting |
| **Drawdown-duration objective.** `U_theta` and `R` are implemented but no hypothesis uses them | "smooth the ride" has never been stated precisely enough to falsify | when the mandate says what it wants from duration, distinct from depth |

## Parked from the closed program — reclassified, not reopened

These are **not** revivals of the prediction question. Each is a different *use* of material the
closed program touched, and each is listed so the distinction stays visible.

| item | the closed use (stays closed) | the reclassified use |
|---|---|---|
| **The option surface** | a predictor of realized risk, or a search for mispricing. Closed — [[docs/PROBLEM-MAP]], and we lack the chain depth, infrastructure and information set to compete there | a **procurement** input: what does the protection I intend to buy actually cost. E5, rejection-only |
| **Cross-market data** | a joint information set for a signal. Closed by F4/F5 — the absorption ratio's trigger was an artifact and its level was half VIX | **independent replication samples for a structural claim** (H1/E4). No signal, no information set, no forecast |
| **S4 / skewed heavy-tailed regime densities** | a fix for the α=0.01 tail failure, in service of a VaR the decision no longer uses | the **paper**. The D3 + dynamics negative plus the PIT asymmetry is publishable and needs no new data |

## Permanently closed — do not park, do not reopen

Listed here only so that "it is not in PARKED" is never read as "it is available."

Prediction of forward risk from public return-volatility estimators (F1, F2), the h=1 EWMA
comparison (F10), GARCH encompassing (F11), within-regime ARCH (S3), the memory-shape question (F3,
U6), the absorption ratio as a trigger (F4, F5), all trigger rules (F9), the Hamilton-filter recovery
board and its six items, **Item 5 and its three resolutions** — the last withdrawn because
[[CHARTER]] §2's C1 and C2 exclude variance targeting on `w_equity` formally, not merely in spirit.

Evidence and reasoning: [[docs/PROBLEM-MAP]] Part II. Code: [[closed-research/README]].

## Related

- [[CHARTER]] — the active program · [[docs/PROBLEM-MAP]] — the evidence base
