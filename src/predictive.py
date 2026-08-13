"""One-step-ahead predictive density for a Markov-switching model, and the
conditional VaR and ES that follow from it.

This is the missing link between `markov_switching` (which returns regime
probabilities) and `evaluation` (which scores risk estimates). Regime
probabilities are not a risk measure; a predictive distribution is.

Three steps, per docs/RESEARCH-PROTOCOL.md section 1.1:

    w[j]  = sum_i P[i,j] * filtered[t][i]              push the state forward
    f(r)  = sum_j w[j] * Normal(mu_j, sigma_j)         a MIXTURE, not a normal
    VaR   = the q solving sum_j w[j]*Phi((q-mu_j)/sigma_j) = alpha

The moment-matching shortcut `mean + sqrt(var)*norm.ppf(alpha)` is WRONG, not
merely imprecise: matching a mixture's first two moments does not match its
quantiles, which is the entire reason mixtures are used. Measured at
w=[0.85,0.15], mu=[0.0015,-0.004], sigma=[0.008,0.026], alpha=0.05 the true
mixture VaR is -1.813% and the moment-matched normal is -2.011% -- an 11% error
in the VaR level, with the sign flipping as alpha moves.

Conventions, both of which invert the model silently if broken:

  - `transition` is ROW = FROM: P[i, j] = Pr(s_next = j | s_now = i), so rows
    sum to one. statsmodels stores the transpose (`regime_transition[j, i, t]`,
    columns summing to one); `transition_matrix` does that flip in one place.
  - `sigmas` are standard deviations, never variances. statsmodels reports
    `sigma2[j]`; `regime_parameters` takes the square root.

All returns are RETURN LEVELS (negative in the left tail), never positive loss
magnitudes.
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
            from scipy import optimize, stats
        except ModuleNotFoundError as exc:
            raise ModuleNotFoundError(
                "predictive.py requires numpy, pandas and scipy."
            ) from exc

        _DEPS = (np, pd, optimize, stats)

    return _DEPS


class TailRisk(NamedTuple):
    var: float
    expected_shortfall: float


def _validate_alpha(alpha: float) -> None:
    if not 0.0 < alpha < 1.0:
        raise ValueError("alpha must lie strictly between 0 and 1.")


def _validate_mixture(weights, means, sigmas):
    np, _, _, _ = _require_dependencies()

    w = np.asarray(weights, dtype="float64").ravel()
    mu = np.asarray(means, dtype="float64").ravel()
    sd = np.asarray(sigmas, dtype="float64").ravel()

    if not (w.size == mu.size == sd.size):
        raise ValueError(
            f"weights, means and sigmas must have equal length "
            f"({w.size}, {mu.size}, {sd.size})."
        )
    if w.size == 0:
        raise ValueError("A mixture needs at least one component.")
    if not (np.isfinite(w).all() and np.isfinite(mu).all() and np.isfinite(sd).all()):
        raise ValueError("Mixture parameters must be finite.")
    if (w < 0.0).any():
        raise ValueError("Mixture weights must be non-negative.")
    if not np.isclose(w.sum(), 1.0, atol=1e-10):
        raise ValueError(f"Mixture weights must sum to 1 (got {w.sum()!r}).")
    if (sd <= 0.0).any():
        raise ValueError("sigmas must be strictly positive standard deviations.")

    return w, mu, sd


def transition_matrix(results) -> "np.ndarray":
    """Row-stochastic transition matrix: P[i, j] = Pr(s_next = j | s_now = i).

    statsmodels stores `regime_transition[j, i, t]` -- columns summing to one,
    verified empirically at k=2 and k=3 against the `p[i->j]` named parameters.
    The transpose here is the only place that convention is handled.
    """
    np, _, _, _ = _require_dependencies()

    stored = np.asarray(results.regime_transition, dtype="float64")
    if stored.ndim != 3:
        raise ValueError(f"Expected a 3-d regime_transition, got shape {stored.shape}.")
    if stored.shape[-1] != 1:
        raise ValueError(
            "Time-varying transition probabilities are not supported "
            f"(regime_transition has {stored.shape[-1]} time steps)."
        )

    transition = stored[:, :, 0].T
    row_sums = transition.sum(axis=1)
    if not np.allclose(row_sums, 1.0, atol=1e-8):
        raise ValueError(f"Transition rows do not sum to 1 after transpose: {row_sums!r}.")

    return transition


def regime_parameters(model, results) -> tuple["np.ndarray", "np.ndarray"]:
    """Per-regime (means, sigmas). sigmas are standard deviations, not variances."""
    np, _, _, _ = _require_dependencies()

    params = np.asarray(results.params, dtype="float64")
    names = model.param_names
    k = model.k_regimes

    means = np.array([params[names.index(f"const[{j}]")] for j in range(k)])
    variances = np.array([params[names.index(f"sigma2[{j}]")] for j in range(k)])

    if (variances <= 0.0).any():
        raise ValueError(f"Fitted regime variances must be positive (got {variances!r}).")

    return means, np.sqrt(variances)


def state_prediction(filtered, transition):
    """One-step-ahead state probabilities from filtered probabilities.

    Row t of the result is the distribution of s_{t+1} given data through t --
    the Hamilton filter's own prediction step. Accepts a single (k,) vector or a
    (T, k) array.
    """
    np, _, _, _ = _require_dependencies()

    xi = np.asarray(filtered, dtype="float64")
    P = np.asarray(transition, dtype="float64")

    if P.ndim != 2 or P.shape[0] != P.shape[1]:
        raise ValueError(f"transition must be square, got shape {P.shape}.")
    if xi.shape[-1] != P.shape[0]:
        raise ValueError(
            f"filtered has {xi.shape[-1]} regimes but transition has {P.shape[0]}."
        )

    # w[j] = sum_i P[i, j] * xi[i], i.e. xi @ P with P row = from. Works
    # unchanged for a (T, k) block because the contraction is on the last axis.
    predicted = xi @ P

    # Renormalize rather than trust the product: filtered rows can sit an ULP off
    # 1.0, and every downstream quantile depends on the weights summing exactly.
    totals = predicted.sum(axis=-1, keepdims=True)
    return predicted / totals


def mixture_cdf(q: float, weights, means, sigmas) -> float:
    """Pr(r <= q) under the normal mixture."""
    np, _, _, stats = _require_dependencies()
    w, mu, sd = _validate_mixture(weights, means, sigmas)
    return float(np.sum(w * stats.norm.cdf((float(q) - mu) / sd)))


def mixture_var(weights, means, sigmas, alpha: float = DEFAULT_ALPHA) -> float:
    """Lower-tail VaR: the q with Pr(r <= q) = alpha. A return level."""
    np, _, optimize, stats = _require_dependencies()
    _validate_alpha(alpha)
    w, mu, sd = _validate_mixture(weights, means, sigmas)

    if w.size == 1:
        return float(mu[0] + sd[0] * stats.norm.ppf(alpha))

    # Bracket: the mixture quantile lies between the smallest and largest
    # component quantiles. At q = min_j Q_j(alpha) every component CDF is <=
    # alpha, so the mixture CDF is <= alpha; symmetrically at the max. Holds for
    # any weights because they sum to one. Far tighter and safer than a
    # hardcoded interval, and it degenerates correctly to a single component.
    component_quantiles = mu + sd * stats.norm.ppf(alpha)
    lo = float(component_quantiles.min())
    hi = float(component_quantiles.max())

    # The mixture CDF is strictly increasing, so padding guarantees the strict
    # sign change brentq requires even when lo == hi in floating point.
    pad = 1e-12 + 1e-6 * float(sd.max())
    lo -= pad
    hi += pad

    def excess(q: float) -> float:
        return float(np.sum(w * stats.norm.cdf((q - mu) / sd))) - alpha

    return float(optimize.brentq(excess, lo, hi, xtol=1e-15, rtol=8.9e-16, maxiter=200))


def mixture_expected_shortfall(
    weights, means, sigmas, alpha: float = DEFAULT_ALPHA, var: float | None = None
) -> float:
    """E[r | r <= VaR_alpha] under the normal mixture, in closed form.

    From the truncated-normal first moment E_j[r * 1{r <= q}] = mu_j*Phi(z_j) -
    sigma_j*phi(z_j) with z_j = (q - mu_j)/sigma_j, summed over components and
    divided by alpha = Pr(r <= q). No simulation is needed at one step.
    """
    np, _, _, stats = _require_dependencies()
    _validate_alpha(alpha)
    w, mu, sd = _validate_mixture(weights, means, sigmas)

    q = mixture_var(w, mu, sd, alpha) if var is None else float(var)
    z = (q - mu) / sd
    partial = mu * stats.norm.cdf(z) - sd * stats.norm.pdf(z)
    return float(np.sum(w * partial) / alpha)


def mixture_tail_risk(weights, means, sigmas, alpha: float = DEFAULT_ALPHA) -> TailRisk:
    """VaR and ES together, solving the quantile once."""
    var = mixture_var(weights, means, sigmas, alpha)
    return TailRisk(
        var=var,
        expected_shortfall=mixture_expected_shortfall(
            weights, means, sigmas, alpha, var=var
        ),
    )


def predictive_tail_risk(model, results, alpha: float = DEFAULT_ALPHA) -> "pd.DataFrame":
    """VaR and ES for every period, indexed by the period being forecast.

    Row t holds the forecast for period t made with data through t-1, so it
    aligns directly against the realized return at t with no shift. That is
    deliberate: an off-by-one here is a look-ahead bug that no test of shape or
    range would catch. The first period has no forecast and is absent.

    NOTE: the parameters come from a single fit. If that fit saw the whole
    sample these numbers carry parameter look-ahead (leak register #2) and are
    not reportable -- use the walk-forward path. See
    docs/POINT-IN-TIME-DISCIPLINE.md.
    """
    np, pd, _, _ = _require_dependencies()
    _validate_alpha(alpha)

    means, sigmas = regime_parameters(model, results)
    transition = transition_matrix(results)

    filtered = np.asarray(results.filtered_marginal_probabilities, dtype="float64")
    if filtered.ndim != 2 or filtered.shape[1] != model.k_regimes:
        raise ValueError(
            f"Expected filtered probabilities of shape (nobs, {model.k_regimes}), "
            f"got {filtered.shape}."
        )

    predicted = state_prediction(filtered, transition)

    index = pd.Index(model.data.row_labels)
    # predicted[t] forecasts t+1, so drop the last (its target is unobserved)
    # and label the rest with the target period.
    rows = [mixture_tail_risk(w, means, sigmas, alpha) for w in predicted[:-1]]

    return pd.DataFrame(
        {
            "var": [r.var for r in rows],
            "expected_shortfall": [r.expected_shortfall for r in rows],
        },
        index=index[1:],
    )
