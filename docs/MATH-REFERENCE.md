# Mathematics Reference — path functionals and admissibility

Last updated: 2026-08-17

The mathematics of the active program. Notation is plain text throughout.

**Why this file was rewritten from nothing.** The previous reference ran to 1,143 lines on conditional
densities, Gaussian mixtures, Hamilton recursions and squared-return autocovariance — and contained
**no treatment of drawdown at all**. The measurement apparatus lived in the space of marginal
distributions while the objective lived in the space of path functionals, and nobody noticed for two
years. That file is preserved at [[closed-research/docs/MATH-REFERENCE]]. This one covers the space the
objective actually lives in.

---

## 1. Admissibility

Let the core hold `N_core(t)` shares of the index at price `S(t)`, and let `V(S_T)` be terminal wealth
as a function of the core's terminal price. An intervention is **admissible** iff:

```
(C1)  N_core(t) is non-decreasing in t
(C2)  dV/dS_T = N_core   for all S_T > S*,  some S*
```

**C1 alone is vacuous.** A short futures overlay of size `h` never sells a share and produces
`V = N·S_T - h·(S_T - F)`, slope `N - h` everywhere: economically a sale. C2 is what excludes it.

**C2 says: buy asymmetry, not exposure reduction.** For a long put at strike `K`,

```
V(S_T) = N·S_T + c·max(K - S_T, 0) - premium
slope  = N        for S_T > K       <- upside preserved, C2 satisfied
       = N - c    for S_T < K
```

`V` is convex and the upside slope is untouched. That is the whole content of "permanently long."

### 1.1 Why put spreads fail C2, derivable without data

Long a put at `K1`, short a deeper put at `K2 < K1`:

```
payoff(S_T) = max(K1 - S_T, 0) - max(K2 - S_T, 0)

            = K1 - K2      for S_T <= K2      slope  0
            = K1 - S_T     for K2 < S_T < K1  slope -1
            = 0            for S_T >= K1      slope  0
```

The payoff slope runs `0 -> -1 -> 0`, so the structure is **neither convex nor concave**, and the
protection is capped below `K2` — flat exactly where the deep tail is. F12 measured this empirically
(spreads buy 3.3-6.8pp of drawdown against outright's 16.8-24.3pp). **C2 gives it a priori.** A
constraint that reproduces a measured result from first principles is doing real work.

## 2. The drawdown process

Let `W(t)` be marked wealth. Define:

```
M(t) = sup_{s <= t} W(s)              running maximum
D(t) = 1 - W(t) / M(t)     in [0,1)   drawdown, reported as POSITIVE depth
```

`D` is the object; everything below is a functional of `D` or of its excursions.

**Excursions.** Maximal intervals on which `D > 0`. For excursion `i`:

```
depth_i     = sup D over the interval
duration_i  = peak to trough, in observations
recovery_i  = trough to new high, in observations
```

An excursion still under water at the end of the sample is **censored**: its `recovery` is a lower
bound, not a duration, and averaging it in as one is an error. `pathfunctionals.Excursion` carries a
`recovered` flag for exactly this and it is checked.

## 3. Why not max drawdown

```
MDD = sup_t D(t) = max_i depth_i
```

`MDD` is an **extreme-value functional**. On a single path it is one order statistic of one sample of
episodes, and on SPY 1993-2026 it is set by a single episode (Oct 2007 - Mar 2009). The 1993- and
2003- subsamples share that episode entirely, so they are not two observations of it.

**Consequence, and it is the binding constraint on the whole program:** the difference of two `MDD`s —
"drawdown bought" — has **effective n = 1**. It has no sampling distribution, no standard error, and no
population interpretation. It may be *reported*; it may not be *ranked on*, and no magnitude may be
asserted from it.

## 4. Conditional Drawdown-at-Risk

Let `mu_D` be the occupation measure of `D` over `[0, T]`:

```
mu_D(A) = (1/T) · Leb{ t in [0,T] : D(t) in A }
```

Then for `alpha` in `(0, 1]`:

```
CDaR_alpha = E[ D | D >= q_{1-alpha}(D) ]      under mu_D
```

the mean of the worst `alpha`-fraction of the drawdown process. Chekhlov, Uryasev & Zabarankin (2005).
It is **coherent** and **convex in the position**, which is what makes it optimizable later; and it is
computed from the *whole path*, so its effective sample is the number of distinct excursions rather
than one.

**The limits are the point:**

```
alpha -> 1    average drawdown (the pain index)      well sampled
alpha -> 0    max drawdown                           effective n = 1
```

`CDaR_alpha` is a one-parameter family interpolating continuously between a statistic we can estimate
and one we cannot. **Report it as a curve in `alpha`.** The `alpha` at which the estimate destabilises
across phases and subsamples *is the measurement* of how much of a claim rests on a single episode.
That converts the sample-size problem from a caveat into an output.

**Leak note.** `alpha` and the excursion threshold are researcher degrees of freedom — rows 10 and 11
of the leak register. Declared in the stub, never selected from the result.

## 5. The rest of the objective space

```
g            = (1/T)·log W(T)                        geometric growth rate
premium_drag = total premium / years                 well sampled: ~1700 rolls
U_theta      = (1/T)·Leb{ t : D(t) > theta }         time under water (Ulcer/pain family)
R            = { recovery_i }                        recovery-time distribution
kappa        = H(t*) / S(t*)                         shares purchasable at the trough
```

`U_theta` is the precise form of "smooth the ride." Annualised volatility is **not** — it is symmetric,
and the mandate never asked for symmetry to be reduced.

`kappa` is the bridge from drawdown reduction to future compounding: `H` is the *liquidatable* hedge
value under a stated causal monetisation rule `rho`, evaluated at the drawdown trough `t*`. With no
`rho`, `kappa` is undefined — which is the current state, and is why E6 exists.

## 6. The three mechanisms, separated

The measured tenor effect is a composite. These have different assumption costs and must never be
quoted as one number.

```
M1  STRIKE ANCHORING
    rolled:   sum_j max( S(t_j)(1-m) - S(t_j + tau_s), 0 )      re-strikes downward
    anchored: max( S(t_peak)(1-m) - S(t_peak + tau_L), 0 )      spans the episode

    Function of the PRICE PATH ONLY. No option pricing, no VIX, no surface.
    Testable on any index and any history. Falsifiable by sign across episodes.

    Careful: at equal contract count this compares protection DELIVERED, not
    protection BOUGHT -- a longer put at the same moneyness finishes ITM more
    often and costs more. The monetary comparison needs M2.

M2  ROLL-COST AVOIDANCE
    Depends on the implied-vol term structure via skewed_vol's sqrt(4/tenor).
    That is an ASSUMPTION, and it favours the conclusion. The chain archive
    begins 2026-08-14 and cannot cover 2008, so M2 is NOT VERIFIABLE on the
    historical sample: a surface fit can REJECT the shape, never confirm the
    cost. Formally asymmetric, in the same way the closed program's GARCH null
    was asymmetric.

M3  MARK-TO-MARKET
    equity[t] = shares·S(t) + contracts·put_value(t)
    A long-dated put's mark rises through a drawdown, mechanically reducing
    measured MDD. Requires pricing AND a policy. Under the currently
    implemented policy -- hold to expiry -- this reduction is a MARK, not cash.

    E0 decomposes it exactly:  MDD(marked) - MDD(hedge marked at zero intra-block)
```

## 7. The clairvoyant bound

`simulate(foresight=True)` skips any block whose structure would expire worth less than it cost. This
is the **expected value of perfect information** (Howard 1966) restricted to block-level on/off rules at
a fixed structure:

```
EVPI(tau, m) = Phi( best block-level rule with perfect foresight ) - Phi( always-on )
```

Two properties worth stating precisely, because this is the strongest construction the repo owns:

1. **It is search-independent.** It bounds what *any* trigger could achieve without anyone having to
   find one. That is why it is stronger evidence than a failed search.
2. **It is a lower bound on the true EVPI**, because the true supremum would also choose tenor and
   strike per block. Quote it as "no block-level rule at this structure beats X," never as "no rule
   beats X."

Currently evaluated at `tau in (4, 13)` only — the tenors the structure grid suggests are dominated.
Extending it is E3.

## References

- Chekhlov, Uryasev & Zabarankin (2005), *Drawdown measure in portfolio optimization* — CDaR,
  coherence, convexity. The core reference for §4.
- Magdon-Ismail & Atiya (2004), *Maximum drawdown* — the distribution of MDD, and why one path is one
  observation of it.
- Grossman & Zhou (1993); Cvitanić & Karatzas (1995) — portfolio choice under a drawdown constraint.
- Carr, Zhang & Hadjiliadis (2011), *Maximum drawdown insurance* — pricing protection on the drawdown
  itself.
- Howard (1966) — expected value of perfect information.
- Ilmanen (2012); Israelov (2017), *Pathetic Protection* — the cost of rolled index put protection.
  Both `[UNREAD]`, and under protocol §0 rule 3 that tag on a paper whose construction we are using is
  itself the defect.

## Related

- [[CHARTER]] §2-§3 — the space and the objective · [[docs/RESEARCH-PROTOCOL]] — the gate
- [[docs/POINT-IN-TIME-DISCIPLINE]] — rows 9-13 govern the knobs above
- [[closed-research/docs/MATH-REFERENCE]] — the closed program's mathematics, intact
