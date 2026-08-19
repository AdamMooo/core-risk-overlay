# Point-in-Time Discipline

Last updated: 2026-08-18. **Binding on the active program.**

Standing rules for this repo. Companion to [[CHARTER]] and [[docs/RESEARCH-PROTOCOL]].

## The rule

> **Every input to a reported number must have been knowable at the time the number claims to
> describe — and every researcher choice must have been fixed before the result it selects among was
> seen.**

Two clauses, because both bind the return-state program and they bind for different reasons. The
first is classical look-ahead: a quantity computed from the future. The second is **selection on
outcome**: a threshold, an offset, a parameter or a sample boundary chosen after seeing which value
gives the answer.

**The return-state program is exposed to both, and this is a change from either closed program.** It
is exposed to the first because a latent state estimated on the whole sample is a smoothed state, and
question (D) is precisely whether `S_t` is measurable with respect to `I_t` — so rows 1 and 2 below
stop being provenance and become live again. It is exposed to the second because the number of
representations, state counts, horizons and functionals available is large and there is one realized
path to try them against. **The charter's answer to the second is structural: the null and the
frequency were fixed before the first experiment ([[CHARTER]] D1, D2) and are not revisited after a
result exists.**

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

**Rows 1-8 were written for the closed prediction program, and 2026-08-18 changes their status.**
Rows 1, 2, 4 and 5 concern a filter that no longer runs in the active tree — but they describe leaks
that any latent-state estimator reintroduces, so they are **retained as live design constraints for
the return-state program**, not merely as provenance. **Row 1 in particular is the one to read
before writing anything:** the smoothed state conditions each observation on the whole sample, the
filtered state does not, and the two disagreed about the 0.5 threshold in 9.7% of real weeks. Rows
2b, 6, 7 and 8 are general data discipline and still bind; row 8 (survivorship) becomes live the
moment the program goes multi-market, which [[CHARTER]] S2 requires. Row 3 is **N/A** — there is no
signal and no live path.

### Rows 9-13 — the CLOSED intervention program's channels

Added 2026-08-17 and **closed 2026-08-18 with the program that owned them.** Every one is selection on
outcome rather than classical look-ahead, and they are retained because the *class* of defect is
exactly what the return-state program must guard against with different knobs. Rows 10 and 11 —
choosing an episode threshold or a CDaR `alpha` after seeing the result — remain live in form the
moment drawdown geometry is used as a state characteristic, and `src/pathfunctionals.py` is still the
place they would bite.

**The return-state program's own channels are not enumerated here yet.** They are added with the
first experiment that creates them, under the same rule as the mathematics: written when needed, not
in advance.

| # | Channel | Status | Where | Fix |
|---|---|---|---|---|
| 9 | **Roll-phase selection.** Blocks walk a fixed calendar grid from index 0, so at 52 weeks the program makes 33 decisions in 33 years and the phase of every roll relative to the crisis is set by the sample's first date. Choosing the offset that maximises the effect is choosing the answer. | **OPEN** | `closed-research/intervention/hedge_economics.py` `simulate` | E1 sweeps offsets `1..tau-1` and reports the **spread** as a `Psi` coordinate. No single phase may be quoted without it. |
| 10 | **Episode-threshold selection.** The depth `theta` defining "an excursion worth counting" is ours to pick, and it changes `n`. | **OPEN** | `src/pathfunctionals.py` `excursions` | `theta` is declared in the experiment's stub before the run, with a sensitivity band, not chosen from the result. |
| 11 | **CDaR `alpha` selection.** `alpha` interpolates from a well-sampled statistic to an n=1 one. Picking the `alpha` that gives the answer is the same defect one level up. | **OPEN** | `src/pathfunctionals.py` `cdar` | Report the **whole curve**, always. The `alpha` at which the estimate destabilises is an output, not a choice. |
| 12 | **Pricing-assumption selection.** `skewed_vol` scales skew as `sqrt(4/tenor)`, which makes long tenor cheap and **favours the conclusion**, and a flat 5% offer spread is applied at every tenor when long-dated puts are thinner. Sweeping and then quoting the favourable slope is selection. | **ACCEPTED and declared** | `closed-research/intervention/hedge_economics.py` `skewed_vol` | Dominance must hold **across the whole sweep**, not at the primary slope. E5 can reject the shape; it cannot confirm historical costs, because the chain archive begins 2026-08-14. |
| 13 | **Monetisation fitted to the path.** A rule `rho` that references the realized trough is clairvoyant, and it will look excellent. | **LATENT** — no rule exists yet, and the first one written is where this bites | E6 | `rho` is causal: it may use only information available at the decision date. The clairvoyant version is computed **separately and labelled as a bound**, never as a policy. |

**Row 13 has a precedent worth naming.** The closed program's own EVPI construction is exactly the
honest form of this: `simulate(foresight=True)` looks at the expiry price before buying, is documented
as not implementable, and exists only to bound others. Any monetisation work follows that pattern.

## Pre-flight checklist

Run this before any number is quoted or written down. **Rewritten 2026-08-18 for the return-state
program**; the intervention program's version is preserved in git history and its four middle rows
are the ones that changed.

- [ ] Every input was knowable at the time the number claims to describe
- [ ] **The state at `t` was estimated from data up to `t`**, filtered and not smoothed, with vintage
      parameters — or the number is explicitly labelled as an in-sample description
- [ ] **The null and the frequency are the charter's**, not ones chosen for this result
- [ ] **Every researcher choice — state count, horizon, functional, window, sample boundary — was
      declared in the stub** before the result was seen
- [ ] The comparison is one the hypothesis could have LOST
- [ ] The claim tuple and the **effective n per coordinate** are attached
- [ ] No magnitude is asserted from a population that is not identified
- [ ] The state is named for what distinguishes it, not for what one would do about it
- [ ] Someone asked out loud: *"is this too good?"*

## The smell test

**If a backtest looks excellent on the first run, assume leakage until proven otherwise.**

**Tells specific to the return-state program.** There is a filter to leak again *and* many knobs, so
watch both:

- **A state that separates the return distribution beautifully.** Check first whether it was estimated
  with information the observer had. A smoothed state is a description of history, and it will look
  excellent.
- **A statistic whose effective n was never stated.** The characteristics most likely to distinguish
  states — tails, downside concentration, drawdown geometry — have effective n ~ 10-15 in all of SPY
  history. A clean separation on those is a statement about a handful of episodes.
- **A representation that arrived after a negative result.** If the state structure appeared only
  after the model class changed, the model class is the finding, and it is a finding about the
  representation rather than about the market ([[docs/RESEARCH-PROTOCOL]] P8).
- **A difference reported without what it is a difference from.** A conditional distribution that
  varies is not evidence of a state; it is what every conditional-variance process does
  ([[CHARTER]] §2).
- **A state that turns out to be measurable only in hindsight.** That is not a leak if it is *labelled*
  — it is charter outcome S4, which is a legitimate ending. It is a leak the moment it is quoted as
  though the observer had it.

**The honest form is already in the repo and should be copied.** The closed program's
`simulate(foresight=True)` peeks at the future before deciding, says so in its own docstring, and
exists solely to bound what any rule could achieve. **A clairvoyant quantity that is labelled as a
bound is one of the most useful things here. The same quantity presented as a capability would be the
worst.**
