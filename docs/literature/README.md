# Reading list — a gate, not a list to admire

Last updated: 2026-08-18

Protocol §0 rule 3: **name the paper that already settles this, or state in writing that none does.**
A finding rediscovered empirically that was already in a cited paper is a process failure and gets
logged as one. That has happened here once — Timmermann's Proposition 5 was derived from scratch while
sitting `[UNREAD]` as row 2 of the closed program's list, whose own reading-order note said what it
contained.

**Status tags:** `[READ]` in full · `[skim]` enough to use · `[UNREAD]` obtained, not read ·
`[WANTED]` not obtained.

The closed program's reading list is preserved at
[[closed-research/docs/literature/README]] and is not maintained.

---

## Blocking — these gate a queued experiment

| paper | status | gates | why |
|---|---|---|---|
| **Israelov (2017), "Pathetic Protection"** | `[skim]` 2026-08-18 — obtained, and the sections that gate E0/E1 read in full | **E0 (closed), E1 (open, and redesigned by it)** | **It does NOT decompose mark versus realized** — zero occurrences of mark-to-market, unrealised or monetise in the text; every drawdown it reports is computed on a marked NAV. So E0's design stood. What it *does* contain is E1's mechanism and E10's ordering — see below | PDF local in this directory, gitignored by policy |
| **Chekhlov, Uryasev & Zabarankin (2005), "Drawdown measure in portfolio optimization"** | `[UNREAD]` | **E2** | The CDaR definition, its coherence and its convexity. `pathfunctionals.cdar` implements it from the definition; confirm the convention (occupation measure vs. sample quantile) before quoting numbers |
| **Ilmanen (2012), "Do financial markets reward buying or selling insurance and lottery tickets?"** | `[UNREAD]` | E5, E7 | The skeptical prior on paying for index protection. E9 is consistent with it; check whether the magnitude is too |

**What Israelov (2017) settles, and the process failure it exposes.** Read 2026-08-18, after E0
had already run — the gate was skipped, and it is logged here as a process failure under §0 rule 3,
the second in this repo's history.

- **It does not touch E0's question.** Drawdowns are computed on the marked NAV of the Cboe PPUT
  index and of simulated protected portfolios. The mark-versus-cash distinction never appears.
  E0 was not a rediscovery.
- **It already contains E10's tenor ordering.** It sweeps 20 / 63 / 250 business-day maturities —
  our 4w / 13w / 52w — and concludes: *"longer-dated options do a less bad job of protecting a
  portfolio against long-term drawdowns than shorter-dated options. Less bad, but not good."*
  **That is E10's ordering and E0's cash magnitude, in a paper that sat `[UNREAD]` as row 1 of
  this list while both were derived empirically.** Our contribution is the decomposition, not the
  ordering.
- **It already contains E1's mechanism, and states it as the paper's central explanation:** *"A
  put option's protective armor is nearly impenetrable over drawdowns that coincide with its
  option expiration cycle. Unfortunately, equity drawdowns have lives of their own that may not
  conveniently coincide with option expiration cycles."* Also: *"The maximal benefits for each
  maturity tend to occur for measurement periods that are most closely aligned with option
  lifespans."* **Under §0 rule 2 this changes E1**: that phase matters is now cited, not tested,
  and E1 must be respecified around the quantity the paper does not give — the *phase spread*
  relative to the effect, which is a `Psi` coordinate ([[CHARTER]] §3, H2).
- **Its remedy is inadmissible here.** The paper's comparison alternative throughout is static
  divestment — 36.5% equity, 63.5% cash, matched to PPUT's realized return. [[CHARTER]] §2's C2
  excludes exactly that. **So its headline verdict does not bind this mandate, while its mechanism
  findings bind it completely.** The permanent-long constraint is what makes the paper's
  conclusion unavailable and its evidence still relevant.
- **One design convention worth noticing:** it scales moneyness to maturity (4.8% / 9.2% / 18.2%
  for 20 / 63 / 250 days, each set to the median drawdown over that horizon) rather than holding
  the strike fixed across tenors as our grid does. Parked, not queued — see [[PARKED]].

## Core to the objective space

| paper | status | why |
|---|---|---|
| Magdon-Ismail & Atiya (2004), "Maximum drawdown" | `[WANTED]` | The distribution of MDD, and the formal statement that one path is one observation of it. Would let the n=1 claim be quantitative rather than argued |
| Grossman & Zhou (1993), "Optimal investment strategies for controlling drawdowns" | `[WANTED]` | Portfolio choice under a drawdown constraint. The closest existing formalization of this mandate |
| Cvitanić & Karatzas (1995), "On portfolio optimization under drawdown constraints" | `[WANTED]` | The continuous-time treatment |
| Carr, Zhang & Hadjiliadis (2011), "Maximum drawdown insurance" | `[WANTED]` | Pricing protection on the drawdown *itself* rather than on the price. Directly the object this project wants, and it may say the instrument choice is wrong |

## Method, carried from the closed program

| paper | status | why it still binds |
|---|---|---|
| Howard (1966), EVPI | `[skim]` | The clairvoyant bound in `simulate(foresight=True)`. Search-independent, and the strongest construction the repo owns |
| Politis & Romano (1994), stationary bootstrap | `[WANTED]` | Only to state precisely what block resampling *cannot* do here — see [[CHARTER]] §9's demotion. Read before anyone proposes it as evidence for a magnitude |

## Deliberately not read

The closed program's list — Hamilton & Susmel (1994), Marcucci (2005), Rydén, Teräsvirta & Åsbrink
(1998), Calvet & Fisher, Corsi, Kritzman et al. — is not on this list. Those papers gate experiments
that are closed. Reading them would be interesting and would move nothing; under protocol §0 rule 5
that makes it decoration.
