"""Evaluation machinery for conditional risk estimates.

Implements the three-test standard in README section 1b. Deliberately knows
nothing about which model produced the estimate: it takes a conditional mean
and volatility series (or a VaR series directly) and scores it. Any candidate
-- the regime model, a GARCH variant, VIX itself, a constant -- is just a
different input here and is scored identically.

Test 1, calibration: Kupiec (1995) unconditional coverage and Christoffersen
(1998) independence / conditional coverage.

Test 2, incremental information: the forecast encompassing regression
    RV[t, t+h] = a + b*IV[t] + c*X[t] + e
with Newey-West standard errors, which are required rather than optional --
overlapping h-period horizons make the errors autocorrelated by construction,
so plain OLS standard errors are wrong and will overstate significance.
"""
from __future__ import annotations

from threading import Lock
from typing import Final, NamedTuple

DEFAULT_ALPHA: Final[float] = 0.05

_DEPS: tuple[object, object, object, object] | None = None
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
            from scipy import stats
        except ModuleNotFoundError as exc:
            raise ModuleNotFoundError(
                "evaluation.py requires numpy, pandas, scipy and statsmodels."
            ) from exc

        _DEPS = (np, pd, sm, stats)

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


def normal_var(conditional_mean, conditional_vol, alpha: float = DEFAULT_ALPHA):
    """Lower-tail VaR under a conditional normal. Returned as a return level."""
    np, _, _, stats = _require_dependencies()
    _validate_alpha(alpha)
    return conditional_mean + conditional_vol * stats.norm.ppf(alpha)


def normal_expected_shortfall(conditional_mean, conditional_vol, alpha: float = DEFAULT_ALPHA):
    """E[r | r < VaR_alpha] under a conditional normal."""
    np, _, _, stats = _require_dependencies()
    _validate_alpha(alpha)
    z = stats.norm.ppf(alpha)
    return conditional_mean - conditional_vol * stats.norm.pdf(z) / alpha


def _validate_alpha(alpha: float) -> None:
    if not 0.0 < alpha < 1.0:
        raise ValueError("alpha must lie strictly between 0 and 1.")


def _safe_log(x: float) -> float:
    np, _, _, _ = _require_dependencies()
    # A cell count of zero contributes nothing to the log-likelihood; guarding
    # here keeps a degenerate transition table from producing -inf.
    return float(np.log(x)) if x > 0.0 else 0.0


def coverage_tests(exceedances, alpha: float = DEFAULT_ALPHA) -> CoverageResult:
    """Kupiec unconditional coverage and Christoffersen independence.

    `exceedances` is a boolean series: True where the realized return breached
    the VaR estimate made before that period.
    """
    np, _, _, stats = _require_dependencies()
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
    np, pd, _, _ = _require_dependencies()

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
    np, pd, sm, _ = _require_dependencies()

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
