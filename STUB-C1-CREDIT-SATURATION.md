# STUB C1 — Credit saturation test

**Status:** pre-registration, written before any code. **Created 2026-10-25.** The first run under
the re-opened repository ([[CLAUDE]] 2026-10-25 policy change). This stub exists to pass the gate in
[[docs/RESEARCH-PROTOCOL]] §0 — not to assert a finding.

**C1** names it: the first candidate under the "credit as a non-return observable" branch
([[docs/LESSONS-LEDGER]] §6 row 1). The branch is a **measurement** programme ([[CLAUDE]] §4
column 2), not prediction, not intervention. **The whole branch is gated by this one experiment.**

---

## The seven fields

### 1. Claim tuple — `(frequency, horizon, functional, sample, null)`

- **Frequency:** daily, non-overlapping weekly aggregation reported as a robustness check.
- **Horizon:** contemporaneous (t vs t), no lead/lag claim. This is a saturation test, not a
  forecasting test.
- **Functional:** incremental R² of HY OAS changes (ΔOAS) in a regression of a public risk-measurement
  target on {ΔVIX, trailing-60d SPY realized vol}, with ΔOAS added last.
- **Sample:** 1996-12-31 to a cut date committed before the run (see §7). FRED
  `BAMLH0A0HYM2` (ICE BofA US High Yield OAS). SPY/VIX from the existing cached loaders.
- **Null:** ΔHY OAS is spanned by {ΔVIX, trailing SPY RV} — incremental R² ≤ 0.02 and
  partial-F p ≥ 0.05.

### 2. Predicted outcome, with reason, before any code

**Prediction (point):** incremental R² of ΔHY OAS over {ΔVIX, RV_60} is **in the range 0.05 – 0.20**;
the null is **rejected**.

**Reason:** Gilchrist–Zakrajšek (2012) decompose corporate bond spreads into a default-expectation
component and an "excess bond premium" (EBP) that moves with intermediary risk appetite and leads
real activity. If any portion of that EBP is contemporaneously uncorrelated with equity-side
volatility, saturation fails. The weaker literature prior — that credit and equity vol are strongly
coupled during stress but decouple in normal regimes — predicts a *small but non-zero* incremental R²
driven mostly by crisis windows. Both priors predict rejection.

**Confidence:** moderate. **The run therefore carries information** — a non-rejection would be the
informative outcome, because it would close the whole branch cheaply ([[CLAUDE]] §6.9).

### 3. Literature check

**Primary:**
- Gilchrist, S. & Zakrajšek, E. (2012). *Credit Spreads and Business Cycle Fluctuations.* AER 102(4).
  Introduces the EBP. **Not yet read in full for this programme.**
- López-Salido, D., Stein, J. C. & Zakrajšek, E. (2017). *Credit-Market Sentiment and the Business
  Cycle.* QJE 132(3). EBP as a predictor of real activity. **Not yet read.**

**Secondary / background:**
- Collin-Dufresne, Goldstein & Martin (2001). *The Determinants of Credit Spread Changes.* JF 56(6).
  The canonical reference that *equity-market variables leave most of the variation in credit
  spreads unexplained* — the paper this experiment is effectively replicating in reverse.
- Krishnamurthy & Muir (2017). *How Credit Cycles across a Financial Crisis.* NBER WP 23850.

**Pre-run reading commitment:** Gilchrist–Zakrajšek (2012) §I–II and Collin-Dufresne et al. (2001)
abstract + §I before any regression is run. Both logged into `docs/literature/` with the
`[UNREAD] → [READ]` discipline from [[literature/README]].

**Known-settled check:** Collin-Dufresne et al. (2001) establishes that equity-market variables
(including vol) explain a *minority* of credit-spread variation (~25% on their sample). If their
finding transfers to the 1996–present FRED series at daily frequency, our prediction (§2) is
settled by them and this run would be a confirmation rather than a discovery. **That is still
useful** — it imports a published result onto this repo's data, which is what [[CLAUDE]] §6.5
asks for — but the stub must be clear this is reproduction of a settled finding, not a new one.

### 4. Mechanism for a difference, with horizon and functional

**Structural difference:** VIX and SPY RV are both functionals of the equity return path.
HY OAS is set in the corporate bond market and prices default probability, recovery expectations,
and risk appetite of a different investor base (bond funds, insurers) with different mandates and
leverage constraints than equity market-makers. The information sets overlap but are not nested in
either direction.

**Horizon at which it becomes observable:** daily. Both VIX and HY OAS respond to macro news within
the trading day; weekly aggregation would blur the identification.

**Functional on which it becomes observable:** first differences (ΔOAS, ΔVIX). Levels are
non-stationary and share common trends (both decline over 1996–2007); differences strip the shared
trend without washing out the saturation structure.

### 5. What would surprise me, and what it changes

| outcome | reaction |
|---|---|
| Incremental R² ≥ 0.05, p < 0.05 (predicted) | **The branch opens.** Charter the next experiment: what *specifically* is in credit that equity vol does not see — EBP decomposition, HY vs IG, duration-adjusted spreads. |
| Incremental R² in [0.02, 0.05], p < 0.05 | **Partial survival.** Statistically distinguishable but economically marginal. Report with a scope caveat; next step depends on whether the residual information is concentrated in crises (which would make it an L2 problem). |
| Incremental R² < 0.02, p ≥ 0.05 (null) | **The branch closes.** Credit does not escape the equity-vol information set at this frequency and sample. Pivot to §6 row 2 (jumps/heavy-tails) or §6 row 3 (declared-monetisation path claims). |
| Partial-F significant *only* in the 2007–2009 window, insignificant everywhere else | **Branch closes with a caveat.** Confirms L2 (effective-n wall) rather than opening a new signal. The incremental R² would be a crisis-conditional artefact. |

### 6. Question — A, B, C, or D ([[CHARTER]] §1 / PROTOCOL P3)

**Question A — existence.** *What differs between credit and equity-vol as risk observables?*
Specifically: does credit carry contemporaneous information not spanned by equity vol?

Not B (identification on what population), not C (persistence/OOS), not D (observable at `t`
from `I_t`). Those follow if A survives.

### 7. Identification

- **Population the claim addresses:** US-listed HY credit market vs US equity index vol, 1996-12-31
  to **cut date committed before the run — proposed 2024-12-31** (freeze 2025+ as held-out,
  consistent with [[docs/POINT-IN-TIME-DISCIPLINE]]'s rule that the cut is written before the fit).
- **What is identified in magnitude:** the incremental R² as an estimate of the fraction of ΔOAS
  variance orthogonal to {ΔVIX, RV_60}, under the maintained assumption that the regression is
  correctly specified. HAC standard errors (Newey–West, 10-day bandwidth) for the partial-F.
- **What is NOT identified:** causal direction, state-conditional structure, out-of-sample
  stability, information at the daily-return frequency about *future* equity drawdown. **Any
  conclusion exceeding "ΔOAS is / is not spanned by {ΔVIX, RV_60} on this sample" is out of
  scope for this run** and must appear in a subsequent charter if it appears at all.
- **Multiple-testing budget:** this is one test with one specification. Robustness checks
  (weekly aggregation, 2010–present subsample, IG OAS as a cross-check) are reported but not
  used to reselect the headline specification.

---

## What the experiment actually is

```
Y = ΔHY_OAS_t    (BAMLH0A0HYM2 first differences, bp/day)

Model 0:  Y = α + β_1 · ΔVIX_t + β_2 · RV_60_t + ε            → R²_0
Model 1:  Y = α + β_1 · ΔVIX_t + β_2 · RV_60_t + γ · [extra] + ε

Headline: run the reverse — regress Y_equity_risk_target on
          ΔVIX, RV_60, then add ΔHY_OAS and report incremental R².
```

**The equity-side risk target is a design choice to commit before the run.** Candidates:

- (a) RV_60 forward-looking (next-60d SPY realized vol) — standard forecasting target, but makes
  this a prediction test, which is **not** what C1 is for.
- (b) **Contemporaneous spanning: regress ΔHY_OAS on {ΔVIX, RV_60} directly**, report the R²
  and the complement. This is the saturation test as literally stated by L1. **Choose this.**
- (c) VIX itself as the LHS with ΔHY_OAS, RV_60 as RHS — tests whether credit spans VIX. A
  mirror run; report alongside (b) as a robustness check.

**Chosen specification:** (b) is the headline. (c) is reported for completeness. (a) is a
different experiment (would need its own stub).

## Data provenance

- `BAMLH0A0HYM2`: ICE BofA US High Yield Index Option-Adjusted Spread, daily, FRED. First obs 1996-12-31.
- `BAMLC0A0CM`: ICE BofA US Corporate Index OAS (IG), daily, FRED, for the robustness check.
- SPY, VIX: existing cached loaders in `src/data_loader.py`. Point-in-time discipline per
  [[docs/POINT-IN-TIME-DISCIPLINE]].

All three series must be added to `data/MANIFEST.md` with sha256 before the run, consistent with
the frozen-data rule.

## Firewall check ([[docs/RESEARCH-PROTOCOL]] §0.1)

- **Claim tuple firewall:** the verdict is "ΔHY_OAS *is* / *is not* spanned by {ΔVIX, RV_60} at
  daily frequency on sample S" — nothing more. No "credit predicts drawdowns," no "credit beats
  VIX," no magnitude claim beyond the R² itself. ✓
- **Statistical-vs-economic firewall:** no sentence in the writeup will contain both an R² and
  a cost-benefit judgement. ✓
- **No-magnitude-without-identification firewall:** the R² is identified under the specification;
  no claim about *which* information in credit matters is made from this run. ✓

## Related

- [[CLAUDE]] — 2026-10-25 policy change, re-opens the repository
- [[docs/LESSONS-LEDGER]] §6 row 1 — the branch this stub opens
- [[docs/LESSONS-LEDGER]] §1 L1 — the saturation lesson being tested
- [[docs/RESEARCH-PROTOCOL]] §0 — the gate this stub passes
- [[docs/POINT-IN-TIME-DISCIPLINE]] — time basis and the cut-date rule
