# CLOSED RESEARCH

**This directory holds TWO closed programs, both preserved for provenance and replication. Neither
is an active research branch and neither receives new experiments.**

| | program | closed | where |
|---|---|---|---|
| 1 | **prediction / regime** — can a public-data latent-state signal say *when* to change a standing overlay? | 2026-08-17 | this directory |
| 2 | **rolled-put / tenor intervention** — which features of drawdown geometry are purchasable, identified, and at what cost? | 2026-08-18 | `intervention/`, with its own README, charter and preregistrations |

**They closed each other.** Programme 2's last surviving structural claim (E4's strike anchoring)
turned out to be conditional on whether a decline grinds or V-bottoms — a quantity knowable only by
the forecast programme 1 had already closed.

The active program is the **return-state** charter at `../CHARTER.md`. It shares no code with either
of these.

Everything below describes programme 1.

This is completed research, not obsolete code. Its negative results are part of what motivates the
program that replaced it, and they are only worth something if they can still be re-run.

---

## What was closed, and why

The program asked: *can a public-data latent-state / volatility-regime signal tell us when to change
the size or timing of a standing put overlay?*

It was closed on 2026-08-17 after three findings, none of which is a failed search:

1. **The measurement is nested inside a free benchmark.** The model's forward-downside information
   is strictly contained in VIX's, on levels (D3: `c = +0.0009`, `p = 0.99`, joint R² equal to
   VIX-alone to four decimals) and on dynamics (F2: adds 0.0004 of R², with power demonstrated
   rather than assumed).
2. **The ceiling on any signal was computed without needing to find one.** The clairvoyant bound
   (EVPI) caps timing at roughly +3pp/yr at the tested tenors; real rules captured 4-7% of it.
3. **The variable that mattered had been fixed by assumption.** The original plan fixed tenor and
   strike and researched the probability estimate. Tenor turned out to dominate.

**Scope of the closure, stated precisely so it is not over-read.** What is closed is the family of
*public return-volatility estimators*, for *decision* purposes, on *SPY*, against *VIX*, on forward
downside semivolatility at h=4 and h=13. It is not a claim that no predictive edge exists anywhere.
Whole classes of information — credit, funding, breadth, positioning — were never tested and are out
of scope rather than refuted.

## Contents

| file | what it established |
|---|---|
| `walkforward.py` | E4: the first look-ahead-free predictive density. Body calibrated, tail broken, degrading monotonically with depth |
| `encompassing.py` | **D3** — the model is nested inside VIX on levels |
| `dynamics_test.py` | **F2** — and on dynamics, the one axis VIX structurally lacks |
| `baselines.py` | E5: every method breaches ~2x at α=0.01. The tail failure belongs to the data, not the model |
| `state_character.py` | E1-E3: a width meter, no direction content, arriving ~13% below the running peak |
| `memory_diagnostic.py` | E8 and F3: daily resolves memory to lag 212; the power-law claim was refuted, weakly |
| `systemic_state.py` | **F4/F5 — REFUTED METHOD.** The expanding-percentile trigger fired 76.9% of weeks in 2004-06 and 4.0% in 2018-26. Retained as evidence of the failure, never as a component |
| `trigger_bracket.py` | Real VIX rules capture 4-7% of available selection skill; no rule beat not hedging on return |
| `figures.py` | The preregistered figure set for the above |
| `checks.py` | 81 checks guarding the pipeline that produced all of it |
| `docs/MATH-REFERENCE.md` | The mathematics of the model class. Densities, mixtures, filters — and, notably, no drawdown |
| `docs/TRANSLATION-LAYER.md` | The width/direction separation. Binding on a filter that no longer exists |
| `docs/STUB-GARCH-ENCOMPASSING.md` | A preregistration that was never executed — see its own closure note |
| `docs/literature/` | The reading list for the closed question |

## Reproducing

Run from the repository root, so the shared `data/` cache resolves:

```
.venv\Scripts\python.exe closed-research/encompassing.py SPY      # D3
.venv\Scripts\python.exe closed-research/dynamics_test.py SPY     # F2
.venv\Scripts\python.exe closed-research/checks.py                # 81 checks
```

Both flagship negatives were verified to reproduce bit-for-bit after the move on 2026-08-17.

**And that claim now has something behind it.** `data/` is gitignored, and `density_spy.csv` -- which
D3 and F2 are computed from -- is a **derived artifact from a long refit loop**, not a download. Until
2026-08-18 "it reproduces" rested entirely on files git does not track. `data/MANIFEST.md` records the
sha256, row count and date range of every cache file and **is** tracked; `checks.py` verifies the cache
against it on every run. A cache that differs from the one that produced these numbers is now detected
rather than silently used.

## Two frozen copies, deliberately

`hedge_economics.py` and `src/data_loader.py` are **duplicated** here rather than imported from the
active tree. `trigger_bracket.py` depends on `simulate()`, and the active program is about to change
`simulate()`'s accounting (E0). Importing across the boundary would let an active change silently
alter an archived result. The duplication is the price of provenance and is intentional.

**Nothing in the active tree imports anything from this directory. Nothing here imports from the
active tree.** Both directions were checked at each transition. `intervention/` follows the same rule
and holds its own frozen copy of `pathfunctionals.py` for the same reason.
