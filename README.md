# Core-Risk-Overlay

Last updated: 2026-08-27

> # A RESEARCH LABORATORY FOR SYSTEMATIC MARKET AND PORTFOLIO RISK.
>
> **Purpose and agent behaviour: [[CLAUDE]] (read first).** This file is what is *established*.
>
> **There is no active research programme.** Three have run and all three are closed, and this file is
> the preserved, reproducible record of what each established and why each stopped. **That is a fact
> about the queue, not about the repository's purpose.** A fourth programme requires a new charter,
> argued from the question — never from the code that happens to be here.

**The repository name is historical**, as is everything else here that reads like an instruction. It
names a programme that no longer runs and does not bound the scope of admissible questions.

The order of work, and code is the last step:

```
real-world risk question -> literature -> mechanism -> observable data
    -> mathematical formulation -> empirical test -> falsification
    -> extension -> implementation
```

- **Purpose, agent behaviour, and the repository-gravity warning:** [[CLAUDE]]
- **The last programme's charter, and its termination record:** [[CHARTER]] §11
- **Process — the gate every experiment passes:** [[docs/RESEARCH-PROTOCOL]]
- **Time basis and leak register:** [[docs/POINT-IN-TIME-DISCIPLINE]] · **Mathematics of the
  drawdown process and the CDaR family:** [[docs/MATH-REFERENCE]] — a live conventions
  document; `src/pathfunctionals.py` implements it and every published CDaR number obeys it
- **What is identified under the null:** [[docs/IDENTIFICATION-UNDER-N1]] · **why Q1 is not licensed
  and what replaces it:** [[docs/DECISION-Q1-CLAIM]]
- **The jump model's mathematics, audited — what the estimator is and what lambda means:**
  [[docs/MATH-AUDIT-JUMPMODEL]]
- **Evidence base from the closed programs, frozen:** [[docs/PROBLEM-MAP]]
- **Deliberately excluded, including the hedging mandate:** [[PARKED]] · **Chronological log:**
  [[core-risk-overlay]]
- **Closed research, preserved and reproducible, not active branches:**
  [[closed-research/README]] (prediction) · [[closed-research/intervention/README]] (rolled-put)

---

## 1. The three programmes, and how each ended

| | programme | closed | how it ended |
|---|---|---|---|
| 1 | **prediction / regime** — can a public-data latent-state signal say *when* to change a standing overlay? | 2026-08-17 | the measurement was **nested inside VIX** on levels and dynamics, with power demonstrated; and a clairvoyant bound capped any timing rule near +3pp/yr where it was measured |
| 2 | **rolled-put / tenor intervention** — which features of drawdown geometry are purchasable, identified, and at what cost? | 2026-08-18 | 82–85% of the measured reduction was **unrealised mark**; the remainder was smaller than the spread from an arbitrary roll offset; no tenor ordering survived in cash anywhere on the drawdown path; and the last structural claim was **conditional on a forecast programme 1 had closed** |
| 3 | **return states** — do distinguishable return-distribution states exist? | 2026-08-19 | **INDETERMINATE.** Two synthetic identification gates, **no market data ever touched**. The observable proposed to read variance-distribution *shape* could not be separated from the instrument used to match variance *dispersion* |

**Programmes 1 and 2 closed each other**: the intervention branch's last surviving claim required
exactly the forecast the prediction branch had ruled out. **Programme 3 stopped before reaching data**
— which is the cheapest place a programme can stop.

## 2. What programme 3 was asking, and where it got to

The object was the conditional law of the forward return path, `F_{s,h} = law of R_{t:t+h} given
S_t = s`, against a stated null and on a functional declared in advance. It asked four questions in
order — existence, characterisation, transition, identification — and **terminated inside the first.**

The obstruction, stated once because it is the programme's terminal result:

```
    RV_B = SUM sigma2_t z2_t
```

The observed block-variance distribution depends on both the latent variance distribution and the
innovation distribution. Matching the latent *dispersion* required using `E[z^4]` as the instrument,
which necessarily changed the observation noise in the same statistic. **The mechanism that removed
the difference under test also contaminated the measurement of it.** Full record:
[[closed-research/return-states/README]].

## 3. What this is not

Four things, each rejected explicitly. The first three have evidence behind the rejection rather than a
preference; the fourth is a statement of scope.

**Not a hedging or option-structure project.** That program ran, and it closed on 2026-08-18. Its
code, results and preregistrations are preserved at [[closed-research/intervention/README]]. Summary
of why: 0 of 40 structures beat the naked book on compound return; 82–85% of the measured drawdown
reduction turned out to be unrealised **mark** rather than cash; the remaining magnitude was smaller
than the spread produced by an arbitrary roll-calendar offset, and in cash its **sign** flipped with
that offset; with the estimand repaired no tenor ordering survived anywhere on the drawdown path in
cash; and the last surviving structural claim proved conditional on whether a decline grinds or
V-bottoms — a quantity knowable only by the forecast the *prediction* program had already closed.

**Not a prediction or timing project.** That program ran too, and closed on 2026-08-17
([[closed-research/README]]). A latent-state model's forward-downside information proved strictly
nested inside VIX's, on levels and on dynamics, with power demonstrated rather than assumed; and a
clairvoyant bound capped what *any* timing rule could be worth near +3pp/yr where it was measured.
**The closure is scoped, not universal** — public return-volatility estimators, for decision
purposes, on SPY, against VIX, at h=4 and h=13. Credit, funding, breadth and positioning were never
tested and are out of scope rather than refuted.

**Not an attempt to out-price the option market.** That needs a fair-value model better than the
market's, plus chain depth, execution infrastructure and a market-maker's information set. We have
none of them and acquiring them is not this project.

**Not a component of another repository's system.** This repository stands alone — no upstream, no
downstream, no sibling to reconcile with, and no governing document outside its own tree. It shares the
`systematic-investing-research/` directory with three governed repositories and is not one of them; it
is neither an extension nor a successor of `regime-detection`; nothing here imports from another
repository and nothing there imports from here. The one cross-repository fact on record is that
point-in-time option chains exist elsewhere, and that is an acquisition option for a question nobody has
argued yet — not a dependency and not an agenda. [[CLAUDE]] §3.

## 4. What the closed programmes left behind

They are evidence and institutional memory, **not a dependency**. Nothing in the active tree imports
from `closed-research/`, and nothing there imports from the active tree.

**Findings that would constrain any new programme directly** — these are boundary conditions, not
history:

| | binds how |
|---|---|
| A finite Gaussian mixture is **Gaussian in the far tail** for any `k` and any weight; the squared-return ACF of any Markov-switching model decays **geometrically** for any `k` | if tail thickness or non-geometric memory is a proposed distinguishing property, the mixture class is disqualified *a priori* |
| At α=0.01 every method breaches ~2x — constant 1.87%, EWMA 2.03–2.36%, MS 1.79% | the tail failure belongs to **the data under a Gaussian assumption**, not to any model |
| Weekly data cannot resolve volatility memory at all; daily resolves it to lag 212 | the active program is **daily** ([[CHARTER]] D2) |
| The fitted state was a **width meter** — vol separating 2.4x, no direction content, drift difference reversing sign between SPY and QQQ | states are named by what distinguishes them, never by what one would do about them |
| Anything whose value depends on counting systemic episodes has effective n ~ 10–15 in all of SPY history | effective n is reported **per coordinate**, before the run |

**Methodological lessons, carried into the protocol:** identification before optimization; mechanism
before magnitude; robustness before ranking; no single-path economic claims; a mark is not a cash
flow, an ordering is not a magnitude, and a bound is not an estimate; effective sample size is
explicit; phase and path dependence matter; negative results are evidence; **"not identified" is a
legitimate result**; research boundaries are explicit; archived research stays reproducible.

## 5. Implementation status

The active tree is deliberately small. **There is no model, no detector, no engine, and none is
designed** — [[CHARTER]] §8.

| component | state |
|---|---|
| `src/data_loader.py` | working — daily and weekly returns, VIX, start-date invariant, explicit calendar |
| `src/pathfunctionals.py` | working — drawdown process, excursions with censoring, CDaR curve, time under water. Retained because drawdown geometry is a **candidate state characteristic**, not because it was an objective |
| `src/manifest.py` | working — the data cache's sha256 manifest. `data/` is gitignored and two caches are derived artifacts, so `data/MANIFEST.md` is what makes "the archives reproduce" checkable rather than asserted |
| `closed-research/return-states/` | return-state programme — 180 checks passing, S0b verified to reproduce after the archive move (control `d' = 7.416`) |
| `src/jumpmodel.py`, `src/sjm_features.py`, `repro_sjm2024.py` | **reproduction in progress, verified** — Shu-Yu-Mulvey (2024) rebuilt with the reactive incumbents the paper omits. Findings and the open list: [[docs/REPRO-SJM2024-FINDINGS]]. **D4 discharged 2026-08-24** — brute-force DP enumeration, synthetic known-state recovery, exact equivalence with the authors' package; surfaced the lambda convention (a lambda here = half its paper-units face value) |
| `d1_cv.py` | the D1/D6 run — the paper's monthly CV lambda selector on the full paper grid, both naming rules, preregistered and scored in [[docs/REPRO-SJM2024-FINDINGS]] |
| `volthreshold.py` | the preregistered volatility-band incumbent — the cheapest falsification of the reproduction's result, scored against Y1–Y3 in [[docs/REPRO-SJM2024-FINDINGS]] |
| `screen0.py` | Screen 0 of [[docs/ASSESSMENT-PRESENT-STATE-RISK]] — the six-coordinate redundancy/disagreement map, preregistered in its §7b |
| `src/Shu/` | **reference copy, never imported** — three modules of the authors' `jumpmodels` package (github.com/Yizhan-Oliver-Shu/jump-models), retained as the source for fidelity items D5/D7/D8. The live cross-check (`d4_crosscheck.py`) imports the pip-installed package, not this copy |
| `src/caching.py` | shared disk-cache helper used by `repro_sjm2024.py` and `screen0.py` |
| `src/ledoitwolf.py` | working — the four Ledoit-Wolf (2008) contracts for the shallow-half inference: delta-method gradient, block-structure Psi, circular block resampler, studentized test. Contract-checked in `checks.py` |
| `inference.py` | the shallow half of the preregistered inference run — Sharpe and pain intervals against the declared equivalence margins; Z1/Z2 scored 2026-08-26 |
| `deeptail_mc.py` | the deep half — parametric Monte Carlo under the three preregistered nulls (N1 GARCH-t, N2 Markov-switching, N3 i.i.d. resampling); Z0 scored, N1/N2 owed |
| `jm_math_audit.py` | the six synthetic experiments behind [[docs/MATH-AUDIT-JUMPMODEL]] §H, preserved for reproducibility |
| `checks.py` | 72 checks — the two retained modules, the data manifest, since D4 the reproduction modules, and since 2026-08-26 the Ledoit-Wolf contracts. The manifest-hash check is red by design mid-run, until `data/MANIFEST.md` is regenerated at the inference run's close. `d4_crosscheck.py` (28 checks) holds the leg needing the authors' `jumpmodels` package. **The three closed programmes carry their own suites, frozen with the code they guard** |
| `closed-research/` | prediction program — 81 checks passing, D3 and F2 verified reproducible |
| `closed-research/intervention/` | rolled-put program — 17 checks passing, E0 verified reproducible after the archive move |

**There is no queue.** `src/data_loader.py`, `src/pathfunctionals.py` and `src/manifest.py` are
retained because they are correct and general, not because anything is planned. **Nothing here is
waiting to be run** except the one preregistered run in flight — N1/N2 of the deep-tail inference
([[docs/REPRO-SJM2024-FINDINGS]], "The run"), whose Z3/Z4 verdicts close the reproduction thread.

## 6. What counts as a result

Profitability is not on this list, and is not required by any item on it.

| criterion | what it demands |
|---|---|
| **measurement validity** | the quantity measures the phenomenon claimed, not a proxy for it |
| **statistical validity** | it survives appropriate inference — effective n stated, overlap not counted as sample |
| **incremental information** | it is not already carried by an established incumbent, tested at matched complexity |
| **stability** | it survives reasonable temporal and specification changes |
| **mechanistic coherence** | there is a defensible reason *why* the relationship exists |
| **reproducibility** | it rebuilds from accessible data and documented procedure |
| **decision relevance** | it could plausibly change a risk-management decision |
| **economic relevance** | the phenomenon corresponds to a meaningful portfolio risk |

A result satisfying some combination of these is valuable. **A closure is a result** — three of them
are the substance of this repository. So is *"indeterminate on the available history"*, which is how
programme 3 ended.

**Risk intelligence is not alpha.** `X_t -> P(adverse outcome given X_t)` and `risk information ->
risk posture` are the objects here; `X_t -> E[R_{t+h}]` is not, and nothing in this repository is
required to solve it. A valid output is *"current conditions imply materially elevated exposure to
this form of systematic risk"* — no asset named.

**Public data is the constraint, stated rather than worked around.** Institutional researchers may
hold proprietary data, positioning, order flow, execution records and deeper option histories. We do
not, and acquiring them is not this project — so the question is usually what defensible risk
information *public* data can carry. A phenomenon that is robust, reproducible and useful for
monitoring but not directly tradable is an acceptable result. The constraint is not an excuse for a
weak test.
