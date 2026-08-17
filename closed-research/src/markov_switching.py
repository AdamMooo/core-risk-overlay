"""Markov-switching model with switching mean and variance (Hamilton 1989).

Renamed from `jump_model.py` on 2026-08-12: that name was wrong. "Statistical
jump model" names a different method (Bemporad et al. 2018; Nystrup et al.
2020-21) which minimizes a penalized loss over the state path and yields no
predictive density. This is a maximum-likelihood latent-state model fitted by
the Hamilton filter, and it does yield one -- a mixture of the regime densities
-- which is what makes conditional VaR and ES available.

The high-variance regime is named for its identification rule: argmax of the
fitted regime variances. Nothing makes it directional; it scores a violent rally
nearly as high as an equal crash (0.9279 up/down probability ratio at
|return| >= 7% on real data). A directional name would overclaim.
"""
from __future__ import annotations

import warnings
from contextlib import contextmanager
from threading import Lock
from typing import Final

N_REGIMES: Final[int] = 2
DEFAULT_SEARCH_REPS: Final[int] = 50
DEFAULT_MAXITER: Final[int] = 1000
DEFAULT_RANDOM_SEED: Final[int] = 20260811
MIN_OBSERVATIONS: Final[int] = 10

# Below this the fit is feasible but not trustworthy. Measured by walkforward.py
# on SPY and QQQ WEEKLY data: at a 260-week minimum window the fits produced
# degenerate parameters (p[0->0] as low as 0.163, p[1->0] pinned at 0.999999, a
# regime variance collapsing to 0.000000), the high-variance label flipped 6
# times across the two tickers, 2-3% of refits failed to converge, and 9.5-16.5%
# of weeks had their risk tier revised by later refits. At a 520-week minimum
# every one of those improved sharply: 1 label flip, 0-1 convergence failures,
# 7.3-7.8% revision, and no degenerate parameter values at all.
#
# This figure is WEEKLY and does not transfer to daily data by multiplying by 5.
# The daily minimum must be re-measured by the same procedure before any daily
# result is quoted. See docs/RESEARCH-PROTOCOL.md section 1.3.
RELIABLE_MIN_OBSERVATIONS: Final[int] = 520

_DEPS: tuple[object, object, object] | None = None
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
            from statsmodels.tsa.regime_switching.markov_regression import MarkovRegression
        except ModuleNotFoundError as exc:
            raise ModuleNotFoundError(
                "markov_switching.py requires numpy, pandas, and statsmodels to be installed."
            ) from exc

        _DEPS = (np, pd, MarkovRegression)

    return _DEPS


@contextmanager
def _seeded_numpy_random(seed: int):
    # statsmodels' random start-parameter search reads the global numpy RNG
    # directly (no random_state hook), so this is the only way to make
    # estimate_high_variance_probability() reproducible across runs.
    np, _, _ = _require_dependencies()
    saved_state = np.random.get_state()
    np.random.seed(seed)
    try:
        yield
    finally:
        np.random.set_state(saved_state)


def _prepare_log_returns(log_returns: "pd.Series") -> "pd.Series":
    np, pd, _ = _require_dependencies()

    returns = pd.Series(log_returns, copy=True).dropna().astype("float64")

    if returns.empty:
        raise ValueError("Log returns are empty.")

    if len(returns) < MIN_OBSERVATIONS:
        raise ValueError(
            f"At least {MIN_OBSERVATIONS} log-return observations are required "
            "to estimate regimes."
        )

    if not np.isfinite(returns).all():
        raise ValueError("Log returns must be finite.")

    if len(returns) < RELIABLE_MIN_OBSERVATIONS:
        warnings.warn(
            f"Fitting on {len(returns)} observations; below "
            f"{RELIABLE_MIN_OBSERVATIONS} the fit is prone to degenerate parameters "
            "and unstable regime labelling. See RELIABLE_MIN_OBSERVATIONS.",
            UserWarning,
            stacklevel=3,
        )

    return returns


def _check_converged(results) -> None:
    if not results.mle_retvals.get("converged"):
        raise RuntimeError(
            f"Maximum-likelihood fit failed to converge (mle_retvals={results.mle_retvals!r})."
        )


# Regime indices are not identified by the likelihood: permuting the labels
# (transition matrix and both regime-specific parameter pairs together) leaves
# the log-likelihood bit-identical. This is the standard label-switching problem
# in mixture and Markov-switching models (Fruhwirth-Schnatter, "Finite Mixture
# and Markov Switching Models").
#
# It is resolved AFTER fitting, by reading which fitted regime carries the
# larger variance, rather than by constraining the optimizer. Enforcing an
# ordering inside transform_params (a previous approach here) is the wrong tool
# for two reasons: labelling is a naming indeterminacy rather than a restriction
# on the model, and the non-differentiable sort corrupted the complex-step
# gradient -- numpy orders complex128 lexicographically, so at a variance tie the
# derivative was credited to the wrong coordinate. BFGS then reported
# convergence having never explored a coordinate at all.
def _high_variance_regime_index(model, results) -> int:
    np, _, _ = _require_dependencies()
    # results.params is name-indexed when endog is a pandas Series, so go
    # positional via the model's own param_names ordering.
    params = np.asarray(results.params, dtype=float)
    variances = [
        params[model.param_names.index(f"sigma2[{regime}]")]
        for regime in range(model.k_regimes)
    ]
    return int(np.argmax(variances))


def fit_markov_switching(
    log_returns: "pd.Series",
    search_reps: int = DEFAULT_SEARCH_REPS,
    maxiter: int = DEFAULT_MAXITER,
    random_seed: int = DEFAULT_RANDOM_SEED,
    k_regimes: int = N_REGIMES,
):
    """Fit the two-regime switching mean/variance model.

    Returns (model, results, high_variance_regime_index). The mean switches as
    well as the variance: with a single common mean the conditional density
    depends only on the squared deviation, which makes the model blind to the
    sign of the return and scores a violent rally as high as an equal-magnitude
    crash. Switching the mean reduces that blindness without removing it.
    """
    _, _, MarkovRegression = _require_dependencies()

    returns = _prepare_log_returns(log_returns)

    model = MarkovRegression(
        returns,
        k_regimes=k_regimes,
        trend="c",
        switching_trend=True,
        switching_variance=True,
    )

    with _seeded_numpy_random(random_seed):
        results = model.fit(search_reps=search_reps, maxiter=maxiter, disp=False)

    _check_converged(results)

    return model, results, _high_variance_regime_index(model, results)


def estimate_high_variance_probability(
    log_returns: "pd.Series",
    search_reps: int = DEFAULT_SEARCH_REPS,
    maxiter: int = DEFAULT_MAXITER,
    random_seed: int = DEFAULT_RANDOM_SEED,
) -> "pd.Series":
    """Real-time probability of being in the high-variance regime each period.

    NOTE: this fits once on the whole series, so the parameters used at time t
    saw the entire sample. The probabilities are filtered but the PARAMETERS are
    not point-in-time. That is leak register #2 and it is fine for correctness
    checks on synthetic data; it is NOT acceptable for any reported result. Use
    the walk-forward path for that.
    """
    _, pd, _ = _require_dependencies()

    model, results, high_variance_regime = fit_markov_switching(
        log_returns,
        search_reps=search_reps,
        maxiter=maxiter,
        random_seed=random_seed,
    )

    # FILTERED, never smoothed. Filtered probabilities condition on data through
    # period t only; statsmodels' smoothed_marginal_probabilities run the Kim
    # smoother, which conditions every period on the entire sample including the
    # future. On real SPY 1993-2026 the two disagree about the 0.5 threshold in
    # 9.7% of weeks, so using smoothed here would put look-ahead bias directly
    # into the signal. See docs/POINT-IN-TIME-DISCIPLINE.md.
    filtered = results.filtered_marginal_probabilities

    if isinstance(filtered, pd.DataFrame):
        probabilities = filtered.iloc[:, high_variance_regime].copy()
    else:
        probabilities = pd.Series(
            filtered[:, high_variance_regime], index=model.data.row_labels
        )

    # The filter's normalization can overshoot 1.0 by an ULP (~2e-16). Harmless
    # in itself, but clip so the returned contract is exactly a probability --
    # a value above 1.0 would produce NaN in any downstream sqrt(1 - p).
    probabilities = probabilities.astype("float64").clip(0.0, 1.0)
    probabilities.name = "high_variance_probability"

    return probabilities
