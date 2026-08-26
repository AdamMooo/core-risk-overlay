# Mathematics — the closed rolled-put / tenor intervention programme

**Closed 2026-08-18. Moved here 2026-08-26 from `docs/MATH-REFERENCE.md` §1, §6 and §7, verbatim.**

Preserved for provenance and replication, exactly as the rest of this directory is. **Not an active
branch, not a backlog, and not a source of next experiments** — see [[README]] for why the programme
closed and what its negatives removed.

Why it moved. These three sections are the mathematics of an admissible *intervention*: the C1/C2
constraint that defines one, the decomposition of the measured tenor effect into strike anchoring,
roll-cost avoidance and mark-to-market, and the clairvoyant bound on what any block-level trigger
could achieve. The functions they describe — `simulate(foresight=True)`, `skewed_vol`,
`m3_decomposition` — live in this directory and nothing outside it calls them. Sitting in the active
mathematics reference, they read as available apparatus rather than as a closed programme's record,
which is the repository-gravity failure `../../CLAUDE.md` §3 exists to prevent.

The drawdown process, the CDaR family and the effective-sample-size argument stayed behind: they are
implemented by `src/pathfunctionals.py`, they are what every published CDaR number in the repository
is computed with, and they are cited by live work. [[docs/MATH-REFERENCE]].

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

- Howard (1966) — expected value of perfect information. §7.
- Ilmanen (2012), *Do financial markets reward buying or selling insurance and lottery tickets?* —
  `[UNREAD]`, and the skeptical prior E5 and E7 were read against.
- Israelov (2017), *Pathetic Protection* — `[skim]` 2026-08-18; the sections gating E0 and E1 read in
  full. It contains E1's mechanism and E10's tenor ordering, which is logged as a process failure in
  [[docs/literature/README]].

## Related

- [[README]] — why the programme closed · [[CHARTER-INTERVENTION]] — its charter
- [[docs/MATH-REFERENCE]] — the path-functional mathematics that stayed live
