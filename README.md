# Core-Risk-Overlay

Last updated: 2026-08-18

A research program on **drawdown intervention design** for a permanently long, globally diversified
equity book: which features of the book's drawdown geometry can be purchased, which of them are
identified from the data available, and at what cost.

- **The active program — question, admissible space, hypotheses, experiment queue:** [[CHARTER]]
  (**read first**)
- **Evidence base, and why the previous program was closed:** [[docs/PROBLEM-MAP]]
- **Process — the gate every experiment passes:** [[docs/RESEARCH-PROTOCOL]]
- **Mathematics:** [[docs/MATH-REFERENCE]] · **Time basis and leak register:**
  [[docs/POINT-IN-TIME-DISCIPLINE]]
- **Deliberately excluded:** [[PARKED]] · **Chronological log:** [[core-risk-overlay]]
- **The completed prediction/regime program:** [[closed-research/README]] — closed research, preserved
  and reproducible, **not an active branch**

---

## 1. The mandate

The portfolio is long equities and stays long — SPY, QQQ, international developed and emerging,
effectively XEQT/VT. Nothing here ever recommends selling the core.

Three things a good answer buys: **cap drawdown depth, smooth the path, stay invested.**

### 1.1 What "permanently long" actually constrains

Stated as mathematics, because as prose it turned out to be ambiguous enough to admit an intervention
it was meant to exclude. A condition on share count alone is vacuous — a short futures overlay
satisfies it and is economically a sale. Two conditions are needed:

```
(C1)  N_core(t) is non-decreasing in t                  the core is never sold
(C2)  dV/dS_T = N_core  for all S_T above some S*       upside slope preserved
```

**C2 is the load-bearing one: an admissible intervention buys asymmetry, not exposure reduction.** It
admits long puts, additive convex sleeves, and monetising a hedge to buy more shares. It excludes
selling the core, delta overlays that replicate selling, variance targeting on equity weight, and — as
it happens — put spreads, whose payoff flattens exactly in the tail the program exists to insure.

**What the constraint is for.** It is a **pre-commitment device**: it removes discretionary timing from
the choice set, which is what makes a negative-expected-value insurance purchase a coherent decision
rather than a bet. It is also a friction minimiser (one-time FX conversion, no realized gains on the
core). It is *not* a belief that equities always rise. Tested by removal: without it the problem becomes
dynamic asset allocation on public data, and this repo's own evidence says it has no edge there. **The
constraint is what makes the problem small enough to have a positive answer.**

## 2. What the overlay is, and what it is not

**It is a purchase.** A put program buys a different path of portfolio outcomes at a cost in
compound return. That is the honest frame and it is where the measurements point.

**An earlier version of this file argued otherwise**, and the argument is withdrawn. It held that
truncating the left tail raises the geometric return *provided premium drag is smaller than the
drawdown avoided*, and treated that proviso as the project's premise. The proviso was measured for the
first time on 2026-08-15: **0 of 40 structures beat the naked book on compound return, in both
samples.** The inequality fails on average at every point tested. That is not a failure of the program —
it is price discovery, and it reframes the question from *does this pay* to *what does this cost and is
the path it buys worth that*.

**Two things it is not, both considered and rejected on page one, both still rejected:**

- **Predicting drawdowns.** Roughly 10-15 systemic drawdowns in all of SPY history, heavily
  overlapping. No model learns a rare, path-dependent label from a dozen examples.
- **Out-pricing the option market.** That needs a fair-value model better than the market's, plus chain
  depth, execution infrastructure and a market-maker's information set. We have none of them, and
  acquiring them is not this project. **Using the surface to know what protection costs is a different
  activity** — procurement, not prediction — and is admissible on that footing only.

## 3. What the previous program established, scoped precisely

The repository spent its first phase asking whether a real-time latent-state model of volatility could
say *when* to scale a standing overlay. That program is **closed**, and the closure is worth stating
carefully in both directions.

**What is established.** The model's forward-downside information is strictly nested inside VIX's, on
levels (`c = +0.0009`, `p = 0.99`; joint R² equal to VIX-alone to four decimals) and on dynamics (adds
0.0004 of R², with power demonstrated rather than assumed). Independently, the clairvoyant bound caps
what *any* timing rule could be worth at roughly +3pp/yr at the tenors tested, and real rules captured
4-7% of it. The measurement itself is honest and characterised: a **width meter** separating realized
volatility ~2.4x out of sample, carrying no direction content, and reading "wide" when the book is
already ~13% below its running peak.

**What is not established, and must not be claimed.** That no predictive edge exists. The closure covers
one family — **public return-volatility estimators** — for **decision** purposes, on **SPY**, against
**VIX**, on forward downside semivolatility at h=4 and h=13. Credit, funding, breadth and positioning
were never tested. They are **out of scope, not refuted.** And the clairvoyant bound was computed only at
4 and 13 weeks, which the structure work suggests are the wrong tenors; closing that corner is a queued
experiment ([[CHARTER]] E3), not a settled fact.

**The diagnosis that matters most for what came next.** The variable that dominated outcomes — option
tenor — had been fixed by assumption in the original plan, while the variable that turned out to be
nearly worthless got the research. The failure was in what was held constant, not in how carefully
anything was measured.

## 4. Capital plumbing (Canadian framework)

Two sub-accounts, to avoid ongoing currency friction:

1. **Core bucket (CAD).** Long-term compounding index assets (VFV, XEQT) or direct blue chips. Never
   sold — C1.
2. **Hedge bucket (USD).** A small dedicated sleeve. CAD converted to USD **once**, via Norbert's
   Gambit or IBKR native conversion, to eliminate repeated spread costs. That USD funds the
   intervention.

**Monetisation is the mandate's stated source of value and has never been implemented.** The claim is:
sell the appreciated hedge in a crash, move the proceeds to the core bucket, buy index exposure at a
discount — which raises `N_core` and is admissible under C1. The simulator holds every position to
expiry instead. Whether the measured drawdown reduction is realizable cash or an unrealized mark was
[[CHARTER]] E0, it ran first as designed, and **the answer is mostly mark**: 82% of the 52-week
reduction on the full sample, 85% on the 2003– subsample. The +16.8pp and +19.9pp headline figures
are **+3.0pp each in cash**, and in the well-sampled `CDaR_alpha` coordinate the full-sample cash
reduction is approximately zero. The mandate's value story is therefore not a refinement to be added
later — it is the precondition for quoting any drawdown magnitude at all ([[CHARTER]] E6). Full
result: [[docs/STUB-E0-M3-DECOMPOSITION]] §9.

## 5. Implementation status

| component | state |
|---|---|
| `src/data_loader.py` | working — daily and weekly returns, VIX, start-date invariant, explicit calendar |
| `research/hedge_economics.py` | working — priced rolled put programs, weekly marks, clairvoyant (EVPI) bound. Carries the two switches E0 and E1 rest on: `mark_hedge` and `phase`. **Benefit-side effective n = 1** |
| `research/structure_map.py` | working — tenor × strike × outright/spread grid, no timing anywhere |
| `research/pathfunctionals.py` | working — drawdown process, excursions, CDaR curve, time under water |
| `research/m3_decomposition.py` | working — E0, the marked-versus-cash accounting decomposition. **H3 rejected 2026-08-18** |
| `research/phase_sweep.py` | working — E1, the roll-phase sweep. **H2's phase clause killed in cash, marginal in marks, 2026-08-18** |
| `research/path_outcomes.py` | working — E2, the CDaR curve and episode-matched depths. **H2 fully resolved 2026-08-18** |
| `checks.py` | 46 checks, all passing — six for the E0 accounting invariant, five for the E1 roll-phase grid, four for E2's window-matched depth |
| `closed-research/` | 81 checks passing; D3 and F2 verified reproducible after the transition |

No live path exists and none is designed. The decision layer — preferences, sizing, tax, whether to run
anything with real money — is downstream of research by construction ([[CHARTER]] §7) and has no
directory yet, deliberately.
