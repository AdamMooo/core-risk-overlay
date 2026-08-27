# Mathematical audit — the statistical jump model as this repository runs it

Last updated: 2026-08-27. Companion to [[docs/MATH-REFERENCE]] (path functionals) and
[[docs/REPRO-SJM2024-FINDINGS]] (the reproduction this model serves). Everything here is about
`closed-research/reproduction-sjm2024/jumpmodel.py` — the code that actually runs — with the authors' package (`closed-research/reproduction-sjm2024/Shu/`,
cross-checked in `d4_crosscheck.py`) and the literature brought in as evidence.

**The question this document answers** (posed 2026-08-27): is "k-means clustering with a penalty
for changing your mind" the correct mathematical characterization of this model, or a loose
analogy? Method: line-by-line translation of the implementation into notation, derivation of the
statistical interpretation from published theorems, two independent literature sweeps (one
instructed specifically to find evidence the characterization is wrong), and six computational
experiments run against the repository's own functions
(`closed-research/reproduction-sjm2024/jm_math_audit.py`, results reproduced in §H).

## A. Exact objective, as implemented

```
L(s, theta) = sum_{t=1..T} ||x_t - theta_{s_t}||^2  +  lambda * #{t >= 2 : s_t != s_{t-1}}
```

minimized jointly over the state path `s in {0..K-1}^T` and the centroids
`theta = (theta_0..theta_{K-1})`, each `theta_k in R^d`. No `1/T`, no `1/2`, no dimension
normalization. This is not a paraphrase: `fit_jump_model` computes exactly this number at
`closed-research/reproduction-sjm2024/jumpmodel.py:119-123` and selects across restarts on it.

**Convention warning (D5 in the findings doc).** The paper and the authors' package put a `1/2`
on the fit term (`closed-research/reproduction-sjm2024/Shu/jump.py:206`), so `lambda_ours = 2 * lambda_package`. The production
run's `lambda = 50` is the paper's `lambda = 25`. Verified exactly, at every lambda tried, in
`d4_crosscheck.py` (28 checks; the objective relation `val_pkg = ours/2` among them). The wider
literature is split on the same factor — Bemporad et al.'s eq. (6) and the Shu papers carry the
1/2, the Nystrup/Lindström line does not — and no paper remarks on it, so **a lambda is not a
well-defined quantity without naming its convention.** Every lambda in this repository is in the
unscaled (`||.||^2`) convention unless labelled "paper units".

## B. Symbols

| symbol | meaning | production value |
|---|---|---|
| `x_t` | feature vector at day t | 3 features: EWM downside deviation (HL 10d), EWM Sortino (HL 20d, 60d), on excess returns (`closed-research/reproduction-sjm2024/sjm_features.py`) |
| `T` | training window length | 3000 trading days |
| `K` | number of states | 2 |
| `theta_k` | centroid of state k | learned |
| `s_t` | state label at t | learned; state 0 = bull by mechanical naming |
| `lambda` | per-switch penalty | 50 (repo convention) = paper 25 |
| `d` | feature dimension | 3 |

Features are standardized (mean/std of the training window only, `repro_sjm2024.py:104-110`),
which is what gives lambda a stable meaning across refits — §F3.

## C. Derivation from the implementation

Every term of §A, pointed at its line:

1. **Fit term.** `_squared_distances` (`closed-research/reproduction-sjm2024/jumpmodel.py:6-8`) is `D(t,k) = ||x_t - theta_k||^2`.
2. **Penalty term.** `viterbi_path` (`:11-41`) minimizes `sum_t D(t, s_t) + lambda * #switches`
   over paths by dynamic programming:
   `V(t,k) = D(t,k) + min(V(t-1,k), lambda + min_j V(t-1,j))` — the O(T*K) collapse of the
   generic O(T*K^2) recursion, exact because when the global argmin is k itself the stay branch
   is already the smaller (docstring argument, `:17-22`). `V(1,k) = D(1,k)`: no initial-state
   cost, which in §D's terms is a uniform initial distribution.
3. **Joint minimization.** Coordinate descent (`:105-117`): state path by exact DP given
   centroids; centroids by cluster means given the path (the exact minimizer of the fit term,
   since the penalty does not involve theta). Termination: state-path fixpoint or 50 iterations.
4. **Restarts.** 10 k-means++ seedings (`:62-72`), best objective kept (`:124-125`).
5. **Empty clusters.** Reseeded to the worst-explained point (`:115-117`). The authors' package
   instead turns an empty cluster's loss column to `+inf`, making it permanently unreachable
   (`closed-research/reproduction-sjm2024/Shu/jump.py:123`, docstring `:91-92`) — a silent collapse to K-1 states. A real
   behavioral divergence between the two implementations; it never bit on the cross-checked
   data (label agreement 1.0000, `d4_crosscheck.py`).
6. **Online rule.** `online_states` (`:140-153`): label at t is `argmin_k V(t,k)` from a forward
   pass only — the terminal state of the optimal path over data up to t, never revised.
   `checks.py` proves it equals the brute-force prefix optimum. (The literature holds two other
   inequivalent online rules — full-window re-decoding, and Nystrup et al.'s one-step greedy
   assignment — so "online inference" underdetermines behavior unless the rule is named. The
   paper's rule and this one coincide.)
7. **Naming.** `order_states_by` (`:131-137`): ascending centroid of the downside-deviation
   feature. Mechanical, so the labeling is not a researcher choice (D6, closed).

The reproduction wraps this in: per-block standardization -> fit on trailing 3000 days ->
forward-only labels for the next 126 days -> 2-day execution lag (`repro_sjm2024.py:100-122`).
The package example additionally winsorizes features at 3 sigma before scaling — absent from the
paper's text and from this reproduction, declared as **D7 (open)** in the findings doc.

## D. Statistical interpretation — what probability model generates this objective

**The published theorem.** Bemporad, Breschi, Piga & Boyd, "Fitting jump models" (Automatica
2018), Proposition 1 with Corollary 1(4), verified verbatim: take a hidden Markov chain `z_t` on
K states with SYMMETRIC transition matrix (one switch probability `q`, split evenly
off-diagonal), UNIFORM initial distribution, and Gaussian emissions
`x_t | z_t ~ N(theta_{z_t}, sigma^2 I_d)` with sigma FIXED (only the means estimated, flat prior
on them). Then minimizing §A is exactly maximizing the JOINT posterior
`p(x_{1:T}, z_{1:T} | theta)` over the pair `(z, theta)`, with the calibration (inverting their
Corollary 1(4) at K = 2 — the inversion is elementary and, per both literature sweeps,
apparently unpublished as a formula):

```
lambda_ours = 2 * sigma^2 * log((1 - q) / q)
```

Derivation: `-log p(x, z | theta) = sum_t ||x_t - theta_{z_t}||^2 / (2 sigma^2)
+ (#switches) * log((1-q)/q) + const`; multiply through by `2 sigma^2`.

**Three consequences, each load-bearing:**

1. **It is not maximum likelihood.** EM maximizes the MARGINAL likelihood, summing over all
   K^T paths; this maximizes the joint over one path. The estimation style's literature name is
   Viterbi training / classification EM / segmental k-means (Juang & Rabiner 1990), and in
   general it is biased and inconsistent: initialized at the true parameters with infinite data,
   Viterbi training moves away from them (Lember & Koloydenko, Bernoulli 2008; Bryant &
   Williamson, Biometrika 1978, for mixtures). Two qualifications keep this honest. First, the
   jump model is not literally Viterbi training — it freezes the transition structure through
   lambda instead of re-estimating it, and no paper analyzes the jump-model variant directly;
   **no consistency theorem for the jump model exists in either direction** (both sweeps
   confirmed the absence). Second, Experiment 4 measured the bias at the MAP-calibrated lambda
   and found it largely suppressed (§H) — the mechanism is demonstrably real at lambda = 0 and
   demonstrably mitigated by the penalty in that design.
2. **The implied prior at production lambda is absurd, and that is informative.** At sigma = 1
   (standardized features), lambda = 50 implies `q = 1/(1 + exp(25)) ≈ 1.4e-11` per day —
   regimes lasting ~10^10 days. The model works at that lambda anyway because the emission
   assumption is false in exactly one direction: the features are EWM-smoothed, so consecutive
   `x_t` are nearly identical and fit-cost increments are strongly autocorrelated — the
   per-observation information the i.i.d. mapping assumes is not there. Experiment 5 traces the
   shape: with moderately autocorrelated noise (rho 0.9) the recovery-optimal lambda plateaus
   ~1-2.5x above the i.i.d. MAP value; by rho 0.97 the identification ceiling itself drops and
   the lambda-accuracy curve goes flat — persistent noise satisfies the persistence prior, and
   no penalty can separate them. The correct reading of lambda = 50 is "a segmentation dial
   tuned to smoothed features", not "a switching prior".
3. **The transition matrix is a hyperparameter, not an estimate.** lambda is declared here
   (selected by validation-Sharpe CV in the paper — D1's subject). The `transmat_` the package
   reports is a descriptive statistic of the fitted path, outside the estimation.

**Scope note for Thread A.** The Z1-Z5 verdicts score the model as a black-box exposure rule on
its out-of-sample path. Consequence 1 would matter if centroids were read as regime parameters;
they are not, anywhere in the reproduction.

## E. Optimization: what is guaranteed and what is not

- The state block is solved EXACTLY (DP; brute-force checks in `checks.py`, and Experiment 1's
  300 fresh random instances, zero mismatches, prefixes included).
- The centroid block is solved EXACTLY (cluster means).
- The alternation is monotone non-increasing and terminates finitely — Bemporad et al. prove
  precisely this and nothing more. It stops at a partial (coordinatewise) optimum: no global
  guarantee, no rate, no basin theory, and no published counterexample study either. The
  repository's own record already exhibits the failure mode: on synthetic two-regime data,
  lambda_ours = 50 recovers truth at 0.979 while lambda_ours = 30 lands in a local optimum
  calling 73% of days bear ([[docs/REPRO-SJM2024-FINDINGS]]) — lambda moves WHICH local optimum
  coordinate descent finds, not merely the cost of segments.
- Ten k-means++ restarts is folklore-sized insurance (Bemporad et al. suggest five), not a bound.

## F. Theoretical properties

**F1. Identifiability.** The objective is invariant to permuting state labels (K! symmetric
minimizers, always — Bemporad et al. note this verbatim). Mechanical naming (§C7) resolves the
permutation after the fit. Minima exist (finitely many paths; means given a path); uniqueness
fails on ties.

**F2. The solution path in lambda.** For fixed centroids the state problem is the 1-D K-level
Potts / L0-segmentation problem. `J*(lambda)` is the lower envelope of finitely many lines
`fit(s) + lambda * switches(s)`, hence piecewise linear and concave; the optimal path is
piecewise CONSTANT in lambda with finitely many breakpoints; the switch count is monotone
non-increasing in lambda (the exchange argument, published as CROPS Theorem 3.1 — Haynes, Eckley
& Fearnhead 2017 — for free segment levels; the transfer to shared centroids is elementary and
unpublished). Counts can be SKIPPED and segmentations for different counts need not be nested —
unlike the fused lasso (L1), whose 1-D path is piecewise linear and merge-monotone at the price
of shrunken jump heights (Hoefling 2010; Storath, Weinmann & Demaret 2014). Experiment 2
exhibits the skip in five data points (§H). Under JOINT fitting the monotonicity guarantee is
lost (the centroids move with lambda); Experiment 3 found no violation on its instance —
evidence, not proof.

**F3. Scale and dimension sensitivity.** Under `x -> c x` the fit term scales by `c^2` and the
penalty does not, so `fit(cX, lambda) = fit(X, lambda / c^2)` — verified EXACTLY, path for path,
in Experiment 6 (k-means++ seeding probabilities are scale-invariant, so with a fixed seed the
optimizer's whole trajectory maps). lambda is therefore meaningless without naming the feature
scale: per-window standardization is load-bearing, and the effective lambda drifts exactly as
far as each refit window's scale does. Same argument in d: the fit term grows with feature
count, the penalty does not, so a fixed lambda is more switch-prone in higher dimension (the
package's sparse variant scales lambda by `1/sqrt(d)` for exactly this reason; the papers never
discuss it). Any future feature-set change silently invalidates lambda comparisons.

**F4. Overlap and hard assignment.** At lambda = 0 (k-means), ambiguous observations are
assigned wholly to the nearer centroid, truncating the overlap and inflating estimated
separation — measured at +78% in Experiment 4's hardest row. At the MAP-calibrated lambda the
same design shows the bias nearly gone and state accuracy equal to the oracle's: the penalty
reassigns ambiguous days to the temporally consistent state rather than the nearer one, which
un-truncates the assignment sets. No theorem covers this; it is a measured property of this
design.

## G. Literature mapping

| formulation | relation | key source |
|---|---|---|
| Bemporad et al. general jump model | §A is the special case: their eq. (6) loss, constant L_trans, L_init = L_mode = 0 | Automatica 2018, eqs. (12)-(13), verified verbatim |
| joint MAP of a constrained Gaussian HMM | exact equivalence — §D | Prop. 1 + Cor. 1(4), verified verbatim |
| Viterbi training / classification EM | same estimation style; bias mechanism transfers, theorems do not (transition structure frozen here) | Juang & Rabiner 1990; Lember & Koloydenko 2008 |
| 1-D Potts / L0 segmentation | the state block at fixed centroids, exactly; consistency theory exists there (Boysen et al., AoS 2009) but for free levels, not K shared centroids | Friedrich et al. 2008; Boysen et al. 2009 |
| fused lasso / TV | a structural CONTRAST, not an equivalence: L1 shrinks levels, path merge-monotone; L0 keeps levels unbiased, path skips counts | Hoefling 2010; Storath et al. 2014 |
| k-means | the lambda = 0 slice, and the M-step | Bemporad 2018; `checks.py` |

Out of scope because the paper's headline and this repository's run are discrete K=2: the
continuous jump model (simplex-valued states, `(L1/2)^2` transition cost, a mode-loss term that
is ON by default in the package), the sparse jump model (Witten-Tibshirani feature weights), and
the fuzzy variant. They share the package, not the audited objective.

## H. Synthetic validation — six experiments against `closed-research/reproduction-sjm2024/jumpmodel.py`

Script: `closed-research/reproduction-sjm2024/jm_math_audit.py` (the follow-up checks are its final section), 2026-08-27.

1. **Exactness.** 200 random instances (T in [2,8], K in [2,3]): `viterbi_path` value equals
   brute-force enumeration, 0 mismatches. 100 instances, every prefix: forward value matrix
   equals brute-force prefix optima, 0 mismatches. (Independently replicates `checks.py`.)
2. **Worked solution path, T=5.** `x = [0, 0.9, 1, 0.2, 0]`, centroids fixed at {0, 1}.
   Cheapest path per switch count: 0 sw / fit 1.85 (`00000`), 1 sw / 1.05 (`11100`),
   2 sw / 0.05 (`01100`). Analytic envelope: single breakpoint at `lambda* = 0.9`
   (`0.05 + 2 lambda = 1.85`), where the optimum jumps from 2 switches to 0 — count 1 is never
   optimal for any lambda (its line `1.05 + lambda` sits above the envelope everywhere;
   at the crossing it costs 1.95 > 1.85). Verified: `01100` at lambda 0.899, `00000` at 0.901.
3. **Monotonicity.** Fixed centroids, T=2000 two-regime data, 41-lambda grid: switch count
   monotone non-increasing (558 -> 4), as the envelope argument requires. Joint fit on the same
   grid: also monotone here — no counterexample found, none guaranteed.
4. **MAP calibration and bias, K=2 HMM data** (q = 0.02, sigma = 1, T = 3000, 20 reps;
   `lambda_MAP = 2 log(0.98/0.02) = 7.78`):

   | true mu | acc k-means | acc JM at lambda_MAP | acc oracle Viterbi | est. mu, JM | est. mu, k-means |
   |---|---|---|---|---|---|
   | 0.5 | 0.690 | 0.939 | 0.940 | 0.512 | 0.892 |
   | 1.0 | 0.841 | 0.987 | 0.986 | 1.006 | 1.164 |
   | 2.0 | 0.977 | 0.999 | 0.999 | 2.001 | 2.017 |

   The jump model with LEARNED centroids matches the oracle that knows the true ones, and the
   hard-assignment separation inflation (+78% at mu = 0.5 for k-means) is nearly eliminated.
5. **Autocorrelated noise** (AR(1) noise, stationary sd 1; mu = 1, q = 0.02): at rho = 0 the
   recovery-optimal lambda is at the i.i.d. MAP value (grid median 6.1 vs 7.78). At rho = 0.9
   the optimum is a plateau at lambda ~ 8-19 (accuracy 0.887/0.886), decaying beyond (0.844 at
   50, 0.723 at 120). At rho = 0.97 the curve is FLAT (0.845 -> 0.834 across lambda 1 -> 19) at
   a degraded ceiling — the argmax is noise on a ridge, and the i.i.d. lambda-to-q mapping has
   no meaning left.
6. **Scale equivariance.** `fit(3X, lambda)` and `fit(X, lambda/9)` return identical state paths
   (up to label swap) at lambda = 5 and 50 — exact, not approximate.

## I. Failure modes, ranked by relevance to this repository

1. **Local optima steered by lambda** — demonstrated in-repo (§E). Mitigated by restarts and by
   fixing seed and lambda by declaration.
2. **lambda is scale- and dimension-relative** (§F3): any feature-set or scaling change silently
   changes what lambda means. Binding on every future variation.
3. **Breakpoint fragility** (§F2): near a breakpoint the segmentation flips discretely; a
   CV-selected lambda inherits the instability (the paper's own procedure — D1 measured its
   lambda-hat whipsaw here).
4. **No consistency theory**, and a known-biased estimation style (§D1) — though the measured
   bias at MAP calibration was small (§H4). Matters only if centroids are ever read as regime
   parameters; currently they are not.
5. **Empty-cluster divergence between implementations** (§C5): silent K collapse in the package
   vs reseeding here.
6. **Model weight outside the objective**: the package's undocumented 3-sigma winsorization
   (D7, open) and the EWM features, which put most of the persistence into the input before the
   model sees it (§D2).

## J. Verdict

**"Is this actually k-means with a switching penalty?" — Yes, exactly**, as the algebraic
object: the implemented objective is literally the k-means loss plus a constant per-switch
penalty, each coordinate block is solved exactly, and the implementation matches the authors'
package path-for-path under the recorded factor-2 convention. **But that is the less informative
of two exact descriptions of the same object.** By published theorem it is equally the JOINT-MAP
estimator (not maximum likelihood) of a Gaussian-emission HMM with symmetric transitions,
uniform initial law, fixed isotropic covariance, and a switching prior frozen at
`lambda = 2 sigma^2 log((1-q)/q)` — and it is that description that carries the content: what
lambda is, why the estimator differs from EM, which defects it inherits and which it measurably
escapes (§H4), and why the implied prior at production lambda is absurd until the i.i.d.
emission assumption is dropped (§D2). "k-means + penalty" names the algebra; "joint-MAP HMM fit
by classification EM with a frozen switching prior" names the statistics. Only the second
predicts the failure modes in §I.

**On a better formulation (the mandate's §11):** none is proposed. The two candidate repairs the
audit surfaced — an adjusted-Viterbi-style bias correction, and dimension-normalized lambda —
address defects that do not bear on the current use (path-level strategy comparison at fixed
d = 3). Under [[CLAUDE]] §6.13 a model change requires a question that needs it, and no live
question does.

## K. Open questions

1. Consistency of the jump-model path/centroids under an HMM data-generating process — open in
   the literature in both directions; the affirmative evidence (including §H4) is simulation.
2. A lambda calibration under autocorrelated emissions — the honest replacement for the broken
   i.i.d. mapping of §D2. Experiment 5 gives the empirical shape only; unpublished.
3. Whether D7 (winsorization) moves the reproduction's residual Sharpe gap — an open item of the
   findings doc, not a mathematics question.
4. Where the (80,60)/(75,55) deep-tail gap comes from — D8, whose priority Z5 raised; this audit
   neither opens nor closes it.

## Related

- [[docs/REPRO-SJM2024-FINDINGS]] — D1-D8 and the preregistered inference run this model serves
- [[docs/MATH-REFERENCE]] — the path functionals the comparisons are scored on
- `closed-research/reproduction-sjm2024/checks.py` (jump-model block) · `closed-research/reproduction-sjm2024/d4_crosscheck.py` — the machine-checked verification record
