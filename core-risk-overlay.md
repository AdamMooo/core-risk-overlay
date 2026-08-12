---
type: project
---

# Core-Risk-Overlay (Portfolio Thermostat)

Last updated: 2026-08-12

Weekly tail-risk insurance overlay: a 2-regime Markov-switching volatility model on weekly SPY
log returns, whose output scales an OTM SPY put layer. Core equities are never sold.
Mandate and trade mechanics in [[README]]. Math in [[docs/MATH-REFERENCE]].
Time-basis rules in [[docs/POINT-IN-TIME-DISCIPLINE]].

## Status

**Pre-implementation, and deliberately so.** `src/data_loader.py` and `src/jump_model.py` are
written; `src/risk_engine.py` and `main.py` are intentional stubs. No backtest exists. No capital
is deployed. ~200 lines of substantive code total.

The 2026-08-12 review found that the model as written is **not fit to generate a signal yet** —
three separate reasons, all cheap to fix at this size. That is the whole point of having stopped.

## Real-data verdict — 2026-08-12

`diagnostics.py`, real SPY weeklies 1993-02-01..2026-08-10, n = 1750, no gaps. The current
specification is **rejected by the data on four independent axes**:

1. **Its stated rationale is false.** The 2006-2011 persistence pathology the constraints exist to
   prevent does not occur (finding 9). Only the variance *ordering* survives as justified.
2. **The `p[0->0] = 0.98` pin is statistically rejected.** LR stat 14.07 vs chi-sq(1) crit 3.841,
   p = 1.8e-4. Unconstrained `p[0->0]` is 0.923, far *below* the pin.
3. **The constraint set cannot represent what the data shows.** The two constraints jointly cap
   ergodic P(jump) at 11.76%; the empirical filtered jump share is **13.77%**. Not a preference — a
   mathematical impossibility. The 0.85 ceiling binds exactly (`p[1->0] = 0.15000000`).
4. **Two discrete variance levels are insufficient.** ARCH-LM(4) on regime-standardized residuals =
   **41.11, p = 2.5e-8** after absorbing 82% of the raw volatility clustering. Ljung-Box on squared
   residuals rejects at 1e-10; on the *level* at p <= 0.005. Corrected AIC **and** BIC both pick
   **k=3** decisively (-8675.9 / -8621.2); the repo's constrained k=2 ranks **last** among all
   switching specs (-8589.6 / -8567.8).

**What the residuals say the model is missing.** Regime-switching absorbs fat tails superbly —
excess kurtosis 8.08 -> 0.22 (97.3%). What remains is **left skew** (-0.25), and the QQ table shows
the right tail sitting essentially on the Normal line (|diff| <= 0.058 at every percentile >= 75)
while the left tail deviates (-0.13 to -0.33 from p5 to p1). A single non-switching mean cannot
represent asymmetry, which is the same root cause as the melt-up blindness in finding 2.
`switching_trend=True` beats the plain k=2 spec on both corrected AIC and BIC.

**The k=3 result is strategically interesting, not just statistically.** The three fitted volatility
levels are 10.0% / 19.6% / 55.7% annualized, and `p[2->0] = 4.4e-19` — there are **no direct
crisis-to-calm transitions**. Crises are entered and exited only through the middle state. That is a
"building stress" regime, which is exactly the middle tier of [[README]] §4's own risk matrix. The
strategy is specified with three tiers while the model is constrained to two states, and the data
prefers three. Caveats: a transition estimated at zero is a boundary solution, k=3 has 6 label
permutations rather than 2, and 10 parameters on 1750 weekly observations invites overfitting.

**Historical detection is good.** Every named episode fires except SVB 2023-03 (peak 0.58, one week
above 0.5). Highest-mean year is **2022 (0.533)** — above 2009 (0.478) and 2008 (0.426). No false
alarms in calm melt-ups (2017 mean 0.013, zero weeks above 0.5).

**Look-ahead, quantified on real data.** max |filtered - smoothed| = **0.732** (2008-12-22); mean gap
0.086; **139 of 1750 weeks (7.9%) disagree about the 0.5 threshold.** Roughly one week in thirteen
would be assigned a different risk tier. Real, and a one-word fix.

**Duration realism fails in both directions.** Model E[D_jump] = 6.67 wks vs empirical mean run 3.77
(too long) and observed max 15 (too short). Model E[D_calm] = 50 vs empirical mean 23.2. The GFC is
fragmented into an 11-week and a 15-week spell split by a calm interlude at 2008-12-15/22.

## Respecification outcome — 2026-08-12

Applied: persistence constraints dropped, `switching_trend=True`, post-hoc relabeling replacing the
`sorted()` constraint, filtered probabilities. Six freely-estimated parameters, nothing pinned.

**Fixed.** llf 4298.82 -> 4310.94; corrected AIC/BIC better on both (-8609.88 / -8577.07); parameter
count now self-consistent (k_free == k_params, dAIC = dBIC = 0.00); `bse` / `pvalues` / `conf_int()`
are legitimate for the first time, because the fitted point is an interior stationary point in the
full 6-d space; gradient healthy in every coordinate (was exactly `-0.0` in the pinned one) and
`Hinv[0,0]` 1.0 -> 144.5; calm-duration realism improved (1.80x vs 2.15x). The switching mean is
jointly justified (LR `const[0]=const[1]`, stat 10.1751, p = 0.001423).

**Post-hoc relabeling proved load-bearing, not cosmetic.** The jump regime lands on **index 0** in
every real-data fit — full history and the 2006-2011 window, with and without the switching mean.
The old code hardcoded `JUMP_REGIME = 1` and depended on the `sorted()` constraint to make that
true. Removing the constraint without adding relabeling would have **inverted the signal**.

**Got worse — the residual battery.** ARCH-LM(4) 41.11 -> 55.65 (p = 2.372e-11); ARCH-LM(12) 48.91
-> 78.83; Ljung-Box(4) on squares 49.68 -> 69.96; Jarque-Bera 22.04 -> 28.29; excess kurtosis 0.221
-> 0.476. Ljung-Box on the level is unchanged and still rejects at every lag. This was checked
against the possibility of being an artifact of the changed residual construction and is not:
standardizing with a single common mean still gives 64.54 / 52.14, and the plain non-switching-mean
k=2 fit gives 59.15 / 47.82 — all worse than the old 49.68 / 41.11.

**Attribution.** Both old constraints were binding (`p[0->0]` at its pin, `p[1->0]` exactly at
0.15), which forced a rare, short, extreme jump regime — 13.8% of weeks at a variance ratio of 7.24
— that incidentally flattened volatility clustering better. That was bought with a boundary solution
and 12 log-likelihood points, and the honest free-parameter count under two binding constraints is 3
rather than 4, giving AIC -8591.63 / BIC -8575.23 — still worse than the new spec.

**The correct reading is that both specifications are decisively rejected by this battery.** Moving
from p = 2.5e-8 to p = 2.4e-11 is not a regression from acceptable to unacceptable; it is one
emphatic rejection replacing another. The limitation is **architectural** — discrete states with
constant within-state variance cannot represent volatility that moves on a continuum — and is not
addressable by reparameterization. Standard-literature response: **SWARCH** (Hamilton & Susmel 1994).

**New problem created: the tier thresholds no longer fit the model.** Ergodic P(jump) moved
0.118 -> **0.264**, and hard-assigned jump weeks are 23.2% of the sample. RCM 25.78 -> 33.53, i.e.
materially fuzzier states. The "jump" regime now reads as an *elevated-volatility* state rather than
a panic detector: 2022 has 43 of 52 weeks above 0.5, and 2000-2002 has 80 of 157. Because the
unconditional mean probability is now 0.264, the model's **resting state sits inside [[README]] §4's
21-60% "building stress" band rather than its 0-20% "do nothing" band.** The tier boundaries were
set by inspection under the old calibration and are now wrong. They must be recalibrated on a
training window only — recalibrating on full history is PIT register channel 5.

**Sign-blindness persists.** Mean spread jump-minus-calm is 0.62%/wk against a jump sigma of
3.84%/wk, so the squared-deviation term stays magnitude-dominated. Big-up vs big-down weeks score
92.80% as similar at the 5% percentile tails, 98.75% at |ret| >= 5%, and **100.00%** at |ret| >= 7%.
Still 5 of the top 20 filtered-probability weeks have positive returns. `const[0]` (the jump mean) is
individually insignificant at p = 0.169.

**k=3 still wins both criteria, by a widening margin:** dAIC +65.9993, dBIC +44.1298 in its favour.

## Signal comparison vs trailing realized vol — 2026-08-12

Preliminary, option-assumption-free. Parameters fit on **1993-2009 only**, then the filter run over
the full series holding them fixed, so the 2010-2026 evaluation has no parameter look-ahead. Tier
boundaries set from training-window quantiles (70/20/10 occupancy) for **both** signals, so
calibration is not a confound. Eval occupancy came out 75.9 / 14.7 / 9.5, close to target.

**Not leakage.** `corr(signal_t, |r_t|) = 0.648` vs `corr(signal_t, |r_{t+1}|) = 0.372` — peaks at
lag 0, never on the future. The regime model's speed is structural: a Bayesian filter updates on one
large return, a moving average needs several.

**The regime model is genuinely earlier.** First week in the hysteria tier, versus 13-week trailing
vol: 2010 flash crash +9 weeks, 2011 downgrade +3, 2018-Q4 +4, 2022 bear **+20** (2022-01-17 vs
2022-06-06), COVID tied. It fired on 2015-08 and 2018-02 where trailing vol never did. It never
lagged. Crises detected: 7/8 vs 5/8 (13w) and 6/8 (8w), at essentially identical precision
(74.4% vs 72.6% / 74.7%, lift ~3.2x over a 22.7% base rate).

**But the forward outcomes undercut the strategy premise.** Mean forward 13-week return by tier:

| signal | calm | stress | hysteria |
|---|---|---|---|
| regime model | +2.64% | +4.29% | **+7.24%** |
| trailing vol 8w | +2.56% | +3.79% | **+8.09%** |
| trailing vol 13w | +2.60% | +4.50% | **+7.42%** |

Every signal says "buy crash insurance" immediately before the periods with the **highest** forward
returns. This is the volatility risk premium: elevated volatility is compensated, and it is also
when options are most expensive. The overlay's premise -- scale insurance up as stress builds -- is
structurally fighting that.

**One genuine edge for the regime model.** P(some week in the next 13 drops below -5%): regime model
17.9% calm -> **26.8%** hysteria (a 1.50x lift, directionally correct). Trailing vol **inverts** --
13w reads 18.6% calm -> **9.5%** hysteria, i.e. its panic tier predicts *less* tail risk than its
calm tier. Since puts pay on the tail rather than the mean, this is the one measure that matters for
the mandate, and it is the one place the regime model separates.

**Consequence for the benchmark: the implied-volatility assumption is now the decisive input, not a
detail.** The question is not whether these signals predict volatility (they do -- forward 13-week
vol 20.3% in hysteria vs 13.4% in calm) but whether outcomes beat *what you paid*, and options are
priced off exactly the volatility these signals detect. A crude IV proxy would not distinguish the
signals; it would decide the answer. **VIX should be added as a third comparator** -- it is free,
real-time, market-implied, and if it times as well as the fitted model then the modelling effort is
redundant.

This is [[regime-detection/regime-detection]]'s recorded conclusion appearing again: measurement
validity (the model does detect regimes) is not decision value.

## VIX — the missing input — 2026-08-12

VIX was absent from the project entirely. [[README]] §2's "Strictly Weekly Closing Prices (Log
Returns)" clause bans intraday and Hawkes, but it also silently excluded every other weekly series.
Like the persistence pin, it is an untested assumption. VIX aligns **1750 of 1750 weeks** with the
SPY return series and is free. It belongs in three distinct roles, and was in none: as a comparator
signal, as the **price of the instrument being bought** (put premium *is* implied vol, so no honest
overlay P&L exists without it), and as a model input — `MarkovRegression` accepts exogenous
regressors and we pass none, which is why the model is really a Gaussian HMM wearing a regression's
name.

**The fitted model is not redundant.** First week in the hysteria tier — the regime model beats VIX
in 4 crises, ties 3, and loses 0: 2015-08 and 2018-02 (VIX never fires), 2018-Q4 by 3 weeks, 2022 by
6 weeks (2022-01-17 vs 2022-02-28); ties on 2010, 2011, COVID. **Caveat:** VIX occupies the hysteria
tier only 53 eval weeks against the regime model's 82, so VIX is the more selective signal in the
evaluation period and the comparison is not perfectly occupancy-matched.

**But VIX is the better tail predictor.** P(some week in the next 13 below -5%): VIX 37.7% in
hysteria vs 17.3% calm; regime model 26.8% vs 17.9%; trailing vol *inverts* at 9.5% vs 18.6%.
Forward 13-week vol in hysteria: VIX 24.35%, regime 20.31%, trailing vol 19.68%.

**And the market charges for exactly that.** Mean variance risk premium (VIX minus 13-week realized)
when each signal is in hysteria: VIX **+8.13** vol points, regime model **+3.34**, trailing vol
**-3.45**. The better a signal predicts tails, the more expensive the insurance is when it fires.
This is the efficient-pricing result, and it is the core difficulty of the entire strategy.

**The "buy when underpriced" reframe FAILS.** Forward outcomes by VRP quintile over the eval period:

| VRP quintile | mean VRP | fwd 13w return | P(week < -5%) |
|---|---|---|---|
| 1 (cheapest) | -4.28 | +4.44% | **8.1%** |
| 2 | +1.65 | +3.02% | 16.3% |
| 3 | +4.01 | +2.77% | 15.9% |
| 4 | +6.23 | +2.13% | 24.6% |
| 5 (richest) | +11.08 | +4.24% | **33.5%** |

Monotonic. Options are cheapest precisely when tail risk is genuinely lowest. There is no free lunch
in buying cheap insurance — it is cheap because it is not needed. Buying puts on a low-VRP screen
alone is not a strategy.

**The one genuinely open avenue: the two signals are nearly orthogonal.** `corr(regime_p, VRP) =
-0.138`, while `corr(regime_p, VIX) = 0.721` (Spearman 0.736). So the regime model is not merely a
laggy VIX, and it carries information the VRP does not. The unanswered question is the *conditional*
cell — does "regime model says stress AND the VRP is not rich" beat either signal alone? That is the
next test, and it is cheap.

## Why we stopped before building risk_engine.py

`src/risk_engine.py:5-8` records the gate: no smoothing or tiering logic until `data_loader.py` and
`jump_model.py` are audited and a math reference exists. That gate was set before anyone knew what
the audit would find, and it paid for itself immediately — every flaw below would otherwise have
been discovered *through* a backtest that looked excellent.

Confirming instance of [[validation-backbone-before-upgrades]].

## What the 2026-08-12 review found

Tiered by consequence, not by discovery order.

### Tier 1 — invalidates the signal, one-line fixes

1. **Look-ahead bias in the state inference.** `jump_model.py:191` returns
   `smoothed_marginal_probabilities` — the Kim smoother, which conditions every week on the *entire*
   sample including the future. The thermostat needs `filtered_marginal_probabilities` (past and
   present only). On the synthetic fixture, the last calm week before the crash reads 0.6% filtered
   vs 20.1% smoothed — a 34x inflation, landing exactly on the "building stress" tier boundary.
   Provenance: `1ec5772`, `copilot-swe-agent[bot]`, following the standard statsmodels tutorial
   pattern, which is retrospective recession-dating and therefore correctly uses the smoother.

2. **The model cannot tell a crash from a melt-up.** `switching_trend=False` gives one common mean
   across both regimes, so the conditional density depends on the *squared* deviation and the sign
   of the return is invisible. Verified: a sign-flipped high-volatility rally (+0.79%/wk average)
   produces a 0.75 filtered jump probability — the README's 61-100% **hysteria** tier, identical
   classification to the -3.21%/wk crash. This is a pure volatility detector, not a crash detector.
   For a put-buying overlay it is a direct premium leak: maximum insurance held through a violent
   rally (think April-August 2020). Fix costs one parameter, `switching_trend=True`. Note the README
   calls the model "jump-diffusion" while there is currently no jump in the mean at all.

### Tier 2 — the measurement instruments are broken

3. **AIC/BIC are miscounted, and the miscount reverses the verdict.** statsmodels reports
   `k_params = 5`, but `p[0->0]` is hard-pinned in `transform_params` and never estimated — only 4
   parameters are free. On the synthetic fixture the reported AIC prefers the unconstrained spec
   (-937.02 vs -937.68); corrected counting prefers the constrained one (-939.02 vs -937.68). One
   unit of `k` decided it. This is not a constant offset, because pinned-vs-free is precisely the
   comparison the penalty term is supposed to adjudicate.

4. **All reported standard errors describe a model that was never fitted.** `cov_params_approx`
   differentiates `loglike` with `transformed=True`, bypassing `transform_params` and therefore
   every repo constraint. So `res.bse`, `pvalues`, `conf_int()`, and the significance columns of
   `summary()` are unusable — including a nonsense 0.0192 standard error reported for the pinned
   `p[0->0]`.

5. **The complex-step gradient is invalid through `sorted()` / `max()`, not merely inaccurate.**
   NumPy orders `complex128` lexicographically, so at a variance tie `sorted()` breaks the tie on
   the *imaginary* (perturbation) part and credits the derivative to the wrong coordinate;
   `max(complex, float)` discards the imaginary part outright. Confirmed downstream:
   `gopt[0] == -0.0` and `Hinv[0,0] == 1.0` **exactly** — the BFGS identity initialization, never
   updated. The optimizer learned nothing about that coordinate and reported `warnflag = 0`,
   `converged = True` regardless.

   Recommended fix handles 3, 4 and 5 together: a **smooth ordered reparameterization**
   (`sigma1^2 = sigma0^2 + exp(delta)`, `p10 = 0.15 + 0.85 * logistic(x)`), which keeps both
   constraints while restoring differentiability and valid covariance.

### Tier 3 — the constraints are justified by an untested assertion

6. **Pinning `p[0->0] = 0.98` inflates the crisis base rate.** The ergodic distribution gives
   `P(jump) = p[0->1] / (p[0->1] + p[1->0])`. Pinning entry at 2%/week fixes the numerator, and on
   the synthetic fixture yields 11.3% of weeks as crisis weeks. The unconstrained MLE gives 6.9%;
   ground truth is 6.7%. The constraints overstate crisis frequency by ~70%, which for a
   threshold-triggered overlay means buying insurance too often. Related: the pin also forces
   *short* crises — expecting entry every 50 weeks means ~3 episodes per 150 weeks, so each must be
   brief to match observed total crisis time (6.4 weeks implied vs 10 actual).

7. **The 0.85 jump-persistence ceiling binds on real data, though not on synthetic.** On the
   synthetic fixture `p[1->0]` fits to 0.157124 against a 0.150 floor (slack +0.0071, not binding).
   On real SPY 1993-2026 it fits to **exactly 0.15000000 — the floor, zero slack.** So the free
   parameter count is arguably 3, not 4. Recorded because the synthetic result was initially
   generalized to "the cap does not bind," which real data contradicts.

8. **`p[0->0] = 0.98` may work against its own stated purpose.** The README justifies the pin as
   blocking the model from "constantly flipping between states." But the free MLE wanted calm
   persistence of 0.9906 (a 106-week expected calm spell); the pin imposes 0.98 (50 weeks). On this
   data the pin makes the model *twitchier* than the unconstrained estimate, not stickier.

9. **The constraint story is CONTRADICTED on real data — tested 2026-08-12.**
   `jump_model.py:88-94` justifies the design by asserting that for windows like 2006-2011 the
   unconstrained MLE pathologically pairs high variance with high persistence (an 18-month crisis
   fitted as one long sticky regime). Fitted on real SPY 2006-01-01..2011-12-31, the unconstrained
   MLE puts the high-variance regime at **E[D] = 18.0 weeks vs 46.3 weeks for the low-variance
   regime** — high variance pairs with *low* persistence, the opposite of the claim. Same on full
   history (13.0 vs 37.5). The claimed pathology does not exist.

   **But the labelling problem is real:** the unconstrained fit does place high variance at index 0
   on both windows. So the comment's *prescription* (a variance-ordering constraint) is load-bearing
   and correct, while its *diagnosis* (a persistence pathology) is wrong. The two persistence
   constraints were justified only by that wrong diagnosis and have no surviving rationale.

### Tier 4 — the validation itself cannot detect misspecification

10. **`checks.py`'s fixture is drawn from exactly the model being fitted** (`checks.py:30-39`:
    Gaussian draws, two variance levels, hard regime boundaries). By construction it can only
    confirm self-recovery; it is structurally incapable of revealing that the model is wrong about
    real returns. It also asserts nothing about standardized residuals, durations, or filtered
    probabilities. Every number quoted above therefore carries more precision than confidence.

## How we found these

Recording the method, because it generalized better than any single finding:

- **Ran the code and inspected internals** rather than trusting descriptions or docstrings. Six of
  the ten findings are invisible from reading alone.
- **Hand-recomputed the Kim smoother** from the filtered probabilities and transition matrix and
  matched statsmodels to 6 decimal places (0.200796). That converted "the smoother leaks the future"
  from an assertion into a demonstrated mechanism, and exposed the amplification factor
  (`~p[1->1] / p[0->1]`, so leakage *grows* with pinned persistence).
- **Fitted the unconstrained spec alongside the constrained one.** Nearly all of Tier 3 came from
  that single comparison; none of it is visible from the constrained fit alone.
- **Read `mle_retvals`** (`gopt`, `Hinv`, `warnflag`) instead of trusting `converged = True`.
- **Ran a counterfactual** — the sign-flipped melt-up — instead of only testing the case the model
  was designed for.
- **Checked git provenance**, which explained the mechanism (generated code inherits its tutorial's
  assumptions, not just its API calls).
- **Three claims made during the review were wrong** (the cap binding; `sorted()` breaking
  invertibility; the subsequent retraction of that concern) and were caught by running code rather
  than by argument. The corrections are recorded above rather than quietly dropped, because the
  error pattern — confident mechanism, untested — is the same one that produced finding 9.

## Decisions

- **2026-08-12** — Validate before layering. `risk_engine.py` and `main.py` stay stubs until the
  Tier 1 and Tier 2 items are closed and real-data diagnostics exist.
- **2026-08-12** — Point-in-time discipline is written down as a standing register
  ([[docs/POINT-IN-TIME-DISCIPLINE]]), not left to code review, because look-ahead bias is the one
  bug class that makes results look *better* and therefore cannot be caught by tests.
- **2026-08-12** — LaTeX belongs in `docs/*.md` for Obsidian; conversational math uses plain
  code-style notation.

## Next

1. ~~Real SPY diagnostics~~ — **done 2026-08-12**, `diagnostics.py`. See the real-data verdict above.
2. **Benchmark against trailing realized vol BEFORE respecifying anything.** This is now the top
   priority, ahead of all model work. [[regime-detection/regime-detection]] already concluded a K=2
   jump model's decision value is dominated by reactive estimators. If a 20-week trailing realized
   vol scales put exposure as well as this does, every item below is wasted effort. Cheap test,
   highest information value, and it can invalidate the whole approach.
3. **Then** the specification decision, which is now a README amendment and not a code tweak:
   - **Keep** the variance-ordering constraint — empirically load-bearing (finding 9).
   - **Drop** the `p[0->0] = 0.98` pin and the 0.85 ceiling — LR-rejected, rationale contradicted,
     and jointly they make the observed 13.77% jump frequency unrepresentable.
   - **Add** `switching_trend=True` — fixes the residual left skew and the sign-blindness, and wins
     on corrected AIC and BIC.
   - **Decide on k=3.** Wins decisively on both criteria and matches the README's own three-tier
     structure, but requires amending [[README]] §2 which mandates two regimes.
4. **Then** `filtered_marginal_probabilities` (7.9% of weeks change tier) and the smooth ordered
   reparameterization, which unblocks trustworthy standard errors.
5. **Then** expanding-window (walk-forward) refitting for parameter look-ahead. Quarterly refits
   first to check parameter stability before building the full loop. Watch the `initialize_known`
   double-multiplication trap in the PIT register.
6. **Only then** `risk_engine.py` (EWMA + tiering) and `main.py`.

Note on the ARCH-LM failure: leftover conditional heteroskedasticity at LM = 41 after two variance
regimes suggests the limitation is the *architecture* — discrete states with constant within-state
variance — not merely the state count. The standard-literature answer is regime-switching GARCH
(**SWARCH**, Hamilton & Susmel 1994), which is likelihood-based and so not banned by [[README]] §2.
Deliberately not proposed as an action: it is a large scope increase and step 2 may make it moot.

Not planned: intraday data, Hawkes processes, K-means, or binary classifiers — banned by
[[README]] §2 and unaffected by any finding above.

## Open questions

- **Does this project belong under the stack charter?** It is not in [[INDEX]] nor in the repo table
  in [[CLAUDE]], so its governance status is undeclared. `regime-detection/governance/CLAUDE.md`
  directs reading `RESEARCH-LEDGER.md` before any new signal, and this is a new signal.
- **Does [[regime-detection/regime-detection]] already answer this?** That project ran a K=2
  statistical jump model and concluded its *decision value is dominated by reactive estimators*
  (measurement validity != decision value). If that conclusion transfers, the correct benchmark for
  this overlay is not "does the regime model work" but "does it beat trailing realized vol at
  scaling put exposure." Worth resolving before spending effort on the walk-forward.
- **Signal/execution timing** — README §4 specifies Friday 3:30pm EST using weekly closes, which do
  not exist at 3:30pm Friday. Thursday close, or Monday execution. Needs a decision.

## Related

- [[README]] — mandate, trade mechanics, risk tier matrix
- [[docs/MATH-REFERENCE]] — the four-layer stack, all derivations, and the audit record of the
  superseded constrained specification
- [[docs/POINT-IN-TIME-DISCIPLINE]] — the leak register and pre-flight checklist
- [[look-ahead-bias-is-self-concealing]] — the vault lesson from this review
- [[regime-detection/regime-detection]] — prior K=2 jump-model work in the stack
- [[INDEX|Home]]
