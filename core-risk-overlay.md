---
type: project
---

# Core-Risk-Overlay

Last updated: 2026-08-12

Tail-risk hedge overlay for a permanently long global equity book. Mandate in [[README]]. Protocol in
[[docs/RESEARCH-PROTOCOL]]. Mathematics in [[docs/MATH-REFERENCE]]. Time-basis rules in
[[docs/POINT-IN-TIME-DISCIPLINE]].

## Status

**Framing settled, naming corrected, evaluation half-built. The model is a candidate under test, not
a thing being defended.**

The question is fixed and absolute ([[README]] §3): *how well does a Markov-switching model provide
real-time information about Value at Risk and the tail risk of equity assets?* Scored on every
observation, no benchmark required. **Real-time** excludes smoothed probabilities by definition.

[[docs/RESEARCH-PROTOCOL]] is preregistered — estimand, tests, reliability battery, decision
thresholds, build order. `src/evaluation.py` scores whatever it is handed and knows nothing about
which model produced it, which is what turns the specification argument into an experiment.

## Target

> Each week: is there a real, **systemic** threat to a long global equity book, large enough that
> paying for a hedge is worth it?

The book is permanently long SPY / QQQ / international and is never sold. The hedge is a small USD
sleeve buying SPY puts, monetized in a crash and recycled into the core at lower prices. Goals:
smooth the ride, cut drawdown depth, stay invested.

Two properties this implies that the current model lacks:

- **Systemic, not single-asset.** SPY alone wobbling is noise; SPY + QQQ + international falling
  together is the event. Those correlate 0.77-0.87 weekly.
- **Continuous, not a switch.** A 2-state model is near-binary by construction — the top-20
  probability weeks all sit at P ≥ 0.99999.

## Open questions

Positions stated, not hedged. None is a tuning question.

1. **Is the target variable right?** *Probably not.* The model estimates the latent state of return
   *variance*; the mandate is about forward *drawdown* over weeks to months. These diverge badly —
   2022 was -24% over 39 weeks at unremarkable weekly volatility, while a single -8% week that
   recovers is high-variance and harmless. Subsumes most of the others. The protocol's answer is to
   score the predictive density directly rather than argue about the target.
2. **Is a discrete-regime model the right class?** *Not alone.* ARCH-LM on standardized residuals
   rejects at 55.6 (p = 2.4e-11) *after* regime-switching — volatility keeps moving within regimes.
   MS(2) has exactly two possible conditional variances, and at daily frequency that binds harder.
   Within-regime ARCH and Student-$t$ regime densities are S3/S4 in the protocol.
3. **How many regimes?** Corrected AIC *and* BIC both prefer **k=3** decisively (ΔAIC 66, ΔBIC 44) on
   real data. k=2 persisted only because [[README]] said so. But k=3 does not fix question 2.
4. **Returns only?** *No.* VIX is free, forward-looking, aligns 1750/1750 weeks. It is the **price**
   side — what acting costs — not a benchmark to beat. Loaded in `data_loader.py`, used by nothing.
5. **Sign-blindness.** Not a bug to patch — it is what modelling variance *means*. Up/down probability
   ratio **1.0000** at |return| ≥ 7% with a common mean; **0.9279** with a switching mean. Follows
   from question 1, and it is why the regime is named `high_variance` rather than anything
   directional.

## Settled by evidence

- **Filtered, never smoothed.** Kim-smoothed probabilities condition on the entire sample including
  the future. Filtered and smoothed disagree at the 0.5 threshold in **9.7%** of real weeks. Guarded
  by two checks.
- **520-week (10-year) minimum history, weekly.** At 260 weeks, walk-forward fits produced degenerate
  parameters (`p[0->0]` to 0.163, `p[1->0]` pinned at 0.999999, a variance collapsing to zero), 6
  label flips across SPY and QQQ, 2-3% convergence failures. At 520: 1 flip, 0-1 failures, 7.3-7.8%
  revision, no degenerate values. **Does not transfer to daily by multiplying by 5** — must be
  re-measured.
- **Post-hoc relabelling is load-bearing.** The high-variance index flips across refits on real data —
  SPY at 2009-01-09, a genuine GFC transition. Any hardcoded index inverts the signal.
- **The data loader must resample daily onto a fixed weekly grid.** `yfinance`'s `interval="1wk"`
  anchors on each series' first observation: SPY from 1993 came back Monday-anchored, from 2010
  Friday-anchored, sharing zero bars. `start=None` silently returned a short window. Both fixed.
- **The 2006-2011 "persistence pathology"** the original constraints existed to prevent **does not
  occur.** The unconstrained high-variance regime is *less* persistent (17.2 vs 44.7 weeks). Those
  constraints were removed.
- **Mixture VaR and ES closed forms verified** against a 40M-draw Monte Carlo to ~1e-5. The
  moment-matched normal approximation errs by 11% of the VaR level at $w=[0.85,0.15]$ — it is wrong,
  not merely imprecise.

## Known defects

| what | where | severity |
|---|---|---|
| Density calibration, DQ, tick loss, ES bootstrap unbuilt | `src/evaluation.py` | blocks the primary test |
| No vintage-parameter VaR path — the only VaR available is full-sample fit | `walkforward.py` | nothing is reportable until this exists |
| Parameter look-ahead in the convenience path | `markov_switching.estimate_high_variance_probability` | documented in the docstring; walk-forward path is the honest one |
| ~7.5% of weeks have their state revised by later refits | model class | reliability number, protocol R4 |
| ~1-2% of refits fail to converge | `markov_switching.py` | policy fixed in protocol §4.5, not yet coded |
| Signal timing unresolved — no weekly close exists at Friday 3:30pm | operational | leak register #3 |
| Daily minimum history unmeasured | `RELIABLE_MIN_OBSERVATIONS` | blocks quoting any daily result |

## Working lesson from 2026-08-12

**Most of this repo was analysis apparatus built while the base was unsettled, and it did active harm
rather than merely wasting effort.** 2065 lines documenting a 2-regime model made k=2 feel decided
when the repo's own diagnostics said k=3. A 764-line diagnostics suite nobody had read produced
numbers that entered permanent documents as fact — including a QQ standardization bug found the first
time it was actually reviewed. That suite is deleted; the documents that cited its line numbers had to
be rewritten.

Two rules that came out of it:

- Sort findings into **deductive** (code does X, math implies Y — solid as stated) and **inductive**
  (this beat that on these episodes — needs a rule-based test bed and honest effective-n, which is
  episodes, not configuration rows). They were being quoted with equal confidence.
- **Fix the design and the kill thresholds before running.** That is now
  [[docs/RESEARCH-PROTOCOL]] §7.

A third, from the naming sweep: **a wrong name is a load-bearing defect.** `jump_model.py` implemented
a Markov-switching model while "statistical jump model" is an established name for a different method.
Every document inherited the confusion.

## Possible output: a paper

A **long-run** goal, not a near-term deliverable — but recording it disciplines the work rather than
adding to it. A paper audience will not accept metrics invented after seeing the data, hand-picked
crisis windows, or economic results without a calibration test. That is exactly the standard
[[docs/RESEARCH-PROTOCOL]] sets, and it is stricter than what this project was applying to itself.

The natural shape, if results support one: *does a conditional regime model carry information about
downside risk that is incremental to implied volatility?* Open in the literature, genuinely uncertain,
and a well-executed negative result is publishable and useful. It is also exactly the question that
decides whether this system should exist.

## First smoke reading — NOT a result

`src/predictive.py` landed 2026-08-12 and the full path runs. On weekly SPY (1,749 forecasts), fitted
**once on the whole sample**, so this carries parameter look-ahead and is not reportable — it is a
smoke test that the plumbing produces sane numbers:

| $\alpha$ | breach rate | Kupiec $p$ | independence $p$ |
|---|---|---|---|
| 0.10 | 0.1109 | 0.134 | 0.724 |
| 0.05 | 0.0555 | 0.303 | 0.782 |
| 0.01 | 0.0114 | 0.555 | **0.020** |

Regimes: high-variance $\sigma$ 3.84%/week, mean -0.26%, expected duration 12.9 weeks; calm $\sigma$
1.50%, mean +0.36%, 36.1 weeks.

**The pattern worth noting:** rates are right at every level, but at $\alpha=0.01$ the breaches
*cluster* — the independence test rejects while Kupiec passes comfortably. That is precisely the
failure Kupiec cannot see and the reason [[README]] §3 calls independence the discriminating test. It
is also what the ARCH-LM rejection predicts: two conditional variance values cannot track scale in
the far tail. Expect the honest walk-forward version to be worse, not better, since look-ahead
flatters.

## Next

Read [[README]] §§1-5 and [[docs/RESEARCH-PROTOCOL]] §§1, 5, 10 — short, and they contain the whole
framing. Then continue protocol §10 from step 2: the density-calibration battery
(PIT/Berkowitz, DQ, tick loss, ES bootstrap) in `src/evaluation.py`, each with a known-answer test
that must reject miscalibrated input.

Not planned: economic backtesting before the calibration tests pass, statistical jump models, intraday
data, Hawkes processes, K-means, binary classifiers.

## Open governance question

Not in [[INDEX]] nor the repo table in [[CLAUDE]], so charter status is undeclared. Related: the
`regime-detection` repo is **no longer on disk** — it is not under `systematic-investing-research/`
and the four governance docs [[CLAUDE]] says live in `regime-detection/governance/` are gone with it.
GitHub (`AdamMooo/regime-detection`, private) should still have them. A read-only assessment survives
at [[portfolio-sprint/assessments/regime-detection]].

## Related

- [[README]] · [[docs/RESEARCH-PROTOCOL]] · [[docs/MATH-REFERENCE]] · [[docs/POINT-IN-TIME-DISCIPLINE]]
- [[look-ahead-bias-is-self-concealing]] — vault lesson from this work
- [[INDEX|Home]]
