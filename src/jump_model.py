from __future__ import annotations

from contextlib import contextmanager
from threading import Lock
from typing import Final

CALM_REGIME: Final[int] = 0
JUMP_REGIME: Final[int] = 1
N_REGIMES: Final[int] = 2
DEFAULT_CALM_STAY_PROBABILITY: Final[float] = 0.98
DEFAULT_JUMP_STAY_CEILING: Final[float] = 0.85
DEFAULT_SEARCH_REPS: Final[int] = 50
DEFAULT_MAXITER: Final[int] = 1000
DEFAULT_RANDOM_SEED: Final[int] = 20260811

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
                "jump_model.py requires numpy, pandas, and statsmodels to be installed."
            ) from exc

        _DEPS = (np, pd, MarkovRegression)

    return _DEPS


@contextmanager
def _seeded_numpy_random(seed: int):
    # statsmodels' random start-parameter search reads the global numpy RNG
    # directly (no random_state hook), so this is the only way to make
    # estimate_jump_regimes() reproducible across runs.
    np, _, _ = _require_dependencies()
    saved_state = np.random.get_state()
    np.random.seed(seed)
    try:
        yield
    finally:
        np.random.set_state(saved_state)


def _prepare_weekly_log_returns(weekly_log_returns: "pd.Series") -> "pd.Series":
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


def _check_converged(results) -> None:
    if not results.mle_retvals.get("converged"):
        raise RuntimeError(
            f"Maximum-likelihood fit failed to converge (mle_retvals={results.mle_retvals!r})."
        )


# Regime 0 is calm and regime 1 is jump *by construction*, not by
# post-hoc labeling. Two constraints are enforced jointly on every
# likelihood evaluation:
#
# 1. Variance ordering: sigma2[0] <= sigma2[1]. Pinning persistence alone
#    does not make a regime "calm" -- persistence and variance are
#    independent knobs, and for some data windows (e.g. 2006-2011) the
#    unconstrained MLE actually prefers pairing high variance with high
#    persistence (an 18-month crisis fit as one long sticky regime).
#    Sorting the two fitted variances at every step removes the
#    ambiguity: the low-variance regime is always index 0, full stop.
# 2. Persistence: p[0->0] pinned at `calm_stay_probability`; regime 1's
#    self-persistence capped at `jump_stay_ceiling` (average duration
#    = 1 / (1 - p)) so a long, low-vol-punctuated crisis still can't be
#    fit as one persistent "calm" regime with brief jump interruptions.
#
# statsmodels only parameterizes column 0 of the transition matrix for a
# 2-regime model (`p[0->0]`, `p[1->0]`); regime 1's self-persistence is
# the complement, 1 - p[1->0].
def _constrained_markov_regression(calm_stay_probability: float, jump_stay_ceiling: float):
    np, _, MarkovRegression = _require_dependencies()
    jump_transition_floor = 1.0 - jump_stay_ceiling

    class ConstrainedMarkovRegression(MarkovRegression):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self._sigma2_indices = None
            self._transition_indices = None

        def _indices(self) -> tuple[tuple[int, int], tuple[int, int]]:
            if self._sigma2_indices is None:
                self._sigma2_indices = (
                    self.param_names.index("sigma2[0]"),
                    self.param_names.index("sigma2[1]"),
                )
                self._transition_indices = (
                    self.param_names.index("p[0->0]"),
                    self.param_names.index("p[1->0]"),
                )
            return self._sigma2_indices, self._transition_indices

        def _apply_constraints(self, params):
            (sigma2_calm, sigma2_jump), (p_calm, p_jump) = self._indices()
            params = params.copy()
            params[sigma2_calm], params[sigma2_jump] = sorted(
                (params[sigma2_calm], params[sigma2_jump])
            )
            params[p_calm] = calm_stay_probability
            params[p_jump] = max(params[p_jump], jump_transition_floor)
            return params

        def transform_params(self, unconstrained):
            # statsmodels stores transformed transition/variance parameters
            # as probabilities/positive reals, so constraints apply here directly.
            constrained = super().transform_params(unconstrained)
            return self._apply_constraints(constrained)

        def untransform_params(self, constrained):
            corrected = self._apply_constraints(np.asarray(constrained, dtype=float))
            return super().untransform_params(corrected)

    return ConstrainedMarkovRegression


def estimate_jump_regimes(
    weekly_log_returns: "pd.Series",
    calm_stay_probability: float = DEFAULT_CALM_STAY_PROBABILITY,
    jump_stay_ceiling: float = DEFAULT_JUMP_STAY_CEILING,
    search_reps: int = DEFAULT_SEARCH_REPS,
    maxiter: int = DEFAULT_MAXITER,
    random_seed: int = DEFAULT_RANDOM_SEED,
) -> "pd.Series":
    """Fit a two-regime jump/diffusion proxy and return the smoothed
    probability of being in the jump (panic) regime each week."""
    _, pd, _ = _require_dependencies()

    if not 0.0 < calm_stay_probability < 1.0:
        raise ValueError("calm_stay_probability must lie strictly between 0 and 1.")
    if not 0.0 < jump_stay_ceiling < calm_stay_probability:
        raise ValueError("jump_stay_ceiling must lie strictly between 0 and calm_stay_probability.")

    returns = _prepare_weekly_log_returns(weekly_log_returns)

    ConstrainedMarkovRegression = _constrained_markov_regression(
        calm_stay_probability, jump_stay_ceiling
    )
    model = ConstrainedMarkovRegression(
        returns,
        k_regimes=N_REGIMES,
        trend="c",
        switching_trend=False,
        switching_variance=True,
    )

    with _seeded_numpy_random(random_seed):
        results = model.fit(search_reps=search_reps, maxiter=maxiter, disp=False)

    _check_converged(results)

    parameter_map = dict(zip(model.param_names, results.params))
    if not parameter_map["sigma2[0]"] <= parameter_map["sigma2[1]"]:
        raise RuntimeError(
            "Fitted variances violate the calm-regime ordering constraint "
            "(sigma2[0] <= sigma2[1]); the constrained fit did not converge "
            "to a feasible point."
        )

    smoothed = results.smoothed_marginal_probabilities

    if isinstance(smoothed, pd.DataFrame):
        jump_probabilities = smoothed.iloc[:, JUMP_REGIME].copy()
    else:
        jump_probabilities = pd.Series(smoothed[:, JUMP_REGIME], index=returns.index)

    jump_probabilities = jump_probabilities.astype("float64")
    jump_probabilities.name = "jump_regime_probability"

    return jump_probabilities
