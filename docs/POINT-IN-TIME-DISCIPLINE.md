# Point-in-Time Discipline

Last updated: 2026-08-12

Standing rules for this repo. Companion to [[MATH-REFERENCE]] (§4.3 has the mechanism).

## The rule

> **Every input to the signal at week `t` must have been knowable at week `t`.**

No exceptions, no "it's probably fine," no "the effect is small." The overlay exists to tell us
what to do *next*, so any number that could not have been computed in real time is not evidence —
it is a description of history.

## Why this file exists

Look-ahead bias is the only bug class that **makes results look better**. Every ordinary bug
announces itself by making something fail. This one announces itself by making everything succeed:

- no exception, no warning, no NaN
- the model converges cleanly, `warnflag = 0`
- `checks.py` passes — it tests shape and reproducibility, never time-basis
- output is in `[0, 1]` and looks entirely plausible
- the equity curve looks *excellent*

Because it is self-concealing, it cannot be caught by ordinary code review or by unit tests. It has
to be enforced structurally, by working through the register below every time the pipeline changes.

The literature calls this **look-ahead bias** or **information leakage**; in ML, **data leakage** /
**train-test contamination**. The institutional countermeasure is **point-in-time (PIT) data
discipline**.

## Leak register

Status meanings: **OPEN** = present and unfixed. **LATENT** = not currently possible, but a
plausible next change introduces it. **ACCEPTED** = present, understood, judged tolerable.
**N/A** = structurally impossible today.

| # | Channel | Status | Where | Fix |
|---|---|---|---|---|
| 1 | **State inference uses the whole sample.** Kim smoother conditions each week on all data through `T`. | **CLOSED** 2026-08-12 | `src/markov_switching.py` | Fixed: returns `filtered_marginal_probabilities`. Guarded by two checks in `checks.py`. The two disagreed about the 0.5 threshold in 9.7% of real weeks. |
| 2 | **Parameter look-ahead.** Variances, mean, and transition probabilities are fitted once on the entire history, so even a *filtered* probability comes from a model tuned knowing the future. | **MEASURED, still open in the live path** | `walkforward.py` | `walkforward.py` refits quarterly on data `<= t` and shows the honest cost: **~7.5% of weeks have their state revised** by later refits, p95 revision 0.19-0.25. `markov_switching.estimate_high_variance_probability` fits once on the whole series and says so in its docstring; it is for correctness checks only. Protocol §4 makes vintage parameters mandatory for every reported number. |
| 2b | **Weekly grid depended on the download start date.** Not look-ahead, but the same class of silent input defect: `yfinance`'s `interval="1wk"` anchors bars on each series' first observation, so SPY from 1993 was Monday-anchored and from 2010 Friday-anchored, sharing zero bars. A live "fetch the last 5 years" would have sat on a different grid than the backtest. | **CLOSED** 2026-08-12 | `src/data_loader.py` | Fixed: download daily, resample to an explicit `W-FRI` grid. Verified start-invariant (max return diff 1.2e-06) and cross-ticker aligned. `start=None` also silently returned a short window; now defaulted and length-guarded. |
| 3 | **Signal/execution timing.** An earlier README specified running Friday 3:30pm EST on weekly closes. Friday's weekly close does not exist at 3:30pm Friday. | **OPEN** | no live path yet | Either generate the signal from Thursday's close, or keep the Friday-close signal and execute Monday. Pick one and write it down before `main.py` is built. |
| 4 | **`initialize_known` applies the transition matrix twice** (`Pi^2 q`, not `Pi q`). Invisible under the default steady-state init because `Pi pi = pi`, but a live trap the moment we hand the filter a known starting state. | **LATENT** | `markov_switching.py:120-122` (statsmodels; docstring does not match behaviour) | Do not use `initialize_known` when building the walk-forward loop for #2 without verifying the extra multiplication. |
| 5 | **Thresholds chosen on full history.** The 20% / 60% tier bands were set by inspection, never fitted. | **CLOSED** 2026-08-12 | — | `risk_engine.py` deleted and tiering removed from scope (protocol §9). Any future threshold must be calibrated on a training window only. |
| 6 | **`auto_adjust=True`** back-adjusts historical prices using split/dividend information known only later. | **ACCEPTED** | `src/data_loader.py` | Benign for log returns — it yields a consistent total-return series, and the adjustment is multiplicative so it cancels in `log(P_t / P_{t-1})` except across distribution dates. Documented rather than fixed. Revisit if we ever model price *levels* or strike distances. |
| 7 | **Full-sample scaling / standardization.** No scaler exists in the pipeline today. | **N/A** | — | If one is ever added, fit it on the training window only. |
| 8 | **Survivorship bias.** Single liquid ETF, no universe selection. | **N/A** | `src/data_loader.py` | Becomes live the moment this goes multi-asset or screens a universe. |

## Pre-flight checklist

Run this before any backtest number is quoted, written down, or acted on:

- [ ] Every probability in the signal path is **filtered**, never smoothed
- [ ] Parameters used at week `t` were fitted only on data up to and including `t`
- [ ] The bar that generated the signal had **closed** before the signal timestamp
- [ ] The execution price is timestamped at or after the signal
- [ ] No threshold, scaler, or hyperparameter was chosen using data after the decision date
- [ ] Someone asked out loud: *"is this too good?"*

## The smell test

**If a backtest looks excellent on the first run, assume leakage until proven otherwise.**

Strategy-specific tell: a risk measure that reliably rises *before* crashes rather than *during*
them is the signature of a smoother, not a forecast. Real-time regime detection is late and
hesitant by construction — the filter needs to actually observe bad returns before it can raise the
probability. A crisis indicator that anticipates crises has read the answer sheet.

Concrete illustration from the synthetic fixture in `checks.py`, week 99 — the last calm week
before the crash:

```
filtered  high-variance probability = 0.0059   <-  0.6%, what we could actually have known
smoothed  high-variance probability = 0.2008   <- 20.1%, after peeking at week 100
```

Same model, same week. The 34x gap is the Kim smoother's backward revision, and it grows as calm
persistence is pinned higher — see [[MATH-REFERENCE]] §4.3.
