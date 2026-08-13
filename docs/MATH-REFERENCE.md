# Math Reference — 2-Regime Markov-Switching Volatility Model

Last updated: 2026-08-12 (**reduced** from 2065 lines: audit records of the deleted constrained
specification compressed into Section 8; repeated worked examples and recitals of fitted
parameter values removed)

Companion to `src/jump_model.py`: every equation is tied to the code it becomes, every technique
named with its standard-literature term.

> **Status note — the specification documented here is not settled.** This document describes
> what the model *is*. It is not a claim that the model is right. Three findings stand against it:
> - Corrected AIC and BIC both prefer $k=3$ over $k=2$ on real data:
>   $\Delta\text{AIC} = +65.9993$, $\Delta\text{BIC} = +44.1298$ favouring three regimes.
> - ARCH-LM(4) on the regime-standardized residuals rejects at $55.652$
>   ($p = 2.372\times10^{-11}$) *after* regime switching — volatility keeps moving *within* regimes.
> - The model's target variable (weekly return variance) may not be the project's actual target
>   (forward drawdown in a long global equity book).
>
> The open-questions list is `README.md` section 2. Read it before treating anything below as
> settled design.

**Scope.** The estimator fitted is `statsmodels`' `MarkovRegression` with
`k_regimes=2, trend="c", switching_trend=True, switching_variance=True`, on weekly SPY log
returns (`src/jump_model.py:125-131`). No subclass, no overrides: six free parameters, all
estimated. Which fitted regime is the "jump" regime is decided **after** the fit, by whichever
carries the larger variance (`_jump_regime_index`, `src/jump_model.py:96-105`).

**Conventions.** Library files (cited by basename) live in
`.venv/.../statsmodels/tsa/regime_switching/`. Numeric examples come from the deterministic
synthetic fit in `checks.py:37-46` ($T = 150$); figures from the real SPY fit ($T = 1750$, via
`diagnostics.py`) are labelled **real**. The jump regime lands on index **1** on the fixture and
on index **0** on every real fit — Section 7's identification problem, not a bug.

---

## Notation

Fixed for the whole document. (Unnumbered, so "Section 1.x" always means a Layer 1 subsection.)

| Symbol | Meaning | statsmodels name | Where |
|---|---|---|---|
| $t$, $T$ | time index and sample length; weekly | `nobs` | `src/data_loader.py:111` |
| $r_t$, $\mathcal F_t$ | weekly log return $\log(P_t/P_{t-1})$; information set $\{r_1,\dots,r_t\}$ | `endog` | `src/data_loader.py:111` |
| $S_t$ | latent regime, $S_t \in \{0,1\}$; labels are meaningless until 7.3 | — | `src/jump_model.py:7` |
| $j^\star$ | **jump** regime index, $= \arg\max_j \hat\sigma_j^2$, decided after the fit | `jump_regime_index` | `src/jump_model.py:96-105` |
| $p_{ij}$ | $\Pr(S_t = j \mid S_{t-1} = i)$ — **row = from, column = to** | `p[i->j]` | `markov_switching.py:1405-1408` |
| $P$, $\Pi$ | $P$ row-stochastic with $P_{ij} = p_{ij}$; $\Pi = P^{\!\top}$, what statsmodels builds | `regime_transition_matrix` | `markov_switching.py:632-664` |
| $\pi$ | ergodic (stationary) distribution, $\Pi\pi = \pi$ | `initial_probabilities` | `markov_switching.py:576-602` |
| $\mu_j$, $\sigma_j^2$ | regime-$j$ intercept and variance; both **switch**, both unrestricted | `const[j]`, `sigma2[j]` | `markov_regression.py:342-352` |
| $\theta$, $\tilde\theta$ | $(p_{00},\,p_{10},\,\mu_0,\,\mu_1,\,\sigma_0^2,\,\sigma_1^2)\in\mathbb R^6$, and its optimizer-space (unconstrained-link) image | `params` | `markov_switching.py:1388-1453` |
| $\eta_t(j)$ | conditional density $f(r_t \mid S_t = j;\theta)$ | `conditional_loglikelihoods` (logged) | `markov_regression.py:190-191` |
| $\xi_{t\mid t-1}$ | **predicted** probs, $\Pr(S_t = \cdot \mid \mathcal F_{t-1})$ | `predicted_marginal_probabilities` | `markov_switching.py:1583-1591` |
| $\xi_{t\mid t}$ | **filtered** probs, $\Pr(S_t = \cdot \mid \mathcal F_t)$ | `filtered_marginal_probabilities` | `markov_switching.py:174` |
| $\xi_{t\mid T}$ | **smoothed** probs, $\Pr(S_t = \cdot \mid \mathcal F_T)$ | `smoothed_marginal_probabilities` | `markov_switching.py:300-303` |
| $\ell_t$, $\ell(\theta)$ | per-period and total log-likelihood | `joint_loglikelihoods`, `llf` | `markov_switching.py:180`, `1902` |
| $z_t$ | regime-standardized residual $(r_t - \hat\mu_{S_t})/\hat\sigma_{S_t}$ | — | `diagnostics.py:545-546` |
| $k$, $\odot$, $\mathbf 1$ | free-parameter count; Hadamard product; column vector of ones | `k_params` | `markov_switching.py:541-546` |

**The one notational trap in this codebase.** $p_{ij}$ above is *from $i$ to $j$*, matching the
statsmodels *parameter name* `p[i->j]`. But the *matrix* statsmodels constructs is the transpose:
`regime_transition_matrix(params)[i, j, 0]` $= p_{ji}$ (`markov_switching.py:643-648`). Columns
sum to one, not rows. It is why `diagnostics.py:145` slices `[:, :, 0]` and then reads $p_{ii}$
off the *diagonal* only, where the ambiguity cannot bite.

---

## The four layers

Everything below is one of four objects, and confusing them is the main source of error.
**Layer 0–1, the model:** a specification — state space, transition law, emission law.
**Layer 2, the Hamilton filter:** a forward recursion that, *given* $\theta$, produces
$\xi_{t\mid t}$ and the likelihood; real-time. **Layer 3, MLE:** an optimizer that searches
$\theta$ by calling the filter repeatedly; machinery, not economics. **Layer 4, the Kim
smoother:** a backward recursion that revises the state probabilities using the whole sample,
after estimation; retrospective.

---

## Layer 0 — What kind of model this actually is

### 0.1 `MarkovRegression` is a class name, not a model name

You are not fitting a regression. The family member instantiated here has **no exogenous
regressors**: `exog=None`, and `trend="c"` merely prepends a column of ones, which with
`switching_trend=True` gets a *separate* coefficient per regime. Drop the regressors and you get

$$r_t = \mu_{S_t} + \varepsilon_t, \qquad \varepsilon_t \mid S_t = j \;\sim\; \mathcal N(0, \sigma_j^2),
\qquad S_t \text{ a 2-state Markov chain}$$

whose literature names, in decreasing generality, are: **Markov-switching / regime-switching
model** (econometrics umbrella); **hidden Markov model (HMM) with Gaussian emissions**
(statistics/ML — discrete latent state, continuous observation, first-order Markov transitions);
**Markov-switching mean and variance model** (Hamilton 1989's switching mean plus the
financial-econometrics switching-variance extension); and **two-component location–scale mixture
of normals with Markov-dependent mixing** (the *marginal* law of $r_t$ is a two-component normal
mixture with weights $\pi$, the chain adding serial dependence to which component is drawn). Any
of those four is a correct search term; "Markov regression" is not. Hamilton (1989) introduced
both the specification and the recursion that evaluates its likelihood, so model and filter share
the surname: `markov_regression.py` implements the model, `cy_hamilton_filter_log` the filter.

One more naming correction: `README.md:15` calls this a "jump-diffusion" model. It is not one. A
jump-diffusion (Merton 1976) is a continuous-time process with a diffusion term plus a **compound
Poisson** jump term, jumps instantaneous and independent across time. This model has no diffusion,
no Poisson process, and its "jumps" are *persistent states* lasting several weeks — a
discrete-time proxy for elevated volatility, not for jump arrivals.

### 0.2 Why classical regression diagnostics do not transfer

| Regression diagnostic | Why it is vacuous or inverted here |
|---|---|
| Residual-vs-fitted plot, linearity of $E[y\mid x]$, $R^2$ | There is no $x$, so nothing to be linear in and no variation explained by covariates. `fittedvalues` is $\sum_j \xi_{t\mid t}(j)\hat\mu_j$ — a monotone re-reading of the regime probability, so plotting residuals against it plots them against the signal. |
| Homoscedasticity | **Deliberately violated.** Heteroskedasticity is the signal being estimated. A Breusch–Pagan or White rejection is the model working. |
| Normality of raw residuals $r_t - \bar r$ | Guaranteed to fail: the raw residual is by construction a location–scale mixture, hence leptokurtic and skewed. Testing it tests the *premise*, not the fit. **Real:** JB $= 4983.75$, excess kurtosis $8.078$, skew $-0.879$. |
| DW / Ljung–Box on raw residuals | Confounds regime persistence with genuine serial correlation in returns. |

What replaces them is Section 6 — plus pseudo-real-time out-of-sample evaluation (4.3), which
matters most for a trading signal and is the one thing the repo still does not do.

---

## Layer 1 — The model

### 1.1 Complete specification

State space $S_t \in \{0, 1\}$. **Transition law** (first-order, time-homogeneous; the `tvtp`
branch is unused since `exog_tvtp=None`), then the **observation (emission) law**:

$$\Pr(S_t = j \mid S_{t-1} = i, S_{t-2}, \dots, \mathcal F_{t-1}) = \Pr(S_t = j\mid S_{t-1}=i) = p_{ij}$$

$$r_t \mid S_t = j \;\sim\; \mathcal N(\mu_j,\ \sigma_j^2), \qquad
\eta_t(j) \;=\; \frac{1}{\sqrt{2\pi\sigma_j^2}}\,
\exp\!\left(-\frac{(r_t-\mu_j)^2}{2\sigma_j^2}\right)$$

computed longhand at `markov_regression.py:190-191` as
`-0.5 * resid**2 / variance - 0.5 * np.log(2*np.pi*variance)`. Note what the switching mean does
*not* buy: the regime log-density ratio is a constant plus a term quadratic in $r_t$, dominated
on real data by the $1/\sigma^2$ asymmetry rather than by the $0.623\%$/wk gap between the means
— worth $0.16$ jump-regime standard deviations — so a large positive week is nearly as strong
evidence of the jump regime as a large negative one.

**Subtlety that matters in 2.4.** The conditional-density array has shape `(2, 2, T)`: `_resid`
repeats the prediction across a redundant $S_{t-1}$ axis, so the filter runs on the *pairwise*
joint even though the emission depends on $S_t$ alone, which inflates the filter's local `order`
to **1** while `model_order` stays **0** (`markov_switching.py:157`). Harmless for the marginal
recursions, since the redundant axis is summed out; not harmless for initialization.

### 1.2 The transition matrix and its indexing

Only $k(k-1) = 2$ transition parameters are free, and statsmodels parameterizes **column 0 of
$\Pi$ only**: the names come from
`['p[%d->%d]' % (j, i) for i in range(k-1) for j in range(k)]`, so with $k=2$ the outer loop
takes only $i=0$ and yields exactly `['p[0->0]', 'p[1->0]']` — both *destinations* are regime 0.
Row 0 gets $(p_{00},\,p_{10})$; row 1 is filled by complement (`markov_switching.py:652-659`):

$$\Pi[:,:,0] \;=\;
\begin{pmatrix} p_{00} & p_{10} \\ 1 - p_{00} & 1 - p_{10}\end{pmatrix}
\;=\;
\begin{pmatrix} p_{00} & p_{10} \\ p_{01} & p_{11}\end{pmatrix}
\;=\; P^{\!\top}, \qquad
P = \begin{pmatrix} p_{00} & p_{01} \\ p_{10} & p_{11}\end{pmatrix}$$

**$\Pi$ is left-stochastic** — each *column* sums to one; assume row-stochastic and you will
silently read $p_{10}$ where you meant $p_{01}$. (It is also 3-D, shape `(2, 2, 1)`, the trailing
axis reserved for TVTP.) **`tm[1,1,0]` $= p_{11}$** is diagonal, so the ambiguity does not bite
there — but it is *not* a fitted parameter, being $1 - p_{10}$; any restriction on regime 1's
self-persistence must go through $p_{10}$.

### 1.3 The parameter vector

Parameters are ordered by block, then number, then regime (`markov_switching.py:323-352`), the
blocks being `regime_transition`, `exog`, `variance`:

$$\theta = \big(\,\underbrace{p_{00},\ p_{10}}_{\texttt{regime\_transition}},\
\underbrace{\mu_0,\ \mu_1}_{\texttt{exog}},\
\underbrace{\sigma_0^2,\ \sigma_1^2}_{\texttt{variance}}\,\big) \in \mathbb R^6$$

`param_names` $=$ `['p[0->0]', 'p[1->0]', 'const[0]', 'const[1]', 'sigma2[0]', 'sigma2[1]']` and
`k_params = 6`, asserted at `checks.py:110-113`. **All six are free**; `src/jump_model.py` defines
no `transform_params` or `untransform_params` override at all. The likelihood separates the
regimes overwhelmingly on variance, so the *variance ratio* decides how sharply they are
identified — $37.7\times$ on the synthetic fixture against $6.53\times$ on real SPY.

### 1.4 Ergodic (stationary) distribution

Two reasons you need it: it is the filter's initial condition (2.4), and it is the model's implied
unconditional frequency of crisis weeks — a prior you assert whether you meant to or not.
$\pi$ satisfies $\Pi\pi = \pi$ with $\mathbf 1^{\!\top}\pi = 1$ (equivalently
$\pi^{\!\top} P = \pi^{\!\top}$: $\pi$ is the left eigenvector of $P$, the right eigenvector of
$\Pi$, for eigenvalue 1). First component:

$$\pi_0 = p_{00}\pi_0 + p_{10}\pi_1
\;\Longrightarrow\; \pi_0(1 - p_{00}) = \pi_1 p_{10}
\;\Longrightarrow\; \pi_0 p_{01} = \pi_1 p_{10}$$

Impose $\pi_0 + \pi_1 = 1$:

$$\boxed{\ \pi_0 = \frac{p_{10}}{p_{01} + p_{10}}, \qquad \pi_1 = \frac{p_{01}}{p_{01} + p_{10}}\ }$$

The chain is irreducible and aperiodic whenever $0 < p_{01}, p_{10} < 1$, so $\pi$ is unique and
limiting — standard finite-state Markov chain theory (Perron–Frobenius). statsmodels solves it
for general $k$ by pseudo-inverse (`markov_switching.py:587-589`), flooring at $10^{-20}$ so the
log-space filter never sees $\log 0$. **Read the result as a claim:** on the real fit
$\pi_{j^\star} = 0.263603$, so the model asserts 26.4% of all weeks are jump-regime weeks — at
that frequency an elevated-volatility state, not a panic detector.

### 1.5 Expected regime duration

Condition on having just entered regime $i$. The run continues with probability $p_{ii}$ each
period independently (first-order Markov), so run length $D_i$ is geometric on $\{1,2,3,\dots\}$:

$$\Pr(D_i = d) = p_{ii}^{\,d-1}(1 - p_{ii}), \qquad
E[D_i] = \sum_{d\ge1} d\,p_{ii}^{\,d-1}(1-p_{ii}) = \boxed{\frac{1}{1 - p_{ii}}}$$

Since $\operatorname{Var}(D_i) = p_{ii}/(1-p_{ii})^2$, the standard deviation of duration is
$\approx E[D_i]$ for $p_{ii}$ near 1: durations are enormously dispersed — a "50-week average"
regime routinely produces 5-week and 150-week runs — so never treat $E[D_i]$ as typical. As a
diagnostic (`diagnostics.py:621-629`) compare it against empirical run lengths of $\hat S_t$; on
the real fit both regimes come out more persistent than the realized episodes, that dispersion
interacting with a fuzzy classifier whose short spells below $0.5$ chop long episodes up.

---

## Layer 2 — The Hamilton filter

Hamilton (1989), *Econometrica* 57(2), 357–384, §2–3. Also the HMM **forward algorithm** with
normalization (Rabiner 1989 calls the normalizer $c_t$); Hamilton's contribution was the framing
in which the normalizer *is* the likelihood contribution.

### 2.1 What "filtered" means, precisely

$$\xi_{t\mid t}(j) \;=\; \Pr\!\big(S_t = j \;\big|\; r_1, r_2, \dots, r_t;\ \theta\big)$$

Conditioning set: **past and present only** — $r_{t+1},\dots,r_T$ do not appear. This is the
object a real-time signal is allowed to use, because at the close of week $t$ it is the entire
posterior available.

### 2.2 The recursion, in three steps

Collect the densities into $\eta_t = (\eta_t(0),\ \eta_t(1))^{\!\top}$. **Step 1 — Prediction**
(propagate the chain one step; Chapman–Kolmogorov):

$$\xi_{t\mid t-1}(i) \;=\; \sum_{j} p_{ji}\,\xi_{t-1\mid t-1}(j)
\qquad\Longleftrightarrow\qquad
\xi_{t\mid t-1} = \Pi\,\xi_{t-1\mid t-1}$$

The matrix form is *why* statsmodels stores $\Pi = P^{\!\top}$: left-stochastic means the
propagation is a plain matrix–vector product with no transpose. **Step 2 — Update** (Bayes'
rule; the regime posterior given the new observation):

$$\xi_{t\mid t}(j)
\;=\; \frac{\eta_t(j)\,\xi_{t\mid t-1}(j)}{\sum_{i}\eta_t(i)\,\xi_{t\mid t-1}(i)}
\qquad\Longleftrightarrow\qquad
\xi_{t\mid t} = \frac{\eta_t \odot \xi_{t\mid t-1}}{\mathbf 1^{\!\top}(\eta_t \odot \xi_{t\mid t-1})}$$

Numerator = prior $\times$ likelihood; denominator = the marginal density of $r_t$, the normalizing
constant Bayes' rule requires. **Step 3 — Likelihood contribution:** that denominator is not
thrown away, it *is* the one-step-ahead predictive density.

$$f(r_t \mid \mathcal F_{t-1};\theta)
= \sum_j f(r_t\mid S_t=j)\Pr(S_t=j\mid\mathcal F_{t-1})
= \mathbf 1^{\!\top}(\eta_t \odot \xi_{t\mid t-1})$$

$$\ell_t = \log\!\big(\mathbf 1^{\!\top}(\eta_t \odot \xi_{t\mid t-1})\big),
\qquad \ell(\theta) = \sum_{t=1}^{T}\ell_t$$

This is the **prediction-error decomposition**: the joint density factorizes as
$f(r_1,\dots,r_T) = \prod_t f(r_t\mid \mathcal F_{t-1})$, and the filter produces each factor as a
by-product of maintaining the state posterior — turning an otherwise intractable $2^T$-term sum
over regime paths into $O(Tk^2)$. Step 1's $\Pr(S_t = j \mid \mathcal F_{t-1})$ is also a genuine
**one-week-ahead forecast**, the only object with *no* dependence on week-$t$ data
(`predicted_marginal_probabilities`).

### 2.3 Log-space form — what the code actually runs

`cy_hamilton_filter_log` converts to logs first (`markov_switching.py:169-170`) and runs the
recursion additively. Writing $L^{\text{pred}}_t = \log\xi_{t\mid t-1}$,
$L^{\text{filt}}_t = \log\xi_{t\mid t}$:

$$L^{\text{pred}}_t(i) = \operatorname*{logsumexp}_{j}\big[\log p_{ji} + L^{\text{filt}}_{t-1}(j)\big]$$

$$a_t(i) = \log\eta_t(i) + L^{\text{pred}}_t(i)$$

$$\ell_t = \operatorname*{logsumexp}_{i} a_t(i), \qquad
L^{\text{filt}}_t(i) = a_t(i) - \ell_t$$

with $\operatorname{logsumexp}(x) = \log\sum_i e^{x_i}$ evaluated by the max-shift trick
$= x^* + \log\sum_i e^{x_i - x^*}$.

**Why log-space is not optional.** Step 2's normalization keeps $\xi_{t|t}$ on $[0,1]$, so the
*probabilities* do not underflow; the unnormalized forward variables do, in both directions. The
running product $\prod_{s\le t} f(r_s\mid\mathcal F_{s-1})$ **grows** — weekly returns are
$O(10^{-2})$, so the density is $O(10)$ and $\ell_t$ mostly positive, reaching
$e^{4310.94} \approx 10^{1872}$ on the real sample against a float64 ceiling near $10^{308}$ —
while a run of crisis weeks evaluated under the *calm* regime drives it back down just as fast.
Line 170 also floors transition probabilities at $10^{-20}$ before logging, load-bearing where
the $k=3$ comparison fit returns $p_{2\to0} = 4.36\times10^{-19}$.

### 2.4 Initialization

Default is **steady-state (ergodic) initialization** (`markov_switching.py:537-538`), never
overridden, so $\xi_{1\mid 0} = \pi$. One wrinkle: `markov_switching.py:187-197` writes $\log\pi$
into the filtered joint array and, because the local `order` is 1 (1.1), applies $\Pi$ **once**
while building the joint; the prediction step applies it again. The effective prior on the first
observation is therefore $\Pi^2\pi$ — invisible here, since $\Pi\pi = \pi$.

**It is not invisible if you call `initialize_known`** (`markov_switching.py:563-574`), the
natural thing to reach for when chaining expanding-window refits (4.3). Verified: seeding
$q = (1 - 10^{-12},\ 10^{-12})$ gives `predicted_marginal_probabilities[:, 0]`
$= (0.98490289,\ 0.01509711)$, exactly $\Pi^2 q$ — not $\Pi q = (0.99195970,\ 0.00804030)$, not
$q$. **Two transition steps are applied, not one**, while the docstring at
`markov_switching.py:120-122` reads as one. Verify the realized
`predicted_marginal_probabilities[:, 0]` against your intent rather than trusting it.

The alternatives (**diffuse initialization**, or free $\xi_{1|0}$) cost parameters or consistency;
ergodic is the only one consistent with the estimated $P$. One last numerical detail reaches the
public contract: Step 2's normalization can return a probability an ULP *above* one, fatal for any
downstream $\sqrt{1-p}$, so `estimate_jump_regimes` clips to $[0,1]$ before returning.

---

## Layer 3 — Maximum likelihood estimation

### 3.1 The objective

$$\hat\theta = \arg\max_{\theta \in \Theta} \ \ell(\theta)
= \arg\max_\theta \sum_{t=1}^{T} \log\!\big(\mathbf 1^{\!\top}(\eta_t(\theta)\odot\xi_{t\mid t-1}(\theta))\big)$$

The filter is the *only* way $\theta$ reaches the objective: `loglikeobs` runs
`self._filter(params)` and returns $(\ell_1,\dots,\ell_T)$ and `loglike` sums it, so every
likelihood evaluation is a full $O(Tk^2)$ filter pass.

Optimizer: BFGS (`markov_switching.py:1028`), with `skip_hessian=True`. Gradients are
**complex-step derivatives**, `approx_fprime_cs` — not finite differences: complex-step
differentiation evaluates $f(x + ih)$ and takes $\operatorname{Im}f/h$, exact to machine
precision *provided $f$ is analytic*, a proviso that is the whole content of Section 8. Because
nothing intercepts the parameter vector, the objective is smooth in every optimizer coordinate,
and `checks.py:124-133` asserts every run that no gradient coordinate is exactly zero and no
inverse-Hessian diagonal entry is still at the BFGS identity value $1.0$.

### 3.2 The constrained ↔ unconstrained reparameterization

BFGS is an unconstrained optimizer and must not be handed a search space where $\sigma^2 < 0$ or
$p \notin [0,1]$ are reachable. statsmodels solves this with a **reparameterization** (a *link
function*, in GLM vocabulary): the optimizer works in $\tilde\theta \in \mathbb R^6$ and every
likelihood evaluation maps $\tilde\theta \mapsto \theta$ first via `transform_params`, with
`untransform_params` running once on the way *out* of setup to convert start values. The repo
overrides neither, and the pair is a genuine mutual inverse — the round trip returns exactly zero
in all six coordinates.

**Transition probabilities** (`markov_switching.py:1444-1449`) go through a multinomial-logistic
**softmax** against a zero baseline, per column of $\Pi$, which for $k=2$ collapses to the plain
**logistic** $p_{i0} = e^{\tilde p_i}/(1 + e^{\tilde p_i})$ with the **logit**
$\log\tfrac{p}{1-p}$ as inverse. **Variances** (`markov_regression.py:384-385`) go through
**squaring**, not logging, so the optimizer's variance coordinate is a *standard deviation*
$\tilde\sigma_j = \pm\sigma_j$; that map is two-to-one, giving the surface a mirror symmetry and
a kink at $\tilde\sigma_j = 0$. **Intercepts** are untouched — already unconstrained, so a
switching mean adds no curvature here.

### 3.3 `search_reps` and the multimodality of the mixture likelihood

`src/jump_model.py:134` passes `search_reps=50`: untransform the base start values, draw 50
perturbations $u_i \sim \mathcal U(-0.5, 0.5)^6$, run 5 EM iterations on each keeping any candidate
that beats the incumbent, then polish the winner with 5 more before BFGS starts.

**Why random restarts are necessary and not defensive coding.** The likelihood of a
finite-mixture or Markov-switching model is **not** globally concave and generically has multiple
local maxima, from three sources all present here. **Label switching** (Section 7) makes the
likelihood *exactly* invariant under permuting regime labels, so every interior mode is
duplicated $k!$ times — for $k=2$, every mode has a twin. **Spurious modes** arise because
driving $\sigma_j^2 \to 0$ with a single observation assigned to regime $j$ sends the density
$\to\infty$: the mixture likelihood is unbounded on the boundary of the parameter space
(Day 1969; Kiefer & Wolfowitz 1956), so any "maximum" you find is a *local interior* maximum and
which one depends on where you start. And **flat ridges** run between high-variance/low-persistence
and moderate-variance/high-persistence configurations. Since `markov_switching.py:1349` draws from
the *global* RNG with no `random_state` hook, `_seeded_numpy_random` (`src/jump_model.py:41-52`)
wraps the fit to keep it deterministic.

**Alternative route: EM / Baum–Welch**, the standard HMM estimator (Baum et al. 1970; Dempster,
Laird & Rubin 1977), whose M-steps are closed-form — the variance step is the
smoothed-probability-weighted second moment
$\hat\sigma_j^2 = \sum_t \xi_{t|T}(j)(r_t - \hat\mu_j)^2 / \sum_t \xi_{t|T}(j)$, the transition
step expected transition counts over expected occupancy. It is monotone in $\ell$ and never
leaves the feasible set but converges only linearly, so statsmodels uses it as a warm-start only:
EM into a good basin, BFGS to finish.

---

## Layer 4 — The Kim smoother

Kim (1994), *Journal of Econometrics* 60(1–2), 1–22; textbook treatment in Kim & Nelson (1999)
ch. 5, cited at `markov_regression.py:80-83`. Equivalent to the HMM **forward–backward
algorithm**, in the "$\gamma$ from $\gamma$" rather than $\beta$-recursion formulation.

### 4.1 What "smoothed" means, precisely

$$\xi_{t\mid T}(j) \;=\; \Pr\!\big(S_t = j \;\big|\; r_1,\dots,r_t,\ \underbrace{r_{t+1},\dots,r_T}_{\text{the future}};\ \hat\theta\big)$$

The conditioning set is the **entire sample** — the whole difference from 2.1.

### 4.2 The backward recursion

Start from the terminal condition $\xi_{T\mid T}$ — the last filtered value, since at $t = T$
there is no future to add. Then recurse **backwards** for $t = T-1, \dots, 1$:

$$\boxed{\ \xi_{t\mid T}(j) \;=\; \xi_{t\mid t}(j)\,\sum_{i}
\frac{p_{ji}\;\xi_{t+1\mid T}(i)}{\xi_{t+1\mid t}(i)}\ }$$

**Derivation** (three lines; the middle is the only place an approximation could enter):

$$\xi_{t\mid T}(j) = \sum_i \Pr(S_t=j, S_{t+1}=i\mid\mathcal F_T)
= \sum_i \Pr(S_{t+1}=i\mid\mathcal F_T)\,\Pr(S_t=j\mid S_{t+1}=i,\mathcal F_T)$$

$$\Pr(S_t=j\mid S_{t+1}=i,\mathcal F_T) \;=\; \Pr(S_t=j\mid S_{t+1}=i,\mathcal F_t)$$

$$\Pr(S_t=j\mid S_{t+1}=i,\mathcal F_t)
= \frac{\Pr(S_t=j\mid\mathcal F_t)\,p_{ji}}{\Pr(S_{t+1}=i\mid\mathcal F_t)}
= \frac{\xi_{t\mid t}(j)\,p_{ji}}{\xi_{t+1\mid t}(i)}$$

The middle step drops $r_{t+1},\dots,r_T$ from the conditioning set. It is valid iff
$\{r_{t+1},\dots,r_T\} \perp S_t \mid S_{t+1}$, which holds **exactly** for a plain HMM where the
emission depends only on the contemporaneous state. Ours does, and `self.order = 0`, so **the Kim
smoother is exact here** — it becomes approximate only for Markov-switching autoregressions,
Kim 1994's caveat, which does not apply to us. Every factor is already available from the forward
pass ($\xi_{t|t}$ from Step 2, $\xi_{t+1|t}$ from Step 1), which is why the smoother costs one
extra $O(Tk^2)$ sweep and no extra filtering. **Log-space form**, matching `cy_kim_smoother_log`
and the log joint arrays retained at `markov_switching.py:214-216`:

$$\log\xi_{t\mid T}(j) = \log\xi_{t\mid t}(j)
+ \operatorname*{logsumexp}_{i}\big[\log p_{ji} + \log\xi_{t+1\mid T}(i) - \log\xi_{t+1\mid t}(i)\big]$$

Sanity check on the terminal condition: `filtered[-1] == smoothed[-1]` exactly.

### 4.3 Why smoothed probabilities are look-ahead bias for a trading signal

**Status: resolved in code.** `estimate_jump_regimes` returns
`results.filtered_marginal_probabilities` (`src/jump_model.py:163`), guarded at
`checks.py:142-149`: the returned series must match the filtered array and must *not* match the
smoothed one. The argument below is why, and the second-order leak it identifies is still open.

Read 4.1 again: $\xi_{t\mid T}$ at week $t$ is computed using weeks $t+1$ through $T$. In a
backtest walking forward through history, the value at 2008-09-15 would be informed by
2008-10-10, 2009-03-06, and every week since. **You cannot have known it at the time**, so any
Sharpe ratio computed from a signal built on $\xi_{t|T}$ is fiction. Measured gap (**real**,
`diagnostics.py:751-759`): $\max_t|\xi_{t|t} - \xi_{t|T}| = 0.704014$, mean $0.109884$, and
**170 of 1750 weeks (9.71%) disagree about the $0.50$ threshold**. Smoothed probabilities are the
*correct* object for retrospective questions — "was 2011-08 a crisis regime?" — and the standard
choice for historical business-cycle dating (Hamilton 1989's original application), but the
*wrong* object for a signal. The synthetic fixture makes the mechanism visible around its true
jump block (weeks 100–109, `checks.py:42`, $j^\star = 1$ here; both series first cross $0.50$ at
week 100):

| week | $\xi_{t\mid t}(j^\star)$ filtered | $\xi_{t\mid T}(j^\star)$ smoothed |
|---|---|---|
| 98 | 0.001810 | 0.035592 |
| 99 | 0.002448 | **0.212773** |
| 100 | 0.998767 | 0.999989 |
| 109 | 1.000000 | 1.000000 |
| 110 | **0.542069** | 0.136462 |
| 111 | 0.116746 | 0.018861 |

- **Week 99** (one week before the true jump): filtered $0.002448$, smoothed $0.212773$ — the
  smoother has already caught an $87\times$ whiff of the crisis from data that had not happened.
  This is anticipation, and on real data with less clean regime edges it is much larger.
- **Week 110** (one week after): filtered $0.542069$, smoothed $0.136462$. The smoother knows calm
  resumed and retroactively suppresses the alarm; the filter, correctly, does not yet know and
  sits just above the coin-flip. Its slower exit is *the honest picture of what you'd have seen*.

**A second, subtler leak survives the fix and is still open.** Returning filtered probabilities
removes the *state* look-ahead but not the *parameter* look-ahead: $\hat\theta$ is still estimated
on the whole sample, and $\hat\sigma_{j^\star}^2$ in particular is largely determined by the worst
weeks in it, so scoring a week before those happened is still cheating. Genuine out-of-sample
evaluation requires **expanding-window (recursive) refitting**: fit on $r_1,\dots,r_s$ only; take
$\xi_{s|s}$ from *that* fit — the last filtered value, which uses no data after $s$ and parameters
that saw none either; record it as the week-$s$ signal; advance, refit, repeat. One full fit per
week, feasible offline, and the only way to get a defensible backtest; the literature term is
**real-time / recursive out-of-sample evaluation** (Chauvet & Piger 2008). Watch three things:
early-window parameter paths are unstable, so set a burn-in well above `MIN_OBSERVATIONS = 10`;
each refit carries its own label-switching risk, so **the jump-regime index must be recomputed per
window**; and `initialize_known` applies $\Pi$ twice.

---

## 5. Model selection

### 5.1 AIC and BIC

$$\text{AIC} = -2\,\ell(\hat\theta) + 2k, \qquad
\text{BIC} = -2\,\ell(\hat\theta) + k\log T$$

`markov_switching.py:1818-1832`, both passing `self.params.shape[0]` as $k$ — i.e. **the length
of the parameter vector**, with no adjustment for restrictions. That count is correct here because
nothing is pinned, which `diagnostics.py:390-403` verifies rather than assumes.

**Three cases worth keeping separate**, because the penalties must count *effective* degrees of
freedom and a parameter fixed by fiat has none. A **point restriction** removes exactly one degree
of freedom. An **inequality restriction** costs nothing while slack and is a boundary case when it
binds — at a binding boundary the limiting distribution is not normal, so no $k$ makes the usual
asymptotics apply. An **ordering constraint** costs nothing at all: it is a labelling
convention, removing a duplicate mode from the likelihood surface rather than a dimension from
the parameter space — the same fact that makes post-hoc relabelling legitimate (7.3).

### 5.2 Testing the number of regimes is a non-standard problem

The obvious move — LR test of $k=1$ against $k=2$, refer $2\Delta\ell$ to $\chi^2_{\nu}$ — **is
invalid**, and not marginally so. Under $H_0: k=1$ the 2-regime model is unidentified three ways
at once:

1. **Nuisance parameters unidentified under the null.** Set $\sigma_0^2 = \sigma_1^2$ and the
   transition probabilities vanish from the likelihood entirely — any values give the identical
   fit, while Wilks' theorem requires all parameters identified under $H_0$.
2. **Parameters on the boundary.** Alternatively reach the null by $\pi_1 \to 0$, a boundary of
   the parameter space; boundary nulls give mixtures of $\chi^2$ at best (Chernoff 1954;
   Self & Liang 1987).
3. **Zero score.** At the null the derivative of $\ell$ in the mixing direction is identically
   zero, so the quadratic expansion around $H_0$ degenerates.

Any one breaks $\chi^2$; all three together mean the LR statistic's null distribution is **not**
$\chi^2$ with any degrees of freedom, and using $\chi^2$ **massively over-rejects** — you will
"find" regimes in i.i.d. Gaussian noise. The same objection applies to $k=2$ versus $k=3$, so the
information-criterion comparison in the status note must not be converted into an LR test. Use
instead **Hansen (1992)**'s empirical-process bound, **the Davies bound** as a cheap conservative
first line of defence, the modern alternatives in Section 9, or a **parametric bootstrap**:
simulate $B$ samples from the fitted 1-regime model, refit both specifications to each, read the
null distribution off the draws. A restriction *within* a fixed number of regimes is by contrast
standard — $H_0: \mu_0 = \mu_1$ is a single point restriction on identified parameters at an
interior point, so $\chi^2_1$ applies (`diagnostics.py:415-424`) — but such a test asks about the
*contrast*, not either coefficient's own significance.

---

## 6. Residual diagnostics that do apply

### 6.1 Regime-standardized residuals

The specification says $r_t = \mu_{S_t} + \sigma_{S_t}\varepsilon_t$ with $\varepsilon_t$ i.i.d.
$\mathcal N(0,1)$, so the object to test is $z_t = (r_t - \hat\mu_{S_t})/\hat\sigma_{S_t}$, which
under correct specification is i.i.d. standard normal. Note the numerator: with a switching mean,
subtracting a single sample mean is wrong and manufactures skew. **Hard classification** takes
$\hat S_t = \arg\max_j \xi_{t|t}(j)$ and standardizes by that regime's moments — simple, discards
classification uncertainty, and is the primary version reported (`diagnostics.py:545-546`). The
**probability-weighted** alternative standardizes by the moments of the *mixture*, which with a
switching mean means the law of total variance,
$v_t = \sum_j \xi_{t|t}(j)(\hat\sigma_j^2 + \hat\mu_j^2) - m_t^2$ with
$m_t = \sum_j \xi_{t|t}(j)\hat\mu_j$ — not the shortcut $v_t = \sum_j \xi_{t|t}(j)\hat\sigma_j^2$,
which understates the variance whenever the regime is uncertain *and* the means differ. Its $z_t$
is not exactly standard normal even under correct specification, so test it against a simulated
reference. Build $z_t$ from $\xi_{t|T}$ for the retrospective, from $\xi_{t|t}$ for the *signal*.

### 6.2 Normality: QQ plot and Jarque–Bera

$$\text{JB} = \frac{T}{6}\left(\widehat{\text{skew}}^2 + \frac{(\widehat{\text{kurt}} - 3)^2}{4}\right)
\;\xrightarrow{d}\; \chi^2_2 \quad\text{under } H_0:\ z_t \sim \mathcal N$$

Jarque & Bera (1980). Read the QQ plot alongside it — JB gives one number, the QQ plot tells you
*where* the failure is, and here the informative region is the tails. A QQ plot straight in the
body that bends only in the extreme left tail means the two-variance mixture handles ordinary
weeks but not genuine tail events; the fix is Student-$t$ emissions, not a third regime. Raw
returns are *supposed* to be leptokurtic — that is the mixture doing its job — so only $z_t$
should be normal, and if it is still fat-tailed the extension is a **Markov-switching model with
$t$-distributed innovations** (Klaassen 2002). **Real:**
JB $= \mathbf{28.285}$, $p = 7.21\times10^{-7}$, $n = 1750$ — **rejected**. Switching absorbs the
overwhelming majority of the raw non-normality, excess kurtosis falling from $8.078$ to $0.476$,
but what remains is a decisive left skew: the QQ table puts the right tail close to the Normal
line while the left runs long.

### 6.3 Ljung–Box on $z_t$: leftover serial correlation in the level

$$Q(m) = T(T+2)\sum_{h=1}^{m}\frac{\hat\rho_h^2}{T-h} \;\xrightarrow{d}\; \chi^2_m$$

Ljung & Box (1978), on the sample autocorrelations of $z_t$; $H_0$ is no autocorrelation up to
lag $m$. Rejection means predictable *level* dynamics the model omits, and the extension is a
Markov-switching AR (`MarkovAutoregression`, which sets `order > 0` and makes the Kim smoother
approximate rather than exact, per 4.2). Weekly equity returns rarely reject this; if yours does
at short lags, suspect the data pipeline (overlapping or misaligned weekly bars) before the model
— here every index spacing is exactly 7 days over all 1750 weeks. **Real:**
$Q(4) = 17.480\ (p = 0.00156)$ through $Q(26) = 39.176\ (p = 0.0469)$, **rejecting at every lag
reported** but far milder than the squared-residual failure below ($17.5$ versus $70.0$): the
level is a nuisance, the variance is the problem.

### 6.4 ARCH-LM on $z_t$: the diagnostic that decides this model's fate

Engle (1982). Regress the squared standardized residual on its own lags:

$$z_t^2 = \alpha_0 + \sum_{k=1}^{q}\alpha_k z_{t-k}^2 + u_t,
\qquad \text{LM} = T R^2 \;\xrightarrow{d}\; \chi^2_q
\quad\text{under } H_0:\ \alpha_1=\dots=\alpha_q=0$$

`statsmodels.stats.diagnostic.het_arch`, `diagnostics.py:214-220`. Ljung–Box on $z_t^2$ tests the
same hypothesis with a different statistic; report both, they rarely disagree. **Real:**
ARCH-LM$(4) = \mathbf{55.652}$ ($p = 2.372\times10^{-11}$), ARCH-LM$(12) = \mathbf{78.830}$
($p = 6.897\times10^{-12}$), Ljung–Box$(4)$ on $z_t^2 = \mathbf{69.955}$
($p = 2.320\times10^{-14}$). The same statistics on *raw* returns are $231.85$ and $350.06$, so
the model absorbs roughly 76–80% of the volatility clustering and leaves a remainder that is
still overwhelmingly significant.

**Why this is the sharpest test of the whole specification.** The model asserts that conditional
volatility takes exactly **two discrete values** — a step function. The competing hypothesis is
that volatility moves on a **continuum**, drifting and clustering *within* what this model calls a
single regime; if that is true, dividing by a constant $\hat\sigma_j$ across an entire episode
leaves the clustering intact and $z_t^2$ stays autocorrelated. ARCH-LM is therefore a direct test
of *are two variance levels enough, or is volatility continuous?* — the only diagnostic in this
list that asks it. A third regime makes the step function finer without making it a continuum; the
relevant literature is the long-running **regime-switching versus GARCH** debate, in Section 9.

### 6.5 Two diagnostics specific to regime-switching models

**Regime classification measure (RCM).** Ang & Bekaert (2002). For $k$ regimes,
$\text{RCM} = 100\,k^k\,\frac{1}{T}\sum_t\prod_j \xi_t(j)$; for $k=2$,
$\text{RCM} = \frac{400}{T}\sum_t \hat p_t(1 - \hat p_t)$. Zero = perfectly sharp classification,
100 = no information. A thermostat whose probabilities hover in the 21–60% "building stress" band
(`README.md:47`) has a high RCM, and RCM tells you whether that is the *market* being ambiguous or
the *model* being uninformative. Computed on **filtered** probabilities, matching the signal:
RCM $= 3.47$ on the synthetic fixture, **$33.53$ on real data** — a third of the way to
uninformative. **Duration realism** is the second: fitted $1/(1-\hat p_{ii})$ against the
empirical run-length distribution of $\hat S_t$ (1.5).

**A limitation of `checks.py` worth stating once.** Its fixture is drawn from exactly the model
being fitted, so every diagnostic here passes on it (JB $p = 0.500$, ARCH-LM(4) $p = 0.170$) while
the same tests reject at $p < 10^{-6}$ on real data — which is why `diagnostics.py` exists
separately.

---

## 7. Identifiability and label switching

### 7.1 The problem

The likelihood of a mixture or Markov-switching model is **invariant to permutation of the regime
labels**. Relabel $0 \leftrightarrow 1$ *everywhere consistently* — swapping **both** regime-
specific parameter pairs **and** transpose-permuting the transition matrix — and $\ell$ is
identical. For $k=2$ the permuted vector is

$$\theta' = (\,p_{11},\ p_{01},\ \mu_1,\ \mu_0,\ \sigma_1^2,\ \sigma_0^2\,)
\qquad\text{i.e.}\qquad p'_{00} = 1 - p_{10},\quad p'_{10} = 1 - p_{00}$$

Verified on the synthetic fit: `loglike(theta)` and `loglike(theta')` are both
$475.3432711040538834$, difference exactly $0.0$ — not close, **bit-identical**. This is exact
algebraic invariance, not numerical coincidence: the permutation acts on the filter's state
indices, and every sum in 2.2's recursion is over all states.

Consequences: the likelihood has $k! = 2$ global maxima; regime *indices* carry no meaning without
an extra convention; and any statement of the form "regime 1 is the jump regime" is a claim that
must be **derived from the fit**, never assumed. The canonical reference is
Frühwirth-Schnatter (2006), *Finite Mixture and Markov Switching Models*, ch. 3 and ch. 3.7 / 11.
The Markov structure does **not** rescue identifiability; it only makes the *model* identified up
to permutation, which is why a labelling convention suffices and priors are not needed.

### 7.2 Standard remedies

| Remedy | Mechanism | Trade-off |
|---|---|---|
| **Ordering (identifiability) constraint** | Restrict $\Theta$ to one representative per permutation orbit, e.g. $\sigma_0^2 \le \sigma_1^2$ | Standard and clean *if* implemented smoothly, i.e. as a reparameterization. Choose the ordering variable that actually separates the regimes — here, variance. Frühwirth-Schnatter (2006) §3.2 |
| **Post-hoc relabelling** | Estimate freely; permute the fitted output so the higher-variance regime is the jump regime | **What this repo does** (7.3). Trivially correct for MLE: one fit, one permutation, no effect on the optimization |

Two further remedies are Bayesian only: **random-permutation sampling** (permute labels each MCMC
sweep, then relabel the draws — k-means in parameter space, or Stephens 2000) and
**order-imposing priors** (Frühwirth-Schnatter 2006, ch. 3.7).

### 7.3 Post-hoc relabelling — the repo's identification strategy

**The code.** `_jump_regime_index` (`src/jump_model.py:96-105`) reads `sigma2[0]` and `sigma2[1]`
off the fitted vector and returns `argmax`; `fit_jump_model` returns it as the third element of
`(model, results, jump_regime_index)` and `estimate_jump_regimes` uses it to select the column.
It runs once, after `fit()`, and touches nothing the optimizer sees.

**Why that is the correct place to resolve it.** (1) The likelihood is exactly invariant to a
joint permutation of the transition matrix and both regime-specific parameter pairs (7.1).
(2) Therefore labelling is a naming indeterminacy, not a restriction on the model — $\theta$ and
$\theta'$ are two names for the same distribution over $(r_1,\dots,r_T)$, so a "constraint" that
picks one does not narrow the set of distributions under consideration, it chooses a coordinate
chart. (3) Therefore resolve it after fitting: there is no wrong basin to keep the optimizer out
of, since both have the same height. Because nothing then intercepts $\theta$, the fitted point is
an ordinary **interior stationary point of $\ell$ in the full 6-dimensional parameter space** —
the precondition for standard MLE inference, and what makes `res.bse` and `res.conf_int()`
legitimate.

**The one operational hazard.** The index is data-dependent, so it must be recomputed for every
fit and never cached. On the synthetic fixture $j^\star = 1$; on real SPY full history and on the
2006–2011 window $j^\star = 0$. A hardcoded index would have inverted the signal on live data —
maximum insurance in calm markets, none in crises — while every check in `checks.py` continued to
pass, because the fixture happens to land the other way. Relabelling says nothing, though, about
whether $k=2$ is right, whether the emissions are Gaussian, or whether the higher-variance regime
deserves the name "jump".

---

## 8. Audit record — the superseded constrained specification

Until 2026-08-12 the repo fitted a `ConstrainedMarkovRegression` subclass that, inside
`transform_params`, pinned $p_{00} = 0.98$, floored $p_{10}$ at $0.15$ (capping jump persistence at
$0.85$), and `sorted()` the two variances on every likelihood evaluation. It was deleted:

- **Projection, not reparameterization.** The constraint operator was idempotent but not injective,
  so `transform_params ∘ untransform_params` was a retraction rather than the identity, and
  `min`/`max` put a kink in an objective BFGS assumes is $C^2$.
- **The complex-step gradient was invalidated, not merely degraded.** NumPy orders `complex128`
  lexicographically, so at a variance tie `sorted()` broke the tie on the *imaginary* (perturbation)
  part and credited the derivative to the wrong coordinate; `max(complex, float)` discarded it.
- **The failure looked exactly like success.** `gopt[0]` was exactly `-0.0` and `Hinv[0,0]` exactly
  `1.0` — the untouched BFGS identity initialization — with `warnflag = 0`. A convergence flag
  cannot detect a coordinate the optimizer never explored; `checks.py:124-133` now asserts on both.
- **Standard errors described an unfitted model.** `cov_params_approx` calls
  `hessian(params, transformed=True)`, which bypasses `transform_params` — the one method the
  constraints lived in — so `bse` and `conf_int()` belonged to a different, unrestricted model at a
  non-stationary point. The parameter count was overstated for the same reason (5.1).
- **The constraints jointly forbade what the data showed.** Pinning $p_{01} = 0.02$ while flooring
  $p_{10} \ge 0.15$ capped the ergodic jump frequency at $11.76\%$ of weeks against a measured
  filtered share of $13.77\%$, and the $6.667$-week duration ceiling made 2008 inexpressible.

Full evidence is in `core-risk-overlay.md`; the deleted code is in `git log`, at the commit
preceding the respecification.

---

## 9. Annotated further reading

**Founding papers — read these two first, in this order.** **Hamilton (1989)**, *Econometrica*
57(2), 357–384 → §2–3 for Section 2's filter derivation and the original switching-*mean*
specification; also the source of the "smoothed probabilities for historical dating" convention
this repo inherited without its caveat (4.3). **Kim (1994)**, *J. Econometrics* 60(1–2), 1–22
→ the backward recursion of 4.2, including when it is exact and when not.

**Textbooks — for when a paper assumes something you don't have.** **Hamilton (1994)**, *Time
Series Analysis*, ch. 22 → the cleanest single exposition of filter + smoother + MLE; start here
if the 1989 notation fights you. **Kim & Nelson (1999)**, *State-Space Models with Regime
Switching* → what statsmodels implements, ch. 4–5 mapping onto `markov_switching.py` almost line
for line. **Frühwirth-Schnatter (2006)**, *Finite Mixture and Markov Switching Models* → ch. 1–3
identifiability, §3.2 ordering constraints, ch. 3.7 / 11 label switching; the authority for
Section 7. **McLachlan & Peel (2000)**, ch. 2–3 → why the mixture likelihood is unbounded and
multimodal, the theory behind `search_reps` (3.3).

**Estimation machinery.** Dempster, Laird & Rubin (1977), *JRSS-B* 39(1) → EM and why the M-steps
are weighted moments; Baum, Petrie, Soules & Weiss (1970), *Ann. Math. Stat.* 41(1) → the
HMM-specific "Baum–Welch"; **Rabiner (1989)**, *Proc. IEEE* 77(2) → the most readable derivation
of forward–backward anywhere; read §V if 2.3 feels opaque.

**Testing for regimes — 5.2.** **Hansen (1992)**, "The Likelihood Ratio Test under Nonstandard
Conditions", *JAE* 7(S1), S61–S82 → the canonical treatment of why your LR test is invalid and
what bound to use instead; read the introduction even if you skip the empirical-process
machinery. **Davies (1987)**, *Biometrika* 74(1), 33–43 (also Davies 1977) → the upcrossing
bound, the cheapest correct thing you can actually compute. Then **Garcia (1998)**, *IER* 39(3)
→ the Markov-switching-specific null distribution; **Cho & White (2007)**, *Econometrica* 75(6)
→ quasi-LR test; **Carrasco, Hu & Ploberger (2014)**, *Econometrica* 82(2) → an asymptotically
optimal test computable without fitting the switching model, the most practical of the group.

**Regimes versus GARCH — 6.4.** **Hamilton & Susmel (1994)**, *J. Econometrics* 64(1–2), 307–333
→ SWARCH, an ARCH process whose scale shifts with a latent regime; the direct answer to a
rejecting ARCH-LM, and worth reading before considering a third regime, since the failure is
step-function-versus-continuum. **Gray (1996)**, *JFE* 42(1) → tractable regime-switching GARCH
and the path-dependence that makes the exact version infeasible; **Haas, Mittnik & Paolella
(2004)**, *JFEc* 2(4) → modern MS-GARCH, the practical choice if you go this route;
**Cai (1994)**, *JBES* 12(3) → the other simultaneous SWARCH paper.
**Lamoureux & Lastrapes (1990)**, *JBES* 8(2), 225–234 (and Diebold 1986) → the reverse argument,
that ignoring regime shifts inflates GARCH persistence; read it so you do not conclude "GARCH is
better" from one failing diagnostic. **Ang & Timmermann (2012)**, *ARFE* 4 → survey.

**Real-time evaluation and diagnostics.** **Chauvet & Piger (2008)**, *JBES* 26(1), 42–49 → the
closest published analogue to this repo's central question, how much apparent skill survives
real-time evaluation; read before building the expanding-window backtest (4.3).
**Ang & Bekaert (2002)**, *JBES* 20(2) → source of the RCM statistic (6.5). Engle (1982),
*Econometrica* 50(4) → ARCH-LM (6.4); Ljung & Box (1978), *Biometrika* 65(2) → 6.3;
Jarque & Bera (1980), *Economics Letters* 6(3) → 6.2.

---

## 10. Glossary — symbols, code names, and literature terms

**Symbols and their statsmodels names** are in the Notation table near the top, which is canonical
and not restated. Three attributes it omits: $p_{01}$ and $p_{11}$ are *not* parameters, being
$1-p_{00}$ and $1-p_{10}$ (`tm[1,0,0]`, `tm[1,1,0]`); $E[D_i]$ is `res.expected_durations`; and
$\mathcal T$ is statsmodels' own `transform_params`, which the repo does not override.

**Literature terms used above, with the section that uses them.**

| Term | Meaning | § |
|---|---|---|
| Markov-switching model / HMM | Latent discrete state drives parameters of an observed process; here with Gaussian emissions, making the marginal law a **location–scale mixture of normals** | 0.1, 1.4 |
| Left-stochastic matrix | Columns sum to 1; statsmodels' $\Pi$, the transpose of the usual $P$ | 1.2 |
| Ergodic / stationary distribution | $\Pi\pi = \pi$; long-run occupancy (Perron–Frobenius). **Steady-state initialization** sets $\xi_{1\mid 0} = \pi$ | 1.4, 2.4 |
| Hamilton filter / forward algorithm | Forward recursion for $\xi_{t\mid t}$ and $\ell_t$; Chapman–Kolmogorov propagation | 2, 2.2 |
| Prediction-error decomposition | $f(r_1..r_T) = \prod_t f(r_t\mid\mathcal F_{t-1})$; makes MLE $O(Tk^2)$ | 2.2 |
| logsumexp | $\log\sum e^{x_i}$, max-shifted; makes the recursion overflow-safe | 2.3 |
| Kim smoother / forward–backward | Backward recursion for $\xi_{t\mid T}$ | 4 |
| Look-ahead bias | Using data unavailable at decision time; cured by real-time (recursive) out-of-sample refitting | 4.3 |
| Reparameterization / link function | Bijection from $\mathbb R^k$ to a constrained $\Theta$; here softmax and squaring, and a **projection/retraction** is what you get when it is done wrong | 3.2, 8 |
| Complex-step differentiation | Exact gradient via $\operatorname{Im}f(x+ih)/h$; requires $f$ analytic — as BFGS requires $C^2$ | 3.1, 8 |
| EM / Baum–Welch | Monotone iterative MLE for latent-variable models; warm-start only here. The mixture likelihood it climbs is **unbounded** — $\sigma_j^2\to0$ on one point sends the density to $\infty$ — hence multimodal | 3.3 |
| Label switching | Likelihood invariant to permuting regime labels; an **ordering constraint** picks one representative per permutation orbit | 7.1, 7.2 |
| **Post-hoc relabelling** | Estimate freely, name the regimes afterwards; the repo's strategy, legitimate because labelling is a **naming indeterminacy** — it indexes coordinates, not distributions | 7.2, 7.3 |
| Interior stationary point | $\nabla\ell = 0$ inside $\Theta$; precondition for Hessian-based inference. A **boundary solution** has a non-normal limiting distribution | 3.1, 7.3, 8 |
| Nuisance parameter unidentified under the null | Why the LR test for $k$ is non-standard; Davies bound | 5.2 |
| ARCH-LM test | $TR^2$ from regressing $z_t^2$ on its lags; tests leftover vol clustering | 6.4 |
| Regime-standardized residual | $z_t = (r_t-\hat\mu_{S_t})/\hat\sigma_{S_t}$; should be i.i.d. $\mathcal N(0,1)$. Its probability-weighted variant uses the **law of total variance** | 6.1 |
| RCM (regime classification measure) | $0$ = sharp classification, $100$ = uninformative | 6.5 |
| SWARCH / MS-GARCH | Regime switching combined with within-regime GARCH | 6.4 |
| Jump-diffusion | Continuous-time diffusion + compound Poisson jumps. **Not this model.** | 0.1 |
