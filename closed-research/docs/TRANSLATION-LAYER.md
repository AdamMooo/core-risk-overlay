# Translation Layer — the width/direction separation

Last updated: 2026-08-14

**Binding architectural constraint.** Companion to `../README.md` §2 (scope boundary),
`RESEARCH-PROTOCOL.md` §0 (the experiment gate), `POINT-IN-TIME-DISCIPLINE.md` (time basis).

A note on naming, once: this repo calls the model a **Markov-switching model** and the Hamilton
filter the *algorithm* that produces its filtered state (`../README.md` §4). "Hamilton filter",
used elsewhere for the same object, maps onto `src/markov_switching.py` here. The distinction
matters only because the property that is load-bearing is **real-time filtering**, not the
particular recursion that delivers it.

---

## 1. What the model measures, and it is settled

The state characterisation (`../state_character.py`, 2026-08-14) established this empirically
rather than assuming it:

| evidence | SPY | QQQ |
|---|---|---|
| realized vol ratio wide/calm | 2.446, CI [1.823, 3.124] | 1.791, CI [1.316, 2.184] |
| drift difference, wide − calm | −0.24%/wk (Welch *t* −0.78) | **+0.46%/wk (Welch *t* +0.91)** |
| down/up ratio at \|r\| ≥ 3%, wide | 1.12 | **0.83** |

Volatility separates monotonically across probability bins, replicates across two assets, and is
stable across sample halves. **The drift difference reverses sign between assets and the tail ratio
straddles 1.0.**

```
Markov-switching state  ->  MARKET WIDTH (volatility environment)
Markov-switching state  ->  bullish / bearish signal          FORBIDDEN
```

**This is the intended result, not a shortfall.** The model estimates the latent state of return
*variance*. Variance is symmetric. A model of variance is blind to sign by construction, which is
why the regime is named `high_variance` and never "crisis", "panic" or "risk-off"
(`../README.md` §4). Measured directly: up/down probability ratio 1.0000 at |r| ≥ 7% with a common
mean, 0.9279 with a switching mean.

## 2. The layer contract

The market environment is at least two-dimensional. This repo measures one axis.

```
        MARKET ENVIRONMENT = (WIDTH, DIRECTION)

  width layer      Markov-switching model      BUILT and characterised
  direction layer  not built, not specified    EMPTY
  decision layer   gated on protocol 7 D5      EMPTY
```

| width | direction | environment |
|---|---|---|
| narrow | up | calm upside |
| narrow | down | calm downside |
| wide | up | volatile upside |
| wide | down | volatile downside |
| **uncertain** | any | insufficient regime confidence |

The width layer determines the **row only**. It has no access to the column and must never be
asked to supply one.

**`uncertain` is a measured state, not a safety valve.** The ambiguous band `P ∈ [0.20, 0.80)`
holds **17.6% of SPY weeks and 13.8% of QQQ weeks**, with a transition diagonal of 66.7% / 65.3%
and a median run of 3 / 2 weeks. It persists rather than being crossed. A layer that forces every
week into narrow-or-wide is discarding a sixth of its own observations, and the abstain branch has
real occupancy to fire on.

## 3. Forbidden in code

Each of these silently converts a width reading into a directional one:

```python
if hamilton_state == 1: bearish = True     # width is not direction
if wide_regime: short_market()             # width is not direction
if high_probability_state: go_to_cash()    # width is not direction
```

**The subtler one, which is not on anybody's list.** Sizing down on width *looks* like risk
management and is a directional inference whenever its justification is "wide means bad":

```python
if wide_regime: position_size *= 0.5       # depends ENTIRELY on the stated reason
```

Legitimate only as **variance targeting** — holding portfolio variance constant when the variance
estimate rises — which is a claim about width and is supported. Illegitimate as "the wide state
predicts losses", which is a claim about direction and is refuted above. The two produce identical
code and different research obligations. **The reason must be written down next to the line.**

Also forbidden: hardcoding a regime index. Regime labels are not identified by the likelihood and
the high-variance index flips across refits on real data. Identification is post-hoc, by
`argmax` of fitted variances, every time.

## 4. Do not hard-code the −13%

The wide state occurs when the book is already **−13.08% (SPY) / −13.54% (QQQ)** below its running
peak at the median, with only 10.4% / 12.3% of wide weeks occurring at a peak.

**What this is:** an empirical characteristic, replicated to within 0.4pp across two assets, of
*when the measurement arrives*. It says a causal filter reports width after some of the move has
happened, which is what a causal filter is.

**What this is not:** a threshold, a trigger level, or a predictive drawdown estimate. It is a
median over overlapping episodes on a sample containing ~10-15 systemic drawdowns in total. Its
direction is partly mechanical — a wide state follows bad returns, and bad returns put a book below
its peak.

**The architectural consequence, which is the part that generalises.** The width reading carries a
timing property, and a consumer that reads only the width silently assumes the reading arrived at
the peak. Any interface this layer exposes must not hide that. This is a documentation obligation
on the contract, not a licence to build a lateness correction.

## 5. The open question, and the horizon that makes it answerable

> **Does this representation of width contain information beyond simpler volatility measurements?**

Status of each comparison, so none is re-run by accident:

| against | status |
|---|---|
| constant (expanding mean/sd) | **run.** Model wins tick loss, DM significant at 10% and 5%. Conditioning on *something* helps. |
| EWMA / RiskMetrics | **run at h=1 and VOID at h=1.** See below. |
| VIX, levels | **run. Null.** D3: c = +0.0009, p = 0.99; joint R² = VIX-alone to 4dp. |
| VIX, dynamics/persistence | **run. Null.** c = −0.0047, p = 0.63; X adds 0.0004 of R². |
| GARCH(1,1) | **never built.** Not implemented anywhere in this repo. |
| ATR / range-based (Parkinson, Garman-Klass, Rogers-Satchell, Yang-Zhang) | **never built.** Needs daily OHLC. |

**Why the EWMA comparison must not be re-run at h=1.** RiskMetrics EWMA is IGARCH: its multi-step
variance forecast is a martingale, `E[sigma2[t+h]] = sigma2[t+1]` for every `h`, so it **never
reverts**. A Markov-switching model reverts toward the stationary regime mix at a rate set by the
**second eigenvalue of P**. That is the entire structural difference between the two, and it is
**exactly zero one step ahead.** A null at h=1 is what theory predicts, not information about the
model. Protocol §0 rule 4 requires naming the horizon at which a difference becomes observable and
voids the comparison if it is invisible there.

**Consequence for the next experiment.** Any "beyond simpler measures" test must be run at
**h > 1**, and its §0 stub must state the horizon and the reverting-vs-martingale mechanism that
makes that horizon the discriminating one. GARCH(1,1) is the sharper opponent than EWMA, because
GARCH also reverts (toward unconditional variance, at rate `alpha + beta`), so the comparison is
between *two* reverting models and isolates whether **discrete regimes** specifically add anything
over smooth mean reversion. That is the question, stated properly.

**That stub is now written: `STUB-GARCH-ENCOMPASSING.md`, preregistered and blocked on a literature
gate.** It records that **h > 1 is necessary but not sufficient** — both models' *point* variance
forecasts share the functional form `long-run level + geometric^h × current deviation`, so the
discriminating functional is the **h-step density**, not the variance. Horizon `h=13` follows from
the chain's mixing time `1/(1-lam) ≈ 11.4` weeks.

**One result that constrains the whole family.** At α=0.01 every method breaches ~2x: MS 1.79%,
constant 1.87%, EWMA 0.97 2.03%, EWMA 0.94 2.36%. What they share is the Gaussian assumption. Tail
comparisons at h=1 therefore carry no information about regime structure — they measure a property
of the data common to all four.

## 6. What is not licensed by anything above

No rule, threshold, sizing, filter or trade. The decision layer is gated on protocol §7 D5 and D5
has never been evaluated. Q3 — is the width reading *incremental* to what a downstream consumer
already observes — is answered **no against VIX for single-asset SPY**, on both levels and
dynamics, for the structural reason that `F^returns ⊆ F^market`. The surviving direction is
**multi-asset**, where the information set genuinely differs.
