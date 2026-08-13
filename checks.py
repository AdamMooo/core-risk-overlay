"""Regression checks for the core-risk-overlay pipeline.

Plain-script smoke test (no pytest) meant to be run after any change to
src/data_loader.py or src/jump_model.py. Uses synthetic data so it has no
network dependency and is fully deterministic. Exits non-zero on failure.

Several checks here are guards against specific defects found in the
2026-08-12 audit -- see core-risk-overlay.md. They are cheap and they encode
mistakes that were already made once.
"""
from __future__ import annotations

import sys
import warnings
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

import numpy as np
import pandas as pd

import data_loader as dl
import evaluation as ev
import jump_model as jm

CALM_TIER_UPPER = 0.20
HYSTERIA_TIER_LOWER = 0.60

FAILURES: list[str] = []


def check(description: str, condition: bool) -> None:
    status = "PASS" if condition else "FAIL"
    print(f"[{status}] {description}")
    if not condition:
        FAILURES.append(description)


def make_synthetic_returns(jump_mean: float = -0.02) -> pd.Series:
    # 100 calm weeks, 10 sharp jump weeks, 40 calm weeks: a known regime
    # pattern the fit should recover, at a realistic calm:jump ratio.
    rng = np.random.default_rng(seed=42)
    calm_a = rng.normal(loc=0.001, scale=0.01, size=100)
    jump = rng.normal(loc=jump_mean, scale=0.06, size=10)
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


def check_vix_alignment() -> None:
    index = pd.date_range("2024-01-01", periods=6, freq="W-MON")
    vix = pd.Series([13.0, 14.5, 22.0, 31.5, 18.0, 15.0], index=index)
    returns = pd.Series(np.linspace(-0.02, 0.02, 6), index=index)

    aligned = dl.align_vix_to_returns(vix, returns)
    check("data_loader: VIX aligns on an exact index match", aligned.index.equals(returns.index))
    check("data_loader: VIX alignment preserves values", bool(np.allclose(aligned, vix)))

    # The whole point of the exact join: a missing week must surface, never be
    # papered over with a stale carried-forward quote.
    for label, gap in [
        ("a missing week", vix.drop(index[2])),
        ("a shifted index", pd.Series(vix.to_numpy(), index=index + pd.Timedelta(days=1))),
    ]:
        try:
            dl.align_vix_to_returns(gap, returns)
            check(f"data_loader: VIX alignment rejects {label}", False)
        except ValueError:
            check(f"data_loader: VIX alignment rejects {label}", True)

    try:
        dl.align_vix_to_returns(vix.copy().mask(vix > 30, -1.0), returns)
        check("data_loader: VIX alignment rejects non-positive values", False)
    except ValueError:
        check("data_loader: VIX alignment rejects non-positive values", True)

    log_vix = dl.to_log_vix(aligned)
    check(
        "data_loader: to_log_vix matches np.log",
        bool(np.allclose(log_vix, np.log(vix))),
    )
    try:
        dl.to_log_vix(pd.Series([10.0, 0.0], index=index[:2]))
        check("data_loader: to_log_vix rejects non-positive values", False)
    except ValueError:
        check("data_loader: to_log_vix rejects non-positive values", True)


def check_evaluation() -> None:
    from scipy import stats

    check(
        "evaluation: normal VaR equals the alpha-quantile",
        np.isclose(ev.normal_var(0.0, 1.0, 0.05), stats.norm.ppf(0.05)),
    )
    check(
        "evaluation: expected shortfall is strictly worse than VaR",
        ev.normal_expected_shortfall(0.0, 1.0, 0.05) < ev.normal_var(0.0, 1.0, 0.05),
    )

    n = 2000
    on_target = np.zeros(n, dtype=bool)
    on_target[np.arange(0, n, 20)] = True          # exactly 5%, evenly spread
    clustered = np.zeros(n, dtype=bool)
    for start in range(0, n, 200):                 # exactly 5%, in blocks of 10
        clustered[start:start + 10] = True

    clean = ev.coverage_tests(on_target, 0.05)
    bunched = ev.coverage_tests(clustered, 0.05)

    check("evaluation: Kupiec does not reject a correctly-sized VaR", clean.p_uc > 0.99)
    check(
        "evaluation: Kupiec rejects a 3x oversized exceedance rate",
        ev.coverage_tests(np.arange(n) % 6 == 0, 0.05).p_uc < 1e-10,
    )
    # Genuinely iid, not the evenly-spaced series above: a breach at exactly
    # every 20th observation is perfectly regular and therefore NOT independent,
    # and Christoffersen rejects it. The test detects excessive regularity as
    # well as clustering.
    iid_hits = np.random.default_rng(7).random(n) < 0.05
    check(
        "evaluation: Christoffersen does not reject independent exceedances",
        ev.coverage_tests(iid_hits, 0.05).p_ind > 0.05,
    )
    # The discriminating case, and the reason README 1b needs no benchmark: both
    # series breach at exactly 5%, so coverage alone cannot tell them apart.
    check(
        "evaluation: Christoffersen rejects clustered exceedances at the same rate",
        bunched.p_ind < 1e-6 and np.isclose(bunched.observed_rate, clean.observed_rate),
    )
    check(
        "evaluation: conditional coverage is the sum of its two parts",
        np.isclose(bunched.lr_cc, bunched.lr_uc + bunched.lr_ind),
    )

    # realized_forward is an evaluation target and must never see r_t itself.
    forward = ev.realized_forward(pd.Series(np.arange(1, 11, dtype=float)), 3, "sum")
    check("evaluation: forward window covers t+1..t+h, excluding t", np.isclose(forward.iloc[0], 9.0))
    check("evaluation: forward window has no value where the future is unknown",
          bool(forward.iloc[-3:].isna().all()))

    rng = np.random.default_rng(7)
    m = 1500
    implied = pd.Series(rng.normal(0.2, 0.05, m))
    informative = pd.Series(rng.normal(0.2, 0.05, m))
    realized = 0.01 + 0.60 * implied + 0.30 * informative + rng.normal(0, 0.01, m)
    fitted = ev.encompassing_regression(realized, implied, informative, horizon=4)
    check(
        "evaluation: encompassing regression recovers known coefficients",
        abs(fitted.beta_implied - 0.60) < 0.05 and abs(fitted.gamma_model - 0.30) < 0.05,
    )
    check("evaluation: Newey-West lags default to horizon - 1", fitted.hac_lags == 3)
    uninformative = pd.Series(rng.normal(0.2, 0.05, m))
    null_fit = ev.encompassing_regression(
        0.01 + 0.60 * implied + rng.normal(0, 0.01, m), implied, uninformative, horizon=4
    )
    check(
        "evaluation: uninformative X gives an insignificant coefficient",
        null_fit.p_model > 0.05,
    )


def check_jump_model_output() -> None:
    returns = make_synthetic_returns()
    jump_index = returns.index[100:110]

    probabilities = jm.estimate_jump_regimes(returns)

    check(
        "jump_model: output length matches input length",
        len(probabilities) == len(returns),
    )
    check(
        "jump_model: output keeps the input DatetimeIndex",
        probabilities.index.equals(returns.index),
    )
    check(
        "jump_model: output is bounded in [0, 1]",
        bool(((probabilities >= 0.0) & (probabilities <= 1.0)).all()),
    )
    check(
        "jump_model: synthetic jump weeks get high jump probability",
        probabilities.loc[jump_index].mean() > 0.8,
    )
    check(
        "jump_model: synthetic calm weeks get low jump probability",
        probabilities.drop(jump_index).mean() < CALM_TIER_UPPER,
    )
    check(
        "jump_model: identical input gives identical output (reproducible)",
        probabilities.equals(jm.estimate_jump_regimes(returns)),
    )


def check_jump_model_internals() -> None:
    returns = make_synthetic_returns()
    model, results, jump_regime = jm.fit_jump_model(returns)
    params = dict(zip(model.param_names, np.asarray(results.params, dtype=float)))

    check(
        "jump_model: mean switches as well as variance (guards sign-blindness)",
        "const[0]" in params and "const[1]" in params,
    )
    check(
        "jump_model: no parameter is pinned (6 free parameters)",
        model.k_params == 6,
    )
    check(
        "jump_model: jump regime is the higher-variance regime",
        params[f"sigma2[{jump_regime}]"] == max(params["sigma2[0]"], params["sigma2[1]"]),
    )

    # The pre-2026-08-12 spec pinned p[0->0] inside transform_params, which
    # corrupted the complex-step gradient: BFGS reported convergence with an
    # exactly-zero gradient and an untouched identity Hessian entry (1.0) in
    # the pinned direction. Both are impossible if every coordinate was
    # genuinely explored.
    gradient = np.asarray(results.mle_retvals["gopt"], dtype=float)
    hessian_diagonal = np.diag(np.asarray(results.mle_retvals["Hinv"], dtype=float))
    check(
        "jump_model: gradient is small in every coordinate at the optimum",
        bool(np.all(np.abs(gradient) < 1e-3)),
    )
    check(
        "jump_model: no coordinate left at the BFGS identity init (never explored)",
        bool(np.all(hessian_diagonal != 1.0)),
    )

    # The single most important guard in this file. Returning smoothed
    # probabilities puts look-ahead bias straight into the trading signal --
    # the Kim smoother conditions every week on the whole sample, including the
    # future. See docs/POINT-IN-TIME-DISCIPLINE.md.
    returned = jm.estimate_jump_regimes(returns)
    filtered = np.asarray(results.filtered_marginal_probabilities)[:, jump_regime]
    smoothed = np.asarray(results.smoothed_marginal_probabilities)[:, jump_regime]
    check(
        "jump_model: returns FILTERED probabilities",
        bool(np.allclose(returned.to_numpy(), filtered)),
    )
    check(
        "jump_model: does NOT return smoothed probabilities (look-ahead guard)",
        not bool(np.allclose(returned.to_numpy(), smoothed)),
    )


def check_short_sample_warning() -> None:
    # The fixture is deliberately 150 weeks, well under the reliable minimum, so
    # the warning must fire here. Silently fitting a short sample is what
    # produced degenerate parameters and flipping regime labels in walkforward.py.
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        jm._prepare_weekly_log_returns(make_synthetic_returns())
    check(
        "jump_model: warns when fitting below the reliable minimum",
        any("RELIABLE_MIN_OBSERVATIONS" in str(w.message) for w in caught),
    )


def check_jump_model_validation() -> None:
    short_returns = make_synthetic_returns().iloc[:5]
    for bad_input, label in [
        (pd.Series(dtype="float64"), "empty series"),
        (short_returns, "fewer than 10 observations"),
        (pd.Series([0.01, np.inf] * 10), "non-finite values"),
    ]:
        try:
            jm.estimate_jump_regimes(bad_input)
            check(f"jump_model: rejects {label}", False)
        except ValueError:
            check(f"jump_model: rejects {label}", True)


def report_known_limitation() -> None:
    # Not a pass/fail assertion: a recorded, measured limitation. The jump
    # regime is identified by variance, so a high-volatility RALLY is still
    # labelled a jump even with a switching mean. Real crisis regimes carry
    # negative drift, so this is expected to matter far less on real data --
    # diagnostics.py measures it there. If it survives on real data the fix
    # belongs in risk_engine.py's tier logic, not in regime identification.
    print()
    print("--- measured limitation: sign-blindness of the jump label ---")
    for label, jump_mean in [("crash ", -0.02), ("melt-up", +0.02)]:
        series = make_synthetic_returns(jump_mean=jump_mean)
        probability = jm.estimate_jump_regimes(series).iloc[100:110].mean()
        tier = "HYSTERIA" if probability > HYSTERIA_TIER_LOWER else "sub-hysteria"
        print(
            f"  {label}: event-window mean return {series.iloc[100:110].mean():+.4f}"
            f"   filtered P {probability:.4f}   tier {tier}"
        )


def main() -> None:
    check_data_loader()
    check_vix_alignment()
    check_evaluation()
    check_short_sample_warning()
    # Every remaining check fits the 150-week fixture, so the short-sample
    # warning is expected throughout and would only be noise.
    warnings.filterwarnings("ignore", message=".*RELIABLE_MIN_OBSERVATIONS.*")
    check_jump_model_output()
    check_jump_model_internals()
    check_jump_model_validation()
    report_known_limitation()

    print()
    if FAILURES:
        print(f"{len(FAILURES)} check(s) FAILED:")
        for failure in FAILURES:
            print(f"  - {failure}")
        sys.exit(1)

    print("All checks passed.")


if __name__ == "__main__":
    main()
