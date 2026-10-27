# STUB C2 — Can sleeve bands be derived from the asset universe, or are declared bands all a retail investor can honestly carry?

**Status:** DRAFT pre-registration, written before any code. **Created 2026-10-26.** This stub exists
to pass the gate in [[docs/RESEARCH-PROTOCOL]] §0 — not to assert a finding.

**C2** names it: the second candidate under the re-opened repository ([[CLAUDE]] 2026-10-25 policy
change). It is a **measurement** programme ([[CLAUDE]] §4), not prediction, not intervention. It
sits adjacent to C1 (credit saturation) and does not depend on it.

> **Context, not scope.** The question arose from the author's governance repo
> (`portfolio-manager`), whose MANDATE declares sleeve ranges by hand (U.S. equity 25–65%,
> etc.) and whose brief currently reports every drift against them. The honest unease is: *how
> is a band created anyway — is it arbitrary?* This stub answers that question **as research**,
> inside the repository built for it, with no code dependency on the governance repo in either
> direction. If the answer is "declared bands are what the data can honestly support", the
> governance repo keeps its declared bands and the author can trust them. If the answer is
> "bands can be derived with a stated error bar", the governance repo may *consider* adopting
> the method — through its own policy process, never by import. See §6.

---

## The seven fields

### 1. Claim tuple — `(frequency, horizon, functional, sample, null)`

- **Frequency:** monthly returns. Daily would overweight microstructure noise and understate the
  rebalancing-horizon decisions a strategic sleeve band is actually about.
- **Horizon:** the strategic-rebalance horizon, declared as **quarterly** (one of the three
  horizons MANDATE.md Tier-1 drift review runs on). No lead/lag claim; this is a measurement
  test, not forecasting.
- **Functional:** the **range of sleeve weights that is identifiable from the asset universe's
  realized covariance under a stated preference**. Concretely, for a stated risk-aversion `γ` and
  a stated estimation window `W`, the sleeve-weight range `[w_low, w_high]` such that *any*
  weight inside the range is within `ε` of the ex-ante minimum-variance / mean-variance frontier
  under bootstrap resampling of `W`.
- **Sample:** monthly total returns in CAD for a seven-asset proxy universe matching MANDATE.md
  sleeves — one ETF per sleeve (VFV.TO / XIC.TO / VIU.TO / VEE.TO / QTUM / BTCO.B.TO / VAB.TO),
  from each ETF's inception to a cut date committed before the run. Shorter-history sleeves
  (QTUM 2014+, BTCO.B.TO 2021+) are handled by the identification gate in §4, not by backfilling.
- **Null:** the identified sleeve-weight ranges are **not meaningfully narrower than
  MANDATE.md's declared ranges** — median width of identified `[w_low, w_high]` ≥ 90% of the
  width of MANDATE.md's `[low, high]` across sleeves and bootstrap replicates. Rejecting the
  null means the data genuinely narrows the policy; failing to reject means declared bands are
  defensible and the research closes with that finding.

### 2. Predicted outcome, with reason, before any code

**Prediction (point):** the identified ranges are **not meaningfully narrower** than the
declared ones. The null is **not rejected**. Confidence: **high**.

**Reason:** three independent arguments, each sufficient on its own:

1. **DeMiguel–Garlappi–Uppal (2009)** show that out-of-sample, no mean-variance-style portfolio
   construction method consistently beats `1/N` across 14 datasets. If the frontier itself is
   not estimable to usable precision from monthly data, neither is the "optimal range" around
   it.
2. **Michaud (1989) estimation error** — Markowitz weights are notoriously sensitive to the
   covariance input; small changes to `Σ̂` move the frontier by multiples of the sleeve-width
   deltas we would need to detect. The signal is small relative to the measurement error on `Σ̂`.
3. **Sample-size derivation** — with 7 assets and ~20 years of monthly returns, the covariance
   matrix has `7 * 8 / 2 = 28` free parameters and ~240 observations. The condition number of
   `Σ̂` under bootstrap resampling is routinely 10²–10³, which propagates to weight-vector
   intervals an order of magnitude wider than MANDATE.md's bands.

**The run therefore carries information** — a *rejection* would be the informative outcome,
because the prior from the literature is strongly against it.

### 3. Literature check

**Primary:**
- DeMiguel, V., Garlappi, L. & Uppal, R. (2009). *Optimal Versus Naive Diversification: How
  Inefficient is the 1/N Portfolio Strategy?* RFS 22(5). **The paper most likely to settle this
  on its own.** `[UNREAD]`
- Michaud, R. (1989). *The Markowitz Optimization Enigma: Is 'Optimized' Optimal?* FAJ 45(1).
  Estimation-error critique of MVO. `[UNREAD]`
- Jobson, J. D. & Korkie, B. (1980). *Estimation for Markowitz Efficient Portfolios.* JASA
  75(371). Original estimation-error analysis for MVO. `[UNREAD]`

**Secondary / background:**
- Ledoit, O. & Wolf, M. (2004). *Honey, I Shrunk the Sample Covariance Matrix.* JPM 30(4). The
  canonical shrinkage estimator — if adopted, must be declared before the run, not chosen on
  results.
- Meucci, A. (2009). *Risk and Asset Allocation.* Textbook treatment of the full estimation →
  allocation chain. Reference, not citation.

**Pre-run reading commitment:** DeMiguel–Garlappi–Uppal (2009) in full and Michaud (1989)
abstract + §I before any code. If DGU already settles the question on comparable samples, this
stub converts to a reproduction (importing a settled result onto a Canadian-retail asset
universe) rather than a new finding — [[CLAUDE]] §6.5 explicitly allows that.

**Known-settled check:** DGU establishes that MVO weights do not beat `1/N` out-of-sample on
monthly data. If that transfers to this universe, it is *stronger* than our null: it would say
not just that the identified ranges are no narrower than MANDATE.md's, but that the point
estimate itself has no out-of-sample edge over equal-weight.

### 4. Mechanism for a difference, with horizon and functional

**Structural difference claim (what we would need to see for a rejection):** a stable,
estimable covariance structure in the seven-sleeve universe at monthly frequency over the
sample window, such that bootstrap resampling of `W` produces sleeve-weight ranges tighter
than MANDATE.md's 20–40pt declared ranges.

**Horizon at which it becomes observable:** monthly. Daily returns are dominated by
microstructure and intraday noise orthogonal to the strategic-sleeve question; quarterly or
annual aggregation leaves too few observations to estimate a 7×7 covariance.

**Functional on which it becomes observable:** bootstrap distribution of sleeve weights at a
stated `γ` under min-variance and mean-variance objectives, reporting:
- width of 10th–90th percentile for each sleeve weight across 1000 block-bootstrap replicates
  (block length matches an estimated serial-correlation decay);
- comparison of that width to MANDATE.md's declared range width.

**Identification gate.** The three short-history sleeves (QTUM 2014+, BTCO.B.TO 2021+) have ~130
and ~55 monthly observations respectively at the cut date. **The 7-asset covariance is run
twice:** once on the longest overlapping window (constrained by the shortest series) and once
on the 4-asset long-history subset. If the two produce qualitatively different identified
ranges for the four sleeves they share, **the identification claim fails** and the run reports
*that* rather than its headline number — the honest answer being that the universe does not
support the question at this sample size, which [[docs/LESSONS-LEDGER]] registers as a lesson,
not a failure.

### 5. What would surprise me, and what it changes about what we claim to know

**Surprising outcome:** rejection — identified ranges are median-width ≤ 50% of MANDATE.md's
across sleeves and bootstrap replicates, *and* the identification gate passes.

**What it changes:** it would establish that for this specific universe at this specific
sample size, the asset data has enough structure to narrow the declared bands, and the
`portfolio-manager` repo's policy process could *consider* a data-informed narrowing — through
its own MANDATE amendment, not by code import (§6).

**Non-rejection (the predicted outcome):** establishes that declared bands at MANDATE.md's
widths are at or below the precision the data can honestly support, which is a positive
finding — it says the governance repo's bands are not arbitrary in the sense that *tighter
bands would be the arbitrary ones*. This closes the question.

**Identification-gate failure:** establishes that the universe at this sample size does not
support the comparison at all. This is also informative — it tells the governance repo that
"derive the bands from the universe" is not a well-posed ask here, and declared bands remain
the only honest answer.

**Decoration outcome (do not run):** the three results above all materially change the state
of knowledge. There is no fourth outcome that is "no update". Field cleared.

### 6. Question

Which of the four does this move — **existence**, **characterisation**, **transition**, or
**identification** ([[CHARTER]] §1 A/B/C/D)?

**Identification.** The question is whether the sleeve-weight range `[w_low, w_high]` is
*recoverable* from this universe at this sample size. The programme does not ask whether the
"true" bands are different (existence); it asks whether the data identifies them tightly
enough to be worth declaring.

**Scope guard — what this stub is NOT.** It is not a recommendation, not an allocation, not an
exposure, not a weight, not a feed to any other repository. It is a measurement on realized
monthly returns in a stated seven-asset universe. If the governance repo later adopts a
derived band under its own MANDATE amendment process, that is a human action in that repo,
not an output of this one. [[CHARTER]] §5 forbids the circular validation that would arise if
`portfolio-manager` imported this result as a weight input, and the no-import boundary stands
exactly as it does for `regime-detection` and `algo-trading-bot`.

### 7. Cut date and the data commitment

**Cut date to be set at run adoption, before any pull.** Expected: 2026-10-26 close.

**Sources:** monthly adjusted total returns in CAD from the existing cached loaders
([[docs/POINT-IN-TIME-DISCIPLINE]] registered sources). CAD conversion for USD-listed proxies
(QTUM) uses FRED `DEXCAUS` on the matching month-end date; no forward-filled FX. ETF inception
dates taken from issuer prospectus, not from the first available price (which can be a
back-filled index value and is a known leak source — see [[docs/POINT-IN-TIME-DISCIPLINE]] §3).

---

## What this stub is NOT doing

- Not asking "what is the optimal portfolio". Optimality is defined only relative to a stated
  preference; the question here is whether *any* portfolio in a stated range is identifiably
  distinguishable from any other.
- Not asking "what is the market doing now". The entire programme runs on realized return
  history; no regime label, no forecast, no state signal.
- Not asking "should I rebalance". That is a governance decision in a different repository
  under a different policy.
- Not a prelude to an optimizer. The repository's `PARKED.md` is explicit on this and the
  closure of the prediction and intervention programmes stands.

---

**Status at close of this draft:** DRAFT. Not yet in the active queue. Adopts when:
(a) DeMiguel–Garlappi–Uppal (2009) and Michaud (1989) move from `[UNREAD]` to `[READ]` in
`docs/literature/`;
(b) the cut date is committed in §7;
(c) the stub is reviewed against [[docs/RESEARCH-PROTOCOL]] §0 one more time by a human and
the review line is added at the bottom of this file.
