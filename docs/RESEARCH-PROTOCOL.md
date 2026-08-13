# Research Protocol

Last updated: 2026-08-12

**Preregistration.** Written before any result exists. Companion to `../README.md` §3 (the question),
`MATH-REFERENCE.md` (the model), `POINT-IN-TIME-DISCIPLINE.md` (the time-basis rules).

Binding: a design choice changed after seeing a result is logged in §9 as a dated amendment, not
silently edited.

**Subject: the Markov-switching model.** Not a horse race. Economic value is out of scope here — no
hedge sizing, instrument, strike, premium or P&L appears below.

> **How well does a Markov-switching model provide real-time information about Value at Risk and
> the tail risk of equity assets?**

**Real-time** excludes Kim-smoothed probabilities by definition (§6 R5 reports them only as a
hindsight illustration). It names the property rather than the algorithm: the Hamilton filter is the
only filter for this model class, so it generalises across every §3 specification.

---

## 1. The estimand

At each time `t`, using only information through `t`, the model emits a **one-step-ahead predictive
distribution** for the next period's log return:

$$F_{t+1|t}(r) = \Pr\left(r_{t+1} \le r \mid \mathcal{F}_t\right)$$

Everything follows from that one object:

| quantity | definition |
|---|---|
| **VaR** at level $\alpha$ | $F_{t+1|t}^{-1}(\alpha)$ |
| **ES** at level $\alpha$ | $\mathbb{E}[r_{t+1} \mid r_{t+1} \le \mathrm{VaR}_{t+1|t}(\alpha)]$ |

Both stated as **return levels** (negative numbers), never as positive loss magnitudes. One
convention, checked in code.

**Why the density and not a point volatility forecast.** A density can be scored on every
observation; a quantile only on its breaches. At $\alpha = 0.05$ over 8,400 days that is 8,400
observations versus ~420. §5 depends entirely on this and it is the largest source of statistical
power available here.

### 1.1 From regime probabilities to a density

**Step 1 — push the state forward one period** (the Hamilton filter's own prediction step,
`MATH-REFERENCE.md` §2.2):

$$w_{t+1|t}[j] = \sum_i \Pr(s_{t+1}=j \mid s_t=i)\,\xi_{t|t}[i]$$

In `statsmodels` naming `p[i->j]` is $\Pr(s_{t+1}=j \mid s_t=i)$, so for $k=2$ the free parameters
`p[0->0]` and `p[1->0]` give $w[0] = p_{00}\xi[0] + p_{10}\xi[1]$, $w[1] = 1 - w[0]$. Getting this
backwards inverts the model silently, so it carries a check.

**Step 2 — the density is a mixture, not a normal:**

$$f_{t+1|t}(r) = \sum_j w_{t+1|t}[j]\,\phi(r;\,\mu_j,\,\sigma_j^2)$$

**Step 3 — VaR inverts the mixture CDF numerically.** Solve for $q$:

$$\sum_j w[j]\,\Phi\!\left(\frac{q-\mu_j}{\sigma_j}\right) = \alpha$$

Strictly increasing, so Brent or bisection is unconditionally reliable.

> **The trap.** `VaR = mean + sqrt(var) * norm.ppf(alpha)` is **wrong**. Matching a mixture's first
> two moments does not match its quantiles — that is why mixtures are used at all. Measured at
> $w=[0.85,0.15]$, $\mu=[0.0015,-0.004]$, $\sigma=[0.008,0.026]$, $\alpha=0.05$: true mixture VaR
> $-1.813\%$, moment-matched normal $-2.011\%$. An **11% error in the VaR level**, sign flipping with
> $\alpha$. Largest at maximum regime uncertainty ($w$ near $0.5$). Measured across the sample, this
> is Figure 3.

**Step 4 — ES in closed form.** No simulation at one step. With $z_j = (q-\mu_j)/\sigma_j$ at the
solved $q$, from the truncated-normal first moment:

$$\mathrm{ES}(\alpha) = \frac{1}{\alpha}\sum_j w[j]\left[\mu_j\Phi(z_j) - \sigma_j\phi(z_j)\right]$$

Both forms verified against a 40M-draw Monte Carlo to $\sim10^{-5}$ (MC noise) on 2026-08-12.

**Required checks** in `checks.py`:

1. Degenerate mixture ($w=[1,0]$) reproduces `evaluation.normal_var` and
   `evaluation.normal_expected_shortfall` to floating-point tolerance.
2. Mixture CDF at the solved VaR returns $\alpha$ to $<10^{-10}$.
3. VaR and ES monotone in $\alpha$; $\mathrm{ES}(\alpha) < \mathrm{VaR}(\alpha)$ always.
4. Simulated draws from the fitted mixture breach the computed VaR at rate $\alpha$ within MC error.
5. State-prediction orientation: a hand-built asymmetric $P$ and known $\xi$ give the hand-computed $w$.

### 1.2 Horizon

**Primary $h=1$**, daily — where the tests have power and the result is clean.

**Secondary $h \in \{5,10,20\}$ days.** Harder: the $h$-period return is a mixture over regime
*paths*, not end-states ($k^h$). Exact enumeration to $h\approx10$ for $k=2$ (1,024 paths), Monte
Carlo beyond. Overlapping windows destroy independence, so inference uses non-overlapping blocks and
overlapping only for description. Secondary, and a gate on nothing.

### 1.3 Frequency: estimate daily, decide weekly

The unit of observation is the **trading day** (~8,400 SPY observations, not 1,750). The *decision*
stays weekly because the target is 1-4 actions per year.

**Consequence.** `markov_switching.RELIABLE_MIN_OBSERVATIONS = 520` was measured on *weekly* data and
does **not** transfer to daily by multiplying by 5. It must be re-measured by the same procedure
`walkforward.py` used — degenerate parameters, label flips, convergence failures, revision rate.
Until re-measured the daily minimum is unknown and is not asserted anywhere.

---

## 2. Data

| item | specification |
|---|---|
| primary asset | SPY, daily adjusted closes, `1993-02-01` → run date |
| replication assets | QQQ; one international developed and one EM ETF |
| price side | `^VIX` daily close, in logs (`data_loader.to_log_vix`) |
| returns | log returns of `auto_adjust=True` closes; adjustment accepted, leak register #6 |
| calendar | trading days present in the SPY series; no fills, no synthetic bars |
| VIX alignment | exact date match, **never** forward-filled; a gap is an error to investigate |

Multi-asset work must use the explicit-grid discipline that fixed the weekly case (leak register
#2b): resample or intersect on an explicit calendar, never trust a vendor's per-series anchoring.

---

## 3. Specifications to settle

These are choices *within* the model class, decided by the §5 battery rather than by assertion.

| # | choice | status |
|---|---|---|
| S1 | $k=2$ vs $k=3$ | corrected AIC **and** BIC both prefer $k=3$ decisively (ΔAIC 66, ΔBIC 44) on real data. An earlier README mandated $k=2$; that was a guess. |
| S2 | switching mean, or common mean | switching, currently. It reduces sign-blindness (up/down ratio 1.0000 → 0.9279) without removing it. |
| S3 | within-regime ARCH | untested. ARCH-LM rejects at 55.6 (p = 2.4e-11) *after* regime-switching, so volatility keeps moving inside regimes. MS(2) has exactly two possible conditional variances; at daily frequency that binds harder. |
| S4 | Gaussian vs Student-$t$ regime densities | untested. Fat tails inside regimes are the cheapest available fix if the density tests reject in the tail. |

**Context rungs** (not gates, not the subject): a constant unconditional VaR from the training window
answers "does conditioning help at all"; a RiskMetrics EWMA answers "does the model beat naive
conditioning." Both are cheap, both run first, and if the model cannot beat EWMA that is the answer
arriving early rather than a bug.

**Preregistered expectation, recorded so a negative is not a surprise.** At daily frequency the
ARCH-LM rejection gets *worse*, not better. The honest prior is that MS(2)-Gaussian fails the density
tests and that S3 or S4 is required. "A 2-state Gaussian Markov-switching model is insufficiently
specified for daily equity VaR, and here is by how much" is a real answer to the stated question.

---

## 4. Point-in-time protocol

Extends `POINT-IN-TIME-DISCIPLINE.md` from probabilities to VaR. **Every reported number is
out-of-sample under this scheme. There is no in-sample VaR table.**

1. **Vintage parameters.** The forecast for $t+1$ uses parameters estimated at the most recent refit
   at or before $t$. Filtered probabilities alone are not enough — leak register #2.
2. **Expanding window** primary; fixed rolling as the §6 sensitivity.
3. **Refit every 21 trading days.** Reported as a sensitivity, not tuned.
4. **Burn-in.** The first $N_{\min}$ observations produce no forecast and are excluded everywhere.
5. **Convergence failure policy, fixed in advance:** carry the previous vintage's parameters forward
   and log it. The count of carried vintages is reported. Dropping failed refits would select the
   sample on estimation success.
6. **Label resolution** by post-hoc variance argmax at every refit. Flip count is reported.
7. **One pass.** Scored once. Iterating a specification against out-of-sample results makes it an
   in-sample result silently.

---

## 5. Accuracy battery

### 5.1 Density calibration — primary, every observation

$u_t = F_{t|t-1}(r_t)$ from the density formed *before* $r_t$. Under correct specification
$u_t \sim \text{iid } U(0,1)$, for any model. Rosenblatt (1952); Diebold, Gunther & Tay (1998).

**Berkowitz (2001).** Transform $z_t = \Phi^{-1}(u_t)$, estimate

$$z_t = \mu + \rho z_{t-1} + \varepsilon_t, \qquad \varepsilon_t \sim N(0,\sigma^2)$$

LR test of $H_0: \mu=0,\ \rho=0,\ \sigma^2=1$, $\chi^2(3)$. Rejection decomposes usefully:
$\mu \ne 0$ location bias, $\sigma^2 > 1$ the model understates risk overall, $\rho \ne 0$ it fails
to track clustering.

**Censored Berkowitz** — the same LR restricted below the $\alpha$-quantile. A model can be calibrated
in the body and wrong in the tail; the full-sample version will not show it.

Reported alongside: PIT histogram (20 bins), PIT ACF, and the ACF of $(u_t-0.5)^2$ — the last detects
volatility dynamics the model has not absorbed.

### 5.2 Quantile coverage

At $\alpha \in \{0.10, 0.05, 0.01\}$, hit sequence $I_t = \mathbf{1}\{r_t < \mathrm{VaR}_{t|t-1}\}$.

| test | catches | status |
|---|---|---|
| Kupiec (1995) unconditional coverage | wrong average rate | **built** |
| Christoffersen (1998) independence / CC | first-order clustering | **built** |
| **Engle & Manganelli (2004) dynamic quantile** | any predictable structure in hits | **to build** |
| Christoffersen & Pelletier (2004) duration | clustering, better small-sample power | optional |

**DQ is the one that matters and it is missing.** Christoffersen's independence test asks only
whether a breach follows a breach — one lag of one variable. DQ regresses $\mathrm{Hit}_t = I_t -
\alpha$ on a constant, $p$ lagged hits, **and the VaR forecast itself**, then Wald-tests all
coefficients jointly. Including $\mathrm{VaR}_t$ is the substantive addition: it detects breaching too
often precisely when the model claims risk is high — invisible to Christoffersen, and exactly the
failure that would matter for an overlay. Report $p \in \{1,4\}$.

### 5.3 Expected shortfall

VaR ignores how bad breaches are; for a book whose problem is drawdown *depth*, ES is the more
faithful object. ES backtests are weaker than VaR backtests — a stated limitation, not worked around.

Primary check, unambiguous to implement: conditional on a breach, the realized return should average
to the predicted ES.

$$\mathbb{E}\left[r_t - \mathrm{ES}_{t|t-1} \mid r_t < \mathrm{VaR}_{t|t-1}\right] = 0$$

Stationary bootstrap over the breach subsample. Acerbi & Székely (2014) Test 2 in substance. Report
mean realized breach severity ÷ mean predicted ES; above 1 means the model understates tail depth.

> **Caution.** The formal Acerbi-Székely statistics and the Fissler-Ziegel (2016) joint (VaR, ES)
> score are stated under sign conventions that differ between papers and depend on whether losses are
> positive or returns negative. Do not implement either from memory or from this document. Verify
> against the source, and validate on a simulated case with known analytic ES first.

### 5.4 Ranking, once calibrated

Calibration is necessary, not sufficient — a correctly calibrated but uninformative VaR is exactly
what the constant rung is. Ranking needs a **consistent scoring function**: the asymmetric
piecewise-linear (tick) loss, Koenker & Bassett (1978),

$$L_\alpha(r,q) = (\alpha - \mathbf{1}\{r<q\})(r-q)$$

whose expectation is uniquely minimized by the true conditional $\alpha$-quantile. That uniqueness is
what makes a lower average tick loss evidence rather than an arbitrary metric. Only *differences* on
the same sample are interpretable. Compare on the loss-difference series with Diebold-Mariano using
Newey-West errors, or Giacomini & White (2006) for rolling-window estimation.

### 5.5 Incremental information over VIX

$$RV_{t,t+h} = a + b\,\mathrm{IV}_t + c\,X_t + \varepsilon_t$$

$RV$ realized downside risk over the horizon, $\mathrm{IV}$ implied volatility, $X$ the model's
measure. Newey-West mandatory. Built (`evaluation.encompassing_regression`).

If $c$ is insignificant the model says nothing the option market has not priced. That is a **capital
decision rule, not a verdict on the research** — most published volatility models do not cleanly beat
implied volatility, and whether model measures carry incremental information is long-running and
unsettled (Christensen & Prabhala; Blair, Poon & Taylor; Jiang & Tian).

---

## 6. Stability and reliability

Accuracy on one configuration is not a result if it moves under choices that should not matter. Each
row produces a reported number.

| # | check | why it can invalidate a result |
|---|---|---|
| R1 | **Seed dispersion.** Refit at seeds 1-20; spread of parameters, log-likelihood, headline statistics. | The mixture likelihood is multimodal and `statsmodels` uses random starts. A conclusion that moves with the seed is not a conclusion. |
| R2 | **Label-flip count** across refits. | A flip inverts the signal. 1 flip at the 520-week weekly minimum; unknown on daily. |
| R3 | **Convergence failures** and carried-vintage count (§4.5). | Undefined live behaviour. |
| R4 | **Vintage revision.** Live estimate at $t$ vs the same $t$ recomputed at later refits. | The honest cost of real-time operation; ~7.5% state revision weekly. Headline reliability number, not a footnote. |
| R5 | **Filtered vs smoothed.** Full battery on Kim-smoothed probabilities, side by side. | Quantifies how much apparent skill in naive regime studies is hindsight (9.7% of weeks disagree at 0.5). Smoothed is reported **only** as a hindsight illustration. |
| R6 | **Window length.** Expanding vs 5y / 10y / 20y rolling. | A result that depends on window choice is a result about the window. |
| R7 | **Refit cadence.** 5 / 21 / 63 days. | As R6. |
| R8 | **Subsamples.** Pre-2008 / 2008-2015 / post-2015, and with GFC and COVID excluded. | A verdict driven entirely by 2008 and 2020 has effective $n=2$. |
| R9 | **Cross-asset replication.** Same battery, same code, QQQ and international. | The cheapest guard against overfitting one series. No asset dropped after the fact. |
| R10 | **Numerical parity.** §1.1 checks 1-5. | Silent numerical error looks like a model finding. |

**Effective sample size.** Distinguish everywhere between *observations* and *independent events*.
Coverage tests over 8,400 days are genuinely powerful. A claim about crisis behaviour rests on ~5
crises whatever the table's row count. Every inductive claim carries its honest effective $n$.

---

## 7. Preregistered decisions

Fixed now so they cannot be adjusted to fit an outcome. These are project decision rules; none makes
the research result uninteresting.

| # | condition | consequence |
|---|---|---|
| D1 | Berkowitz and DQ both reject at $\alpha=0.05$ across R8 subsamples, for every specification in §3 | No conditional VaR reaches any live path. Report the failure — it answers the question. |
| D2 | The model loses to the EWMA rung on tick loss, DM significant at 5% | The specification is rejected for this purpose. A better-specified conditional model takes the slot. |
| D3 | $c \approx 0$ in §5.5 | **No capital is committed.** VIX is free and needs no model. The result is still reported. |
| D4 | Any headline verdict flips under R1 (seed) or R6 (window) | Not reportable as stated. Report the instability instead. |
| D5 | D1-D3 all clear | *Only then* is economic value designed, in its own preregistration. |

**Nothing economic is designed, implemented or run until D5.** A premature version was written and
deleted on 2026-08-12 because it preregistered a test of a specification then in question. Do not
rebuild it early.

**Known threat to D5, recorded now.** A causal filter is late by construction — it must observe bad
returns before raising the probability. For a put buyer the lag is transmitted through premium: by
the time the measure fires, implied volatility has repriced. This threatens economic value
specifically, not calibration, and it is why D5 is gated rather than assumed.

---

## 8. Reporting skeleton

Fixed in advance so the analysis has a target and cannot sprawl.

- **Table 1** — data and sample: span, $n$, burn-in, out-of-sample $n$, exceedance counts by $\alpha$.
- **Table 2** — density calibration: Berkowitz LR full and censored, decomposed into
  $\mu/\rho/\sigma^2$, per specification. *Primary result.*
- **Table 3** — coverage: Kupiec, Christoffersen IND/CC, DQ(1), DQ(4), per specification per $\alpha$.
- **Table 4** — ES: breach-severity ratio and bootstrap interval.
- **Table 5** — tick loss and DM statistics against the context rungs.
- **Table 6** — reliability: R1-R9 as rows, verdict stability as columns.
- **Table 7** — encompassing regression against VIX, Newey-West, per horizon.
- **Figure 1** — PIT histogram and ACF.
- **Figure 2** — VaR path through 2008 and 2020, realized returns and breaches marked.
- **Figure 3** — mixture VaR minus moment-matched normal VaR against regime uncertainty $w$ (§1.1).
- **Figure 4** — filtered vs smoothed VaR paths (R5).

---

## 9. Out of scope

- **Economic value, hedge sizing, strikes, tenor, premium, P&L.** Gated on D5.
- **Crisis-detection hit rate, lead time, accuracy on hand-selected episodes.** Permanently excluded:
  invented after seeing the data, each selects its own test bed from hindsight.
- **Risk tiers.** The 0.20 / 0.60 bands are not used anywhere. Removed from code 2026-08-12.
- **Statistical jump models, intraday data, Hawkes processes, K-means, binary classifiers.**
- **Any claim of edge over the option market.**

### Amendments

*None yet. Every change to §1-§8 after a result exists is logged here with date and reason.*

---

## 10. Build order

1. ~~**`src/predictive.py`** — mixture density: state prediction, CDF, VaR by Brent, ES closed form.~~
   **Done 2026-08-12.** 23 checks, including all five §1.1 requirements. statsmodels'
   `regime_transition` was verified empirically at $k=2$ and $k=3$ to be stored `[to, from]` with
   columns summing to one; `transition_matrix` does that transpose in one place and cross-checks
   against the `p[i->j]` named parameters.
2. **Extend `src/evaluation.py`** — PIT and Berkowitz (full and censored), DQ, tick loss, ES
   breach-severity bootstrap, DM/GW. Each with a known-answer check: correctly-specified simulated
   data must **fail to reject**, deliberately miscalibrated data must **reject**. A test that never
   rejects is worse than no test.
3. **Context rungs** — constant and EWMA end-to-end through the battery. Shakes out the harness before
   any model number is quoted.
4. **Daily data** — `data_loader` daily path, and re-measure $N_{\min}$ (§1.3).
5. **Walk-forward VaR** — extend `walkforward.py` from probabilities to predictive densities under §4,
   emitting vintage-correct VaR/ES/PIT series.
6. **The §3 specifications** — S1 through S4.
7. **§6 reliability sweep** — R1-R10.

---

## 11. Reading list

- Rosenblatt (1952); Diebold, Gunther & Tay (1998) — PIT, density forecast evaluation.
- **Berkowitz (2001)** — the §5.1 test.
- Kupiec (1995); **Christoffersen (1998)** — coverage and independence.
- **Engle & Manganelli (2004)**, *CAViaR* — the DQ test.
- Christoffersen & Pelletier (2004) — duration-based backtests.
- Koenker & Bassett (1978) — tick loss and quantile consistency.
- Acerbi & Székely (2014); **Fissler & Ziegel (2016)**; Patton, Ziegel & Chen (2019) — ES backtesting
  and joint elicitability. Verify sign conventions against the sources (§5.3).
- Diebold & Mariano (1995); **Giacomini & White (2006)**; Clark & West (2007) — forecast comparison.
- **Hamilton (1989)**; Frühwirth-Schnatter (2006) — the model class and label switching.
- Hamilton & Susmel (1994); Gray (1996) — regime-switching with within-regime ARCH (S3).
- Andersen & Bollerslev (1998) — realized volatility; why daily beats weekly.
- Christensen & Prabhala (1998); Blair, Poon & Taylor (2001); Jiang & Tian (2005) — the §5.5
  literature.
