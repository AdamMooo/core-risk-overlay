# CLOSED — the rolled-put / tenor intervention program

**Closed 2026-08-18.** Preserved for provenance and replication. **Not an active branch, not a
backlog, and not a source of next experiments.** The active program is the return-state charter at
`../../CHARTER.md`.

This is completed research. Its negatives are the reason the program that replaced it exists, and
they are only worth something if they can still be re-run.

---

## The question it asked

> Under a permanent-long constraint, which features of the book's drawdown geometry are demonstrably
> alterable by an admissible intervention; which of those alterations are identified in magnitude
> from available data; and at what cost?

## Why it closed, in the order the results landed

| | result | what it removed |
|---|---|---|
| **E9** | 0 of 40 structures beat the naked book on CAGR, both samples | the founding arithmetic. The overlay is a purchase |
| **E0** | 82% (1993–) / 85% (2003–) of the 52w drawdown reduction is unrealised **mark**; +16.8pp becomes +3.0pp in cash | every magnitude in the repo, until an accounting label was attached to it |
| **E1** | in cash the *sign* of the 52w result is set by roll-calendar alignment (−6.3 to +7.8pp); the phase spread is 1.85–6.82x the effect | the magnitude, in both accountings |
| **E2** | with the estimand repaired — `CDaR(worst q%)`, episodes matched on the naked book — **no tenor ordering survives in cash at any q**; in marks it survives only where `Psi` shows 1–2 episodes carrying the coordinate | the ordering as a path property |
| **E4** | M1 strike anchoring is a **deductible-count effect**, `m·(SUM re-strike levels − S_0)`, vanishing by identity at `m=0`, failing 100% of episodes at `m=5%`, and conditional on decline shape | the last unconditional structural claim |

**The terminal finding.** E4 left M1 real but conditional on whether a decline grinds or V-bottoms —
a quantity knowable only by the forecast the *prediction* program closed. The intervention branch's
remaining value was gated on the prediction branch's answer, and that answer was no. **The two
programs closed each other.**

## E3, E5, E6, E7 are CLOSED, not queued

They were downstream of a claim that no longer stands. None is future work. None creates an
obligation. Reopening any of them requires a new charter, not an experiment. See `../../PARKED.md`.

## Contents

| file | what it established |
|---|---|
| `hedge_economics.py` | `simulate()`, Black-Scholes puts, the `skewed_vol` surface assumption, the EVPI clairvoyant bound. Carries the `mark_hedge` and `phase` switches E0 and E1 rest on |
| `structure_map.py` | E9, E10, F6, F12 — the tenor x strike x outright/spread grid, no timing anywhere |
| `m3_decomposition.py` | **E0** — the marked-versus-cash accounting decomposition. H3 rejected |
| `phase_sweep.py` | **E1** — the roll-phase sweep. H2's phase clause killed in cash |
| `path_outcomes.py` | **E2** — the CDaR curve and episode-matched depths. H2 fully resolved |
| `anchoring.py` | **E4** — payoff-geometry anchoring across four markets and a century. No pricing anywhere in it |
| `pathfunctionals.py` | frozen copy — see below |
| `checks.py` | 17 checks: the E0 accounting invariant, E1's roll-phase grid, E4's payoff arithmetic |

Preregistrations and full results: `../../docs/STUB-E0-M3-DECOMPOSITION.md`, `STUB-E1-ROLL-PHASE.md`,
`STUB-E2-DRAWDOWN-PATH.md`, `STUB-E4-STRIKE-ANCHORING.md`. Evidence base: `../../docs/PROBLEM-MAP.md`.

## Reproducing

Run from the repository root, so the shared `data/` cache resolves:

```
.venv\Scripts\python.exe closed-research/intervention/m3_decomposition.py   # E0
.venv\Scripts\python.exe closed-research/intervention/phase_sweep.py        # E1
.venv\Scripts\python.exe closed-research/intervention/path_outcomes.py      # E2
.venv\Scripts\python.exe closed-research/intervention/anchoring.py          # E4
.venv\Scripts\python.exe closed-research/intervention/checks.py             # 17 checks
```

E0 was verified to reproduce after the move on 2026-08-18.

## The frozen copy, deliberately

`pathfunctionals.py` is **duplicated** here rather than imported from `../../src/`. The active
program retains drawdown functionals as a candidate state characteristic and may change them;
importing across the boundary would let an active change silently alter an archived result. Same
reason `data_loader.py` is frozen one level up at `../src/`. The duplication is the price of
provenance and is intentional.

**Nothing in the active tree imports from this directory. Nothing here imports from the active
tree.**
