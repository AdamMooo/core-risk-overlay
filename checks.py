"""Regression checks for the core-risk-overlay pipeline.

Plain-script smoke test (no pytest) meant to be run after any change to
src/data_loader.py or src/jump_model.py. Uses synthetic data so it has no
network dependency and is fully deterministic. Exits non-zero on failure.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

import numpy as np
import pandas as pd

import data_loader as dl
import jump_model as jm

FAILURES: list[str] = []


def check(description: str, condition: bool) -> None:
    status = "PASS" if condition else "FAIL"
    print(f"[{status}] {description}")
    if not condition:
        FAILURES.append(description)


def make_synthetic_returns() -> pd.Series:
    # 100 calm weeks, 10 sharp jump weeks, 40 calm weeks: a known regime
    # pattern the fit should recover, at a realistic calm:jump ratio.
    rng = np.random.default_rng(seed=42)
    calm_a = rng.normal(loc=0.001, scale=0.01, size=100)
    jump = rng.normal(loc=-0.02, scale=0.06, size=10)
    calm_b = rng.normal(loc=0.001, scale=0.01, size=40)
    values = np.concatenate([calm_a, jump, calm_b])
    index = pd.date_range("2020-01-06", periods=len(values), freq="W-MON")
    return pd.Series(values, index=index, name="weekly_log_return")


def check_data_loader() -> None:
    prices = pd.Series(
        [100.0, 102.0, 101.0, 105.0],
        index=pd.date_range("2024-01-01", periods=4, freq="W-MON"),
    )
    returns = dl.compute_weekly_log_returns(prices)
    check("data_loader: log-return count is prices - 1", len(returns) == len(prices) - 1)
    check(
        "data_loader: log-return math matches np.log(p1/p0)",
        np.isclose(returns.iloc[0], np.log(102.0 / 100.0)),
    )

    for bad_prices in [pd.Series(dtype="float64"), pd.Series([1.0]), pd.Series([1.0, -1.0])]:
        try:
            dl.compute_weekly_log_returns(bad_prices)
            check(f"data_loader: rejects invalid input {bad_prices.tolist()}", False)
        except ValueError:
            check(f"data_loader: rejects invalid input {bad_prices.tolist()}", True)


def check_jump_model() -> None:
    returns = make_synthetic_returns()
    jump_index = returns.index[100:110]

    probabilities = jm.estimate_jump_regimes(returns)
    check(
        "jump_model: output length matches input length",
        len(probabilities) == len(returns),
    )
    check(
        "jump_model: synthetic jump weeks get high jump probability",
        probabilities.loc[jump_index].mean() > 0.8,
    )
    check(
        "jump_model: synthetic calm weeks get low jump probability",
        probabilities.drop(jump_index).mean() < 0.2,
    )

    repeat = jm.estimate_jump_regimes(returns)
    check("jump_model: identical input gives identical output (reproducible)", probabilities.equals(repeat))

    ConstrainedMarkovRegression = jm._constrained_markov_regression(
        jm.DEFAULT_CALM_STAY_PROBABILITY, jm.DEFAULT_JUMP_STAY_CEILING
    )
    model = ConstrainedMarkovRegression(
        returns, k_regimes=jm.N_REGIMES, trend="c", switching_trend=False, switching_variance=True
    )
    with jm._seeded_numpy_random(jm.DEFAULT_RANDOM_SEED):
        results = model.fit(search_reps=jm.DEFAULT_SEARCH_REPS, maxiter=jm.DEFAULT_MAXITER, disp=False)
    params = dict(zip(model.param_names, results.params))
    tm = model.regime_transition_matrix(results.params)

    check("jump_model: calm persistence pinned exactly at 0.98", params["p[0->0]"] == 0.98)
    check(
        "jump_model: jump persistence respects the 0.85 ceiling",
        tm[1, 1, 0] <= jm.DEFAULT_JUMP_STAY_CEILING + 1e-9,
    )
    check("jump_model: calm regime has lower variance (sigma2[0] <= sigma2[1])", params["sigma2[0]"] <= params["sigma2[1]"])

    try:
        bad_results = model.fit(search_reps=0, maxiter=1, disp=False)
        jm._check_converged(bad_results)
        check("jump_model: convergence check catches a failed fit", False)
    except RuntimeError:
        check("jump_model: convergence check catches a failed fit", True)

    for bad_value in [-0.1, 0.0, 1.0, 1.5]:
        try:
            jm.estimate_jump_regimes(returns, calm_stay_probability=bad_value)
            check(f"jump_model: rejects calm_stay_probability={bad_value}", False)
        except ValueError:
            check(f"jump_model: rejects calm_stay_probability={bad_value}", True)


def main() -> None:
    check_data_loader()
    check_jump_model()

    print()
    if FAILURES:
        print(f"{len(FAILURES)} check(s) FAILED:")
        for failure in FAILURES:
            print(f"  - {failure}")
        sys.exit(1)

    print("All checks passed.")


if __name__ == "__main__":
    main()
