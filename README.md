# Core-Risk-Overlay

Last updated: 2026-08-18

> # THERE IS NO ACTIVE RESEARCH PROGRAMME IN THIS REPOSITORY.
>
> Three programmes have run and all three are closed. The repository is a preserved, reproducible
> record of what each established and why each stopped. **A fourth would require a new charter.**

**The repository name is historical**, as is everything else here that reads like an instruction.

- **The last programme's charter, and its termination record:** [[CHARTER]] §11 (**read first**)
- **Process — the gate every experiment passes:** [[docs/RESEARCH-PROTOCOL]]
- **Time basis and leak register:** [[docs/POINT-IN-TIME-DISCIPLINE]] · **Mathematics:**
  [[docs/MATH-REFERENCE]]
- **What is identified under the null:** [[docs/IDENTIFICATION-UNDER-N1]] · **why Q1 is not licensed
  and what replaces it:** [[docs/DECISION-Q1-CLAIM]]
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

Three things, each considered and rejected explicitly, each with evidence behind the rejection rather
than a preference.

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

## 4. What the closed programmes left behind

They are evidence and institutional memory, **not a dependency**. Nothing in the active tree imports
from `closed-research/`, and nothing there imports from the active tree.

**Findings that constrain the new program directly** — these are boundary conditions, not history:

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
| `closed-research/return-states/` | return-state programme — 140 checks passing, S0b verified to reproduce after the archive move (control `d' = 7.416`) |
| `checks.py` | 37 checks, all passing — the two retained modules and the data manifest. **The three closed programmes carry their own suites, frozen with the code they guard** |
| `closed-research/` | prediction program — 81 checks passing, D3 and F2 verified reproducible |
| `closed-research/intervention/` | rolled-put program — 17 checks passing, E0 verified reproducible after the archive move |

**There is no queue.** `src/data_loader.py`, `src/pathfunctionals.py` and `src/manifest.py` are
retained because they are correct and general, not because anything is planned. **Nothing here is
waiting to be run.**
