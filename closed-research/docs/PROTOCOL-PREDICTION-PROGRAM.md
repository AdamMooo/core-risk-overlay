> # CLOSED 2026-08-17 — preregistration of the completed prediction program
>
> This is the protocol of the closed prediction/regime program, preserved intact so that D3, F2, E4,
> E5 and E8 remain interpretable against the design that produced them. **It is not binding on the
> active program.**
>
> **What was harvested into the active protocol** (`../../docs/RESEARCH-PROTOCOL.md`): §0's stub gate
> and §0.2's standing principles P1-P10. They are the best process assets this repo produced and they
> transfer with adaptation.
>
> **What did not transfer, because it is specific to a question no longer asked:** §1 the estimand
> (a one-step predictive density), §1.2-1.3 horizon and frequency, §3 specifications S1-S4, §5 the
> accuracy battery, §7 the D1-D5 decision gates, §8 the reporting skeleton, §10 the build order, §11
> the reading list. The active program's gates are [[CHARTER]] §8 and its objective space is
> [[CHARTER]] §3.
>
> **§Amendments is the most valuable section here** and is left untouched. It records the process
> failures honestly, including the 2026-08-14 rediscovery of Timmermann's Proposition 5 that was
> already sitting UNREAD in the reading list, and the 2026-08-13 horizon amendment. Read it as method.

---

# Research Protocol

Last updated: 2026-08-13

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

## 0. Rules of engagement — the gate every experiment passes before code is written

**Why this section exists.** On 2026-08-13 the context rungs were run and the result recorded as
*"the model does not beat a moving average."* Three devices already in this document each forbade
it: the header above says **"Not a horse race"**; §3 requires a **preregistered expectation** so a
negative is not a surprise; §11 line for Hamilton & Susmel (1994) cites the paper that already
answers the specification question. The outcome was entailed by theory before the code ran — a
one-step tick-loss comparison between MS(2) and RiskMetrics EWMA cannot distinguish them, because
their one-step conditional variances nearly coincide by construction. The rules existed. Nothing
made them run *before* the experiment. This section is that gate.

**No experiment runs until a five-field stub is committed.** If any field cannot be filled honestly,
the experiment does not run. The stub is committed *before* the commit carrying its results.

1. **Claim tuple — `(frequency, horizon, functional, sample)`.** A test of a one-step *marginal*
   cannot support a claim about a *path* functional, at any sample size. Drawdown is a path
   functional; VaR at $h=1$ is a marginal one. The tuple appears in the heading of every section
   that reports the result, so no reader can inherit a wider claim than was measured.
2. **Predicted outcome, with its reason, written before any code.** If the prediction is confident
   and derivable from theory or a citable paper, **the run carries no information — do not run it.**
   Record the prediction and its source instead. This is the §3 device, made mandatory.
3. **Literature check.** Name the paper that already settles this, or state in writing that none
   does. §11 is a gate, not a list to admire. A finding rediscovered empirically that was already in
   a cited paper is a process failure and gets logged as one.
4. **Mechanism for a difference.** For any comparison: state the structural difference between the
   two objects, **the horizon at which it becomes observable, and the FUNCTIONAL on which it becomes
   observable.** If the difference is invisible at the proposed horizon *or* invisible in the
   proposed functional, the comparison is void and does not run. EWMA is IGARCH — its
   multi-step variance forecast is a martingale and never reverts; MS($k$) reverts toward the
   stationary regime mix at a rate set by the second eigenvalue of $P$. That is the whole difference
   between them and it is exactly zero at $h=1$.

   **The functional clause was added 2026-08-14 and it is not redundant with the horizon clause —
   they catch different failures.** The $h=1$ EWMA comparison was void on *horizon*. The proposed
   $h=13$ GARCH comparison is void on *functional*: for **any** $h$, both
   $\mathbb{E}_t[\sigma^2_{t+h}]$ are `long-run level + (geometric rate)^h × current deviation`,
   a single state-independent rate each — the same two-parameter curve. Moving to $h>1$ does not
   rescue a point-variance comparison. The models separate only in the **shape of the $h$-step
   density**, because MS mixes over $2^h$ regime paths and a single-regime GARCH cannot. **Naming
   the horizon without naming the functional would have licensed the same mistake twice.**
5. **What would surprise me, and what decision it changes.** Name the outcome that would move a
   decision in §7. If no outcome moves any decision, the run is decoration and does not run.

**Two firewalls, absolute.**

- **Statistical loss never licenses an economic claim, and no economic claim rests on a loss
  function.** No sentence may contain both a loss-function number and a cost-benefit judgement.
  "Indistinguishable on tick loss" says *nothing* about economic value; economic value is gated on
  D5 and has never been measured here.
- **A verdict may not exceed its claim tuple.** Absent a horizon at which two models differ, the
  only sayable sentence is "indistinguishable at horizon $h$, as predicted" — never "does not beat",
  never "thin return", never any word implying the model was given a fair chance to differ.

**Standing consequence.** D2 in §7 is written as a tick-loss horse race and inherits this defect: it
does not name a horizon. It is not actionable until amended, and no D2 verdict may be recorded
against a $h=1$ comparison.

### 0.2 Standing research principles

Added 2026-08-14. These govern *what to work on and why*, where the five-field stub above governs
*whether a specific run may happen*. Most were already latent in this document; they are written
down because a principle that lives only in a conversation stops binding when the conversation ends.

**P1 — The governing question, asked at every stage.**

> **What does this model know that the simpler alternative does not?**

Answerable and convincing → build on it. Not answerable → stop. This is the whole programme in one
line.

**P2 — Identifiability before implementation.** Ask *what mathematical object actually differs*
before asking what to run. Two models producing the same functional at the proposed horizon do not
become distinguishable by collecting more data. **The response to an uninformative experiment is to
redesign it, not to enlarge it.**

**P3 — Three questions, never collapsed.** (A) What does the model measure? (B) Does the
measurement carry incremental information? (C) Is that information useful to a portfolio? **A → C
directly is forbidden.** A statistically interesting representation does not license a rule. Current
state: A answered (width, not direction — `TRANSLATION-LAYER.md`); B is the live question; C is
gated on D5 and untouched.

**P4 — Do not optimise toward usefulness.** "Adds nothing beyond GARCH" and "adds something" are
both successful outcomes. The objective is to discover what information the model contains, not to
make it win. A result that has to be hunted for is not a result.

**P5 — Mechanism first, then test.** `mechanism → observable consequence → test → falsification
criterion`. Never start from "what backtest should we run"; start from *what would have to be true
for this model to carry information the alternative lacks*, then build the **smallest** experiment
that separates those possibilities.

**P6 — Literature is part of the model, not a citation duty.** It supplies known mechanisms, already-
tested specifications, redundant comparisons, questionable assumptions, and alternative explanations
requiring control. **Do not collapse distinct model classes into "regime switching":**

| class | within-regime dynamics | example in the literature |
|---|---|---|
| **plain MS** | none — constant variance inside each regime | **what this repo fits** |
| **GARCH / GJR / EGARCH** | smooth, single regime | the opponent |
| **SWARCH / MS-GARCH** | ARCH or GARCH *inside* each regime | Hamilton & Susmel (1994); Marcucci (2005); this repo's **S3** |

Conflating row 1 with row 3 misreads a paper as evidence about a model it never fitted. Both
blocking papers in `STUB-GARCH-ENCOMPASSING.md` §14.2 are row 3.

**P7 — The reason for the code is the hypothesis, not the code.** Identical lines carry different
claims and need different evidence. `if wide: size *= 0.5` is **variance targeting** (supported) or
**"wide predicts losses"** (refuted) depending only on the stated reason. **The reason is written
next to the line, always.** Be most suspicious when a result is attractive: ask whether it measures
what it appears to.

**P8 — Ask whether the comparison is about information sets or about structure.** If
$\mathcal{F}^{(A)}_t \neq \mathcal{F}^{(B)}_t$, the result is about *access*, not *estimator
quality*, and no amount of modelling closes the gap. VIX failed here — it observes the option
market, so `F^returns ⊆ F^market` and containment is structural. **GARCH does not**: it and the MS
model compress the *same* return history, each into a one-dimensional statistic, differing only in
*how*. That is what makes it a legitimate specification comparison and not D3 again.

**P9 — Complexity does not count as evidence.** Each rung must earn its place by incremental
information:

```
simple observable  ->  smooth model  ->  regime model  ->  regime + within-state dynamics
```

An interesting *interpretation* is not a role. If GARCH explains everything the regime state
explains, the regime model has not earned one. Conversely, a distributional feature GARCH **cannot**
reproduce is the justification for going further.

**The concrete ladder for this repo, with the status of each rung:**

| rung | specification | status |
|---|---|---|
| 0 | **constant** (expanding mean/sd) | **run.** Model beats it on tick loss, DM significant at 10% and 5%. Conditioning on *something* helps. |
| 1 | **EWMA / IGARCH** | **run at $h=1$ and VOID there** — martingale variance, no reversion, difference from MS exactly zero one step ahead. |
| 2 | **GARCH(1,1)**, smooth single regime | **never built.** GJR-GARCH(1,1) declared alongside as a stronger opponent, not as the mechanism test. |
| 3 | **plain MS** — switching mean and variance, no within-regime dynamics | **built and characterised.** What this repo actually fits. |
| 4 | **SWARCH / MS-GARCH** — ARCH inside each regime | **not built.** This repo's S3. Where Hamilton & Susmel (1994) and Marcucci (2005) both sit. |

**Two rules on the ladder.** (a) **Do not ask a richer rung to rescue a failed experiment
retroactively** — the order is `experiment → result → diagnosis → new stub → next specification`,
and a rerun on a richer model prompted by a null is a search for a version that passes. (b) The
literature's strong evidence for **rung 4** does not settle the behaviour of **rung 3**; it
constrains interpretation and motivates the next rung if rung 3 fails. Rungs 3 and 4 are different
models and are never both called "regime switching".

**P10 — Enforce these against whoever proposes the violation, including the person directing the
work.** Push back, in writing, on: turning width into direction; treating labels as economically
meaningful without evidence; optimising thresholds before a mechanism exists; running models that
are structurally indistinguishable at the chosen horizon *or functional*; interpreting a null
without power; citing a paper without checking what it tested; introducing a rule before the
measurement's usefulness is established; adding complexity without naming its incremental
information.

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

**Amended 2026-08-13** — see §Amendments. Horizon was previously "secondary, and a gate on nothing."

**$h=1$ is the prerequisite, not the verdict.** One-step density calibration is what earns the right
to say anything at any horizon: an estimator whose one-step conditioning is dishonest cannot be
trusted about paths. It is necessary, it is built, and it is where the tests have power. It is *not*
where this model class differs from anything.

**Multi-period is co-primary, because the model's content lives there.** The distinguishing structure
of a Markov-switching model is persistence and mean reversion: $w_{t+h} = \xi_t' P^h$ converges to the
stationary regime mix at a rate set by the second eigenvalue of $P$. An EWMA is IGARCH — its
multi-step variance forecast is a martingale and never reverts. **That difference is exactly zero at
$h=1$ and grows with $h$.** Scoring only $h=1$ marginalizes out the one thing the model was chosen
for, and any comparison at $h=1$ is void under §0.4.

**The mandate's object is a path functional.** Drawdown depth over a holding period is a property of
the whole path, not of the marginal distribution at any single step. Two processes can share
identical one-step marginals at every $t$ and have completely different drawdown distributions,
because drawdown depends on the serial dependence — which is precisely what $P$ encodes. No sample
size at $h=1$ can substitute.

**Mechanics.** The $h$-period return is a mixture over regime *paths*, not end-states: $k^h$ of them.
Exact enumeration to $h \approx 10$ for $k=2$ (1,024 paths), Monte Carlo beyond. Every input needed —
vintage $P$, regime means and variances, filtered $\xi_t$ — is already produced by `walkforward.py`.
No new estimator, no new fitting, no new specification.

**Frequency is a separate and still-open decision** (§1.3). Horizon is stated in periods here
deliberately; the period length does not change any argument above.

**The power problem, stated before running rather than discovered after.** The horizon where this
model can differ is the horizon where proof is hardest. Non-overlapping 13-period blocks over 1,230
observations give ~94 independent observations, and any drawdown claim rests on 3-4 systemic episodes
whatever a table's row count says (§6, effective sample size). **Overlapping windows are permitted for
description only and never for inference** — inflating $n$ by overlap is the single most available way
to fake a result here, and it is forbidden.

**Preregistered third outcome.** "Indeterminate — cannot be settled on 33 years of one index" is a
legitimate and reportable finding, accepted now so that the pressure to manufacture $n$ has no
purchase later. It is also what makes sample extension (a longer index history, or the multi-asset
mandate) a *power* decision rather than a nice-to-have.

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

**Censored Berkowitz** — the same LR restricted below the $\alpha$-quantile, testing
$H_0: \mu=0,\ \sigma^2=1$ against $\chi^2(2)$. $\rho$ is **dropped**: once the sample above the cutoff
is censored to a single indicator, the AR coefficient is not identified. See the amendment below. A
model can be calibrated in the body and wrong in the tail; the full-sample version will not show it.

Both are built (`evaluation.berkowitz_test`, `evaluation.censored_berkowitz_test`) on the exact
likelihood, with the null and alternative evaluated through the same function so $LR \ge 0$ by
construction rather than by hope. The discriminating case is measured, not asserted: a standardized
$t(4)$ scored as $N(0,1)$ — zero mean, unit variance, no dependence, wrong only in the tail — gives
full $p = 0.89$ and censored $p = 4\times10^{-37}$.

**Blind spot, measured.** $\rho$ tests autocorrelation in the *level* of $z$. Volatility dynamics the
model has not absorbed live in $z^2$ and are invisible to the full LR: a stochastic-volatility series
scored at constant volatility returns $\mu=0.007$, $\rho=0.041$, $\sigma^2=0.998$, $p=0.07$ — **not
rejected** — while the Ljung-Box on $(u_t-0.5)^2$ rejects at $p<10^{-16}$. A passing Berkowitz is
never read without that companion statistic. This is the §3 open question about within-regime ARCH
appearing in the scoring layer.

**PIT clipping.** $u_t \in \{0,1\}$ sends $z_t$ to $\pm\infty$. Clipping at $10^{-10}$ is
unavoidable; every result carries `n_clipped`, because a clipped observation is the model's *worst*
miss — the density called the realized return impossible — and silently absorbing it would delete the
most informative failure in the sample.

Reported alongside: PIT histogram (20 bins), PIT ACF, and the ACF of $(u_t-0.5)^2$ — the last detects
volatility dynamics the model has not absorbed.

**Open gap: the Ljung-Box lag count is not preregistered, and the result depends on it.** On the
2026-08-13 SPY run, $(u_t-0.5)^2$ gave $p$ = 0.0004 / 0.0075 / 0.045 / 0.062 / 0.099 / 0.108 at
5 / 10 / 15 / 20 / 26 / 52 lags. The dependence is concentrated at lags 1-4 and dilutes as
uninformative lags are added, so the finding is real but **short-horizon**. Quote the sweep, never a
single $p$. Choosing a lag count now would be post-hoc selection under §9; it is fixed only when a
specification is next amended, and before the run that uses it.

**The 20-bin histogram is not a tail check.** At $n \approx 1{,}200$ the entire $\alpha=0.01$ story
sits inside the leftmost bin. Use the QQ plot of $z_t$ and the censored LR for the tail; the
histogram speaks to the body.

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
- **Figure 1** — PIT histogram and ACF. **Built** (`figures.py`).
- **Figure 2** — VaR path through 2008 and 2020, realized returns and breaches marked. **Built.**
- **Figure 3** — mixture VaR minus moment-matched normal VaR against regime uncertainty $w$ (§1.1).
  **Built.**
- **Figure 4** — filtered vs smoothed VaR paths (R5). Needs the smoothed path; not built.

`figures.py` draws nothing outside this list, so the analysis cannot sprawl into whatever happens to
look interesting. The one addition, `fig_tail_failure`, plots only quantities Tables 3 and 4 already
report (breach rate by $\alpha$, ES ratio, QQ of $z_t$) and introduces no new measure.

---

## 9. Out of scope

- **Economic value, hedge sizing, strikes, tenor, premium, P&L.** Gated on D5.
- **Crisis-detection hit rate, lead time, accuracy on hand-selected episodes.** Permanently excluded:
  invented after seeing the data, each selects its own test bed from hindsight.
- **Risk tiers.** The 0.20 / 0.60 bands are not used anywhere. Removed from code 2026-08-12.
- **Statistical jump models, intraday data, Hawkes processes, K-means, binary classifiers.**
- **Any claim of edge over the option market.**

### Amendments

Every change to §1-§8 after a result exists is logged here with date and reason.

**2026-08-14 — PROCESS FAILURE under §0 rule 3: `memory_diagnostic.py`'s deductive result was
published in 1999 and sat `[UNREAD]` as row 2 of the reading list.**

§0 rule 3: *"A finding rediscovered empirically that was already in a cited paper is a process
failure and gets logged as one."* This is that log. Timmermann (1999/2000) was **read in full**
on 2026-08-14 from the LSE FMG working paper (DP 323).

On 2026-08-13 this repo derived and recorded as a "deductive result — algebra, not a fitted claim":

```
Cov(r[t]^2, r[t+k]^2) = pi_0 * pi_1 * (v_0 - v_1)^2 * lam^k          (repo, 2026-08-13)
```

Timmermann's **Proposition 5 / eq. (30)**, for the same model, is:

```
Cov(y[t]^2, y[t-n]^2) = pi_1 (1 - pi_1) (mu_2^2 - mu_1^2 + sigma_2^2 - sigma_1^2)^2 vec(P^n)' v_1
```

with first-order case scaling by $(p_{11}+p_{22}-1)$ — the repo's $\lambda$. **Same result.** The
registry's own reading-order note already said row 2 *"give[s] the h=1 near-equivalence with an
EWMA analytically"*, and it was not read.

**The repo's version is also formally incomplete:** it drops the mean terms
$(\mu_2^2 - \mu_1^2)$, which are absent only when the means are common. Our model switches means.
Measured at the fitted parameters ($\mu = +0.36\%, -0.26\%$; $\sigma = 1.50\%, 3.84\%$) the mean
contribution is $-6.20\times10^{-6}$ against a variance term of $1.2496\times10^{-3}$, so the
repo's formula **overstates the autocovariance by 1.00%**. Numerically negligible here; formally
wrong, and now corrected. No conclusion in the repo changes.

**2026-08-14 — asymmetric interpretation of the MS-vs-GARCH experiment made binding.**

Recorded in full at `STUB-GARCH-ENCOMPASSING.md` §11.1-§11.5; the load-bearing points, so they
survive independently of that file:

- **$H_0^{\text{spec}}$ and $H_0^{\text{struct}}$ are different hypotheses.** The experiment tests
  whether *plain MS* adds density information over GARCH. It **cannot** establish that discrete
  regime structure adds nothing, at any sample size, because the base specification is
  independently known to be misspecified within regimes (ARCH-LM 55.6, $p = 2.4\times10^{-11}$).
- **A null is reportable only as** *"no incremental information was detected from this particular
  plain-MS specification relative to the tested GARCH benchmark."*
- **No retroactive repair.** A null does not license swapping in SWARCH/MS-GARCH and rerunning.
  The order is `experiment → result → diagnosis → new stub → next specification`. The S3 question
  ("does within-regime ARCH recover information plain MS fails to express?") is a *subsequent*
  experiment.
- **Three verdicts, assigned before any conclusion is written: POSITIVE / NULL / INCONCLUSIVE.** A
  result failing the power requirement is **INCONCLUSIVE, never NULL**.
- **The positive branch is confounded too**, which the amendment as proposed did not cover:
  `markov_switching.py` fits a **switching mean** as well as a switching variance, while the GARCH
  benchmark has a constant mean, so a positive could be the mixture *mean* rather than the regime
  *variance* structure. A **common-mean MS variant is now a required companion**, without which a
  positive result is not interpretable. §10's criteria amended accordingly.
- **P9's ladder made concrete** with per-rung status (§0.2). Rungs 3 (plain MS) and 4
  (SWARCH/MS-GARCH) are never both called "regime switching".

*Not selected on a result* — no code has been run for this comparison.

**2026-08-14 — §0 rule 4 amended to require the FUNCTIONAL; §0.2 standing principles added.**

*Rule 4.* Previously required naming the structural difference and **the horizon** at which it
becomes observable. It now also requires naming **the functional**. The gap was found while writing
`STUB-GARCH-ENCOMPASSING.md`: for a Markov-switching model against GARCH(1,1), both
$\mathbb{E}_t[\sigma^2_{t+h}]$ take the form `long-run level + (geometric rate)^h × current
deviation` with a single state-independent rate each, **at every $h$**. So a point-variance
comparison is void on *functional* however the horizon is chosen — the $h=1$ EWMA failure repeated
on a different axis, and rule 4 as written would not have caught it. The models separate in the
**shape of the $h$-step density**, where MS mixes over $2^h$ regime paths.

*Not selected on a result* — no code was run and no result exists for this comparison. Logged here
rather than silently edited because §0 binds itself.

*§0.2.* Ten standing principles governing what to work on, as distinct from the five-field stub
which governs whether a given run may happen. Includes P6's model-class taxonomy (plain MS vs
GARCH vs SWARCH/MS-GARCH), which corrects a live conflation risk: both papers blocking the GARCH
stub fit **within-regime ARCH**, so they are evidence about **S3**, not about the plain
switching-variance model this repo fits. §11 cites Hamilton & Susmel as answering "the
specification question" and that phrasing should be re-checked against the paper when it is
obtained.

**2026-08-13 — D3 FIRED. §5.5 run; consequence applied.**

`encompassing.py`. Forward downside semivolatility on log VIX and the model's `-ES(0.05)`, weekly,
$h \in \{4, 13\}$, SPY 2003-2026, 1,230 walk-forward forecasts, non-overlapping stride-$h$ for
inference per §1.2. At $h=4$, $n=307$: $c = +0.0009$, $p = 0.9935$. Joint $R^2 = 0.1015$ against
VIX-alone $R^2 = 0.1015$ — identical to four decimals. Model alone $R^2 = 0.0471$. $h=13$ agrees.
Alignment verified adversarially (leaky 0.2488 > true 0.1015 > stale 0.0769).

**Consequence, as preregistered: no capital is committed.** The model's downside information is
strictly nested inside implied volatility for this functional at these horizons.

*Scope of the verdict, stated so it is not over-read.* $X$ was a **level**. This tests whether the
model's *height* adds to VIX's height. It does not test persistence, which is the model's actual
content and is untested. §1.2's amendment predicted exactly this failure of level-based scoring and
the run reproduced it. **D3 closes the level-based case only.**

*Consequence for §3.* S3 and S4 address marginal and tail-shape properties — level properties. They
cannot answer the untested question and are deprioritized rather than retired. §10's build order
still lists them ahead of any dynamics test and is stale in that respect.

**2026-08-13 — §1.3 daily path built; the frequency decision is now load-bearing and measured.**

`data_loader.download_daily_prices` / `load_daily_log_returns`, cached at `data/spy_daily.csv`.
All 64 checks pass unchanged.

The weekly series **cannot identify volatility decay shape at all**: at $n = 1{,}750$ the
white-noise ACF band is $\pm 0.0469$ and the empirical squared-return ACF falls inside it by lag 8.
At daily frequency ($n = 8{,}441$, band $\pm 0.0213$) the ACF is significant out to **lag 212**,
about ten months, with 54% of lags 1-250 significant.

*A claim was made and refuted the same day, recorded under §0 rather than quietly dropped.* It was
asserted that volatility exhibits power-law memory that a finite-state Markov chain structurally
cannot match, and that MSM (Calvet & Fisher) or HAR (Corsi) was therefore required. On daily SPY
the **exponential fit wins** ($R^2$ 0.7192 against 0.6219 over lags 1-250; 0.8644 against 0.7719
over 1-63), and $H = 0.423$ is below 0.5. The measured gap is one of **duration, not shape** — the
model's implied memory reaches ~138 trading days against the data's 212.

The refutation is itself weak and must not be over-read either: the verdict **flips with the
window** (exp / power / exp across 1-63, 1-126, 1-250), which is a D4 condition; the ACF is
non-monotone at lags 1-5; and an $R^2$ race on log-ACF is not a long-memory test — GPH or local
Whittle, estimating $d$ with a standard error, is. The likely cause is that squared daily returns
are a noisy variance proxy whose measurement error attenuates the ACF at long lags
(Andersen & Bollerslev 1998, `[skim]`, already listed in §11).

*Neither claim is settled.* The open item is a better daily volatility proxy — range-based
estimators from OHLC (Parkinson 1980; Garman-Klass 1980; Rogers-Satchell 1991; Yang-Zhang 2000),
which stay inside §9's exclusion of intraday data — followed by a real long-memory test.

**2026-08-13 — §1.2, horizon promoted from "secondary, and a gate on nothing" to co-primary.**

*Reason, stated as a structural argument rather than a result.* The distinguishing content of a
Markov-switching model is persistence and mean reversion, carried by $P$. At $h=1$ its conditional
variance nearly coincides with a tuned EWMA's, so the two models are indistinguishable there **by
construction, not by measurement.** The entire battery as originally written scored $h=1$ only, which
marginalizes out the property the model was selected for. Separately, the mandate's object — drawdown
depth over a holding period — is a *path* functional, and path functionals are not determined by
one-step marginals at any sample size, because they depend on the serial dependence $P$ encodes.

*Why this is admissible under §0 and not outcome-driven.* The argument is deductive and would have
held before any data was seen; it rests on the algebra of $P^h$ and on EWMA's IGARCH martingale
property, neither of which involves a fitted number. It **widens** what must be tested rather than
narrowing it, and it makes the null it replaces *harder* to claim, not easier: the $h=1$ tick-loss
comparison that previously fed D2 is now explicitly void (§0, standing consequence). No existing
result is reinterpreted as favourable — the $h=1$ calibration findings stand exactly as measured, and
the $\alpha=0.01$ tail failure across every Gaussian estimator is untouched.

*Prompted by a process failure, recorded so it stays visible.* On 2026-08-13 a one-step tick-loss
comparison was run and recorded as "the model does not beat a moving average." That outcome was
entailed by theory before the code ran. §0 was written the same day as the gate that must run first,
and this amendment fixes the design defect §0 exposed. Under §0.3, Timmermann (2000) — closed-form
Markov-switching moments — and Rydén, Teräsvirta & Åsbrink (1998) are `[UNREAD]` and now block the
horizon work until read; both are directly on this question.

*Consequences elsewhere, not yet applied.* D2 in §7 names no horizon and is not actionable until
amended. §5.4 ranking and §8 Table 5 inherit the $h=1$ assumption. §10 build order still lists $h=1$
refinements ahead of any horizon work. Each is a separate amendment and none is made here.

**2026-08-13 — §5.1, censored Berkowitz is $\chi^2(2)$, not $\chi^2(3)$.** As originally written §5.1
said "the same LR restricted below the $\alpha$-quantile", implying all three restrictions. $\rho$ is
not identified on a censored sample: observations above the cutoff enter the likelihood only through
$\Pr(z > z^*)$, so the lag structure that $\rho$ describes is unobserved for the large majority of the
sample. The tail test therefore restricts $(\mu, \sigma^2)$ only, against $\chi^2(2)$ — the standard
form. Decided **before any real-data result existed**, on identification grounds, not to move a
p-value.

---

## 10. Build order

1. ~~**`src/predictive.py`** — mixture density: state prediction, CDF, VaR by Brent, ES closed form.~~
   **Done 2026-08-12.** 23 checks, including all five §1.1 requirements. statsmodels'
   `regime_transition` was verified empirically at $k=2$ and $k=3$ to be stored `[to, from]` with
   columns summing to one; `transition_matrix` does that transpose in one place and cross-checks
   against the `p[i->j]` named parameters.
2. **Extend `src/evaluation.py`** — Each with a known-answer check: correctly-specified simulated
   data must **fail to reject**, deliberately miscalibrated data must **reject**. A test that never
   rejects is worse than no test.
   - ~~PIT, Berkowitz full and censored, PIT histogram/ACF/Ljung-Box.~~ **Done 2026-08-13.** 23
     checks: null quiet on both forms; understated risk, location bias and serial dependence each
     rejected *and* correctly diagnosed by the parameter that owns them ($\sigma^2 \to 2.25$,
     $\mu \to 0.5$, $\rho \to 0.6$); the body-correct/tail-wrong case separating the two forms; the
     $z^2$ blind spot; clip counting; validation.
   - **DQ (Engle-Manganelli)** — next.
   - **Tick loss and DM/GW.**
   - **ES breach-severity bootstrap.**
3. **Context rungs** — constant and EWMA end-to-end through the battery. Shakes out the harness before
   any model number is quoted.
4. **Daily data** — `data_loader` daily path, and re-measure $N_{\min}$ (§1.3).
5. **Walk-forward VaR** — extend `walkforward.py` from probabilities to predictive densities under §4,
   emitting vintage-correct VaR/ES/PIT series.
6. **The §3 specifications** — S1 through S4.
7. **§6 reliability sweep** — R1-R10.

---

## 11. Reading list — a §0.3 gate, not a list to admire

**Status marks: `[read]` · `[skim]` · `[UNREAD]`.** An `[UNREAD]` entry whose question is about to be
investigated empirically **blocks that experiment** under §0.3. Full metadata and acquisition status
live in `literature/README.md`.

**On 2026-08-13 the entry for Hamilton & Susmel (1994) was already in this list, marked nothing, and
S3 was rediscovered empirically instead of read.** That is the failure §0 exists to stop.

### Would have prevented the 2026-08-13 waste — read these first

- **Rydén, Teräsvirta & Åsbrink (1998)** `[UNREAD]` — a hidden Markov model reproduces most stylized
  facts of daily returns but **fails specifically on the slow decay of squared-return
  autocorrelation.** That is this repo's ARCH-LM rejection of 55.6, published 1998.
- **Timmermann (2000)** `[READ IN FULL 2026-08-14]` — moments and autocorrelation structure of
  Markov-switching models in closed form. Gives the $h=1$ near-equivalence with an EWMA
  analytically, which is the result the rungs spent a run discovering. **Version caveat: what was
  read is the free author copy — LSE Financial Markets Group DP 323, May 1999 — not the published
  *J. Econometrics* 96(1), 75-111 article. They may differ.** Findings and the INFORMS adjudication
  are at `literature/README.md` row 2 and `STUB-GARCH-ENCOMPASSING.md` §14.3; the process
  failure it exposed is logged under §Amendments above.
- **Cont (2001)** `[UNREAD]` — the stylized-facts reference. Aggregational Gaussianity (daily returns
  are materially more leptokurtic than weekly), volatility clustering, heavy tails. Settles §1.3's
  frequency trade-off on the specification side.

### The model's actual comparative advantage — persistence over a horizon

- **Ang & Bekaert (2002)** `[UNREAD]` — regime shifts used for allocation across horizons, not for
  one-step quantiles.
- **Guidolin & Timmermann (2007)** `[UNREAD]` — allocation under *multivariate* regime switching.
  Closest published shape to the mandate: multi-asset and multi-horizon.
- **Magdon-Ismail, Atiya, Pratap & Abu-Mostafa (2004)** `[UNREAD]` — maximum drawdown as a path
  functional. The object the mandate names and the battery does not measure.

### The model class and its specifications

- **Hamilton (1989)** `[read]`; Frühwirth-Schnatter (2006) `[skim]` — the class, and label switching.
- **Hamilton & Susmel (1994)** `[UNREAD]`; Gray (1996) `[UNREAD]` — regime switching with
  within-regime ARCH. **This is S3.** Cited here since before the ARCH-LM run.
- **Haas, Mittnik & Paolella (2004)** `[UNREAD]`; Klaassen (2002) `[UNREAD]` — Markov-switching
  GARCH done properly, and $t$ innovations inside regimes. S3 and S4 together.

### The evaluation battery — the part that is actually built

- Rosenblatt (1952) `[skim]`; Diebold, Gunther & Tay (1998) `[read]` — PIT, density evaluation.
- **Berkowitz (2001)** `[read]` — the §5.1 test.
- Kupiec (1995) `[read]`; **Christoffersen (1998)** `[read]` — coverage and independence.
- **Engle & Manganelli (2004)**, *CAViaR* `[UNREAD]` — the DQ test. Blocks §5.2 under §0.3.
- Christoffersen & Pelletier (2004) `[UNREAD]` — duration-based backtests.
- Koenker & Bassett (1978) `[skim]` — tick loss and quantile consistency.
- Acerbi & Székely (2014) `[UNREAD]`; **Fissler & Ziegel (2016)** `[UNREAD]`; Patton, Ziegel & Chen
  (2019) `[UNREAD]` — ES backtesting and joint elicitability. Verify sign conventions (§5.3).
- Diebold & Mariano (1995) `[read]`; **Giacomini & White (2006)** `[UNREAD]`; Clark & West (2007)
  `[UNREAD]` — forecast comparison.
- Andersen & Bollerslev (1998) `[skim]` — realized volatility; why daily beats weekly.
- Christensen & Prabhala (1998); Blair, Poon & Taylor (2001); Jiang & Tian (2005) — all `[UNREAD]`,
  the §5.5 literature.
