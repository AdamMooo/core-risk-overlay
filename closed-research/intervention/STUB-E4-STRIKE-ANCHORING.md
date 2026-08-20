# §0 Stub — E4, strike anchoring as pure path geometry

> **CLOSED BRANCH — PRESERVED AS EVIDENCE, NOT AS A DESIGN.** This preregistration belongs to the
> rolled-put / tenor intervention program, closed 2026-08-18
> ([[closed-research/intervention/README]]). It is kept intact because its result is evidence and
> because a stub edited after the fact is worthless. **Nothing in it is a queued experiment, and its
> code now lives at `closed-research/intervention/`.** The active program is [[CHARTER]].


Committed 2026-08-18, **before any code**, under [[docs/RESEARCH-PROTOCOL]] §0 and [[closed-research/intervention/CHARTER-INTERVENTION|CHARTER-INTERVENTION]] §8.
Status: preregistration. Results are appended below in a later commit, and nothing above the results
rule may be edited once they exist.

**What E4 is not.** It is **not an attempt to rescue the put-overlay hypothesis.** The economic
hypothesis for rolled outright puts is **provisionally negative** — E9 (0 of 40 structures beat the
naked book on compound return), E0 (82–85% of the measured reduction is unrealised mark), E1 (the
magnitude is smaller than the spread from an arbitrary roll offset, and in cash the sign flips with
it), E2 (no tenor ordering survives in cash anywhere on the drawdown path; in cash the programme
*deepens* episodes in 72–84% of pairs). **Those results stand and E4 cannot revise them**, because E4
prices nothing and pays no premium.

**What E4 is.** M1 — strike anchoring versus re-striking — is the single claim that survived E0, E1
and E2, and it survived as *contract geometry* ([[closed-research/intervention/CHARTER-INTERVENTION|CHARTER-INTERVENTION]] §9.1). It has only ever been observed on
one path, inside a priced simulator, on a coordinate that turned out to be broken. E4 tests it where
it actually lives: **as arithmetic on price paths, across genuinely distinct historical episodes and
markets, with no option data of any kind.**

---

## 1. The claim, stated as arithmetic

Over a horizon `H` from a start `t0`, at matched notional (one unit of index at every instant in both
legs) and matched moneyness `m`, comparing **gross intrinsic payoffs only**:

```
anchored     P_A(t0)     = max( (1-m)·S(t0) - S(t0+H) , 0 )

re-striking  P_R(t0, s)  = SUM over i = 0 .. H/s - 1  of
                           max( (1-m)·S(t0 + i·s) - S(t0 + (i+1)·s) , 0 )
```

**No premium, no implied volatility, no pricing model, no monetisation rule, no signal, no
conditioning.** Both legs are functions of the price path and `m` alone.

### 1.1 The mechanism is the deductible, and this is derivable

Write `a_i = S(t0+i·s) - S(t0+(i+1)·s)` for the decline over sub-period `i`, so `SUM a_i = S(t0) -
S(t0+H)`. **At `m = 0`:**

```
P_R = SUM max(a_i, 0)  >=  max( SUM a_i , 0 ) = P_A
```

the positive part of a sum never exceeds the sum of positive parts. **So with no deductible the
re-striking leg weakly dominates, always, on every path.** M1 is therefore *not* the claim that long
contracts protect better. It is:

> **A deductible of `m·S` charged ONCE beats the same deductible charged `H/s` times — when the
> decline is persistent enough that both legs would have paid anyway.**

When every leg finishes in the money the difference is an exact identity:

```
P_A - P_R  =  m · ( SUM_i S(t0 + i·s)  -  S(t0) )
```

`H/s - 1` extra deductibles, priced at the levels the market re-strikes to. **Both statements above
are derivable, carry no information, and are recorded rather than tested** ([[docs/RESEARCH-PROTOCOL]] §0
rule 2). They also bound the effect: it is zero at `m = 0` and scales with `m`.

### 1.2 What is therefore actually open

**Which regime real declines belong to, and how consistently, across episodes and markets that do not
share a decade.** A monotone grind favours anchoring by the identity above; a V-shape favours
re-striking, because the anchored contract can expire above its strike having paid nothing while each
short leg collects its own segment. **That is an empirical question about the shape of historical
declines and it is the only thing E4 measures.**

### 1.3 What E4 cannot say, stated before it runs

**A gross-payoff comparison is exactly the comparison that flatters the anchored leg**, because the
anchored contract is the more expensive one and its cost is omitted here by construction. **E4
therefore establishes nothing about whether any overlay is worth buying, at any tenor.** If M1
survives, what survives is a mechanism, not a recommendation; [[closed-research/intervention/CHARTER-INTERVENTION|CHARTER-INTERVENTION]] §9.1's forbidden sentences
continue to apply in full.

## 2. Claim tuple

```
frequency   weekly closes, W-FRI, resampled from daily (start-date invariant)
horizon     H = 52 weeks primary, 104 declared as robustness
functional  gross intrinsic payoff difference P_A - P_R, reduced to its SIGN.
            No population-average magnitude is reported anywhere in E4
sample      four indices, deliberately non-contemporaneous:
              ^GSPC  1927-12-30 -   ~5,150 weeks   the escape from one episode
              ^N225  1965-01-08 -   ~3,210 weeks   a different bubble and a
                                                   thirty-year bear market
              ^FTSE  1984-01-06 -   ~2,225 weeks
              ^GDAXI 1988-01-01 -   ~2,015 weeks
design      every week with a complete horizon is a start. NO start is chosen,
            and in particular NO start is placed at an episode peak
```

**Declared before the run, none of it selectable afterwards:**

```
m             0.10 primary; 0.05 and 0.15 as declared robustness
s             4, 13, 26 weeks
episodes      excursions of the INDEX ITSELF, threshold 0.20 primary and 0.10
              robustness -- INHERITED from E2 unchanged, not re-chosen for E4
membership    a start belongs to an episode if [t0, t0+H] intersects the
              episode's [peak, recovery] window
```

### 2.1 No hindsight, by construction

**Anchoring "at the peak" is clairvoyant and is excluded.** A real programme rolls on a calendar and
cannot know a peak is a peak. Every start in the grid is an ordinary week; the episode structure is
used only to *group* results afterwards, never to place a start. This is the same discipline that
made E1's phase sweep exhaustive rather than selective.

## 3. Predicted outcome, with its reason

**Derivable, recorded, not tested:** §1.1 in full — `m = 0` gives re-striking weak dominance, the
identity when all legs finish in the money, and the effect scaling with `m`.

**The informative part, predicted in advance.**

> **Prediction: M1 survives — the episode vote flips in fewer than 1/3 of episodes — and the failures
> are concentrated in fast V-shaped declines, with 2020 and 1987 voting AGAINST it at `H = 52`.**

Reason: a 52-week contract struck in February 2020 expires in February 2021, well above its strike,
having paid nothing, while four-week legs collect the March collapse as it happens. The same holds
for October 1987. **This prediction is worth recording because it is the exact complement of E0's
finding** — 2020 showed +24.9pp of *marked* protection and −0.0pp in cash — and if it holds, the
episodes where anchoring fails on payoff geometry are the same episodes where the marked-versus-cash
gap was widest.

**Secondary prediction:** the vote is more favourable to anchoring at `H = 104` and at larger `m`,
both by §1.1.

**Genuinely uncertain:** Japan. A thirty-year grinding bear is the most favourable possible terrain
for anchoring by the identity, but it is also the market whose declines are slowest relative to a
52-week contract, so a fixed `H` may straddle recoveries repeatedly.

## 4. Literature

Israelov (2017) `[skim]` measures protective-put drawdown outcomes over rolling windows and does not
separate the deductible-count mechanism from pricing; its comparison is against divestment, which
[[closed-research/intervention/CHARTER-INTERVENTION|CHARTER-INTERVENTION]] §2 C2 excludes. **No paper settles the deductible-count identity of §1.1**, which is in
any case arithmetic rather than an empirical claim. Nothing in the reading list gates E4, and no new
reading is required for it — recorded explicitly so that "no gate" is a finding rather than an
omission, after E0 skipped one.

## 5. Mechanism for a difference

**Structural difference.** The two legs differ in *where the strike sits relative to the path's
starting level*: one strike anchored at `t0`, versus `H/s` strikes each re-anchored to whatever the
market has already fallen to. That is the whole of M1 and it involves no pricing.

**Horizon at which it is observable:** `H` weeks, concentrated in persistent declines.

**Functional on which it is observable:** the sign of the gross payoff difference. **Invisible at
`m = 0`** — where the ordering reverses deterministically — which is the sharpest available statement
of what the mechanism actually is.

## 6. What would surprise me, and what it changes

- **M1 failing** (flips in ≥ 1/3 of episodes) would **close the rolled-put/tenor branch**: the last
  surviving claim from E9/E10 would be gone, and the negative result would be recorded as final for
  this instrument class.
- **M1 surviving in every market including Japan** would be the strongest structural result the repo
  has, and it would still not license a pricing or monetisation experiment — see §1.3 and the
  stopping rule in §9.
- **A clean split by decline shape** — anchoring winning in grinds and losing in V-shapes — would
  mean M1 is real but conditional on a path property nobody can observe in advance, which is a
  materially weaker claim than "M1 holds".

## 7. Identification

**Preserved from [[closed-research/intervention/CHARTER-INTERVENTION|CHARTER-INTERVENTION]] §5, unchanged, because nothing about E4 relaxes it.**

- **Episodes are not draws from a superpopulation.** Market structure, monetary regime and index
  composition differ across 1929, 1987, 2000-02, 2008-09, 2020 and 2022. Cross-episode work
  establishes **robustness of a mechanism** and can **falsify** a magnitude. It cannot **estimate**
  one.
- **Four markets are not four independent replications.** Global equity co-movement is high and
  rising; 2008 and 2020 appear in all four series, and 1987 in two. **Cross-market agreement in those
  windows is close to one observation reported four times.** The genuinely independent content is
  where the calendars do *not* overlap: US 1929-1954, Japan 1990-2003.
- **Overlapping starts are description, never inference** ([[docs/RESEARCH-PROTOCOL]] §2). There are
  thousands of starts and they share nearly all their data. **`n_starts` is not a sample size**, and
  the fraction of starts favouring a leg is a descriptive count, not a probability.
- **No standard error, no test statistic, no confidence interval, and no population-average payoff
  difference.** Sign and ordering only, exactly as [[closed-research/intervention/CHARTER-INTERVENTION|CHARTER-INTERVENTION]] §4 requires of every active
  hypothesis.

**What E4 can add that E0-E2 could not:** genuinely distinct *episodes*. The benefit side of the
priced work had effective n = 1. Here the count is the number of independent declines, and it is
larger — perhaps 15-25 across four markets, with the caveat above about overlap. **This raises the
episode count. It does not create a population.**

## 8. Verdict rule, fixed in advance

**H1** ([[closed-research/intervention/CHARTER-INTERVENTION|CHARTER-INTERVENTION]] §4): *strike anchoring (M1) dominates re-striking for a multi-month drawdown at
equal premium budget* — tested here at equal notional and zero premium, which is the payoff-geometry
half of it.

```
per start      sign of  P_A - P_R
episode vote   the episode votes FOR M1 if P_A >= P_R at >= 1/2 of the starts
               whose horizon intersects it
KILLED         the vote flips in >= 1/3 of episodes, pooled across markets
               (CHARTER H1's own kill condition, unchanged)
SURVIVES       flips in < 1/3
```

Reported **per market and per episode**, never pooled into a single number without the breakdown.
The unconditional all-starts fraction is reported as *context only* and is explicitly labelled
description, not inference.

### 8.1 Amendment, made BEFORE any code ran — ties, and the asymmetry they create

Noticed while writing the implementation and recorded here rather than discovered afterwards. **No
run has happened at the time of this amendment** (git history is the evidence: the stub commit
precedes `research/anchoring.py` entirely).

**The defect.** `P_A >= P_R` counts a tie as a vote FOR M1, and the overwhelmingly common case is
`P_A = P_R = 0` — any start whose horizon sits in rising or flat prices. Episode windows include
their recovery leg, so they contain many such starts. The preregistered rule is therefore **biased
toward M1 surviving**, and the bias grows with how much of an episode window is recovery.

**What changes, and what does not.**

- **The kill condition is unchanged and still keys on the preregistered rule.** Changing a verdict
  rule while writing the code that will test it is exactly the move [[docs/RESEARCH-PROTOCOL]] §0 exists
  to prevent, and the rule was fixed in advance.
- **Two additional numbers are reported beside it, as `Psi`:** the count of **informative starts**
  (at least one leg strictly positive) and the vote **among informative starts only**.
- **The verdict is asymmetric, and this is now stated in advance.** Because the rule is biased toward
  survival: **a KILL is strong evidence and a SURVIVAL is weak.** If M1 survives under the
  preregistered rule but loses the informative-start vote, that is reported as **survival on a biased
  rule, contradicted on the diagnostic** — and it is not to be quoted as M1 holding.


## 9. Exact outputs, and the stopping rule

```
1  the grid: markets, spans, episode counts at both thresholds
2  per-episode votes, per market, at the primary (H=52, s=4, m=0.10)
3  the flip count against the 1/3 kill condition
4  robustness: the same vote count at H=104, at s=13 and 26, at m=0.05 and 0.15
5  the m=0 control -- re-striking must dominate, or the implementation is wrong
6  Psi: episode counts, calendar overlap between markets, starts per episode
7  verdict
```

**Stopping rule, binding, written before the result is known.**

- **If M1 fails:** close the rolled-put/tenor branch, record the negative result in [[closed-research/intervention/CHARTER-INTERVENTION|CHARTER-INTERVENTION]] and
  [[PROBLEM-MAP]], and stop.
- **If M1 survives:** **stop anyway.** The next question — whether the mechanism is important enough
  to justify investigating its economic implementation — is a decision about the programme, not an
  experiment, and it is not taken inside E4. **No pricing, no monetisation, no additional structures,
  and no automatic progression to E5, E6 or E7.**

New code: `research/anchoring.py` and nothing else. `data_loader.download_weekly_prices` already
provides a start-date-invariant W-FRI grid across tickers and is reused unchanged. **The payoff
arithmetic gets its own tests**, including the `m = 0` dominance identity and the monotone-decline
identity, because it is the only new arithmetic in the experiment.

---
--- RESULTS RULE. Everything above was committed 2026-08-18 in 277cf7a, amended in
--- 93f980b, both before `research/anchoring.py` existed. Nothing above has been edited since.
---

# §10 Results — 2026-08-18

Run: `.venv\Scripts\python.exe research/anchoring.py`.
New code: `research/anchoring.py`. `data_loader.download_weekly_prices` reused unchanged. Checks:
**52 passing**, six of them new and specific to the payoff arithmetic. Run before and after.

Data: **^GSPC 1927-12-30 (5,147 weeks), ^N225 1965 (3,213), ^FTSE 1984 (2,225), ^GDAXI 1988
(2,016)** — 12,601 weekly observations, 29 episodes at the 20% threshold and 62 at 10%.

## 10.1 The verdict, in the order the stub requires it be read

| | |
|---|---|
| **Preregistered rule (§8)** | **M1 SURVIVES** — the episode vote flips in **4 of 29** episodes = **13.8%**, against a 1/3 kill line |
| **Declared diagnostic (§8.1)** | **CONTRADICTED** — excluding starts where both legs pay zero, the vote flips in **15 of 28** = **54%**. A majority of episodes votes *against* M1 |
| **Therefore** | per §8.1, fixed before the run: *"If M1 survives under the preregistered rule but loses the informative-start vote, that is reported as survival on a biased rule, contradicted on the diagnostic — and it is not to be quoted as M1 holding."* |

**The amendment earned its place.** The gap between 13.8% and 54% is entirely the ties: starts whose
horizon sits in flat or rising prices, where both legs pay zero and the rule scores that as a vote
*for* M1. Had the amendment not been written before the run, 13.8% would have been the headline.

## 10.2 The deductible is the whole mechanism, and the sweep shows it

Flip share on the informative diagnostic — **higher is worse for M1** — at `H = 52`:

| `m` | `s = 4` (thr 20% / 10%) | `s = 13` | `s = 26` |
|---|---|---|---|
| **5%** | **100% / 100%** | 100% / 100% | 83% / 90% |
| **10%** | 54% / 61% | 76% / 77% | 76% / 76% |
| **15%** | 40% / 45% | 59% / 70% | 69% / 74% |

> **At a 5% deductible, M1 fails in every single episode, in every market, at `s = 4` and `s = 13`.**

This is §1.1's derivation appearing in the data exactly as written: the advantage is `m · (Σ
re-strike levels − S₀)`, it vanishes as `m → 0`, and at `m = 0` the ordering reverses
deterministically. **M1 is not a property of long contracts. It is a property of large deductibles.**

The `s` dimension agrees: the advantage scales with the *number* of extra deductibles, `H/s − 1`. At
`s = 26` there is one extra deductible and M1 flips in 69–90% of episodes; at `s = 4` there are
twelve and it flips in 40–61%.

## 10.3 The shape split, which is the actual finding

Per-episode informative votes at the primary grid. **Anchoring wins slow grinds and loses fast
crashes**, without exception worth the name:

| votes **FOR** M1 — persistent declines | | votes **AGAINST** M1 — V-shapes and crashes | |
|---|---|---|---|
| S&P 1973–80 | 87/134 = 65% | **S&P 2020** | **0/53 = 0%** |
| S&P 2000–07 | 98/137 = 72% | **DAX 2020** | **0/53 = 0%** |
| DAX 2000–07 | 109/174 = 63% | DAX 1998 | 0/69 = 0% |
| Nikkei 1989–2024 | 481/862 = 56% | Nikkei 1970 | 1/94 = 1% |
| FTSE 1999–2015 | 164/289 = 57% | FTSE 1998 | 1/31 = 3% |
| S&P 2021–23 | 26/35 = 74% | S&P 1987 | 5/54 = 9% |
| S&P 1968–72 | 48/63 = 76% | FTSE 1987 | 8/62 = 13% |
| S&P 1961–63 | 30/48 = 63% | S&P 2008 | 58/142 = 41% |
| | | S&P 1929–54 | 275/576 = 48% |

**2020 is the cleanest result in the run: zero of 53 informative starts favoured anchoring, in two
independent markets.** A contract struck in February 2020 expired in February 2021 above its strike,
having paid nothing, while four-week legs collected the March collapse as it happened.

## 10.4 And the split routes straight into the closed programme

The condition that decides M1 is **whether the coming decline is a grind or a V** — that is, its
persistence relative to the horizon. That property is not observable at the moment the contract must
be bought.

> **To exploit M1 you would have to forecast the shape of a decline before it happens. That is the
> prediction problem this repository closed** ([[PROBLEM-MAP]] Part I), and [[PARKED]]'s
> permanently-closed list forbids reopening it.

So M1 is real, conditional, and **unusable without the one thing the programme has established it
does not have.** This is the third of the three outcomes named in §6 — "M1 is real but conditional on
a path property nobody can observe in advance, which is a materially weaker claim than *M1 holds*" —
and it is the one that landed.

## 10.5 Predictions, scored

- **"M1 survives, flips < 1/3" — CONFIRMED on the preregistered rule** (13.8%), and **contradicted on
  the diagnostic** (54%). Recorded as both, in that order.
- **"Failures concentrated in fast V-shapes, with 2020 and 1987 voting AGAINST" — CONFIRMED, sharply.**
  2020 at 0/53 in two markets; 1987 at 5/54 (S&P) and 8/62 (FTSE).
- **"More favourable at larger `m`" — CONFIRMED**, monotonically: 100% → 54% → 40% flips as `m` goes
  5% → 10% → 15%.
- **"More favourable at `H = 104`" — REFUTED.** The diagnostic flip share *rises* to 89–98%. My §3
  reasoning counted the extra deductibles (`H/s − 1` grows with `H`) and forgot the other side: a
  two-year contract has two years in which the market can recover above its strike and pay nothing.
  The deductible-count intuition is only half the mechanism, and the stub asserted it as though it
  were the whole one.

## 10.6 `Psi`

- **29 episodes is not 29 observations.** Block 6's overlap table: the 2000–07, 2008, 2020 and 2022
  windows appear in three or four markets each, and are **one event reported several times**. Only
  five episodes have no calendar overlap with another market at all — S&P 1929–54, 1956–58, 1961–63,
  1980–82 and Nikkei 1965. **The genuinely independent content is US 1929–1954 and Japan 1990–2003.**
- **Two mega-episodes dominate the start counts.** The excursion definition runs peak-to-full-
  recovery, so S&P 1929–54 is one 25-year "episode" (1,358 starts) and Nikkei 1989–2024 is one
  34-year one (1,833 starts) — together 42% of all starts at the primary threshold. That is a known
  limitation of the inherited definition. **It was not re-tuned after seeing the result**, because
  choosing episode boundaries from an outcome is precisely what §0 forbids.
- **Starts overlap almost completely.** `n_starts` is not a sample size, the vote shares are
  descriptive counts, and **no standard error, test statistic, confidence interval or population-
  average payoff difference appears anywhere in E4** — as declared in §7.
- **The `m = 0` control passed exactly:** `max(anchored − restriking) = 0.00e+00` in all four
  markets, at every `H` and `s`. The implementation reproduces the dominance identity to the bit.

## 10.7 What E4 establishes, and what it does not

**Establishes.**

- **M1 is a deductible-count effect, not a tenor effect.** It vanishes at `m = 0` by identity and
  fails in 100% of episodes at `m = 5%`. Any statement of it that does not name the deductible is
  wrong.
- **M1 is conditional on decline shape**, holding in persistent grinds and failing in V-shaped
  crashes, across four markets and a century — including 0/53 in 2020 in two markets independently.
- **The condition is not observable in advance**, and observing it would be the closed prediction
  problem.
- **The preregistered verdict is SURVIVES and the declared diagnostic contradicts it.** Both are
  recorded; neither is suppressed; the §8.1 asymmetry decides how they combine.

**Does not establish.**

- **Nothing economic. No premium was paid anywhere in E4.** The gross-payoff comparison omits the
  anchored leg's higher cost by construction — the comparison that flatters it — and it still could
  not win on the diagnostic at the primary grid. **E9, E0, E1 and E2 stand entirely unchanged, and
  the economic hypothesis for rolled outright puts remains provisionally negative.**
- **No population claim.** Episodes are not draws from a superpopulation; four markets are not four
  replications; overlapping starts are description, never inference. Effective independent episodes:
  perhaps 12–15, not 29.
- **Nothing about instruments other than a rolled outright put**, and nothing about timing: no rule
  in E4 conditions on anything.

## 10.8 The stopping rule, honoured

**E4 stops here.** No pricing, no monetisation, no additional structures, and **no progression to E5,
E6 or E7** — the rule was written into §9 before the result was known and the result does not change
it.

**The branch decision is not taken inside E4.** The outcome is neither the clean failure that §9 says
closes the rolled-put/tenor branch nor the clean survival that §9 says triggers a reassessment: the
preregistered rule says SURVIVES, the diagnostic declared in advance contradicts it, and what remains
is a conditional mechanism that cannot be acted on without a forecast the programme has closed.
**That is a decision about the programme, and it is recorded as open.**

## Related

- [[closed-research/intervention/CHARTER-INTERVENTION|CHARTER-INTERVENTION]] §4 H1 — the hypothesis · §9 E4 — the queue entry · §9.1 — what survived E0-E2
- [[closed-research/intervention/STUB-E2-DRAWDOWN-PATH]] · [[closed-research/intervention/STUB-E1-ROLL-PHASE]] · [[closed-research/intervention/STUB-E0-M3-DECOMPOSITION]]
- [[docs/RESEARCH-PROTOCOL]] §0 — the gate · [[POINT-IN-TIME-DISCIPLINE]] — the leak register
