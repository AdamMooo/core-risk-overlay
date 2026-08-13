# Core-Risk-Overlay

Last updated: 2026-08-12

A systematic tail-risk hedge for a permanently long, globally diversified equity book.

---

## 1. The mandate

The portfolio is long equities and stays long: SPY, QQQ, international developed and emerging —
effectively an XEQT / VT exposure. Nothing here ever recommends selling the core.

The overlay's job is to answer one question each week:

> **Is there a real, systemic threat to a long global equity book right now — large enough that
> paying for a hedge is worth it?**

Three things a good answer buys:

1. **Smooth the ride** — reduce the volatility of the experience, not just the statistics.
2. **Reduce drawdowns** — cap the depth of the bad periods.
3. **Stay invested** — the hedge is funded by a small sleeve, so core exposure is only marginally
   reduced. If a crash comes, the hedge is monetized and recycled into the core at lower prices. If
   it doesn't, the cost is the premium and the core keeps compounding.

**Systemic is the operative word.** SPY wobbling alone is noise. SPY, QQQ and international falling
together is the event worth insuring. Measured on our own data, those markets correlate 0.77–0.87
with SPY weekly, and it is precisely that joint behaviour the signal should be reading.

**The measure is continuous; the action is rare.** The underlying exposure estimate should move
smoothly, but it should cross into "act" infrequently — an expected **1-4 times per year, possibly
less**. Those are not in tension: a continuous measure with a high, sustained threshold. Discrete
on/off tiering of the *measure* was a first-pass simplification and is not justified.

---

## 1a. This is risk management, not alpha — which is why it can work

The model does **not** try to predict crashes, and it does **not** try to out-price the option
market. Both were considered and rejected:

- **Predicting drawdowns** is untrainable here. There are perhaps 10-15 systemic drawdowns in the
  entire SPY history, heavily overlapping. No model learns a rare, path-dependent label from ~12
  examples.
- **Trading mispriced insurance** requires a fair-value model better than the market's. Ours rejects
  ARCH-LM at 55.6 (p = 2.4e-11) — it is demonstrably misspecified, so any gap between its forecast
  and VIX is more likely our error than the market's. VIX is a clearing price set by participants
  with better models and capital at risk. Claiming edge over it is an extraordinary claim with no
  evidence behind it.

**The framing that survives is risk management.** Buying *fairly priced* insurance is not a losing
trade — fire insurance has negative expected value and is entirely rational, because it truncates a
tail you cannot afford. The question is not "is this cheap" but "how exposed am I right now, and is
paying the fair price worth it."

This works here for a specific structural reason: **the core is never sold.** Given that
pre-commitment, options are the only available lever, so the comparison is not "puts versus cash"
but "puts versus bearing the entire drawdown." That is a far lower bar than beating the option
market.

**And risk management is alpha, arithmetically.** Compounding is path-dependent: a -50% drawdown
requires +100% to recover. Truncating the left tail raises the *geometric* return even when the
hedge has negative expected value, provided the premium drag is smaller than the drawdown avoided.
The edge comes from reshaping the distribution, not from forecasting it.

**Therefore the success metric is compound growth rate and drawdown depth, hedged versus unhedged,
net of all premium and costs.** Not signal accuracy, not crisis-detection hit rate, not forecast
error. Those were metrics invented after the fact; this one follows from the mandate.

**Scope boundary.** The model answers *when*. It never decides *what* to buy or *how much*.
Instrument choice, strike, tenor and sizing are separate decisions made outside it.

---

## 1b. The research question, and what would answer it

> **How well does a Markov-switching jump model with Hamilton filtering provide information about
> Value at Risk and the risk of equity assets?**

That is the question. It is stated absolutely, not comparatively, and it is answerable without any
benchmark at all.

### Test 1 — calibration. Primary, absolute, no benchmark required.

Express the output as a conditional **Value at Risk / Expected Shortfall** at a stated horizon and
confidence level. That is the standard object in the risk-management literature and it carries
standard backtests:

- **Kupiec (1995) unconditional coverage** — do exceedances occur at the stated rate?
- **Christoffersen (1998) independence and conditional coverage** — are exceedances independent, or
  do they cluster?

**The independence test is the discriminating one, and it is why no benchmark is needed.** A
constant, unconditional VaR passes Kupiec trivially: set it at the historical 5th percentile and
roughly 5% of observations breach it by construction. But if volatility clusters, its breaches
*bunch together* and the independence test rejects. So "does conditioning on a latent regime state
actually add anything?" is answered inside the absolute test.

Scored on **every observation**, not on a handful of crisis episodes. That is what makes this
settleable rather than arguable, and it is the whole reason this framing is preferred to forecasting
drawdowns directly.

### Benchmark ladder — context, not gates

Each rung answers a different question. The research question lives in the top two.

| benchmark | question it answers |
|---|---|
| none — coverage tests alone | is the stated risk level honest? |
| unconditional / constant VaR | does conditioning help at all? |
| trailing realized volatility | does the *model* beat naive conditioning? |
| implied volatility (VIX) | does it beat the free market price? |

### Test 2 — incremental information over VIX. The system's gate, not the paper's bar.

The **forecast encompassing regression**:

$$RV_{t,t+h} \;=\; a \;+\; b\,\mathrm{IV}_t \;+\; c\,X_t \;+\; \varepsilon_t$$

with $RV$ realized (downside) risk over the horizon, $\mathrm{IV}$ implied volatility, and $X$ the
model's measure. Newey-West standard errors are mandatory, not optional: overlapping $h$-period
horizons make the errors autocorrelated by construction, so ordinary OLS standard errors overstate
significance.

If $c$ is not significant, the model tells you nothing the option market has not already priced —
and since VIX is free and requires no model, **capital should not be committed.** That is a decision
rule, not a verdict on the research: most published volatility models do not cleanly beat implied
volatility, and the question of whether model-based measures carry incremental information is
long-running and unsettled (Christensen & Prabhala; Blair, Poon & Taylor; Jiang & Tian). A paper
does not become uninteresting for landing on $c \approx 0$.

Competing specifications — the regime model, GARCH-family variants, or both — are simply different
$X$ in this same regression. **GARCH is a candidate for the slot, never a benchmark to beat.** If a
GARCH measure turns out more informative, that is a result to adopt, not a defeat.

### Test 3 — economic value. Gated.

Compound growth rate and maximum drawdown of the hedged book against unhedged, net of all premium,
spread and conversion costs. Does not run unless Test 1 passes and Test 2 clears the VIX gate.
Apparent economic value from an uncalibrated signal is a small-sample artifact.

### Filtered versus smoothed is itself a result

Any VaR built on Kim-smoothed probabilities is evaluated against data it has already seen — it will
look excellent and be worthless. The real-time measure must be filtered. But reporting **both** —
filtered for live VaR, smoothed for retrospective regime dating — quantifies how much apparent skill
in naive regime-switching risk studies is hindsight. On this data the two disagree about the 0.5
threshold in **9.7%** of weeks. That gap is a finding, not a footnote.

### Deliberately not used

Crisis-detection hit rate, lead time versus other signals, and accuracy on hand-selected episodes.
All three were invented during the 2026-08-12 review after seeing the data, and all three select
their own test bed from hindsight.
---

## 2. What is settled, and what is not

The first version of this file declared a list of "immutable constraints." Most of them were
first-pass guesses made before any data was examined, and several were later contradicted by that
data while continuing to constrain the work. Nothing below is immutable. Each item carries its
status.

**Settled by evidence:**

- **Daily data, weekly decisions — these are separate choices.** Earlier versions of this file fused
  them into a single "weekly cadence" constraint, which was a mistake. Estimation should use daily
  closes: ~8,400 observations instead of 1,750 for SPY, a 10-year minimum history that is 2,500
  observations rather than 520, materially less lag (a weekly bar can conceal four days of
  deterioration — in March 2020 that is the entire event), and volatility estimated from
  higher-frequency data is substantially more accurate, which is among the most robust results in
  the literature (Andersen-Bollerslev, realized volatility). The *decision* stays weekly or
  event-driven, because the target is 1-4 actions per year, not 250. Estimate fast, act slow — that
  is what a filter is for, and the two frequencies were only coupled by accident. Intraday tick data
  and high-frequency point processes (Hawkes and similar) remain out of scope; daily closes are not
  that, and the original ban was over-applied.
- **Filtered, never smoothed.** Any state estimate must condition only on data available at the
  time. `statsmodels`' `smoothed_marginal_probabilities` runs the Kim smoother over the whole
  sample including the future, and was doing exactly that here until 2026-08-12. See
  `docs/POINT-IN-TIME-DISCIPLINE.md`.
- **Ten-year minimum history.** Below ~520 weekly observations the current model produces degenerate
  parameters and unstable regime labelling. Measured, not assumed.
- **Post-hoc regime relabelling.** Regime indices are not identified by the likelihood; the label
  flips across refits on real data. Any hardcoded index inverts the signal.

**Open — previously written here as settled, and wrongly:**

- **Number of regimes.** Corrected AIC *and* BIC both prefer **k=3** over k=2, decisively
  (dAIC +66, dBIC +44) and on real data. This file previously mandated two regimes; that mandate was
  a first-pass choice, not a result.
- **Whether a discrete-regime model is the right class at all.** ARCH-LM on standardized residuals
  rejects at 55.6 (p = 2.4e-11) *after* regime-switching, i.e. volatility keeps moving continuously
  within regimes. A near-binary state probability is also a poor fit for the continuous hedge ratio
  described in section 1.
- **How to measure exposure.** *Settled in framing, open in specification.* The model should
  estimate current conditional **tail exposure**, not forecast crashes. But conditional variance —
  what it estimates today — is symmetric, and symmetry is not what hurts a long book: the model
  scores a violent rally as high as an equal crash (up/down ratio **1.0000** at |return| ≥ 7%).
  Downside semivariance, conditional VaR and expected shortfall all measure the thing that actually
  matters and are equally estimable from daily data. Which one is unresolved.
- **What role VIX plays.** *Settled in principle:* it is the **price** side — what acting costs —
  not a benchmark to beat. Needed to answer "is paying for this worth it," never "am I smarter than
  the option market." It is loaded in `data_loader.py` and used by nothing.
- **Whether to model a single asset.** Systemic risk is a joint phenomenon; the current model sees
  only SPY.

Machine-learning clustering and rigid binary classifiers remain out of scope — a preference for
interpretable likelihood-based models, stated as a preference rather than a law.

---

## 3. Capital plumbing (the Canadian framework)

Two sub-accounts, to avoid ongoing currency friction:

1. **Core bucket (CAD).** Long-term compounding index assets (VFV, XEQT) or direct blue chips. Never
   sold during a crash.
2. **Hedge bucket (USD).** A small dedicated cash sleeve. CAD is converted to USD **once**, via
   Norbert's Gambit or IBKR's native conversion, to eliminate repeated spread costs. That USD buys
   liquid US-listed SPY puts.

When a hedge pays off: sell the inflated puts, move the proceeds into the core bucket, and buy more
index exposure at the discount. If markets recover instead, the core was never sold.

---

## 4. Implementation status

| component | state |
|---|---|
| `src/data_loader.py` | working — weekly returns and VIX, start-date invariant, validated |
| `src/jump_model.py` | working — 2-regime switching mean/variance, filtered output, no look-ahead |
| `src/risk_engine.py` | **stub** |
| `main.py` | **stub** |
| `checks.py` | 29 checks, all passing |
| `walkforward.py` | walk-forward correctness harness |
| `diagnostics.py` | statistical battery (has a known QQ standardization bug) |

The model has never been run in the mode it exists for: there is no live weekly path. Sizing and
tiering logic is deliberately unwritten, because the open questions in section 2 determine what
shape it should take.

Current state, evidence and open decisions live in `core-risk-overlay.md`. The mathematics is in
`docs/MATH-REFERENCE.md`.
