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
| **I** | **§0.1 — rejected** | The option-surface branch and the short-horizon framing that produced it |
| **I** | **§0 / §0.2 — the board** | **The forward path: recover the Hamilton-filter question from the long-horizon objective** |
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

**The board is a hypothesis about where to look, not a plan of record. If evidence shows the board is
wrong, or that some other path has a better chance of producing economic value, change the board.**
Doing so is the document working, not the document failing.

**This has now happened once, and the worked example is the best argument for the rule.** The board
was four steps of option-structure work, resting on a short-horizon framing. That framing was
rejected on 2026-08-15 (§0.1) and the board became the six-item Hamilton-filter recovery (§0). The
measurements taken under the old board remain true; the *direction* did not survive.

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

## 0.1 REJECTED — the option-surface branch, and the framing that produced it

**Decision 2026-08-15, and it replaces the previous board entirely.** The skew/surface branch is
**rejected as a research direction for this project** — not postponed, not gated on data quality.

**Why it was wrong, at three levels:**

1. **It failed standing rule 1 on its own terms.** The trigger was *`options-quant` started archiving
   SPY chains on 2026-08-14*. That is availability, not a decision that needed improving. Rule 1
   exists to catch exactly this and did not fire because the person writing the rule wrote the step.
2. **We cannot compete where it leads.** Serious work on option pricing needs historical chain depth,
   execution infrastructure, latency, and a market-maker's information set. We have none of them and
   acquiring them is not this project.
3. **It is the wrong problem.** The surface question is *"can we out-price short-dated insurance"* in
   another costume. [[README]] §2 rejected that on page one. The route back in was through hedge
   implementation rather than through the research question, which is why it did not look like a
   repeat.

**Consequences, recorded so nothing is silently dropped:**

- **The recent surface work is an exploratory detour**, produced by the incorrect short-horizon
  framing. `structure_map.py` and its measurements stand as *measurements* (E9–E11, F6, F7, §1.1) —
  they were run honestly and they are true of what they measured. They are **not** a direction.
- **Protection economics (§5.0) moves to PARKED, not resolved.** Rejecting the surface work means its
  cost side stays unverified in *both* directions. §1.1's tenor result keeps its caveat permanently
  and must never be quoted as settled.
- **The old insurance-framing reopening bar is deleted**, not softened. "Reduce premium paid at fixed
  protection" presupposed the framing being rejected here. A Hamilton-filter research path does not
  need a way back in through insurance pricing; it needs its own objective, which is §0.

## 0. The board — recover the Hamilton-filter question from the long-horizon objective

**A failed short-horizon tail-risk test falsified one application of the model. It did not falsify
the model for the economic problem this project intended to investigate.** Every test to date ran at
h=1 to h=13 against spot (30-day) VIX on forward downside semivolatility — the claim tuples on D3,
the dynamics test and the walk-forward density all say so explicitly, and that scoping is what makes
them re-usable now rather than sunk.

Six items to recover, **in order, and none of them is code.** The validation framework is decided
*after*, not before — choosing the test first is how this repo arrived at h=1 comparisons that
theory says are uninformative.

| # | recover | status |
|---|---|---|
| **1** | **What state or process is the filter actually meant to identify?** Not "high variance" by fitted argmax — what real thing is it a measurement of | OPEN |
| **2** | **Over what horizon should that state persist?** Must be answered from the economics, then checked against the model's own mixing time (§0.2) | OPEN — partly derivable |
| **3** | **How are strengthening, weakening, persistence and decay represented?** The mapping from those words onto `P`, its diagonal, and `lam2` | **derivable now — §0.2** |
| **4** | **Where does longer-horizon mean reversion fit?** | **derivable now — §0.2** |
| **5** | **What economic decision would the information ultimately support?** | OPEN — **Adam's to set.** Everything downstream depends on it |
| **6** | **What out-of-sample result would demonstrate genuine economic value?** | BLOCKED on 1–5 |

**The board is now these six questions.** Changed under standing rule 6 — the previous four steps
were the best-supported path given the framing, the framing was wrong, so the board moved. That is
the mechanism working.

## 0.2 What the repo can already answer — items 3 and 4

Derivable from material already in this repo, so the recovery does not start from nothing. Notation
is `filt[t][j] = P(state j | returns through t)`, transition `p[i->j]`.

| concept | representation | fitted value (weekly SPY) |
|---|---|---|
| **persistence** | diagonal of `P`; expected duration `1 / (1 - p[j->j])` | calm 36.1 weeks, wide 12.9 weeks |
| **strengthening / weakening** | the likelihood-ratio update on `filt[t]` each step | saturating — top-20 weeks sit at `P >= 0.99999` |
| **decay of belief** | second eigenvalue `lam2 = p00 + p11 - 1`; deviation from the ergodic mix decays as `lam2^h` | median `lam2` = 0.9126 across 95 vintages |
| **mixing time** | `1 / (1 - lam2)` | **~11.4 weeks** |
| **mean reversion** | `E_t[sigma2(t+h)] = ergodic level + lam2^h * (current deviation)` | this *is* the model's distinguishing content |

**Two consequences that should shape items 1, 2 and 6.**

- **Mean reversion is the whole structural difference, and it is exactly zero at h=1.** EWMA is
  IGARCH — its multi-step variance forecast is a martingale and never reverts. MS reverts toward the
  ergodic mix at `lam2^h`. At one step the two are identical by construction, which is why F10 was
  declared VOID and why h=1 results carry no information about this model class. **The horizon
  question in item 2 is not a preference; it is the difference between testing the model and not.**
- **The model misdescribes its own persistence, and this is a live tension rather than a settled
  defect.** Fitted duration for the wide state is 12.9 weeks (SPY) / 26.7 (QQQ); *realized* band runs
  are 5.1 / 4.3 weeks, stable across assets while the fitted parameter is not. Item 1 has to say
  which of those the state is supposed to be a measurement of.

**The effective-sample constraint, stated up front because it binds item 6.** Longer horizon means
fewer independent observations from the same history: 1,230 OOS weeks is ~307 non-overlapping at h=4
(D3's actual n), ~95 at h=13, ~47 at h=26. **The horizon that makes the model testable is the horizon
that starves the test.** Any answer to item 6 must state its effective n before it is run — see F9
and the §2 common-cause note.

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
| **Protection economics** | Is long-dated put protection economically attractive at all — does it buy drawdown at a price worth paying? | **UNRESOLVED, and now PARKED** (§0.1). Every cost number depends on U1, an unverified skew parameterization that favours the conclusion — and U1 is no longer being measured. §1.1 therefore keeps its caveat permanently and is never quoted as settled |
| **Signal economics** | Conditional on a structure, is varying it over time worth anything? | **BOUNDED — at h=1 to h=13, against spot VIX, on forward downside semivolatility.** §5.1–5.2. That scoping is load-bearing: it is a bound on the *tested* application, not on the model class at longer horizon (§0) |

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

*This is the §0 board, in full. It is the six-item Hamilton-filter recovery, and none of it is code.*

1. **Recover items 1–6 of §0**, in order, then decide the validation framework. The framework is
   chosen *last* on purpose: this repo's recurring failure is picking a test before stating what the
   model is supposed to know, which is how it arrived at h=1 comparisons that theory says cannot
   discriminate (F10) and at level-vs-level tests that structurally could not see persistence.
2. **Item 5 — the economic decision — is the blocking one and it is Adam's to set**, not a
   measurement. Items 1–4 can be drafted against the repo's existing material (§0.2); item 6 cannot
   be written at all until 5 exists, and writing it earlier is how a metric gets invented to fit a
   model rather than a decision.

### Does not qualify — and why, so it is not re-proposed

- **The option-surface / skew branch. REJECTED 2026-08-15** — see §0.1. Not postponed and not gated on
  data quality: we lack the chain depth, infrastructure, latency and market-maker information set to
  compete there, and it is the "out-price the insurance" question [[README]] §2 rejected on page one,
  re-entering through hedge implementation. **Availability of SPY chains is not a reason** (rule 1).
- **The remaining structure work** — clairvoyant grid at 26w/52w, recycling rule, the trend-sleeve
  comparison. These were board items 2–4 under the rejected framing. They are **parked, not
  falsified**: they measure protection economics, which §5.0 now marks PARKED. They return only if
  item 5 names a decision they serve.
- **Any new signal, measure, indicator or estimator** *added alongside* the recovery. The board is six
  questions; answering them is the work. Rule 1 applies unchanged.
- **Multi-asset / absorption ratio.** F4 and F5 refuted the trigger and showed the level is half VIX;
  effective n ≈ 3–6. Unchanged by this redirection.
- **GARCH encompassing (F11), S3 within-regime ARCH, S4 Student-t, DQ, ES bootstrap, R1–R10.**
  Unchanged — but note the GARCH stub's *horizon* reasoning (mixing time ⇒ h=13, and the h-step
  density rather than a point forecast as the discriminating functional) is **the best material in
  the repo for §0 item 2** and should be harvested there rather than re-derived.
- **MSM, HAR, daily refit, U6.** Parked with F3, unchanged.

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

### On reopening bars

**The previous one is deleted, not softened.** It read: *reduce premium paid at fixed protection, at
26–52 week tenor, by more than ~1pp/yr*. It was well-posed, and it presupposed the insurance-pricing
framing §0.1 rejects — it would have routed the Hamilton filter straight back into the problem this
redirection exists to leave. **A model does not need a way back in through insurance pricing.**

The replacement is §0 item 6, and it does not exist yet **by design**: the out-of-sample bar that
would demonstrate genuine economic value cannot be written until item 5 names the economic decision.
Writing the bar first is how a metric gets invented to fit a model instead of a decision, which is
the error §2's F-rows were produced by.

---

## Related

- [[core-risk-overlay]] — chronological log · [[README]] — mandate
- [[docs/RESEARCH-PROTOCOL]] — preregistration and §0 gate (still binding on anything that runs)
- [[docs/TRANSLATION-LAYER]] — width/direction separation, binding
