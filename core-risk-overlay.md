---
type: project
---

# Core-Risk-Overlay

Last updated: 2026-08-12

Tail-risk hedge overlay for a permanently long global equity book. Mandate and open questions in
[[README]]. Mathematics in [[docs/MATH-REFERENCE]]. Time-basis rules in
[[docs/POINT-IN-TIME-DISCIPLINE]].

## Status

**Pre-implementation. The model's form is under review, not its parameters.**

A 2-regime Markov-switching model on weekly SPY returns exists and works: no look-ahead, valid
inference, documented minimum history. But it was inherited from a Copilot scaffold and never chosen
against a stated target — the target was only written down on 2026-08-12. Now that it exists, four
concrete mismatches between form and target are visible (see Open Questions). `risk_engine.py` and
`main.py` remain stubs, deliberately: their shape depends on those answers.

## The target — stated 2026-08-12

> Each week: is there a real, **systemic** threat to a long global equity book, large enough that
> paying for a hedge is worth it?

The book is permanently long SPY / QQQ / international (XEQT- or VT-like) and is never sold. The
hedge is a small USD sleeve buying SPY puts, monetized in a crash and recycled into the core at
lower prices. Goals: smooth the ride, cut drawdown depth, stay invested.

Two properties this implies, neither of which the current model has:

- **Systemic, not single-asset.** SPY alone wobbling is noise; SPY + QQQ + international falling
  together is the event. Those correlate 0.77-0.87 weekly, and that joint behaviour is the signal.
- **Continuous, not a switch.** A hedge ratio that moves smoothly from none to meaningful. A 2-state
  HMM is near-binary by construction — the top-20 probability weeks all sit at P >= 0.99999.

## Open questions — the real ones

Positions stated, not hedged. None of these is a tuning question.

1. **Is the target variable right?** *No, probably not.* The model estimates the latent state of
   weekly return *variance*; the mandate is about forward *drawdown* over weeks to months. These
   diverge badly — 2022 was -24% over 39 weeks at unremarkable weekly volatility, while a single
   -8% week that recovers is high-variance and harmless. This question subsumes most of the others.
2. **Is a discrete-regime model the right class?** *Probably not alone.* ARCH-LM on standardized
   residuals rejects at 55.6 (p = 2.4e-11) *after* regime-switching — volatility keeps moving within
   regimes. And near-binary output contradicts the continuous hedge ratio the mandate wants.
   Asymmetric GARCH (GJR-GARCH / EGARCH) matches the target far better: continuous, and asymmetric
   in the right direction by construction. **Untested here — the claim that it forecasts drawdowns
   better is unverified.**
3. **How many regimes?** Corrected AIC *and* BIC both prefer **k=3** decisively (dAIC +66, dBIC +44)
   on real data. We stayed at k=2 because [[README]] said so. But k=3 does not fix question 2, so
   this is likely the wrong axis to move on.
4. **Model returns only?** *No.* VIX is free, forward-looking, aligns 1750/1750 weeks, and predicts
   forward tail events better than the current model (37.7% vs 26.8% for a sub -5% week within 13).
   It is loaded in `data_loader.py` and used by nothing.
5. **Sign-blindness.** Not a bug to patch — it is what modelling variance *means*. Up/down
   probability ratio is **1.0000** at |return| >= 7%; adding a switching mean moved it only to
   0.9279. Follows directly from question 1.

## Settled by evidence

- **Filtered, never smoothed.** Smoothed (Kim) probabilities condition on the entire sample
  including the future. Filtered and smoothed disagree about the 0.5 threshold in **9.7%** of real
  weeks. Guarded in `checks.py`.
- **520-week (10-year) minimum history.** At a 260-week minimum, walk-forward fits produced
  degenerate parameters (`p[0->0]` to 0.163, `p[1->0]` pinned at 0.999999, a variance collapsing to
  zero), 6 regime-label flips across SPY and QQQ, 2-3% convergence failures and 9.5-16.5% tier
  revision. At 520 weeks: 1 flip, 0-1 failures, 7.3-7.8% revision, no degenerate values.
  `jump_model.RELIABLE_MIN_OBSERVATIONS`.
- **Post-hoc relabelling is load-bearing.** The jump-regime index flips across refits on real data —
  SPY at 2009-01-09, a genuine GFC transition. Any hardcoded index inverts the signal. Never remove.
- **The data loader must resample daily to a fixed weekly grid.** `yfinance`'s `interval="1wk"`
  anchors on each series' first observation: SPY from 1993 came back Monday-anchored, from 2010
  Friday-anchored, sharing zero bars. `start=None` silently returns a short window. Both fixed and
  guarded.
- **The 2006-2011 "persistence pathology"** that the original constraints existed to prevent **does
  not occur.** The unconstrained crisis regime is *less* persistent (17.2 vs 44.7 weeks). Those
  constraints were removed.

## Known defects

| what | where | severity |
|---|---|---|
| `risk_engine.py`, `main.py` are stubs — no live path exists | those files | blocks everything |
| QQ table compares unstandardized values to N(0,1) quantiles | `diagnostics.py` | reported numbers were partly a scale artifact |
| Crisis windows hand-typed from hindsight | `diagnostics.py` | biased test bed |
| ~7.5% of weeks have their tier revised by later refits | model class | tiering logic must absorb it |
| ~1-2% of refits fail to converge, no policy | `jump_model.py` | live operation undefined |
| Signal timing: README says Friday 3:30pm on weekly closes that don't exist yet | operational | unresolved |

## Working lesson from 2026-08-12

**4599 lines in this repo; 665 are the base (`data_loader`, `jump_model`, `checks`) and 49 are the
deliverable, both stubs.** The rest is analysis apparatus built while the base was unsettled. That
apparatus did active harm, not just wasted effort: 2065 lines documenting a 2-regime model made
k=2 feel decided when the repo's own diagnostics said k=3, and a 764-line diagnostics suite nobody
had read produced numbers that went into permanent documents as fact — including a QQ bug found the
first time it was actually reviewed.

Sort findings into **deductive** (code does X, math implies Y — no statistics, solid as stated) and
**inductive** (this beat that on these episodes — needs a rule-based test bed and honest effective-n,
which is episodes, not configuration rows). They were being quoted with equal confidence.

Before any confirmatory economic test: fix the design and the kill thresholds in advance, as
`algo-trading-bot/SWEEP_PREREG.md` does. A premature version of that document was written and
deleted on 2026-08-12 — it preregistered a test of a form now in question.

## Next

1. **Settle question 1** — what the model should predict. Everything else follows.
2. Then decide whether to fix the current form or replace it.
3. Only then `risk_engine.py` and `main.py`.

Not planned: intraday data, Hawkes, K-means, binary classifiers.

## Open governance question

Not in [[INDEX]] nor the repo table in [[CLAUDE]], so charter status is undeclared.
[[regime-detection/regime-detection]] already concluded a K=2 jump model's decision value is
dominated by reactive estimators — the same pattern found here independently.

## Related

- [[README]] · [[docs/MATH-REFERENCE]] · [[docs/POINT-IN-TIME-DISCIPLINE]]
- [[look-ahead-bias-is-self-concealing]] — vault lesson from this work
- [[INDEX|Home]]
