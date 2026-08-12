from __future__ import annotations

from threading import Lock
from typing import Final


N_REGIMES: Final[int] = 2
CALM_REGIME: Final[int] = 0
DEFAULT_CALM_STAY_PROBABILITY: Final[float] = 0.98
DEFAULT_SEARCH_REPS: Final[int] = 50
DEFAULT_MAXITER: Final[int] = 1000
_DEPS: tuple[object, object, object] | None = None
_DEPS_LOCK = Lock()


def _require_dependencies():
    """Load optional third-party dependencies for the jump model."""
    global _DEPS

    with _DEPS_LOCK:
        if _DEPS is not None:
            return _DEPS

        try:
            import numpy as np
            import pandas as pd
            from statsmodels.tsa.regimeswitching.markov_regression import MarkovRegression
        except ModuleNotFoundError as exc:
            raise ModuleNotFoundError(
                "jump_model.py requires numpy, pandas, and statsmodels to be installed."
            ) from exc

        _DEPS = (np, pd, MarkovRegression)

    return _DEPS


def _transition_parameter_index(model) -> int:
    """Return the parameter index for the calm regime's stay probability."""
    np, _, _ = _require_dependencies()
    transition_indices = np.atleast_1d(model.parameters[CALM_REGIME, "regime_transition"])
    return int(transition_indices[0])



def _prepare_weekly_log_returns(weekly_log_returns: "pd.Series") -> "pd.Series":
    """Validate weekly log returns before passing them into the likelihood engine."""
    np, pd, _ = _require_dependencies()

    returns = pd.Series(weekly_log_returns, copy=True).dropna().astype("float64")

    if returns.empty:
        raise ValueError("Weekly log returns are empty.")

    if len(returns) < 10:
        raise ValueError(
            "At least 10 weekly log-return observations are required to estimate regimes."
        )

    if not np.isfinite(returns).all():
        raise ValueError("Weekly log returns must be finite.")

    return returns


def _extract_jump_regime_index(results) -> int:
    """Identify the regime with the largest fitted variance."""
    parameter_names = list(results.model.param_names)
    parameter_values = list(results.params)
    parameter_map = dict(zip(parameter_names, parameter_values))

    regime_variances = {
        regime: parameter_map[f"sigma2[{regime}]"] for regime in range(N_REGIMES)
    }
    return max(regime_variances, key=regime_variances.get)


def _constrained_markov_regression(calm_stay_probability: float):
    """Create a MarkovRegression subclass with a fixed calm-state persistence."""
    np, _, MarkovRegression = _require_dependencies()
    calm_logit = float(np.log(calm_stay_probability / (1.0 - calm_stay_probability)))

    class ConstrainedMarkovRegression(MarkovRegression):
        def transform_params(self, unconstrained):
            constrained = super().transform_params(unconstrained)
            transition_index = _transition_parameter_index(self)
            # statsmodels stores transformed transition parameters as probabilities.
            constrained[transition_index] = calm_stay_probability
            return constrained

        def untransform_params(self, constrained):
            unconstrained = super().untransform_params(constrained)
            transition_index = _transition_parameter_index(self)
            unconstrained[transition_index] = calm_logit
            return unconstrained

    return ConstrainedMarkovRegression


def estimate_jump_regimes(
    weekly_log_returns: "pd.Series",
    calm_stay_probability: float = DEFAULT_CALM_STAY_PROBABILITY,
    search_reps: int = DEFAULT_SEARCH_REPS,
    maxiter: int = DEFAULT_MAXITER,
) -> "pd.Series":
    """Fit a two-regime jump/diffusion proxy and return jump-state probabilities."""
    _, pd, _ = _require_dependencies()

    if not 0.0 < calm_stay_probability < 1.0:
        raise ValueError("calm_stay_probability must lie strictly between 0 and 1.")

    returns = _prepare_weekly_log_returns(weekly_log_returns)
    ConstrainedMarkovRegression = _constrained_markov_regression(calm_stay_probability)
    model = ConstrainedMarkovRegression(
        returns,
        k_regimes=N_REGIMES,
        trend="c",
        switching_trend=False,
        switching_variance=True,
    )

    results = model.fit(
        search_reps=search_reps,
        maxiter=maxiter,
        disp=False,
    )

    jump_regime = _extract_jump_regime_index(results)
    smoothed = results.smoothed_marginal_probabilities

    if isinstance(smoothed, pd.DataFrame):
        jump_probabilities = smoothed.iloc[:, jump_regime].copy()
    else:
        jump_probabilities = pd.Series(
            smoothed[:, jump_regime],
            index=returns.index,
        )
    jump_probabilities = jump_probabilities.astype("float64")
    jump_probabilities.name = "jump_regime_probability"

    return jump_probabilities
