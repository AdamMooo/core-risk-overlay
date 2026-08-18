# Problem Map

Last updated: 2026-08-17

**What this document is.** The standing answer to *what is the problem, what has been established,
and why the project is pointed where it is.* Organised by epistemic status, not by date.
[[core-risk-overlay]] is the chronological log and keeps that job.

**Status: EVIDENCE BASE AND TRANSITION RECORD.** As of 2026-08-17 this file no longer sets the
agenda. [[CHARTER]] does. What lives here is Part II — the evidence — and Part I, the record of how
one research program was closed and another adopted.

**Why the split.** This document was governing while there was a board to govern. There is now a
charter with one experiment queue, and two documents that both claim to say what happens next is
exactly the ambiguity the transition exists to remove.

---

# Part I — the transition

## 0. AMENDMENT 2026-08-17 — the prediction program is closed; intervention design replaces it

*Recorded as a first-class amendment, in full, because otherwise the repository will eventually look
like someone simply changed their mind.*

### 0.1 The original question

From the first README (`564e14e`, 2026-08-11), titled **"Portfolio Thermostat"**, steelmanned:

> For a permanently-long retail book that is never sold, can a slow, likelihood-based, real-time
> measure of market conditions tell us **when to scale a standing OTM put overlay up or down** — and
> does doing so improve the book's path outcome versus a fixed policy?

Note what that document **fixed by assumption**: 3-6 month expiry, 10-20% OTM, weekly cadence, k=2,
`p00 ≈ 0.98`, monetise at 90%. And what it made **the subject of research**: the probability estimate.

### 0.2 What was established

Decomposing the original question:

| sub-question | verdict |
|---|---|
| Can market state be measured in real time from public data? | **Yes.** A width meter separating realized vol ~2.4x out of sample, replicating on two assets, arriving ~13% below the running peak (E1-E3) |
| Is that measurement incremental to cheaper public alternatives? | **No**, scoped. Nested inside VIX on levels (F1) and on dynamics (F2), with power demonstrated |
| Does scaling on it beat a fixed policy? | **Bounded** at 4w/13w: clairvoyant ceiling +2.8 to +3.2pp/yr, real rules capture 4-7%, no rule beat not hedging on return |
| What *is* the best fixed policy? | **Barely asked.** One run, 2026-08-15, and its benefit metric has effective n = 1 |

**Three things make the negative stronger than a failed search**, and they are why this is a closure
rather than a fatigue:

1. **EVPI is a supremum over all block-level triggers**, computed without finding one. Search-independent.
2. **The benchmark was free.** Losing to VIX is losing to a number on a screen, not to a tuned rival.
3. **Power was demonstrated, not assumed.** F2's input ranged 0.80-1.31, correlated only −0.53 with
   VIX, had standalone R² 0.034 — and added 0.0004. That is a coefficient that is zero.

### 0.3 What was NOT established, stated so the closure is not over-read

**"We failed to find an edge" and "there is no edge" are not the same statement**, and only the first
is supported in general.

- The closure covers **one family** — public return-volatility estimators — for **decision** purposes,
  on **SPY**, against **VIX**, on forward downside semivolatility at **h=4 and h=13**. Credit, funding,
  breadth and positioning were never tested: **out of scope, not refuted.**
- **The EVPI ceiling was computed only at 4 and 13 weeks** — the tenors E10 suggests are dominated.
  `hedge_economics.TENOR_WEEKS = (4, 13)` is why. That corner is open and is [[CHARTER]] E3.
- Even if E3 finds a large ceiling at 52w, the branch does not reopen: a 52-week program makes 33
  decisions in 33 years, so capture could never be demonstrated on it. **E3 either closes the
  prediction program or proves it undecidable on this data.** Both are terminal, which is why it is
  queued rather than dropped.

### 0.4 Why the program is closed

Not because the answer was disappointing. Three structural reasons:

1. **Containment explains the negative rather than merely recording it.** `F_returns ⊆ F_market`: the
   option market observes the same return path plus everything else. Realized vol, EWMA, GARCH, the MS
   state and the absorption ratio are five smoothings of one public quantity — recent return
   magnitude. They differ in *how they smooth*, not in *what they see*. The absorption ratio was built
   specifically to escape this and came back +0.4965 correlated with VIX.
2. **The ceiling is low wherever it has been measured**, by a construction that does not depend on
   finding a signal.
3. **The variable that dominated outcomes was fixed by assumption.** Tenor. The original plan held
   constant the thing that mattered and researched the thing that did not.

> **The old program's failure was in what it held constant, never in how carefully it measured.**

### 0.5 Why intervention design replaces it

The mandate forbids selling the core. Formalised ([[CHARTER]] §2) that means the decision variables are
**the contract and the policy** — tenor, strike, roll schedule, notional, monetisation — every one of
which is a *choice*, not a forecast. The only positive result in the project's history came from that
space, and it came with no model at all.

The mathematical object changes accordingly: from conditional densities and latent states to the
drawdown process `D(t) = 1 - W(t)/M(t)` and its functionals. **The objective always lived there.** The
previous 1,143-line mathematics reference contained no treatment of drawdown whatsoever.

### 0.6 Infrastructure retained

The point-in-time discipline and leak register; the adversarial alignment checks; the claim-tuple
gate and the standing principles (protocol §0, §0.2 → [[docs/RESEARCH-PROTOCOL]]); the EVPI
construction; `src/data_loader.py`; and 81 checks guarding the closed pipeline so its negatives stay
reproducible. **Verified 2026-08-17: D3 and F2 reproduce bit-for-bit after the migration.**

### 0.7 Prohibited from reopening

Prediction of forward risk from public return-volatility estimators (F1, F2); the h=1 EWMA comparison
(F10); GARCH encompassing (F11); within-regime ARCH (S3); the memory-shape question (F3, U6); the
absorption ratio as a trigger (F4, F5); all trigger rules (F9); the Hamilton-filter recovery board and
its six items; and **Item 5 with its three resolutions** — withdrawn rather than answered, because
[[CHARTER]] §2's C1 and C2 exclude variance targeting on equity weight formally, not merely in spirit.

Three items are **reclassified, not reopened** — the surface as *procurement* rather than prediction,
cross-market data as *independent replication for a structural claim* rather than as a joint
information set, and S4 as *the paper*. The distinctions are set out in [[PARKED]].

### 0.8 The correction that reframes the project

`README` §2 held that truncating the left tail raises geometric return *provided premium drag is
smaller than the drawdown avoided*, and treated that proviso as the premise. **E9 measured it: 0 of 40
structures beat the naked book on CAGR, in both samples.** The inequality fails on average everywhere
tested.

**That is price discovery, not failure.** The overlay is a purchase of a different outcome path at a
cost in compound return. The question becomes what that path is worth — which makes the remaining work
a procurement problem and a preference problem, and moves the preference explicitly downstream of
research ([[CHARTER]] §7).

---

# Part II — the evidence base

*Preserved verbatim from the closed program. This is the asset. It constrains what may be rebuilt; it
does not set the agenda.*

> **Three corrections attach to everything below. Two were found on 2026-08-17; the third was
> measured on 2026-08-18 and is the largest.**
>
> 1. **Effective n on the benefit side is 1, not ~10.** `hedge_economics.summarize` returns
>    `max_drawdown` as a single `.min()` of the drawdown series, and on both reported samples that
>    statistic is set by the same episode (Oct 2007 - Mar 2009). §5's asymmetry table below is
>    therefore right about the **cost** column (~1,700 rolls) and wrong about the **benefit** column.
>    **The structure axis and the timing axis share the same sample wall; they differ only on cost.**
> 2. **Roll phase is an unswept hidden parameter.** Blocks walk a fixed calendar grid, so a 52-week
>    program makes 33 decisions in 33 years and the alignment of the crisis to the roll boundary is set
>    by the sample's first date.
>
> 3. **The measured drawdown reduction is mostly a mark, not cash.** E0 (2026-08-18) reran the
>    identical simulation under one accounting change — recognise the hedge when it becomes a cash
>    flow rather than continuously — and **82% of the 52-week reduction on the full sample, 85% on
>    the 2003– subsample, is mark.** +16.8pp becomes +3.0pp; +19.9pp becomes +3.0pp. In the
>    well-sampled `CDaR_alpha` coordinate the full-sample cash reduction at 52w is zero to slightly
>    negative at every alpha. **The accounting interval is wider than the effect inside it**, so no
>    magnitude below is interpretable until [[CHARTER]] E6 specifies a monetisation rule. Full
>    result: [[STUB-E0-M3-DECOMPOSITION]] §9.
>
> Consequently the **orderings** in §1.1 are probably robust
> while the **magnitudes** are one draw at one phase and are **not identified**. Do not quote them as
> effect sizes. [[CHARTER]] E1 and E2 test exactly this.

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
| E12 | **The drawdown reduction is predominantly a mark.** Same path, same contracts, one accounting change: 82% (1993–) and 85% (2003–) of the 52w reduction is unrealised mark; the cash-recognised reduction is ~+3pp and flat from 26w to 52w | `m3_decomposition.py` | `[I]` |

### 1.1 The tenor result — the largest measured effect in the repo

Drawdown bought (pp) @ cost (pp/yr of CAGR), outright puts, skew slope 0.60, 5% offer spread:

| strike | sample | 4w | 13w | 26w | 52w |
|---|---|---|---|---|---|
| 10% OTM | 1993–2026 | −1.1 @ 3.28 | +1.1 @ 3.39 | **+10.8 @ 2.74** | **+16.8 @ 2.36** |
| 10% OTM | 2003–2026 | +5.1 @ 2.85 | +5.7 @ 2.98 | **+17.8 @ 2.51** | **+19.9 @ 2.49** |
| 15% OTM | 1993–2026 | +4.1 @ 1.14 | +3.3 @ 1.85 | +10.6 @ 1.59 | +11.8 @ 1.77 |
| 15% OTM | 2003–2026 | +4.1 @ 0.94 | +3.3 @ 1.64 | +12.5 @ 1.42 | +16.0 @ 1.70 |
| **10% OTM, in CASH** | 1993–2026 | **−4.7** | **−4.8** | **+3.2** | **+3.0** |
| **10% OTM, in CASH** | 2003–2026 | **+1.1** | **−0.9** | **+4.4** | **+3.0** |

**Extending tenor buys three to four times the protection for the same money or less.** Cost is flat
to *falling* across the row. This is not a trade-off being navigated; it is a dominated region of the
design space that the repo occupied for two years without measuring.

**The two cash rows are E0, and they are the same table under the accounting the investor actually
banks.** The sign of the tenor ordering survives — long tenor beats short, which is M1 and needs no
pricing — and everything else about the row changes. The cash reduction is **flat from 26w to 52w**,
it is *larger at 26w* on the 2003– sample, and at 4w and 13w it is **negative on the full sample**:
the program deepens the worst drawdown by about 5pp, because premium is paid continuously and the
payoff lands after the trough. The monotone climb across the marked row is a mark that grows with
the length of the block interior — 51 unrecognised weeks at 52w against three at 4w. **Read the
marked row as the ordering and the cash row as the size.**

**And the ordering is not ours.** Israelov (2017), *Pathetic Protection*, sweeps 20 / 63 / 250
business-day maturities and reports that *"longer-dated options do a less bad job of protecting a
portfolio against long-term drawdowns than shorter-dated options. Less bad, but not good"* — E10's
ordering and, in cash, roughly its size. It was `[UNREAD]` at row 1 of the reading list while E10
was derived empirically, and it is logged as a §0-rule-3 process failure in
[[literature/README]]. **What this repo adds is the decomposition, not the ordering.** The paper's
own remedy — static divestment — is inadmissible under [[CHARTER]] §2 C2, so its verdict does not
transfer while its mechanisms do.

Best drawdown bought anywhere in the grid: **52w 5% OTM outright, +20.6pp @ 3.41 (full) / +24.3pp @
3.74 (2003+)**. **In cash the full-sample figure is +2.3pp** (share 89%). The 2003– cell has never
been quoted in cash and must not be quoted at all until it is.

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
| U3 | **Recycling.** README §1 monetises the hedge and buys the core back lower; `simulate` reinvests passively at the next roll | **Promoted by E0 from open question to precondition.** The marked-versus-cash interval is 13.9pp wide inside a 16.8pp claim, so `rho` and `kappa` ([[CHARTER]] E6) now gate the interpretation of every magnitude in §1.1 — not just this row |
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

---

## 5. The decision problem, restated

Superseded by [[CHARTER]] §1. Preserved here in its closed form because the *change* is the finding.

**As it stood on 2026-08-15:** *"Given a permanently long global equity book that is never sold, choose
a standing put structure (tenor, strike, notional, roll rule) and then decide whether to vary it over
time."*

**What changed.** It presumed the instrument and treated "vary it over time" as a live second half.
E3 will close or make undecidable the second half; and the first half turned out to be underspecified
in three ways nobody had noticed — no monetisation rule, no phase sweep, and a benefit statistic with
no sampling distribution.

### 5.0 Protection economics and signal economics remain separate

**Still binding, and it is the rule that diagnosed Item 5.** Never state a result about one in the
vocabulary of the other.

| | question | status |
|---|---|---|
| **Protection economics** | Is protection economically attractive at all — what path does it buy, at what cost? | **THE ACTIVE PROGRAM.** Reopened deliberately, because it is the half that was never measured properly |
| **Signal economics** | Conditional on a structure, is varying it over time worth anything? | **CLOSED at 4w/13w**; undecidable-or-closed at 26w/52w pending E3 |

**The permitted inference and the forbidden one.** Permitted: *timing appears much less valuable than
this project assumed.* Forbidden: *therefore buy long-dated protection.* The second does not follow.
E9 points the other way on return, and the drawdown side is not identified.

**And the generalisable lesson.** Item 5 proposed variance targeting on equity weight, scored against
constant weight — signal economics with the base case never measured. It recreated this exact error in
a new instrument, one day after the rule that names it was made binding. **The rule is only as good as
its application to the next proposal, including one's own.**

## 6. What research would materially change the decision

**Superseded by [[CHARTER]] §9, which is the single experiment queue.** No list of candidate work
lives in this file, deliberately: two documents proposing next steps is how a second research program
starts.

The gate is unchanged in spirit and stronger in form — [[docs/RESEARCH-PROTOCOL]] §0, now seven fields,
with `BOUNDARY` empty meaning *do not run* and `IDENTIFICATION` written before the run.

## Related

- [[CHARTER]] — the active program, and the only queue · [[PARKED]] — deliberately excluded
- [[README]] — the mandate · [[core-risk-overlay]] — chronological log
- [[docs/RESEARCH-PROTOCOL]] — the gate · [[docs/MATH-REFERENCE]] — path functionals
- [[docs/POINT-IN-TIME-DISCIPLINE]] — leak register, including this program's own channels
- [[closed-research/README]] — the completed prediction program, reproducible
