# §0 Stub — E1, the roll-phase sweep

Committed 2026-08-18, **before any code**, under [[RESEARCH-PROTOCOL]] §0 and [[CHARTER]] §8.
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
inadmissible under [[CHARTER]] §2 C2, so its verdict does not transfer while its mechanism does.

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

**H2** ([[CHARTER]] §4), phase clause only: *the phase spread is small relative to the effect.*

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

## Related

- [[CHARTER]] §4 H2 — the hypothesis · §9 E1 — the queue entry
- [[STUB-E0-M3-DECOMPOSITION]] — E0, which promoted this and supplied the cash accounting
- [[RESEARCH-PROTOCOL]] §0 — the gate · [[POINT-IN-TIME-DISCIPLINE]] — the leak register
- [[literature/README]] — Israelov (2017), and the process failure that respecified this experiment
