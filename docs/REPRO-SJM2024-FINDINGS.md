# Reproduction findings — Shu, Yu & Mulvey (2024), statistical jump model

Last updated: 2026-08-24. **STATUS: IN PROGRESS AND PROVISIONAL.** No charter, no programme. This
records what has run so it is not lost, not what has been established.

**D4 is discharged (2026-08-24), with one correction it surfaced — the lambda convention (below).**
The implementation is verified three ways: the dynamic programme against brute-force enumeration of
every state path (exact, 15 instances plus prefix costs and online argmin — `checks.py`); known-state
recovery on synthetic regimes, both directly in feature space (accuracy 0.991) and end-to-end through
the feature pipeline (0.979 away from switches — `checks.py`); and exact equivalence against the
authors' own `jumpmodels` package with centroids held fixed, at every penalty tried, on K=2 and K=3,
plus free-fit label agreement of 1.0000 on both synthetic features and a real cached `^GSPC` window
(`d4_crosscheck.py`). The findings below are now evidence, subject to the reinterpretation the lambda
convention forces.

Paper: *Downside Risk Reduction Using Regime-Switching Signals: A Statistical Jump Model Approach*,
Journal of Asset Management 25(5), 2024. arXiv 2402.05272. Authors' code: `Yizhan-Oliver-Shu/jump-models`.

## What this is, and why it is allowed to exist

A **reproduction plus the incumbent comparison the paper omits** — [[CLAUDE]] §1 (reproduction
environment) and standing requirement 5. The paper's comparison set is buy-and-hold and a Gaussian HMM.
It contains no reactive benchmark, which is precisely the comparison that decided the closed prediction
programme.

**The 0/1 exposure rule is F9, permanently closed in [[PARKED]] §4.** It is reconstructed only because
reproducing the claim requires reproducing the rule. The output is a verification result, there is no
live path, and if the only sayable conclusion becomes "so switch to T-bills when the state flips", it
stops there.

## Configuration

| | |
|---|---|
| model | K=2 statistical jump model, coordinate descent, 10 restarts, k-means++ seeding |
| features | EWM downside deviation HL=10d; EWM Sortino HL=20d and 60d; on excess returns |
| state naming | mechanical — ascending centroid of the downside-deviation feature, so state 0 = bull |
| training | trailing 3000 days, standardised on the training window only, parameters refit every 126 days |
| inference | **online**: forward pass only, state at t = argmin_k V(t,k), never revised by later data |
| data | `^GSPC` daily 1970-, risk-free `DTB3` from FRED |
| costs | 10bp one-way, execution lag 2 days (signal at t held from t+2) |
| incumbents added | 200-day moving average; 10% volatility target capped at 1.0 |

## Result — `^GSPC`, out-of-sample 1990-01-02 to 2023-12-29, lambda fixed at 50

| | Buy & hold | Jump model | 200d MA | Vol target 10% |
|---|---|---|---|---|
| CAGR | **7.9%** | 6.3% | 6.5% | 6.3% |
| Volatility | 18.2% | 10.2% | 11.4% | 10.2% |
| Sharpe | 0.37 | 0.40 | 0.38 | 0.40 |
| Sortino | 0.52 | 0.55 | 0.52 | 0.55 |
| Max drawdown | −56.8% | **−20.3%** | −22.9% | −28.7% |
| Turnover/yr | 3% | 179% | 715% | 169% |
| Time invested | 100% | 60% | 74% | 72% |

**CDaR — mean of the worst q% of drawdown days, whole curve (leak row 11: never one alpha)**

| worst | Buy & hold | Jump model | 200d MA | Vol target |
|---|---|---|---|---|
| 1% | 48.6% | **18.2%** | 21.7% | 26.7% |
| 5% | 43.1% | **16.1%** | 20.6% | 23.0% |
| 10% | 37.7% | **13.7%** | 19.7% | 19.8% |
| 25% | 28.9% | **10.1%** | 16.7% | 14.5% |
| 50% | 19.9% | **7.9%** | 12.4% | 10.3% |
| average (pain index) | 10.8% | **4.6%** | 7.1% | 5.8% |

**Time under water** — days more than 10% below the running peak: 38.1% / **9.4%** / 30.5% / 19.5%.
More than 20% below: 21.4% / **0.0%** / 3.8% / 4.0%.

**Per-episode depth**, each strategy measured from its own peak inside the same window
(`depth_in_window`, the E2 repair):

| episode | Buy & hold | Jump model | 200d MA | Vol target |
|---|---|---|---|---|
| Gulf war 1990 | 19.9% | 9.4% | 9.4% | 13.3% |
| LTCM 1998 | 19.3% | 9.7% | 13.5% | 12.0% |
| Dot-com 2000-02 | 49.1% | **0.0%** | 13.7% | 28.6% |
| GFC 2007-09 | 56.8% | **5.0%** | 11.3% | 22.0% |
| COVID 2020 | 33.9% | 12.8% | 12.8% | 17.5% |
| Inflation 2022 | 25.4% | 9.8% | 15.4% | 13.9% |

## The three findings, ranked by how much they survive scrutiny

**1. Path dominance holds across the whole CDaR curve, and that is the strongest claim here.** The jump
model is lowest at every alpha from the worst 1% to the pain index, against both reactive incumbents.
Unlike max drawdown, the high-alpha end of that curve uses many days, so it is not an n=1 statistic. The
paper's claim — downside risk reduction — reproduces, and it reproduces *against benchmarks the paper
did not run*.

**2. It is not a return result, and Sharpe cannot see the difference.** CAGR 6.3% against buy-and-hold's
7.9%: the strategy pays 1.6pp/yr for the path. Sharpe ties at 0.40 vs 0.37 because it divides by total
volatility and is blind to path shape. **Any claim of the form "it beats buy-and-hold" is false on
return and true only on path.** Both halves must be said together.

> **Scope narrowed 2026-08-24, after reading the paper's full results table.** This is a fact about
> *this configuration* — fixed half-strength lambda on a price index — and **not yet a fact about the
> paper's procedure.** The paper's own Table 4 (total-return data, monthly CV lambda) reports JM CAGR
> 11.2% against buy-and-hold's 10.2%: a return *win*, at 44%/yr turnover against our 179%. Dividends
> favour buy-and-hold (invested 100% of the time vs ~60%), so D2 cannot explain their direction of the
> gap — the D1 selection procedure is what separates "pays 1.6pp/yr for the path" from "wins on both."
> Whether their return claim survives replication is exactly what D1+D2 decide, and until they run,
> finding 2 must be quoted with this caveat attached.
>
> **Resolved the same day — the caveat was right.** The D1 run (section below) has the CV strategy at
> CAGR 8.4% against buy-and-hold's 7.9% on price-only data: the return cost belongs to the *fixed-lambda
> configuration*, not to the paper's procedure. Finding 2 survives only in this form: **the paper's
> procedure buys its return back by surrendering crash depth** (MaxDD −34.0% for the CV against −20.3%
> for fixed paper-25), and Sharpe still cannot see that difference. The trade-off, not the return cost,
> is the durable half of the finding.

**3. The advantage is concentrated in one decade, and that is the binding limitation.** CAGR by decade:

| | Buy & hold | Jump model | 200d MA | Vol target |
|---|---|---|---|---|
| 1990s | **15.1%** | 5.8% | 11.2% | 11.5% |
| 2000s | −2.7% | **5.6%** | 2.3% | 0.7% |
| 2010s | **11.2%** | 6.0% | 6.0% | 7.2% |
| 2020s (3y) | 10.3% | 9.7% | 6.3% | 5.6% |

The entire edge is the 2000s (+8.3pp/yr against buy-and-hold), which is dot-com plus the GFC — the two
episodes where per-episode depth was 0.0% and 5.0%. In every other decade it loses, and in the 1990s it
loses by 9.3pp/yr. **Effective n on the thing that generates the result is two episodes**, which is the
same wall as [[systemic-events-are-too-rare-to-calibrate]] and the same shape as the closed intervention
programme's n=1 benefit side.

## The lambda convention — D4's one correction (2026-08-24)

The authors' package computes the per-observation loss as `0.5 * ||x - theta||^2`
(`jumpmodels/jump.py`, `do_E_step`); `src/jumpmodel.py` uses `||x - theta||^2`. Minimising
`0.5*D + lam*J` is minimising `D + 2*lam*J`, so **a lambda here is worth half its face value in the
package's units**: `lambda_ours = 2 * lambda_package`. Verified exactly in `d4_crosscheck.py` — at the
matched penalty the two implementations return identical paths, identical online states, and objectives
in the predicted 2:1 relation; at the *same face value* they return different paths on the paper's own
grid, so the factor of two is material, not cosmetic.

Consequences for everything above:

- **The headline run at "lambda = 50" reproduces the paper's lambda = 25.** Every row of the sweep
  table below is at half its nominal paper-units value: the grid actually run is paper-lambda
  {0, 2.5, 7.5, 17.5, 25, 35, 75}.
- **D1's suspect status is strengthened.** The paper's CV-selected penalties live in package units;
  this run's fixed penalty was effectively half of what its face value suggested, and the sweep shows
  performance still rising past it. Part of the residual 0.17 Sharpe gap plausibly lives here.
- **No finding reverses.** Path dominance, the return cost, the one-decade concentration and the
  monotone state-vs-RV AUC are all read off runs whose lambda labels shift, not whose outputs change.

## What D4 turned up beyond verification

On synthetic two-regime data (deterministic blocks, 18% bear), coordinate descent at lambda_ours = 50
recovers the truth at 0.979 — but **at lambda_ours = 30 it lands in a local optimum that calls 73% of
days bear**, with 10 k-means++ restarts. The jump penalty does not only tune persistence; it changes
*which* local optimum the alternating fit finds. Relevant to D1: a CV sweep over lambda is also a sweep
over qualitatively different fits, not a smooth dial. (`checks.py` pins the working configuration;
the fragile one is recorded here rather than checked, because it is a property of the method, not a
defect of the implementation.)

Two resolution bounds on the feature pipeline, established while building the recovery check: the EWM
features lag a switch (so recovery is scored away from switch dates), and **regimes shorter than the
60-day Sortino halflife are not resolvable at all** — a random chain that draws short bear segments
blurs the centroids together (a 25-day bear segment cannot be seen through a 60-day memory). This is a
bound on the paper's feature set, not on the optimizer.

## The jump-penalty sweep, and the diagnostic it triggered

Paper window, same configuration, lambda over the paper's own grid **(face values in this repo's
units — halve them for paper units, per the lambda convention above)**:

| lambda | Sharpe | Max DD | switches/yr | **state-vs-RV AUC** |
|---|---|---|---|---|
| 0 (k-means) | 0.04 | −25.6% | 15.01 | 0.762 |
| 5 | 0.25 | −17.6% | 5.38 | 0.795 |
| 15 | 0.31 | −20.5% | 3.27 | 0.796 |
| 35 | 0.31 | −21.3% | 2.38 | 0.818 |
| 50 | 0.40 | −20.3% | 1.79 | 0.850 |
| 70 | **0.44** | −20.7% | 1.44 | 0.882 |
| 150 | — | — | 0.76 | **0.947** |

**The sharpest observation in the run: performance and volatility-equivalence rise together.** The last
column is the AUC for separating the fitted state using nothing but trailing 60-day realized volatility.
It climbs monotonically with the jump penalty, reaching 0.947. **The more persistent the state — and the
better the strategy performs — the more exactly the state is a slow volatility threshold.**

This is [[docs/PROBLEM-MAP]] §0.9 firing as written: unsupervised compression of volatility-dominated
return features produces a volatility meter, and the free check is that the labels come out nearly
monotone in trailing realized volatility. They do.

It also means the jump penalty is not adding information. It is adding **persistence**, and persistence
is what turns a noisy volatility classifier into a tradeable one by suppressing whipsaw: at lambda = 0
the same features give Sharpe 0.04 and 1503% turnover; at lambda = 70, Sharpe 0.44 and 144%. The model's
contribution is a turnover control with a dial, not a new observable.

## Not reproduced: the paper's margin

Paper Table 4, S&P 500 (total return, 1990-2023): buy-and-hold Sharpe 0.48 / CAGR 10.2% / MDD −55.2% /
turnover 0%; HMM 0.54 / 8.5% / −28.9% / 141%; **JM 0.68 / 11.2% / −26.6% / 44%**. We get Sharpe 0.37
and 0.40.

- The **benchmark** gap is explained by D2. `^GSPC` is price-only; ~1.8pp/yr of dividends over 18.2% vol
  is +0.10 of Sharpe, giving 0.47 against the paper's 0.48.
- Applying the same correction to the jump model (invested 60% of the time, so about +0.11) gives ~0.51
  against the paper's 0.68. **A residual gap of roughly 0.17 is not explained by dividends.**
- lambda = 70 (face, ours) already reaches 0.44 and performance was still rising, so **D1 (fixed penalty
  rather than the paper's monthly CV selection) is the prime suspect** for the residual.
- **The turnover fingerprint (added 2026-08-24) pins the suspect down further.** The paper's 44%/yr
  turnover on a 0/1 rule is ~0.44 switches per year — one round trip every four to five years. Our
  sweep's most persistent run, lambda 150 face (paper 75), still switches 0.76/yr. So their CV is
  living at or beyond the top of the grid we ran — consistent with their delay robustness (Sharpe
  0.68 → 0.71 → 0.70 at 1/5/10-day delays: a signal that slow barely notices a two-week delay), and
  with our own sweep, where Sharpe rises monotonically in the penalty. When D1 is implemented, expect
  the selected lambdas to sit high; if they do not and the margin still closes, that is worth more
  attention, not less.

## Fidelity audit against the paper's text — 2026-08-24, arXiv v3 read directly

Item by item, what the paper says against what this reproduction does. **Confirmed matches:** features
exactly (EWM DD halflife 10 on excess returns; EWM Sortino halflives 20 and 60 — their Table 2);
K = 2; coordinate descent with 10 initialisations keeping the lowest objective; 3000-day training
window; refit every six months; standardised features; 10bp one-way cost; execution timing (their
"switch at end of t+1 after a signal at t" is our `shift(2)`); 0/1 rule into the local risk-free rate.
**The loss is stated in the paper itself as `l(x, theta) := 0.5 * ||x - theta||^2` (their §3.4)** — D5
is now confirmed at the source, not only against the package.

Deviations, restated against the text:

| | paper | this repro | status |
|---|---|---|---|
| lambda | monthly CV, 8-year lookback validation, criterion = validation Sharpe of the online strategy with 1-day delay, grid {0, 5, 15, 35, 70, 150} (paper units) | fixed at 50 face = paper 25 | **D1**, open — full spec now extracted |
| data | Bloomberg total-return S&P 500, DAX, Nikkei 225; GFD 3-month yields per country; 1970-2023 | `^GSPC` price index + FRED DTB3, US only | **D2**, open — and the multi-market half was undeclared until now |
| online window | rolling 3000 days ending at t, daily | window start frozen within each 126-day block | **D3**, declared |
| state naming | **bull = the state with the higher cumulative return** (in training) | bull = the lower downside-deviation centroid | **D6, newly declared** — almost surely coincident at K=2 on vol-dominated features, but it is a different rule and must be verified, not assumed |
| HMM benchmark | 2-state Gaussian HMM on daily log TR, 3000d window, refit **daily**, online Viterbi + median filter with CV-selected length | not built | open list |
| feature clipping | not mentioned in the paper; **their `jumpmodels` package ships `DataClipperStd`, 3-sigma winsorization (`mean ± 3*std`, population std) fit on the training window, applied before scaling** — confirmed by reading `preprocess.py` directly (2026-08-25) | none | **D7, newly declared** — this is an implementation choice absent from the text entirely; reproducing what the authors actually ran, not what they described, requires it |
| refit warm-start | not mentioned in the paper; **their `BaseClusteringAlgo.init_centers()` appends the previous fit's `centers_` as an 11th k-means++ candidate on every refit** (`base.py`) | fresh k-means++ restarts every 126-day block, `seed=0`, no memory of the prior block | **D8, newly declared** — see local-optimum note below |

Running the paper's grid in this repo's units means lambda ∈ {0, 10, 30, 70, 140, 300}.

## The paper's own weaknesses — what to learn rather than inherit

Read critically, with what each one implies for how this reproduction proceeds. Every claim below is
checked against the paper's text, not assumed.

1. **No statistical inference anywhere.** Confirmed: no interval, bootstrap or test on any performance
   difference — every ordering is a point estimate on one path per market, and the three markets are
   correlated global equity indices, not three replications. This is the same defect our open list
   already refuses to inherit (block bootstrap before any ordering is claimed distinguishable).
2. **The hyperparameter is selected on the quantity being reported.** Monthly lambda-hat maximises
   trailing 8-year validation *Sharpe* — formally out-of-sample, but the selection criterion is the
   headline metric, the validation window holds one or two bear episodes at a time, and the paper never
   reports the lambda-hat path (confirmed absent), so the reader cannot see how much the procedure
   whipsaws or what it actually selected. When D1 runs here, **the lambda-hat time series is a required
   output**, and [[docs/POINT-IN-TIME-DISCIPLINE]]'s selection-on-outcome clause applies in full.
3. **Sharpe is the headline for a downside-risk claim.** The paper's stated objective is downside risk
   reduction, scored by Sharpe, volatility and a single max drawdown — an n=1 path statistic. No CDaR
   at any level, no time under water, no per-episode depth, no subperiod analysis (confirmed). Our
   whole-curve CDaR and decade tables are the repair, and the decade table is what exposed the
   one-decade concentration the paper's format cannot see.
4. **The comparison set contains no reactive incumbent.** Buy-and-hold and a deliberately noisy HMM
   (refit daily, then median-filtered). No moving average, no volatility target, no raw vol threshold —
   despite our diagnostic showing the fitted state is a slow volatility threshold (AUC 0.947 at high
   penalty). The JM-vs-HMM margin the paper reports is partly a persistence margin, not an
   information margin: its own turnover column says so (44% vs 141%).
5. **Anticipation language for a trailing signal.** "Anticipated unfavorable regimes" describes a
   state that is (our measurement) near-monotone in trailing 60-day realized volatility with
   hysteresis. The paper itself concedes latency at crash turning points (their §4). The honest
   description is: a persistence-regularised volatility threshold that reacts slowly and holds its
   position — which is also *why* it survives 10-day execution delays.
6. **What the paper gets right, kept explicitly:** total-return data with matched local risk-free
   legs; the delay-robustness table (1/5/10 days); a 10bp cost applied throughout; and online
   inference stated carefully (the state at t uses data through t only). None of these should be
   cheapened while criticising the rest.

## Extension — QQQ, out-of-sample 2011-2026 (partial, and it sharpens finding 3)

Not a reproduction: the paper does not test QQQ, and this window contains **no systemic crisis** — no
dot-com, no GFC, only COVID and 2022. That is exactly what makes it informative.

| CAGR by decade | Buy & hold | Jump model | 200d MA | Vol target |
|---|---|---|---|---|
| 2010s (8y) | **16.9%** | 13.4% | 8.3% | 9.9% |
| 2020s (6y) | **20.7%** | 11.9% | 18.2% | 10.6% |

Per-episode depth: COVID 28.6% → **13.2%**; inflation 2022 34.3% → **10.0%**. Regime switches 1.94/yr,
bear 20.6% of days, **state-vs-RV AUC 0.955**.

**Reading:** in a sample without a systemic episode the jump model buys path smoothing and pays for it in
return, giving up 3.5pp/yr in the 2010s and 8.8pp/yr in the 2020s. It still halves episode depth. This is
finding 3 restated on different data — the return advantage requires a 2000s-shaped decade, and the path
advantage does not. Full table pending a rerun; the summary rows above are all that was captured.

## Declared deviations

| | deviation | consequence |
|---|---|---|
| D1 | lambda fixed, not reselected monthly by trailing 8-year validation Sharpe | reproduces the model, not the selection procedure. Prime suspect for the residual margin |
| D2 | `^GSPC` price index, not total return | return *levels* are not comparable to the paper's; orderings and path metrics are |
| D3 | online window start frozen within each 126-day block rather than rolling daily | state at t still uses only data up to t |
| D4 | ~~implementation unverified~~ **discharged 2026-08-24**: brute-force DP enumeration and synthetic known-state recovery (`checks.py`), exact equivalence with the authors' package (`d4_crosscheck.py`) | surfaced D5 |
| D5 | **lambda face values are 2x the paper's units** (the paper's §3.4 loss is `0.5*\|\|x-theta\|\|^2`, ours is unscaled; confirmed in both the text and the package) — the lambda=50 run is the paper's lambda=25 | run labels reinterpreted, no outputs change; sharpens D1 |
| D6 | state naming: paper names bull as the higher-cumulative-return state; this repro names bull as the lower downside-deviation centroid | declared and **closed 2026-08-24**: rules disagree on 4/540 fits (all at paper-lambda >= 70, at the 1987 crash and dot-com top); rule-B rerun shows every conclusion survives under either rule |
| D7 | no feature clipping; the authors' `jumpmodels` package (`preprocess.py::DataClipperStd`) winsorizes each feature to `mean ± 3*std` of the training window (population std) before scaling — this is source-code fidelity, absent from the paper's text entirely | open — not yet run at any lambda, including the D1 CV run above; a plausible partial explanation for the residual Sharpe gap independent of D1 |
| D8 | fresh k-means++ restarts every 126-day refit block (`seed=0`, no memory of the prior block); the authors' `BaseClusteringAlgo.init_centers()` (`base.py`) appends the previous block's fitted `centers_` as an 11th k-means++ candidate on every refit | open — interacts with the documented local-optimum fragility (lambda_ours=30 landing in a 73%-bear local optimum, see "What D4 turned up" above): warm-starting could suppress spurious optimum-switching between adjacent blocks independently of lambda, so part of the switches/yr and persistence gap may not be a lambda-selection effect at all |

**Source note:** D7 and D8 came from reading the authors' actual `jumpmodels` package source (`src/Shu/preprocess.py`, `src/Shu/base.py`, `src/Shu/jump.py` — supplied 2026-08-25), not from the paper's text. The paper under-specifies the implementation on both counts; reproducing what the authors' code actually does, rather than only what their prose describes, is the standard [[CLAUDE]] standing requirement 5 asks for.

**Confirmed against the authors' public repo directly** (`github.com/Yizhan-Oliver-Shu/jump-models`, `examples/nasdaq/example.py`, read 2026-08-25 — a package usage demo on the Nasdaq-100, not the paper's own S&P 500 study code, which is not in this repo):

- **D7's exact sequencing.** `X_train_processed = scalar.fit_transform(clipper.fit_transform(X_train))`, then `X_test_processed = scalar.transform(clipper.transform(X_test))` — clip *then* scale, both fitted only on the training window and applied unrefit to held-out data. Confirms clip-before-scale, not just that clipping exists.
- **D8's mechanism is demonstrated, not hypothetical.** The example refits by calling `jm.set_params(jump_penalty=...).fit(X_train_processed, ...)` on the *same* `JumpModel` instance repeatedly. Because `init_centers()` appends `self.centers_` whenever it already exists on the instance, warm-starting from the prior fit is a side effect of the authors' own idiom for refitting, not an opt-in flag.
- **No CV/backtest code exists in the public package.** `jump-models` is the modelling library only (`jumpmodels/`) plus one demo (`examples/nasdaq/`, single train/test split, no rolling CV). The monthly trailing-8-year lambda selection in the paper has no released reference implementation — `d1_cv.py`'s CV loop is this repository's own construction from the paper's prose, not a reproduction of the authors' code. Flag any future claim of "reproducing the CV procedure" accordingly — it reproduces the *description*, D1 always said so, but there is now nothing left to check it against.

## Preregistered for the D1/D6 run — written 2026-08-24, before the run

The run: one pass fitting all six paper-grid lambdas per refit block, recording both naming rules per
(block, lambda), emitting the fixed-lambda sweep on the paper's actual grid, then the monthly CV
selector on top. Implementation choices the paper leaves unstated, fixed now: validation Sharpe is
computed on excess strategy returns **net of the 10bp cost** under the same execution convention as the
headline; reselection every 21 trading days; ties break toward the **larger** lambda (fewer trades);
naming rule B uses cumulative raw return over training days assigned to each state; the CV needs a full
8-year signal history, so the effective OOS start is the first date that has one (the paper's
1970-start / 12-year train / 8-year validation arithmetic lands this at ~1990, which is presumably why
those numbers were chosen).

Expectations, stated before any number is seen:

| | expectation | basis | if it fails |
|---|---|---|---|
| X1 | the two naming rules (D6) never disagree at any lambda > 0 | K=2 on vol-dominated features: the high-downside state should also be the low-cumret state | any disagreement at a lambda used in a quoted table invalidates that block's signal — find which results it touches before anything else |
| X2 | the selected lambda-hat concentrates at the persistent end: median >= 70 in paper units | the paper's 44%/yr turnover = 0.44 switches/yr, beyond our lambda-150-face run's 0.76 | the paper's turnover comes from somewhere else — e.g. the CV whipsawing between candidates suppresses trades some other way; investigate before interpreting |
| X3 | the CV strategy's Sharpe lands at or above the best fixed-lambda run on the same window | the selection criterion IS Sharpe on a trailing window, and Sharpe here rises monotonically in lambda | the procedure subtracts value — selection noise (whipsaw between candidate tracks) costs more than adaptivity earns; that would itself be a finding against the paper's procedure |
| X4 | dividend arithmetic for the return claim: on a price index the strategy is *relatively* penalised ~0.55–0.7pp/yr vs buy-and-hold (dividends accrue ~1.8pp/yr times the fraction of time invested). The paper's TR return win (11.2 vs 10.2) therefore predicts **JM CAGR >= B&H CAGR − 0.7pp on our price data** | finding 2's scope caveat | if CV-selected JM still trails B&H by well over 0.7pp, the paper's return claim fails to replicate on public data — reportable either way |

## The D1/D6 run — 2026-08-24, scored against the preregistration

Run: `.venv\Scripts\python.exe d1_cv.py`. 90 blocks x 6 lambdas, one pass; both windows reported
because every signal and every selection is causal, so truncation needs no refit.

**Paper window (1990-01-02 to 2023-12-29), `^GSPC` price index:**

| | CAGR | Vol | Sharpe | MaxDD | Turnover | TimeIn | pain | AUC |
|---|---|---|---|---|---|---|---|---|
| Buy & hold | 7.9% | 18.2% | 0.37 | −56.8% | 3% | 100% | 10.8% | — |
| lam paper 5 | 4.9% | 9.5% | 0.28 | −18.5% | 397% | 57% | 5.7% | 0.791 |
| lam paper 15 | 4.9% | 9.8% | 0.27 | −22.1% | 297% | 58% | 6.4% | 0.822 |
| lam paper 35 | 7.0% | 10.4% | 0.45 | −19.2% | 156% | 63% | **4.3%** | 0.894 |
| lam paper 70 | 6.2% | 11.9% | 0.36 | −26.7% | 97% | 72% | 6.2% | 0.946 |
| lam paper 150 | 8.0% | 13.5% | 0.45 | −35.9% | 32% | 79% | 5.7% | 0.905 |
| **CV monthly (D1)** | **8.4%** | 12.5% | **0.50** | −34.0% | 85% | 75% | 4.7% | 0.931 |

Verdicts:

- **X1 (naming rules never disagree at lambda > 0): FAILED, narrowly and informatively.** 4 of 540
  (block, lambda) fits disagree — none at paper-lambda <= 35, one at 70 (block 2000-05-01), three at
  150 (1986-11-12, 1987-05-14, 1999-10-29). **Two of the four sit at the 1987 crash and two at the
  dot-com top.** The mechanism: at high persistence the two-state split can put the late-90s melt-up
  (high-vol, high-*return*) days into the high-downside-deviation state, so "bear = high DD" and
  "bear = lower cumret" genuinely diverge — the naming rule changes what the state *means*, exactly
  where the money is. No previously quoted table is touched (all used rule A at lambdas where the rules
  agree), but the CV row above is rule-A named while the paper's procedure is rule-B — **a rule-B CV
  rerun is required before the CV row may be quoted as "the paper's procedure."**

  **The rule-B rerun ran the same day (`d1_cv.py --naming cumret`) and D6 is now closed as immaterial
  at the level of conclusions.** Under the paper's naming: CV Sharpe 0.50 (unchanged), CAGR 8.5% vs
  8.4%, MaxDD −34.0% (identical), pain 4.8% vs 4.7%, lambda-hat median still 150 with 57% of months
  there (series: `figures/sjm2024_lambda_hat_cumret.csv`). The four inverted blocks move only the fixed
  paper-70/150 rows, by hundredths (paper-70 Sharpe 0.34 vs 0.36 — the paper's rule is *slightly hurt*
  by calling the melt-up state bull into the dot-com top, which is the direction the mechanism
  predicts). Every conclusion above survives under either rule, and the CV row may now be quoted as the
  paper's procedure.
- **X2 (lambda-hat concentrates high): CONFIRMED.** Median 150 paper units — the top of the grid — with
  58% of the 440 monthly selections at 150, 41% at 15/35, and 11 switches of lambda-hat itself. The
  turnover fingerprint is only partially reproduced (85%/yr vs the paper's 44%), so their selections
  likely sit at 150 even more often than ours, or TR data reranks the validation.
- **X3 (CV >= best fixed): CONFIRMED.** 0.50 against 0.45 — the selection procedure added Sharpe over
  every fixed candidate on this path.
- **X4 (return claim): CONSISTENT WITH REPLICATION.** The CV strategy earns **8.4% against buy-and-hold's
  7.9% on price-only data** — it wins by +0.5pp/yr *before* the ~0.45pp/yr relative dividend penalty,
  implying roughly par on TR data against the paper's +1.0pp. Directionally replicated; the full margin
  is not, and D2/D3/D6 remain as candidates for the remainder. Dividend-adjusted Sharpe lands ~0.61
  against the paper's 0.68 — **the residual gap shrinks from 0.17 to ~0.07** once the selection
  procedure exists.

**What the CV actually bought, and what it sold — the observation that matters most here.** The
fixed-lambda headline run (paper 25) had MaxDD −20.3% and paid 1.6pp/yr for it. The CV strategy earns
back the return (8.4% vs 7.9%) **and its MaxDD is −34.0%** — because Sharpe-selected lambda drifts to
the persistent end, where the state is so slow (32% turnover at paper-150) that it rides well into
crashes before exiting (that row's MaxDD is −35.9%). The pain index still halves (4.7% vs 10.8%), so
shallow-and-frequent drawdown days improve, but the deep tail gives back much of the protection the
fixed-lambda configuration had. **The paper's procedure and the paper's pitch are two different
strategies: the CV maximises Sharpe and surrenders crash depth; the fixed mid-lambda buys crash depth
and pays return.** The paper reports MDD −26.6% for its CV — between our two — and never shows the
trade-off because it never runs the fixed-lambda column.

Also recorded: the sweep on the full paper grid is **not monotone in lambda** — Sharpe dips at paper-70
(0.36, and that is the row whose 2000-05 block has the naming instability) — and neither is the
state-vs-RV AUC (0.946 at 70, 0.905 at 150). The earlier half-strength sweep's "monotone rise" was a
truncation artifact.

## Preregistered for the volatility-threshold incumbent — written 2026-08-24, before the run

The question: **does the jump model add anything beyond a persistence-regularised volatility
threshold?** The AUC diagnostic (0.85–0.95 across the useful lambda range) says the fitted state is
nearly a function of trailing realized volatility; if a two-parameter threshold rule matches the JM's
whole battery, the model's contribution reduces to threshold selection with a persistence dial, and the
paper's machinery is decoration. This is the cheapest falsification left and the baseline the paper
never ran.

The incumbent, fixed before any result is seen. Trailing 60-day realized volatility (the diagnostic's
own measure). Exit to cash when RV crosses **above** its trailing-3000-day percentile `p_exit`;
re-enter when RV falls **below** percentile `p_reenter < p_exit` (the two-sided band is the hysteresis
that supplies persistence). Percentiles computed point-in-time on the same 3000-day window the JM
trains on, refit on the same 126-day block schedule, same 10bp cost, same execution lag, same
risk-free leg. **Three preregistered parameter pairs, all reported, none selected:**
(80, 60), (75, 55), (85, 65). No performance tuning of any kind.

Expectations:

| | expectation | basis | if it fails |
|---|---|---|---|
| Y1 | at least one variant recovers **most** of the fixed-lambda JM's pain-index improvement (indicatively: pain within ~1.5pp of the JM's 4.3–4.7% band, against buy-and-hold's 10.8%) | AUC 0.89–0.95: the state largely *is* an RV threshold | the JM's edge does not reduce to slow vol thresholding — the feature set (Sortino terms) or the fit contributes something a threshold cannot; that would *raise* the reproduction's assessment of the paper |
| Y2 | the JM retains an edge at the deep end of the CDaR curve (worst 1–5%) over every variant | the jump penalty reacts to level shifts faster than a percentile band re-anchors | if a threshold variant matches or beats the deep end too, the equivalence is complete and the reproduction's summary line becomes "a volatility threshold with hysteresis reproduces the paper's result" |
| Y3 | threshold variants cluster tightly with each other relative to their distance from buy-and-hold | if the three variants disagree wildly the "simple incumbent" is itself fragile and cannot serve as a reference class | report the spread as the incumbent's own instability; no variant may then be quoted alone |

## The volatility-threshold run — 2026-08-24, scored against the preregistration

Run: `.venv\Scripts\python.exe volthreshold.py`. Paper window shown; the full sample agrees.

| | CAGR | Sharpe | MaxDD | Turnover | TuW>10% | CDaR 1% | 5% | 25% | pain |
|---|---|---|---|---|---|---|---|---|---|
| Buy & hold | 7.9% | 0.37 | −56.8% | 3% | 38.1% | 48.6% | 43.1% | 28.9% | 10.8% |
| JM fixed paper-25 | 6.3% | 0.40 | **−20.3%** | 179% | **9.4%** | **18.2%** | **16.1%** | **10.1%** | 4.6% |
| JM fixed paper-35 | 6.8% | 0.44 | −20.7% | 144% | 9.8% | 19.0% | 16.3% | 10.5% | 4.4% |
| RV band (80,60) | 5.8% | 0.34 | −22.3% | 85% | 19.4% | 19.7% | 17.8% | 13.0% | 5.6% |
| **RV band (75,55)** | 6.7% | **0.44** | −22.8% | 79% | 11.4% | 18.9% | 16.6% | 10.7% | **4.2%** |
| RV band (85,65) | 5.8% | 0.32 | −32.8% | 85% | 34.0% | 32.3% | 30.2% | 21.3% | 8.3% |

Verdicts:

- **Y1 (a band recovers most of the pain improvement): CONFIRMED, and then some.** The (75,55) band's
  pain index is **4.2% — better than both jump-model rows** (4.6%, 4.4%), with the same Sharpe as the
  JM's best fixed run (0.44) at half the turnover. On the shallow half of the drawdown distribution the
  two-parameter volatility band is not an approximation of the jump model; it is at least its equal.
- **Y2 (JM keeps a deep-tail edge over every variant): CONFIRMED, narrowly.** At the worst 1/5/25% of
  drawdown days the JM (paper-25) beats the best band by 0.7 / 0.5 / 0.6pp, and its MaxDD is 2.5pp
  shallower. The edge exists at every deep alpha against every variant — and it is **under 1pp on a
  curve whose deep end is generated by two episodes**, so it is a point estimate awaiting the block
  bootstrap, not an established margin.
- **Y3 (variants cluster): FAILED.** Moving the exit percentile from 75 to 85 takes the pain index from
  4.2% to 8.3% and MaxDD from −22.8% to −32.8%. The band family is fragile in its parameters, so no
  single band may be quoted as "the simple incumbent" — the family is quoted with its spread. The fair
  counterpoint recorded with it: the JM's own dial has the same disease in different places (the paper-70
  Sharpe dip, the lambda-30-ours local optimum on synthetic data). Neither family gives a stable rule
  for free; the JM's mid-grid is the more forgiving neighbourhood.

**The reproduction's summary line, as it now stands (pending the rule-B rerun and the bootstrap):** the
paper's jump-model strategy is, to within episode-level noise, **a persistence-regularised volatility
threshold**. Its distinguishable residual is confined to the deepest quarter of the drawdown
distribution and is smaller than 1pp of CDaR against the best of three preregistered two-parameter
bands; whether even that survives inference is the bootstrap's question. What the machinery buys that
the band does not is dial-robustness near its sweet spot — a legitimate, smaller claim than the paper's.

## Open, in the order worth doing

1. ~~Discharge D4~~ — **done 2026-08-24**, see the lambda convention and the D4 section above.
2. ~~Verify D6 / rerun at the paper's grid / implement D1~~ — **done 2026-08-24**, one run (`d1_cv.py`),
   scored against the preregistration above.
3. ~~Rerun the CV with rule-B naming~~ — **done 2026-08-24**: immaterial at the level of conclusions
   (CV Sharpe unchanged at 0.50; only the fixed paper-70/150 rows move, by hundredths). D6 closed.
4. ~~The volatility-threshold incumbent~~ — **done 2026-08-24** (`volthreshold.py`), preregistered and
   scored above: Y1 confirmed (the (75,55) band matches or beats the JM on the shallow half), Y2
   narrowly confirmed (JM's deep-tail edge < 1pp, awaiting inference), Y3 failed (the band family is
   parameter-fragile).
5. **Remove D2** by rerunning on `^SP500TR` (total return, 1988-), accepting the shorter out-of-sample.
   Note the DAX (`^GDAXI`) is a performance index — total return by construction — so it is the one
   paper market replicable on public TR data at full length, and the Nikkei's decades-long grind is the
   one bear shape the US sample does not contain.
6. **Inference.** Every ordering above is a point estimate with no interval — the paper reports none
   either, confirmed. The CV-vs-fixed and JM-vs-incumbent orderings hang on a handful of episodes.
   Nothing is claimed as distinguishable until a block bootstrap says so.
7. **The HMM benchmark, now fully specified from the text**: 2-state Gaussian HMM on daily log total
   returns, 3000-day window refit daily, online Viterbi, median filter with CV-selected length — to
   check the paper's own margin over it rather than only over buy-and-hold.

## Related

- [[docs/PROBLEM-MAP]] §0.9 — the diagnostic this run confirmed · [[PARKED]] §4 — F9, the constraint
- [[docs/POINT-IN-TIME-DISCIPLINE]] — leak row 11 (report the whole CDaR curve), and the selection-on-outcome
  clause that D1 tests · [[docs/RESEARCH-PROTOCOL]] §0.1 — no magnitude without identification
- Code: `src/jumpmodel.py`, `src/sjm_features.py`, `repro_sjm2024.py`. Figure: `figures/sjm2024_gspc.png`
