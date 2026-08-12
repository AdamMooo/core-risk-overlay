# Math Reference — 2-Regime Markov-Switching Volatility Model

Last updated: 2026-08-12 (revised the same day, after the model was respecified: the constrained
subclass was deleted and replaced by a plain `MarkovRegression` with a switching mean and
post-hoc regime relabelling)

Companion to `src/jump_model.py`. Written to be re-read: every equation is tied to the line of
code it becomes, and every technique is named with its standard-literature term so you can go
read the primary source.

**Scope.** The estimator actually fitted in this repo is `statsmodels`' `MarkovRegression` with
`k_regimes=2, trend="c", switching_trend=True, switching_variance=True`, on weekly SPY
log returns (`src/jump_model.py:125-131`). No subclass, no overrides, no restrictions: six free
parameters, all estimated. Which of the two fitted regimes is the "jump" regime is decided
**after** the fit, by whichever carries the larger variance (`_jump_regime_index`,
`src/jump_model.py:96-105`).

**Specification history.** Until 2026-08-12 this repo fitted a `ConstrainedMarkovRegression`
subclass with `switching_trend=False`, which pinned $p_{00} = 0.98$, capped jump-regime
persistence at $0.85$, and sorted the two variances inside `transform_params` on every
likelihood evaluation. That specification was **replaced on 2026-08-12** after real-SPY
diagnostics rejected it on four independent axes — the pin was LR-rejected, the persistence
ceiling bound exactly, the two constraints jointly made the observed crisis frequency
mathematically unrepresentable, and the constraints' stated rationale turned out to be false on
the data. The evidence is in `core-risk-overlay.md` ("Real-data verdict — 2026-08-12"); the
*mathematics* of why the mechanism was defective — the corrupted complex-step gradient, the
non-invertible transform, the standard errors belonging to an unfitted model — is preserved
below in Sections 1.4, 1.5, 3.3, 3.5, 5.1–5.2, 7.4 and 8.1, all explicitly marked as audit
records of superseded code. Those sections are the most valuable content in this document; they
are kept because the failure mode generalizes, not because the code still exists. The deleted
code is recoverable from git history, at the commit preceding the respecification
(`git show <that-commit>:src/jump_model.py`).

**Code path conventions used below.** Repo files are relative to the repo root
(`src/jump_model.py:105`). Library files live in
`.venv/Lib/site-packages/statsmodels/tsa/regime_switching/` and are referenced by basename:
`markov_switching.py:110`, `markov_regression.py:191`. Line numbers verified against
statsmodels as vendored in this `.venv`.

**Worked numbers.** Unless labelled otherwise, every numeric example below comes from the
deterministic synthetic fit in `checks.py:37-46` (100 calm weeks, 10 jump weeks, 40 calm weeks;
$T = 150$), fitted with `DEFAULT_RANDOM_SEED = 20260811`. It reproduces without a network call.
Figures from the real SPY fit (1993-02-01 .. 2026-08-10, $T = 1750$, produced by
`diagnostics.py` off the `data/spy_weekly.csv` cache) are labelled **real**. Figures produced by
the superseded constrained specification are labelled **historical (superseded spec)** — no
current code path reproduces them.

**One warning about the synthetic fixture.** On the synthetic data the jump regime lands on
index **1**; on every real-data fit it lands on index **0**. That is not a bug, it is the
identification problem of Section 7 doing exactly what the theory says it does. Never carry a
regime index between fits.

---

## Notation

Fixed for the whole document. Do not read any symbol differently in a later section.
(This table is unnumbered so that "Section 1.x" always means a Layer 1 subsection.)

| Symbol | Meaning | statsmodels name | Where |
|---|---|---|---|
| $t$ | time index, $t = 1,\dots,T$; weekly | — | `src/data_loader.py:111` |
| $T$ | sample length ($T = 150$ synthetic) | `nobs` | `markov_switching.py:516` |
| $r_t$ | weekly log return, $\log(P_t/P_{t-1})$ | `endog` | `src/data_loader.py:111` |
| $\mathcal F_t$ | information set $\{r_1,\dots,r_t\}$ | — | — |
| $S_t$ | latent regime, $S_t \in \{0,1\}$; labels carry no meaning until Section 7.3 | — | `src/jump_model.py:7` |
| $j^\star$ | the **jump** regime index, $= \arg\max_j \hat\sigma_j^2$, decided after the fit | `jump_regime_index` | `src/jump_model.py:96-105` |
| $p_{ij}$ | $\Pr(S_t = j \mid S_{t-1} = i)$ — **row = from, column = to** | `p[i->j]` | `markov_switching.py:1405-1408` |
| $P$ | $2\times2$ row-stochastic matrix with $P_{ij} = p_{ij}$ | — | — |
| $\Pi$ | $P^{\!\top}$, the left-stochastic matrix statsmodels builds | `regime_transition_matrix` | `markov_switching.py:632-664` |
| $\pi$ | ergodic (stationary) distribution, column vector, $\Pi\pi = \pi$ | `initial_probabilities` | `markov_switching.py:576-602` |
| $\mu_j$ | regime-$j$ intercept; **switches** since 2026-08-12 | `const[j]` | `markov_regression.py:106-108`, `342-345` |
| $\sigma_j^2$ | variance in regime $j$; **unrestricted** | `sigma2[j]` | `markov_regression.py:350-352` |
| $\theta$ | parameter vector $(p_{00},\,p_{10},\,\mu_0,\,\mu_1,\,\sigma_0^2,\,\sigma_1^2)\in\mathbb R^6$ | `params` | `markov_switching.py:1388-1410` |
| $\tilde\theta$ | optimizer-space (unconstrained-link) vector | — | `markov_switching.py:1412-1453` |
| $\eta_t(j)$ | conditional density $f(r_t \mid S_t = j;\theta)$ | `conditional_loglikelihoods` (logged) | `markov_regression.py:190-191` |
| $\xi_{t\mid t-1}$ | **predicted** probs, $\Pr(S_t = \cdot \mid \mathcal F_{t-1})$ | `predicted_marginal_probabilities` | `markov_switching.py:1583-1591` |
| $\xi_{t\mid t}$ | **filtered** probs, $\Pr(S_t = \cdot \mid \mathcal F_t)$ | `filtered_marginal_probabilities` | `markov_switching.py:174` |
| $\xi_{t\mid T}$ | **smoothed** probs, $\Pr(S_t = \cdot \mid \mathcal F_T)$ | `smoothed_marginal_probabilities` | `markov_switching.py:300-303` |
| $\ell_t$ | per-period log-likelihood contribution $\log f(r_t\mid\mathcal F_{t-1})$ | `joint_loglikelihoods` | `markov_switching.py:180-181` |
| $\ell(\theta)$ | total log-likelihood $\sum_t \ell_t$ | `llf` | `markov_switching.py:1902-1907` |
| $z_t$ | regime-standardized residual $(r_t - \hat\mu_{S_t})/\hat\sigma_{S_t}$ | — | `diagnostics.py:545-546` |
| $k$ | number of free parameters | `k_params` | `markov_switching.py:541-546` |
| $\odot$ | elementwise (Hadamard) product | — | — |
| $\mathbf 1$ | column vector of ones | — | — |

**The one notational trap in this codebase.** $p_{ij}$ above is *from $i$ to $j$*, matching the
statsmodels *parameter name* `p[i->j]`. But the *matrix* statsmodels constructs is the transpose:
`regime_transition_matrix(params)[i, j, 0]` $= \Pr(S_t = i \mid S_{t-1} = j) = p_{ji}$
(`markov_switching.py:643-648`). Columns sum to one, not rows. So $\Pi = P^{\!\top}$. Section 1.2
works this through explicitly; it is the reason `diagnostics.py:145` slices
`model.regime_transition_matrix(results.params)[:, :, 0]` and then reads $p_{ii}$ off the
*diagonal* only (`diagnostics.py:172`, `602-605`), where the row/column ambiguity cannot bite.

---

## Layer 0 — What kind of model this actually is

### 0.1 `MarkovRegression` is a class name, not a model name

You are not fitting a regression. `MarkovRegression` is statsmodels' name for a family; the
family member you instantiated has **no exogenous regressors**. `exog=None` at
`src/jump_model.py:125-131`, and `trend="c"` merely prepends a column of ones
(`markov_regression.py:106-108`). The design matrix is $\mathbf 1$ and nothing else — but with
`switching_trend=True` that single column gets a *separate* coefficient per regime.

Drop the regressors from the general form and you get:

$$r_t = \mu_{S_t} + \varepsilon_t, \qquad \varepsilon_t \mid S_t = j \;\sim\; \mathcal N(0, \sigma_j^2),
\qquad S_t \text{ a 2-state Markov chain}$$

The literature names for this object, in decreasing generality:

- **Markov-switching model** / **regime-switching model** — the econometrics umbrella term.
- **Hidden Markov model (HMM) with Gaussian emissions** — the statistics/ML term. Discrete
  latent state, continuous observation, first-order Markov transitions. Exactly that.
- **Markov-switching mean and variance model.** With both $\mu_j$ and $\sigma_j^2$ switching,
  this is Hamilton (1989)'s original specification (switching mean) *plus* the
  financial-econometrics switching-variance extension. Before 2026-08-12 the repo fitted only
  the latter, whose precise name is **Markov-switching heteroskedasticity**; that term no longer
  describes this model.
- **Two-component location–scale mixture of normals with Markov-dependent mixing** — the
  mixture-model reading. The *marginal* distribution of $r_t$ is a two-component normal mixture
  with weights $\pi$ (Section 1.4); the Markov chain adds serial dependence to which component
  is drawn. It was a pure *scale* mixture under the superseded common-mean spec.

Any of those four is a correct thing to type into a search bar. "Markov regression" is not.

**Why one name covers two things.** Hamilton (1989) introduced, in one paper, (a) the
econometric specification and (b) the forward recursion that evaluates its likelihood. The
model and the filter therefore share the name "Hamilton". `markov_regression.py` implements the
model; `cy_hamilton_filter_log` at `markov_switching.py:110-231` implements the filter. Two
different objects, one surname.

### 0.2 One more naming correction

`README.md:15` calls this a "jump-diffusion" model. It is not one. A jump-diffusion
(Merton 1976) is a continuous-time process with a diffusion term plus a **compound Poisson**
jump term, where jumps are instantaneous and independent across time. This model has no
diffusion, no Poisson process, and its "jumps" are *persistent states* lasting several weeks.
It is a Markov-modulated Gaussian process — a discrete-time proxy for elevated volatility, not
for jump arrivals. (The docstring at `src/jump_model.py:114-120` no longer repeats the claim;
`README.md` still does.)

That is fine as a design choice (the mandate at `README.md:14` bans point processes outright),
but keep the name straight or you will read the wrong literature.

### 0.3 Why classical regression diagnostics do not transfer

| Regression diagnostic | Why it is vacuous or inverted here |
|---|---|
| Linearity of $E[y\mid x]$ | There is no $x$. Nothing to be linear in. |
| Residual-vs-fitted plot | `fittedvalues` is the probability-weighted conditional mean (`markov_switching.py:1880-1885`). Since `switching_trend=True`, `predict_conditional` now returns a *different* constant per regime (`markov_regression.py:164-168`) — verified: the two rows are $0.00057463$ and $-0.02935889$ on the synthetic fit — so `model.predict(params)` takes $T$ distinct values instead of one. It is nonetheless not a regression fitted value: it is $\sum_j \xi_{t\mid t}(j)\hat\mu_j$, i.e. a monotone re-reading of the regime probability. Plotting residuals against it plots them against the signal. (**Historical (superseded spec):** with a common mean it was the single constant $0.00035796$ for all $t$ — one vertical strip of points.) |
| Homoscedasticity | **Deliberately violated.** Heteroskedasticity is the signal being estimated, not a nuisance to be tested away. A Breusch–Pagan or White test rejecting is the model working. |
| $R^2$ | Undefined/meaningless. There is no variation being explained by covariates. |
| Normality of raw residuals $r_t - \bar r$ | Guaranteed to fail. The raw residual is by construction a two-component location–scale mixture, hence leptokurtic and skewed. Testing it tests the specification's *premise*, not its fit. **Real:** JB $= 4983.75$, excess kurtosis $8.078$, skew $-0.879$ (`diagnostics.py:302-303`). |
| DW / Ljung–Box on raw residuals | Confounds regime persistence with genuine serial correlation in returns. |

What replaces them (all developed in Section 6):

1. **Regime-standardized residuals** $z_t = (r_t - \hat\mu_{S_t})/\hat\sigma_{S_t}$, which
   *should* be i.i.d. $\mathcal N(0,1)$ if the specification is right. Normality (Jarque–Bera,
   QQ), Ljung–Box on $z_t$, and ARCH-LM on $z_t$ all apply to $z_t$ and only to $z_t$.
   Implemented at `diagnostics.py:545-551`, run in section D of that script.
2. **Regime classification sharpness** — the RCM statistic of Ang & Bekaert (2002),
   `diagnostics.py:560-562`.
3. **Duration realism** — fitted $1/(1-p_{ii})$ against observed run lengths,
   `diagnostics.py:594-644`.
4. **Out-of-sample / pseudo-real-time evaluation** — Section 4.3. This is the diagnostic that
   actually matters for a trading signal, has no regression analogue, and is the one thing on
   this list the repo still does not do.

---

## Layer 1 — The model

### 1.1 Complete specification

State space: $S_t \in \{0, 1\}$, $t = 1,\dots,T$.

**Transition law** (first-order, time-homogeneous — the `tvtp` branch at
`markov_switching.py:604-630` is unused because `exog_tvtp=None`):

$$\Pr(S_t = j \mid S_{t-1} = i, S_{t-2}, \dots, \mathcal F_{t-1}) = \Pr(S_t = j\mid S_{t-1}=i) = p_{ij}$$

**Observation (emission) law:**

$$r_t \mid S_t = j \;\sim\; \mathcal N(\mu_j,\ \sigma_j^2), \qquad
\eta_t(j) \;=\; \frac{1}{\sqrt{2\pi\sigma_j^2}}\,
\exp\!\left(-\frac{(r_t-\mu_j)^2}{2\sigma_j^2}\right)$$

**Both** the mean and the variance carry the subscript $j$ (`switching_trend=True`,
`switching_variance=True`, `src/jump_model.py:129-130`). This is the 2026-08-12 change: the
superseded spec shared one $\mu$ across regimes, so the conditional density depended only on
$(r_t - \hat\mu)^2$ and the sign of the return was invisible. It now enters through $\mu_j$.

How much that buys is an empirical question with a measured answer, and the answer is
"less than you would hope". **Real:** $\hat\mu_{j^\star} = -0.2597\%$/wk versus
$\hat\mu_{\text{calm}} = +0.3635\%$/wk, a spread of $0.623\%$/wk, against
$\hat\sigma_{j^\star} = 3.8375\%$/wk. The location term shifts the density centre by
$0.16$ jump-regime standard deviations while the scale term changes the density by a factor of
$2.56$ in $\sigma$; the squared-deviation term still dominates. Section 7.5 quantifies the
residual sign-blindness; Section 8.3 records it as an open finding.

**Implementation.** `markov_regression.py:190-191` computes $\log\eta_t(j)$ directly:

```
conditional_loglikelihoods = -0.5 * resid**2 / variance - 0.5 * np.log(2*np.pi*variance)
```

Term-by-term: `resid` is $r_t - \mu_j$ from `_resid` (`markov_regression.py:172-175`), which is
`endog` minus `predict_conditional`. That function loops over regimes and dots the design matrix
with **that regime's** coefficient block, `params[self.parameters[i, 'exog']]`
(`markov_regression.py:164-168`) — with `switching_trend=True` those blocks are disjoint, so the
returned rows are $\mu_0$ and $\mu_1$ (verified: $0.00057463$ and $-0.02935889$ on the synthetic
fit; under the superseded common-mean spec both rows were identical). `variance` is
$\sigma_j^2$ reshaped to broadcast over the regime axis (`markov_regression.py:186-188`). So
`-0.5*resid**2/variance` $= -\tfrac{(r_t-\mu_j)^2}{2\sigma_j^2}$ and
`-0.5*np.log(2*np.pi*variance)` $= -\tfrac12\log(2\pi\sigma_j^2)$. There is no third term:
the log-density is written out longhand, no `scipy.stats` call.

**Implementation subtlety worth knowing.** That array still has shape `(2, 2, T)`, not `(2, T)`
— verified on the current fit, and the two slices along axis 1 remain bit-identical. `_resid`
(`markov_regression.py:173-174`) repeats the prediction across a redundant $S_{t-1}$ axis, so
the filter runs on the *pairwise* joint $\Pr(S_t, S_{t-1}\mid\cdot)$ even though the emission
depends on $S_t$ alone. Inside `cy_hamilton_filter_log` the local variable
`order = conditional_loglikelihoods.ndim - 2` therefore equals **1** while `model_order`
(`self.order`) is **0** (`markov_switching.py:157`). This is harmless for the marginal
recursions in Section 2 — the redundant axis carries no information and is summed out at
`markov_switching.py:223-226` — but it is *not* harmless for initialization (Section 2.4).

### 1.2 The transition matrix and its indexing

Only $k(k-1) = 2$ transition parameters are free for $k=2$ regimes, and statsmodels
parameterizes **column 0 of $\Pi$ only** (`markov_switching.py:530-535`: the parameter block
has length `k_regimes - 1 = 1` per regime). The parameter names come from
`markov_switching.py:1405-1408`:

```python
['p[%d->%d]' % (j, i) for i in range(self.k_regimes-1) for j in range(self.k_regimes)]
```

With `k_regimes=2` the outer loop `i` takes only the value $0$, so this yields exactly
`['p[0->0]', 'p[1->0]']` — both *destinations* are regime 0. The matrix is filled at
`markov_switching.py:652-659`:

```python
regime_transition_matrix[:-1, :, 0] = np.reshape(params[...], (k_regimes-1, k_regimes))
regime_transition_matrix[-1, :, 0]  = 1 - np.sum(regime_transition_matrix[:-1, :, 0], axis=0)
```

Row 0 gets $(p_{00},\,p_{10})$; row 1 is filled by complement. Writing out the returned array:

$$\Pi[:,:,0] \;=\;
\begin{pmatrix} p_{00} & p_{10} \\ 1 - p_{00} & 1 - p_{10}\end{pmatrix}
\;=\;
\begin{pmatrix} p_{00} & p_{10} \\ p_{01} & p_{11}\end{pmatrix}
\;=\; P^{\!\top}, \qquad
P = \begin{pmatrix} p_{00} & p_{01} \\ p_{10} & p_{11}\end{pmatrix}$$

Three consequences to internalize:

1. **$\Pi$ is left-stochastic** — each *column* sums to one. Verified: column sums
   $= (1.0, 1.0)$. If you assume row-stochastic you will silently read $p_{10}$ where you meant
   $p_{01}$.
2. **$\Pi$ is 3-D**, shape `(2, 2, 1)`, with the trailing axis reserved for time-varying
   transition probabilities (`markov_switching.py:638-640`). With no TVTP it has length 1, so
   the trailing index is always `0`. This is why `diagnostics.py:145` writes
   `model.regime_transition_matrix(results.params)[:, :, 0]`.
3. **`tm[1, 1, 0]` $= p_{11}$** is a diagonal element, so the row/column ambiguity does not bite
   there — but it is *not* a fitted parameter. It is $1 - p_{10}$, derived. Any restriction you
   might want to place on regime 1's self-persistence has to be expressed through $p_{10}$;
   there is no `p[1->1]` to touch. (This is why the superseded spec *floored* `p[1->0]` in order
   to *cap* $p_{11}$ — see Section 8.1.)

Fitted values (synthetic): $p_{00} = 0.99195970$, $p_{10} = 0.11427967$, hence
$p_{01} = 0.00804030$, $p_{11} = 0.88572033$.

$$\Pi[:,:,0] = \begin{pmatrix} 0.99195970 & 0.11427967 \\ 0.00804030 & 0.88572033 \end{pmatrix}$$

Fitted values (**real**, full 1750-week history): $p_{00} = 0.92256954$,
$p_{10} = 0.02771728$. Note that on real data $j^\star = 0$, so here $p_{00}$ is the *jump*
regime's self-persistence and $p_{11} = 0.97228272$ is the calm regime's — the exact opposite of
the synthetic assignment. Read the index off `jump_regime_index`, never off the parameter name.

### 1.3 The parameter vector

Parameters are ordered lexicographically by block, then by number, then by regime
(`markov_switching.py:323-352`). Blocks are registered in order: `regime_transition`
(`markov_switching.py:535`), then `exog`, then `variance` (`markov_regression.py:140-141`).
For this configuration:

$$\theta = \big(\,\underbrace{p_{00},\ p_{10}}_{\texttt{regime\_transition}},\
\underbrace{\mu_0,\ \mu_1}_{\texttt{exog}},\
\underbrace{\sigma_0^2,\ \sigma_1^2}_{\texttt{variance}}\,\big) \in \mathbb R^6$$

`param_names` $=$ `['p[0->0]', 'p[1->0]', 'const[0]', 'const[1]', 'sigma2[0]', 'sigma2[1]']`,
and `k_params = 6` — asserted at `checks.py:110-113`. `const[0]`/`const[1]` are two entries
because `switching_trend=True` makes `switching_coeffs` truthy and routes through the
per-regime naming branch at `markov_regression.py:342-345`; the superseded common-mean spec
produced a single `const` from the else-branch at `markov_regression.py:347`.
`sigma2[0]`/`sigma2[1]` are two entries because `switching_variance=True` routes through
`markov_regression.py:350-352`.

**All six are free.** Nothing is pinned, capped, sorted, or otherwise touched between the
optimizer and the likelihood; `src/jump_model.py` defines no `transform_params` or
`untransform_params` override at all.

Fitted (synthetic):

$$\hat\theta = (0.99195970,\ 0.11427967,\ 5.746325\times10^{-4},\ -2.9358894\times10^{-2},\
7.132980\times10^{-5},\ 2.6871139\times10^{-3})$$

In volatility units: $\hat\sigma_0 = 0.8446\%$/week ($\approx 6.09\%$ annualized at
$\sqrt{52}$), $\hat\sigma_1 = 5.1837\%$/week ($\approx 37.38\%$ annualized). A $6.14\times$
ratio in $\sigma$, $37.67\times$ in variance, so $j^\star = 1$ here.

Fitted (**real**, 1750 weeks): $\hat\theta = (0.92256954,\ 0.02771728,\ -2.596858\times10^{-3},\
3.634863\times10^{-3},\ 1.4726414\times10^{-3},\ 2.2551175\times10^{-4})$, $\ell = 4310.9380$,
$j^\star = 0$. In volatility units $\hat\sigma_{j^\star} = 3.8375\%$/week ($27.67\%$ annualized)
against $\hat\sigma_{\text{calm}} = 1.5017\%$/week ($10.83\%$) — only a $2.56\times$ ratio in
$\sigma$, $6.53\times$ in variance.

The likelihood separates the two regimes overwhelmingly on variance, so it is the *variance
ratio* that determines how sharply regimes are identified. Compare the two fits above: the
synthetic fixture has a $37.7\times$ variance ratio and classifies almost perfectly
(RCM $3.47$, Section 6.5); real SPY has $6.53\times$ and classifies fuzzily (RCM $33.53$). That
single number explains most of the difference between "this works beautifully" on the fixture
and the open findings in Section 8.

### 1.4 Ergodic (stationary) distribution

**Why you need it.** Two reasons. (a) It is the filter's initial condition — statsmodels'
default (Section 2.4). (b) It is the model's implied unconditional frequency of crisis weeks,
which is a strong prior you are asserting whether you meant to or not.

**Derivation.** $\pi$ is the distribution satisfying $\Pi\pi = \pi$ with $\mathbf 1^{\!\top}\pi = 1$
(equivalently $\pi^{\!\top} P = \pi^{\!\top}$ — $\pi$ is the left eigenvector of $P$, the right
eigenvector of $\Pi$, for eigenvalue 1). Write out the first component:

$$\pi_0 = p_{00}\pi_0 + p_{10}\pi_1
\;\Longrightarrow\; \pi_0(1 - p_{00}) = \pi_1 p_{10}
\;\Longrightarrow\; \pi_0 p_{01} = \pi_1 p_{10}$$

Impose $\pi_0 + \pi_1 = 1$:

$$\boxed{\ \pi_0 = \frac{p_{10}}{p_{01} + p_{10}}, \qquad \pi_1 = \frac{p_{01}}{p_{01} + p_{10}}\ }$$

The chain is irreducible and aperiodic whenever $0 < p_{01}, p_{10} < 1$, so $\pi$ is unique and
is the limiting distribution — standard finite-state Markov chain theory (Perron–Frobenius).

**How statsmodels computes it** (`markov_switching.py:587-589`), for general $k$:

```python
A = np.c_[(np.eye(m) - regime_transition).T, np.ones(m)].T
probabilities = np.linalg.pinv(A)[:, -1]
```

Unpacking: $A$ is the $(m+1)\times m$ stack $\begin{pmatrix} I - \Pi \\ \mathbf 1^{\!\top}\end{pmatrix}$,
and $A\pi = (0,\dots,0,1)^{\!\top}$ encodes $(I-\Pi)\pi = 0$ together with
$\mathbf 1^{\!\top}\pi = 1$. Since the target is the last standard basis vector,
$\pi = A^{+}e_{m+1} = $ `pinv(A)[:, -1]`. Using the pseudo-inverse rather than solving makes
it robust to the rank deficiency of $I - \Pi$. Line `markov_switching.py:600` then floors the
result at $10^{-20}$ so the log-space filter never sees $\log 0$.

**Numbers (synthetic fit).** $\pi_1 = 0.00804030/(0.00804030 + 0.11427967) = 0.0657317$.
statsmodels reports `initial_probabilities` $= (0.93426828,\ 0.06573172)$. Match.

**Numbers (real fit).** $\pi_{j^\star} = \pi_0 = 0.02771728/(0.02771728 + 0.07743046)
= 0.263603$. The model asserts that **26.4% of all weeks are jump-regime weeks**. Against a
hard-assigned share of $23.2\%$ (406 of 1750, `diagnostics.py:555-558`) that is internally
consistent — and it is also a statement that the "jump" regime is not a panic state. See
Section 8.4.

**Audit record: how the superseded constraints made this quantity unrepresentable.** With
$p_{00}$ pinned at $0.98$, $p_{01} = 0.02$ was *fixed*; with $p_{10}$ floored at $0.15$:

$$\pi_1 = \frac{0.02}{0.02 + p_{10}}, \qquad p_{10}\in[0.15,\,1)
\;\Longrightarrow\; \pi_1 \in \big(0.0196,\ 0.1176\big]$$

**The two constraints jointly capped the unconditional jump frequency at 11.76% of weeks.**
Neither announced this on its own; it falls out of combining them. The measured filtered jump
share on real SPY was **13.77%**, strictly outside that interval — not a preference the
likelihood could trade off, a region of outcome space the parameterization could not reach at
all. This is the cleanest of the four reasons the specification was abandoned, because it is a
pure arithmetic contradiction rather than a judgement call: the model was forbidden from
describing what the data showed, and nothing in the fit output said so. The general lesson is
that when you impose two constraints on different parameters, you must work out what they imply
*jointly* for every derived quantity you care about, because the optimizer will not tell you.

### 1.5 Expected regime duration

**Derivation.** Condition on having just entered regime $i$. The run continues with probability
$p_{ii}$ each period independently (first-order Markov), so the run length $D_i$ is geometric
on $\{1,2,3,\dots\}$:

$$\Pr(D_i = d) = p_{ii}^{\,d-1}(1 - p_{ii}), \qquad
E[D_i] = \sum_{d\ge1} d\,p_{ii}^{\,d-1}(1-p_{ii}) = \boxed{\frac{1}{1 - p_{ii}}}$$

Also useful: $\operatorname{Var}(D_i) = p_{ii}/(1-p_{ii})^2$, so the *standard deviation* of
duration is $\sqrt{p_{ii}}/(1-p_{ii}) \approx E[D_i]$ for $p_{ii}$ near 1. Durations are
enormously dispersed; a "50-week average" regime routinely produces 5-week and 150-week runs.
Never treat $E[D_i]$ as a typical value.

Implemented at `markov_switching.py:1593-1614`; the arithmetic is line
`markov_switching.py:1607`, `expected_durations[~degenerate] = 1 / (1 - diag[~degenerate])`,
with $p_{ii}=1$ mapped to `np.inf` (lines 1611-1612).

**Worked numbers:**

| Fit | Calm $p_{ii}$ | $E[D_{\text{calm}}]$ | Jump $p_{ii}$ | $E[D_{\text{jump}}]$ |
|---|---|---|---|---|
| Synthetic ($j^\star = 1$) | $p_{00} = 0.99195970$ | $124.373$ wks | $p_{11} = 0.88572033$ | $8.750$ wks |
| **Real** ($j^\star = 0$) | $p_{11} = 0.97228272$ | $36.079$ wks | $p_{00} = 0.92256954$ | $12.915$ wks |
| *Historical (superseded spec)* | $p_{00} = 0.98$ pinned | $50.0$ wks | $p_{11} \le 0.85$ capped | $\le 6.667$ wks |

statsmodels reports `expected_durations` $= (124.37344066,\ 8.75046258)$ on the synthetic fit
and $(12.9148,\ 36.0786)$ on the real fit — confirming both the formula and the arithmetic.

**How the real fit scores on duration realism** (`diagnostics.py:621-629`): against a model
$E[D_{\text{jump}}] = 12.915$ weeks, the empirical mean run of weeks with filtered
$P(\text{jump}) > 0.5$ is $6.15$ weeks over 66 episodes, median $4$, max $33$
(2022-04-11 .. 2022-11-21). Model $E[D_{\text{calm}}] = 36.08$ against an empirical mean calm
run of $20.06$. Both regimes are fitted as **more persistent than the realized episodes**, which
is the geometric-duration dispersion above interacting with a fuzzy classifier: short spells
below the $0.5$ line chop long model episodes into pieces.

**Audit record: the superseded ceiling made 2008 inexpressible.** Read the third row again.
$6.667$ weeks was the *maximum average crisis length the old parameterization could express*.
The Sep 2008 – Mar 2009 acute phase of the GFC ran roughly 26 weeks; the full Oct 2007 – Mar
2009 drawdown roughly 74. The model could not represent either as a single regime episode, and
what it did instead was chop a long crisis into several ~6-week spells separated by brief calm
interludes. The current unrestricted fit reaches a 33-week episode without difficulty.

---

## Layer 2 — The Hamilton filter

Hamilton (1989), *Econometrica* 57(2), 357–384, §2–3. The recursion is also the HMM
**forward algorithm** with normalization (Rabiner 1989 calls the normalizer $c_t$); Hamilton's
contribution was the econometric framing in which the normalizer *is* the likelihood
contribution.

### 2.1 What "filtered" means, precisely

$$\xi_{t\mid t}(j) \;=\; \Pr\!\big(S_t = j \;\big|\; r_1, r_2, \dots, r_t;\ \theta\big)$$

Conditioning set: **past and present only**. $r_{t+1},\dots,r_T$ do not appear. This is the
object a real-time signal is allowed to use, because at the close of week $t$ it is the entire
posterior available. Docstring confirmation, `markov_switching.py:136-138`: "the probability of
being in each regime conditional on time $t$ information."

### 2.2 The recursion, in three steps

Collect the densities into a vector $\eta_t = (\eta_t(0),\ \eta_t(1))^{\!\top}$.

**Step 1 — Prediction** (propagate the chain one step forward; Chapman–Kolmogorov):

$$\xi_{t\mid t-1}(i) \;=\; \sum_{j} p_{ji}\,\xi_{t-1\mid t-1}(j)
\qquad\Longleftrightarrow\qquad
\xi_{t\mid t-1} = \Pi\,\xi_{t-1\mid t-1}$$

The matrix form is *why* statsmodels stores $\Pi = P^{\!\top}$ rather than $P$: left-stochastic
means the propagation is a plain matrix–vector product with no transpose.

**Step 2 — Update** (Bayes' rule; the regime posterior given the new observation):

$$\xi_{t\mid t}(j)
\;=\; \frac{\eta_t(j)\,\xi_{t\mid t-1}(j)}{\sum_{i}\eta_t(i)\,\xi_{t\mid t-1}(i)}
\qquad\Longleftrightarrow\qquad
\xi_{t\mid t} = \frac{\eta_t \odot \xi_{t\mid t-1}}{\mathbf 1^{\!\top}(\eta_t \odot \xi_{t\mid t-1})}$$

Numerator = prior $\times$ likelihood; denominator = the marginal density of $r_t$, which is
exactly the normalizing constant Bayes' rule requires.

**Step 3 — Likelihood contribution.** The denominator from Step 2 is not thrown away. It *is*
the one-step-ahead predictive density of the observation:

$$f(r_t \mid \mathcal F_{t-1};\theta)
= \sum_j f(r_t\mid S_t=j)\Pr(S_t=j\mid\mathcal F_{t-1})
= \mathbf 1^{\!\top}(\eta_t \odot \xi_{t\mid t-1})$$

$$\ell_t = \log\!\big(\mathbf 1^{\!\top}(\eta_t \odot \xi_{t\mid t-1})\big),
\qquad \ell(\theta) = \sum_{t=1}^{T}\ell_t$$

This is the **prediction-error decomposition** of the likelihood: the joint density factorizes
as $f(r_1,\dots,r_T) = \prod_t f(r_t\mid \mathcal F_{t-1})$, and the filter produces each factor
as a by-product of maintaining the state posterior. That single fact is what makes an otherwise
intractable $2^T$-term sum over regime paths cost $O(Tk^2)$.

Note also that $\Pr(S_t = j \mid \mathcal F_{t-1})$ from Step 1 is genuinely a **one-week-ahead
forecast** of the regime, available at $t-1$. statsmodels exposes it as
`predicted_marginal_probabilities` (`markov_switching.py:1583-1591`). It is strictly weaker than
$\xi_{t|t}$ but strictly stronger than nothing, and it is the only object with *no* dependence on
week-$t$ data at all.

### 2.3 Log-space form — what the code actually runs

`cy_hamilton_filter_log` converts everything to logs first (`markov_switching.py:169-170`) and
runs the recursion additively. Writing $L^{\text{pred}}_t = \log\xi_{t\mid t-1}$,
$L^{\text{filt}}_t = \log\xi_{t\mid t}$:

$$L^{\text{pred}}_t(i) = \operatorname*{logsumexp}_{j}\big[\log p_{ji} + L^{\text{filt}}_{t-1}(j)\big]$$

$$a_t(i) = \log\eta_t(i) + L^{\text{pred}}_t(i)$$

$$\ell_t = \operatorname*{logsumexp}_{i} a_t(i), \qquad
L^{\text{filt}}_t(i) = a_t(i) - \ell_t$$

where $\operatorname{logsumexp}(x) = \log\sum_i e^{x_i}$, evaluated by the max-shift trick
$= x^* + \log\sum_i e^{x_i - x^*}$.

**Why log-space is not optional.** Step 2's normalization keeps $\xi_{t|t}$ on $[0,1]$, so the
*probabilities* do not underflow. The unnormalized forward variables do — in both directions.
Concretely: $\ell_t$ ranges from $-2.58$ to $+3.85$ nats per week on the synthetic fit, mostly
positive because weekly returns are $O(10^{-2})$ so the *density* is $O(10)$. The running
product $\prod_{s\le t} f(r_s\mid\mathcal F_{s-1})$ therefore **grows**, reaching $e^{475.34}$
$\approx 10^{206}$ on the 150-week fixture and $e^{4310.94} \approx 10^{1872}$ on the 1750-week
real sample. float64 tops out near $10^{308}$, i.e. about $710$ nats, so on real SPY the naive
product overflows after roughly $710/2.46 \approx 290$ weeks — a fifth of the way through the
sample. Conversely a crisis week evaluated under the *calm* regime carries $\log\eta_t$ on the
order of $-31$ (a $-7\%$ week) to $-67$ (a $-10\%$ week) at the synthetic
$\hat\mu_0 = 0.0575\%,\ \hat\sigma_0 = 0.8446\%$; a run of those drives the product back down
just as fast. Log-space makes accumulation additive and unconditionally stable, at the cost of
one $\operatorname{logsumexp}$ per state per period.

(**Correction to an earlier version of this document**, which asserted that $\exp(473.5)$
overflows float64. It does not — $10^{206}$ is comfortably representable. The overflow argument
needs the real sample length to bite, which is why the corrected figure above is stated for
$T = 1750$ rather than for the fixture.)

Line `markov_switching.py:170` also floors transition probabilities at $10^{-20}$ before
logging, so a transition estimated at zero degrades to $-46$ nats rather than $-\infty$. That
floor is load-bearing on real data: the $k=3$ comparison fit in `diagnostics.py` returns
$p_{2\to0} = 4.36\times10^{-19}$ (Section 8.5), which is below the floor and would otherwise
have produced $\log 0$.

The inner loop is compiled Cython (`markov_switching.py:203-212`, dispatching by BLAS dtype
prefix to `_hamilton_filter.cp313-win_amd64.pyd`); only the `.pyd` ships in this `.venv`, so
the recursion above is reconstructed from the documented input/output quantities at
`markov_switching.py:117-151` plus the initialization and post-processing that *are* in Python.
Lines `markov_switching.py:219-226` exponentiate back and marginalize the redundant $S_{t-1}$
axis; `markov_switching.py:214-216` retains the *log* arrays because the smoother needs them
(Section 4).

### 2.4 Initialization — what statsmodels actually does

Default is **steady-state (ergodic) initialization**, set in the constructor at
`markov_switching.py:537-538` (`self._initialization = 'steady-state'`) and computed by the
`pinv` solve of Section 1.4. `src/jump_model.py` never overrides it, so:

$$\xi_{1\mid 0} = \pi$$

The mechanics have one wrinkle. `markov_switching.py:187-197` writes $\log\pi$ into
`filtered_joint_probabilities[..., 0]` and, because the local `order` is 1 (Section 1.1), the
loop at lines 192-196 applies $\Pi$ **once** while building the joint. The filter's own
prediction step then applies $\Pi$ again. So the effective prior on the first observation is
$\Pi^2\pi$. Under steady-state initialization this is invisible: $\Pi\pi = \pi$, so
$\Pi^2\pi = \pi$, exactly as intended. Verified on the current fit:
`predicted_marginal_probabilities[:, 0]` $= (0.93426828,\ 0.06573172) = \pi$.

**But it is not invisible if you ever call `initialize_known`** (`markov_switching.py:563-574`),
which is the natural thing to reach for when chaining expanding-window refits (Section 4.3).
Re-verified against the current specification: seeding $q = (1 - 10^{-12},\ 10^{-12})$ gives
`predicted_marginal_probabilities[:, 0]` $= (0.98490289,\ 0.01509711)$, which is exactly
$\Pi^2 q$, not $\Pi q = (0.99195970,\ 0.00804030)$ and not $q$. **Two transition steps are
applied, not one.** The docstring at `markov_switching.py:120-122` says the
initial probabilities describe the chain "at time $t = -\text{order}$", which for
`MarkovRegression` reads as one step, not two. Do not trust the docstring on this point; the
redundant regime axis in `_conditional_loglikelihoods` inflates the local `order` to 1 while
`model_order` stays 0, and the two disagree. If you use known initialization, pass $\Pi^{-2}q$
or, more sanely, verify the realized `predicted_marginal_probabilities[:, 0]` against your
intent.

Alternatives named for completeness: **diffuse initialization** ($\xi_{1|0} = (1/k,\dots,1/k)$)
and treating $\xi_{1|0}$ as $k-1$ extra free parameters. Ergodic initialization is the
conventional choice for a stationary chain and costs no parameters; it is also the only one of
the three that is *internally consistent* with the estimated $P$.

### 2.5 Filtered probabilities from the synthetic fit

Jump-regime probability $\xi_{t\mid\cdot}(j^\star)$ around the true jump block (weeks 100–109,
`checks.py:42`, `checks.py:71`), with $j^\star = 1$ on this fixture:

| week | $\xi_{t\mid t}(j^\star)$ filtered | $\xi_{t\mid T}(j^\star)$ smoothed |
|---|---|---|
| 98 | 0.001810 | 0.035592 |
| 99 | 0.002448 | **0.212773** |
| 100 | 0.998767 | 0.999989 |
| … | … | … |
| 109 | 1.000000 | 1.000000 |
| 110 | **0.542069** | 0.136462 |
| 111 | 0.116746 | 0.018861 |

Both cross $0.50$ first at week 100 — on data this clean, either would trigger the thermostat on
the same week. Section 4.3 explains why that is luck, not a general property. Max absolute
discrepancy across the sample: $0.405607$, at week 110.

**One numerical detail that reaches the public contract.** The filter's normalization at Step 2
can put the returned probability an ULP *above* one: the synthetic fit's maximum filtered value
is $1 + 2.22\times10^{-16}$ and the real fit's is $1 + 8.88\times10^{-16}$, one observation each.
Harmless for tiering, fatal for any downstream $\sqrt{1-p}$, which is why
`estimate_jump_regimes` clips to $[0,1]$ before returning (`src/jump_model.py:172-175`).

---

## Layer 3 — Maximum likelihood estimation

### 3.1 The objective

$$\hat\theta = \arg\max_{\theta \in \Theta} \ \ell(\theta)
= \arg\max_\theta \sum_{t=1}^{T} \log\!\big(\mathbf 1^{\!\top}(\eta_t(\theta)\odot\xi_{t\mid t-1}(\theta))\big)$$

The filter is the *only* way $\theta$ reaches the objective: `loglikeobs`
(`markov_switching.py:943-962`) runs `self._filter(params)` and returns element `[5]`, which is
`joint_loglikelihoods` $= (\ell_1,\dots,\ell_T)$ per the name list at
`markov_switching.py:828-834`. `loglike` (`markov_switching.py:964-976`) sums it. Every
likelihood evaluation is a full $O(Tk^2)$ filter pass.

Optimizer: BFGS (`method='bfgs'` default, `markov_switching.py:1028`), invoked at
`markov_switching.py:1125-1130` with `skip_hessian=True`. Gradients are **complex-step
derivatives**, `approx_fprime_cs` (`markov_switching.py:978-992`) — not finite differences.
Complex-step differentiation evaluates $f(x + ih)$ and takes $\operatorname{Im}f/h$, exact to
machine precision *provided $f$ is analytic*. Hold that thought for Section 3.5.

Synthetic fit: $\ell(\hat\theta) = 475.3433$, converged in 31 function and 31 gradient calls,
`warnflag = 0`. **Real** fit: $\ell(\hat\theta) = 4310.9380$, converged.

**The convergence report is now worth believing.** Because nothing intercepts the parameter
vector, the objective is smooth in every optimizer coordinate and the returned diagnostics
describe the surface that was actually maximized:

```
gopt      max |g_i| = 2.84e-06        (all six coordinates)
Hinv diag = [144.51, 128.15, 7.95e-05, 3.86e-02, 4.37e-05, 1.89e-02]
```

No coordinate has an exactly-zero gradient and no diagonal entry of the inverse-Hessian estimate
is still sitting at the BFGS identity initialization of $1.0$. Under the superseded spec one
coordinate had both, which is the signature of a direction the optimizer never explored
(Section 3.5b). `checks.py:124-133` now asserts both properties on every run, so the regression
cannot recur silently.

### 3.2 The constrained ↔ unconstrained reparameterization

BFGS is an unconstrained optimizer. It must not be handed a search space where
$\sigma^2 < 0$ or $p \notin [0,1]$ are reachable. statsmodels solves this with a
**reparameterization** (a *link function*, in GLM vocabulary): the optimizer works in
$\tilde\theta \in \mathbb R^6$ and every likelihood evaluation maps
$\tilde\theta \mapsto \theta$ first.

`transform_params`: $\mathbb R^6 \to \Theta$ (unconstrained $\to$ constrained), called on the way
*in* to the likelihood.
`untransform_params`: $\Theta \to \mathbb R^6$, called once on the way *out* of setup at
`markov_switching.py:1120-1121` to convert start values.

These are statsmodels' own methods and nothing else. The repo overrides neither; the pair is a
genuine mutual inverse, verified on the current fit:
`transform_params(untransform_params(θ)) - θ` is exactly the zero vector in all six
coordinates. Section 3.5c records what happened when that was not true.

**Transition probabilities** (`markov_switching.py:1444-1449`) — multinomial-logistic /
**softmax** against a zero baseline, applied per column of $\Pi$:

```python
tmp1 = unconstrained[self.parameters[i, 'regime_transition']]
tmp2 = np.r_[0, tmp1]
constrained[...] = np.exp(tmp1 - logsumexp(tmp2))
```

For $k=2$ each column has a single free parameter, so this collapses to the plain **logistic**:

$$p_{i0} = \frac{e^{\tilde p_i}}{1 + e^{\tilde p_i}} = \operatorname{logistic}(\tilde p_i)$$

Inverse (`markov_switching.py:1502-1503`, special-cased for $k=2$) is the **logit**:

```python
unconstrained[s] = -np.log(1. / constrained[s] - 1)
```

$= -\log\!\big(\tfrac{1-p}{p}\big) = \log\tfrac{p}{1-p}$. For $k > 2$ the inverse has no closed
form and statsmodels runs a root-find (`markov_switching.py:1505-1512`).

**Variances** (`markov_regression.py:384-385`) — **squaring**, not logging:

```python
constrained[self.parameters['variance']] = unconstrained[self.parameters['variance']]**2
```

with inverse $\sqrt{\cdot}$ at `markov_regression.py:414-415`. So the optimizer's variance
coordinate is $\tilde\sigma_j = \pm\sigma_j$, a *standard deviation*, not a log-variance. Two
things follow. (i) The map is two-to-one — $\pm\tilde\sigma_j$ give the same model — so the
likelihood surface has a mirror symmetry through $\tilde\sigma_j = 0$ and a saddle/kink at the
origin. (ii) Scaling is in $\sigma$ not $\log\sigma$, so gradient magnitudes differ from the
log-parameterization you might expect from GARCH code. Verified fitted unconstrained vector
(synthetic):
$\tilde\theta = (4.8152159,\ -2.0477525,\ 0.00057463,\ -0.02935889,\ 0.00844570,\ 0.05183738)$,
whose last two entries are $\hat\sigma_0, \hat\sigma_1$ and whose first is
$\operatorname{logit}(0.99195970) = 4.8152159$.

**Intercepts**: untouched (`markov_regression.py:380-381`), $\mu_0$ and $\mu_1$ are already
unconstrained — and are copied through elementwise, so a switching mean adds no new curvature to
the link map.

### 3.3 (audit record) Why the superseded constraints lived in `transform_params`

> **This section documents deleted code.** `ConstrainedMarkovRegression` and
> `_constrained_markov_regression()` were removed on 2026-08-12 along with `CALM_REGIME`,
> `JUMP_REGIME`, `DEFAULT_CALM_STAY_PROBABILITY` and `DEFAULT_JUMP_STAY_CEILING`. Nothing
> described here is in `src/jump_model.py` today. It is retained because the *mechanism* by
> which it failed is the transferable content, and because the design decision was defensible
> on its face — which is exactly what makes it worth remembering.

`transform_params` is the *unavoidable chokepoint*: nothing reaches the filter without passing
through it (`markov_switching.py:957-958`, `1120-1121`, `913-914`). Injecting there guaranteed
the constraint held on **every likelihood evaluation**, including inside the random search and
inside the numerical gradient. That was the reason for the design, and it was a real reason —
`statsmodels` exposes no constraint API, and the argument at the time was that post-hoc
relabelling after `fit()` would not stop the optimizer wandering into the mislabelled basin
during estimation. Section 7.3 explains why that argument, applied to a *labelling* constraint,
is wrong: there is no such thing as the wrong basin when the two basins have identical
likelihood.

The deleted body:

```python
def _apply_constraints(self, params):
    (sigma2_calm, sigma2_jump), (p_calm, p_jump) = self._indices()
    params = params.copy()
    params[sigma2_calm], params[sigma2_jump] = sorted(
        (params[sigma2_calm], params[sigma2_jump])
    )
    params[p_calm] = calm_stay_probability                       # 0.98
    params[p_jump] = max(params[p_jump], jump_transition_floor)  # 1 - 0.85
    return params
```

Mapping to math, where $\mathcal C$ denotes the constraint operator:

| Operation | Math |
|---|---|
| `sorted()` on the variance pair | $(\sigma_0^2,\sigma_1^2) \mapsto (\min,\max)$ — enforced $\sigma_0^2 \le \sigma_1^2$ |
| hard pin | $p_{00} := 0.98$ — a point restriction, one dimension removed |
| floor | $p_{10} := \max(p_{10},\,0.15)$, i.e. $p_{11} \le 0.85$ — an inequality restriction |

It was applied on the way in (after `super().transform_params`) and again on the way out
(*before* `super().untransform_params`). The composition was therefore

$$\text{transform} = \mathcal C \circ \mathcal T, \qquad
\text{untransform} = \mathcal T^{-1}\circ\,\mathcal C$$

with $\mathcal T$ the statsmodels logit/square map. $\mathcal C$ is a **projection onto the
feasible set**: idempotent ($\mathcal C^2 = \mathcal C$) but not injective. Consequences in
Section 3.5.

### 3.4 `search_reps` and the multimodality of the mixture likelihood

`src/jump_model.py:134` passes `search_reps=50` (default `DEFAULT_SEARCH_REPS`,
`src/jump_model.py:8`). The mechanism (`markov_switching.py:1300-1370`):

1. Untransform the base start values into $\mathbb R^6$ (line 1335).
2. Draw 50 perturbations $u_i \sim \mathcal U(-0.5, 0.5)^6$ scaled by `search_scale=1`
   (lines 1346-1349).
3. For each, run 5 EM iterations (`search_iter=5`, line 1358) and keep the candidate if its
   log-likelihood beats the incumbent (lines 1361-1364).
4. Return the winner, transformed (line 1370).

Then a further 5 EM iterations polish the winner (`markov_switching.py:1113-1118`,
`em_iter=5`) before BFGS starts.

**Why random restarts are necessary and not defensive coding.** The likelihood of a
finite-mixture or Markov-switching model is **not** globally concave and generically has
multiple local maxima. Three distinct sources, all present here:

- **Label switching** (Section 7): the likelihood is *exactly* invariant under permuting regime
  labels, so every interior mode is duplicated $k!$ times. For $k=2$, every mode has a twin.
- **Spurious modes / unbounded likelihood**: driving $\sigma_j^2 \to 0$ while a single
  observation is assigned to regime $j$ sends the density $\to\infty$. The mixture likelihood is
  unbounded on the boundary of the parameter space (Day 1969; Kiefer & Wolfowitz 1956). Any
  "maximum" you find is a *local interior* maximum, and which one you find depends on where you
  start.
- **Flat ridges** between "high variance, low persistence" and "moderate variance, high
  persistence" configurations, which trade off against each other. The superseded code's comment
  asserted this happened on the 2006–2011 window; it was tested on real data on 2026-08-12 and
  **the claimed pathology does not occur** — the unrestricted fit puts the high-variance regime
  at $E[D] = 17.22$ weeks against $44.66$ for the low-variance one (`diagnostics.py:490-501`),
  i.e. high variance pairs with *low* persistence, the opposite of the claim. The ridge is real
  as geometry; the specific direction the comment asserted was not.

The seeding wrapper `_seeded_numpy_random` (`src/jump_model.py:41-52`) exists because
`markov_switching.py:1349` calls `np.random.uniform` on the *global* RNG with no
`random_state` hook. Without it, `estimate_jump_regimes` is nondeterministic, and
`checks.py:95-98` (identical input $\Rightarrow$ identical output) would fail intermittently.
The wrapper saves and restores global RNG state, so it does not leak.

**Empirical confirmation that the label indeterminacy is real, not theoretical.** Fit the
plain `MarkovRegression` with a *common* mean to the same synthetic data with the same seed:

$$\hat\theta = (\underbrace{0.873109}_{p_{00}},\ \underbrace{0.009415}_{p_{10}},\
0.000470,\ \underbrace{0.003459}_{\sigma_0^2},\ \underbrace{0.000070}_{\sigma_1^2}),
\qquad \ell = 473.8417$$

Read the variances: $\sigma_0^2 \gg \sigma_1^2$. That fit labelled the **high-volatility regime
as index 0**, with $E[D_0] = 7.88$ weeks and $E[D_1] = 106.2$ weeks. On data explicitly
constructed to have an obvious calm state, `regime 0` came out as the crisis. The repo's own
6-parameter spec lands the *other* way on this fixture ($j^\star = 1$) and lands on
$j^\star = 0$ on both real-data windows tested (`diagnostics.py:513-515` reports "relabelling
was REQUIRED" for full history and for 2006–2011). Which basin you get is a function of the
data and the seed, and nothing else. **Hardcoding a regime index would invert the signal on
real SPY**, which is precisely why `_jump_regime_index` exists.

**Alternative estimation route: EM / Baum–Welch.** For HMMs the EM algorithm has closed-form
M-steps and is the standard estimator (Baum et al. 1970; Dempster, Laird & Rubin 1977;
Rabiner 1989 for the HMM-specific "Baum–Welch" naming). statsmodels implements it at
`markov_switching.py:1146-1236` and `markov_regression.py:200-288` but uses it **only as a
warm-start**, never as the final estimator. The M-step for variances,
`markov_regression.py:271-274`, is the smoothed-probability-weighted second moment:

$$\hat\sigma_j^2 \;=\; \frac{\sum_t \xi_{t\mid T}(j)\,(r_t - \hat\mu)^2}{\sum_t \xi_{t\mid T}(j)}$$

and for transitions, `markov_switching.py:1280-1284`:

$$\hat p_{ij} \;=\; \frac{\sum_t \Pr(S_t = j, S_{t-1} = i \mid \mathcal F_T)}{\sum_t \Pr(S_{t-1} = i \mid \mathcal F_T)}$$

i.e. expected transition counts over expected occupancy — the multinomial MLE with soft counts.
With `switching_trend=True` there is now also an active M-step for the means,
`markov_regression.py:250-254`: a probability-weighted least-squares fit per regime,
$\hat\mu_j = \sum_t \xi_{t|T}(j)\,r_t \big/ \sum_t \xi_{t|T}(j)$ for the intercept-only design
(the code writes it as `pinv(tmp_exog) @ tmp_endog` with both sides scaled by
$\sqrt{\xi_{t|T}(j)}$, which is the same thing). Under the superseded common-mean spec that
branch was skipped in favour of the pooled OLS at `markov_regression.py:238-243`.

EM is monotone in $\ell$ and never leaves the feasible set, which is exactly the property the
`sorted()` hack tried and failed to buy (Section 3.5). It converges linearly, hence
statsmodels' hybrid: EM to get into a good basin, BFGS to finish with quadratic-ish
convergence.

**A warm-start mismatch that no longer exists.** `_em_iteration` calls
`self.smooth(params0, transformed=True)` (`markov_switching.py:1251`) — `transformed=True` means
`transform_params` is **not** called. Candidates are also *ranked* by
`self.loglike(proposed_params)` at `markov_switching.py:1361`, again with `transformed=True`.
Under the superseded constrained subclass this meant the 50 restarts explored and scored a
*different* surface from the one BFGS then maximized, and the constraints were re-imposed only
at the search boundaries (`markov_switching.py:1365`, `1370`, `1121`). With no overrides,
`transformed=True` is now a no-op distinction: search, ranking and final optimization all act on
the same likelihood. **Resolved by deletion**, and worth knowing before you are ever tempted to
reintroduce a `transform_params` override.

### 3.5 (audit record) Why `sorted()` inside `transform_params` was a genuine problem

> **This section documents deleted code**, retained as the audit trail. The mechanism below is
> the single most transferable thing in this document: a constraint that looks like a
> one-line convenience silently invalidated the gradient, the inverse Hessian, the standard
> errors and the parameter count, while every convergence indicator kept reporting success.

The constraint achieved its stated goal — the post-fit ordering assertion never fired. The
problems were all downstream of *how*.

**(a) Non-differentiability at $\sigma_0^2 = \sigma_1^2$.** As a function of the unconstrained
coordinates, $\mathcal C$ contained $\min(\cdot,\cdot)$ and $\max(\cdot,\cdot)$. These are
continuous but have a **kink** on the diagonal $\sigma_0^2 = \sigma_1^2$: the one-sided
derivatives swap which input they credit. The `max()` enforcing the persistence floor had the
same defect on the surface $p_{10} = 0.15$ — and that surface was *touched*, since the real-SPY
fit landed at exactly $p_{10} = 0.15000000$, zero slack. BFGS assumes $\ell$ is $C^2$ and builds
a secant approximation to $\nabla^2\ell$; on a kink the secant conditions are inconsistent and
the inverse-Hessian estimate degrades. The correct tool for a non-smooth objective is a
derivative-free or subgradient method, not BFGS.

**(b) The complex-step gradient was invalid, not merely inaccurate.** This is worse than the
usual finite-difference story. `approx_fprime_cs` requires $\ell$ **analytic**, and perturbs
$\tilde\theta_j \to \tilde\theta_j + ih$ with $h$ tiny, reading the derivative off
$\operatorname{Im}f/h$. The whole method depends on the imaginary part surviving the
computation. Two ways it did not:

*Ordering.* NumPy orders `complex128` **lexicographically** — real part first, then imaginary
part. So when the two variances tie in their real parts, `sorted()` breaks the tie **on the
imaginary part**, i.e. on the perturbation direction itself. Verified:

```
sorted((np.complex128(1e-4 + 1e-10j), np.complex128(1e-4))) -> [1e-4+0j, 1e-4+1e-10j]
```

At a variance tie the derivative is therefore credited to whichever coordinate the perturbation
happened to make "larger" — the *imaginary* coordinate decides which *real* coordinate receives
the sensitivity. That is not an approximation error; it is an attribution to the wrong variable.

*Clipping and pinning.* `max(np.complex128(0.1 + 1e-10j), 0.15)` returns the real `0.15`,
discarding the imaginary part outright — verified — so the derivative in that direction was
silently **zero** whenever the floor bound. It bound exactly on real SPY. The pin did the same
thing unconditionally: assigning a real constant into a complex array zeroes the imaginary part,
so $\partial\ell/\partial\tilde p_{00} \equiv 0$ at every point.

**The evidence, and why it is conclusive.** Two `mle_retvals` entries from the superseded fit:

```
mle_retvals['gopt'][0]    == -0.0   exactly
mle_retvals['Hinv'][0,0]  ==  1.0   exactly
warnflag                  ==  0
```

Neither number is "small"; both are *exact*. An exactly-zero gradient component is what you get
when the imaginary part was discarded, not when a real optimization converged. An inverse-Hessian
diagonal of exactly $1.0$ is the **BFGS identity initialization, never updated** — the rank-one
BFGS update is proportional to the observed change in gradient along the step, and that change
was identically zero, so the update contributed nothing in that direction. Taken together they
say: this coordinate was never explored. And BFGS reported `warnflag = 0`, `converged = True`
anyway, because a zero gradient is its convergence criterion. **The failure looked exactly like
success.** That is why `checks.py:124-133` now asserts against both signatures directly rather
than trusting `converged`.

**(c) The transform was not invertible, so `transform ∘ untransform ≠ id`.** statsmodels'
contract requires the pair to be mutual inverses. $\mathcal C$ is a projection, so the
composition was a **retraction**, not the identity. Verified at the time — all five values below
are **historical (superseded spec)** and no current code path reproduces them:

```
p                    = [0.98, 0.157124, 0.000358, 6.709e-05, 3.20685e-03]
transform(untransform(p)) - p  = [0, 2.8e-17, 0, 0, 0]      # fine: p is already feasible
q = p with sigma2 swapped      = [0.98, 0.157124, 0.000358, 3.20685e-03, 6.709e-05]
transform(untransform(q))      = [0.98, 0.157124, 0.000358, 6.709e-05, 3.20685e-03]   # != q
```

Any infeasible point was silently *moved*. The map was idempotent and stable at feasible points,
so it did not blow up — but two distinct $\theta$ values shared one $\tilde\theta$, and
`untransform_params` no longer answered "which $\tilde\theta$ produces this $\theta$?" It
answered "which $\tilde\theta$ produces the nearest feasible $\theta$?" On the current
specification the same round-trip returns the exact zero vector (Section 3.2).

**(d) Reported standard errors described a model that was never fitted.** This is the sharpest
practical consequence and it is easy to miss. The covariance matrix (`cov_type='approx'` default,
`markov_switching.py:1044`) comes from `cov_params_approx` at
`markov_switching.py:1834-1846`, which calls `self.model.hessian(self.params, transformed=True)`.
And `hessian` (`markov_switching.py:1010-1025`) is:

```python
return approx_hess_cs(params, self.loglike)
```

It passes no `args`, so `loglike` ran at its default `transformed=True` — meaning
`transform_params` was **never called** and the repo's constraints were **never applied** along
the differentiation path. This is the crux: the constraints lived in `transform_params`, and the
covariance calculation is the one code path in statsmodels that deliberately bypasses
`transform_params`. Verified at the time: with $p_{00}$ moved to $0.90$,
`model.loglike(p, transformed=True)` changed from $473.5077$ to $465.5101$ — the pinned
parameter was fully live on that surface. And the gradient of *that* surface at $\hat\theta$ was
$(51.76,\ 0.0005,\ -0.075,\ 43.70,\ -0.043)$: nowhere near zero, in exactly the pinned and
sorted coordinates.

So `bse` was the standard-error vector of a **different, unrestricted 5-parameter model**,
evaluated at a point that is not a stationary point of it. Observed:

```
bse = [1.92e-02, 1.19e-01, 7.46e-04, 1.04e-05, 1.44e-03]
```

A standard error of $0.0192$ was reported for `p[0->0]`, a number that was assigned by fiat and
never estimated. `res.bse`, `res.pvalues`, `res.conf_int()` and `res.summary()`'s significance
columns were all unusable under that specification — not merely conservative or approximate,
but describing a model that was not fitted. (Separately: even for a correctly-implemented
constrained fit, a parameter at an inequality boundary has a non-normal limiting distribution,
so $\hat\theta \pm 1.96\,\text{se}$ would not have applied to $p_{10}$ either — and it sat
exactly on its boundary on real data.)

**Fixes that were on the table, and what actually happened.**

1. **Reparameterize instead of projecting.** Replace the free pair
   $(\sigma_0^2, \sigma_1^2)$ with $(\sigma_0^2,\ \delta)$ where $\sigma_1^2 = \sigma_0^2 + e^{\delta}$
   and $\delta \in\mathbb R$. This makes $\sigma_0^2 < \sigma_1^2$ hold **identically and
   smoothly** everywhere, is a genuine bijection $\mathbb R^2 \to \{\sigma_0^2 < \sigma_1^2\}$,
   and restores $C^\infty$, so BFGS, complex-step gradients, and Hessian-based standard errors
   all become valid again. Same idea for the persistence cap:
   $p_{10} = 0.15 + 0.85\cdot\operatorname{logistic}(\tilde p_{10})$ enforces the floor smoothly.
   This was the recommended fix *given that the constraints were to be kept*.
2. **Drop the pin and use EM**, which cannot leave the feasible set and needs no gradient.
3. **Estimate freely, relabel afterwards** (Section 7.3).

**What was done on 2026-08-12: option 3, plus deletion of the other two constraints.** The
persistence pin and ceiling were dropped outright rather than smoothed, because real-data
diagnostics rejected them on their merits (LR-rejected pin, exactly-binding ceiling, and an
ergodic jump frequency the pair could not reach — Section 1.4). The ordering constraint was
dropped as a *constraint* and re-expressed as a post-hoc labelling rule, because labelling is
not a restriction on the model at all (Section 7.3). Option 1 became unnecessary: with nothing
to enforce, there is nothing to enforce smoothly. All four defects (a)–(d) are resolved by
having no override rather than by having a better one — see Section 8.1.

---

## Layer 4 — The Kim smoother

Kim (1994), *Journal of Econometrics* 60(1–2), 1–22; textbook treatment in Kim & Nelson (1999)
ch. 5, which is what statsmodels cites at `markov_regression.py:80-83`. Equivalent to the HMM
**forward–backward algorithm**, in the "$\gamma$ from $\gamma$" formulation rather than the
$\beta$-recursion formulation.

### 4.1 What "smoothed" means, precisely

$$\xi_{t\mid T}(j) \;=\; \Pr\!\big(S_t = j \;\big|\; r_1,\dots,r_t,\ \underbrace{r_{t+1},\dots,r_T}_{\text{the future}};\ \hat\theta\big)$$

The conditioning set is the **entire sample**. Docstring, `markov_switching.py:263-265`: "the
probability of being in each regime conditional on all information."

### 4.2 The backward recursion

Start from the terminal condition $\xi_{T\mid T}$ — the last filtered value, since at $t = T$
there is no future to add. Then recurse **backwards** for $t = T-1, \dots, 1$:

$$\boxed{\ \xi_{t\mid T}(j) \;=\; \xi_{t\mid t}(j)\,\sum_{i}
\frac{p_{ji}\;\xi_{t+1\mid T}(i)}{\xi_{t+1\mid t}(i)}\ }$$

**Derivation** (three lines, and the middle one is the only place an approximation could enter):

$$\xi_{t\mid T}(j) = \sum_i \Pr(S_t=j, S_{t+1}=i\mid\mathcal F_T)
= \sum_i \Pr(S_{t+1}=i\mid\mathcal F_T)\,\Pr(S_t=j\mid S_{t+1}=i,\mathcal F_T)$$

$$\Pr(S_t=j\mid S_{t+1}=i,\mathcal F_T) \;=\; \Pr(S_t=j\mid S_{t+1}=i,\mathcal F_t)$$

$$\Pr(S_t=j\mid S_{t+1}=i,\mathcal F_t)
= \frac{\Pr(S_t=j\mid\mathcal F_t)\,p_{ji}}{\Pr(S_{t+1}=i\mid\mathcal F_t)}
= \frac{\xi_{t\mid t}(j)\,p_{ji}}{\xi_{t+1\mid t}(i)}$$

The middle step drops $r_{t+1},\dots,r_T$ from the conditioning set. It is valid iff
$\{r_{t+1},\dots,r_T\} \perp S_t \mid S_{t+1}$ — which holds **exactly** for a plain HMM, where
the emission depends only on the contemporaneous state. Our emission does
(`markov_regression.py:190-191`), `self.order = 0`, so **the Kim smoother is exact here**, not
an approximation. (It becomes an approximation for Markov-switching autoregressions where
$f(r_t\mid\cdot)$ depends on lagged regimes; that is the caveat Kim 1994 discusses and it does
not apply to us.)

Every factor is already available from the forward pass: $\xi_{t|t}$ from Step 2, $\xi_{t+1|t}$
from Step 1. That is why the smoother costs one extra $O(Tk^2)$ sweep and no extra filtering.

**Log-space form**, matching `cy_kim_smoother_log`:

$$\log\xi_{t\mid T}(j) = \log\xi_{t\mid t}(j)
+ \operatorname*{logsumexp}_{i}\big[\log p_{ji} + \log\xi_{t+1\mid T}(i) - \log\xi_{t+1\mid t}(i)\big]$$

`markov_switching.py:932-933` passes `predicted_joint_probabilities_log` and
`filtered_joint_probabilities_log` — the log arrays deliberately retained at
`markov_switching.py:214-216` — which are exactly the $\log\xi_{t+1|t}$ and $\log\xi_{t|t}$ terms
above (as pairwise joints, per Section 1.1). Line `markov_switching.py:283` logs the transition
matrix with the same $10^{-20}$ floor; lines `markov_switching.py:300-303` marginalize the
redundant axis to get `smoothed_marginal_probabilities`.

Sanity check on the terminal condition: verified on the current fit,
`filtered[-1] == smoothed[-1]` exactly ($0.00144603$).

### 4.3 Why smoothed probabilities are look-ahead bias for a trading signal

**Status: resolved in code.** `estimate_jump_regimes` returns
`results.filtered_marginal_probabilities` (`src/jump_model.py:163`), guarded by two assertions
at `checks.py:142-149` — one that the returned series matches the filtered array, one that it
does *not* match the smoothed array. The argument below is retained because it is the reason for
that choice and because the second-order leak it identifies is still open.

Read the definition in 4.1 again: $\xi_{t\mid T}$ at week $t$ is computed using weeks $t+1$
through $T$. In a backtest that walks forward through history, the value at 2008-09-15 would be
informed by 2008-10-10, 2009-03-06, and every week since. **You cannot have known it at the
time.** Any Sharpe ratio computed from a signal built on $\xi_{t|T}$ is fiction.

**How big the gap actually is (real, `diagnostics.py:751-759`):**
$\max_t|\xi_{t|t} - \xi_{t|T}| = 0.704014$ (on 2025-03-24), mean $0.109884$, and **170 of 1750
weeks (9.71%) disagree about the $0.50$ threshold** — roughly one week in ten would have been
assigned a different risk tier. That is the measured size of the bug that was fixed.

Smoothed probabilities are the *correct* object for the retrospective questions — "was
2011-08 a crisis regime?", "how many crisis episodes since 1993?", "what was their duration
distribution?" — and are the standard choice for historical business-cycle dating (Hamilton
1989's original application). They are the *wrong* object for a signal.

The synthetic table in Section 2.5 makes the mechanism visible:

- **Week 99** (one week before the true jump): filtered $0.002448$, smoothed $0.212773$. The
  smoother has already caught an $87\times$ whiff of the crisis from data that had not happened.
  This is anticipation, and on real data with less clean regime edges it is much larger.
- **Week 110** (one week after): filtered $0.542069$, smoothed $0.136462$. The smoother knows
  calm resumed and retroactively suppresses the alarm; the filter, correctly, does not yet know
  and sits just above the coin-flip. The filter's slower exit is *the honest picture of what
  you'd have seen*.

**A second, subtler leak that survives the fix, and is still open.** Returning
`filtered_marginal_probabilities` removes the *state* look-ahead but not the *parameter*
look-ahead. $\hat\theta$ is still estimated on $r_1,\dots,r_T$ — the whole sample. So
$\xi_{t|t}(\hat\theta)$ conditions on data up to $t$ *given parameters* that saw everything.
$\hat\sigma_{j^\star}^2$ in particular is largely determined by the worst weeks in the sample;
using it to score a week before those happened is still cheating, just quietly.

Genuine out-of-sample evaluation requires **expanding-window (recursive) refitting**:

1. Fit on $r_1,\dots,r_s$ only.
2. Take $\xi_{s|s}$ from *that* fit — the last filtered value, which uses no data after $s$ and
   parameters that saw no data after $s$.
3. Record it as the week-$s$ signal. Advance $s$, refit, repeat.

Cost: one full fit per week. With 50 `search_reps` and ~1700 weeks of SPY history that is
substantial but entirely feasible offline; it is the only way to get a defensible backtest. The
literature term is **real-time / recursive out-of-sample evaluation**; Chauvet & Piger (2008)
do exactly this for Markov-switching recession dating and quantify how much the smoothed-vs-
real-time gap costs, which is the closest published analogue to this repo's question.

Two things to watch when you build it: (a) parameter paths will be unstable in the early
windows, so set a minimum burn-in well above the `MIN_OBSERVATIONS = 10` floor at
`src/jump_model.py:11`, `63-67`; (b) each refit is a fresh optimization with its own
label-switching risk, so **the jump-regime index must be recomputed per window** and never
cached across refits. `fit_jump_model` already returns it alongside the results
(`src/jump_model.py:138`), so the correct loop consumes the tuple rather than assuming an index
— the whole point of Section 7.3. A third thing: `initialize_known` is the natural way to chain
windows and it applies $\Pi$ twice (Section 2.4).

---

## 5. Model selection

### 5.1 AIC and BIC as statsmodels computes them

$$\text{AIC} = -2\,\ell(\hat\theta) + 2k, \qquad
\text{BIC} = -2\,\ell(\hat\theta) + k\log T$$

`markov_switching.py:1818-1824` and `1826-1832`, both passing `self.params.shape[0]` as $k$ —
i.e. **the length of the parameter vector**, with no adjustment for restrictions.

**For the current specification, that count is correct.** Nothing is pinned, so
`k_params = 6` free parameters is the honest number, and the reported and corrected criteria
coincide. `diagnostics.py:390-403` verifies this rather than assuming it, reconciling
`model.k_params` against an explicitly written-down `k_free` for every spec it fits and printing
$|\Delta\text{AIC}|$ and $|\Delta\text{BIC}|$; all three switching specs return $0.00\text{e}{+}00$.

Synthetic fit, $\ell = 475.3433$, $T = 150$, $k = 6$: AIC $= -938.6865$, BIC $= -920.6227$.
**Real** fit, $\ell = 4310.9380$, $T = 1750$, $k = 6$: AIC $= -8609.8760$,
BIC $= -8577.0718$.

**Audit record: the parameter-count subtlety under pinned parameters.** Under the superseded
spec, $p_{00}$ was assigned by fiat and never estimated — confirmed by
$\partial\ell/\partial\tilde p_{00} \equiv 0$ (Section 3.5b) — so the free-parameter count was
$k = 4$, not the $5$ statsmodels reported: $(p_{10},\ \mu,\ \sigma_0^2,\ \sigma_1^2)$. Three
distinct cases are worth separating, because they are easy to conflate:

- A **point restriction** (the pin) removes exactly one degree of freedom. $k$ drops by 1.
- An **inequality restriction** (the persistence ceiling) costs nothing while slack, and is a
  boundary case when it binds — which it did, exactly, on real SPY. At a binding boundary the
  effective count is arguably $3$, and more importantly the parameter's limiting distribution is
  no longer normal, so no $k$ makes the usual asymptotics apply.
- An **ordering constraint** costs nothing at all. It is a labelling convention: it removes a
  redundant duplicate mode from the likelihood surface, not a dimension from the parameter
  space. This is the same fact that makes post-hoc relabelling legitimate (Section 7.3).

### 5.2 (audit record) Why the miscount was not a harmless constant offset

It would be harmless if you only ever compared a model to itself. You do not — AIC/BIC exist to
choose *between specifications*, and the size of the error **differed by specification**:

| Specification | $k$ statsmodels reports | $k$ actually free | Overstatement |
|---|---|---|---|
| **2 regimes, current repo spec (switching mean)** | **6** | **6** | **0** |
| 2 regimes, common mean, unrestricted | 5 | 5 | 0 |
| 3 regimes, common mean, unrestricted | 10 | 10 | 0 |
| 1 regime (plain Gaussian i.i.d.) | 2 | 2 | 0 |
| *Superseded: 2 regimes, $p_{00}$ pinned + ceiling* | 5 | 4 (3 at the boundary) | **1–2** |

(Counts follow `markov_switching.py:530-535` and `markov_regression.py:140-141`: $k(k-1)$
transition parameters, $1$ intercept if non-switching or $k$ if switching, $k$ variances if
switching. For $k=3$ with a common mean: $6 + 1 + 3 = 10$.)

The offset was $+2$ in AIC and $+\log T$ in BIC for the pinned row and $0$ for the others. So
every comparison that crossed a pinned/unpinned boundary was biased — and biased *against* the
constrained model, which was the one being defended. **Historical (superseded spec):** on the
synthetic data statsmodels reported AIC $-937.02$ (constrained) versus $-937.68$
(unrestricted, common mean), suggesting the unrestricted model was better; with correct counts
it was $-939.02$ versus $-937.68$ and the ranking **flipped**. A single unit of $k$ decided the
comparison. Neither figure is reproducible today.

The general principle survives the respecification: AIC/BIC penalties must count *effective
degrees of freedom*, and a parameter fixed by fiat has none. The habit `diagnostics.py` keeps —
compute AIC/BIC yourself from `res.llf` and an explicit $k$, then *check* it against `res.aic`
rather than replacing it — is cheap and is what turned the agreement above into a verified fact
rather than an assumption.

### 5.3 Testing the number of regimes is a non-standard problem

The obvious move — likelihood-ratio test of $k=1$ against $k=2$, refer $2\Delta\ell$ to
$\chi^2_{\nu}$ — **is invalid**, and not marginally so.

Under $H_0: k=1$, the 2-regime model is unidentified in three ways at once:

1. **Nuisance parameters unidentified under the null.** Set $\sigma_0^2 = \sigma_1^2$ and the
   transition probabilities $p_{00}, p_{11}$ vanish from the likelihood entirely — any values
   give the identical fit. Wilks' theorem requires all parameters identified under $H_0$.
2. **Parameters on the boundary.** Alternatively reach the null by $\pi_1 \to 0$, i.e.
   $p_{11} \to 0$ or $p_{01}\to 0$ — a boundary of the parameter space. Boundary nulls give
   mixtures of $\chi^2$ distributions at best (Chernoff 1954, Self & Liang 1987).
3. **Zero score.** At the null, the first derivative of $\ell$ with respect to the
   mixing direction is identically zero, so the usual quadratic expansion of $\ell$ around
   $H_0$ degenerates and higher-order terms drive the asymptotics.

Any one of these breaks $\chi^2$. All three together mean the LR statistic's null distribution
is **not** $\chi^2$ with any degrees of freedom, and using $\chi^2$ **massively over-rejects** —
you will "find" regimes in i.i.d. Gaussian noise.

What to use instead:

- **Hansen (1992)**, *Journal of Applied Econometrics* 7(S1), S61–S82: treats the LR statistic
  as an empirical process indexed by the unidentified nuisance parameters and computes a bound
  on its distribution by simulation. The standardized-LR-as-a-process framing is the canonical
  reference; see also Hansen (1996) on the general "testing when a nuisance parameter is present
  only under the alternative" problem.
- **The Davies bound** (Davies 1977, 1987): $\sup_\gamma$ of a test statistic over a nuisance
  parameter $\gamma$ has an upper $p$-value bound derived from the expected number of upcrossings
  of the process. Cheap, conservative, and the standard first line of defence.
- **Garcia (1998)**, *International Economic Review* 39(3): derives the asymptotic null
  distribution for the Markov-switching case specifically, under the boundary-of-parameter-space
  route.
- **Cho & White (2007)**, *Econometrica* 75(6): quasi-LR test for regime switching.
- **Carrasco, Hu & Ploberger (2014)**, *Econometrica* 82(2): an optimal test for parameter
  instability that is *asymptotically* valid and computationally cheap, avoiding the need to
  estimate the switching model at all under $H_0$.
- **Parametric bootstrap.** Practically, the most defensible route for one specific comparison:
  simulate $B$ samples of length $T$ from the fitted 1-regime model, refit both specifications
  to each, and read the LR statistic's null distribution off the $B$ draws. Slow, assumption-
  light, easy to get right.

**In contrast**, testing the *switching mean* is standard: $H_0:\ \mu_0 = \mu_1$ is a single
point restriction on identified parameters at an interior point, with the number of regimes held
fixed at two, so
$2[\ell_{\text{unrestricted}} - \ell_{\text{restricted}}] \xrightarrow{d} \chi^2_1$.
`diagnostics.py:415-424` runs exactly this, and flags in a comment that it is *not* a test of
the number of regimes.

- **Real:** $2(4310.9380 - 4305.8504) = \mathbf{10.1751}$, $p = \mathbf{0.001423}$ against a
  $\chi^2_1$ critical value of $3.841$. **The common mean is rejected.** This is the evidence
  that justified `switching_trend=True`.
- Synthetic: $2(475.3433 - 473.8417) = 3.0032$, $p = 0.0831$. Not rejected — as it should not
  be, because `checks.py:41-43` draws the calm blocks at $+0.001$ and the jump block at
  $-0.02$ with only 10 jump observations, which is too little data to resolve a mean shift.
  Another reminder that the fixture is a control, not evidence.

**Why an insignificant $\hat\mu_{j^\star}$ is compatible with a rejected $\mu_0 = \mu_1$.** The
real fit reports `const[0]` $= -0.00259686$ with std err $0.00188989$, $z = -1.374$,
$p = 0.169$ — individually **not** significant, and its 95% CI $(-0.00630,\ 0.00111)$ contains
zero. There is no contradiction, because the two tests ask different questions:

$$\text{Wald on } \texttt{const[0]}: \ H_0:\ \mu_{j^\star} = 0
\qquad\text{versus}\qquad
\text{LR}: \ H_0:\ \mu_{j^\star} = \mu_{\text{calm}}$$

The LR statistic tests the *contrast* $\mu_0 - \mu_1$, not either level. That contrast is
$-0.00623172$ and it is estimated far more precisely than $\mu_{j^\star}$ alone relative to its
own size, because the calm mean is pinned down by 1344 quiet weeks
($\text{se} = 0.000458$) while the jump mean is not. Computing the contrast's standard error
properly from the covariance matrix, $\operatorname{Var}(\hat\mu_0 - \hat\mu_1) =
V_{00} + V_{11} - 2V_{01}$ with $V_{01} = -5.10\times10^{-8}$ (correlation $-0.059$), gives
$\text{se} = 0.00197070$ and a Wald $z = -3.1622$, $p = 0.001566$ — within rounding of the LR's
$p = 0.001423$, exactly as the asymptotic equivalence of Wald and LR predicts ($z^2 = 10.0$
against LR $= 10.18$). Zero sits comfortably inside `const[0]`'s interval; $+0.363\%$/wk does
not. **Read contrasts, not coefficients, when the hypothesis is about a difference.**

**Audit record.** The same $\chi^2_1$ argument applied to the superseded $p_{00} = 0.98$ pin —
also a point restriction at an interior value of an identified parameter. On synthetic data it
gave $2(473.8417 - 473.5077) = 0.668 < 3.841$, not rejected. On **real** SPY it gave
$\mathbf{14.07}$, $p = 1.8\times10^{-4}$: **the pin was decisively rejected**, with the
unrestricted $p_{00} = 0.923$ falling far *below* the pinned $0.98$. Recorded because the
synthetic result was initially read as vindication and the real-data result reversed it. Two
caveats applied to the constrained side of that comparison and are worth carrying forward: the
restricted "maximum" was not reliably the constrained maximum (Section 3.5a–b), and the
restricted and unrestricted fits sat in mirror-image label basins, which does not affect the
maximized value but does make a naive element-wise diff of the parameter vectors meaningless.

---

## 6. Residual diagnostics that do apply

### 6.1 Regime-standardized residuals

The specification says $r_t = \mu_{S_t} + \sigma_{S_t}\varepsilon_t$ with $\varepsilon_t$ i.i.d.
$\mathcal N(0,1)$. So the object to test is

$$z_t \;=\; \frac{r_t - \hat\mu_{S_t}}{\hat\sigma_{S_t}}$$

which under correct specification is i.i.d. standard normal. Note the numerator: with a
switching mean, subtracting a single sample mean is wrong and will manufacture skew. Two ways to
pick $\hat\mu_{S_t}, \hat\sigma_{S_t}$:

- **Hard classification**: $\hat S_t = \arg\max_j \xi_{t|t}(j)$ (or $\xi_{t|T}$), then
  $z_t = (r_t-\hat\mu_{\hat S_t})/\hat\sigma_{\hat S_t}$. Simple; discards classification
  uncertainty and is the primary version reported below. `diagnostics.py:545-546`.
- **Probability-weighted (mixture moments)**: standardize by the moments of the *mixture*, not
  by a mixture of the variances. With a switching mean the spread between the two means is
  itself part of the conditional variance, so the correct pair is
  $$m_t = \sum_j \xi_{t|t}(j)\,\hat\mu_j, \qquad
  v_t = \sum_j \xi_{t|t}(j)\big(\hat\sigma_j^2 + \hat\mu_j^2\big) - m_t^2$$
  which is the law of total variance, $E[\operatorname{Var}] + \operatorname{Var}[E]$. Dropping
  the second term — the common shortcut $v_t = \sum_j \xi_{t|t}(j)\hat\sigma_j^2$ — understates
  the variance whenever the regime is uncertain *and* the means differ. `diagnostics.py:549-551`
  implements the correct version. Note $z_t$ is then not exactly standard normal even under
  correct specification, because a mixture of scaled normals is not normal; test it against a
  simulated reference rather than $\mathcal N(0,1)$. Empirically it is the *worse* diagnostic
  here (sd $0.857$, excess kurtosis $0.965$ on real data, against $1.008$ and $0.476$ for hard
  assignment), which is that non-normality showing up.

`diagnostics.py` section D computes both, on the **filtered** probabilities. For the
retrospective, use $\xi_{t|T}$; to diagnose the *signal*, use $\xi_{t|t}$ — the two disagree in
9.71% of weeks (Section 4.3) and the filtered version is the one whose failures matter
operationally.

### 6.2 Normality: QQ plot and Jarque–Bera

$$\text{JB} = \frac{T}{6}\left(\widehat{\text{skew}}^2 + \frac{(\widehat{\text{kurt}} - 3)^2}{4}\right)
\;\xrightarrow{d}\; \chi^2_2 \quad\text{under } H_0:\ z_t \sim \mathcal N$$

Jarque & Bera (1980). Available as
`statsmodels.stats.stattools.jarque_bera`. Read the QQ plot alongside it — JB gives you one
number, the QQ plot tells you *where* the failure is, and for this model the informative region
is the tails. A QQ plot that is straight in the body and bends only in the extreme left tail
means the two-variance mixture handles ordinary weeks but not genuine tail events; the fix is
Student-$t$ emissions, not a third regime.

**Interpretation caution.** Raw returns $r_t - \bar r$ are *supposed* to be leptokurtic — that
is the mixture doing its job. It is only $z_t$, after centring and dividing by the
regime-specific $\hat\mu, \hat\sigma$, that should be normal. If $z_t$ is still fat-tailed, the
mixture has not absorbed all the kurtosis, and the natural extension is a **Markov-switching
model with $t$-distributed innovations** (Klaassen 2002; Haas, Mittnik & Paolella 2004).

Synthetic check: $\hat z$ has mean $0.0002$, sd $1.0111$, skew $0.187$, excess kurtosis $0.286$;
JB $= 1.385$, $p = 0.500$. Passes — as it must, since `checks.py:37-46` generates data from
exactly this specification. **This is a control, not evidence** (Section 8.6).

**Real:** JB $= \mathbf{28.285}$, $p = 7.21\times10^{-7}$, skew $-0.2006$, excess kurtosis
$0.4764$, on $n = 1750$. **Rejected.** Two-regime switching still absorbs the overwhelming
majority of the raw non-normality — excess kurtosis falls from $8.078$ to $0.476$, a 94%
reduction — but what remains is a statistically decisive left skew. The QQ table
(`diagnostics.py:235-245`) localizes it: the right tail sits close to the Normal line
($|\text{diff}| \le 0.096$ at every percentile $\ge 75$) while the left tail runs long
($-0.080$ at p5, $-0.101$ at p1). Crashes are still fatter than two Gaussian regimes allow.

**This got worse, not better, at the respecification.** JB was $22.04$ and excess kurtosis
$0.221$ under the superseded constrained fit. Section 8.2 explains why, and why the direction of
that change is not the indictment it looks like.

### 6.3 Ljung–Box on $z_t$: leftover serial correlation in the level

$$Q(m) = T(T+2)\sum_{h=1}^{m}\frac{\hat\rho_h^2}{T-h} \;\xrightarrow{d}\; \chi^2_m$$

Ljung & Box (1978), on $\hat\rho_h = $ sample autocorrelation of $z_t$ at lag $h$. $H_0$: no
autocorrelation up to lag $m$. Rejection means predictable *level* dynamics the model omits —
the extension would be a Markov-switching AR (`MarkovAutoregression`, which sets `order > 0`
and makes the Kim smoother approximate rather than exact, per Section 4.2). Weekly equity
returns rarely reject this; if yours does at short lags, suspect the data pipeline (overlapping
or misaligned weekly bars from `interval="1wk"` at `src/data_loader.py:43-50`) before you
suspect the model. Here the pipeline checks out: `diagnostics.py:286-291` reports every index
spacing is exactly 7 days, zero non-7-day gaps, over all 1750 weeks.

Synthetic: $Q(4) = 6.96\ (p=0.138)$, $Q(8) = 12.41\ (p=0.134)$. Passes.

**Real:** $Q(4) = 17.480\ (p = 0.00156)$, $Q(8) = 23.584\ (p = 0.00269)$,
$Q(12) = 28.567\ (p = 0.00457)$, $Q(26) = 39.176\ (p = 0.0469)$. **Rejects at every lag
reported**, and this is essentially unchanged from the superseded fit — the switching mean did
not help here, which makes sense: a regime-dependent *level* is not an autoregression. The
honest reading is that weekly SPY has some level predictability this model does not attempt to
capture, and the natural extension is `MarkovAutoregression`. Note it is much milder than the
squared-residual failure below ($Q(4) = 17.5$ versus $70.0$); the level is a nuisance, the
variance is the problem.

### 6.4 ARCH-LM on $z_t$: the diagnostic that actually decides this model's fate

Engle (1982). Regress the squared standardized residual on its own lags:

$$z_t^2 = \alpha_0 + \sum_{k=1}^{q}\alpha_k z_{t-k}^2 + u_t,
\qquad \text{LM} = T R^2 \;\xrightarrow{d}\; \chi^2_q
\quad\text{under } H_0:\ \alpha_1=\dots=\alpha_q=0$$

`statsmodels.stats.diagnostic.het_arch`, `diagnostics.py:214-220`. Equivalently, Ljung–Box on
$z_t^2$ tests the same hypothesis with a different statistic; report both, they rarely disagree.

Synthetic: LM$(4) = 6.42$, $p = 0.170$; LM$(8) = 11.75$, $p = 0.163$; Ljung–Box on $z_t^2$:
$Q(4) = 5.62\ (p=0.229)$, $Q(8) = 10.07\ (p=0.260)$. Again a control, not evidence.

**Real, and this is the finding that decides the specification's fate:**

| Statistic | Superseded constrained fit | **Current fit** | $p$ (current) |
|---|---|---|---|
| ARCH-LM(4) on $z_t$ | $41.11$ | $\mathbf{55.652}$ | $2.372\times10^{-11}$ |
| ARCH-LM(12) on $z_t$ | $48.91$ | $\mathbf{78.830}$ | $6.897\times10^{-12}$ |
| Ljung–Box(4) on $z_t^2$ | $49.68$ | $\mathbf{69.955}$ | $2.320\times10^{-14}$ |

For scale, the same statistics on *raw* returns are ARCH-LM$(4) = 231.85$ and Ljung–Box$(4)$ on
squares $= 350.06$. So the model absorbs roughly 76–80% of the volatility clustering and leaves
the rest, which is still overwhelmingly significant. Section 8.2 works through why the number
went *up* after respecification and why that does not mean the old spec was better.

**Why this is the sharpest test of the whole specification.** Read what a rejection means. The
model asserts that conditional volatility takes exactly **two discrete values**,
$\hat\sigma_{\text{calm}}$ and $\hat\sigma_{j^\star}$ — $1.50\%$ and $3.84\%$ per week on real
data. It is a step function. The competing hypothesis is that volatility moves on a
**continuum**, drifting and clustering *within* what this model calls a single regime. If that
is true, then dividing by a constant $\hat\sigma_j$ across an entire episode leaves the
clustering intact, and $z_t^2$ stays autocorrelated. ARCH-LM on $z_t$ is therefore a direct test
of

> *are two variance levels enough, or is volatility continuous?*

and it is the only diagnostic in this list that asks that question.

The relevant literature is the long-running **regime-switching versus GARCH** debate:

- **Hamilton & Susmel (1994)**, *Journal of Econometrics* 64(1–2), 307–333 — **SWARCH**:
  Markov-switching ARCH, i.e. an ARCH process whose *scale* shifts with a latent regime. This is
  the canonical hybrid and the direct answer to a failing ARCH-LM. Read it first.
- **Cai (1994)**, *JBES* 12(3) — the other simultaneous SWARCH paper.
- **Gray (1996)**, *Journal of Financial Economics* 42(1) — regime-switching GARCH with a
  tractable recombining likelihood, sidestepping the path-dependence problem that makes exact
  MS-GARCH intractable.
- **Klaassen (2002)**, *Empirical Economics* 27(2) — improvement on Gray using the full
  filtered probability vector; also handles $t$ innovations.
- **Haas, Mittnik & Paolella (2004)**, *Journal of Financial Econometrics* 2(4) — the modern
  MS-GARCH formulation with parallel regime-specific variance processes.
- **Diebold (1986)** and **Lamoureux & Lastrapes (1990)** — the *reverse* direction of the same
  argument: unmodelled structural breaks and regime shifts inflate estimated GARCH persistence
  toward IGARCH. The two literatures each diagnose the other's residuals, which is why you
  should read one of these before concluding that a failing ARCH-LM means "use GARCH instead".
- **Ang & Timmermann (2012)**, *Annual Review of Financial Economics* 4 — survey; the place to
  start for how practitioners actually choose between the two.

**How to react, now that it has rejected.** Three options, and the mandate constrains which are
open:

1. **Add regimes** ($k=3$: calm / stressed / crisis). Cheapest change, keeps the discrete-state
   framing, and the information criteria already prefer it decisively (Section 8.5). But it
   costs $2k$ new parameters, the number-of-regimes test is non-standard (Section 5.3), it
   multiplies the label-switching problem from $2!$ to $3!$ modes, and it does not address the
   root cause — three constant variances are still a step function.
2. **GARCH within regimes** — **SWARCH** (Hamilton & Susmel 1994) or MS-GARCH. Statistically the
   right answer if volatility really is continuous, and the standard-literature response to
   exactly this diagnostic. It is likelihood-based, so `README.md`'s methodological ban does not
   exclude it, but `README.md:15` commits to "purely likelihood-based time-series modelling via
   a 2-regime switching model", so it is a change of specification, not a tweak.
3. **Accept the misspecification deliberately.** `README.md:16-17` wants a *coarse, sticky*
   thermostat with three discrete action tiers and explicitly does not want a continuous
   volatility forecast. A 2-state model that fails ARCH-LM can still be a perfectly good switch:
   it throws away within-regime volatility variation *on purpose*.

Option 3 is defensible — but only if you know the magnitude of what you are discarding. "It
fails ARCH-LM with LM $= 8$" and "it fails with LM $= 56$" are different situations, and the
measured value is $55.65$ at 4 lags and $78.83$ at 12. The thermostat is discarding a large and
statistically unambiguous amount of structure. Whether that matters is a *decision-value*
question, not a likelihood question, and the cheapest way to answer it is the benchmark against
trailing realized volatility recorded as the top priority in `core-risk-overlay.md`.

### 6.5 Two diagnostics specific to regime-switching models

**Regime classification measure (RCM).** Ang & Bekaert (2002). For $k$ regimes,
$\text{RCM} = 100\,k^k\,\frac{1}{T}\sum_t\prod_j \xi_{t|T}(j)$; for $k=2$ this is

$$\text{RCM} = \frac{400}{T}\sum_{t=1}^{T}\hat p_t\,(1 - \hat p_t), \qquad \hat p_t = \xi_{t\mid T}(1)$$

$0$ = perfectly sharp classification (every $\hat p_t \in \{0,1\}$), $100$ = no information
(every $\hat p_t = 0.5$). Directly relevant here: a thermostat whose probabilities hover in the
21–60% "building stress" band (`README.md:47`) is one with a high RCM, and RCM tells you whether
that is the *market* being ambiguous or the *model* being uninformative. Computed at
`diagnostics.py:560-562` on **filtered** probabilities, matching the signal.

Synthetic: RCM $= 3.47$ filtered, $1.84$ smoothed — near-perfect separation, because the fixture
has a $37.7\times$ variance ratio. **Real: RCM $= 33.53$**, up from $25.78$ under the superseded
fit. A third of the way to uninformative. Section 8.4 treats this as an open finding.

**Duration realism.** Compare fitted $1/(1-\hat p_{ii})$ against the empirical distribution of
run lengths in $\hat S_t$, and against the calendar (Section 1.5, `diagnostics.py:594-644`).
This is the cheapest diagnostic in this document. It now runs on every `diagnostics.py`
invocation and it is what showed that the superseded persistence ceiling could not express the
GFC as one episode.

---

## 7. Identifiability and label switching

### 7.1 The problem

The likelihood of a mixture or Markov-switching model is **invariant to permutation of the
regime labels**. Relabel $0 \leftrightarrow 1$ *everywhere consistently* — swap **both**
regime-specific parameter pairs (the means and the variances) **and** transpose-permute the
transition matrix — and you get an identical value of $\ell$.

For $k=2$ the permuted parameter vector is

$$\theta' = (\,p_{11},\ p_{01},\ \mu_1,\ \mu_0,\ \sigma_1^2,\ \sigma_0^2\,)
\qquad\text{i.e.}\qquad p'_{00} = p_{11} = 1 - p_{10},\quad p'_{10} = p_{01} = 1 - p_{00}$$

Verified numerically on the current synthetic fit. Ordering is
$(p_{00},\ p_{10},\ \mu_0,\ \mu_1,\ \sigma_0^2,\ \sigma_1^2)$:

```
theta  = [0.99195970, 0.11427967,  0.00057463, -0.02935889, 7.132980e-05, 2.6871139e-03]
theta' = [0.88572033, 0.00804030, -0.02935889,  0.00057463, 2.6871139e-03, 7.132980e-05]

loglike(theta)  = 475.3432711040538834
loglike(theta') = 475.3432711040538834
difference      = 0.0   exactly
```

Not close — **bit-identical**, to the last stored digit. This is exact algebraic invariance, not
a numerical coincidence: the permutation acts on the filter's state indices, and every sum in
the recursion of Section 2.2 is over all states, so relabelling permutes the summands and
nothing else.

Consequences: the likelihood has $k! = 2$ global maxima; regime *indices* carry no meaning
without an extra convention; and any statement of the form "regime 1 is the jump regime" is a
claim that must be **derived from the fit**, never assumed. Section 3.4 shows fits landing in
either basin on real data. The canonical reference for the whole topic is
Frühwirth-Schnatter (2006), *Finite Mixture and Markov Switching Models*, ch. 3 (identifiability)
and ch. 3.7 / ch. 11 (label switching in practice).

The Markov structure does **not** rescue identifiability, though it is worth knowing what it
does buy: transition dynamics make the *model* identified up to permutation (the joint
distribution of $(r_t, r_{t+1})$ pins down more than the marginal mixture does), which is why
you can get away with a labelling convention rather than needing informative priors. But it
leaves the $k!$ permutation exactly free.

### 7.2 Standard remedies

| Remedy | Mechanism | Trade-off |
|---|---|---|
| **Ordering (identifiability) constraint** | Restrict $\Theta$ to a region containing one representative per permutation orbit, e.g. $\sigma_0^2 \le \sigma_1^2$ or $\mu_0 \le \mu_1$ | Standard and clean *if* implemented smoothly, i.e. as a reparameterization. Choose the ordering variable that actually separates the regimes — here, variance. Frühwirth-Schnatter (2006) §3.2 |
| **Post-hoc relabelling** | Estimate freely; permute the fitted output so the higher-variance regime is the jump regime | **What this repo does** (Section 7.3). Trivially correct for MLE: one fit, one permutation, no effect on the optimization. Its classic weakness — that it cannot express a constraint you need to hold *during* the fit — does not apply, because labelling is not such a constraint |
| **Random-permutation sampling / relabelling algorithms** | For MCMC: deliberately permute labels each sweep to explore all modes, then relabel the posterior draws (k-means in parameter space, or Stephens' 2000 relabelling algorithm) | Bayesian only; the right answer if you go MCMC |
| **Prior-based / weakly informative priors** | Order-imposing or regime-distinguishing priors | Bayesian only; Frühwirth-Schnatter (2006) ch. 3.7 discusses at length |

Those four are the standard menu. For a single maximum-likelihood fit, the first two are the
live options and the choice between them is the subject of the next section.

### 7.3 Post-hoc relabelling — the repo's identification strategy

**The code.** `_jump_regime_index` (`src/jump_model.py:96-105`) reads
`sigma2[0]` and `sigma2[1]` off the fitted vector by position — via `model.param_names.index`,
because `results.params` is name-indexed when `endog` is a pandas Series — and returns
`argmax`. `fit_jump_model` returns it as the third element of `(model, results,
jump_regime_index)` (`src/jump_model.py:138`), and `estimate_jump_regimes` uses it to select the
column (`src/jump_model.py:166-170`). That is the entire mechanism. It runs once, after
`fit()`, and touches nothing the optimizer sees.

**Why that is the correct place to resolve it.** The argument is three steps and each one is
verified above:

1. **The likelihood is exactly invariant** to a joint permutation of the transition matrix and
   both regime-specific parameter pairs. Section 7.1: bit-identical $\ell$, difference exactly
   $0.0$.
2. **Therefore labelling is a naming indeterminacy, not a restriction on the model.** The two
   parameter vectors $\theta$ and $\theta'$ are two names for the same probability
   distribution over $(r_1,\dots,r_T)$. No observable quantity distinguishes them. A "constraint"
   that picks one is not narrowing the set of distributions under consideration — it is choosing
   a coordinate chart.
3. **Therefore it should be resolved after fitting, not by constraining the optimizer.** There
   is no wrong basin to keep the optimizer out of: both basins have the same height and describe
   the same model. Constraining the search buys nothing and, if done by projection rather than
   reparameterization, costs everything in Section 3.5.

**What this restores.** Because nothing intercepts $\theta$ between the optimizer and the
likelihood, the fitted point is an ordinary **interior stationary point of $\ell$ in the full
6-dimensional parameter space**. That is the precondition for every piece of standard MLE
inference, and it makes `res.bse`, `res.pvalues` and `res.conf_int()` legitimate again — they
now describe the model that was actually fitted, evaluated at a point where $\nabla\ell = 0$
(verified: $\max_i|g_i| = 2.8\times10^{-6}$, Section 3.1). `diagnostics.py:184-202` reports the
full table for the real fit, with the reason recorded in a comment at `diagnostics.py:185-187`.
Under the superseded specification the same call returned a standard error for a parameter that
had been assigned by fiat (Section 3.5d).

Note what post-hoc relabelling does **not** fix: it says nothing about whether $k=2$ is right,
whether the emissions are Gaussian, or whether the higher-variance regime deserves the name
"jump". Those are Section 8.

**The one operational hazard.** Because the index is data-dependent, it must be recomputed for
every fit and never cached. On the synthetic fixture $j^\star = 1$; on real SPY full history and
on the 2006–2011 window $j^\star = 0$. `diagnostics.py:513-515` prints "relabelling was
REQUIRED" for both real windows. A hardcoded index would have inverted the signal on live data —
maximum insurance in calm markets, none in crises — while every check in `checks.py` continued
to pass, because the fixture happens to land the other way. That asymmetry is the strongest
single argument for the design.

### 7.4 (audit record) The superseded ordering constraint

> **This section documents deleted code**, retained as the audit trail.

**What `sorted()` inside `transform_params` got right.** The choice of *ordering variable* was
correct: variance is what actually distinguishes the two states, so ordering on $\sigma^2$
identifies the labels reliably. And the underlying diagnosis — that the labels genuinely need
resolving, that the fit does land on the "wrong" index on real data — was right, and is
confirmed by `diagnostics.py` section C. This was not gratuitous complexity; it addressed a real
problem, and the current code addresses the same problem.

**What it got wrong, twice over.**

*Mechanically*: it implemented the standard remedy by the non-standard mechanism of
**projection**, and paid in three places — the objective lost differentiability at the ordering
boundary (3.5a), the complex-step gradient became branch-dependent and could attribute a
derivative to the wrong coordinate (3.5b), and the transform stopped being invertible, breaking
statsmodels' documented contract (3.5c). The literature's ordering constraint is a *restriction
of the domain*, implemented as a reparameterization; this was a *modification of the map*, and
those are not the same thing.

*Conceptually*: it treated a naming indeterminacy as if it were a restriction on the model, and
therefore reached for the one tool — constraining the optimizer — whose entire cost is paid
during optimization and whose entire benefit was available for free afterwards. Section 7.3
step 2 is the observation that was missing. The smooth reparameterization
$\sigma_1^2 = \sigma_0^2 + e^{\delta}$ would have removed the mechanical objection while leaving
the conceptual one intact: it is still a coordinate chart imposed on a search that did not need
one. Deleting the constraint is strictly simpler than fixing it.

**The related claim that was also wrong.** The deleted comment justified the *persistence*
constraints by asserting that on windows like 2006–2011 the unrestricted MLE pathologically
pairs high variance with high persistence. Tested on real SPY 2006-01-01..2011-12-31: the
unrestricted fit gives $E[D]$ of $17.22$ weeks for the high-variance regime against $44.66$ for
the low-variance one — high variance pairs with *low* persistence, the opposite of the claim.
Same on full history ($12.91$ versus $36.08$). The prescription (resolve the labels) was
load-bearing; the diagnosis (a persistence pathology) was fiction, and the two persistence
constraints rested on nothing else.

### 7.5 The switching mean does not fully fix sign-blindness

Under the superseded common-mean spec, the *only* thing distinguishing the regimes was scale, so
regime inference ran purely on $|r_t - \hat\mu|$ and a $+7\%$ week was exactly as strong
evidence of the jump regime as a $-7\%$ week. For a *tail-risk insurance* signal
(`README.md:8`) that is a direct premium leak: maximum insurance held through a violent rally.

`switching_trend=True` costs one parameter, lets the jump regime carry negative drift, and is
strongly supported by the data (LR $= 10.18$, $p = 0.0014$, Section 5.3). It also makes this
Hamilton (1989)'s original switching-mean specification with the later switching-variance
extension layered on. But **it does not make the signal sign-aware in practice**, and the reason
is a magnitude comparison rather than anything subtle. The conditional log-density difference
between the two regimes is

$$\log\frac{\eta_t(j^\star)}{\eta_t(\text{calm})}
= \underbrace{\tfrac12\log\frac{\sigma_{\text{calm}}^2}{\sigma_{j^\star}^2}}_{\text{constant}}
\;+\; \underbrace{\frac{(r_t-\mu_{\text{calm}})^2}{2\sigma_{\text{calm}}^2}
- \frac{(r_t-\mu_{j^\star})^2}{2\sigma_{j^\star}^2}}_{\text{quadratic in }r_t}$$

and the quadratic term is dominated by the $1/\sigma^2$ asymmetry, not by the $0.62\%$/wk gap
between the two means. With $\hat\sigma_{j^\star} = 3.84\%$/wk, that gap is $0.16$ jump-regime
standard deviations. **Real** measurements (`diagnostics.py:693-723`):

| Comparison | Mean $P(\text{jump})$, up | down | ratio (1.0 = fully sign-blind) |
|---|---|---|---|
| 5% percentile tails ($n = 88$ each) | $0.821163$ | $0.884911$ | $\mathbf{0.9280}$ |
| $\lvert r\rvert \ge 5\%$ | $0.983631$ | $0.996069$ | $\mathbf{0.9875}$ |
| $\lvert r\rvert \ge 7\%$ | $0.999974$ | $0.999998$ | $\mathbf{1.0000}$ |

The asymmetry that exists is concentrated in moderate moves ($\ge 3\%$: ratio $0.805$) and
vanishes entirely in the tail, which is the region a tail-risk overlay is built for. **5 of the
20 highest-probability weeks in 33 years still have positive returns** — 2008-11-24 ($+12.48\%$),
2020-04-06 ($+11.41\%$), 2008-10-27 ($+10.66\%$), 2020-03-23 ($+10.22\%$), 2009-03-09
($+9.90\%$) — all at $P(\text{jump}) \ge 0.99999999$. Those are bear-market rallies, so a
volatility detector is *correct* to flag them; the point is that a put-buying overlay sized off
this number buys most insurance at exactly the moments the rally is already underway. Recorded
as an open finding at Section 8.3; the honest fix is in `risk_engine.py`'s tier logic, not in
regime identification.

---

## 8. Known issues

Rewritten 2026-08-12 against the respecified code. The four findings that motivated the
respecification are **resolved** and are recorded in 8.1 with the mechanism that closed each.
Everything from 8.2 onwards is **OPEN** and was measured on real SPY after the respecification.

The uncomfortable summary: the specification is now internally sound — valid gradients, valid
standard errors, honest parameter counts, no unrepresentable regions — and it is still
**decisively rejected by its own residual diagnostics**. Fixing the machinery did not fix the
model.

### 8.1 RESOLVED by the 2026-08-12 respecification

Each item states the defect, the mechanism that closed it, and the guard that stops it
recurring. The mathematics is preserved in the audit-record sections cross-referenced; do not
delete those, they are why these are closed.

| # | Defect | Resolved by | Guard |
|---|---|---|---|
| 1 | Smoothed probabilities returned to a real-time consumer | `estimate_jump_regimes` returns `filtered_marginal_probabilities` (`src/jump_model.py:163`) | `checks.py:142-149` asserts the return matches filtered and does **not** match smoothed |
| 2 | AIC/BIC counted 5 parameters when 4 were free | The pin is gone; `k_params = 6` is now the honest count | `checks.py:110-113`; `diagnostics.py:390-403` reconciles `k_params` against an explicit `k_free` for every spec |
| 3 | `sorted()`/`max()` corrupted the complex-step gradient | No `transform_params` override exists; the objective is smooth in every coordinate | `checks.py:124-133` asserts $\max_i\lvert g_i\rvert < 10^{-3}$ and that no `Hinv` diagonal entry is still $1.0$ |
| 4 | `bse` / `pvalues` / `conf_int()` described an unfitted model | Post-hoc relabelling puts $\hat\theta$ at an interior stationary point of the *fitted* likelihood | `diagnostics.py:184-202` now reports the table, with the reason in a comment at `:185-187` |

**1 — the look-ahead leak.** $\xi_{t\mid T}$ conditions on $r_{t+1},\dots,r_T$ (Section 4.1),
and the weekly protocol at `README.md:41-48` consumed that value on Friday of week $t$ to size
option positions. Measured magnitude before the fix (**real**): $\max_t|\xi_{t|t}-\xi_{t|T}| =
0.704014$, mean $0.109884$, and **170 of 1750 weeks (9.71%) disagreed about the $0.50$
threshold**. Roughly one week in ten would have been assigned a different risk tier. Note the
second-order leak in Section 4.3 is **not** closed: filtered probabilities from a full-sample
fit still carry *parameter* look-ahead, and a defensible backtest needs expanding-window
refitting.

**2 — the parameter count.** `markov_switching.py:1824` and `1832` pass
`self.params.shape[0]`, which is correct only when every element is free. It now is. The
general habit — compute AIC/BIC from `res.llf` with an explicit $k$, then *check* against
`res.aic` — is retained in `diagnostics.py` precisely because the failure was silent. Section
5.1–5.2 keeps the arithmetic of what a pin, an inequality restriction, and an ordering
convention each cost.

**3 — the gradient.** `gopt[0]` was exactly `-0.0` and `Hinv[0,0]` exactly `1.0` — the
untouched BFGS identity initialization — with `warnflag = 0` and `converged = True`. The
mechanism is Section 3.5b: numpy orders `complex128` lexicographically, so at a variance tie
`sorted()` broke the tie on the *imaginary* (perturbation) part and credited the derivative to
the wrong coordinate, while `max(complex, float)` discarded the imaginary part outright. This
is the finding with the widest transfer: **a convergence flag cannot detect a coordinate the
optimizer never explored**, so assert on the gradient and the Hessian directly.

**4 — the standard errors.** `cov_params_approx` (`markov_switching.py:1834-1846`) calls
`self.model.hessian(self.params, transformed=True)`, and `hessian`
(`markov_switching.py:1010-1025`) is `approx_hess_cs(params, self.loglike)` with no `args` — so
`loglike` ran at `transformed=True` and `transform_params` was never called along the
differentiation path. The constraints lived in exactly the one method the covariance calculation
bypasses. The reported gradient of that surface at $\hat\theta$ was $(51.8, 0.0005, -0.075,
43.7, -0.043)$: not a stationary point of anything. Section 3.5d.

**Also resolved, incidentally:** the `search_reps` warm-start no longer explores a different
surface from the one BFGS maximizes (Section 3.4), and `transform_params ∘ untransform_params`
is once again exactly the identity (Section 3.2).

**Not resolved, deliberately unchanged:** `initialize_known` still applies $\Pi$ twice rather
than once (Section 2.4). It is a statsmodels behaviour, invisible under the default steady-state
initialization since $\Pi\pi = \pi$, and a live trap for the expanding-window refit that has not
been built yet.

### 8.2 OPEN — the residual battery still rejects, and got worse

The regime-standardized residuals $z_t$ are the object the specification claims are i.i.d.
$\mathcal N(0,1)$ (Section 6.1). They are not, and every statistic moved in the wrong direction
at the respecification:

| Statistic on $z_t$ (hard assignment, filtered) | Superseded spec | **Current spec** | $p$ (current) |
|---|---|---|---|
| ARCH-LM(4) | $41.11$ | $\mathbf{55.65}$ | $2.372\times10^{-11}$ |
| ARCH-LM(12) | $48.91$ | $\mathbf{78.83}$ | $6.897\times10^{-12}$ |
| Ljung–Box(4) on $z_t^2$ | $49.68$ | $\mathbf{69.96}$ | $2.320\times10^{-14}$ |
| Jarque–Bera | $22.04$ | $\mathbf{28.29}$ | $7.210\times10^{-7}$ |
| Excess kurtosis | $0.221$ | $\mathbf{0.476}$ | — |
| Ljung–Box(4) on the level | $\approx$ unchanged | $17.48$ | $0.00156$ |

Ljung–Box on the *level* is essentially unchanged and still rejects at every lag tested
($Q(4) = 17.48$ through $Q(26) = 39.18$, all $p < 0.05$) — a regime-dependent intercept is not
an autoregression, so there was no reason to expect it to move.

**Attribute the deterioration correctly.** It is tempting to read this table as "the old
specification fitted better". It did not. The old constraints — $p_{00}$ pinned at $0.98$ and
$p_{11}$ capped at $0.85$ — forced the jump regime to be **rare, short and extreme**: entry
fixed at 2%/week, average duration at most $6.67$ weeks, and therefore a much higher fitted
$\hat\sigma_{j^\star}$ to absorb the same crisis weeks in fewer of them. A rare/extreme
high-variance state incidentally flattens volatility clustering better, because it acts as a
crude outlier bucket: the worst weeks get divided by a very large $\hat\sigma$ and the leftover
$z_t^2$ series looks calmer. That flattering residual behaviour was **bought with**:

- a boundary solution — $p_{10}$ sat at exactly $0.15000000$, zero slack, so the ceiling was
  binding and the reported inference was invalid on those grounds alone;
- a region of outcome space the model could not reach — ergodic $P(\text{jump}) \le 11.76\%$
  against an observed $13.77\%$ (Section 1.4);
- **12 log-likelihood points**. The superseded fit reached $\ell \approx 4298.8$; the current
  unrestricted fit reaches $4310.94$. The data prefers the current specification by
  $2\Delta\ell \approx 24$, and it prefers it on both corrected information criteria.

So: the old numbers were a better *residual* score obtained by refusing to fit the data. Trading
$12$ log-likelihood points for a $25\%$ reduction in an ARCH-LM statistic that rejects at
$p < 10^{-8}$ either way is not a trade worth making.

**The implication is architectural, not a parameterization choice.** Both specifications are
rejected decisively by this battery, at $p < 10^{-8}$, in the same direction, with and without
constraints, with and without a switching mean. What they share is the thing being tested:
**discrete states with constant within-state variance**. If conditional volatility moves on a
continuum, dividing by a constant $\hat\sigma_j$ across an entire episode leaves the clustering
intact by construction, and no amount of re-parameterizing two constant variances will change
that. Adding a third regime (Section 8.5) makes the step function finer but does not make it a
continuum.

The standard-literature response is **SWARCH** — Hamilton & Susmel (1994), "Autoregressive
Conditional Heteroskedasticity and Changes in Regime", *Journal of Econometrics* 64(1–2),
307–333: an ARCH process whose scale shifts with a latent Markov regime. It is likelihood-based,
so `README.md`'s methodological ban does not exclude it, but it is a specification change rather
than a tweak. See Section 6.4 for the three options and their trade-offs, and
`core-risk-overlay.md` for why the realized-volatility benchmark should be run *before* any of
them.

### 8.3 OPEN — sign-blindness persists

`switching_trend=True` was adopted specifically to make the signal aware of the sign of the
return, and it is statistically justified (LR $= 10.1751$, $p = 0.001423$, Section 5.3). It does
not deliver the behaviour it was adopted for.

**Math.** The mean spread jump-minus-calm is $0.623\%$/wk against
$\hat\sigma_{j^\star} = 3.84\%$/wk — $0.16$ jump-regime standard deviations. The conditional
density difference stays dominated by the squared-deviation term (Section 7.5).

**Real measurements.** Big-up versus big-down weeks score $\mathbf{92.80\%}$ as similar at the
5% percentile tails, $\mathbf{98.75\%}$ at $|r| \ge 5\%$, and $\mathbf{100.00\%}$ at
$|r| \ge 7\%$. The residual asymmetry lives entirely in moderate moves and vanishes in the tail
— the opposite of the profile a tail-risk overlay needs. **5 of the top 20 filtered-probability
weeks have positive returns**, all above $P = 0.99999999$.

**Why this is a live cost.** For a put-buying overlay (`README.md:8`), a violent bear-market
rally pushes the thermostat into the 61–100% "hysteria" tier at `README.md:48` exactly as hard
as the crash that preceded it. Think April–August 2020: 2020-04-06 ($+11.41\%$) and 2020-03-23
($+10.22\%$) both score $1.00000000$. The model is not wrong — those *are* high-volatility
weeks — but the tier they trigger buys the most insurance after the drawdown has happened.

**Fix direction.** Not in regime identification: the jump regime is identified by variance and
should be, since variance is what separates the states ($6.5\times$ in variance versus $0.16$
standard deviations in mean). The asymmetry belongs in `risk_engine.py`'s tier logic — e.g.
conditioning the tier on drawdown state or on the sign of trailing returns alongside
$P(\text{jump})$ — where it can be specified explicitly rather than hoped for from a likelihood
that does not weight it.

### 8.4 OPEN — the regime is materially fuzzier, and no longer reads as a panic detector

Dropping the constraints let the jump regime become common and mild:

| Quantity | Superseded spec | **Current spec** |
|---|---|---|
| RCM (Ang–Bekaert, filtered) | $25.78$ | $\mathbf{33.53}$ |
| Ergodic $P(\text{jump})$ | $0.118$ | $\mathbf{0.264}$ |
| Hard-assigned jump share | — | $\mathbf{23.2\%}$ of weeks (406 of 1750) |
| $\hat\sigma_{j^\star}$ | high (constrained short/extreme) | $3.84\%$/wk ($27.67\%$ annualized) |
| Variance ratio jump/calm | — | $6.53\times$ |

An RCM of $33.53$ means the filtered probabilities spend a great deal of time away from
$\{0,1\}$: a third of the way to "no information". And the model's own long-run claim is that
**26.4% of all weeks are jump weeks**.

**Read the episode composition and the name stops fitting.** In 2022, **43 of 52 weeks** are
above $0.5$; across 2000–2002, **80 of 157**. The longest episode is 33 consecutive weeks
(2022-04-11 .. 2022-11-21). A state that occupies most of a slow grinding bear market and a
quarter of all history is an **elevated-volatility state**, not a panic detector. That is a
perfectly coherent object and it may well be the more useful one for sizing an overlay — but it
is not what `README.md`'s tier language describes, and calling it "jump" or "hysteria" will
mislead whoever reads the output next.

Two consequences worth separating. (a) *Statistically* this is not a defect: the unrestricted
MLE is telling you what two Gaussian states fit best, and the answer is one common mild state
and one common wide state, not one calm state and one rare catastrophe. (b) *Operationally* it
changes what the thermostat is. A signal that is above $0.5$ in 23% of weeks implies a very
different premium budget from one that fires 12% of the time. This needs a decision in
`README.md` §4, not a code change.

### 8.5 OPEN — k=3 wins both criteria by a widening margin

On the full real history, corrected AIC and BIC both prefer three regimes, and the margin grew
after the respecification:

$$\Delta\text{AIC} = +65.9993, \qquad \Delta\text{BIC} = +44.1298 \quad\text{favouring } k=3$$

(positive means the repo's $k=2$ spec is worse). The $k=3$ fit gives annualized volatilities of
$10.00\% / 19.59\% / 55.66\%$ with expected durations $46.59 / 22.10 / 4.95$ weeks — a genuine
three-tier structure that matches `README.md` §4's own risk matrix, which is specified with
three tiers while `README.md` §2 mandates two states.

**The caveat that must travel with the result.** The $k=3$ fit returns
$p_{2\to0} = 4.358864\times10^{-19}$ — a **boundary zero**. There are no direct crisis-to-calm
transitions; crises are entered and exited only through the middle state. Substantively that is
interesting. Statistically it means the same thing a binding inequality constraint meant in
Section 8.1: a parameter on the boundary of its space has a non-normal limiting distribution, so
**that fit's own standard errors are untrustworthy**, exactly as the superseded $k=2$ fit's
were.

Its **information criteria are not** affected by this. AIC and BIC are functions of $\ell$ and
$k$ only; neither requires the estimate to be interior, and `diagnostics.py:390-403` confirms
$k_{\text{sm}} = k_{\text{free}} = 10$ with zero discrepancy. So the ranking stands even though
the inference within the model does not. Do not use one to dismiss the other.

Also note: this is *not* a likelihood-ratio test of $k=2$ versus $k=3$, and must not be
converted into one. That test is non-standard for all three reasons in Section 5.3.

### 8.6 OPEN — `checks.py` cannot detect misspecification

`checks.py:37-46` draws its fixture from exactly the model being fitted: Gaussian emissions,
two variance levels, one mean per block, hard regime boundaries. By construction it can only
confirm that the estimator recovers its own generating process. It is structurally incapable of
revealing that the model is wrong about real returns, and every diagnostic in Section 6 passes
on it (JB $p = 0.500$, ARCH-LM(4) $p = 0.170$, Ljung–Box(4) on squares $p = 0.229$) while the
same tests reject at $p < 10^{-6}$ on real data.

The file has improved: it now asserts the parameter count, the switching mean, the gradient and
Hessian signatures, the filtered-not-smoothed contract, and the jump index's derivation from
variance (`checks.py:101-149`), and it reports the sign-blindness limitation as a measured
number rather than a claim (`checks.py:166-182`). Those are all guards against defects that
actually occurred. None of them is a test of *fit*.

The missing test is a fixture the model should **fail**: generate the calm periods with
within-regime volatility drift (GARCH-simulated, say) and assert that ARCH-LM on $z_t$
*rejects*. A test that fails when the model is right is worth as much as one that passes, and
until one exists, `checks.py` passing tells you the plumbing works and nothing about whether the
specification does. That distinction is the whole reason `diagnostics.py` exists as a separate
real-data script.

---

## 9. Annotated further reading

**The two founding papers — read these first, in this order.**

- **Hamilton, J. D. (1989).** "A New Approach to the Economic Analysis of Nonstationary Time
  Series and the Business Cycle." *Econometrica* 57(2), 357–384.
  → §2–3 for the filter derivation in Section 2, and the original specification (switching
  *mean*, not variance) — which since 2026-08-12 is half of what this repo fits. Also the source
  of the "smoothed probabilities for historical dating" convention that this repo inherited
  without inheriting its caveat, and then corrected (Section 4.3).
- **Kim, C.-J. (1994).** "Dynamic Linear Models with Markov-Switching." *Journal of
  Econometrics* 60(1–2), 1–22.
  → The backward recursion in Section 4.2, including the conditional-independence step and
  exactly when it is exact rather than approximate.

**Textbooks — for when a paper assumes something you don't have.**

- **Hamilton, J. D. (1994).** *Time Series Analysis*, Princeton UP, **Chapter 22**.
  → The cleanest single exposition of filter + smoother + MLE for regime switching. Start here
  if the 1989 paper's notation fights you.
- **Kim, C.-J. & Nelson, C. R. (1999).** *State-Space Models with Regime Switching*, MIT Press.
  → What statsmodels actually implements — cited at `markov_regression.py:80-83`. Ch. 4–5 map
  onto `markov_switching.py` almost line for line. The single most useful book for reading this
  library's source.
- **Frühwirth-Schnatter, S. (2006).** *Finite Mixture and Markov Switching Models*, Springer.
  → Ch. 1–3 for identifiability, §3.2 for ordering constraints, Ch. 3.7 and Ch. 11 for label
  switching. The authoritative treatment of Section 7, cited in `src/jump_model.py:85-86`, and
  the reference to cite when choosing between an ordering constraint, post-hoc relabelling, and
  prior-based approaches.
- **McLachlan, G. & Peel, D. (2000).** *Finite Mixture Models*, Wiley.
  → Ch. 2–3 for why the mixture likelihood is unbounded and multimodal, which is the theory
  behind `search_reps` in Section 3.4.

**Estimation machinery.**

- **Dempster, A. P., Laird, N. M. & Rubin, D. B. (1977).** "Maximum Likelihood from Incomplete
  Data via the EM Algorithm." *JRSS-B* 39(1), 1–38.
  → EM in general. Read for *why* the M-step formulas at `markov_regression.py:271-274` are
  weighted moments.
- **Baum, L. E., Petrie, T., Soules, G. & Weiss, N. (1970).** *Annals of Mathematical
  Statistics* 41(1), 164–171.
  → The HMM-specific EM ("Baum–Welch"), predating and specializing Dempster et al.
- **Rabiner, L. R. (1989).** "A Tutorial on Hidden Markov Models…" *Proceedings of the IEEE*
  77(2), 257–286.
  → The most readable derivation of forward–backward anywhere, with the scaling factors made
  explicit. If Section 2.3's log-space arithmetic feels opaque, read §V of this.

**Testing for regimes — Section 5.3.**

- **Hansen, B. E. (1992).** "The Likelihood Ratio Test under Nonstandard Conditions: Testing the
  Markov Switching Model." *Journal of Applied Econometrics* 7(S1), S61–S82.
  → The canonical treatment of why your LR test is invalid and what bound to use instead. Read
  the introduction even if you skip the empirical-process machinery.
- **Davies, R. B. (1987).** "Hypothesis Testing when a Nuisance Parameter is Present Only under
  the Alternative." *Biometrika* 74(1), 33–43. (See also Davies 1977, *Biometrika* 64.)
  → The upcrossing bound. Short, and the cheapest correct thing you can actually compute.
- **Garcia, R. (1998).** "Asymptotic Null Distribution of the Likelihood Ratio Test in Markov
  Switching Models." *International Economic Review* 39(3), 763–788.
  → The Markov-switching-specific null distribution.
- **Cho, J. S. & White, H. (2007).** "Testing for Regime Switching." *Econometrica* 75(6),
  1671–1720.
  → Quasi-LR test; the more modern alternative to Hansen.
- **Carrasco, M., Hu, L. & Ploberger, W. (2014).** "Optimal Test for Markov Switching
  Parameters." *Econometrica* 82(2), 765–784.
  → An asymptotically optimal test you can compute without fitting the switching model. The
  most practical of this group if you need one number.

**Regimes versus GARCH — Section 6.4.**

- **Hamilton, J. D. & Susmel, R. (1994).** "Autoregressive Conditional Heteroskedasticity and
  Changes in Regime." *Journal of Econometrics* 64(1–2), 307–333.
  → SWARCH. The direct answer to "my ARCH-LM on $z_t$ rejects", which on real SPY it does, at
  $55.65$ / $p = 2.4\times10^{-11}$ (Section 8.2). Read this before considering a third regime:
  the failure is a step-function-versus-continuum problem, and a third step does not fix it.
- **Gray, S. F. (1996).** "Modeling the Conditional Distribution of Interest Rates as a
  Regime-Switching Process." *Journal of Financial Economics* 42(1), 27–62.
  → Tractable regime-switching GARCH; explains the path-dependence problem that makes the exact
  version infeasible.
- **Haas, M., Mittnik, S. & Paolella, M. S. (2004).** "A New Approach to Markov-Switching GARCH
  Models." *Journal of Financial Econometrics* 2(4), 493–530.
  → The modern MS-GARCH formulation, and the practical choice if you go this route.
- **Lamoureux, C. G. & Lastrapes, W. D. (1990).** "Persistence in Variance, Structural Change,
  and the GARCH Model." *JBES* 8(2), 225–234.
  → The reverse argument: ignoring regime shifts inflates GARCH persistence. Read it so you do
  not conclude "GARCH is better" from a single failing diagnostic.
- **Ang, A. & Timmermann, A. (2012).** "Regime Changes and Financial Markets." *Annual Review of
  Financial Economics* 4, 313–337.
  → Survey. The best single-sitting orientation to how regime models are actually used and
  where they fail in finance.

**Real-time versus revised probabilities — Section 4.3.**

- **Chauvet, M. & Piger, J. (2008).** "A Comparison of the Real-Time Performance of Business
  Cycle Dating Methods." *JBES* 26(1), 42–49.
  → The closest published analogue to this repo's central question: how much of a
  Markov-switching model's apparent skill survives when you evaluate it in real time instead of
  with smoothed full-sample probabilities. Read before building the expanding-window backtest.
- **Ang, A. & Bekaert, G. (2002).** "Regime Switches in Interest Rates." *JBES* 20(2), 163–182.
  → Source of the RCM statistic in Section 6.5.

**Diagnostics.**

- **Engle, R. F. (1982).** *Econometrica* 50(4), 987–1007. → The ARCH-LM test of Section 6.4.
- **Ljung, G. M. & Box, G. E. P. (1978).** *Biometrika* 65(2), 297–303. → Section 6.3.
- **Jarque, C. M. & Bera, A. K. (1980).** *Economics Letters* 6(3), 255–259. → Section 6.2.

---

## 10. Glossary — symbols, code names, and literature terms

**Symbols.** See the Notation table near the top; it is canonical and is not restated here.

**Symbol ↔ statsmodels name ↔ code location.**

| Symbol | `params` / attribute | Defined at |
|---|---|---|
| $p_{00}$ | `params['p[0->0]']`, `tm[0,0,0]` | `markov_switching.py:1405-1408` |
| $p_{10}$ | `params['p[1->0]']`, `tm[0,1,0]` | `markov_switching.py:1405-1408` |
| $p_{01}$ | not a parameter; $= 1 - p_{00} =$ `tm[1,0,0]` | `markov_switching.py:658-659` |
| $p_{11}$ | not a parameter; $= 1 - p_{10} =$ `tm[1,1,0]` | `markov_switching.py:658-659` |
| $\mu_j$ | `params['const[j]']` | `markov_regression.py:106-108`, `342-345` |
| $\sigma_j^2$ | `params['sigma2[j]']` | `markov_regression.py:350-352` |
| $j^\star$ | `jump_regime_index` (3rd return of `fit_jump_model`) | `src/jump_model.py:96-105`, `138` |
| $\Pi$ | `regime_transition_matrix(params)` | `markov_switching.py:632-664` |
| $\pi$ | `initial_probabilities(params)` | `markov_switching.py:576-602` |
| $\log\eta_t(j)$ | `_conditional_loglikelihoods(params)` | `markov_regression.py:190-191` |
| $\xi_{t\mid t-1}$ | `res.predicted_marginal_probabilities` | `markov_switching.py:1583-1591` |
| $\xi_{t\mid t}$ | `res.filtered_marginal_probabilities` | `markov_switching.py:223-226` |
| $\xi_{t\mid T}$ | `res.smoothed_marginal_probabilities` | `markov_switching.py:300-303` |
| $\ell_t$ | `res.llf_obs` / `joint_loglikelihoods` | `markov_switching.py:943-962` |
| $\ell(\theta)$ | `res.llf` | `markov_switching.py:1902-1907` |
| $E[D_i]$ | `res.expected_durations` | `markov_switching.py:1593-1614` |
| $\mathcal T$ | `transform_params` (statsmodels; the repo overrides nothing) | `markov_switching.py:1412-1453`, `markov_regression.py:358-387` |
| $\mathcal C$ | `_apply_constraints` — **deleted 2026-08-12**, see Sections 3.3 and 3.5 | no longer in the repo |

**Literature terms used above, with the section that uses them.**

| Term | Meaning | §|
|---|---|---|
| Markov-switching model | Latent discrete state drives parameters of an observed process | 0.1 |
| Hidden Markov model (HMM) | Same object, statistics/ML naming | 0.1 |
| Gaussian emission | Observation density is normal given the state | 1.1 |
| Location–scale mixture of normals | Marginal law: normals with different means *and* variances, mixed by weight | 0.1, 1.4 |
| Left-stochastic matrix | Columns sum to 1; statsmodels' $\Pi$ | 1.2 |
| Ergodic / stationary distribution | $\Pi\pi = \pi$; the chain's long-run occupancy | 1.4 |
| Perron–Frobenius | Guarantees a unique positive $\pi$ for an irreducible aperiodic chain | 1.4 |
| Geometric duration | Run length is geometric under first-order Markov; mean $1/(1-p_{ii})$ | 1.5 |
| Hamilton filter / forward algorithm | Forward recursion for $\xi_{t\mid t}$ and $\ell_t$ | 2 |
| Chapman–Kolmogorov | The one-step propagation $\xi_{t\mid t-1} = \Pi\xi_{t-1\mid t-1}$ | 2.2 |
| Prediction-error decomposition | $f(r_1..r_T) = \prod_t f(r_t\mid\mathcal F_{t-1})$; makes MLE $O(Tk^2)$ | 2.2 |
| logsumexp | $\log\sum e^{x_i}$, max-shifted; makes the recursion overflow-safe | 2.3 |
| Steady-state initialization | $\xi_{1\mid 0} = \pi$; statsmodels' default | 2.4 |
| Kim smoother / forward–backward | Backward recursion for $\xi_{t\mid T}$ | 4 |
| Look-ahead bias | Using data unavailable at decision time | 4.3, 8.1 |
| Real-time / recursive out-of-sample | Refit on data through $s$ only, take $\xi_{s\mid s}$, advance $s$ | 4.3 |
| Reparameterization / link function | Bijection from $\mathbb R^k$ to a constrained $\Theta$ | 3.2 |
| Multinomial logistic (softmax) | The probability transform statsmodels uses | 3.2 |
| Complex-step differentiation | Exact gradient via $\operatorname{Im}f(x+ih)/h$; requires $f$ analytic | 3.1, 3.5b |
| BFGS | Quasi-Newton optimizer; assumes $C^2$ objective | 3.1, 3.5a |
| EM / Baum–Welch | Monotone iterative MLE for latent-variable models | 3.4 |
| Multimodality of the mixture likelihood | Several local maxima; motivates random restarts | 3.4 |
| Unbounded mixture likelihood | $\sigma_j^2\to0$ on a single point sends the density to $\infty$ | 3.4 |
| Label switching | Likelihood invariant to permuting regime labels | 7.1 |
| Ordering / identifiability constraint | One representative per permutation orbit | 7.2, 7.4 |
| **Post-hoc relabelling** | Estimate freely, name the regimes afterwards; the repo's strategy | 7.2, 7.3 |
| Naming indeterminacy | An unidentified quantity that indexes coordinates, not distributions | 7.3 |
| Interior stationary point | $\nabla\ell = 0$ inside $\Theta$; precondition for Hessian-based inference | 3.1, 7.3 |
| Boundary solution | Estimate on the edge of $\Theta$; non-normal limiting distribution | 5.1, 8.1, 8.5 |
| Law of total variance | $\operatorname{Var} = E[\operatorname{Var}] + \operatorname{Var}[E]$; mixture-moment $z_t$ | 6.1 |
| Wald / LR equivalence | $z^2 \approx$ LR asymptotically; why a contrast can reject when a level does not | 5.3 |
| Projection / retraction | A non-injective map onto a feasible set; not an inverse pair | 3.3, 3.5c |
| Nuisance parameter unidentified under the null | Why the LR test for $k$ is non-standard | 5.3 |
| Davies bound | Upcrossing-based conservative $p$-value for a sup-statistic | 5.3 |
| ARCH-LM test | $TR^2$ from regressing $z_t^2$ on its lags; tests leftover vol clustering | 6.4 |
| Regime-standardized residual | $z_t = (r_t-\hat\mu)/\hat\sigma_{S_t}$; should be i.i.d. $\mathcal N(0,1)$ | 6.1 |
| RCM (regime classification measure) | $0$ = sharp classification, $100$ = uninformative | 6.5 |
| SWARCH / MS-GARCH | Regime switching combined with within-regime GARCH | 6.4 |
| Jump-diffusion | Continuous-time diffusion + compound Poisson jumps. **Not this model.** | 0.2 |
