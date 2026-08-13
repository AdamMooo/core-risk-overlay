"""Scoring machinery for conditional risk estimates.

Deliberately knows nothing about which model produced the estimate: it takes a
conditional mean and volatility (or a VaR series directly) and scores it. A
constant, a trailing-volatility rung and VIX are therefore scored by exactly
this code, which is what keeps the comparison honest.

Density calibration -- the PIT (Rosenblatt 1952) and the Berkowitz (2001) LR,
full and tail-censored. This is the PRIMARY test: u = F(r) is iid U(0,1) under
any correctly-specified density, so the identical code scores a constant, an
EWMA rung, VIX and the regime mixture.

Quantile calibration -- Kupiec (1995) unconditional coverage, Christoffersen
(1998) independence and conditional coverage.

Incremental information over implied volatility -- the encompassing regression
    RV[t, t+h] = a + b*IV[t] + c*X[t] + e
with Newey-West standard errors, which are required rather than optional:
overlapping h-period horizons make the errors autocorrelated by construction,
so plain OLS standard errors overstate significance.

Still to build -- the Engle-Manganelli dynamic quantile test, tick loss with
Diebold-Mariano, and the ES breach-severity bootstrap. See
docs/RESEARCH-PROTOCOL.md sections 5 and 10.
"""
from __future__ import annotations

from threading import Lock
from typing import Final, NamedTuple

DEFAULT_ALPHA: Final[float] = 0.05

# u_t exactly 0 or 1 sends z_t to +-inf and takes the whole log-likelihood with
# it. Clipping is unavoidable, but a clipped observation is the model's WORST
# miss -- the density called the realized return impossible. Every result that
# clips carries the count, so the number can never be swallowed silently.
PIT_CLIP_EPS: Final[float] = 1e-10

_DEPS: tuple[object, object, object, object, object] | None = None
_DEPS_LOCK = Lock()


def _require_dependencies():
    global _DEPS

    if _DEPS is not None:
        return _DEPS

    with _DEPS_LOCK:
        if _DEPS is not None:
            return _DEPS

        try:
            import numpy as np
            import pandas as pd
            import statsmodels.api as sm
            from scipy import optimize, stats
        except ModuleNotFoundError as exc:
            raise ModuleNotFoundError(
                "evaluation.py requires numpy, pandas, scipy and statsmodels."
            ) from exc

        _DEPS = (np, pd, sm, stats, optimize)

    return _DEPS


class CoverageResult(NamedTuple):
    n: int
    exceedances: int
    expected_rate: float
    observed_rate: float
    lr_uc: float
    p_uc: float
    lr_ind: float
    p_ind: float
    lr_cc: float
    p_cc: float


class EncompassingResult(NamedTuple):
    n: int
    horizon: int
    hac_lags: int
    const: float
    beta_implied: float
    gamma_model: float
    se_const: float
    se_implied: float
    se_model: float
    t_implied: float
    t_model: float
    p_implied: float
    p_model: float
    r_squared: float


class BerkowitzResult(NamedTuple):
    n: int
    n_clipped: int
    mu: float
    rho: float
    sigma2: float
    log_likelihood: float
    log_likelihood_null: float
    lr: float
    df: int
    p_value: float


class CensoredBerkowitzResult(NamedTuple):
    n: int
    n_tail: int
    alpha: float
    cutoff: float
    n_clipped: int
    mu: float
    sigma2: float
    log_likelihood: float
    log_likelihood_null: float
    lr: float
    df: int
    p_value: float


class PitDiagnostics(NamedTuple):
    n: int
    n_clipped: int
    bins: int
    bin_counts: tuple[int, ...]
    bin_expected: float
    uniformity_chi2: float
    uniformity_p: float
    lags: int
    acf_level: tuple[float, ...]
    acf_squared: tuple[float, ...]
    ljung_box_level: float
    ljung_box_level_p: float
    ljung_box_squared: float
    ljung_box_squared_p: float


def normal_var(conditional_mean, conditional_vol, alpha: float = DEFAULT_ALPHA):
    """Lower-tail VaR under a conditional normal. Returned as a return level."""
    np, _, _, stats, _ = _require_dependencies()
    _validate_alpha(alpha)
    return conditional_mean + conditional_vol * stats.norm.ppf(alpha)


def normal_expected_shortfall(conditional_mean, conditional_vol, alpha: float = DEFAULT_ALPHA):
    """E[r | r < VaR_alpha] under a conditional normal."""
    np, _, _, stats, _ = _require_dependencies()
    _validate_alpha(alpha)
    z = stats.norm.ppf(alpha)
    return conditional_mean - conditional_vol * stats.norm.pdf(z) / alpha


def _validate_alpha(alpha: float) -> None:
    if not 0.0 < alpha < 1.0:
        raise ValueError("alpha must lie strictly between 0 and 1.")


def _safe_log(x: float) -> float:
    np, _, _, _, _ = _require_dependencies()
    # A cell count of zero contributes nothing to the log-likelihood; guarding
    # here keeps a degenerate transition table from producing -inf.
    return float(np.log(x)) if x > 0.0 else 0.0


def coverage_tests(exceedances, alpha: float = DEFAULT_ALPHA) -> CoverageResult:
    """Kupiec unconditional coverage and Christoffersen independence.

    `exceedances` is a boolean series: True where the realized return breached
    the VaR estimate made before that period.
    """
    np, _, _, stats, _ = _require_dependencies()
    _validate_alpha(alpha)

    hits = np.asarray(exceedances, dtype=bool).ravel()
    n = hits.size
    if n < 2:
        raise ValueError("At least two observations are required.")

    x = int(hits.sum())
    pi_hat = x / n

    # Kupiec proportion-of-failures: LR = -2 log( L(alpha) / L(pi_hat) ), chi2(1).
    ll_null = (n - x) * _safe_log(1.0 - alpha) + x * _safe_log(alpha)
    ll_alt = (n - x) * _safe_log(1.0 - pi_hat) + x * _safe_log(pi_hat)
    lr_uc = -2.0 * (ll_null - ll_alt)
    p_uc = float(stats.chi2.sf(lr_uc, 1))

    # Christoffersen independence: exceedances should not cluster. Counts of
    # transitions i -> j between consecutive periods.
    previous, current = hits[:-1], hits[1:]
    n00 = int(np.sum(~previous & ~current))
    n01 = int(np.sum(~previous & current))
    n10 = int(np.sum(previous & ~current))
    n11 = int(np.sum(previous & current))

    pi_01 = n01 / (n00 + n01) if (n00 + n01) > 0 else 0.0
    pi_11 = n11 / (n10 + n11) if (n10 + n11) > 0 else 0.0
    pi_bar = (n01 + n11) / (n00 + n01 + n10 + n11)

    ll_ind_null = (n00 + n10) * _safe_log(1.0 - pi_bar) + (n01 + n11) * _safe_log(pi_bar)
    ll_ind_alt = (
        n00 * _safe_log(1.0 - pi_01)
        + n01 * _safe_log(pi_01)
        + n10 * _safe_log(1.0 - pi_11)
        + n11 * _safe_log(pi_11)
    )
    lr_ind = -2.0 * (ll_ind_null - ll_ind_alt)
    p_ind = float(stats.chi2.sf(lr_ind, 1))

    lr_cc = lr_uc + lr_ind
    p_cc = float(stats.chi2.sf(lr_cc, 2))

    return CoverageResult(
        n=n,
        exceedances=x,
        expected_rate=alpha,
        observed_rate=pi_hat,
        lr_uc=float(lr_uc),
        p_uc=p_uc,
        lr_ind=float(lr_ind),
        p_ind=p_ind,
        lr_cc=float(lr_cc),
        p_cc=p_cc,
    )


def realized_forward(returns, horizon: int, statistic: str = "vol"):
    """Realized risk over (t, t+horizon], aligned to the decision made at t.

    Strictly forward-looking and therefore an EVALUATION target only. Feeding
    this back into a signal would be look-ahead bias -- see
    docs/POINT-IN-TIME-DISCIPLINE.md.
    """
    np, pd, _, _, _ = _require_dependencies()

    series = pd.Series(returns).astype("float64")
    if horizon < 1:
        raise ValueError("horizon must be at least 1 period.")

    reversed_series = series[::-1]
    if statistic == "vol":
        out = reversed_series.rolling(horizon).std()[::-1]
    elif statistic == "semivol":
        # Downside semivolatility: only negative deviations, which is the half
        # of the distribution a long book actually cares about.
        downside = series.where(series < 0.0, 0.0)
        out = (downside[::-1] ** 2).rolling(horizon).mean()[::-1] ** 0.5
    elif statistic == "sum":
        out = reversed_series.rolling(horizon).sum()[::-1]
    elif statistic == "min":
        out = reversed_series.rolling(horizon).min()[::-1]
    else:
        raise ValueError(f"Unknown statistic '{statistic}'.")

    return out.shift(-1)


def encompassing_regression(
    realized, implied, model_measure, horizon: int, hac_lags: int | None = None
) -> EncompassingResult:
    """Does `model_measure` add information beyond `implied`?

    Newey-West lags default to horizon - 1, the minimum needed to account for
    the moving-average structure that overlapping horizons induce.
    """
    np, pd, sm, _, _ = _require_dependencies()

    frame = pd.concat(
        [
            pd.Series(realized).rename("rv"),
            pd.Series(implied).rename("iv"),
            pd.Series(model_measure).rename("x"),
        ],
        axis=1,
    ).dropna()

    if frame.empty:
        raise ValueError("No overlapping non-missing observations.")
    if len(frame) < 30:
        raise ValueError(f"Only {len(frame)} usable observations; too few to regress.")

    lags = int(hac_lags) if hac_lags is not None else max(horizon - 1, 0)

    design = sm.add_constant(frame[["iv", "x"]].to_numpy(), has_constant="add")
    fitted = sm.OLS(frame["rv"].to_numpy(), design).fit(
        cov_type="HAC", cov_kwds={"maxlags": lags}
    )

    return EncompassingResult(
        n=int(fitted.nobs),
        horizon=horizon,
        hac_lags=lags,
        const=float(fitted.params[0]),
        beta_implied=float(fitted.params[1]),
        gamma_model=float(fitted.params[2]),
        se_const=float(fitted.bse[0]),
        se_implied=float(fitted.bse[1]),
        se_model=float(fitted.bse[2]),
        t_implied=float(fitted.tvalues[1]),
        t_model=float(fitted.tvalues[2]),
        p_implied=float(fitted.pvalues[1]),
        p_model=float(fitted.pvalues[2]),
        r_squared=float(fitted.rsquared),
    )


def pit_to_normal(u, clip_eps: float = PIT_CLIP_EPS) -> tuple["np.ndarray", int]:
    """z = Phi^-1(u), with clipped observations counted rather than hidden.

    Returns (z, n_clipped). A clipped u is an observation the predictive density
    assigned essentially zero probability -- the single most informative failure
    the model can produce. It must reach the caller as a number.
    """
    np, pd, _, stats, _ = _require_dependencies()

    values = np.asarray(pd.Series(u).dropna(), dtype="float64").ravel()
    if values.size == 0:
        raise ValueError("No non-missing PIT values.")
    if not np.isfinite(values).all():
        raise ValueError("PIT values must be finite.")
    if (values < 0.0).any() or (values > 1.0).any():
        raise ValueError("PIT values must lie in [0, 1]; got values outside.")
    if not 0.0 < clip_eps < 0.5:
        raise ValueError("clip_eps must lie strictly between 0 and 0.5.")

    n_clipped = int(np.sum((values <= clip_eps) | (values >= 1.0 - clip_eps)))
    clipped = np.clip(values, clip_eps, 1.0 - clip_eps)
    return stats.norm.ppf(clipped), n_clipped


def _ar1_negative_log_likelihood(params, z, np) -> float:
    mu, rho, log_sigma = params
    sigma2 = float(np.exp(2.0 * log_sigma))

    # EXACT likelihood: observation 1 contributes its stationary marginal
    # z_1 ~ N(mu/(1-rho), sigma2/(1-rho^2)). The conditional shortcut drops that
    # term and reduces to OLS -- a different statistic, and Berkowitz specifies
    # the exact one. Evaluating null and alternative through this same function
    # is what guarantees LR >= 0 rather than hoping the optimizer behaves.
    stationary_var = sigma2 / (1.0 - rho * rho)
    stationary_mean = mu / (1.0 - rho)
    log_2pi = float(np.log(2.0 * np.pi))

    ll = -0.5 * (
        log_2pi + np.log(stationary_var) + (z[0] - stationary_mean) ** 2 / stationary_var
    )
    residual = z[1:] - mu - rho * z[:-1]
    ll += float(np.sum(-0.5 * (log_2pi + np.log(sigma2) + residual**2 / sigma2)))
    return -float(ll)


def berkowitz_test(u, clip_eps: float = PIT_CLIP_EPS) -> BerkowitzResult:
    """Berkowitz (2001) LR test that the PIT series is iid U(0,1).

    z_t = Phi^-1(u_t); under correct specification z_t ~ iid N(0,1). Fit

        z_t = mu + rho*z_{t-1} + e_t,   e_t ~ N(0, sigma2)

    and LR-test H0: mu=0, rho=0, sigma2=1 against chi2(3). The decomposition is
    the point: mu != 0 is location bias, sigma2 > 1 means the model understates
    risk overall, rho != 0 means it fails to track volatility clustering.

    Primary test of docs/RESEARCH-PROTOCOL.md section 5.1. Applies to ANY
    predictive density, which is why it takes u rather than a model.

    KNOWN BLIND SPOT, measured in checks.py: rho tests autocorrelation in the
    LEVEL of z. Unabsorbed volatility dynamics live in z^2 and are invisible
    here -- a stochastic-vol series scored at constant volatility returns
    mu=0.007, rho=0.041, sigma2=0.998 and p=0.07, failing to reject, while the
    Ljung-Box on (u-0.5)^2 in `pit_diagnostics` rejects at p<1e-16. Never read a
    passing Berkowitz without that companion statistic.
    """
    np, _, _, stats, optimize = _require_dependencies()

    z, n_clipped = pit_to_normal(u, clip_eps)
    n = int(z.size)
    if n < 10:
        raise ValueError(f"Berkowitz needs at least 10 observations; got {n}.")

    # Two starts: the OLS estimate, and the null itself. The AR(1) likelihood is
    # well behaved, but starting at the null guarantees the optimizer can never
    # return a fit worse than H0 and hand back a negative LR.
    lag_corr = float(np.corrcoef(z[1:], z[:-1])[0, 1]) if n > 2 else 0.0
    rho0 = float(np.clip(lag_corr if np.isfinite(lag_corr) else 0.0, -0.9, 0.9))
    mu0 = float(np.mean(z)) * (1.0 - rho0)
    resid0 = z[1:] - mu0 - rho0 * z[:-1]
    sigma0 = max(float(np.std(resid0, ddof=0)), 1e-6)

    bounds = [(None, None), (-0.999, 0.999), (np.log(1e-8), np.log(1e4))]
    best = None
    for start in ([mu0, rho0, float(np.log(sigma0))], [0.0, 0.0, 0.0]):
        fit = optimize.minimize(
            _ar1_negative_log_likelihood, start, args=(z, np),
            method="L-BFGS-B", bounds=bounds,
        )
        if best is None or fit.fun < best.fun:
            best = fit

    mu_hat, rho_hat, log_sigma_hat = (float(v) for v in best.x)
    ll_alt = -float(best.fun)
    ll_null = -_ar1_negative_log_likelihood([0.0, 0.0, 0.0], z, np)

    lr = 2.0 * (ll_alt - ll_null)
    return BerkowitzResult(
        n=n,
        n_clipped=n_clipped,
        mu=mu_hat,
        rho=rho_hat,
        sigma2=float(np.exp(2.0 * log_sigma_hat)),
        log_likelihood=ll_alt,
        log_likelihood_null=ll_null,
        lr=lr,
        df=3,
        p_value=float(stats.chi2.sf(max(lr, 0.0), 3)),
    )


def _censored_negative_log_likelihood(params, z, cutoff, np, stats) -> float:
    mu, log_sigma = params
    sigma = float(np.exp(log_sigma))

    below = z < cutoff
    ll = float(np.sum(stats.norm.logpdf(z[below], loc=mu, scale=sigma)))
    n_above = int(z.size - int(below.sum()))
    if n_above:
        # logsf, not log(1 - cdf): the survival function stays accurate where
        # the complement underflows to exactly 1.0.
        ll += n_above * float(stats.norm.logsf(cutoff, loc=mu, scale=sigma))
    return -ll


def censored_berkowitz_test(
    u, alpha: float = DEFAULT_ALPHA, clip_eps: float = PIT_CLIP_EPS
) -> CensoredBerkowitzResult:
    """Berkowitz LR restricted to the left tail below the alpha-quantile.

    A model can be calibrated in the body and wrong in the tail; the full-sample
    version will not show it. Observations above the cutoff contribute only
    Pr(z > cutoff), so the fit is driven entirely by tail shape.

    df = 2, NOT 3. rho is not identified once most of the sample is censored to
    a single indicator, so the AR term is dropped and only (mu, sigma2) are
    tested. This is the standard tail form and departs from the wording of
    RESEARCH-PROTOCOL section 5.1 as originally written -- logged in that
    document's Amendments section, 2026-08-13.
    """
    np, _, _, stats, optimize = _require_dependencies()
    _validate_alpha(alpha)

    z, n_clipped = pit_to_normal(u, clip_eps)
    n = int(z.size)
    cutoff = float(stats.norm.ppf(alpha))
    n_tail = int(np.sum(z < cutoff))

    # With no tail observations the likelihood is maximized by pushing mu to
    # +inf: an unbounded, meaningless "fit". Refuse rather than report it.
    if n_tail < 10:
        raise ValueError(
            f"Only {n_tail} observations below the alpha={alpha} cutoff; "
            "too few to identify the censored likelihood (need 10)."
        )

    tail = z[z < cutoff]
    bounds = [(None, None), (np.log(1e-8), np.log(1e4))]
    best = None
    for start in ([float(np.mean(tail)), 0.0], [0.0, 0.0]):
        fit = optimize.minimize(
            _censored_negative_log_likelihood, start, args=(z, cutoff, np, stats),
            method="L-BFGS-B", bounds=bounds,
        )
        if best is None or fit.fun < best.fun:
            best = fit

    mu_hat, log_sigma_hat = (float(v) for v in best.x)
    ll_alt = -float(best.fun)
    ll_null = -_censored_negative_log_likelihood([0.0, 0.0], z, cutoff, np, stats)

    lr = 2.0 * (ll_alt - ll_null)
    return CensoredBerkowitzResult(
        n=n,
        n_tail=n_tail,
        alpha=alpha,
        cutoff=cutoff,
        n_clipped=n_clipped,
        mu=mu_hat,
        sigma2=float(np.exp(2.0 * log_sigma_hat)),
        log_likelihood=ll_alt,
        log_likelihood_null=ll_null,
        lr=lr,
        df=2,
        p_value=float(stats.chi2.sf(max(lr, 0.0), 2)),
    )


def tick_loss(returns, var, alpha: float = DEFAULT_ALPHA):
    """Koenker-Bassett asymmetric piecewise-linear loss, per observation.

        L(r, q) = (alpha - 1{r < q}) * (r - q)

    Its expectation is uniquely minimized by the true conditional alpha-quantile.
    That uniqueness -- "consistency" for the quantile functional -- is what makes
    a lower average tick loss evidence rather than an arbitrary preference. See
    RESEARCH-PROTOCOL section 5.4.

    Only DIFFERENCES on the same sample are interpretable. The level carries no
    meaning on its own, so never quote it alone.
    """
    np, pd, _, _, _ = _require_dependencies()
    _validate_alpha(alpha)

    frame = pd.concat(
        [pd.Series(returns).rename("r"), pd.Series(var).rename("q")], axis=1
    ).dropna()
    if frame.empty:
        raise ValueError("No overlapping non-missing observations.")

    r = frame["r"].to_numpy(dtype="float64")
    q = frame["q"].to_numpy(dtype="float64")
    return pd.Series((alpha - (r < q).astype("float64")) * (r - q), index=frame.index)


class DieboldMarianoResult(NamedTuple):
    n: int
    mean_difference: float
    std_error: float
    statistic: float
    p_value: float
    hac_lags: int
    better: str


def diebold_mariano(loss_a, loss_b, hac_lags: int | None = None,
                    label_a: str = "a", label_b: str = "b") -> DieboldMarianoResult:
    """Test whether two loss series differ, Newey-West corrected.

    d_t = loss_a - loss_b; H0 is E[d] = 0, equal predictive accuracy. Negative
    statistic favours `a`. Newey-West is used because loss differences are
    serially correlated even at h=1 -- volatility clusters, so the periods where
    one model beats the other come in runs.

    Diebold & Mariano (1995). With estimated parameters and a rolling window,
    Giacomini & White (2006) is the formally correct reference; the statistic is
    the same, the null is about the forecasting METHOD rather than the model.
    """
    np, pd, _, stats, _ = _require_dependencies()

    frame = pd.concat(
        [pd.Series(loss_a).rename("a"), pd.Series(loss_b).rename("b")], axis=1
    ).dropna()
    n = len(frame)
    if n < 30:
        raise ValueError(f"Only {n} overlapping observations; too few for DM.")

    d = (frame["a"] - frame["b"]).to_numpy(dtype="float64")
    d_bar = float(d.mean())

    lags = int(hac_lags) if hac_lags is not None else int(np.floor(4 * (n / 100) ** (2 / 9)))
    centered = d - d_bar
    gamma0 = float(np.dot(centered, centered) / n)
    variance = gamma0
    for k in range(1, lags + 1):
        gamma_k = float(np.dot(centered[k:], centered[:-k]) / n)
        variance += 2.0 * (1.0 - k / (lags + 1.0)) * gamma_k

    # A negative Newey-West variance is possible with the Bartlett kernel on
    # short samples; fall back to the uncorrected variance rather than emit nan.
    if variance <= 0.0:
        variance = gamma0

    se = float(np.sqrt(variance / n))
    statistic = d_bar / se if se > 0 else 0.0

    return DieboldMarianoResult(
        n=n,
        mean_difference=d_bar,
        std_error=se,
        statistic=float(statistic),
        p_value=float(2.0 * stats.norm.sf(abs(statistic))),
        hac_lags=lags,
        better=label_a if d_bar < 0 else label_b,
    )


def _autocorrelations(x, lags: int, np) -> "np.ndarray":
    centered = x - float(np.mean(x))
    denominator = float(np.dot(centered, centered))
    if denominator <= 0.0:
        raise ValueError("Series has zero variance; autocorrelation is undefined.")
    return np.array(
        [float(np.dot(centered[k:], centered[:-k])) / denominator
         for k in range(1, lags + 1)]
    )


def _ljung_box(acf, n: int, np, stats) -> tuple[float, float]:
    m = acf.size
    k = np.arange(1, m + 1)
    q = float(n * (n + 2) * np.sum(acf**2 / (n - k)))
    return q, float(stats.chi2.sf(q, m))


def pit_diagnostics(u, bins: int = 20, lags: int = 10,
                    clip_eps: float = PIT_CLIP_EPS) -> PitDiagnostics:
    """Histogram and serial-dependence diagnostics on the PIT series.

    Reported alongside Berkowitz per RESEARCH-PROTOCOL section 5.1. The ACF of
    (u - 0.5)^2 is the substantive one: it detects volatility dynamics the model
    has not absorbed, which a level ACF near zero can easily hide.
    """
    np, pd, _, stats, _ = _require_dependencies()

    values = np.asarray(pd.Series(u).dropna(), dtype="float64").ravel()
    _, n_clipped = pit_to_normal(values, clip_eps)
    n = int(values.size)

    if bins < 2:
        raise ValueError("bins must be at least 2.")
    if not 1 <= lags < n:
        raise ValueError(f"lags must lie in [1, {n - 1}]; got {lags}.")

    counts, _ = np.histogram(values, bins=bins, range=(0.0, 1.0))
    expected = n / bins
    chi2_stat = float(np.sum((counts - expected) ** 2 / expected))

    acf_level = _autocorrelations(values, lags, np)
    acf_squared = _autocorrelations((values - 0.5) ** 2, lags, np)
    q_level, p_level = _ljung_box(acf_level, n, np, stats)
    q_squared, p_squared = _ljung_box(acf_squared, n, np, stats)

    return PitDiagnostics(
        n=n,
        n_clipped=n_clipped,
        bins=bins,
        bin_counts=tuple(int(c) for c in counts),
        bin_expected=float(expected),
        uniformity_chi2=chi2_stat,
        uniformity_p=float(stats.chi2.sf(chi2_stat, bins - 1)),
        lags=lags,
        acf_level=tuple(float(v) for v in acf_level),
        acf_squared=tuple(float(v) for v in acf_squared),
        ljung_box_level=q_level,
        ljung_box_level_p=p_level,
        ljung_box_squared=q_squared,
        ljung_box_squared_p=p_squared,
    )
