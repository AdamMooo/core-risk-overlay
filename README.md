# Core-Risk-Overlay

Last updated: 2026-08-18

**The repository name is historical.** It names a program that no longer runs. What is active here is
a research program on **return states**.

> **We are not trying to win the pricing game. We are trying to determine whether the return
> distribution itself enters distinguishable states, how those states transition, and whether the
> change in distribution is real, persistent, and identifiable.**

- **The active program — object, null, boundary, gate, stopping rules, queue:** [[CHARTER]]
  (**read first**)
- **Process — the gate every experiment passes:** [[docs/RESEARCH-PROTOCOL]]
- **Time basis and leak register:** [[docs/POINT-IN-TIME-DISCIPLINE]] · **Mathematics:**
  [[docs/MATH-REFERENCE]]
- **Evidence base from the closed programs, frozen:** [[docs/PROBLEM-MAP]]
- **Deliberately excluded, including the hedging mandate:** [[PARKED]] · **Chronological log:**
  [[core-risk-overlay]]
- **Closed research, preserved and reproducible, not active branches:**
  [[closed-research/README]] (prediction) · [[closed-research/intervention/README]] (rolled-put)

---

## 1. The question

> **Are there empirically distinguishable states in which the distribution of future equity returns
> is sufficiently different from the ordinary state that the statistical character of the risk one is
> holding has materially changed?**

The object of study is the conditional law of the forward return path, `F_{s,h} = law of R_{t:t+h}
given S_t = s`. The program asks whether such states **exist**, what **characterises** them, how they
**transition**, and whether they are **identified** — in the sample, and in real time.

**It terminates there.** What one should do about a state is a different question, belonging to a
different charter that does not exist. See [[CHARTER]] §3 and §7.

## 2. What this is not

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

## 3. What the two closed programs left behind

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

## 4. Implementation status

The active tree is deliberately small. **There is no model, no detector, no engine, and none is
designed** — [[CHARTER]] §8.

| component | state |
|---|---|
| `src/data_loader.py` | working — daily and weekly returns, VIX, start-date invariant, explicit calendar |
| `src/pathfunctionals.py` | working — drawdown process, excursions with censoring, CDaR curve, time under water. Retained because drawdown geometry is a **candidate state characteristic**, not because it was an objective |
| `checks.py` | 35 checks, all passing, covering the two modules above |
| `closed-research/` | prediction program — 81 checks passing, D3 and F2 verified reproducible |
| `closed-research/intervention/` | rolled-put program — 17 checks passing, E0 verified reproducible after the archive move |

**Everything else is a document.** That is the intended shape at this stage: the first experiment is
not written until [[docs/STUB-S0-WHAT-COUNTS-AS-EVIDENCE]] fixes what a state claim would have to
beat.
