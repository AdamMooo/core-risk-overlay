# §0 Stub — E4, strike anchoring as pure path geometry

Committed 2026-08-18, **before any code**, under [[RESEARCH-PROTOCOL]] §0 and [[CHARTER]] §8.
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
and E2, and it survived as *contract geometry* ([[CHARTER]] §9.1). It has only ever been observed on
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
are derivable, carry no information, and are recorded rather than tested** ([[RESEARCH-PROTOCOL]] §0
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
survives, what survives is a mechanism, not a recommendation; [[CHARTER]] §9.1's forbidden sentences
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
[[CHARTER]] §2 C2 excludes. **No paper settles the deductible-count identity of §1.1**, which is in
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

**Preserved from [[CHARTER]] §5, unchanged, because nothing about E4 relaxes it.**

- **Episodes are not draws from a superpopulation.** Market structure, monetary regime and index
  composition differ across 1929, 1987, 2000-02, 2008-09, 2020 and 2022. Cross-episode work
  establishes **robustness of a mechanism** and can **falsify** a magnitude. It cannot **estimate**
  one.
- **Four markets are not four independent replications.** Global equity co-movement is high and
  rising; 2008 and 2020 appear in all four series, and 1987 in two. **Cross-market agreement in those
  windows is close to one observation reported four times.** The genuinely independent content is
  where the calendars do *not* overlap: US 1929-1954, Japan 1990-2003.
- **Overlapping starts are description, never inference** ([[RESEARCH-PROTOCOL]] §2). There are
  thousands of starts and they share nearly all their data. **`n_starts` is not a sample size**, and
  the fraction of starts favouring a leg is a descriptive count, not a probability.
- **No standard error, no test statistic, no confidence interval, and no population-average payoff
  difference.** Sign and ordering only, exactly as [[CHARTER]] §4 requires of every active
  hypothesis.

**What E4 can add that E0-E2 could not:** genuinely distinct *episodes*. The benefit side of the
priced work had effective n = 1. Here the count is the number of independent declines, and it is
larger — perhaps 15-25 across four markets, with the caveat above about overlap. **This raises the
episode count. It does not create a population.**

## 8. Verdict rule, fixed in advance

**H1** ([[CHARTER]] §4): *strike anchoring (M1) dominates re-striking for a multi-month drawdown at
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

- **If M1 fails:** close the rolled-put/tenor branch, record the negative result in [[CHARTER]] and
  [[PROBLEM-MAP]], and stop.
- **If M1 survives:** **stop anyway.** The next question — whether the mechanism is important enough
  to justify investigating its economic implementation — is a decision about the programme, not an
  experiment, and it is not taken inside E4. **No pricing, no monetisation, no additional structures,
  and no automatic progression to E5, E6 or E7.**

New code: `research/anchoring.py` and nothing else. `data_loader.download_weekly_prices` already
provides a start-date-invariant W-FRI grid across tickers and is reused unchanged. **The payoff
arithmetic gets its own tests**, including the `m = 0` dominance identity and the monotone-decline
identity, because it is the only new arithmetic in the experiment.

## Related

- [[CHARTER]] §4 H1 — the hypothesis · §9 E4 — the queue entry · §9.1 — what survived E0-E2
- [[STUB-E2-DRAWDOWN-PATH]] · [[STUB-E1-ROLL-PHASE]] · [[STUB-E0-M3-DECOMPOSITION]]
- [[RESEARCH-PROTOCOL]] §0 — the gate · [[POINT-IN-TIME-DISCIPLINE]] — the leak register
