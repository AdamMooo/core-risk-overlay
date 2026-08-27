# CLOSED — the Shu–Yu–Mulvey (2024) reproduction

**Closed 2026-08-27.** Preserved for provenance and replication. **Not an active branch, not a
backlog, and not a source of next experiments.** There is no active research programme in this
repository.

This is completed research. A reproduction is only worth something if it can still be re-run, and
its verdicts only bind if the code that produced them is frozen with them.

---

## The question it asked

> Can Shu, Yu & Mulvey (2024) — the statistical jump model as a downside-risk regime overlay on
> ^GSPC — be reproduced from public data, and does its downside-risk result survive honest
> inference against the reactive incumbents the paper never ran?

A VERIFICATION programme throughout, never a strategy: the 0/1 exposure rule is F9, permanently
closed in `../../PARKED.md` §4, and was reconstructed only because reproducing the paper's claim
requires reproducing the paper's rule.

## Why it closed, in the order the results landed

| | result | what it settled |
|---|---|---|
| **D4** | the lambda convention. The authors' package computes the loss as `0.5*||x-theta||^2`; this implementation uses `||x-theta||^2`, so `lambda_ours = 2 * lambda_package` — every lambda quoted here is worth HALF its face value in paper units (the lambda=50 run reproduces the paper's 25). Established by brute-force DP enumeration, synthetic known-state recovery, and exact path equivalence against the pip `jumpmodels` package | the implementation, and the units every later number is quoted in |
| **Y1–Y3** | the persistence-matched volatility-threshold bands — the baseline the paper never ran, preregistered with three parameter pairs, none selected — scored against the jump model on the claim's own functionals (whole CDaR curve, time under water, not Sharpe alone). Verdicts recorded in `REPRO-SJM2024-FINDINGS.md` | whether the fitted state carries information a trailing-vol band lacks |
| **Z1 / Z2** | the SHALLOW half (`inference.py`): Ledoit-Wolf studentized block bootstrap for the Sharpe difference, percentile intervals for pain and shallow CDaR, every block length on the declared grid reported, largest p the headline. **Z1 held; Z2 failed** — see the preregistration in `REPRO-SJM2024-FINDINGS.md` for the binding verdict text | the distinguishability and equivalence reads on the averaging functionals |
| **Z0** | the amendment: the N3 i.i.d. control's gap centre is read against the rules' exposure difference (JM ~62% in-market vs bands 62–73%), not against zero — a non-zero centre is expected and is not a failure. Written before any deep-half number was read | what the deep-half control is allowed to mean |
| **Z3** | ⟨PLACEHOLDER Z3 — N1 GARCH(1,1)-t main-null verdict, unread at archive time; transcribe from REPRO-SJM2024-FINDINGS.md once N2's rows land⟩ | |
| **Z4** | ⟨PLACEHOLDER Z4 — N2 Markov-switching power-check verdict, unread at archive time; transcribe from REPRO-SJM2024-FINDINGS.md once N2's rows land⟩ | |

The deep half asks its question under three named nulls because MaxDD and CDaR at 1–5% on this
sample are produced by two episodes (2000–02, 2007–09): effective sample size 2, so a block
bootstrap p-value there reports the block-length knob, not the market. The deep-tail difference is
declared unidentified in magnitude; only distribution width and containment may be quoted.

## Contents

| file | what it is |
|---|---|
| `repro_sjm2024.py` | the reproduction: the paper's 0/1 rule rebuilt with the reactive incumbents its comparison omits (200d SMA, capped vol target), scored on the whole CDaR curve. Declared deviations D1–D4 in its header |
| `d1_cv.py` | the D1/D6 run — the paper's monthly CV lambda selector on the full paper grid, both state-naming rules, the lambda-hat series the paper never reports |
| `d4_crosscheck.py` | D4's third leg: exact equivalence with the authors' `jumpmodels` package and the lambda-convention demonstration. 28 checks; needs `pip install jumpmodels` |
| `volthreshold.py` | the preregistered volatility-band incumbent — the cheapest falsification of the reproduction's result |
| `inference.py` | the shallow half: Ledoit-Wolf Sharpe test, percentile intervals for pain/shallow CDaR, leave-one-episode-out. Z1/Z2 scored here |
| `deeptail_mc.py` | the deep half: end-to-end Monte Carlo under N3 (i.i.d. control), N1 (GARCH-t main null), N2 (Markov-switching power check). Z0/Z3/Z4 |
| `jm_math_audit.py` | the six synthetic experiments behind `../../docs/MATH-AUDIT-JUMPMODEL.md` §H |
| `jumpmodel.py` | the estimator: coordinate-descent jump model, Viterbi/forward DP, online states |
| `sjm_features.py` | the paper's EWM feature set (downside deviation, Sortino) |
| `ledoitwolf.py` | Ledoit-Wolf (2008) studentized circular block bootstrap, prewhitened-QS HAC, Politis-White reference |
| `Shu/` | **reference copy, never imported and not importable** (no `__init__.py`, no `utils.py`) — three modules of the authors' package, retained as the source for fidelity items D5/D7/D8. `d4_crosscheck.py` imports the pip-installed package, not this |
| `caching.py`, `data_loader.py`, `pathfunctionals.py` | frozen copies — see below |
| `checks.py` | 35 checks frozen with the code they guard: the D4 in-repo legs (11), the feature algebra (3), the Ledoit-Wolf contracts (21) |

Preregistrations, findings and verdict text: `../../docs/REPRO-SJM2024-FINDINGS.md`. The
mathematical audit: `../../docs/MATH-AUDIT-JUMPMODEL.md` (evidence-status in the authority table).

## Reproducing

Run from the repository root, so the shared `data/` cache resolves:

```
.venv\Scripts\python.exe closed-research/reproduction-sjm2024/repro_sjm2024.py
.venv\Scripts\python.exe closed-research/reproduction-sjm2024/d1_cv.py
.venv\Scripts\python.exe closed-research/reproduction-sjm2024/volthreshold.py
.venv\Scripts\python.exe closed-research/reproduction-sjm2024/inference.py
.venv\Scripts\python.exe closed-research/reproduction-sjm2024/deeptail_mc.py    # hours; --paths 20 to smoke
.venv\Scripts\python.exe closed-research/reproduction-sjm2024/jm_math_audit.py
.venv\Scripts\python.exe closed-research/reproduction-sjm2024/checks.py         # 35 checks
.venv\Scripts\python.exe closed-research/reproduction-sjm2024/d4_crosscheck.py  # 28 checks; pip install jumpmodels
```

**The inputs are pinned.** `data/MANIFEST.md` records the sha256 of every cache file these scripts
read and write (`sjm_gspc_daily.csv`, `sjm_dtb3.csv`, and the derived `infer_nets_gspc.csv`,
`deeptail_mc.csv`, `deeptail_nulls.json`), and the root `checks.py` verifies it. A cache that
differs from the one that produced these numbers is detected rather than silently used.

## The frozen copies, deliberately

`caching.py`, `data_loader.py` and `pathfunctionals.py` are **duplicated** here rather than
imported from `../../src/`, on the same precedent as the other archives: those three modules stay
live (`screen0.py` and the drawdown/CDaR conventions still use them), and importing across the
boundary would let a later change to the active tree silently alter an archived result. The
duplication is the price of provenance and is intentional. `jumpmodel.py`, `sjm_features.py` and
`ledoitwolf.py` are not copies — they moved here outright, and no live version exists.

**Nothing in the active tree imports from this directory. Nothing here imports from the active
tree.**

## The evidence gap, stated

Two cited artifacts exist only on untracked disk: `figures/sjm2024_gspc.png` (the reproduction's
headline figure) and `figures/sjm2024_lambda_hat.csv` / `figures/sjm2024_lambda_hat_cumret.csv`
(the D1 lambda-hat series, the output the paper never reports). `figures/` is gitignored, so a
fresh clone does not contain them and no hash pins them — unlike the `data/` caches, which
`data/MANIFEST.md` covers. They are regenerated by `repro_sjm2024.py` and `d1_cv.py`
respectively, at those same repo-root paths, but a regeneration years from now depends on the
gitignored `data/` cache surviving. This gap is stated rather than papered over.
