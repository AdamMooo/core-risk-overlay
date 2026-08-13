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

**The output should be continuous, not a switch.** A hedge ratio that moves smoothly from none to
meaningful. Discrete on/off tiering is a simplification that was never justified and probably does
not match the problem.

---

## 2. What is settled, and what is not

The first version of this file declared a list of "immutable constraints." Most of them were
first-pass guesses made before any data was examined, and several were later contradicted by that
data while continuing to constrain the work. Nothing below is immutable. Each item carries its
status.

**Settled by evidence:**

- **Weekly cadence.** Intraday and high-frequency point processes (Hawkes and similar) stay out of
  scope. This is a deliberate scope choice about the kind of risk being measured, not a finding.
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
- **Whether the target variable is right.** The model estimates the latent state of *weekly return
  variance*. The mandate is about *forward drawdown* over weeks to months. These diverge: 2022 was
  −24% over 39 weeks at unremarkable weekly volatility, while a single −8% week that recovers is
  high-variance and harmless. Variance is also symmetric by construction — the model scores a
  violent rally as high as an equal crash (up/down ratio **1.0000** at |return| ≥ 7%).
- **Whether to model returns alone.** VIX is a direct, free, forward-looking measure and predicts
  forward tail events better than the current model does (37.7% vs 26.8%). It is currently unused by
  anything in the pipeline.
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
