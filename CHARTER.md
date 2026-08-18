# Charter — Drawdown Intervention Design

Adopted 2026-08-17. **This is the only active research program in this repository.**

The program it replaces is closed and preserved at [[closed-research/README]]. The reasoning that
produced the transition is recorded as a dated amendment in [[docs/PROBLEM-MAP]].

---

## 1. The research question

> **Under a permanent-long constraint, which features of the book's drawdown geometry are
> demonstrably alterable by an admissible intervention; which of those alterations are identified in
> magnitude from available data; and at what cost — with "not identified" treated as a legitimate
> result rather than a gap to be filled by assumption.**

Not "which hedge is best." The question is what is *purchasable*, what is *knowable*, and what is
neither.

**Identification first, optimization second.** The closed program's failure was not carelessness —
it measured extremely carefully. It optimized inside a space it had never identified. A ranking built
from a single realized path is an in-sample ranking however rigorous the arithmetic, and calling it a
frontier does not change that.

## 2. Admissible interventions

The permanent-long constraint stated as mathematics. A share-count condition alone is vacuous — a
short futures overlay satisfies it and is economically a sale. Two conditions are needed:

```
(C1)  N_core(t) is non-decreasing in t                  no sale of the core
(C2)  dV/dS_T = N_core  for all S_T above some S*       upside slope preserved
      where V(S_T) is terminal wealth as a function of the core's terminal price
```

C2 is the load-bearing one: **an admissible intervention buys asymmetry, not exposure reduction.**

| candidate | C1 | C2 | verdict |
|---|---|---|---|
| long put | ok | ok | **admissible** |
| put spread | ok | **fails** — payoff flattens below the short strike | inadmissible. C2 reproduces F12 *a priori* |
| short futures / delta overlay | ok | **fails** — slope reduced everywhere | inadmissible; letter-legal, economically a sale |
| variance targeting `w_equity` down | **fails** | fails | inadmissible at the level of the state variable |
| additive convex sleeve (trend, duration, gold) | ok | ok | **admissible** |
| monetize the hedge, buy shares | ok (raises `N_core`) | ok | **admissible, and required by the mandate's own value story** |

**The space.**

```
I_opt    = { (tau, m, phase, h, rho) }    tenor, moneyness, roll phase,
                                          notional, monetisation rule
           consumes premium from the hedge sleeve

I_sleeve = { additive convex sleeves }
           consumes capital from the hedge sleeve

I = I_opt  union  I_sleeve
```

Comparable **only at matched cash outlay from the hedge sleeve**, with outlay reported as a
coordinate rather than held equal by assumption. The current grid compares at matched *notional*,
which is a weaker equalization.

**Not in the space, and why.** *New-capital deployment rate* is a different problem: its magnitude
scales with (inflow / AUM), a personal parameter rather than a market one. *Monetisation* is not a
standalone intervention — it is a coordinate `rho` of every structure, and a structure quoted without
one is underspecified.

## 3. The objective space

Given marked wealth `W(t)`, running maximum `M(t) = sup_{s<=t} W(s)`, drawdown `D(t) = 1 - W(t)/M(t)`:

```
Phi(I) = ( g              geometric growth rate -- participation
           premium_drag   decomposition of g, well sampled (~1700 rolls)
           CDaR_alpha(.)  drawdown depth as a CURVE in alpha, not a point
           {depth_i}      per-excursion depths -- the robustness object
           U_theta        time under water: "smooth the ride", made measurable
           R              recovery-time distribution
           kappa )        shares purchasable at the trough under a stated rho
```

`kappa` is the mechanism by which drawdown reduction becomes future compounding. Without it,
"recycled into the core at lower prices" is a sentence with no referent.

**Excluded by construction, each for a stated reason.** Annualised volatility — symmetric, and the
mandate never asked for it. Sharpe — same. Hedge efficiency — F7: the denominator goes to zero, so a
structure protecting nothing scores best. **Max drawdown as a ranking key** — an extreme-value
functional with effective n = 1 on one path.

**Diagnostics travel with every row and never enter `Phi`:**

```
Psi(I) = ( phase spread, pricing sensitivity, episode sign-consistency,
           effective n per coordinate )
```

`Phi` is *how good is this*. `Psi` is *how well do we know it*. Conflating them is exactly how
"efficiency 218.23 at a cost of 0.03pp/yr" happened.

## 4. Falsifiable hypotheses

**No active hypothesis may assert a numerical effect magnitude as though it were identified when the
underlying population is not identified.** Orderings, signs and falsifications only. This is the most
important lesson carried out of the closed program.

| | hypothesis | kill condition | assumption cost |
|---|---|---|---|
| **H1** | Strike anchoring (M1) dominates re-striking for a multi-month drawdown at equal premium budget | ordering flips in >= 1/3 of episodes | **price paths only.** No option data |
| **H2** | The tenor ordering survives on `CDaR_alpha` and per-excursion depths, and the phase spread is small relative to the effect | **PHASE CLAUSE RESOLVED 2026-08-18 (E1): KILLED in cash** (R = 1.85 and 6.82), **MARGINAL in marks** (0.71, 0.85), never SURVIVES. The *ordering* holds at 56 of 56 alignments in marks and is alignment-dependent in cash. The excursion clause is still open and belongs to E2 | free |
| **H3** | ~~M3 is not the dominant source of the measured drawdown reduction~~ **REJECTED 2026-08-18 (E0)** — the gap is 82% (1993–) and 85% (2003–) of the 52w reduction, and exceeds the reduction entirely at 13w | marked-versus-cash gap exceeds half the measured reduction | free |
| **H4** | Timing value at 26w and 52w does not exceed the 4w/13w EVPI ceiling | it materially exceeds it — in which case the branch is *undecidable* at n=33, not open | one line |
| **H5** | The long-tenor cost advantage is not an artifact of `sqrt(4/tenor)` or a tenor-flat spread | a plausibly steeper long-tenor skew reverses the cost ordering. **Asymmetric: rejection clean, confirmation impossible** | archived chains |
| **H6** | The measured reduction is realizable under a stated `rho`, not only marked | `kappa` under the rule is less than half the marked reduction | a policy |
| **H7** | An additive convex sleeve reaches a robustly non-dominated point at matched outlay | dominated on every coordinate of `Phi` | one or two price series |

## 5. Identification assumptions, declared in advance

- **Episodes are not draws from a superpopulation.** Market structure, monetary regime, index
  composition and the depth of the listed options market all differ across 1987, 2000-02, 2008-09,
  2020 and 2022. Cross-episode work establishes **robustness of a mechanism** and can **falsify** a
  magnitude. It cannot **estimate** one. The entitled inference is binomial and conditional on our own
  episode definition.
- **Historical option costs are not identified**, and cannot be made so. The chain archive begins
  2026-08-14.
- **`max_drawdown` has no sampling distribution on one path.** On this sample it is set by one
  episode, and the 1993- and 2003- samples share it entirely.
- **Tax, currency and long-tenor liquidity are unmodelled terms with stated signs.** Tax on
  monetisation and wider long-tenor spreads point against the hedge; USD strength in a crisis, which
  raises a USD put's CAD value exactly when needed, points for it.

## 6. Robust non-dominance

A point is admissible to the frontier only if it dominates **at every roll phase, across the full
pricing sweep, on `CDaR_alpha` rather than max drawdown, under a stated `rho`, at matched outlay, with
per-episode sign consistency above a preregistered threshold.** Anything weaker is reported as
*conditionally better under assumptions A*, with A enumerated.

**The robust set may be empty, or it may be most of the grid. Either is a finding.**

## 7. The research / decision firewall

**Research may establish:** mechanism, ordering, robustness, identified quantities, unknown
quantities.

**Research may not establish:** *therefore allocate x%.*

That belongs downstream and there is no `decision/` directory yet, deliberately — an empty directory
is an invitation to fill it. Preference ordering, sizing, account and tax structure, and whether
anything goes live are the decision layer's, and it is created when it has contents.

**Dominance requires no preferences at all.** A point is dominated if another is at least as good on
every coordinate; that is a fact about the world. Preferences are needed only to select *among*
non-dominated points, and if the robust set turns out thin they barely matter. So: build the frontier,
publish the dominated set, and ask for a preference only if several non-dominated points survive.

## 8. The gate — seven fields, and no code before they are filled

Extends the closed program's five-field stub, which is the best process asset it produced.

```
1. CLAIM TUPLE        (frequency, horizon, functional, sample)
2. PREDICTED OUTCOME  with its reason, before any code. Confidently derivable
                      from theory -> the run carries no information; do not run it.
3. LITERATURE         name the paper that settles this, or state that none does.
4. MECHANISM          the structural difference, the horizon AND the functional
                      at which it becomes observable. Invisible in either -> void.
5. SURPRISE           the outcome that would move a decision. None -> decoration.

6. BOUNDARY           which of the six does this move?  identification /
                      mechanism validity / robustness / realizability /
                      economic comparability / frontier.
                      BOUNDARY = empty  =>  DO NOT RUN. It goes in PARKED.md.

7. IDENTIFICATION     what population the claim addresses, what is identified in
                      magnitude, what is not. "Not identified" is a permitted
                      answer and is written BEFORE the run.
```

## 9. The experiment queue

**One queue. No parallel programs. Each experiment must be capable of killing the next.**

**E0 closed 2026-08-18 and it killed a magnitude rather than an experiment** — which is what §9 was
built to allow. The queue order is unchanged; what changed is that E6 now gates the interpretation
of every row above it, and E1 inherited E0's urgency.

**E1 closed 2026-08-18 and triggered nothing automatically.** E2 and E3 stand where they were;
what runs next is an open decision, deliberately not taken inside the experiment that preceded it.

| | experiment | why here |
|---|---|---|
| **E0** | ~~M3 decomposition~~ **RAN 2026-08-18. H3 REJECTED.** 82% of the 52w reduction is mark; +16.8pp becomes +3.0pp in cash; the cash reduction is flat from 26w to 52w and negative at 4w/13w. [[docs/STUB-E0-M3-DECOMPOSITION]] | It ran first, and it was right to. Every magnitude in the repo now carries an accounting label, and E6 stopped being optional |
| **E1** | ~~Roll-phase sweep~~ **RAN 2026-08-18. H2's phase clause killed in cash, marginal in marks.** In cash the *sign* of the 52w result is set by the roll calendar (−6.3 to +7.8pp). Phase is now a declared coordinate of every row. [[docs/STUB-E1-ROLL-PHASE]] | it cost one parameter and removed a magnitude the repo had published for three days |
| **E2** | Per-excursion depths and the `CDaR_alpha` curve | free; the sample-size problem becomes an output |
| **E3** | Clairvoyant bound at 26w and 52w (`TENOR_WEEKS`) | one line; closes or renders undecidable the old program's last open corner |
| **E4** | M1 payoff-only anchoring test, S&P 1927+ and cross-market | the only real escape from one episode; needs no option data |
| **E5** | Surface shape as a bounded sensitivity, rejection only | procurement, firewalled from any forecasting use |
| **E6** | Specify `rho`, then measure `kappa` — **reclassified by E0 from queued experiment to PRECONDITION.** The marked-versus-cash interval is wider than the effect inside it, so no drawdown magnitude is interpretable until a rule is stated | the mandate's value story, never once implemented |
| **E7** | Additive sleeve at matched outlay | the instrument comparison never run |

**Block bootstrap is explicitly demoted.** With block length far below crisis length it shatters the
path dependence drawdown is made of; near crisis length it resamples the same episode as a unit. It
manufactures pseudo-replications of one path and cannot create a second independent crisis. Admissible
only as a *stated* variance estimate under block-scale exchangeability, never as evidence for a
magnitude.

## 10. Scope discipline

**The codebase must make scope creep harder, not easier.**

- A new idea passes charter, boundary, identification and preregistration **before** it gets code.
- An interesting idea that does not belong goes in [[PARKED]], written down rather than built around.
- A closed idea goes in `closed-research/` and does not come back without meeting its own stated
  reopening condition.
- An experiment appears in **exactly one** queue — §9 above.
- No orphan TODOs. No "we should also test" branches accumulating quietly.

## Related

- [[README]] — the mandate · [[docs/PROBLEM-MAP]] — evidence base and the transition amendment
- [[docs/RESEARCH-PROTOCOL]] — the gate and the standing principles
- [[docs/POINT-IN-TIME-DISCIPLINE]] — the leak register, including this program's own channels
- [[docs/MATH-REFERENCE]] — path functionals · [[PARKED]] — deliberately excluded
- [[closed-research/README]] — the completed prediction program
