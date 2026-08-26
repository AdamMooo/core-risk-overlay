# Reading list — a gate, not a list to admire

Last updated: 2026-08-26

Protocol §0 rule 3: **name the paper that already settles this, or state in writing that none does.**
A finding rediscovered empirically that was already in a cited paper is a process failure and gets
logged as one. That has happened here once — Timmermann's Proposition 5 was derived from scratch while
sitting `[UNREAD]` as row 2 of the closed program's list, whose own reading-order note said what it
contained.

**Status tags:** `[READ]` in full · `[skim]` enough to use · `[UNREAD]` obtained, not read ·
`[WANTED]` not obtained.

**Status 2026-08-18: this list gated the CLOSED intervention program.** Every row below is retained
as evidence — including the process failure it logs — and **no row is a blocking gate any more**,
because the experiments they gated are closed. The return-state program starts a new list when its
first experiment needs one; until then a list of papers is an agenda, and this repository has
learned what an unowned agenda does.

The prediction program's reading list is preserved at
[[closed-research/docs/literature/README]] and is not maintained either.

---

## Blocking now — the SJM reproduction and the present-state assessment (added 2026-08-25)

These rows gate live work. Nothing else was added, deliberately: the assessment's own literature
table ([[docs/ASSESSMENT-PRESENT-STATE-RISK]] §3) holds the context papers (Moreira-Muir, Cederburg
et al., Bollerslev-Tauchen-Zhou, Kritzman) whose experiments have already run — duplicating them
here would be the agenda this file warns about.

| paper | status | gates | why |
|---|---|---|---|
| **Shu, Yu & Mulvey (2024), "Downside Risk Reduction Using Regime-Switching Signals"**, J. Asset Management 25(5), arXiv 2402.05272 | `[READ]` — v3 read directly 2026-08-24 for the fidelity audit; PDF local as of 2026-08-25 | the whole reproduction — [[docs/REPRO-SJM2024-FINDINGS]] | the object under reproduction. The fidelity audit, the D1–D8 deviation register and the critique of its own weaknesses all live in the findings doc, not here |
| **Lunde & Timmermann (2004), "Duration Dependence in Stock Prices"**, JBES 22(3):253–273; UCSD working-paper PDF local | `[UNREAD]` — obtained 2026-08-25 | **Screen 1a** ([[docs/ASSESSMENT-PRESENT-STATE-RISK]] §11a) | establishes that bull/bear regime hazard depends on age — but on Bry-Boschan-style directional regimes, not an RV band, and the **sign and shape of each hazard must be read from the primary before 1a's result is interpreted**; search-snippet knowledge of it disagreed with itself on the bull-hazard direction |
| **Xie, "Asset Pricing Implications of Volatility Term Structure Risk"**, SSRN 2517868 | `[WANTED]` — **unobtainable**: SSRN 403s direct fetch, the citeseerx mirror redirects to an archive that is also unreachable | **Screen 1b** (§11b) | the regime-switching disaster model in which VIX term-structure slope prices expected disaster *length* — the mechanism behind 1b's null. Only the abstract-level claim is used, stated as such in §11, per the [[CHARTER]] §9.2 precedent for an unobtained source |
| **Ledoit & Wolf (2008), "Robust performance hypothesis testing with the Sharpe ratio"**, JEF 15(5):850–859; publisher PDF local | `[READ]` in full 2026-08-26 — §§2–3.2.2 and Remark 3.2 are the implementation | **the shallow half of the inference run**, open item 6 of [[docs/REPRO-SJM2024-FINDINGS]] | it *is* the test, not a citation for one: studentized circular block bootstrap on the Sharpe difference, prewhitened-QS HAC standard error, p-value by their Eq. (9). Jobson–Korkie/Memmel is invalid on daily equity returns because Ω assumes i.i.d. normal pairs (§2) |
| **Politis & Romano (1994), stationary bootstrap** | `[WANTED]` — **unobtainable**: JASA paywalled, no author or mirror copy of the original found | **the block bootstrap**, open item 6 of [[docs/REPRO-SJM2024-FINDINGS]] | **gate discharged on substitutes, 2026-08-26**, per the [[CHARTER]] §9.2 precedent for an unobtained source. What the gate needed — what block resampling cannot license, and how the block length is chosen rather than tuned — is in the two rows below, both by the same author and both read. The demotion note in the closed intervention charter still binds |
| **Politis (2003), "The impact of bootstrap methods on time series analysis"**, Statist. Sci. 18(2):219–230; PDF local | `[skim]` 2026-08-26 | the same gate | the author's own review of the block/stationary bootstraps and their validity conditions — the substitute for the 1994 original on *what the method assumes* |
| **Politis & White (2004), "Automatic block-length selection for the dependent bootstrap"**, Econometric Reviews 23(1):53–70 (with the Patton–Politis–White 2009 correction); PDF local | `[skim]` 2026-08-26 | the same gate | the substitute for the 1994 original on *choosing* the block length. Used in the inference run as a **reported reference point only** — the preregistered rule is the max-p over a declared grid, so that no block length is selected on the outcome |

## Was blocking — these gated experiments that are now closed

| paper | status | gates | why |
|---|---|---|---|
| **Israelov (2017), "Pathetic Protection"** | `[skim]` 2026-08-18 — obtained, and the sections that gate E0/E1 read in full | **E0 (closed), E1 (open, and redesigned by it)** | **It does NOT decompose mark versus realized** — zero occurrences of mark-to-market, unrealised or monetise in the text; every drawdown it reports is computed on a marked NAV. So E0's design stood. What it *does* contain is E1's mechanism and E10's ordering — see below | PDF local in this directory, gitignored by policy |
| **Chekhlov, Uryasev & Zabarankin, "Portfolio optimization with drawdown constraints" (2000 working paper of the 2005 IJTAF article)** | `[skim]` 2026-08-18 — **read BEFORE E2, as the register required** | **E2 (gate closed)** | It settled the convention and the answer was not the expected one: **their `alpha` is a confidence level and ours is the fraction averaged, so the two are complements.** Also: the discrete estimator is the upper CDaR when `alpha*N` is not integer; convexity is in the portfolio weights and licenses nothing here; and the authors themselves scope CDaR to a *single sample path*, leaving the multi-path case open — which agrees with this repo's identification stance. [[MATH-REFERENCE]] §4.1 | PDF local, gitignored |
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
  relative to the effect, which is a `Psi` coordinate ([[closed-research/intervention/CHARTER-INTERVENTION|CHARTER-INTERVENTION]] §3, H2).
- **Its remedy is inadmissible here.** The paper's comparison alternative throughout is static
  divestment — 36.5% equity, 63.5% cash, matched to PPUT's realized return. [[closed-research/intervention/CHARTER-INTERVENTION|CHARTER-INTERVENTION]] §2's C2
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
| Politis & Romano (1994), stationary bootstrap | `[WANTED]` | Only to state precisely what block resampling *cannot* do here — see [[closed-research/intervention/CHARTER-INTERVENTION|CHARTER-INTERVENTION]] §9's demotion. Read before anyone proposes it as evidence for a magnitude |

## Deliberately not read

The closed program's list — Hamilton & Susmel (1994), Marcucci (2005), Rydén, Teräsvirta & Åsbrink
(1998), Calvet & Fisher, Corsi, Kritzman et al. — is not on this list. Those papers gate experiments
that are closed. Reading them would be interesting and would move nothing; under protocol §0 rule 5
that makes it decoration.
