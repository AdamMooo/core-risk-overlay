# Point-in-Time Discipline

Last updated: 2026-08-17. **Binding on the active program.**

Standing rules for this repo. Companion to [[CHARTER]] and [[docs/RESEARCH-PROTOCOL]].

## The rule

> **Every input to a reported number must have been knowable at the time the number claims to
> describe — and every researcher choice must have been fixed before the result it selects among was
> seen.**

Two clauses, because the second is the one this program is exposed to. The first is classical
look-ahead: a quantity computed from the future. The second is **selection on outcome**: a threshold,
an offset, a parameter or a sample boundary chosen after seeing which value gives the answer. The
closed program's risk was almost entirely the first. **The active program's risk is almost entirely
the second**, because its interventions are fixed rules rather than filters, so there is no state to
leak — but there are many knobs, and one realized path to turn them against.

No exceptions, no "it's probably fine," no "the effect is small." A number that could not have been
produced without knowing the answer is not evidence; it is a description of history.

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

**Rows 1-8 were written for the closed prediction program.** Rows 1, 2, 4 and 5 concern a filter that
no longer runs in the active tree and are retained for provenance; 2b, 6, 7 and 8 are general data
discipline and still bind. Row 3 (signal/execution timing) is **N/A** in the active program, which has
no signal.

### Rows 9-13 — the active program's own channels

Added 2026-08-17 with the transition. **Every one is selection on outcome rather than classical
look-ahead, and none of them is caught by rows 1-8.** These are the channels that make the difference
between an experiment and a search.

| # | Channel | Status | Where | Fix |
|---|---|---|---|---|
| 9 | **Roll-phase selection.** Blocks walk a fixed calendar grid from index 0, so at 52 weeks the program makes 33 decisions in 33 years and the phase of every roll relative to the crisis is set by the sample's first date. Choosing the offset that maximises the effect is choosing the answer. | **OPEN** | `research/hedge_economics.py` `simulate` | E1 sweeps offsets `1..tau-1` and reports the **spread** as a `Psi` coordinate. No single phase may be quoted without it. |
| 10 | **Episode-threshold selection.** The depth `theta` defining "an excursion worth counting" is ours to pick, and it changes `n`. | **OPEN** | `research/pathfunctionals.py` `excursions` | `theta` is declared in the experiment's stub before the run, with a sensitivity band, not chosen from the result. |
| 11 | **CDaR `alpha` selection.** `alpha` interpolates from a well-sampled statistic to an n=1 one. Picking the `alpha` that gives the answer is the same defect one level up. | **OPEN** | `research/pathfunctionals.py` `cdar` | Report the **whole curve**, always. The `alpha` at which the estimate destabilises is an output, not a choice. |
| 12 | **Pricing-assumption selection.** `skewed_vol` scales skew as `sqrt(4/tenor)`, which makes long tenor cheap and **favours the conclusion**, and a flat 5% offer spread is applied at every tenor when long-dated puts are thinner. Sweeping and then quoting the favourable slope is selection. | **ACCEPTED and declared** | `research/hedge_economics.py` `skewed_vol` | Dominance must hold **across the whole sweep**, not at the primary slope. E5 can reject the shape; it cannot confirm historical costs, because the chain archive begins 2026-08-14. |
| 13 | **Monetisation fitted to the path.** A rule `rho` that references the realized trough is clairvoyant, and it will look excellent. | **LATENT** — no rule exists yet, and the first one written is where this bites | E6 | `rho` is causal: it may use only information available at the decision date. The clairvoyant version is computed **separately and labelled as a bound**, never as a policy. |

**Row 13 has a precedent worth naming.** The closed program's own EVPI construction is exactly the
honest form of this: `simulate(foresight=True)` looks at the expiry price before buying, is documented
as not implementable, and exists only to bound others. Any monetisation work follows that pattern.

## Pre-flight checklist

Run this before any number is quoted, written down, or acted on:

- [ ] Every input was knowable at the time the number claims to describe
- [ ] **Roll phase was swept, not chosen**, and its spread is reported alongside the estimate
- [ ] **Episode threshold and CDaR `alpha` were declared in the stub**, before the result was seen
- [ ] The pricing sweep was reported **whole**, not at its most favourable slope
- [ ] Any monetisation rule uses only information available at its decision date
- [ ] The claim tuple and the **effective n per coordinate** are attached
- [ ] No magnitude is asserted from a population that is not identified
- [ ] Someone asked out loud: *"is this too good?"*

## The smell test

**If a backtest looks excellent on the first run, assume leakage until proven otherwise.**

**Tells specific to the active program.** There is no filter to leak, so watch the knobs instead:

- **A result that is stable in its central estimate and unreported in its spread.** If an effect
  survives one roll phase and the other 51 were never run, the spread *is* the result.
- **A statistic whose effective n was never stated.** Max drawdown on this sample is one episode. Any
  ranking on it is a ranking of how one crisis happened to align with one calendar.
- **A monetisation rule that performs beautifully.** Selling near the trough is trivially optimal in
  hindsight and impossible in advance. If `rho` looks excellent, check what date it references.
- **A pricing assumption quoted at its primary value.** The skew sweep exists because the shape is
  unknown; reporting the slope that flatters the conclusion is the same defect as picking a threshold.

**The honest form is already in the repo and should be copied.** `simulate(foresight=True)` peeks at
expiry before buying, says so in its own docstring, and exists solely to bound what any rule could
achieve. A clairvoyant quantity that is *labelled* as a bound is one of the most useful things here.
The same quantity presented as a strategy would be the worst.
