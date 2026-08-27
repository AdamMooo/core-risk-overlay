# Identification under N1 — what is unidentified, and whether Q1's test is valid

> **CLOSED PROGRAMME — PRESERVED AS EVIDENCE.** The return-state programme terminated 2026-08-19 as
> INDETERMINATE ([[CHARTER]] §11). This document is kept intact because the reasoning is the asset;
> nothing in it is a live instruction, and no experiment it describes is queued. **The code moved to
> `closed-research/return-states/`** — path references inside the results sections below record where
> it was when it ran. Full record: [[closed-research/return-states/README]].


Written 2026-08-18, **before Q1 is designed**, as the gate item standing between S0's result and Q1's
stub. Companion to [[CHARTER]] §2 (the null) and [[closed-research/return-states/STUB-S0-WHAT-COUNTS-AS-EVIDENCE]] (which
named the literature but did not work through it).

**Conclusion in one paragraph.** The classical identification failure that makes regime-number testing
hard — Davies' problem — **does not apply to Q1 as S0 has framed it**, because Q1's null N1 is a fully
identified model and Q1's statistic is not a likelihood ratio. That is a real advantage and it was not
an accident of the design. But three separate issues do threaten Q1, and the largest is not
statistical: **rejecting N1 does not identify what replaced it.** Each is flagged below as requiring a
preregistered choice in Q1's stub. **Nothing preregistered is changed here.**

---

## 1. The classical problem, and why it is not ours

The literature the stub named concerns a specific test: `H0: one regime` against `H1: two regimes`,
**inside the Markov-switching likelihood**. Under that null the model is not identified, in several
distinct ways that compound:

```
  1. NUISANCE PARAMETERS UNIDENTIFIED UNDER H0
     With one regime, the transition probabilities p11, p22 and the second
     regime's parameters may take ANY value without changing the likelihood.
     The LR statistic becomes a supremum over a parameter space that does not
     exist under the null -- Davies' problem.

  2. THE NULL SITS ON THE BOUNDARY of the parameter space
     (a mixing weight of 0 or 1), which breaks the standard quadratic expansion
     independently of (1).

  3. THE SCORE IS IDENTICALLY ZERO / THE INFORMATION MATRIX IS DEGENERATE
     in the relevant direction, so the usual second-order expansion is not just
     wrong but vacuous, and higher-order terms are required.

  Consequence: the LR statistic has NO chi-square limit. Not "approximately",
  not "in small samples" -- the limit is a functional of a Gaussian process,
  and which functional depends on which of the three features binds.
```

**Q1's null is not that null.** N1 is GARCH(1,1). Its three parameters are identified and estimable
by quasi-maximum likelihood; there is no mixing weight, no transition matrix, no unidentified
direction. **Under N1 nothing is unidentified.** Q1 computes a moment statistic on the series and
compares it against that statistic's distribution simulated from a fitted N1. That is a **parametric
bootstrap / Monte Carlo specification test**, not a likelihood ratio test, and Davies' problem never
enters.

This is the class Dufour & Luger occupy: they state that "conventional likelihood-based methods are
plagued by identification failures" when testing for Markov switching, and their remedy is exactly
moment-based statistics evaluated by Monte Carlo test techniques. **Q1's design is a member of that
family**, arrived at independently in S0 and confirmed here.

**So the answer to the question this document was asked is:** *nothing is unidentified under N1. What
is unidentified is the alternative* — and that is §3 below, which is the real problem.

## 2. What the literature establishes, and how far each source was actually read

Read-depth is stated per row because [[docs/RESEARCH-PROTOCOL]] §0 rule 3 makes an unread citation a
process failure, and because this environment cannot render several of these PDFs.

| paper | read | what it establishes | bearing on Q1 |
|---|---|---|---|
| **Hansen (1992)**, *The likelihood ratio test under nonstandard conditions*, J. Applied Econometrics 7(S1) S61–S82 | `[abstract]` — publisher abstract and author's page verified; **full text not rendered in this environment** | Uses empirical process theory to **bound** the asymptotic distribution of standardised LR statistics when regularity fails through unidentified nuisance parameters and identically-zero scores | It is a **bound**, so the resulting test is **conservative**: it controls size at the cost of power. Recorded so that an LR route is never proposed here as though it were a sharp test |
| **Garcia (1998)**, *Asymptotic null distribution of the LR test in Markov switching models*, International Economic Review 39(3) 763–788 | `[bibliographic only]` — **abstract not obtained.** Paywalled; the CIRANO working-paper version was not retrieved | Derives an asymptotic null distribution for the sup-LR statistic under the nonstandard conditions | **Cited here as the problem's history, not as support for anything.** No claim in this repository rests on it |
| **Cho & White (2007)**, *Testing for Regime Switching*, Econometrica 75(6) 1671–1720 | `[abstract]` — Econometric Society listing verified verbatim | A **quasi**-likelihood ratio statistic for a *mixture* model, testing one regime against two. Setting involves "nuisance parameters on the boundary of the parameter space, nuisance parameters identified only under the alternative, or approximations using derivatives higher than second order". Obtains null distributions **different from those in the literature** | Two bearings. First, it confirms the three-way compounding in §1. Second, and sharper: **its quasi-likelihood "ignores certain serial correlation properties"** — it treats the data as a mixture rather than a Markov chain. For this program that discards precisely the persistence that motivates the question |
| **Carter & Steigerwald (2012)**, *Testing for Regime Switching: A Comment*, Econometrica 80(4) 1809–1812 | `[bibliographic only]` — **content not obtained**; both the Wiley page and the open working paper failed to render | Comments on the properties of the Cho–White QLR test in a Markov-switching **autoregression** | **Flagged as an unresolved reading gap.** A published comment exists on the exact test the stub cited approvingly. Any future proposal to use the Cho–White QLR here must read it first |
| **Kasahara & Shimotsu (2018)**, *Testing the Number of Regimes in Markov Regime Switching Models*, arXiv:1801.06862 | `[abstract]` — verbatim | The asymptotic distribution of the LR statistic for `M0` vs `M0+1` regimes "**has been an unresolved problem**" as of 2018; they derive it; **contiguous alternatives converge to the null at rate `n^(-1/8)`** in regime-switching models with normal density; parametric bootstrap validity established | **The most consequential row.** See §4 |
| **Dufour & Luger**, *Identification-robust moment-based tests for Markov-switching in autoregressive models*, arXiv:1701.00029 | `[abstract]` — verbatim | Likelihood methods are "plagued by identification failures"; remedy is moments of normal mixtures implied by the regime-switching process, evaluated by **Monte Carlo test techniques**; reports "very respectable power" with computational simplicity | **Q1's design class, independently arrived at.** The nearest prior art to what S0 produced, and the first thing to read in full before Q1's stub is written |

**Two rows are gaps and are recorded as gaps**, not glossed: Garcia (1998) and Carter & Steigerwald
(2012) were not obtained. Neither supports any claim made here. Under §0 rule 3 that is the honest
state, and it is written down rather than papered over with a secondary summary — the standing
instruction from the closed program's reading list excludes citing papers through the papers that
cite them.

## 3. ISSUE 1 — rejecting N1 does not establish states. This is the largest one.

**Flagged, not resolved. It requires a preregistered choice in Q1's stub.**

S0 established that T3 separates a two-state switching process from GARCH(1,1). It established
**nothing** about switching versus any other departure from GARCH(1,1). Elevated dispersion of block
realized variance is equally consistent with, at least:

```
    long memory in volatility          (FIGARCH; hyperbolic rather than
                                        geometric decay -- and note Ryden,
                                        Terasvirta & Asbrink report exactly
                                        this as what HMMs FAIL to reproduce)
    structural breaks in unconditional variance
    stochastic volatility with fat-tailed volatility innovations
    non-Gaussian return innovations at fixed volatility dynamics
    a two-state switching process       <- the one the programme cares about
```

So a Q1 rejection licenses **"the data are not GARCH(1,1)"** and does *not* license **"return states
exist"**. As [[CHARTER]] §9 currently words Q1 — *does a discrete, persistent state structure produce
forward return distributions that N1 does not* — **the question is wider than the test can answer.**

**This is a wording problem in a preregistered document and I am not fixing it by editing the wording.**
It is recorded here, and Q1's stub must resolve it explicitly by choosing one of:

```
  (a) Narrow Q1's claim to what the test delivers: "the data are not N1",
      reported as a falsification of the null and NOT as evidence for states.
      Cheapest, and the only option that needs no new machinery.

  (b) Add a second null -- a long-memory volatility process -- so that a
      rejection is of a CLASS rather than of one member. This is a new S0-style
      identification study before Q1, not a bolt-on.

  (c) Declare in advance that Q1 is a NECESSARY-CONDITION test: failure to
      reject ends the programme under S1, and rejection advances nothing by
      itself. Asymmetric by construction, and honest.
```

**(c) is the option most consistent with [[CHARTER]] §6**, whose stopping rules are already asymmetric
— S1 through S4 are endings, and there is no rule that says "distinguishable from N1 ⇒ states exist".
But the choice is the author's, it belongs in Q1's stub before the run, and stating it here is as far
as this document goes.

## 4. ISSUE 2 — S0 measured detectability at fixed alternatives, not local power

**Flagged, not resolved.**

Kasahara & Shimotsu's rate is the warning. In regime-switching models with normal density, contiguous
alternatives approach the null at **`n^(-1/8)`**, not the usual `n^(-1/2)`. Concretely, at Q1's
sample size:

```
    n = 8,300      n^(-1/2) = 0.011        n^(-1/8) = 0.324
```

The neighbourhood of the null within which alternatives remain undetectable shrinks roughly **thirty
times more slowly** than in a regular problem. That rate is derived for the LR statistic and does not
transfer automatically to T3 — but it says the information about regime structure in a return series
accumulates very slowly, and no moment statistic is exempt from the underlying reason.

**S0 measured `d'` at fixed, well-separated parameter values.** It did not trace how `d'` decays as
the alternative approaches the null. What it did observe is the same phenomenon in coarse form:
**T3 never survived at a variance ratio of 2**, while surviving strongly at 4 and 6.5. That is the
local-power curve showing itself at three points.

Q1's stub must state, in advance, what it does when the market's implied contrast is small. The
default already recorded in [[CHARTER]] §9.1 is that a Q1 negative is **INCONCLUSIVE rather than S1**
unless power against the realised contrast is demonstrated. That default stands and is not weakened
here.

## 5. ISSUE 3 — parameter uncertainty in the simulated null

**Flagged, not resolved.**

Q1 estimates N1's parameters from the same series on which T3 is computed, then simulates the null
distribution of T3 from the fitted values. Holding the estimates fixed treats them as known and
**understates the null distribution's spread**, which inflates rejection rates. Kasahara & Shimotsu
establish parametric bootstrap validity *for their LR setting*; that result does not transfer to an
arbitrary moment statistic by assertion.

Q1's stub must declare which of these it does, before the run:

```
  re-estimate N1 on every bootstrap replicate  (correct, ~R times the cost)
  fix the estimates and DEMONSTRATE the size distortion is small at n = 8,300
  fix the estimates and report the test as approximate, with the direction of
    the distortion stated (it inflates rejections, i.e. it favours the
    programme's own hypothesis -- which is the direction that requires the
    most care)
```

## 6. What this changes about Q1's validity — the summary

| | status |
|---|---|
| Davies' problem / unidentified nuisance parameters | **Does not apply.** Q1's null is identified; Q1's statistic is not a likelihood ratio |
| Boundary and degenerate-information problems | **Do not apply**, same reason |
| Hansen's conservatism | **Not inherited** — it is a property of the LR route Q1 does not take. Recorded so the route is not proposed later as though it were sharp |
| Cho–White's serial-correlation-ignoring quasi-likelihood | **Not inherited**, and a reason not to adopt that route here even if identification were solved |
| **Rejection does not identify the alternative** | **APPLIES, and it is the binding limitation.** §3 |
| **Very slow accumulation of regime information** | **APPLIES in spirit**; S0 saw it at three points. §4 |
| **Bootstrap parameter uncertainty** | **APPLIES.** §5 |

**Q1's test is valid as a test of N1.** It is not, without a preregistered narrowing, a test of the
question [[CHARTER]] §9 currently asks.

## 7. What is NOT changed by this document

The null (N1), the frequency (daily), the functional (T3, dispersion of log realized variance over
21-day blocks with 63 as the declared sensitivity), the forbidden candidates, and the mismatch-floor
rule are all as S0 left them. **No preregistered choice has been altered.** Three issues are flagged
for Q1's stub to resolve before it runs.

## Related

- [[CHARTER]] §2 — the null · §6 — the stopping rules · §9.1 — what S0 fixed
- [[closed-research/return-states/STUB-S0-WHAT-COUNTS-AS-EVIDENCE]] — the experiment that produced the functional
- [[docs/RESEARCH-PROTOCOL]] §0 rule 3 — the literature gate this document discharges
- [[docs/POINT-IN-TIME-DISCIPLINE]] — row 1, the smoothed-versus-filtered constraint
