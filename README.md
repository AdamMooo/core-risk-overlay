# Core-Risk-Overlay

Last updated: 2026-08-13

A systematic tail-risk hedge for a permanently long, globally diversified equity book — and a
research program testing whether the risk measure it needs can be built honestly.

- **The question and how it gets answered:** `docs/RESEARCH-PROTOCOL.md` (binding, preregistered)
- **Current state and next build:** `core-risk-overlay.md`
- **Mathematics:** `docs/MATH-REFERENCE.md` · **Time-basis rules:** `docs/POINT-IN-TIME-DISCIPLINE.md`

---

## 1. The mandate

The portfolio is long equities and stays long — SPY, QQQ, international developed and emerging,
effectively XEQT/VT. Nothing here ever recommends selling the core. The overlay answers one
question:

> **Is there a real, systemic threat to a long global equity book right now — large enough that
> paying for a hedge is worth it?**

**Systemic is the operative word.** SPY wobbling alone is noise. SPY, QQQ and international falling
together is the event worth insuring. Those markets correlate 0.77-0.87 with SPY weekly, and it is
that joint behaviour the signal should read.

**The measure is continuous; the action is rare.** A smoothly moving exposure estimate crossing a
high, sustained threshold an expected 1-4 times per year. Discrete on/off tiering of the *measure*
was a first-pass simplification and is not used.

Three things a good answer buys: smooth the ride, cap drawdown depth, stay invested — the hedge is
funded by a small sleeve, monetized in a crash and recycled into the core at lower prices.

## 2. Risk management, not alpha — which is why it can work

The model does **not** predict crashes and does **not** try to out-price the option market. Both
were considered and rejected:

- **Predicting drawdowns** is untrainable: ~10-15 systemic drawdowns in all of SPY history, heavily
  overlapping. No model learns a rare, path-dependent label from ~12 examples.
- **Trading mispriced insurance** needs a fair-value model better than the market's. Ours rejects
  ARCH-LM at 55.6 (p = 2.4e-11) — demonstrably misspecified, so any gap between its forecast and
  VIX is more likely our error than the market's.

**What survives is risk management.** Buying *fairly priced* insurance is not a losing trade — fire
insurance has negative expected value and is entirely rational, because it truncates a tail you
cannot afford. The question is not "is this cheap" but "how exposed am I right now."

This works for a structural reason: **the core is never sold.** Given that pre-commitment, options
are the only lever, so the comparison is not "puts versus cash" but "puts versus bearing the entire
drawdown" — a far lower bar than beating the option market.

And risk management is alpha, arithmetically. Compounding is path-dependent: -50% needs +100% to
recover. Truncating the left tail raises the *geometric* return even at negative expected value,
provided premium drag is smaller than the drawdown avoided. The edge is reshaping the distribution,
not forecasting it.

**Scope boundary.** The model answers *when*. It never decides *what* to buy or *how much*.

## 3. The research question

> **How well does a Markov-switching model provide real-time information about Value at Risk and
> the tail risk of equity assets?**

Stated absolutely, not comparatively, and answerable with no benchmark at all. **Real-time** is
load-bearing: it excludes Kim-smoothed probabilities by definition, and it is the property that
matters rather than the algorithm that delivers it — the Hamilton filter is *the* filter for this
model class, so naming it would add nothing and would not generalise across the specifications in
protocol §3. The full protocol —
estimand, tests, preregistered decision thresholds — is `docs/RESEARCH-PROTOCOL.md`. Why it is
shaped this way:

- **Absolute.** The model emits a predictive density. Density calibration (PIT / Berkowitz) and
  quantile coverage (Kupiec, Christoffersen, dynamic quantile) score it on *every observation*,
  against nothing but its own stated risk level. That is what makes it settleable rather than
  arguable.
- **The independence tests are the discriminating ones.** A constant, unconditional VaR passes
  Kupiec trivially — set it at the historical 5th percentile and ~5% of observations breach it by
  construction. But if volatility clusters, its breaches *bunch*, and the independence and dynamic
  quantile tests reject. So "does conditioning on a latent regime state add anything?" is answered
  inside the absolute test.
- **ES is the headline functional**, VaR the better-tested one. The mandate is about drawdown
  *depth*; VaR measures frequency, ES measures depth. Both are functionals of the same density.
- **Economic value is gated** and not designed. Apparent economic value from an uncalibrated signal
  is a small-sample artifact.
- **Filtered, never smoothed.** Any VaR built on Kim-smoothed probabilities is evaluated against
  data it has already seen. Reporting both quantifies how much apparent skill in naive
  regime-switching studies is hindsight — the two disagree at the 0.5 threshold in 9.7% of weeks.

A constant VaR and a trailing-realized-volatility VaR are computed as **context rungs**, not gates —
they say whether conditioning helps at all and whether the model beats naive conditioning. VIX is
the one real gate, and it is the *system's* gate rather than the paper's bar (protocol §7).

**Deliberately not used:** crisis-detection hit rate, lead time versus other signals, accuracy on
hand-selected episodes. All three were invented after seeing the data, and each selects its own test
bed from hindsight.

## 4. Naming

`src/jump_model.py` was renamed to `src/markov_switching.py` on 2026-08-12 because the name was
simply wrong. What the file implements is a **Markov-switching model** (Hamilton 1989): a latent
discrete state with a Markov transition matrix, estimated by maximum likelihood via the Hamilton
filter, yielding a predictive density.

"Statistical jump model" is the established name of a *different* method (Bemporad et al. 2018;
Nystrup et al. 2020-21) that minimizes a penalized loss over the state path by dynamic programming
and yields no density. Nothing in this repo implements it. The old name invited that confusion, so
it is gone.

The high-variance regime is called **`high_variance`**, never "jump", "panic" or "crisis". The label
is resolved by argmax of fitted regime variances and nothing makes it directional — it scores a
violent rally nearly as high as an equal crash. A directional name would overclaim.

## 5. Settled, and open

**Settled by evidence:**

- **Daily data, weekly decisions — separate choices.** Estimate on daily closes (~8,400 observations
  vs 1,750; materially less lag; volatility from higher-frequency data is substantially more
  accurate — Andersen-Bollerslev). *Decide* weekly, because the target is 1-4 actions per year.
  Estimate fast, act slow. Intraday tick data and Hawkes processes remain out of scope.
- **Filtered, never smoothed.** `statsmodels`' `smoothed_marginal_probabilities` runs the Kim
  smoother over the whole sample including the future.
- **Post-hoc regime relabelling is load-bearing.** Regime indices are not identified by the
  likelihood; the label flips across refits on real data. Any hardcoded index inverts the signal.
- **Ten-year (520-week) minimum history**, measured. **This is a weekly figure and does not transfer
  to daily by multiplying by 5** — it must be re-measured before any daily result is quoted.

**Open:**

- **Number of regimes.** Corrected AIC *and* BIC both prefer **k=3** over k=2 decisively (ΔAIC 66,
  ΔBIC 44) on real data. An earlier version of this file mandated k=2; that was a guess, not a
  result.
- **Whether a discrete-regime model is the right class.** ARCH-LM rejects at 55.6 (p = 2.4e-11)
  *after* regime-switching — volatility keeps moving continuously within regimes. Not because MS(2)
  has "only two conditional variances" — the mixture weight gives it a continuum. The binding limit
  is that **a finite Gaussian mixture is Gaussian in the far tail for any k and any weight**, so more
  regimes cannot fix a tail; only the regime density can (S4). At daily frequency returns are more
  leptokurtic still, so the handicap gets worse, not better.
- **Which functional.** Conditional variance is symmetric, and symmetry is not what hurts a long
  book (up/down probability ratio 1.0000 at |return| ≥ 7% with a common mean; 0.9279 with a
  switching mean). Downside semivariance, VaR and ES all measure the thing that matters.
- **Single asset.** Systemic risk is joint; the current model sees only SPY.
- **Detection lag.** A causal filter is late by construction — it must observe bad returns before it
  can raise the probability. For a put buyer that lag is transmitted through premium: by the time the
  measure fires, VIX has repriced. A preregistered threat to economic value (protocol §7), not to
  calibration.

**What VIX is for:** the **price** side — what acting costs — never a benchmark to beat. Loaded in
`data_loader.py` and currently used by nothing.

Machine-learning clustering and rigid binary classifiers are out of scope — a preference for
interpretable likelihood-based models, stated as a preference rather than a law.

## 6. Capital plumbing (Canadian framework)

Two sub-accounts, to avoid ongoing currency friction:

1. **Core bucket (CAD).** Long-term compounding index assets (VFV, XEQT) or direct blue chips.
   Never sold during a crash.
2. **Hedge bucket (USD).** A small dedicated cash sleeve. CAD converted to USD **once**, via
   Norbert's Gambit or IBKR native conversion, to eliminate repeated spread costs. That USD buys
   liquid US-listed SPY puts.

When a hedge pays off: sell the inflated puts, move proceeds to the core bucket, buy index exposure
at the discount. If markets recover instead, the core was never sold.

## 7. Implementation status

| component | state |
|---|---|
| `src/data_loader.py` | working — weekly returns and VIX, start-date invariant, validated |
| `src/markov_switching.py` | working — 2-regime switching mean/variance, filtered, no look-ahead |
| `src/evaluation.py` | working — coverage tests, forward-aligned targets, Newey-West encompassing |
| `src/predictive.py` | working — mixture predictive density, VaR by Brent, closed-form ES |
| `checks.py` | 64 checks, all passing |
| `walkforward.py` | walk-forward correctness harness (weekly; vintage parameters) |
| `main.py` | placeholder — no live path until the preregistered gates D1-D3 clear |

The model has never been run in the mode it exists for. Sizing and threshold logic is deliberately
unwritten because the open questions above determine its shape.
