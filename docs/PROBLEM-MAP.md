# Problem Map

Last updated: 2026-08-15

**The objective is unchanged and sits above everything in this file: build an economically valuable
tool.** This document is the route, not the destination — see §0.0.

**What this document is.** The standing answer to *what is the problem, where do we stand, and what
would have to be true for the next piece of research to matter.* It is organised by epistemic status,
not by date. [[core-risk-overlay]] is the chronological log and keeps that job; this file is the
current-state summary and is rewritten in place rather than appended to.

**Why it exists.** Through 2026-08-14 this repo behaved as a signal-discovery engine: an unanswered
question was treated as sufficient reason to build another estimator. Scope reset 2026-08-15 —
**no signal is added unless we can first name the decision it would improve and by how much.**
Sections 5 and 6 are the gate.

**Status: GOVERNING.** Confirmed 2026-08-15. This is the research map. Where it and any other
document disagree about what is worth building, this one wins.

### How to read this

Two parts, doing two different jobs. Do not read them as one list.

| | part | job |
|---|---|---|
| **I** | **§0.0 — the hierarchy** | **What the objective is, and why the board is only the route to it.** Read before §0 |
| **I** | **§0 — the board** | **The forward path. What we are doing next and what it decides.** One screen |
| **II** | §1–§6 — the evidence base | Why the board looks like that, and what must not be rebuilt. **Past evidence prevents repeated mistakes; it does not set the agenda** |

The archaeology in Part II is governance, not clutter — §2 in particular exists so dead ends are not
re-proposed. But the forward plan does not answer to it. A finding that does not constrain the next
decision does not need to be reconciled with.

### Standing rules

1. **No research is added because it is technically available.** Availability is not a reason. The
   §6 gate is: name the decision it improves, and the size of the improvement, *first*.
2. **The branches closed in §2 and §6 stay closed** — GARCH encompassing, S3 within-regime ARCH, S4
   Student-t, MSM/HAR, multi-asset — **unless their own documented reopening condition is actually
   met.** "Structurally valid" is not a reopening condition; it is why they are retained rather than
   deleted. The reopening condition for the signal family is at the end of §6 and is a *quantitative*
   bar, not an argument.
3. **Protection economics and signal economics are reported separately** (§5.0). A result about one
   is never stated in the vocabulary of the other.
4. **Measurement phases do not optimize.** When a run exists to check whether a prior result survives
   a better input, it may not tune against that input while measuring it.
5. **This repo is not accountable to `regime-detection`.** That was a learning ground — jump models,
   k-means, lag experiments — and it lives on GitHub. It is not a dependency, not a closed branch of
   this research, and not a migration risk to be tracked here. **Do not raise it.**
6. **The board is not the objective** (§0.0). Economic value is. If the evidence says the board is
   wrong, or that another path has a better chance of producing economic value, **change the board** —
   at the §6 bar, not on assertion. Rules 1–2 prevent research being *added* on availability; they
   never make the four steps an end in themselves.

---

# Part I — the forward path

*If you read one screen of this document, read this one.*

## 0.0 The hierarchy — what is the objective and what is merely the route

Stated explicitly because the layer below keeps getting mistaken for the layer above.

| level | statement | revisable? |
|---|---|---|
| **Objective** | **Build an economically valuable tool** — a hedge that measurably improves the outcome of a permanently long global equity book | **No.** This is the point of the repo |
| **Research question** | Is there something sufficiently exploitable to support that objective — and if so, where does the value actually sit? | No, but it is *answerable in the negative* |
| **The board (§0)** | The current best-supported path for investigating that question | **Yes. Evidence, not commitment** |

**The board is a hypothesis about where to look, not a plan of record.** It is where it is because the
structure map bounded the signal axis and left the pricing assumption unverified — that is the *reason*
for the four steps, and if the reason stops holding the board changes. **If evidence shows the board is
wrong, or that some other path has a better chance of producing economic value, change the board.**
Doing so is the document working, not the document failing.

**What this does not license.** Standing rules 1 and 2 still bind. They gate research justified by
*availability* — "we could build this" — and they are not a licence-in-reverse either: a branch does not
reopen because someone asserts it might be valuable. **The bar for changing the board is the same bar as
§6: name the decision it improves and the size of the improvement.** The difference is only that a
*better* answer to that question replaces a step, rather than being added alongside it.

**And the negative is a permitted outcome.** "No economically valuable tool exists at this instrument,
for this book" is a real possible answer, and E9 (0 of 40 structures beat the naked book on CAGR) is
currently pointing at it. Step 3 exists precisely because the objective is economic value rather than
*shipping a hedge* — if options are the wrong instrument, the objective survives and the instrument does
not. Reaching that conclusion honestly would be a success of this repo, not a failure of it.

## 0. The board

Four steps, in order. Each is carried in full at the §6 reference; nothing here is new.

| # | step | what it decides | ref |
|---|---|---|---|
| **1** | **Fit the real SPY skew surface** from `options-quant`'s archived chains | Whether the §1.1 tenor result — the largest finding in the repo — survives realistic option economics. It can overturn it, which is why it is first | §6.1, U1 |
| **2** | **Extend the clairvoyant grid to 26w and 52w** | Completes §5.2 and converts it from suggestive to settled. One line | §6.2, U2 |
| **3** | **Decide the objective: options economics or drawdown reduction** | A decision for Adam, not a measurement. Gates how much of the rest is worth doing at all | §6.3, U4 |
| **4** | **Specify and measure the recycling rule** | README §1 claims monetize-and-rebuy as a source of value; it has never been written as a rule, so it has never been measured | §6.4, U3 |

**Two constraints bind this board.**

- **Step 1 is MEASUREMENT ONLY** (§6.1). No optimizing strikes, tenors, signals or recycling rules
  while the surface is being estimated, and no re-ranking the §1.1 grid as a by-product.
- **All four steps are *protection* economics** (§5.0). *Signal* economics is bounded and closed to
  new work unless §6's quantitative reopening bar is met.

**Nothing else is on the path.** §6 "Does not qualify" says why for each closed branch, and standing
rule 1 says availability is not a reason to add one.

---

# Part II — the evidence base

*Why the board looks like that. Governance, not agenda.*

## 1. Established empirically

Claims that survived a preregistered run with adversarial alignment checks. Each is `[D]` deductive
(code/algebra implies it) or `[I]` inductive (measured on a sample, carries an effective-n).

| # | claim | evidence | kind |
|---|---|---|---|
| E1 | The MS state is a **width meter**: realized vol separates 2.446x (SPY) / 1.791x (QQQ) across probability bins, monotone in all six bins, stable across sample halves | `state_character.py` | `[I]` |
| E2 | It carries **no direction content** — the drift difference *reverses sign* between SPY and QQQ, down/up tail ratio straddles 1.0 | `state_character.py` | `[I]` |
| E3 | By the time it says "wide", the book is already **~13% below its running peak** at the median, within 0.4pp on two assets | `state_character.py` | `[I]` |
| E4 | The predictive density is **body-calibrated, tail-broken**: breach 1.79% at a promised 1%, degrading monotonically with depth on three independent measures | `walkforward.py density` | `[I]` |
| E5 | The 1% failure is a property of **the data, not the model** — constant 1.87%, EWMA 2.03–2.36%, MS 1.79%. Shared assumption is Gaussian | `baselines.py` | `[I]` |
| E6 | Squared-return ACF of any Markov-switching model decays **geometrically**, for any k and any parameters | Timmermann (2000) Prop. 5 | `[D]` |
| E7 | A finite Gaussian mixture is **Gaussian in the far tail** for any k and any weight — more regimes cannot fix a tail | algebra | `[D]` |
| E8 | Daily data resolves volatility memory to **lag 212 (~10 months)**; weekly hid all of it inside a ±0.0469 noise band | `memory_diagnostic.py` | `[I]` |
| E9 | **No structure in the grid beats the naked book on CAGR** — 0 of 40, both samples. README §2's inequality fails on average everywhere tested | `structure_map.py` | `[I]` |
| E10 | **Tenor is the dominant structural variable and the effect is monotone and large** — see §1.1 | `structure_map.py` | `[I]` |
| E11 | Correcting the equity skew moved hedge efficiency **17.58 → 3.6**; at 5–10% OTM the drawdown benefit turned *negative* on the full sample | `hedge_economics.py` | `[I]` |

### 1.1 The tenor result — the largest measured effect in the repo

Drawdown bought (pp) @ cost (pp/yr of CAGR), outright puts, skew slope 0.60, 5% offer spread:

| strike | sample | 4w | 13w | 26w | 52w |
|---|---|---|---|---|---|
| 10% OTM | 1993–2026 | −1.1 @ 3.28 | +1.1 @ 3.39 | **+10.8 @ 2.74** | **+16.8 @ 2.36** |
| 10% OTM | 2003–2026 | +5.1 @ 2.85 | +5.7 @ 2.98 | **+17.8 @ 2.51** | **+19.9 @ 2.49** |
| 15% OTM | 1993–2026 | +4.1 @ 1.14 | +3.3 @ 1.85 | +10.6 @ 1.59 | +11.8 @ 1.77 |
| 15% OTM | 2003–2026 | +4.1 @ 0.94 | +3.3 @ 1.64 | +12.5 @ 1.42 | +16.0 @ 1.70 |

**Extending tenor buys three to four times the protection for the same money or less.** Cost is flat
to *falling* across the row. This is not a trade-off being navigated; it is a dominated region of the
design space that the repo occupied for two years without measuring.

Best drawdown bought anywhere in the grid: **52w 5% OTM outright, +20.6pp @ 3.41 (full) / +24.3pp @
3.74 (2003+)**.

---

## 2. Falsified, or shown uninformative

Recorded so none of it is rebuilt. Distinguish **falsified** (tested, wrong) from **uninformative**
(tested, cannot discriminate) — the second is not an invitation to retest with more effort.

| # | claim | status | why |
|---|---|---|---|
| F1 | The MS model adds information about forward downside risk **beyond VIX, on levels** | FALSIFIED | D3: joint R² 0.1015 vs VIX-alone 0.1015, identical to 4 dp; c = +0.0009, p = 0.99 |
| F2 | …**on dynamics** (persistence, the one thing VIX structurally lacks) | FALSIFIED | scale-free `Var_4/Var_1` adds **0.0004 of R²**; power demonstrated, not assumed |
| F3 | Volatility has **power-law memory** a Markov chain cannot match | FALSIFIED (weakly) | exponential wins at daily, H = 0.423; but the verdict flips with window, so the refutation is itself weak |
| F4 | The **absorption ratio** identifies systemic stress VIX cannot see | FALSIFIED | its expanding-percentile trigger fired 76.9% of weeks in 2004–06 and 4.0% in 2018–26 — governed by accumulated history, not markets. All three "AR-only" episodes retracted |
| F5 | Correlation-vs-covariance isolates coupling from level | FALSIFIED | `corr(AR_corr, AR_cov) = +0.9825`. The design choice was inert. AR is `+0.4965` correlated with VIX — half VIX |
| F6 | **Deep OTM is where tail insurance lives** | FALSIFIED | 30% OTM at 4w/13w buys **negative** drawdown. The drawdown-bought table is dominated by *shallow* strikes at long tenor |
| F7 | Hedge **efficiency** (dd bought ÷ cost) is a usable selection metric | FALSIFIED | denominator → 0. At slope 0.00 the grid's best efficiency is **218.23 at a cost of 0.03pp/yr** — a structure protecting nothing. Rank on drawdown bought at a stated cost instead |
| F8 | The signal is effectively **binary** | FALSIFIED | the ambiguous band is 17.6% of SPY weeks with a 66.7% transition diagonal — a state, not a corridor |
| F9 | Any trigger rule can be **confirmed** on this data | UNINFORMATIVE | 8 rules against ~5 systemic episodes. Power to kill, never to confirm |
| F10 | **EWMA vs MS at h=1** discriminates the model class | UNINFORMATIVE | structurally identical one step ahead; a DM null is what theory predicts. Declared VOID |
| F11 | **GARCH encompassing** would settle whether regimes add anything | UNINFORMATIVE *a priori* | ARCH-LM rejects at 55.6 *after* regime-switching, so a null is confounded by known misspecification. Formally ASYMMETRIC: positive is clean, null is uninterpretable |
| F12 | Put **spreads** improve the hedge | FALSIFIED for this mandate | they top the efficiency table (13.90) and buy 3.3–6.8pp of drawdown against outright's 16.8–24.3pp. Cheap, and capped exactly where the program exists to pay |

**The common cause of F9–F11 and F4.** Anything whose value depends on counting systemic drawdowns
has an effective sample of ~10–15 in all of SPY history. Not fixable by better estimators, better
triggers, or better calibration.

---

## 3. Genuinely unknown

Only items where the answer is not already determined by §1 or §2.

| # | unknown | why it is still open |
|---|---|---|
| U1 | **The real skew surface.** `skewed_vol` is `IV = VIX + slope × pct_OTM × sqrt(4/tenor)`, slope swept over 0.0–0.8 with 0.60 primary. "The repo has no option chain" | every cost number in §1.1 depends on it, and the `sqrt(4/tenor)` term is what makes long tenor cheap — **the tenor result rests on an unverified parameterization that systematically favours the conclusion** |
| U2 | **The clairvoyant ceiling at 52w.** Computed at 4w and 13w only | it is the denominator of the entire signal question at the tenor that actually works (§5) |
| U3 | **Recycling.** README §1 monetises the hedge and buys the core back lower; `simulate` reinvests passively at the next roll | never sized deliberately. May matter more than any strike choice |
| U4 | **The honest competitors.** A trend sleeve or long duration carry neutral-to-positive carry instead of bleeding | never compared. Needs data this repo lacks |
| U5 | **Daily minimum history.** `RELIABLE_MIN_OBSERVATIONS` = 520 is a *weekly* figure | blocks quoting any daily model result |
| U6 | **Long-memory order `d` with a standard error** (GPH / local Whittle), and a better vol proxy (Parkinson, Garman-Klass, Yang-Zhang) | F3's refutation is weak and window-dependent; an R² race is not a long-memory test |

---

## 4. Why each unknown is unknown

The question the user asked, and the one that decides what to build. **Insufficient data**, **wrong
method**, and **unclear objective** have completely different remedies, and only the first is fixed by
running something.

| unknown | cause | remedy | worth doing? |
|---|---|---|---|
| U1 skew surface | **insufficient data** — genuinely absent input, and it is *available* | `options-quant` has archived point-in-time SPY chains since 2026-08-14 with 25Δ risk reversal and butterfly per expiry. Fit the real term-and-strike surface, replace the sweep | **yes — highest value per hour in the repo** |
| U2 52w clairvoyant | **insufficient computation** — trivially absent | add 26w/52w to `hedge_economics.py`'s tenor loop. One line | **yes — cheapest** |
| U3 recycling | **unclear objective** — "monetize and recycle" was never specified as a rule | write the rule down before measuring it; the measurement is easy once the decision is stated | yes, after U1/U2 |
| U4 competitors | **unclear objective** — is the mandate "hedge with options" or "reduce drawdown"? README §1 assumes the instrument | resolve the objective first. If it is the second, this is the most important open item in the repo | **decide, then scope** |
| U5 daily min history | insufficient data-work | re-measure | only if the memory strand is revived |
| U6 memory shape | **wrong method** (R² race) *and* insufficient data (noisy proxy) | GPH/local Whittle on a range-based proxy | **low — see §6** |

**Nothing in §3 is blocked by an inappropriate model class.** That was the 2024–2026 hypothesis and
§2 retired it. The live constraints are one missing dataset (U1), one missing objective (U4), and one
missing line of code (U2).

---

## 5. The actual decision problem

Stated as a decision, not a research question.

> **Given a permanently long global equity book that is never sold, choose a standing put structure
> (tenor, strike, notional, roll rule) and then decide whether to vary it over time.**

### 5.0 Protection economics and signal economics are separate questions

**Confirmed as binding 2026-08-15.** These decompose the decision and they are at completely
different stages of evidence. Conflating them is the error the structure map makes *easy*, because
one set of tables carries both.

| | question | status |
|---|---|---|
| **Protection economics** | Is long-dated put protection economically attractive at all — does it buy drawdown at a price worth paying? | **UNRESOLVED.** Every cost number depends on U1, an unverified skew parameterization that favours the conclusion |
| **Signal economics** | Conditional on a structure, is varying it over time worth anything? | **BOUNDED.** §5.1–5.2: ≤ ~3pp/yr ceiling, real rules capture 4–7%, and the protection axis is near-saturated by structure alone |

**The permitted inference and the forbidden one.** Permitted: *timing appears much less valuable than
this project assumed.* Forbidden: *therefore buy long-dated protection.* The second does not follow
and is not supported by anything measured. §1.1 and §5.2 establish a **relative** ordering among
structures under a fixed pricing assumption; they establish **no absolute** claim that any of them is
worth buying. E9 points the other way — 0 of 40 beat the naked book on CAGR.

Two axes, and they are **not** symmetric:

| axis | observations available | measured effect size | status |
|---|---|---|---|
| **Structure** — tenor, strike, spread vs outright, notional | ~1,700 weekly rolls over 33 years; every parameter paid thousands of times | **3–4x** difference in drawdown bought at equal cost (§1.1) | measured 2026-08-15, largely unexplored before |
| **Timing** — when to be on | ~10–15 systemic drawdowns, heavily overlapping | ≤ ~3pp/yr ceiling; real rules capture **4–7%** of it | measured, and bounded |

### 5.1 What a perfect signal would actually buy — the decomposition

Subsample 2003–2026, skew slope 0.60. Always-on against the **clairvoyant bound at the same strike
and tenor** (EVPI — the strict ceiling on what *any* trigger could ever achieve there):

| structure | always-on: dd bought @ cost | clairvoyant: dd bought @ CAGR gain | what timing adds |
|---|---|---|---|
| 13w 5% OTM | +13.1 @ −5.15 | +14.5 @ **+3.31** | **+1.4pp of drawdown, +8.46pp/yr of return** |
| 13w 10% OTM | +5.7 @ −2.98 | +8.7 @ +1.86 | +3.0pp of drawdown, +4.84pp/yr |
| 13w 15% OTM | +3.3 @ −1.64 | +6.0 @ +1.03 | +2.7pp of drawdown, +2.67pp/yr |

**Read it.** At the structure where the hedge actually works, perfect foresight buys **1.4 more
points of drawdown protection** and **8.5 points a year of premium**. A signal is not a protection
device. It is a **cost-reduction device**, and that is the whole of its value.

### 5.2 The finding that reorders the project

Always-on at **52w 5% OTM** buys **+24.3pp** of drawdown at a cost of 3.74pp/yr (2003+).
The **clairvoyant** 4w 5% OTM bound is **+24.7pp**. The clairvoyant 13w 5% bound is **+14.5pp**.

**Choosing the tenor correctly, with no signal at all, delivers as much drawdown reduction as perfect
foresight at the tenors previously tested.** The apparent value of timing was substantially an
artifact of holding structure at 4–13 weeks. It is a property of the structure chosen, not of the
market.

*Honest limit:* the 52w clairvoyant column does not exist (U2), so this compares 52w always-on
against 4w/13w clairvoyant. It does **not** show timing is worthless at 52w — it shows the
protection axis is close to saturated by structure alone. The premium axis is untouched by this
comparison and remains the live question.

---

## 6. What research would materially change the decision

The gate. An item qualifies only if a plausible outcome **changes an action**.

### Qualifies

*This is the §0 board, in full. Items 1–4 are the same four steps in the same order.*

1. **Fit the real skew surface from `options-quant` chains (U1).** Every cost figure in §1.1 and §5
   is conditional on a swept assumption, and the `sqrt(4/tenor)` term is load-bearing *in the
   direction of the conclusion*. If real 52-week skew is steeper than the parameterization assumes,
   the tenor result shrinks or inverts. **This can overturn the single largest finding in the repo**,
   which is exactly what makes it worth running first. Data-only; no import, no code dependency.

   > **MEASUREMENT ONLY — binding constraint, 2026-08-15.** While estimating the surface, do not
   > optimize strikes, tenors, signals or recycling rules, and do not re-rank the §1.1 grid as a
   > by-product. The deliverable is *a measured surface and a statement of whether the synthetic
   > tenor result survives it* — nothing else. The question is whether §1.1 stands under realistic
   > option economics, and that question is destroyed by tuning against the answer while it is being
   > measured. This is a §5.0 protection-economics question and must not be reported in
   > signal-economics terms.
2. **Extend the clairvoyant grid to 26w and 52w (U2).** One line. Completes §5.2 and converts it from
   suggestive to settled. Until it exists, "timing is worth ~3pp/yr" is a claim about 4w and 13w only.
3. **Resolve the objective in U4: options, or drawdown reduction?** If the mandate is drawdown
   reduction, a trend sleeve is the honest competitor and the entire options program is one branch of
   a comparison never run. This is not a measurement — it is a decision only the user can make, and
   it gates how much of §6 is worth doing at all.
4. **Specify and size the recycling rule (U3).** README §1 claims monetize-and-rebuy as a source of
   value; it has never been a rule, so it has never been measured.

### Does not qualify — and why, so it is not re-proposed

- **Any new signal, measure, indicator or estimator.** §5.1 fixes the value of a *perfect* one at
  ~3pp/yr and real rules capture 4–7% of that. A better width meter does not move a decision.
  **Precondition for reopening:** score it as *premium avoided per unit of protection retained*
  against the §5.1 decomposition, at 26w/52w. Any other scoring is answering a question we no longer
  have.
- **Multi-asset / absorption ratio.** F4 and F5 refuted the trigger and showed the level is half VIX;
  effective n ≈ 3–6. Kritzman's standardised shift is the correct repair, and it is a repair to an
  underpowered measurement of an axis §5.1 already bounded.
- **GARCH encompassing (F11), S3 within-regime ARCH, S4 Student-t, DQ, ES bootstrap, R1–R10.** All
  address marginal/level properties of a model whose incremental information is falsified on both
  axes. Valid if the paper is written; not on the decision path.
- **MSM, HAR, daily refit, U6.** Parked with F3. They serve the memory question, and the memory
  question serves the signal program, which is bounded.

### The one thing that would reopen signal research

A demonstration that some measure reduces **premium paid** at fixed protection, at 26–52 week tenor,
by more than ~1pp/yr out of sample. That is a well-posed, falsifiable, decision-relevant target, and
it is the first one this repo has had. Nothing currently in hand suggests it exists — VIX-timed entry
at long tenor is the obvious first candidate and has not been tried, because the repo spent its
effort at 4–13 weeks where structure was dominating the answer.

---

## Related

- [[core-risk-overlay]] — chronological log · [[README]] — mandate
- [[docs/RESEARCH-PROTOCOL]] — preregistration and §0 gate (still binding on anything that runs)
- [[docs/TRANSLATION-LAYER]] — width/direction separation, binding
