"""Regression checks for the core-risk-overlay pipeline.

Plain-script smoke test (no pytest) meant to be run after any change to
anything under src/. Uses synthetic data so it has no network dependency and is
fully deterministic. Exits non-zero on failure.

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
import markov_switching as ms
import predictive as pr

# A plain sanity bound on the fixture's calm periods, NOT a tier threshold.
# Tiering is out of scope -- see docs/RESEARCH-PROTOCOL.md section 9.
CALM_PROBABILITY_MAX = 0.20

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


def check_density_calibration() -> None:
    """Known-answer battery for PIT / Berkowitz (RESEARCH-PROTOCOL section 10, step 2).

    Every case is simulated with a KNOWN defect and a known correct answer. The
    protocol's requirement is two-sided and both halves are enforced here:
    correctly-specified input must FAIL TO REJECT, and each deliberately
    miscalibrated input must REJECT. A test that never rejects is worse than no
    test, and a test that always rejects is equally useless.
    """
    from scipy import stats

    rng = np.random.default_rng(11)
    n = 5000

    # --- the null: correctly specified, both forms must stay quiet ------------
    correct = stats.norm.cdf(rng.normal(0.0, 1.0, n))
    clean = ev.berkowitz_test(correct)
    clean_tail = ev.censored_berkowitz_test(correct, 0.05)
    check("evaluation: Berkowitz does not reject a correctly-specified density",
          clean.p_value > 0.05)
    check("evaluation: censored Berkowitz does not reject it either",
          clean_tail.p_value > 0.05)
    check("evaluation: Berkowitz recovers mu=0, rho=0, sigma2=1 under the null",
          abs(clean.mu) < 0.05 and abs(clean.rho) < 0.05 and abs(clean.sigma2 - 1.0) < 0.05)

    # --- understated risk: the failure that matters most for an overlay -------
    understated = ev.berkowitz_test(stats.norm.cdf(rng.normal(0.0, 1.5, n)))
    check("evaluation: Berkowitz rejects a density that understates risk",
          understated.p_value < 1e-6)
    check("evaluation: sigma2 diagnoses the understatement as 1.5^2",
          abs(understated.sigma2 - 2.25) < 0.15)

    # --- location bias -------------------------------------------------------
    biased = ev.berkowitz_test(stats.norm.cdf(rng.normal(0.5, 1.0, n)))
    check("evaluation: Berkowitz rejects a location-biased density",
          biased.p_value < 1e-6)
    check("evaluation: mu diagnoses the location bias as +0.5",
          abs(biased.mu - 0.5) < 0.05)

    # --- serial dependence in the level --------------------------------------
    # Unit unconditional variance, so the ONLY defect is dependence. Note the
    # fitted sigma2 is the innovation variance 1 - rho^2 = 0.64, not 1: the
    # "sigma2 > 1 means understated risk" reading only holds at rho = 0.
    rho_true = 0.6
    innovations = rng.normal(0.0, np.sqrt(1.0 - rho_true**2), n)
    z = np.empty(n)
    z[0] = innovations[0]
    for t in range(1, n):
        z[t] = rho_true * z[t - 1] + innovations[t]
    dependent = ev.berkowitz_test(stats.norm.cdf(z))
    check("evaluation: Berkowitz rejects serially dependent PIT values",
          dependent.p_value < 1e-6)
    check("evaluation: rho recovers the true AR(1) coefficient 0.6",
          abs(dependent.rho - rho_true) < 0.05)

    # --- the case the censored version exists for ----------------------------
    # Standardized t(4): unit variance, zero mean, no dependence -- correct in
    # the body and wrong only in the tail. The full test cannot see it.
    fat_tailed = stats.norm.cdf(rng.standard_t(4, n) / np.sqrt(4.0 / 2.0))
    body_ok = ev.berkowitz_test(fat_tailed)
    tail_bad = ev.censored_berkowitz_test(fat_tailed, 0.05)
    check(
        "evaluation: full Berkowitz MISSES a body-correct, tail-wrong density "
        f"(p={body_ok.p_value:.2f})",
        body_ok.p_value > 0.05,
    )
    check(
        "evaluation: censored Berkowitz catches it "
        f"(p={tail_bad.p_value:.1e}, sigma2={tail_bad.sigma2:.2f})",
        tail_bad.p_value < 1e-6 and tail_bad.sigma2 > 1.0,
    )
    check("evaluation: censored Berkowitz is chi2(2), rho dropped (amended 2026-08-13)",
          tail_bad.df == 2 and clean.df == 3)

    # --- LR is a likelihood ratio, so it cannot be negative -------------------
    check(
        "evaluation: LR >= 0 in every case (optimizer never loses to the null)",
        all(r.lr >= 0.0 for r in (clean, clean_tail, understated, biased,
                                  dependent, body_ok, tail_bad)),
    )

    # --- PIT diagnostics: the companion the primary test needs ---------------
    uniform_diagnostics = ev.pit_diagnostics(np.random.default_rng(3).random(4000))
    check("evaluation: PIT histogram does not reject genuinely uniform values",
          uniform_diagnostics.uniformity_p > 0.05)
    check("evaluation: Ljung-Box on (u-0.5)^2 stays quiet on iid values",
          uniform_diagnostics.ljung_box_squared_p > 0.05)
    check("evaluation: PIT histogram bins account for every observation",
          sum(uniform_diagnostics.bin_counts) == uniform_diagnostics.n)

    # Berkowitz's documented blind spot, measured rather than asserted:
    # persistent volatility scored at constant volatility. rho tests the LEVEL
    # of z, so the full test passes; the dynamics are only visible in z^2.
    vol_rng = np.random.default_rng(3)
    vol_rng.random(4000)                       # keep the stream aligned with above
    log_variance = np.zeros(4000)
    for t in range(1, 4000):
        log_variance[t] = 0.97 * log_variance[t - 1] + vol_rng.normal(0.0, 0.25)
    heteroskedastic = vol_rng.normal(0.0, 1.0, 4000) * np.exp(0.5 * log_variance)
    vol_pit = stats.norm.cdf(heteroskedastic / heteroskedastic.std())
    vol_diagnostics = ev.pit_diagnostics(vol_pit)
    check(
        "evaluation: squared-PIT Ljung-Box catches unabsorbed volatility dynamics",
        vol_diagnostics.ljung_box_squared_p < 1e-6,
    )
    check(
        "evaluation: ... which the level ACF does not (why both are reported)",
        vol_diagnostics.ljung_box_level_p > vol_diagnostics.ljung_box_squared_p * 1e6,
    )

    # --- clipping is counted, never silent -----------------------------------
    with_impossible = np.concatenate([[0.0, 1.0], rng.random(200)])
    _, clipped = ev.pit_to_normal(with_impossible)
    check("evaluation: PIT clipping counts the model's impossible observations",
          clipped == 2)
    check("evaluation: the clip count reaches the Berkowitz result",
          ev.berkowitz_test(with_impossible).n_clipped == 2)

    # --- boundary validation -------------------------------------------------
    for bad, label in [
        (lambda: ev.berkowitz_test(np.full(50, -0.1)), "PIT values below 0"),
        (lambda: ev.berkowitz_test(np.full(50, 1.2)), "PIT values above 1"),
        (lambda: ev.berkowitz_test(rng.random(5)), "fewer than 10 observations"),
        (lambda: ev.censored_berkowitz_test(0.1 + 0.9 * rng.random(300), 0.01),
         "too few observations below the cutoff"),
        (lambda: ev.pit_diagnostics(rng.random(100), lags=100), "lags >= n"),
    ]:
        check(f"evaluation: rejects {label}", _raises(bad))


def check_markov_switching_output() -> None:
    returns = make_synthetic_returns()
    event_index = returns.index[100:110]

    probabilities = ms.estimate_high_variance_probability(returns)

    check(
        "markov_switching: output length matches input length",
        len(probabilities) == len(returns),
    )
    check(
        "markov_switching: output keeps the input DatetimeIndex",
        probabilities.index.equals(returns.index),
    )
    check(
        "markov_switching: output is bounded in [0, 1]",
        bool(((probabilities >= 0.0) & (probabilities <= 1.0)).all()),
    )
    check(
        "markov_switching: synthetic event weeks get high probability",
        probabilities.loc[event_index].mean() > 0.8,
    )
    check(
        "markov_switching: synthetic calm weeks get low probability",
        probabilities.drop(event_index).mean() < CALM_PROBABILITY_MAX,
    )
    check(
        "markov_switching: identical input gives identical output (reproducible)",
        probabilities.equals(ms.estimate_high_variance_probability(returns)),
    )


def check_markov_switching_internals() -> None:
    returns = make_synthetic_returns()
    model, results, high_variance_regime = ms.fit_markov_switching(returns)
    params = dict(zip(model.param_names, np.asarray(results.params, dtype=float)))

    check(
        "markov_switching: mean switches as well as variance (guards sign-blindness)",
        "const[0]" in params and "const[1]" in params,
    )
    check(
        "markov_switching: no parameter is pinned (6 free parameters)",
        model.k_params == 6,
    )
    check(
        "markov_switching: identified regime is the higher-variance regime",
        params[f"sigma2[{high_variance_regime}]"]
        == max(params["sigma2[0]"], params["sigma2[1]"]),
    )

    # The pre-2026-08-12 spec pinned p[0->0] inside transform_params, which
    # corrupted the complex-step gradient: BFGS reported convergence with an
    # exactly-zero gradient and an untouched identity Hessian entry (1.0) in
    # the pinned direction. Both are impossible if every coordinate was
    # genuinely explored.
    gradient = np.asarray(results.mle_retvals["gopt"], dtype=float)
    hessian_diagonal = np.diag(np.asarray(results.mle_retvals["Hinv"], dtype=float))
    check(
        "markov_switching: gradient is small in every coordinate at the optimum",
        bool(np.all(np.abs(gradient) < 1e-3)),
    )
    check(
        "markov_switching: no coordinate left at the BFGS identity init (never explored)",
        bool(np.all(hessian_diagonal != 1.0)),
    )

    # The single most important guard in this file. Returning smoothed
    # probabilities puts look-ahead bias straight into the trading signal --
    # the Kim smoother conditions every week on the whole sample, including the
    # future. See docs/POINT-IN-TIME-DISCIPLINE.md.
    returned = ms.estimate_high_variance_probability(returns)
    filtered = np.asarray(results.filtered_marginal_probabilities)[:, high_variance_regime]
    smoothed = np.asarray(results.smoothed_marginal_probabilities)[:, high_variance_regime]
    check(
        "markov_switching: returns FILTERED probabilities",
        bool(np.allclose(returned.to_numpy(), filtered)),
    )
    check(
        "markov_switching: does NOT return smoothed probabilities (look-ahead guard)",
        not bool(np.allclose(returned.to_numpy(), smoothed)),
    )


def check_short_sample_warning() -> None:
    # The fixture is deliberately 150 weeks, well under the reliable minimum, so
    # the warning must fire here. Silently fitting a short sample is what
    # produced degenerate parameters and flipping regime labels in walkforward.py.
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        ms._prepare_log_returns(make_synthetic_returns())
    check(
        "markov_switching: warns when fitting below the reliable minimum",
        any("RELIABLE_MIN_OBSERVATIONS" in str(w.message) for w in caught),
    )


def check_markov_switching_validation() -> None:
    short_returns = make_synthetic_returns().iloc[:5]
    for bad_input, label in [
        (pd.Series(dtype="float64"), "empty series"),
        (short_returns, "fewer than 10 observations"),
        (pd.Series([0.01, np.inf] * 10), "non-finite values"),
    ]:
        try:
            ms.estimate_high_variance_probability(bad_input)
            check(f"markov_switching: rejects {label}", False)
        except ValueError:
            check(f"markov_switching: rejects {label}", True)


def check_predictive() -> None:
    from scipy import stats

    alpha = 0.05
    weights = np.array([0.85, 0.15])
    means = np.array([0.0015, -0.004])
    sigmas = np.array([0.008, 0.026])

    # 1. A degenerate mixture must reproduce the closed-form normal exactly.
    #    This is the strongest available check: it ties the mixture solver to
    #    code that was verified independently.
    for w in ([1.0, 0.0], [0.0, 1.0]):
        active = int(np.argmax(w))
        var = pr.mixture_var(w, means, sigmas, alpha)
        es = pr.mixture_expected_shortfall(w, means, sigmas, alpha)
        check(
            f"predictive: degenerate mixture w={w} matches evaluation.normal_var",
            bool(np.isclose(var, ev.normal_var(means[active], sigmas[active], alpha),
                            rtol=0, atol=1e-12)),
        )
        check(
            f"predictive: degenerate mixture w={w} matches normal_expected_shortfall",
            bool(np.isclose(es, ev.normal_expected_shortfall(means[active], sigmas[active],
                                                             alpha), rtol=0, atol=1e-12)),
        )

    # 2. The solved quantile must actually be the alpha-quantile.
    var = pr.mixture_var(weights, means, sigmas, alpha)
    check(
        "predictive: mixture CDF at the solved VaR returns alpha",
        abs(pr.mixture_cdf(var, weights, means, sigmas) - alpha) < 1e-10,
    )

    # 3. Monotonicity, and ES strictly worse than VaR.
    quantiles = [pr.mixture_var(weights, means, sigmas, a) for a in (0.01, 0.05, 0.10, 0.25)]
    check(
        "predictive: VaR is increasing in alpha",
        all(a < b for a, b in zip(quantiles, quantiles[1:])),
    )
    shortfalls = [pr.mixture_expected_shortfall(weights, means, sigmas, a)
                  for a in (0.01, 0.05, 0.10, 0.25)]
    check(
        "predictive: ES is increasing in alpha",
        all(a < b for a, b in zip(shortfalls, shortfalls[1:])),
    )
    check(
        "predictive: ES is strictly worse than VaR at every alpha",
        all(e < v for e, v in zip(shortfalls, quantiles)),
    )

    # 4. Monte Carlo: draws from the mixture must breach at rate alpha, and the
    #    mean of the breaches must equal the closed-form ES.
    rng = np.random.default_rng(20260812)
    n = 400_000
    component = rng.random(n) < weights[0]
    draws = np.where(component,
                     rng.normal(means[0], sigmas[0], n),
                     rng.normal(means[1], sigmas[1], n))
    breach_rate = float((draws < var).mean())
    check(
        f"predictive: simulated breach rate {breach_rate:.4f} matches alpha={alpha}",
        abs(breach_rate - alpha) < 4.0 * np.sqrt(alpha * (1 - alpha) / n),
    )
    es = pr.mixture_expected_shortfall(weights, means, sigmas, alpha, var=var)
    check(
        "predictive: closed-form ES matches the mean of simulated breaches",
        abs(float(draws[draws < var].mean()) - es) < 5e-4,
    )

    # 5. The moment-matched normal is WRONG, not merely imprecise. Guarding the
    #    magnitude keeps anyone from "simplifying" the solver back to it.
    mean = float(np.sum(weights * means))
    total_var = float(np.sum(weights * sigmas**2) + np.sum(weights * (means - mean) ** 2))
    naive = mean + np.sqrt(total_var) * stats.norm.ppf(alpha)
    check(
        "predictive: moment-matched normal errs by >5% of the VaR level (documented trap)",
        abs(naive - var) / abs(var) > 0.05,
    )

    # 6. State prediction orientation, by hand. A transposed transition matrix
    #    inverts the model silently and nothing else here would catch it.
    transition = np.array([[0.90, 0.10],
                           [0.40, 0.60]])
    predicted = pr.state_prediction(np.array([0.7, 0.3]), transition)
    check(
        "predictive: state_prediction matches the hand-computed forward step",
        bool(np.allclose(predicted, [0.7 * 0.90 + 0.3 * 0.40,
                                     0.7 * 0.10 + 0.3 * 0.60])),
    )
    check(
        "predictive: state_prediction rejects a transposed/ragged transition",
        _raises(lambda: pr.state_prediction(np.array([0.7, 0.3]), np.ones((3, 3)))),
    )

    # 7. statsmodels orientation, against the model rather than against memory:
    #    the row-stochastic matrix must agree with the p[i->j] named parameters.
    returns = make_synthetic_returns()
    model, results, _ = ms.fit_markov_switching(returns)
    P = pr.transition_matrix(results)
    params = dict(zip(model.param_names, np.asarray(results.params, dtype=float)))
    check(
        "predictive: transition_matrix agrees with the p[i->j] parameters",
        bool(np.allclose([[params["p[0->0]"], 1 - params["p[0->0]"]],
                          [params["p[1->0]"], 1 - params["p[1->0]"]]], P)),
    )
    check(
        "predictive: transition rows sum to 1 (row = from)",
        bool(np.allclose(P.sum(axis=1), 1.0)),
    )

    # 8. The series path must align to the period being FORECAST, not the period
    #    the forecast was made in. An off-by-one here is look-ahead bias.
    frame = pr.predictive_tail_risk(model, results, alpha)
    check(
        "predictive: series is indexed by the forecast target, one shorter than input",
        len(frame) == len(returns) - 1 and frame.index.equals(returns.index[1:]),
    )
    check(
        "predictive: series VaR reproduces the standalone mixture VaR at t=0",
        bool(np.isclose(
            frame["var"].iloc[0],
            pr.mixture_var(
                pr.state_prediction(
                    np.asarray(results.filtered_marginal_probabilities, dtype=float)[0], P),
                *pr.regime_parameters(model, results), alpha),
        )),
    )
    check(
        "predictive: no NaN in the series output",
        bool(frame.notna().all().all()),
    )

    # 9. Boundary validation.
    for bad, label in [
        (lambda: pr.mixture_var([0.5, 0.4], means, sigmas, alpha), "weights not summing to 1"),
        (lambda: pr.mixture_var([1.5, -0.5], means, sigmas, alpha), "negative weights"),
        (lambda: pr.mixture_var(weights, means, [0.01, 0.0], alpha), "a zero sigma"),
        (lambda: pr.mixture_var(weights, means, sigmas, 0.0), "alpha = 0"),
        (lambda: pr.mixture_var(weights, means[:1], sigmas, alpha), "mismatched lengths"),
    ]:
        check(f"predictive: rejects {label}", _raises(bad))


def _raises(call) -> bool:
    try:
        call()
    except (ValueError, ZeroDivisionError):
        return True
    return False


def report_known_limitation() -> None:
    # Not a pass/fail assertion: a recorded, measured limitation. The regime is
    # identified by variance, so a high-volatility RALLY is labelled high-variance
    # even with a switching mean. A ratio near 1.0 means fully sign-blind. This
    # is why the regime is not named directionally -- see markov_switching.py.
    print()
    print("--- measured limitation: sign-blindness (synthetic fixture) ---")
    probabilities = {}
    for label, event_mean in [("crash  ", -0.02), ("melt-up", +0.02)]:
        series = make_synthetic_returns(jump_mean=event_mean)
        probabilities[label] = ms.estimate_high_variance_probability(series).iloc[100:110].mean()
        print(
            f"  {label}: event-window mean return {series.iloc[100:110].mean():+.4f}"
            f"   filtered P {probabilities[label]:.4f}"
        )
    print(f"  up/down probability ratio: {probabilities['melt-up'] / probabilities['crash  ']:.4f}")


def main() -> None:
    check_data_loader()
    check_vix_alignment()
    check_evaluation()
    check_density_calibration()
    check_short_sample_warning()
    # Every remaining check fits the 150-week fixture, so the short-sample
    # warning is expected throughout and would only be noise.
    warnings.filterwarnings("ignore", message=".*RELIABLE_MIN_OBSERVATIONS.*")
    check_markov_switching_output()
    check_markov_switching_internals()
    check_markov_switching_validation()
    check_predictive()
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
