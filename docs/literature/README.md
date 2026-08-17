# Reading list — a gate, not a list to admire

Last updated: 2026-08-17

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
| **Israelov (2017), "Pathetic Protection"** | `[UNREAD]` | **E0, E1** | On rolled-put drag specifically, which is the exact construction `simulate` implements. If it already decomposes mark versus realized, E0's design changes. **This is the single highest-priority read in the repo** — it is the paper closest to the next experiment |
| **Chekhlov, Uryasev & Zabarankin (2005), "Drawdown measure in portfolio optimization"** | `[UNREAD]` | **E2** | The CDaR definition, its coherence and its convexity. `pathfunctionals.cdar` implements it from the definition; confirm the convention (occupation measure vs. sample quantile) before quoting numbers |
| **Ilmanen (2012), "Do financial markets reward buying or selling insurance and lottery tickets?"** | `[UNREAD]` | E5, E7 | The skeptical prior on paying for index protection. E9 is consistent with it; check whether the magnitude is too |

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
