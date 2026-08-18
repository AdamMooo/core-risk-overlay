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

## Related

- [[CHARTER]] — E0 heads the queue · [[RESEARCH-PROTOCOL]] §0 — the gate
- [[POINT-IN-TIME-DISCIPLINE]] — the leak register these declarations answer to
- [[MATH-REFERENCE]] — the path functionals · [[PROBLEM-MAP]] — the evidence base
