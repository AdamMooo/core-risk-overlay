# Math Reference — Markov-Switching Models

Last updated: 2026-08-13

**What this is.** A self-contained treatment of the model class this project uses: the
specification, the recursions that make it computable, the estimator, the theorems that say when
any of it is valid, and where to read further. Written to be studied, not consulted.

**What this is deliberately not.** It is not a companion to the code. There are no line numbers,
no library internals, no fitted parameter values, no current-status claims. Those live in
`../README.md` (the question and where it stands), `RESEARCH-PROTOCOL.md` (what gets measured and
how it is scored), `POINT-IN-TIME-DISCIPLINE.md` (time-basis rules), and `../core-risk-overlay.md`
(the running log). Everything here is true of the model whether or not this repo exists, and stays
true when the specification changes.

Where an implementation detail is load-bearing for *understanding* — a convention that inverts a
result if you get it backwards — it appears as a convention warning, not as a code citation.

---

## 0. Prerequisites and reading path

### 0.1 What you need before each part

Read down the table until you hit a row whose "you need" column contains something you cannot
state from memory. Fix that first; the sections above it will not save you.

| Part | You need | Standard source |
|---|---|---|
| §1 The model | Conditional probability, Bayes' rule, the normal density. Finite-state Markov chains: transition matrices, irreducibility, aperiodicity, stationary distributions | Grimmett & Stirzaker ch. 6; Norris, *Markov Chains* ch. 1 |
| §2 The filter | Law of total probability, matrix–vector products, floating-point underflow | Hamilton (1994) ch. 22; Rabiner (1989) §III |
| §3 Predictive density | Mixture distributions, CDF inversion, truncated-normal moments | Any mathematical-statistics text; McLachlan & Peel ch. 1 |
| §4 MLE | Likelihood, score, Fisher information, the delta method; unconstrained numerical optimization (BFGS); latent-variable EM | Casella & Berger ch. 7, 10; Nocedal & Wright ch. 6; Dempster, Laird & Rubin (1977) |
| §5 Identifiability | Group actions on a parameter space (only informally); what "identified" means | Frühwirth-Schnatter (2006) ch. 1, 3 |
| §6 Choosing $k$ | Wilks' theorem and *its hypotheses* — this section is entirely about the hypotheses failing | Hansen (1992) intro; Self & Liang (1987) |
| §7 Diagnostics | Autocorrelation, LM/score tests, $\chi^2$ asymptotics | Engle (1982); Ljung & Box (1978) |

### 0.2 A reading path that works

1. **Hamilton (1994) ch. 22.** The cleanest single exposition of model + filter + smoother + MLE
   in one notation. Read this before the 1989 paper, not after.
2. **Hamilton (1989)** §2–3. The founding paper; now it will read easily.
3. **Rabiner (1989)** §III–V. The same recursions from the HMM side, with the clearest available
   derivation of forward–backward. Reading both vocabularies is worth the duplication: half the
   literature says "filtered probabilities", the other half says "$\alpha$-pass".
4. **Kim (1994)** for the smoother, and its exactness condition.
5. **Frühwirth-Schnatter (2006)** ch. 1–3 for identifiability and label switching.
6. **McLachlan & Peel (2000)** ch. 2–3 for why the mixture likelihood is unbounded and multimodal.

§9 annotates these plus the specialist literature by the question each one answers.

---

## Notation

Fixed for the whole document.

| Symbol | Meaning |
|---|---|
| $t$, $T$ | time index, sample length |
| $r_t$ | observed return at $t$ (log return unless stated) |
| $\mathcal F_t$ | information set $\{r_1,\dots,r_t\}$ |
| $S_t$ | latent regime, $S_t \in \{0,\dots,k-1\}$; labels carry no meaning until §5 |
| $k$ | number of regimes |
| $p_{ij}$ | $\Pr(S_t = j \mid S_{t-1} = i)$ — **row = from, column = to** |
| $P$ | transition matrix, $P_{ij} = p_{ij}$; **row**-stochastic |
| $\Pi = P^{\!\top}$ | the **column**-stochastic transpose (see §1.3) |
| $\pi$ | ergodic (stationary) distribution, $P^{\!\top}\pi = \pi$ |
| $\mu_j,\ \sigma_j^2$ | regime-$j$ mean and variance |
| $\theta$ | the full parameter vector |
| $\eta_t(j)$ | conditional density $f(r_t \mid S_t = j;\theta)$ |
| $\xi_{t\mid t-1}$ | **predicted** state probabilities, $\Pr(S_t = \cdot \mid \mathcal F_{t-1})$ |
| $\xi_{t\mid t}$ | **filtered**, $\Pr(S_t = \cdot \mid \mathcal F_t)$ |
| $\xi_{t\mid T}$ | **smoothed**, $\Pr(S_t = \cdot \mid \mathcal F_T)$ |
| $\ell_t$, $\ell(\theta)$ | per-period and total log-likelihood |
| $z_t$ | regime-standardized residual, $(r_t - \hat\mu_{S_t})/\hat\sigma_{S_t}$ |
| $\phi,\ \Phi$ | standard normal pdf and cdf |
| $\odot$, $\mathbf 1$ | Hadamard (elementwise) product; column vector of ones |

### The four layers

Four distinct objects, and confusing them is the main source of error in this literature.

- **Layer 1 — the model.** A specification: state space, transition law, emission law. Economics.
- **Layer 2 — the Hamilton filter.** A forward recursion that, *given* $\theta$, produces
  $\xi_{t\mid t}$ and the likelihood. Real-time: uses data up to $t$ only.
- **Layer 3 — MLE.** An optimizer that searches $\theta$ by calling the filter repeatedly.
  Machinery, not economics.
- **Layer 4 — the Kim smoother.** A backward recursion that revises state probabilities using the
  whole sample, after estimation. Retrospective: uses data up to $T$.

A signal may use Layers 1–3. It may not use Layer 4 (§2.7).

---

## 1. The model

### 1.1 Specification

$$r_t = \mu_{S_t} + \varepsilon_t, \qquad
\varepsilon_t \mid S_t = j \;\sim\; \mathcal N(0,\ \sigma_j^2)$$

$$\Pr(S_t = j \mid S_{t-1} = i,\ S_{t-2},\dots,\ \mathcal F_{t-1})
\;=\; \Pr(S_t = j \mid S_{t-1} = i) \;=\; p_{ij}$$

Three assumptions, each separately falsifiable and each with its own escape hatch in §8:

1. **First-order, time-homogeneous transitions.** Where you are next depends on where you are now
   and nothing else — not on how long you have been there (that would be semi-Markov / duration
   dependence), not on any covariate (that would be TVTP).
2. **Conditional independence of emissions.** Given $S_t$, $r_t$ is independent of everything
   else. This is what makes the filter exact and the smoother exact; drop it (Markov-switching AR,
   MS-GARCH) and things get harder in specific, named ways.
3. **Gaussian emissions with regime-specific mean and variance.** Two free scale parameters is
   the entire model of heteroskedasticity: volatility takes $k$ discrete values and nothing in
   between. §7.5 is the test of exactly this.

The emission density, which the filter calls $T\times k$ times:

$$\eta_t(j) \;=\; \frac{1}{\sqrt{2\pi\sigma_j^2}}
\exp\!\left(-\frac{(r_t-\mu_j)^2}{2\sigma_j^2}\right)$$

**What a switching mean does and does not buy.** The log-density ratio between two regimes,

$$\log\frac{\eta_t(1)}{\eta_t(0)}
= \tfrac12\log\frac{\sigma_0^2}{\sigma_1^2}
- \frac{(r_t-\mu_1)^2}{2\sigma_1^2} + \frac{(r_t-\mu_0)^2}{2\sigma_0^2}$$

is quadratic in $r_t$. On equity returns the $1/\sigma^2$ asymmetry dominates the mean gap by an
order of magnitude, so **a large positive week is nearly as strong evidence of the high-variance
regime as a large negative one.** The model is a width meter, not a direction meter. Any intuition
that treats high $\Pr(\text{high-variance regime})$ as a bearish forecast is importing something
the likelihood never asserted.

### 1.2 What this is called, and what it is not

In decreasing generality:

- **Markov-switching / regime-switching model** — the econometrics umbrella term.
- **Hidden Markov model (HMM) with Gaussian emissions** — the statistics/ML name. Discrete latent
  state, continuous observation, first-order transitions. Identical object.
- **Markov-switching mean and variance model** — Hamilton (1989)'s switching mean plus the
  financial-econometrics switching-variance extension.
- **Two-component location–scale mixture of normals with Markov-dependent mixing** — the
  *marginal* law of $r_t$ is a normal mixture with weights $\pi$; the chain adds serial dependence
  to *which component is drawn*.

All four are correct search terms. Two labels are wrong and worth ruling out explicitly:

- **"Markov regression"** is a class name in one library, not a model name. With no exogenous
  regressors there is no regression: a constant term with a regime-specific coefficient is just
  $\mu_{S_t}$.
- **"Jump-diffusion"** is a different model. Merton (1976) is continuous-time: a diffusion plus a
  **compound Poisson** jump term, jumps instantaneous and independent across time. This model has
  no diffusion, no Poisson process, and its "jumps" are *persistent states lasting weeks*. It is a
  discrete-time proxy for elevated volatility, not for jump arrivals.

### 1.3 The transition matrix, and the one convention that inverts results

$P$ is **row**-stochastic: $P_{ij} = \Pr(S_t=j \mid S_{t-1}=i)$, rows sum to one, and a row vector
of probabilities propagates as $\xi^{\!\top}P$. That is the textbook convention (Norris, Hamilton).

Filtering code overwhelmingly stores the **transpose** $\Pi = P^{\!\top}$ instead, because then a
*column* vector propagates as the plain matrix–vector product $\Pi\xi$ with no transpose in the
inner loop. $\Pi$ is **column**-stochastic. For $k=2$:

$$P = \begin{pmatrix} p_{00} & p_{01} \\ p_{10} & p_{11}\end{pmatrix},
\qquad
\Pi = \begin{pmatrix} p_{00} & p_{10} \\ p_{01} & p_{11}\end{pmatrix}$$

> **Convention warning.** Read $\Pi$ as though it were row-stochastic and you will silently use
> $p_{10}$ where you meant $p_{01}$ — swapping the entry and exit rates of the crisis regime. The
> resulting model is internally consistent, converges cleanly, and is wrong. The diagonal is
> ambiguity-free ($\Pi_{ii} = p_{ii}$), which is why persistence checks pass while the
> off-diagonals are transposed. **Always verify orientation numerically**: build an asymmetric $P$
> with known entries, push a known $\xi$ through one step by hand, compare.

Only $k(k-1)$ of the $k^2$ entries are free — each row is a probability vector summing to one. For
$k=2$ that is two free parameters, conventionally $p_{00}$ and $p_{11}$ (or $p_{00}$ and $p_{10}$,
depending on which library you are in), with the rest by complement. A restriction on $p_{11}$ is
therefore a restriction on $p_{10}$; they are the same knob.

### 1.4 Ergodic (stationary) distribution

Two reasons you need it. It is the filter's natural initial condition (§2.5), and it is the
model's implied **unconditional frequency of crisis weeks** — a prior you assert whether or not you
meant to.

$\pi$ satisfies $\pi^{\!\top}P = \pi^{\!\top}$ with $\mathbf 1^{\!\top}\pi = 1$: $\pi$ is the left
eigenvector of $P$ for eigenvalue 1, equivalently the right eigenvector of $\Pi$. For $k=2$, write
the first component out:

$$\pi_0 = p_{00}\pi_0 + p_{10}\pi_1
\;\Longrightarrow\; \pi_0(1 - p_{00}) = \pi_1 p_{10}
\;\Longrightarrow\; \pi_0\,p_{01} = \pi_1\,p_{10}$$

The middle equality is a **flow balance** statement — in steady state, mass leaving regime 0 per
period equals mass entering it. Impose $\pi_0 + \pi_1 = 1$:

$$\boxed{\ \pi_0 = \frac{p_{10}}{p_{01} + p_{10}}, \qquad
\pi_1 = \frac{p_{01}}{p_{01} + p_{10}}\ }$$

Each regime's share is proportional to the rate of entering it. **Theorem** (Perron–Frobenius for
stochastic matrices): if the chain is irreducible and aperiodic — for $k=2$, if
$0 < p_{01},\,p_{10} < 1$ — then $\pi$ exists, is unique, is strictly positive, and is *limiting*:
$P^h \to \mathbf 1\pi^{\!\top}$. For general $k$ solve $(P^{\!\top} - I)\pi = 0$ with the
normalization appended, by pseudo-inverse or eigendecomposition.

**Read the result as a claim, always.** $\pi_{j^\star}$ is the model saying "this fraction of all
weeks are crisis weeks." If that comes out near a quarter, the fitted object is an
elevated-volatility indicator, not a crash detector, regardless of what you named the regime.

### 1.5 $h$-step transitions and the mixing rate

How far ahead does a regime forecast carry information? The answer is an eigenvalue. For $k=2$ the
eigenvalues of $P$ are $1$ and

$$\lambda \;=\; p_{00} + p_{11} - 1 \;=\; 1 - p_{01} - p_{10}$$

and the $h$-step matrix has a closed form:

$$P^h \;=\; \begin{pmatrix}\pi_0 & \pi_1\\ \pi_0 & \pi_1\end{pmatrix}
\;+\; \lambda^h \begin{pmatrix}\pi_1 & -\pi_1\\ -\pi_0 & \pi_0\end{pmatrix}$$

(Check $h=0$: the two terms sum to $I$. Check $h=1$: the $(0,0)$ entry is
$\pi_0 + \lambda\pi_1 = p_{00}$.) So the $h$-step forecast is the ergodic distribution plus a
deviation that decays **geometrically at rate $\lambda$**. Everything about horizon follows:

$$\text{half-life} \;=\; \frac{\log 0.5}{\log \lambda}$$

With $p_{00}=0.98$ and $p_{11}=0.90$, $\lambda = 0.88$ and the half-life is about 5.4 periods:
five periods out, the model has forgotten half of what it knew about the state. **This is the
honest horizon of the signal**, and it is a property of the fitted transition matrix alone — no
backtest required to compute it. $\lambda$ near 1 means slow mixing (persistent, informative,
sluggish); $\lambda$ near 0 means the chain is nearly i.i.d. and the regime label is nearly
worthless one step out.

### 1.6 Expected duration, and why the average is a lie

Condition on having just entered regime $i$. Each period the run continues with probability
$p_{ii}$, independently (first-order Markov), so the run length $D_i$ is **geometric** on
$\{1,2,3,\dots\}$:

$$\Pr(D_i = d) = p_{ii}^{\,d-1}(1 - p_{ii}), \qquad
E[D_i] = \sum_{d\ge1} d\,p_{ii}^{\,d-1}(1-p_{ii}) = \boxed{\frac{1}{1 - p_{ii}}}$$

The sum is $\sum_d d x^{d-1}(1-x) = (1-x)\frac{d}{dx}\frac{1}{1-x} = \frac{1}{1-x}$.

$\operatorname{Var}(D_i) = p_{ii}/(1-p_{ii})^2$, so the standard deviation of duration is
$\sqrt{p_{ii}}\,E[D_i] \approx E[D_i]$ whenever $p_{ii}$ is near 1. **Duration is as dispersed as
it is long.** A regime with a 50-week "average" duration routinely produces 5-week and 150-week
runs — the geometric distribution's mode is always 1. Never quote $E[D_i]$ as a typical episode
length; quote the distribution, or quantiles of it.

Useful as a diagnostic all the same: compare the fitted $1/(1-\hat p_{ii})$ against the empirical
run-length distribution of the classified states. Systematic mismatch in either direction means
the geometric assumption is wrong, and the escape hatch is a semi-Markov model (§8).

### 1.7 The marginal law: moments of a mixture

Unconditionally, $r_t$ is drawn from component $j$ with probability $\pi_j$. Write
$m = \sum_j \pi_j \mu_j$ and $d_j = \mu_j - m$. Then

$$\operatorname{Var}(r_t) \;=\; \underbrace{\sum_j \pi_j\sigma_j^2}_{\text{within}}
\;+\; \underbrace{\sum_j \pi_j d_j^2}_{\text{between}}$$

which is the **law of total variance**, $\operatorname{Var}(r) = E[\operatorname{Var}(r\mid S)] +
\operatorname{Var}(E[r\mid S])$. The third and fourth central moments follow from the normal's own
moments ($E[\varepsilon^3]=0$, $E[\varepsilon^4]=3\sigma^4$):

$$E[(r-m)^3] = \sum_j \pi_j\big(d_j^3 + 3 d_j\sigma_j^2\big), \qquad
E[(r-m)^4] = \sum_j \pi_j\big(d_j^4 + 6 d_j^2\sigma_j^2 + 3\sigma_j^4\big)$$

**Theorem (a variance mixture is always leptokurtic).** Set all $\mu_j$ equal, so $d_j = 0$. Then

$$\text{kurtosis} = \frac{3\sum_j \pi_j\sigma_j^4}{\big(\sum_j \pi_j\sigma_j^2\big)^2} \;\ge\; 3$$

by Cauchy–Schwarz (or Jensen on $x\mapsto x^2$), with equality iff all $\sigma_j$ are equal. This
is the whole reason the model is used on returns: **mixing normals of different widths manufactures
fat tails out of Gaussian components.** It also tells you what to expect from diagnostics — raw
returns are *supposed* to be leptokurtic here, so testing them for normality tests the premise, not
the fit (§7.1).

**Serial dependence in the level.** With $\varepsilon_t$ independent across $t$,

$$\operatorname{Cov}(r_t, r_{t-h}) = \operatorname{Cov}(\mu_{S_t}, \mu_{S_{t-h}})
= \lambda^{h}\,\pi_0\pi_1(\mu_0 - \mu_1)^2 \quad (k=2)$$

using §1.5's eigenvalue. So a switching *mean* induces genuine autocorrelation in returns, decaying
at the mixing rate; a switching *variance* alone induces none in the level but plenty in the
squares. Both facts show up in §7.4 and §7.5.

---

## 2. The Hamilton filter

Hamilton (1989), *Econometrica* 57(2), 357–384, §2–3. Identical to the HMM **forward algorithm**
with normalization (Rabiner 1989 calls the normalizer $c_t$). Hamilton's contribution was the
framing in which **the normalizer is the likelihood contribution** — which is what turns a state
estimator into an estimator of $\theta$.

### 2.1 Three conditioning sets, never interchangeable

$$\xi_{t\mid t-1}(j) = \Pr(S_t = j \mid \mathcal F_{t-1}), \quad
\xi_{t\mid t}(j) = \Pr(S_t = j \mid \mathcal F_{t}), \quad
\xi_{t\mid T}(j) = \Pr(S_t = j \mid \mathcal F_{T})$$

**Predicted** uses data through $t-1$ — a genuine one-step-ahead forecast, the only one of the
three with no dependence on period-$t$ data. **Filtered** uses past and present: the full posterior
available at the close of period $t$, and the only object a real-time signal may use.
**Smoothed** uses the entire sample including the future (§2.7).

### 2.2 The recursion

Collect densities into $\eta_t = (\eta_t(0),\dots,\eta_t(k-1))^{\!\top}$.

**Step 1 — Prediction** (propagate the chain one period; Chapman–Kolmogorov):

$$\xi_{t\mid t-1}(j) \;=\; \sum_{i} p_{ij}\,\xi_{t-1\mid t-1}(i)
\qquad\Longleftrightarrow\qquad
\xi_{t\mid t-1} = \Pi\,\xi_{t-1\mid t-1}$$

**Step 2 — Update** (Bayes' rule, with the new observation as evidence):

$$\xi_{t\mid t}(j)
= \frac{\eta_t(j)\,\xi_{t\mid t-1}(j)}{\sum_{i}\eta_t(i)\,\xi_{t\mid t-1}(i)}
\qquad\Longleftrightarrow\qquad
\xi_{t\mid t} = \frac{\eta_t \odot \xi_{t\mid t-1}}
{\mathbf 1^{\!\top}(\eta_t \odot \xi_{t\mid t-1})}$$

Numerator is prior $\times$ likelihood; the denominator is the normalizing constant Bayes' rule
demands.

**Step 3 — Harvest the denominator.** It is not bookkeeping — it *is* the one-step-ahead
predictive density of the observation:

$$f(r_t \mid \mathcal F_{t-1};\theta)
= \sum_j f(r_t \mid S_t = j)\Pr(S_t = j \mid \mathcal F_{t-1})
= \mathbf 1^{\!\top}(\eta_t \odot \xi_{t\mid t-1})$$

$$\ell_t = \log\big(\mathbf 1^{\!\top}(\eta_t \odot \xi_{t\mid t-1})\big),
\qquad \ell(\theta) = \sum_{t=1}^{T}\ell_t$$

Initialize with $\xi_{1\mid 0}$ (§2.5) and iterate. Cost: $O(Tk^2)$, one pass.

### 2.3 The prediction-error decomposition

Why is a one-pass recursion enough to get the exact likelihood of a latent-state model? Because
the joint density always factorizes as

$$f(r_1,\dots,r_T;\theta) = \prod_{t=1}^{T} f(r_t \mid \mathcal F_{t-1};\theta)$$

and the filter produces each factor as a *by-product* of maintaining the state posterior. This is
the **prediction-error decomposition**, the same device that makes the Kalman filter an estimator
rather than just a smoother.

The alternative — summing the complete-data likelihood over all regime paths — costs $k^T$ terms.
The recursion collapses that to $Tk^2$ because $\xi_{t|t}$ is a **sufficient statistic** for the
path history: everything the past says about the future travels through the current state
distribution. That is the Markov property doing computational work.

### 2.4 Log space, and why it is not optional

Real implementations run the recursion additively on logs:

$$L^{\text{pred}}_t(j) = \operatorname*{logsumexp}_{i}\big[\log p_{ij} + L^{\text{filt}}_{t-1}(i)\big]$$

$$a_t(j) = \log\eta_t(j) + L^{\text{pred}}_t(j), \qquad
\ell_t = \operatorname*{logsumexp}_{j} a_t(j), \qquad
L^{\text{filt}}_t(j) = a_t(j) - \ell_t$$

with $\operatorname{logsumexp}(x) = x^* + \log\sum_i e^{x_i - x^*}$, $x^* = \max_i x_i$ — the
max-shift trick, which makes the largest exponentiated term exactly 1 and the rest smaller.

**The failure it prevents.** Step 2's normalization keeps the *probabilities* in $[0,1]$, so those
never underflow. The quantity that blows up is the running product
$\prod_{s\le t} f(r_s\mid\mathcal F_{s-1})$. Note the direction: for daily or weekly returns of
order $10^{-2}$, the *density* is of order $10^{2}$, so the product **overflows** — a few thousand
observations puts it past the float64 ceiling of $\sim10^{308}$ long before you finish the sample.
A run of crisis observations scored under the calm regime drives it to zero just as fast. Both
directions are fatal, and neither announces itself as anything but a `nan`.

Second numerical rule: **floor transition probabilities before logging.** Fitted transitions can
legitimately come back at $10^{-19}$; $\log 0$ poisons the whole recursion. Flooring at something
like $10^{-20}$ costs nothing and is standard.

### 2.5 Initialization

Three choices for $\xi_{1\mid 0}$:

| Choice | Definition | Cost |
|---|---|---|
| **Ergodic / steady-state** | $\xi_{1\mid0} = \pi(\theta)$, recomputed at every likelihood evaluation | None. The only choice consistent with the $P$ being estimated. Default, and correct |
| **Diffuse / uniform** | $\xi_{1\mid0} = (1/k,\dots,1/k)$ | Asserts something the model contradicts; harmless for large $T$, biting for short windows |
| **Estimated** | Treat $\xi_{1\mid0}$ as $k-1$ extra free parameters | Costs parameters to learn one observation's worth of information |
| **Known** | Seed a specific distribution, e.g. carrying state across refits | Only defensible if you can defend the seed |

For $T$ in the hundreds the choice is invisible — the filter forgets its initial condition at rate
$\lambda^t$ (§1.5). For short expanding-window refits it is not invisible, and the burn-in must be
long relative to the mixing half-life.

> **Convention warning.** Libraries differ on whether the seeded distribution is interpreted as
> $\xi_{1|0}$ (already predicted) or $\xi_{0|0}$ (to be propagated once more). Getting it wrong
> applies $\Pi$ one extra time. With ergodic initialization this is invisible, because
> $\Pi\pi = \pi$ — which is exactly why the bug survives testing and then bites the first time you
> seed anything else. Verify the realized first predicted probability against a hand computation.

### 2.6 Marginal modes are not the most likely path

$\hat S_t = \arg\max_j \xi_{t|t}(j)$ maximizes the probability of being right at each $t$
separately. It does **not** produce the most likely *sequence*: the pointwise-optimal path can even
have zero probability under $P$ if it strings together a transition the chain forbids.

The most likely sequence is a different optimization, solved by the **Viterbi algorithm** — the
same $O(Tk^2)$ dynamic program with $\operatorname{logsumexp}$ replaced by $\max$, plus a
backpointer array. Use marginals when you want per-period probabilities (a risk signal); use
Viterbi when you want a single coherent state history (regime dating, plotting episodes). Reporting
one and describing it as the other is a common and quiet error.

### 2.7 The Kim smoother, and why a signal may not use it

Kim (1994), *J. Econometrics* 60(1–2), 1–22. Equivalent to HMM **forward–backward**.

Start from $\xi_{T\mid T}$ — at $t=T$ there is no future left to add, so the smoothed and filtered
values coincide (a free correctness check). Recurse backwards for $t = T-1,\dots,1$:

$$\boxed{\ \xi_{t\mid T}(i) \;=\; \xi_{t\mid t}(i)\,\sum_{j}
\frac{p_{ij}\;\xi_{t+1\mid T}(j)}{\xi_{t+1\mid t}(j)}\ }$$

**Derivation** — three lines, and the middle one is the only place an assumption enters:

$$\xi_{t\mid T}(i) = \sum_j \Pr(S_t=i, S_{t+1}=j\mid\mathcal F_T)
= \sum_j \Pr(S_{t+1}=j\mid\mathcal F_T)\,\Pr(S_t=i\mid S_{t+1}=j,\mathcal F_T)$$

$$\Pr(S_t=i\mid S_{t+1}=j,\ \mathcal F_T) \;=\; \Pr(S_t=i\mid S_{t+1}=j,\ \mathcal F_t)$$

$$\Pr(S_t=i\mid S_{t+1}=j,\mathcal F_t)
= \frac{\Pr(S_t=i\mid\mathcal F_t)\,p_{ij}}{\Pr(S_{t+1}=j\mid\mathcal F_t)}
= \frac{\xi_{t\mid t}(i)\,p_{ij}}{\xi_{t+1\mid t}(j)}$$

The middle step drops $r_{t+1},\dots,r_T$ from the conditioning set. **It is valid iff
$\{r_{t+1},\dots,r_T\} \perp S_t \mid S_{t+1}$** — which holds *exactly* when emissions depend only
on the contemporaneous state (§1.1, assumption 2). For a plain Markov-switching model the Kim
smoother is therefore **exact**, not an approximation. It becomes approximate for
Markov-switching *autoregressions*, where the emission depends on lagged $r$ and hence on lagged
states: that is Kim (1994)'s own caveat and the reason the paper exists.

Every quantity on the right is already available from the forward pass, so smoothing costs one
extra $O(Tk^2)$ sweep and no extra filtering.

**Why it is look-ahead bias for a signal.** $\xi_{t\mid T}$ at period $t$ is computed using periods
$t+1,\dots,T$. In a backtest walking forward through history, the value at 2008-09-15 would be
informed by 2008-10-10, by 2009-03-06, and by every week since. **You could not have known it.**
Any performance statistic built on smoothed probabilities is fiction, and the failure is
self-concealing: nothing errors, everything looks better.

The mechanism is easy to see at a regime edge. One period *before* a volatility burst, the
smoother already assigns substantial crisis probability — it has seen the burst. One period
*after* the burst ends, the smoother has retroactively suppressed the alarm, while the filter,
correctly, does not yet know calm has resumed and exits slowly. **The filter's sluggish exit is
the honest picture of what you would have seen.**

Smoothed probabilities are the *right* object for retrospective questions — "was that period a
crisis regime?" — and are the standard tool for historical business-cycle dating, which is
Hamilton (1989)'s original application. That inheritance is why the convention is so widespread,
and why it is so often misapplied.

**The second, subtler leak.** Using filtered probabilities removes the *state* look-ahead but not
the *parameter* look-ahead: if $\hat\theta$ was estimated on the whole sample, then $\hat\sigma^2$
of the crisis regime is largely determined by the worst episodes in it, and scoring a period that
preceded them still cheats. The cure is **expanding-window (recursive) refitting**: fit on
$r_1,\dots,r_s$ only, take $\xi_{s|s}$ from *that* fit, record it as the period-$s$ signal, advance,
refit, repeat. The literature term is **real-time / recursive out-of-sample evaluation**
(Chauvet & Piger 2008). Three hazards: early-window parameter paths are unstable, so burn-in must
be generous; each refit carries its own label-switching risk, so the regime index must be
**recomputed per window** (§5.3); and the initialization convention above must be verified once.

---

## 3. From state probabilities to a predictive density

This is the section that connects the model to anything decision-relevant. The state posterior is
not the output; the **predictive density of the next return** is.

### 3.1 One step ahead: a mixture, not a normal

Push the state forward one period, then integrate the emission law over it:

$$w_j \;=\; \xi_{t+1\mid t}(j) = \sum_i p_{ij}\,\xi_{t\mid t}(i),
\qquad
f_{t+1\mid t}(r) \;=\; \sum_j w_j\,\phi(r;\ \mu_j,\ \sigma_j^2)$$

This is Step 1 and Step 3 of the filter reused as a forecast. Everything downstream — VaR, ES,
density scores — is a functional of this one object.

### 3.2 Quantiles: invert the CDF, never match moments

$\text{VaR}$ at level $\alpha$ is the $\alpha$-quantile, i.e. the $q$ solving

$$\sum_j w_j\,\Phi\!\left(\frac{q-\mu_j}{\sigma_j}\right) \;=\; \alpha$$

The mixture CDF is continuous and strictly increasing, so bisection or Brent converges
unconditionally; there is no closed form and no need for one.

> **The trap.** $q = m + \sqrt{v}\,\Phi^{-1}(\alpha)$, using the mixture's own mean and variance
> from §1.7, is **wrong**. Matching the first two moments of a mixture does not match its
> quantiles — *that non-equality is the entire reason for using a mixture*. If a two-moment
> summary sufficed, the model would be a GARCH. The error is largest exactly where the model is
> most interesting: at maximum regime uncertainty, $w$ near $(0.5, 0.5)$, where the true density is
> visibly bimodal in the tails and the moment-matched normal is not. The sign of the error flips
> with $\alpha$, so it will not even show up as a consistent bias.

### 3.3 Expected shortfall in closed form

$\text{ES}(\alpha) = E[r \mid r \le q]$ where $q$ is the VaR. No simulation is needed at one step.

**Lemma (truncated normal first moment).** For $X\sim\mathcal N(\mu,\sigma^2)$ and
$z = (q-\mu)/\sigma$:

$$E[X\,\mathbf 1\{X\le q\}] = \int_{-\infty}^{q} x\,\tfrac1\sigma\phi\!\big(\tfrac{x-\mu}{\sigma}\big)dx
\;\overset{x = \mu+\sigma u}{=}\; \int_{-\infty}^{z}(\mu + \sigma u)\phi(u)\,du
= \mu\Phi(z) - \sigma\phi(z)$$

using $\int_{-\infty}^{z} u\phi(u)du = -\phi(z)$, which follows from $\phi'(u) = -u\phi(u)$.
Summing over components with $z_j = (q-\mu_j)/\sigma_j$ and dividing by $\Pr(r\le q) = \alpha$:

$$\boxed{\ \text{ES}(\alpha) = \frac{1}{\alpha}\sum_j w_j\Big[\mu_j\Phi(z_j) - \sigma_j\phi(z_j)\Big]\ }$$

Both VaR and ES are **return levels** — negative numbers — under this convention. Pick one sign
convention and check it, because half the literature reports losses as positive.

### 3.4 Multi-step: the horizon problem

At horizon $h$ the state distribution is $\xi_{t+h|t} = (\Pi)^h \xi_{t|t}$, which is cheap
(§1.5 gives the closed form for $k=2$). But the **$h$-period cumulative return** is not a mixture
over end-states — it is a mixture over regime *paths*, because the return accumulates
$\sum_{s=1}^{h}(\mu_{S_{t+s}} + \varepsilon_{t+s})$ and each path contributes a different normal:

$$r_{t+1:t+h} \mid \text{path } (s_1,\dots,s_h) \;\sim\;
\mathcal N\!\Big(\textstyle\sum_u \mu_{s_u},\ \sum_u \sigma^2_{s_u}\Big)$$

with path probability $\xi_{t|t}(i)\prod_u p_{s_{u-1}s_u}$. There are $k^h$ paths. Exact
enumeration is feasible to $h\approx10$ for $k=2$ ($1{,}024$ paths); beyond that, Monte Carlo over
paths, or a moment-based approximation if you only need the first two moments (but see §3.2 for why
those do not give you quantiles).

**The overlapping-windows trap.** Evaluating $h$-step forecasts on overlapping windows destroys
independence of the scores and invalidates every standard error you compute from them. Use
non-overlapping blocks for inference; overlapping only for description.

### 3.5 Scoring a density

Two theorems worth carrying:

**Log score.** $-\sum_t \log f_{t+1|t}(r_{t+1})$ is a **strictly proper** scoring rule: its
expectation is uniquely minimized by the true predictive density. So a model cannot game it — any
deviation from the truth costs. It is also exactly the out-of-sample analogue of $-\ell(\theta)$,
which makes it the natural bridge between fitting and evaluation.

**Probability integral transform (Rosenblatt 1952).** If $F_{t+1|t}$ is the *correct* predictive
CDF then

$$u_t \;=\; F_{t+1\mid t}(r_{t+1}) \;\sim\; \text{i.i.d. } U(0,1)$$

Both parts matter: **uniform** says the density has the right shape, **independent** says nothing
predictable is left. This holds for any model and any distribution — which is what makes it the
universal density-forecast diagnostic (Diebold, Gunther & Tay 1998). Berkowitz (2001) turns it into
a likelihood-ratio test by mapping $z_t = \Phi^{-1}(u_t)$ and testing mean 0, variance 1, no AR(1)
against a Gaussian alternative, which recovers power the histogram throws away.

The full evaluation battery — coverage tests, the censored variants, forecast comparison — is
design, not model math, and lives in `RESEARCH-PROTOCOL.md` §5.

---

## 4. Maximum likelihood estimation

### 4.1 The objective

$$\hat\theta = \arg\max_{\theta\in\Theta}\ \ell(\theta)
= \arg\max_\theta \sum_{t=1}^{T}\log\big(\mathbf 1^{\!\top}(\eta_t(\theta)\odot\xi_{t\mid t-1}(\theta))\big)$$

The filter is the *only* channel through which $\theta$ reaches the objective, so every likelihood
evaluation is a full $O(Tk^2)$ forward pass, and every gradient evaluation is several. This is why
the parameter count matters more than the sample size for fitting cost.

### 4.2 The geometry: unbounded, multimodal, permutation-invariant

The mixture likelihood is **not globally concave** and generically has many local maxima. Three
distinct sources, all present in any regime-switching fit:

1. **Label switching.** The likelihood is *exactly* invariant to permuting regime labels (§5), so
   every interior mode is duplicated $k!$ times. For $k=2$, every mode has a twin.
2. **Unboundedness on the boundary.** Send $\sigma_j^2 \to 0$ with a single observation assigned to
   regime $j$ and its density $\to\infty$: the likelihood is **unbounded** (Day 1969; Kiefer &
   Wolfowitz 1956). Therefore "the MLE" for a normal mixture is not the global maximum — it does
   not exist. What consistency theory delivers is a **local interior maximizer**, and which one you
   find depends on where you start.
3. **Flat ridges.** High-variance/low-persistence and moderate-variance/high-persistence
   configurations trade off against each other along a nearly-flat ridge. Optimizers stall there
   and report convergence.

**Consequence: random restarts are a correctness requirement, not defensive coding.** Perturb the
start values many times, run a few EM iterations on each, keep the best basin, then polish with a
gradient method. A single-start fit of a mixture model is not an estimate, it is a sample from the
basin structure. Because restarts consume random numbers, **seed them** — otherwise the fit is
irreproducible in a way that looks like data-dependence.

### 4.3 Constraints as reparameterizations

Gradient optimizers are unconstrained and must never be handed a search space where
$\sigma^2 < 0$ or $p \notin [0,1]$ is reachable. The correct device is a **link function**: the
optimizer works in $\tilde\theta \in \mathbb R^d$, and the likelihood maps
$\tilde\theta \mapsto \theta$ before evaluating.

| Parameter | Link | Inverse | Note |
|---|---|---|---|
| Transition probabilities | multinomial-logistic (**softmax**) against a zero baseline, per row | log-odds | For $k=2$ collapses to the plain **logistic** $p = e^{\tilde p}/(1+e^{\tilde p})$, inverse **logit** $\log\frac{p}{1-p}$ |
| Variances | $\sigma^2 = \tilde\sigma^2$ (squaring) or $\sigma^2 = e^{\tilde\sigma}$ (log) | $\pm\sqrt{\cdot}$, or $\log$ | Squaring is **two-to-one**: it mirrors the surface and puts a kink at zero. Log is injective and better behaved, at the cost of never reaching the boundary |
| Means | identity | identity | Already unconstrained |

The requirement is that the map be a **bijection onto the feasible set** and smooth. Then the
optimizer's problem is genuinely unconstrained, the chain rule carries derivatives through cleanly,
and the fitted point is an **interior stationary point** — which is the precondition for every
standard-error formula in §4.6.

### 4.4 A projection is not a reparameterization

The tempting shortcut — clip, `sort`, `min`/`max`, or otherwise *project* the parameter vector onto
the feasible set inside the likelihood — is a different and broken thing. Worth stating as a
standing rule, because the failure mode is silent:

- **A projection is idempotent but not injective.** Many $\tilde\theta$ map to the same $\theta$,
  so the round trip is a *retraction*, not the identity, and the "parameter" the optimizer moves is
  not the parameter the model uses.
- **It puts a kink in an objective the optimizer assumes is $C^2$.** BFGS builds a curvature
  estimate from gradient differences; at a non-differentiable seam that estimate is meaningless.
- **It silently kills exact gradients.** Complex-step differentiation — evaluating $f(x+ih)$ and
  taking $\operatorname{Im}f/h$, exact to machine precision — requires $f$ to be *analytic*. A
  comparison-based operation on complex numbers compares lexicographically, breaking ties on the
  *imaginary* (perturbation) part, and credits the derivative to the wrong coordinate. `max` of a
  complex and a float discards it entirely.
- **The failure looks exactly like success.** A coordinate the optimizer never explored shows a
  gradient of exactly $-0.0$ and an inverse-Hessian diagonal still sitting at its identity
  initialization of $1.0$ — with a clean convergence flag. **A convergence flag cannot detect a
  direction that was never searched.** Assert on the gradient and inverse-Hessian entries directly.
- **Standard errors then describe a different model.** Covariance routines typically evaluate the
  Hessian at the *transformed* parameters, bypassing the very method the constraints lived in — so
  the reported errors belong to an unrestricted model at a non-stationary point.

If a genuine restriction is wanted, impose it as a reparameterization (§4.3), or fit the
restricted model directly with fewer parameters, and count the degrees of freedom accordingly
(§6.1).

### 4.5 EM / Baum–Welch

The alternative estimator, and the standard one on the HMM side (Baum et al. 1970; Dempster, Laird
& Rubin 1977). Worth knowing even if you finish with a gradient method, because every M-step is a
closed form you can read as a definition.

**Complete-data log-likelihood** — what you could write down if the states were observed:

$$\log p(r, S;\theta) = \log \pi_{S_1}
+ \sum_{t=2}^{T}\log p_{S_{t-1}S_t}
+ \sum_{t=1}^{T}\log \eta_t(S_t)$$

**E-step**: take its expectation under the current parameters, which replaces indicator variables
with smoothed probabilities. Two are needed — the marginal $\xi_{t|T}(j)$ from §2.7, and the
**smoothed pairwise** probability

$$\xi_{t-1,t\mid T}(i,j) \;=\; \frac{\xi_{t-1\mid t-1}(i)\ p_{ij}\ \xi_{t\mid T}(j)}{\xi_{t\mid t-1}(j)}$$

giving

$$Q(\theta\mid\theta^{(n)}) = \sum_j \xi_{1|T}(j)\log\pi_j
+ \sum_{t=2}^{T}\sum_{i,j}\xi_{t-1,t|T}(i,j)\log p_{ij}
+ \sum_{t}\sum_j \xi_{t|T}(j)\log\phi(r_t;\mu_j,\sigma_j^2)$$

**M-step**: maximize $Q$. The three blocks separate.

*Transitions* — maximize $\sum_{i,j} n_{ij}\log p_{ij}$ subject to $\sum_j p_{ij}=1$, with
$n_{ij} = \sum_t \xi_{t-1,t|T}(i,j)$. Lagrangian $\Rightarrow n_{ij}/p_{ij} = \nu_i \Rightarrow$

$$\hat p_{ij} = \frac{\sum_t \xi_{t-1,t\mid T}(i,j)}{\sum_t \xi_{t-1\mid T}(i)}
= \frac{\text{expected transitions } i\to j}{\text{expected time spent in } i}$$

*Means and variances* — differentiate the weighted Gaussian log-likelihood and set to zero:

$$\hat\mu_j = \frac{\sum_t \xi_{t|T}(j)\,r_t}{\sum_t \xi_{t|T}(j)}, \qquad
\hat\sigma_j^2 = \frac{\sum_t \xi_{t|T}(j)\,(r_t-\hat\mu_j)^2}{\sum_t \xi_{t|T}(j)}$$

Probability-weighted sample moments — exactly the formulas you would guess, which is the pleasant
thing about EM for exponential families.

**Properties.** Each iteration is **monotone** in $\ell$ (Jensen's inequality guarantees it), never
leaves the feasible set, and needs no step size. But convergence is only **linear**, and it slows
precisely near the optimum. Hence the standard hybrid: **EM to find a good basin, quasi-Newton to
finish** — combining EM's robustness to bad starts with BFGS's superlinear endgame.

### 4.6 Standard errors, and the delta method

The observed information $\hat I = -\nabla^2\ell(\hat\theta)$ gives
$\widehat{\operatorname{Var}}(\hat\theta) = \hat I^{-1}$, valid only at an **interior stationary
point** of a smooth objective (hence §4.3–4.4).

For an HMM the score has a clean form via the **Fisher identity**:
$\nabla\ell(\theta) = E_\theta[\nabla \log p(r,S;\theta) \mid r]$ — the gradient of the complete-data
log-likelihood, averaged under the smoothed state posterior. This is the same $Q$ from §4.5,
differentiated at $\theta^{(n)} = \theta$; Louis (1982) extends it to the information matrix.

**Most quantities you want to report are functions of $\theta$, not coordinates of it**, so they
need the delta method: $\operatorname{Var}(g(\hat\theta)) \approx \nabla g^{\!\top} V \nabla g$.
Two cases worth having at hand:

*Expected duration.* $g(p_{ii}) = 1/(1-p_{ii})$, so $g' = 1/(1-p_{ii})^2 = E[D_i]^2$ and

$$\text{se}\big(\widehat{E[D_i]}\big) \approx E[D_i]^2\ \text{se}(\hat p_{ii})$$

The **square** is the point: at $p_{ii} = 0.98$, a standard error of $0.01$ on the transition
probability becomes a standard error of 25 periods on the duration. Persistent regimes have
enormous duration uncertainty even when the transition matrix looks precisely estimated. Report the
interval, and expect it to be embarrassing.

*Ergodic probability.* With $\pi_0 = p_{10}/(p_{01}+p_{10})$,

$$\frac{\partial \pi_0}{\partial p_{01}} = \frac{-p_{10}}{(p_{01}+p_{10})^2}, \qquad
\frac{\partial \pi_0}{\partial p_{10}} = \frac{p_{01}}{(p_{01}+p_{10})^2}$$

and the covariance term between them is not optional — the two transition parameters are typically
correlated.

### 4.7 What is actually proved about the estimator

Do not assume standard MLE asymptotics apply because the model has a likelihood. The results, in
the order they were established:

- **Baum & Petrie (1966)** — consistency and asymptotic normality for finite-alphabet HMMs.
- **Leroux (1992)** — consistency for general HMMs, **up to label permutation**, under
  identifiability and stationarity.
- **Bickel, Ritov & Rydén (1998)** — asymptotic normality of the MLE for general state-space HMMs;
  the central reference.
- **Douc, Moulines & Rydén (2004)** — extension to autoregressive models with Markov regimes
  (the MS-AR case).

The conditions these need, and which you should actually check: the chain is ergodic; the true
parameter is in the **interior** of a compact parameter space; the model is identifiable up to
permutation; the emission family is regular. **None of them rescue the boundary cases** — the
statements are about a consistent *local* maximizer, which is why §4.2's unboundedness and §6.2's
non-standard testing problem are not contradicted by any of this.

---

## 5. Identifiability and label switching

### 5.1 The invariance

**Theorem.** The likelihood of a mixture or Markov-switching model is invariant to permutation of
the regime labels, provided the permutation is applied *consistently* — to every regime-specific
parameter **and** to the transition matrix (which is permuted on both indices,
$p'_{ij} = p_{\sigma(i)\sigma(j)}$).

For $k=2$ the permuted vector is

$$\theta' = (\,\mu_1,\ \mu_0,\ \sigma_1^2,\ \sigma_0^2,\ p'_{00}=p_{11},\ p'_{11}=p_{00}\,)$$

and $\ell(\theta') = \ell(\theta)$ **exactly** — bit-identical, not approximately. This is
algebraic, not numerical: the permutation acts on the filter's state indices, and every sum in
§2.2's recursion runs over all states.

**Consequences.**

- The likelihood has $k!$ global maxima (times whatever local structure §4.2 adds).
- Regime *indices* carry no meaning without an extra convention.
- Any statement of the form "regime 1 is the crisis regime" is a **claim that must be derived from
  the fit**, never assumed.

The Markov structure does **not** rescue identifiability. It makes the model identified *up to
permutation*, which is precisely why a labelling convention suffices and nothing stronger is needed.
Canonical reference: Frühwirth-Schnatter (2006) ch. 3.

### 5.2 Remedies

| Remedy | Mechanism | Trade-off |
|---|---|---|
| **Ordering (identifiability) constraint** | Restrict $\Theta$ to one representative per permutation orbit, e.g. $\sigma_0^2 \le \sigma_1^2$ | Clean *if* implemented as a smooth reparameterization (§4.3), broken if implemented as a sort (§4.4). Choose the ordering variable that actually separates the regimes — for financial returns, variance, not mean |
| **Post-hoc relabelling** | Fit freely; permute the fitted output afterwards | Trivially correct for MLE: one fit, one permutation, zero effect on the optimization. §5.3 |
| **Random-permutation sampling** | Bayesian: permute labels each MCMC sweep, then relabel draws (k-means in parameter space; Stephens 2000) | MCMC only |
| **Order-imposing priors** | Bayesian: a prior supported on one orbit representative | MCMC only; the prior is doing the identifying |

### 5.3 Post-hoc relabelling is a coordinate choice, not a restriction

The argument, in three steps, because it is the one that justifies doing nothing during estimation:

1. The likelihood is exactly invariant under a joint permutation (§5.1).
2. Therefore labelling is a **naming indeterminacy, not a restriction on the model**. $\theta$ and
   $\theta'$ are two names for the *same distribution* over $(r_1,\dots,r_T)$. A "constraint" that
   picks one does not narrow the set of distributions under consideration — it chooses a coordinate
   chart.
3. Therefore resolve it *after* fitting. There is no wrong basin to keep the optimizer out of; both
   have identical height.

The payoff is §4.6: because nothing intercepts $\theta$ during estimation, the fitted point is an
ordinary interior stationary point in the full parameter space, and Hessian-based standard errors
are legitimate. It also means an ordering constraint **costs zero degrees of freedom** in §6.1 —
it removes a duplicate mode, not a dimension.

**The operational hazard.** The identified index is **data-dependent**. Which fitted index carries
the larger variance can differ between a synthetic fixture and real data, between two samples, and
between two windows of the same walk-forward. It must be recomputed for every fit and never cached
or hard-coded. A hard-coded index inverts the signal — maximum insurance in calm markets, none in
crises — while every shape-and-reproducibility test keeps passing.

### 5.4 What identification does not give you

Naming the high-variance regime says nothing about whether $k=2$ is right, whether the emissions
are Gaussian, whether the transitions are first-order, or whether the higher-variance regime
deserves an economic name at all. It fixes the coordinate system. That is all.

---

## 6. Choosing $k$, and testing for regimes

### 6.1 Information criteria

$$\text{AIC} = -2\,\ell(\hat\theta) + 2\kappa, \qquad
\text{BIC} = -2\,\ell(\hat\theta) + \kappa\log T,
\qquad \text{AICc} = \text{AIC} + \frac{2\kappa(\kappa+1)}{T-\kappa-1}$$

with $\kappa$ the number of **effective** free parameters — which is where the care goes, since a
parameter fixed by fiat has no degrees of freedom and a library will happily count the length of
the parameter vector instead. Three cases, kept separate:

| Restriction type | Cost in $\kappa$ | Note |
|---|---|---|
| **Point restriction** ($\mu_0 = \mu_1$, or $p_{00}$ pinned) | exactly 1 each | The straightforward case |
| **Inequality restriction** ($p_{11} \le 0.85$) | 0 while slack | When it **binds** you are at a boundary, and no value of $\kappa$ makes the usual asymptotics apply |
| **Ordering constraint** ($\sigma_0^2\le\sigma_1^2$) | 0 | A labelling convention (§5.3), not a dimension |

Also note that AIC and BIC differ in what they target — AIC estimates predictive KL divergence,
BIC approximates the Bayesian marginal likelihood — so they answer different questions and are
allowed to disagree. When they agree, the case is stronger than either alone. And a caveat specific
to this class: the regularity conditions behind both criteria are the same ones §6.2 shows to fail
when comparing $k$, so treat them as **evidence, not tests**.

### 6.2 Why the LR test for the number of regimes is invalid

The obvious move — likelihood-ratio test of $k=1$ against $k=2$, refer $2\Delta\ell$ to
$\chi^2_\nu$ — **is invalid, and not marginally so.** Under $H_0: k=1$ the two-regime model is
unidentified three ways at once:

1. **Nuisance parameters unidentified under the null.** Set $\sigma_0^2=\sigma_1^2$ and
   $\mu_0=\mu_1$: the transition probabilities vanish from the likelihood entirely. Any values give
   an identical fit. Wilks' theorem requires all parameters identified under $H_0$.
2. **Parameters on the boundary.** You can also reach the null via $\pi_1 \to 0$, a boundary of the
   parameter space. Boundary nulls give mixtures of $\chi^2$ *at best* (Chernoff 1954;
   Self & Liang 1987).
3. **Zero score.** At the null, the derivative of $\ell$ in the mixing direction is identically
   zero, so the quadratic expansion that produces the $\chi^2$ limit degenerates.

Any one of the three breaks Wilks. All three together mean the null distribution of the LR
statistic is **not $\chi^2$ with any degrees of freedom**, and using $\chi^2$ **massively
over-rejects** — you will "find" regimes in i.i.d. Gaussian noise. The same objection applies to
$k=2$ versus $k=3$: an information-criterion comparison must never be reinterpreted as a
significance test.

### 6.3 What to use instead

- **Parametric bootstrap** — the practical default. Simulate $B$ samples from the fitted
  $k$-regime model, refit both specifications to each, read the null distribution of $2\Delta\ell$
  off the draws. Expensive, assumption-light, and correct if the null model is.
- **Davies (1977, 1987) bound** — a cheap conservative upper bound on the p-value via the
  upcrossing argument. The least you can do.
- **Hansen (1992)** — the canonical empirical-process treatment: treat the likelihood as a function
  of the unidentified nuisance parameters and bound its supremum.
- **Garcia (1998)** — the Markov-switching-specific null distribution.
- **Carrasco, Hu & Ploberger (2014)** — an asymptotically optimal test that does **not require
  fitting the switching model at all**. The most practical of the formal options.

**A restriction *within* a fixed $k$ is by contrast entirely standard.** $H_0:\mu_0=\mu_1$ is a
single point restriction on identified parameters at an interior point, so $\chi^2_1$ applies
normally. Note what it asks, though: whether the two means *differ*, not whether either is
individually significant.

---

## 7. Diagnostics

### 7.1 Why classical regression diagnostics do not transfer

| Diagnostic | Why it is vacuous or inverted here |
|---|---|
| $R^2$, residual-vs-fitted, linearity of $E[y\mid x]$ | There is no $x$. Nothing to be linear in, no variation explained by covariates. "Fitted values" are $\sum_j\xi_{t|t}(j)\hat\mu_j$ — a monotone re-reading of the regime probability, so plotting residuals against them plots them against the signal |
| Homoscedasticity (Breusch–Pagan, White) | **Deliberately violated.** Heteroskedasticity is the thing being estimated. A rejection is the model working |
| Normality of raw residuals $r_t - \bar r$ | Guaranteed to fail: by construction the raw residual is a location–scale mixture, hence leptokurtic (§1.7). Testing it tests the premise, not the fit |
| Durbin–Watson / Ljung–Box on raw returns | Confounds regime persistence (§1.7's $\lambda^h$ term) with genuine serial correlation |

What replaces them: the residual defined in §7.2, tested by §7.3–7.5; the regime-specific
diagnostics of §7.6; and, above all, out-of-sample predictive scoring (§3.5), which is the only
family of checks that cannot be satisfied by overfitting.

### 7.2 Regime-standardized residuals

The specification says $r_t = \mu_{S_t} + \sigma_{S_t}\varepsilon_t$ with $\varepsilon_t$ i.i.d.
$\mathcal N(0,1)$. So the object to test is

$$z_t = \frac{r_t - \hat\mu_{S_t}}{\hat\sigma_{S_t}}$$

which under correct specification is i.i.d. standard normal. Note the numerator: **with a switching
mean, subtracting a single sample mean is wrong** and manufactures skew all by itself.

$S_t$ is unobserved, so there are two constructions:

**Hard classification.** $\hat S_t = \arg\max_j \xi_{t|t}(j)$, then standardize by that regime's
moments. Simple, interpretable, discards classification uncertainty. The usual primary version.

**Probability-weighted.** Standardize by the moments of the *mixture*, which with a switching mean
means the law of total variance (§1.7):

$$m_t = \sum_j \xi_{t|t}(j)\hat\mu_j, \qquad
v_t = \sum_j \xi_{t|t}(j)\big(\hat\sigma_j^2 + \hat\mu_j^2\big) - m_t^2$$

**not** the shortcut $v_t = \sum_j \xi_{t|t}(j)\hat\sigma_j^2$, which drops the between-regime term
and understates the variance whenever the regime is uncertain *and* the means differ. This $z_t$ is
not exactly standard normal even under correct specification (a mixture standardized by its own
first two moments is not normal — §3.2 again), so test it against a **simulated reference
distribution**, not against $\mathcal N(0,1)$ tables.

**Which probabilities to use** follows §2.7: $\xi_{t|t}$ for anything describing the signal,
$\xi_{t|T}$ only for retrospective description.

### 7.3 Normality: QQ plot and Jarque–Bera

$$\text{JB} = \frac{T}{6}\left(\widehat{\text{skew}}^2
+ \frac{(\widehat{\text{kurt}}-3)^2}{4}\right) \;\xrightarrow{d}\; \chi^2_2$$

Jarque & Bera (1980). Always read the QQ plot next to it: JB gives one number, the plot tells you
*where* the failure is, and here the informative region is the tails.

The diagnostic reading that matters: a QQ plot **straight in the body but bending in the extreme
left tail** means the variance mixture handles ordinary periods but not genuine tail events. The
fix for that is heavier-tailed emissions — a **Markov-switching model with $t$-distributed
innovations** (Klaassen 2002) — **not** another regime. Adding regimes to fix a tail problem is
fitting a step function to a shape problem.

### 7.4 Ljung–Box on $z_t$

$$Q(m) = T(T+2)\sum_{h=1}^{m}\frac{\hat\rho_h^2}{T-h}\;\xrightarrow{d}\;\chi^2_m$$

Ljung & Box (1978), on the sample autocorrelations of $z_t$; $H_0$ is no autocorrelation to lag
$m$. Rejection means predictable **level** dynamics the model omits, and the named extension is a
Markov-switching AR — which sets the emission order above zero and makes the Kim smoother
approximate rather than exact (§2.7).

Practical note: equity returns rarely reject this at weekly or daily frequency. If yours does, and
especially at lag 1, **suspect the data pipeline before the model** — overlapping bars, misaligned
resampling, or a stale-price effect will all show up here first.

### 7.5 ARCH-LM on $z_t$: the test that decides the specification

Engle (1982). Regress the squared standardized residual on its own lags:

$$z_t^2 = \alpha_0 + \sum_{i=1}^{q}\alpha_i z_{t-i}^2 + u_t,
\qquad \text{LM} = T R^2 \;\xrightarrow{d}\; \chi^2_q
\quad\text{under } H_0:\ \alpha_1=\dots=\alpha_q=0$$

Ljung–Box on $z_t^2$ tests the same hypothesis with a different statistic; report both, they rarely
disagree.

**Why this is the sharpest test of the whole model class.** The specification asserts that
conditional volatility takes exactly $k$ **discrete values** — a step function. The competing
hypothesis is that volatility moves on a **continuum**, drifting and clustering *within* what the
model calls a single regime. If the continuum view is right, then dividing by a constant
$\hat\sigma_j$ across an entire episode leaves the clustering intact, and $z_t^2$ stays
autocorrelated.

So ARCH-LM on $z_t$ is a direct test of **"are $k$ variance levels enough, or is volatility
continuous?"** — the only diagnostic in this list that asks it, and the one whose answer determines
whether you stay in this model class.

**Read the remedy correctly.** A third regime makes the step function finer without making it a
continuum, and typically buys much less than it costs. The relevant literature is the long-running
**regime-switching versus GARCH** debate (§9): SWARCH and MS-GARCH combine the two rather than
choosing, which is usually the honest response to a rejecting ARCH-LM.

### 7.6 Two diagnostics specific to regime-switching models

**Regime classification measure (RCM).** Ang & Bekaert (2002). For $k$ regimes,

$$\text{RCM} = 100\,k^k\,\frac{1}{T}\sum_t\prod_j \xi_t(j),
\qquad\text{for } k=2:\quad \text{RCM} = \frac{400}{T}\sum_t \hat p_t(1-\hat p_t)$$

$0$ = perfectly sharp classification, $100$ = no information (probabilities pinned at $1/k$
throughout). Computed on **filtered** probabilities if you want it to describe the signal; on
smoothed if you want it to describe the historical dating. Its value: when probabilities hover in
the ambiguous middle, RCM tells you whether that is *the market* being genuinely ambiguous or *the
model* being uninformative — which the probability path alone cannot.

**Duration realism.** Fitted $1/(1-\hat p_{ii})$ against the empirical run-length distribution of
the classified state, remembering §1.6 (compare distributions, not means). Persistent
overestimation of duration usually means the classifier is chopping long episodes into pieces at
threshold crossings; persistent underestimation means the geometric assumption is fighting the data
and a semi-Markov model is indicated.

### 7.7 The synthetic-fixture trap

A fixture simulated from exactly the model being fitted will pass every diagnostic in this section
— that is what it is for, and it is the right way to test that the *code* is correct. It says
nothing whatever about whether the *model* fits reality, and the same battery on real data can
reject the same specification at $p < 10^{-6}$.

State the distinction every time results are reported: **fixture results validate the
implementation; real-data results validate the model.** Confusing the two is how a specification
survives longer than its evidence.

---

## 8. Extensions, in the order you would reach for them

Each row is a specific assumption from §1.1 being relaxed, with the diagnostic that sends you
there.

| Extension | Relaxes | Reach for it when | Cost |
|---|---|---|---|
| **Student-$t$ emissions** (Klaassen 2002) | Gaussian emissions | $z_t$ still fat-tailed, QQ bending only in the tails (§7.3) | One df parameter per regime (or shared). Cheap; usually the first thing to try |
| **More regimes**, $k>2$ | $k=2$ | Information criteria prefer it *and* the extra regime is economically interpretable | $2k + k(k-1)$ parameters, worse multimodality, harder identification, more label-switching risk |
| **Markov-switching AR** | Conditional independence of emissions | Ljung–Box on $z_t$ rejects (§7.4) | The Kim smoother becomes **approximate** (§2.7); the filter's state must track lagged regimes |
| **SWARCH** (Hamilton & Susmel 1994) | Constant variance within regime | ARCH-LM rejects (§7.5) | An ARCH process whose scale shifts with the latent regime. The direct answer to the step-function-vs-continuum problem |
| **MS-GARCH** (Gray 1996; Haas, Mittnik & Paolella 2004) | Same, with GARCH memory | Same, and you want persistence too | The exact version is **path-dependent** ($k^t$ histories) and infeasible; Gray and Haas et al. are the two standard tractable collapses |
| **TVTP** — time-varying transition probabilities (Filardo 1994; Diebold, Lee & Weinbach 1994) | Time-homogeneous transitions | You have a covariate that should drive regime *switching* (a credit spread, VIX term structure) | $p_{ij,t} = \Lambda(x_t'\beta)$ via logistic link. Adds parameters and a covariate-timing problem: $x_t$ must be point-in-time |
| **Semi-Markov / duration dependence** | Geometric durations | Empirical run lengths clearly non-geometric (§7.6) | Explicit duration distribution per regime; the filter grows a duration dimension |
| **Multivariate / factor MS** | Univariate observation | You want cross-asset regimes | $k$ covariance matrices; parameters explode as $O(kn^2)$ |

Rule of thumb for the whole table: **relax the assumption the diagnostics reject, not the one that
is easiest to relax.** Adding regimes is easy and is almost never the answer to a tail or a
clustering failure.

---

## 9. Annotated further reading

Organized by the question each source answers.

**Founding papers — these two, in this order.**
**Hamilton (1989)**, *Econometrica* 57(2), 357–384 → §2's filter derivation and the original
switching-*mean* specification; also the origin of the "smoothed probabilities for historical
dating" convention that §2.7 warns about inheriting without its caveat.
**Kim (1994)**, *J. Econometrics* 60(1–2), 1–22 → the backward recursion, including exactly when it
is exact.

**Textbooks — for when a paper assumes something you do not have.**
**Hamilton (1994)**, *Time Series Analysis*, ch. 22 → the cleanest single exposition of filter +
smoother + MLE; start here if the 1989 notation fights you.
**Kim & Nelson (1999)**, *State-Space Models with Regime Switching*, ch. 4–5 → what most
implementations actually implement, algorithm by algorithm.
**Frühwirth-Schnatter (2006)**, *Finite Mixture and Markov Switching Models* → ch. 1–3
identifiability, §3.2 ordering constraints, ch. 3.7 / 11 label switching. The authority for §5.
**McLachlan & Peel (2000)**, ch. 2–3 → why the mixture likelihood is unbounded and multimodal; the
theory behind §4.2.

**Estimation machinery.**
Dempster, Laird & Rubin (1977), *JRSS-B* 39(1) → EM, and why the M-steps are weighted moments.
Baum, Petrie, Soules & Weiss (1970), *Ann. Math. Stat.* 41(1) → the HMM-specific "Baum–Welch".
**Rabiner (1989)**, *Proc. IEEE* 77(2) → the most readable derivation of forward–backward anywhere;
read §V if §2.4 feels opaque, and §VI for Viterbi.
Louis (1982), *JRSS-B* 44(2) → observed information from EM output (§4.6).
Bickel, Ritov & Rydén (1998), *Ann. Stat.* 26(4); Douc, Moulines & Rydén (2004), *Ann. Stat.* 32(5)
→ the asymptotic theory of §4.7. Leroux (1992) for consistency.

**Testing for regimes — §6.**
**Hansen (1992)**, "The Likelihood Ratio Test under Nonstandard Conditions", *JAE* 7(S1), S61–S82
→ the canonical treatment of why your LR test is invalid; read the introduction even if you skip
the empirical-process machinery.
**Davies (1987)**, *Biometrika* 74(1), 33–43 (and Davies 1977) → the upcrossing bound; the cheapest
correct thing you can compute.
Garcia (1998), *IER* 39(3) → the MS-specific null distribution. Cho & White (2007), *Econometrica*
75(6) → quasi-LR. **Carrasco, Hu & Ploberger (2014)**, *Econometrica* 82(2) → an optimal test that
does not require fitting the switching model.

**Regimes versus GARCH — §7.5, §8.**
**Hamilton & Susmel (1994)**, *J. Econometrics* 64(1–2), 307–333 → SWARCH; the direct answer to a
rejecting ARCH-LM and worth reading *before* considering another regime.
Gray (1996), *JFE* 42(1) → tractable MS-GARCH and the path-dependence that makes the exact version
infeasible. Haas, Mittnik & Paolella (2004), *JFEc* 2(4) → the modern practical choice.
Cai (1994), *JBES* 12(3) → the other simultaneous SWARCH paper.
**Lamoureux & Lastrapes (1990)**, *JBES* 8(2), 225–234 (and Diebold 1986) → the reverse argument:
ignoring regime shifts *inflates* GARCH persistence. Read it so you do not conclude "GARCH wins"
from one failing diagnostic.
Ang & Timmermann (2012), *ARFE* 4 → survey of the whole area.

**Real-time evaluation and density scoring — §2.7, §3.5.**
**Chauvet & Piger (2008)**, *JBES* 26(1), 42–49 → how much apparent regime-detection skill survives
real-time evaluation. Read before building any expanding-window backtest.
Rosenblatt (1952); **Diebold, Gunther & Tay (1998)**, *IER* 39(4) → the PIT and density-forecast
evaluation. Berkowitz (2001), *JBES* 19(4) → the LR test built on it.
Gneiting & Raftery (2007), *JASA* 102(477) → proper scoring rules, and why the log score is the one
to use.

**Diagnostics.** Ang & Bekaert (2002), *JBES* 20(2) → RCM (§7.6). Engle (1982), *Econometrica*
50(4) → ARCH-LM. Ljung & Box (1978), *Biometrika* 65(2). Jarque & Bera (1980), *Economics Letters*
6(3).

---

## 10. Glossary

Symbols are in the Notation table, which is canonical and not restated.

| Term | Meaning | § |
|---|---|---|
| Markov-switching model / HMM | Latent discrete state drives the parameters of an observed process; with Gaussian emissions the marginal law is a **location–scale mixture of normals** | 1.1, 1.2 |
| Row- vs column-stochastic | $P$ has rows summing to 1; filtering code usually stores $\Pi = P^{\!\top}$, columns summing to 1. Confusing them transposes the entry and exit rates | 1.3 |
| Ergodic / stationary distribution | $\pi^{\!\top}P = \pi^{\!\top}$; long-run occupancy, unique and limiting by Perron–Frobenius. **Steady-state initialization** sets $\xi_{1\mid0}=\pi$ | 1.4, 2.5 |
| Second eigenvalue / mixing rate | $\lambda = 1 - p_{01} - p_{10}$ for $k=2$; the $h$-step forecast decays to $\pi$ as $\lambda^h$. Sets the honest forecast horizon | 1.5 |
| Expected duration | $1/(1-p_{ii})$, geometric. **As dispersed as it is long** — never quote the mean alone | 1.6 |
| Law of total variance | $\operatorname{Var}(r)=E[\operatorname{Var}(r\mid S)]+\operatorname{Var}(E[r\mid S])$: within-regime plus between-regime | 1.7, 7.2 |
| Hamilton filter / forward algorithm | Forward recursion producing $\xi_{t\mid t}$ and $\ell_t$; Chapman–Kolmogorov propagation then Bayes update | 2.2 |
| Prediction-error decomposition | $f(r_1..r_T)=\prod_t f(r_t\mid\mathcal F_{t-1})$; turns a $k^T$ path sum into $O(Tk^2)$ | 2.3 |
| logsumexp | $\log\sum e^{x_i}$, max-shifted; makes the recursion overflow-safe | 2.4 |
| Viterbi | DP for the single most likely state *path* — not the sequence of marginal modes | 2.6 |
| Kim smoother / forward–backward | Backward recursion for $\xi_{t\mid T}$; **exact** iff emissions depend only on the contemporaneous state | 2.7 |
| Look-ahead bias | Using data unavailable at decision time. Cured by real-time (recursive) refitting; the parameter channel survives fixing the state channel | 2.7 |
| Predictive density | $f_{t+1\mid t}(r)=\sum_j w_j\phi(r;\mu_j,\sigma_j^2)$; everything decision-relevant is a functional of it | 3.1 |
| Moment matching fallacy | A mixture's quantiles are not the quantiles of a normal with its mean and variance — which is the point of using a mixture | 3.2 |
| Proper scoring rule | A score minimized in expectation only by the true density; the log score is strictly proper | 3.5 |
| PIT (probability integral transform) | $u_t = F_{t+1\mid t}(r_{t+1})$ is i.i.d. $U(0,1)$ iff the density forecast is correct (Rosenblatt) | 3.5 |
| Reparameterization / link function | Smooth bijection $\mathbb R^d \to \Theta$ (softmax, logit, log); the **only** correct way to constrain a gradient optimizer | 4.3 |
| Projection / retraction | Clipping or sorting inside the objective. Idempotent but not injective: kinks the surface, breaks exact gradients, and fails silently | 4.4 |
| Complex-step differentiation | Exact derivative via $\operatorname{Im}f(x+ih)/h$; requires $f$ **analytic**, which any comparison operation destroys | 4.4 |
| EM / Baum–Welch | Monotone iterative MLE for latent-variable models; closed-form weighted-moment M-steps, linear convergence. Warm start for a quasi-Newton finish | 4.5 |
| Unbounded likelihood | $\sigma_j^2\to0$ on one observation sends the density to $\infty$; the MLE is a **local interior** maximizer, hence random restarts | 4.2, 4.7 |
| Fisher identity / Louis' method | The score equals the complete-data score averaged over the smoothed posterior; gives the information matrix from EM output | 4.6 |
| Delta method | $\operatorname{Var}(g(\hat\theta))\approx\nabla g^{\!\top}V\nabla g$; duration's variance carries a **squared** amplification | 4.6 |
| Label switching | The likelihood is exactly invariant to consistent permutation of regime labels; $k!$ equivalent maxima | 5.1 |
| Ordering constraint | Picks one representative per permutation orbit. Costs **zero** degrees of freedom | 5.2, 6.1 |
| Post-hoc relabelling | Fit freely, name the regimes afterwards. Legitimate because labelling is a **naming indeterminacy** — it indexes coordinates, not distributions. The index is data-dependent and must never be cached | 5.3 |
| Interior stationary point | $\nabla\ell = 0$ inside $\Theta$; precondition for Hessian-based inference. A **boundary solution** has a non-normal limiting distribution | 4.3, 4.6 |
| Nuisance parameter unidentified under the null | Why the LR test for $k$ is non-standard; the Davies/Hansen problem | 6.2 |
| Regime-standardized residual | $z_t=(r_t-\hat\mu_{S_t})/\hat\sigma_{S_t}$; i.i.d. $\mathcal N(0,1)$ under correct specification | 7.2 |
| ARCH-LM | $TR^2$ from regressing $z_t^2$ on its lags. Tests **step function versus continuum** — the decisive test for this model class | 7.5 |
| RCM | Regime classification measure: 0 = sharp, 100 = uninformative | 7.6 |
| SWARCH / MS-GARCH | Regime switching combined with within-regime ARCH/GARCH | 7.5, 8 |
| TVTP | Transition probabilities driven by covariates through a logistic link | 8 |
| Jump-diffusion | Continuous-time diffusion + compound Poisson jumps. **Not this model** | 1.2 |
