# §0 Stub — E1, the roll-phase sweep

> **CLOSED BRANCH — PRESERVED AS EVIDENCE, NOT AS A DESIGN.** This preregistration belongs to the
> rolled-put / tenor intervention program, closed 2026-08-18
> ([[closed-research/intervention/README]]). It is kept intact because its result is evidence and
> because a stub edited after the fact is worthless. **Nothing in it is a queued experiment, and its
> code now lives at `closed-research/intervention/`.** The active program is [[CHARTER]].


Committed 2026-08-18, **before any code**, under [[docs/RESEARCH-PROTOCOL]] §0 and [[closed-research/intervention/CHARTER-INTERVENTION|CHARTER-INTERVENTION]] §8.
Status: preregistration. Results are appended below in a later commit, and nothing above the results
rule may be edited once they exist.

**E1 does exactly one thing: it determines whether the tenor result is materially dependent on an
arbitrary roll-calendar alignment.** It is a robustness test of an intervention result. It is not a
reopening of signal or timing research — no rule conditions on anything, no state is estimated, and
the prediction program stays closed ([[PARKED]], permanently-closed list).

**The defect it addresses.** `simulate` walks blocks from index 0, so for tenor `tau` the roll dates
are `{0, tau, 2tau, ...}` and their alignment against the 2007–09 decline is set by the sample's
first date and nothing else. At 52 weeks that is 33 decisions in 33 years. The phase of those
decisions is a free parameter that has never been varied, and the entire measured benefit comes from
one episode, so the published number could be calendar luck rather than structure.

**Respecified 2026-08-18 by Israelov (2017).** The paper's central mechanism is expiration-cycle
misalignment — *"equity drawdowns have lives of their own that may not conveniently coincide with
option expiration cycles"*. **That phase matters is therefore cited, not tested**, and under §0 rule 2
a run demonstrating it carries no information and must not be performed. E1 measures the quantity the
paper does not supply: **the size of the phase spread relative to the size of the tenor effect**,
which is the clause H2 actually turns on.

---

## 1. Claim tuple

```
frequency   weekly marks
horizon     the full holding period
functional  drawdown bought versus the naked book, in two coordinates:
              max drawdown  -- the coordinate E10 was published in, and therefore
                               the coordinate the question must be asked in
              CDaR_0.05     -- one declared alpha, to say whether any phase
                               sensitivity found is a max-drawdown artifact.
                               Not a new criterion: CHARTER §3 already ranks here
sample      SPY weekly, 1993-02-05 to 2026-08-14, and the inherited 2003-01-24
            subsample. ONE path, unchanged by the sweep -- see §4
design      ALWAYS-ON, h = 1.00, 10% OTM, slope 0.60, 5% offer. No signal, no
            timing, no conditioning of any kind
```

**Declared before the run, all of it fixed here:**

```
phase grid    p = 0 .. tau-1, EVERY offset, for tau in (4, 13, 26, 52)
              4 + 13 + 26 + 52 = 95 alignments per accounting per sample
accountings   marked AND cash (mark_hedge False), because E0 makes a
              marked-only answer uninterpretable
alpha         0.05, single value, declared now
effect        bought(52w, p=0) - bought(4w, p=0), same sample, same accounting.
              Phase 0 is the alignment E10 was published at, so it is the
              denominator the question is about
floor         |effect| < 1.0pp  =>  ratio not reportable (F7, as in E0)
```

**Implementation of the phase shift, fixed now because it is a real choice.** The sweep must move the
roll grid *without* moving the sample — otherwise phase is confounded with start date, sample length
and the naked baseline. So at phase `p` the first block is a **stub of length `p` weeks** and rolls
land at `{p, p+tau, p+2tau, ...}`. The naked book is byte-identical across all phases, and `p = 0`
reproduces today's behaviour exactly. **Known nuisance, declared rather than hidden:** the stub block
buys one shorter-dated option, priced at its own `p`-week tenor, so premium differs marginally across
phases. It is one block out of 33 to 437, at the start of the sample and far from the episode that
sets the result.

## 2. Predicted outcome, with its reason

**Derivable or cited, therefore carrying no information — recorded, not tested.**

- **That phase matters at all.** Israelov (2017), above. Also mechanical: `spread` must be zero at
  `p = 0` by construction and non-zero elsewhere unless the crisis is invariant to alignment.
- **Spread grows with tenor.** A 4-week block can be misaligned by at most three weeks; a 52-week
  block by up to 51. The number of distinct alignments is `tau` itself.

**The informative part, predicted in advance.** The ratio

```
R(tau) = spread(tau) / effect,     spread(tau) = max_p bought - min_p bought
```

> **Prediction: `R(52w) > 1` under marked accounting on the full sample — the phase spread exceeds
> the entire tenor effect, and H2's phase clause fails.**

Reason, and it is M1 rather than pricing: the 52-week benefit is one option spanning the peak. If a
roll lands near the October 2007 high, the strike is set 10% below the peak and the contract spans
the whole first leg down. If it lands six months into the decline, the strike re-anchors roughly 20%
lower and no contract ever spans the peak-to-trough distance. Whether a roll falls near the peak is
calendar luck, and there are only 33 rolls.

**Secondary prediction, on the ordering.** `separation = min_p bought(52w) - max_p bought(4w)`.
Predicted **positive under marked** — long tenor still beats short at every alignment — and
**negative or near zero under cash**, where the whole effect is only about 8pp and 52w cash bought
only +3.0pp at `p = 0`.

## 3. Literature

**Israelov (2017), `[skim]`, is the paper**, and it is why this experiment is respecified rather than
merely promoted. It establishes the mechanism and does not quantify the spread-to-effect ratio on a
permanent-long book, which is the only thing E1 measures. Its own remedy — static divestment — is
inadmissible under [[closed-research/intervention/CHARTER-INTERVENTION|CHARTER-INTERVENTION]] §2 C2, so its verdict does not transfer while its mechanism does.

No other paper settles this. Chekhlov, Uryasev & Zabarankin (2005) remains `[UNREAD]` and gates E2,
not E1; the single declared alpha here is used as a robustness coordinate, not as an optimisation
criterion, and no CDaR number produced by E1 is to be quoted outside the repo before that paper is
read.

## 4. Mechanism for a difference

**Structural difference.** The contract's strike is set at the spot prevailing on the roll date. Two
phases therefore purchase *different strikes on different dates* against the same price path, and at
long tenor the difference is the distance between a strike anchored near the peak and one anchored
part-way down. Nothing about pricing, estimation or information is involved — it is arithmetic about
where the strike sits, the same M1 mechanism the tenor result rests on.

**Horizon at which it is observable:** the full holding period, concentrated in one episode.

**Functional on which it is observable:** drawdown bought. **Invisible in the return coordinates to
first order** — premium differs only by the stub block — so a phase effect that showed up mainly in
CAGR would indicate an implementation error, not a finding.

## 5. What would surprise me, and what it changes

- **A small spread — `R(52w) < 1/3`** — would surprise me and would substantially rehabilitate the
  magnitude of E10 as a structural claim rather than an alignment.
- **`R > 1` with `separation > 0`** is the outcome I expect: the *ordering* is robust to alignment
  while the *magnitude* is not, which is precisely the marked/cash split E0 already produced in a
  different coordinate. It would mean the repo may keep saying "long tenor dominates short" and may
  not quote a number for how much.
- **`separation <= 0`** would be the strong result: at some alignment a 4-week program beats a
  52-week one, and the tenor ordering itself — not just its size — is calendar luck.

**Decision changed:** whether [[PROBLEM-MAP]] §1.1 may state a tenor magnitude at all, in either
accounting, and whether "roll phase" must become a declared coordinate of every future row rather
than an unstated default.

## 6. Boundary

**Robustness.** Single, and this is the whole point of the experiment: E1 moves no other boundary. It
adds no intervention class, no data source, no hypothesis and no criterion. It takes one published
number and asks how much of it survives varying an implementation choice that was never chosen.

## 7. Identification

**Population addressed: none, and the temptation here is specific and must be named in advance.**

**The 52 phases are not 52 observations.** They are 52 overlapping views of *the same crisis*, and
they are deterministic functions of one path. The spread is therefore a **sensitivity of a
single-path statistic to an arbitrary implementation choice**, not a sampling distribution of an
effect.

**Consequently, forbidden in advance and not on the grounds that the numbers come out badly:**

- no standard error, confidence interval or t-statistic computed from the phase distribution;
- no "mean across phases" quoted as an estimate of the effect — the mean of 52 views of one episode
  is still one episode;
- no selection of a phase, or of a range of phases, after seeing the result;
- no claim that a wide spread makes the effect *uncertain in the statistical sense*. It makes the
  published number **arbitrary**, which is a different and more damaging thing.

**Identified.** The spread on this path, exactly — it is arithmetic. The sign of its dependence on
tenor. The ordering test's outcome at every alignment actually computed.

**Not identified.** Anything about a second crisis. **Effective n on the benefit side remains 1 and
E1 does not improve it** — sweeping phase multiplies the *views* of one episode, not the episodes.
This is the same wall E0 hit and the same wall the closed program hit; see the auto-memory note that
three strands share one sample wall.

## 8. Verdict rule, fixed in advance

**H2** ([[closed-research/intervention/CHARTER-INTERVENTION|CHARTER-INTERVENTION]] §4), phase clause only: *the phase spread is small relative to the effect.*

```
SURVIVES        R(52w) <= 1/3
MARGINAL        1/3 < R(52w) <= 1        reported as marginal, not rounded to a verdict
KILLED          R(52w) > 1               the spread exceeds the whole tenor effect
INDETERMINATE   |effect| < 1.0pp         denominator floor, declared as in E0

ORDERING        separation = min_p bought(52w) - max_p bought(4w)
                > 0  ordering survives every alignment tested
                <= 0 the ordering itself is phase-dependent
```

Each verdict is reported **separately for marked and for cash**, and neither is allowed to stand in
for the other.

## 9. Exact outputs — the whole of them

Six blocks, per sample. Nothing else is printed and nothing else is computed.

```
1  phase grid                 the offsets swept, per tenor
2  marked result by phase     bought (pp) at every offset
3  cash result by phase       bought (pp) at every offset
4  phase range and spread     min / median / max / spread, per tenor per accounting
5  spread vs the effect       R = spread / effect, with the effect stated, plus the
                              same ratio on CDaR_0.05 to show whether the sensitivity
                              is a max-drawdown artifact
6  verdict                    against §8, marked and cash separately
```

**No frontier, no ranking, no optimisation, no new file beyond `research/phase_sweep.py`, and no
follow-on experiment triggered automatically.** Anything E1 turns up that is interesting and outside
this list goes to [[PARKED]].

---
--- RESULTS RULE. Everything above was committed 2026-08-18 in 2eb1b1e, before
--- `research/phase_sweep.py` existed. Nothing above it has been edited since.
---

# §10 Results — 2026-08-18

Run: `.venv\Scripts\python.exe research/phase_sweep.py SPY`.
Implementation: `hedge_economics.simulate(..., phase=p)` — the roll grid moves, the sample does not.
Checks: 42 passing, five of them new and specific to the phase mechanic. Run before and after.

**One deviation from the stub's §9 output list, declared here.** Block 4 carries one added column:
the **year the hedged book's max drawdown is set in**, modal across phases. [[closed-research/intervention/CHARTER-INTERVENTION|CHARTER-INTERVENTION]] §2 forbids
reporting a `Phi` row without its `Psi`, and this particular `Psi` turned out to be load-bearing —
see §10.4. No other block changed and nothing else was computed.

## 10.1 The verdicts, against the rule fixed in §8

| sample | accounting | effect (52w−4w @ p=0) | spread at 52w | R | **verdict** |
|---|---|---|---|---|---|
| 1993– | marked | +18.0 | 12.7 | **0.71** | MARGINAL |
| 1993– | **cash** | +7.6 | 14.1 | **1.85** | **KILLED** |
| 2003– | marked | +14.7 | 12.5 | **0.85** | MARGINAL |
| 2003– | **cash** | +1.8 | 12.6 | **6.82** | **KILLED** |

**H2's phase clause is killed under cash accounting in both samples, and marginal under marked in
both.** Nothing here reaches the preregistered SURVIVES threshold of `R <= 1/3` anywhere.

The same ratio in the coordinate declared as the artifact check, `CDaR_0.05`: **0.79** and **1.41**
(1993–), **1.14** and **4.10** (2003–). **The phase sensitivity is not a max-drawdown artifact** — it
is at least as large in the well-sampled coordinate, and on the 2003– sample under marked accounting
the CDaR ratio (1.14) would flip that cell's verdict from MARGINAL to KILLED. The rule keyed on max
drawdown, so the recorded verdict stands as MARGINAL; the CDaR number is reported beside it and not
substituted for it.

## 10.2 The ordering

```
separation = min over phases of bought(52w)  -  max over phases of bought(4w)

1993-   marked   +6.0pp   (min 52w +10.3  vs  max 4w  +4.4)   survives every alignment
1993-   cash     -9.0pp   (min 52w  -6.3  vs  max 4w  +2.7)   PHASE-DEPENDENT
2003-   marked  +13.1pp   (min 52w +18.7  vs  max 4w  +5.6)   survives every alignment
2003-   cash     -7.5pp   (min 52w  -4.8  vs  max 4w  +2.7)   PHASE-DEPENDENT
```

**In marks, long tenor beats short tenor at every one of the 56 alignments tested, in both samples.**
In cash it does not: there exist alignments at which a 4-week program buys more drawdown reduction
than a 52-week one, in both samples.

## 10.3 What the headline number actually ranges over

52-week, 10% OTM, the cell [[PROBLEM-MAP]] §1.1 publishes:

| | published (p=0) | min | max | range |
|---|---|---|---|---|
| 1993– marked | +16.8 | +10.3 | +23.0 | 12.7 |
| 1993– **cash** | +3.0 | **−6.3** | **+7.8** | 14.1 |
| 2003– marked | +19.9 | +18.7 | +31.1 | 12.5 |
| 2003– **cash** | +3.0 | **−4.8** | **+7.8** | 12.6 |

> **In cash, the sign of the 52-week result is set by the roll calendar.** The same program, the same
> path, the same contracts: at one arbitrary offset it removes 7.8pp of drawdown and at another it
> adds 6.3pp.

**The published alignment is not a flattering one.** On the 2003– sample, `p = 0` gives +19.9 — the
*second lowest of 52*. The original result was never cherry-picked. It was arbitrary, which is the
finding.

## 10.4 The `Psi` column, which changes how §10.1 should be read

The naked book's max drawdown is set in **2009**, in both samples. The hedged book's is not:

| tenor | acct | modal episode, 1993– | modal episode, 2003– |
|---|---|---|---|
| 4w | marked | 2009 (4/4) | 2009 (4/4) |
| 13w | marked | 2009 (6/13) | 2009 (13/13) |
| 26w | marked | **2003 (25/26)** | 2009 (26/26) |
| 52w | marked | **2003 (51/52)** | 2009 (39/52) |
| 52w | cash | 2009 (37/52) | 2009 (39/52) |

**On the full sample, in marks, at 26 and 52 weeks, "drawdown bought" is a difference between two
different episodes.** The hedged book's worst drawdown is the 2000–03 decline — which a rolled put
program barely touches — while the naked book's is 2008–09. So `+16.8pp` does not mean "the 2008
drawdown was 16.8pp shallower". It means **the 2008 trough was pushed below the 2003 trough, and the
statistic then stopped measuring 2008 at all.**

This is the extreme-value pathology the charter names, appearing in the wild: `max` is censored from
below by the next-deepest episode, so protection beyond that point is invisible in the coordinate,
and the reported number is bounded by the distance between two unrelated episodes.

**The 2003– subsample is the control, and it is why this does not explain the result away.** That
sample excludes the dot-com decline, the episodes match (2009 for both books at 13w, 26w, and 39/52
phases at 52w), and the marked ratio there is **0.85** — still MARGINAL, still nowhere near
SURVIVES. **The phase sensitivity is real and is not an artifact of episode switching.**

## 10.5 Predictions, scored

- **`R(52w) > 1` under marked accounting on the full sample — REFUTED.** It came in at 0.71.
  *Post-hoc, and labelled as such:* §10.4 supplies the reason — on the full sample the marked
  statistic is pinned to the 2003 trough, so no alignment can push it much further and the spread is
  compressed by censoring. The prediction was about the 2008 window; the coordinate had stopped
  reporting on the 2008 window.
- **`separation > 0` marked and `<= 0` cash — CONFIRMED**, both samples, both signs as predicted.
- **"Spread grows with tenor", asserted in §2 as derivable and carrying no information — REFUTED,
  and it should never have been called derivable.** Full-sample marked spreads run 11.8 (4w), 12.6
  (13w), **14.1 (26w)**, 12.7 (52w). Not monotone, and the widest is 26w. Block length bounds *how
  far* an alignment can slip; it does not determine how much the outcome moves, because that depends
  on the fine structure of the decline — whether a given window happens to contain October 2008.
  **A 4-week program has a spread of 11.8pp on four alignments.** Filed as a §2 error, not a finding.

## 10.6 What E1 establishes, and what it does not

**Establishes.**

- **The tenor result is materially dependent on an arbitrary roll-calendar alignment.** Killed in
  cash in both samples; marginal in marks in both; never survives.
- **In cash, even the sign is alignment-dependent** at 52 weeks, and the tenor *ordering* is
  alignment-dependent too.
- **In marks, the ordering is robust** to alignment — 56 of 56 alignments — while its magnitude is
  not.
- **Roll phase must be a declared coordinate of every future row.** It was never chosen; it fell out
  of the sample's first date.

**Does not establish.**

- **Nothing about a second crisis.** The 52 phases are 52 overlapping views of one episode. Per §7,
  no standard error, no confidence interval, no mean-as-estimate has been computed, and none may be.
  **Effective n on the benefit side is still 1.** The spread does not make the published number
  uncertain — it makes it arbitrary.
- **Nothing about timing, signals or conditioning.** No rule here conditions on anything; the phase
  is swept exhaustively, not selected. The prediction program stays closed.
- **No new magnitude.** E1 produces no number that may be quoted as an effect. It removes one.

## 10.7 Consequences booked

1. [[closed-research/intervention/CHARTER-INTERVENTION|CHARTER-INTERVENTION]] §4 — H2's phase clause: **killed in cash, marginal in marks.** The tenor-ordering
   clause of H2 survives in marks only.
2. [[PROBLEM-MAP]] §1.1 — the tenor table carries the phase range and the episode `Psi`; E10's
   magnitude is withdrawn from quotation in both accountings.
3. [[closed-research/intervention/CHARTER-INTERVENTION|CHARTER-INTERVENTION]] §9 — E1 closed. **No experiment is triggered automatically.** E2 and E3 stay where
   they are, and the decision about what runs next is recorded as open.
4. One observation belongs to E2 and is parked there rather than pursued here: max drawdown is
   censored from below by the next-deepest episode, which is an argument about the *coordinate* and
   is exactly what E2's per-excursion depths and CDaR curve exist to replace.

## Related

- [[closed-research/intervention/CHARTER-INTERVENTION|CHARTER-INTERVENTION]] §4 H2 — the hypothesis · §9 E1 — the queue entry
- [[closed-research/intervention/STUB-E0-M3-DECOMPOSITION]] — E0, which promoted this and supplied the cash accounting
- [[docs/RESEARCH-PROTOCOL]] §0 — the gate · [[POINT-IN-TIME-DISCIPLINE]] — the leak register
- [[docs/literature/README]] — Israelov (2017), and the process failure that respecified this experiment
