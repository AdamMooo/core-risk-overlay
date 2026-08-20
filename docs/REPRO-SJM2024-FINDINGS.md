# Reproduction findings — Shu, Yu & Mulvey (2024), statistical jump model

Last updated: 2026-08-20. **STATUS: IN PROGRESS AND PROVISIONAL.** No charter, no programme. This
records what has run so it is not lost, not what has been established.

**Nothing here is believable until D4 is discharged.** The jump-model implementation has not been
verified against the authors' package or against synthetic data with known states. A null or a win from
unverified code is not evidence either way.

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

## The jump-penalty sweep, and the diagnostic it triggered

Paper window, same configuration, lambda over the paper's own grid:

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

Paper reports S&P Sharpe — buy-and-hold 0.48, HMM 0.54, JM 0.68. We get 0.37 and 0.40.

- The **benchmark** gap is explained by D2. `^GSPC` is price-only; ~1.8pp/yr of dividends over 18.2% vol
  is +0.10 of Sharpe, giving 0.47 against the paper's 0.48.
- Applying the same correction to the jump model (invested 60% of the time, so about +0.11) gives ~0.51
  against the paper's 0.68. **A residual gap of roughly 0.17 is not explained by dividends.**
- lambda = 70 already reaches 0.44 and performance was still rising, so **D1 (fixed penalty rather than
  the paper's monthly CV selection) is the prime suspect** for the residual.

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
| D4 | **implementation unverified** against the authors' package or synthetic known-state data | **nothing above is evidence until this is discharged** |

## Open, in the order worth doing

1. **Discharge D4.** Fit on simulated two-regime data with known states and confirm recovery; cross-check
   against `jump-models`.
2. **Implement D1** — monthly lambda selection on a trailing 8-year window — and see whether the residual
   0.17 closes. Note what this procedure is: selecting the hyperparameter that dominates performance by
   maximising realised performance, on a window containing one or two bear episodes.
3. **Remove D2** by rerunning on `^SP500TR` (total return, 1988-), accepting the shorter out-of-sample.
4. **Inference.** 61 switches and about four decisive declines in 34 years. Every ordering above is a
   point estimate with no interval. Nothing is claimed as distinguishable until a block bootstrap says so.
5. **The HMM benchmark**, to check the paper's own margin over it rather than only over buy-and-hold.

## Related

- [[docs/PROBLEM-MAP]] §0.9 — the diagnostic this run confirmed · [[PARKED]] §4 — F9, the constraint
- [[docs/POINT-IN-TIME-DISCIPLINE]] — leak row 11 (report the whole CDaR curve), and the selection-on-outcome
  clause that D1 tests · [[docs/RESEARCH-PROTOCOL]] §0.1 — no magnitude without identification
- Code: `src/jumpmodel.py`, `src/sjm_features.py`, `repro_sjm2024.py`. Figure: `figures/sjm2024_gspc.png`
