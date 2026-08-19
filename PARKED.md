# Parked

Last updated: 2026-08-18

**Ideas deliberately excluded from the active program, written down rather than built around.**

This file exists so that an interesting thought has somewhere to go that is not the codebase. Under
[[CHARTER]] §5, an experiment whose `QUESTION` field is empty does not run — it lands here. Under
§10, this is the only place a non-queued idea may live.

**Parked means parked. This is not a backlog and not a queue.** Nothing moves from here to
[[CHARTER]] §9 without meeting the nine-field gate. Most items here carry the reopening condition
**"requires a new charter"**, which means exactly what it says: a new research question with its own
admissible space and its own gate, not an amendment to this program.

---

## 0. The mandate — parked 2026-08-18, and it is parked as MOTIVATION, not as work

The portfolio this research was originally started for is long equities and stays long — SPY, QQQ,
international developed and emerging, effectively XEQT/VT. Nothing ever recommends selling the core.
Three things a good answer was meant to buy: cap drawdown depth, smooth the path, stay invested.

Stated as mathematics, "permanently long" is two conditions, and the formalisation is worth keeping
because it took a program to arrive at:

```
(C1)  N_core(t) is non-decreasing in t                  the core is never sold
(C2)  dV/dS_T = N_core  for all S_T above some S*       upside slope preserved
```

C2 is the load-bearing one: an admissible intervention buys **asymmetry**, not exposure reduction. It
excludes short futures and delta overlays (letter-legal, economically a sale), variance targeting on
equity weight, and put spreads, whose payoff flattens exactly in the tail the program existed to
insure.

**Why this is parked rather than in the charter.** The reason anyone cares whether return states
exist is that the risk/reward of remaining fully exposed might change across them. **That sentence
contains an exposure decision.** Sitting in the charter it would make every experiment get read
against an intended intervention, which is how the last two programs ended up where they did
([[CHARTER]] §7). It lives here, visible, and it governs nothing.

**What would unpark it:** a new charter, written only if the return-state program reaches an S5
ending with states that are real, persistent and identifiable in real time.

## 1. Parked from the intervention program's closure (2026-08-18)

**All of these require a new charter.** They are not future work, and none of them is a "next
experiment" — each was downstream of a claim that no longer stands.

| item | what it was | why it does not run |
|---|---|---|
| **E3 — clairvoyant bound at 26w/52w** | the last open corner of the *prediction* question, at the tenors the structure map said mattered | its own stub conceded the 52w answer is undecidable at 33 decisions in 33 years, and the prediction question is closed. **CLOSED, not parked** |
| **E5 — surface shape as a bounded sensitivity** | procurement: what the protection actually costs, rejection-only | procurement for a purchase that is no longer being considered |
| **E6 — specify `rho`, measure `kappa`** | the monetisation rule, and the precondition for interpreting any drawdown magnitude | there are no drawdown magnitudes being quoted |
| **E7 — additive convex sleeve at matched outlay** | the instrument comparison that was never run | instrument comparison is across the firewall by definition |
| **Ladders, horizon-scaled moneyness, matched-budget comparison, optimal tenor as a convex program, monetisation as optimal stopping** | five refinements of the structure grid | all are optimisation inside a space whose effect did not survive identification |
| **Deductible size as the live axis** | E4 made `m`, not tenor, the variable M1 actually depends on | it is an economic question the moment it is asked seriously, and E4 pays no premium |
| **Tax, currency, drawdown-duration objective** | decision-layer inputs and an unstated objective | they depend on account structure and on a preference, neither of which is a research fact |

**Conditioning on decline shape is parked as UNAVAILABLE, and this is the most important row in the
file.** E4 showed M1 wins persistent grinds and loses V-shapes, so a rule choosing tenor by the
coming decline's shape would capture it. **This is the closed prediction programme wearing a
different hat.** Knowing whether a decline will grind or V-bottom, at the moment the contract is
bought, is a forecast of exactly the kind F1/F2 closed. It is listed so that "E4 found a conditional
effect" is never read as "so condition on it". **Nothing unparks it.** It is also the worked example
the charter cites: a conditional finding is not a rule.

## 2. Parked from the return-state transition (2026-08-18)

| item | why parked | what would unpark it |
|---|---|---|
| **Sample definition.** `SUBSAMPLE_START = 2003-01-24` is the closed model's 520-week burn-in, inherited by the archived modules for no active reason | it is weekly, and the active program is daily. Any active experiment declares its own sample in its stub, with a reason | nothing — it is an archived constant now. A new sample choice is a stub field, not an unparking |
| **`RELIABLE_MIN_OBSERVATIONS = 520`** | a weekly figure with no daily equivalent measured (U5) | it becomes a live question the moment an experiment needs a minimum daily history, and is answered **inside that stub**, not here |
| **The absorption ratio, breadth, cross-sectional dependence as *state characteristics*** | genuinely candidate descriptors under [[CHARTER]] §1, and equally genuinely the place where F4/F5 already failed once — the absorption ratio's expanding-percentile trigger fired 76.9% of weeks in 2004–06 and 4.0% in 2018–26, governed by accumulated history rather than markets | Q2, and only after Q1 returns. Any use must be as a **characteristic** measured on a fixed window, never as a percentile trigger, and must state effective n per coordinate |
| **S4 — skewed heavy-tailed regime densities, as the paper** | the D3 + dynamics negative plus the PIT asymmetry is publishable and needs no new data. It is writing, not research | it is available to write at any time; it does not enter the queue because it produces no new finding |

## 3. Parked from the closed programs — reclassified, not reopened

These are **not** revivals. Each is a different *use* of material a closed program touched, listed so
the distinction stays visible.

| item | the closed use (stays closed) | the reclassified use |
|---|---|---|
| **The option surface** | a predictor of realized risk, or a search for mispricing | **nothing in the active program.** Reclassified once already, as procurement (E5); that use closed with the intervention branch. Requires a new charter |
| **Cross-market data** | a joint information set for a signal | **independent replication samples**, which is what [[CHARTER]] S2 requires. The `^GSPC` 1927+, `^N225`, `^FTSE` and `^GDAXI` series obtained for E4 are retained for exactly this. No signal, no information set, no forecast |
| **The walk-forward MS pipeline** | a real-time risk estimate to size an overlay | **one candidate representation** of latent state, to be audited against the new question rather than revived. It is archived; if a return-state experiment needs a switching model it is written fresh under [[CHARTER]] §10's last clause |

## 4. Permanently closed — do not park, do not reopen

Listed only so that "it is not in PARKED" is never read as "it is available."

Prediction of forward risk from public return-volatility estimators (F1, F2), the h=1 EWMA comparison
(F10), GARCH encompassing as a *prediction* test (F11), within-regime ARCH (S3), the memory-shape
question (F3, U6), the absorption ratio as a trigger (F4, F5), all trigger rules (F9), the
Hamilton-filter recovery board and its six items, **Item 5 and its three resolutions**, and
**conditioning tenor on decline shape** (§1 above).

**One clarification, because the boundary is thin.** F11 closed GARCH encompassing as a test of
whether regimes add *predictive* information over a smooth-reverting model, and it closed as
UNINFORMATIVE because ARCH-LM rejects at 55.6 *after* regime-switching, so a null is confounded by
known misspecification. A smoothly-reverting conditional-scale process is now the active program's
**null** ([[CHARTER]] D1), which is a different role: it is the object a state claim must beat, not a
rival forecaster being scored. The distinction must be stated in any stub that uses it, and a stub
that blurs it is running F11 again.

Evidence and reasoning: [[docs/PROBLEM-MAP]] Part II. Code:
[[closed-research/README]] · [[closed-research/intervention/README]].

## Related

- [[CHARTER]] — the active program · [[docs/PROBLEM-MAP]] — the evidence base
