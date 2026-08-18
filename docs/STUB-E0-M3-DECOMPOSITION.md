# §0 Stub — E0, the M3 decomposition

Committed 2026-08-18, **before any code**, under [[RESEARCH-PROTOCOL]] §0 and [[CHARTER]] §8.
Status: preregistration. Results are appended below in a later commit, and nothing above the results
rule may be edited once they exist.

**The question.** `research/hedge_economics.py:simulate` marks the outstanding put weekly and puts
that mark inside the wealth series from which every drawdown number in this repo is computed. The
money, however, arrives at expiry. So: **is the measured drawdown reduction wealth the investor can
spend, or a model mark on a contract that is never sold?**

The experiment is one accounting difference on the same path, same parameters, same contracts:

```
W_marked(t) = shares * S_t + contracts * P(S_t, K, tau - t, sigma_t)     what the repo computes
W_cash(t)   = shares * S_t                                   for block_start < t < block_end
            = shares * S_t + contracts * max(K - S_t, 0)     at t = block_end
```

`W_cash` recognizes the hedge only when it becomes a cash flow. It is the accounting under which the
program's cash flows are exactly as `simulate` already transacts them — no monetisation rule is
added or assumed, because none exists. E6 later places a stated rule `rho` between these two curves;
E0 measures how far apart they are, which is the width of the interval `rho` has to live in.

---

## 1. Claim tuple

```
frequency   weekly marks
horizon     the full holding period; the divergence lives in block interiors of
            length (tenor - 1) weeks
functional  the drawdown process D(t) = 1 - W(t)/M(t) and its functionals:
            CDaR_alpha as a curve, per-excursion depths, time under water.
            max_drawdown reported ONLY as a labelled diagnostic -- it is the
            statistic the existing headline numbers were built on, and a
            decomposition has to be shown in the coordinate the error was made in
sample      SPY weekly, 1993-02-05 to 2026-08-14, n = 1750 weeks, ONE path.
            Reported on the full sample AND on the inherited 2003-01-24
            subsample; neither is changed here (PARKED, sample definition)
design      ALWAYS-ON, h = 1.00, no signal, no timing, roll phase offset 0
```

**Declared before the run, per [[POINT-IN-TIME-DISCIPLINE]] rows 10-11 — these are researcher
degrees of freedom and are fixed now, not after seeing the answer:**

```
tenors                (4, 13, 26, 52) weeks
moneyness             0.10 primary; 0.05 and 0.15 as sensitivity
skew slope            0.6 (structure_map's PRIMARY_SLOPE), offer spread 5%
CDaR alphas           (0.01, 0.05, 0.10, 0.25, 0.50, 1.00) -- pathfunctionals'
                      default, unchanged
excursion threshold   0.10
```

## 2. Predicted outcome, with its reason

**Derivable from the construction, therefore carrying no information — recorded, not tested.**

- The two curves are **equal at every roll boundary and at the terminal date**. Premium paid, payoff
  received, terminal wealth and CAGR are *identical*. The difference is entirely interior. If any of
  those differ, the implementation is wrong; that is a check, not a finding.
- The gap is **monotone non-decreasing in tenor**: a block's interior is `tenor - 1` weeks long, so a
  4-week program leaves 3 weeks of mark unrecognized and a 52-week program leaves 51.

**The informative part, predicted in advance.** The share of the measured drawdown reduction that
does *not* survive cash accounting:

```
gap_share(tenor) = ( dDD_marked - dDD_cash ) / dDD_marked
```

> **Prediction: gap_share > 0.5 at 52 weeks — i.e. H3 fails at long tenor — and gap_share < 0.2 at 4
> and 13 weeks.**

Reason: the 2007-09 peak-to-trough runs about 17 months, longer than a single 52-week block. The
trough therefore falls *inside* a block with high probability, which is exactly where the two
accountings diverge maximally — and it is where the put's mark is largest. At 4 weeks the put expires
into the decline repeatedly, so nearly all of its value is recognized as cash within weeks of being
earned.

The direction is derivable and would not on its own have justified a run. The magnitude on this path
is not derivable, and it is what decides H3.

## 3. Literature

**No paper settles this.** It is an accounting fact about this repository's own simulator, not a
claim about markets, and no external result can say what our code recognizes as wealth.

Adjacent, both still `[UNREAD]` and recorded as such: Israelov (2017), *Pathetic Protection*, on
rolled-put drag; Ilmanen (2012) on the cost of index put protection. The nearest genuinely relevant
literature is on the monetisation problem — when a hedge's mark should be converted to cash — and
that is E6's, not E0's.

## 4. Mechanism for a difference

**Structural difference.** Marked accounting recognizes the put's model value continuously; cash
accounting recognizes it only when it becomes a cash flow. These are different objects, not two
estimates of one object.

**Horizon at which it is observable:** within a block, up to `tenor - 1` weeks. Zero at every roll
boundary.

**Functional on which it is observable:** any path functional of `D`. **Identically zero** on
terminal wealth, CAGR, premium drag and payoff. That the difference is invisible in the return
coordinates and visible only in the drawdown coordinates is the whole design — it is what makes this
a decomposition of the existing number rather than a rival simulation to be compared against it.

## 5. What would surprise me, and what it changes

- **A small gap at 52 weeks** would surprise me. It would mean the tenor result describes payoffs the
  investor actually receives, and E6 would become a refinement rather than a precondition.
- **A gap exceeding the whole reduction** — cash accounting showing *more* drawdown than the naked
  book — would mean the long-tenor program worsens the experienced path while improving the reported
  one, and would kill the long-tenor branch as currently stated.

**Decision changed either way:** whether the frontier of [[CHARTER]] §3 is built on marked wealth at
all, and whether E6 must run before any subsequent number is interpretable.

## 6. Boundary

**Realizability**, primarily — the third of P3's four questions, and the one the repo has never
touched.

**Economic comparability**, secondarily: tenors are currently compared on an accounting that flatters
long tenor asymmetrically, because long tenor has more interior in which to accrue an unrecognized
mark. If `gap_share` rises with tenor, the existing tenor ordering is partly an artifact of the
accounting and not only of the contract.

## 7. Identification

**Population addressed: none.** This is a decomposition of a statistic computed on a single realized
path.

**Identified in magnitude.** The gap on this path, exactly — it is arithmetic, not estimation, and
carries no sampling error whatever. Also identified: the *sign* of the gap and its *ordering across
tenors*, both of which follow from block-interior length and are structural.

**Not identified.** Any claim that "the mark accounts for X% of the reduction" transfers to another
crisis. That share depends on the phase of the crisis within the block — unswept, and E1's entire
subject — and on the shape of this particular decline. The benefit side's effective n remains **1**,
and E0 does not improve it. **E0 reduces what the existing numbers mean; it does not add an
observation.**

## 8. Verdict rule, fixed in advance

**H3** ([[CHARTER]] §4): *M3 is not the dominant source of the measured drawdown reduction.*

```
REJECTED at a tenor     gap_share > 0.5 there
SURVIVES at a tenor     gap_share <= 0.5 there
INDETERMINATE           dDD_marked < 1.0pp at that tenor -- the denominator is
                        going to zero and the ratio is not reportable
```

The third arm is not a hedge against an inconvenient answer; it is F7 applied before the fact. F7 was
discovered by publishing an efficiency of 218.23 whose denominator was 0.03. A ratio whose
denominator can approach zero gets its floor declared before the run, every time.

---
--- RESULTS RULE. Everything above was committed 2026-08-18 in dc69f13, before
--- `research/m3_decomposition.py` existed. Nothing above it has been edited since.
---

# §9 Results — 2026-08-18

Run: `.venv\Scripts\python.exe research/m3_decomposition.py SPY`.
Implementation: `hedge_economics.simulate(..., mark_hedge=False)` — one branch, six lines including
its comment. Regression checks: `checks.py`, six new, 37 passing.

## 9.0 The precondition held exactly

| tenor | boundary max abs diff | terminal | premium | payoff |
|---|---|---|---|---|
| 4, 13, 26, 52 | `0.00e+00` | `0.00e+00` | `0.00e+00` | `0.00e+00` |

Not "small" — **zero**, at every roll boundary and on every cash flow, at all four tenors. The two
curves are the same program under two accountings, and the entire difference is interior. The
decomposition is therefore uncontaminated: whatever follows is M3 and nothing else.

## 9.1 The headline

**Drawdown bought (pp), 10% OTM, h=1.00, slope 0.60, 5% offer, roll phase 0.**
*Max drawdown — the diagnostic coordinate, effective n = 1, reported because it is the coordinate the
existing headline numbers were made in.*

| sample | tenor | naked | marked | cash | bought (marked) | bought (cash) | gap | share | H3 |
|---|---|---|---|---|---|---|---|---|---|
| 1993– | 4 | 54.6% | 55.7% | 59.3% | −1.1 | −4.7 | +3.5 | n/a | INDETERMINATE |
| 1993– | 13 | 54.6% | 53.5% | 59.5% | +1.1 | −4.8 | +6.0 | 531% | **REJECTED** |
| 1993– | 26 | 54.6% | 43.8% | 51.4% | +10.8 | **+3.2** | +7.6 | 70% | **REJECTED** |
| 1993– | 52 | 54.6% | 37.8% | 51.7% | **+16.8** | **+3.0** | +13.9 | 82% | **REJECTED** |
| 2003– | 4 | 54.6% | 49.5% | 53.5% | +5.1 | +1.1 | +4.0 | 78% | **REJECTED** |
| 2003– | 13 | 54.6% | 48.9% | 55.5% | +5.7 | −0.9 | +6.6 | 116% | **REJECTED** |
| 2003– | 26 | 54.6% | 36.8% | 50.2% | +17.8 | **+4.4** | +13.4 | 75% | **REJECTED** |
| 2003– | 52 | 54.6% | 34.7% | 51.7% | **+19.9** | **+3.0** | +16.9 | 85% | **REJECTED** |

Strike sensitivity, full sample, 52w: 5% OTM **+20.6 → +2.3** (share 89%); 15% OTM **+11.8 → +3.8**
(67%).

**H3 is rejected in fifteen of the sixteen cells where the ratio is reportable**, across both samples
and all three strikes. The single survivor is 4w 15% OTM on the full sample, at 46% — and it survives
by four points, on the shallowest reduction in the table.

**M3 is not merely present. It is the majority of the effect nearly everywhere it can be measured.**

## 9.2 What the number becomes

> **+16.8pp becomes +3.0pp. +19.9pp becomes +3.0pp. +24.3pp — the best cell in the repo — is a
> marked number and has never been quoted in cash.**

The two samples disagree about the marked reduction (+16.8 vs +19.9) and agree exactly about the cash
one (+3.0 vs +3.0). That agreement is not corroboration; both samples contain the same crisis. It is
worth noticing only because the *disagreement* sat entirely in the part that turns out to be mark.

## 9.3 The tenor result is substantially an accounting artifact

E10 — "extending tenor buys three to four times the protection for the same money or less", the
largest measured effect in the repo — decomposes as:

| | 4w | 13w | 26w | 52w |
|---|---|---|---|---|
| bought, marked, 1993– | −1.1 | +1.1 | +10.8 | +16.8 |
| bought, **cash**, 1993– | −4.7 | −4.8 | **+3.2** | **+3.0** |
| bought, **cash**, 2003– | +1.1 | −0.9 | **+4.4** | **+3.0** |

**The sign survives; the magnitude and the interior ordering do not.** Long tenor still beats short
tenor in cash — that is M1, strike anchoring, and it is arithmetic about where the strike sits. But
the cash-recognised reduction is **flat from 26 weeks to 52 weeks**, and on the 2003– sample it is
*larger* at 26w than at 52w. The monotone climb across the row — the shape that made E10 read as a
dominated region of the design space rather than a trade-off — is a mark that grows with the length
of the block interior. It has to: a 52-week block has 51 weeks in which to accrue an unrecognised
mark, and a 4-week block has three.

**At short tenor, cash accounting turns the program's max drawdown *worse than the naked book* — about
5pp worse on the full sample.** Premium is paid continuously; the payoff arrives at expiry, after the
trough. Nothing in the marked view showed this.

## 9.4 In the well-sampled coordinate the cash reduction is approximately zero

`CDaR_alpha` reduction (pp), 10% OTM, full sample. `alpha → 0` is max drawdown with n = 1; `alpha = 1`
is the average drawdown over the whole occupation measure, which is the well-sampled end.

| tenor | acct | 0.01 | 0.05 | 0.10 | 0.25 | 0.50 | 1.00 |
|---|---|---|---|---|---|---|---|
| 26 | marked | +4.3 | +3.5 | +1.2 | −0.8 | −0.8 | −0.6 |
| 26 | **cash** | −0.1 | +0.2 | −1.3 | −2.3 | −2.3 | −1.4 |
| 52 | marked | +10.0 | +8.1 | +5.8 | +3.5 | +2.2 | +1.0 |
| 52 | **cash** | −0.5 | +0.0 | −0.2 | −0.6 | −1.0 | −0.8 |

**On the full sample, in cash, at every alpha, the 52-week program bought nothing.** The reduction is
zero to slightly negative across the entire curve. On the 2003– subsample it is genuinely positive at
the extreme end (52w: +0.6 / +3.5 / +2.9 at alpha 0.01 / 0.05 / 0.10, decaying to −0.2 at alpha = 1;
26w is stronger throughout, at +2.3 / +5.3 / +4.8) — so a cash benefit does exist there, it is
concentrated in the deepest fraction of the drawdown process, and it is a few points rather than
twenty.

This is the CDaR curve doing exactly the job it was built for. The marked effect decays smoothly in
alpha, which is the signature of a statistic resting on the deepest part of one episode; the cash
effect has almost nothing to decay from.

## 9.5 The mark erases excursions the investor still lives through

Full sample, excursions deeper than 10% (threshold declared in advance), and time under water:

| | n ≥ 10% | deepest three | U(10%) | mean depth |
|---|---|---|---|---|
| naked | 9 | 54.6% 45.7% 31.8% | 31.7% | 25.6% |
| 52w marked | 6 | 37.8% 34.7% 15.0% | 29.1% | 20.9% |
| 52w **cash** | **9** | 51.7% 48.8% 31.8% | **34.1%** | 26.9% |

Marked accounting removes three excursions from the record. In cash there are still nine — the same
nine the unhedged book has — and **the book spends more time under water than if it had never hedged
at all**: 34.1% against 31.7%. Premium drag is continuous and the offset is not.

"Smooth the ride" is one of the mandate's three stated goals ([[README]] §1). Measured in cash, on
this path, at this phase, the 52-week program did the opposite of it.

## 9.6 Predictions, scored

- **Derivable part — CONFIRMED exactly.** Curves equal at every boundary, cash flows identical, gap
  monotone non-decreasing in tenor (+3.5, +6.0, +7.6, +13.9). As stated in advance, this carries no
  information; it is a check.
- **`gap_share > 0.5` at 52 weeks — CONFIRMED.** 82% full, 85% subsample, 89% at 5% OTM, 67% at 15%.
- **`gap_share < 0.2` at 4 and 13 weeks — REFUTED**, and the way it failed is the useful part. The
  absolute gap at short tenor is not small (+3.5pp at 4w, +6.0pp at 13w): in a fast crash a
  three-week-old put carries a large mark at 80 vol. And the *share* at short tenor is not a quantity
  at all, because its denominator is the near-zero reduction E10 had already reported.

  **The process lesson. §8 declares a denominator floor because the denominator was known to go to
  zero, and then §2 predicts the ratio at exactly the tenors where that floor binds.** The floor
  caught it — those cells print INDETERMINATE rather than 531% — but the prediction should have been
  stated in pp of gap, not in share. F7 twice in one document, in opposite directions.

## 9.7 What this establishes, and what it does not

**Establishes.**

- H3 is rejected. **M3 is the dominant source of the measured drawdown reduction** at every tenor and
  strike where the ratio is reportable, in both samples.
- The accounting interval is **wider than the effect it contains**: 13.9pp of gap inside a 16.8pp
  claim at 52w full sample; 16.9pp inside 19.9pp at 2003–.
- Therefore **E6 is not a refinement, it is a precondition.** No drawdown magnitude produced by
  `hedge_economics.simulate` is interpretable until a monetisation rule `rho` is specified and
  `kappa` measured. That includes every number in [[PROBLEM-MAP]] §1.1.
- The **tenor ordering's sign** is unaffected — it is M1, and needs no pricing — while its
  **magnitude** and its 26w-vs-52w interior ordering do not survive the accounting change.

**Does not establish.**

- **That the marked number is wrong.** Cash accounting is not the truth either: it recognises nothing
  until expiry, and a real investor can sell. The realizable path under any stated rule lies
  *between* the two curves. E0 establishes that the interval is too wide to quote a point from — not
  which endpoint is right.
- **Any magnitude.** One path, one crisis, one unswept roll phase, effective n = 1 on the benefit
  side. E0 adds no observation; it reduces what the existing ones mean. The 82% share is an
  accounting fact about this path, not an effect size, and it depends on where the crisis fell inside
  the block. **E1 is now materially more urgent**: phase determines how much of a crisis lands in a
  block interior, and phase is precisely what is unswept.
- **Anything about `I_sleeve`.** Additive convex sleeves are marked continuously *and* are sellable
  continuously, so this decomposition does not transfer to them. E7 must state its accounting for
  both arms.

## 9.9 The literature gate, closed late — and it was not empty

**Process failure, recorded first.** [[literature/README]] lists Israelov (2017), *Pathetic
Protection*, as **blocking on E0**, and the carried focus note for 2026-08-18 said so explicitly:
*"Before E0: read it. If it already decomposes mark vs realized, E0's design changes. Protocol §0
rule 3 makes this a gate, not a courtesy."* **E0 ran first and the paper was read after.** §3 above
stands as written — it was honest about the paper's status and wrong to proceed on it. This is the
second §0-rule-3 failure in the repo's history; the first was Timmermann's Proposition 5.

**The gate is now closed, and the verdict is mixed.**

- **E0's design survives untouched.** The paper never distinguishes marked from realized value —
  zero occurrences of *mark-to-market*, *unrealised* or *monetise* in the full text, and every
  drawdown it reports is computed on a marked NAV, the Cboe PPUT index's or a simulated
  portfolio's. **The decomposition run above is not in the literature.** Had the gate been
  honoured, E0 would have run unchanged.
- **E10 was a rediscovery.** The paper sweeps 20 / 63 / 250 business-day maturities and concludes
  that *"longer-dated options do a less bad job ... Less bad, but not good."* That is the tenor
  ordering and, in cash, roughly the magnitude. It sat `[UNREAD]` as row 1 of the reading list
  while the repo derived it empirically over two days.
- **E1 is changed.** The paper's central mechanism is expiration-cycle misalignment — *"equity
  drawdowns have lives of their own that may not conveniently coincide with option expiration
  cycles"*. Under §0 rule 2, that phase matters is now **citable rather than testable**, and a run
  demonstrating it carries no information. E1 must be respecified around what the paper does not
  supply: the **phase spread relative to the effect**, a `Psi` coordinate, which is what H2
  actually turns on.
- **Its remedy is inadmissible here**, and this is the load-bearing difference. The paper's
  alternative throughout is static divestment. [[CHARTER]] §2 C2 excludes it. **Its verdict does
  not bind this mandate; its mechanisms bind it entirely** — which is precisely the case in which
  a paper is most dangerous to skip and most useless to cite as an answer.

## 9.8 Consequences booked

1. `research/structure_map.py` — its M3 caveat is now a measurement, not a warning.
2. [[PROBLEM-MAP]] §1.1 — the tenor table carries a cash row and a rider; E10 is qualified in place.
3. [[CHARTER]] §9 — E0 closed; **E1 promoted** on the argument above; E6 reclassified from queued
   experiment to precondition.
4. No number in this repository may be quoted as a drawdown reduction without its accounting named.

## Related

- [[CHARTER]] — E0 heads the queue · [[RESEARCH-PROTOCOL]] §0 — the gate
- [[POINT-IN-TIME-DISCIPLINE]] — the leak register these declarations answer to
- [[MATH-REFERENCE]] — the path functionals · [[PROBLEM-MAP]] — the evidence base
