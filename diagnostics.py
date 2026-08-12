"""Statistical diagnostics for the 2-regime Markov-switching volatility model.

Plain-script report (no pytest) run against REAL SPY weekly log returns. Follows
docs/MATH-REFERENCE.md sections 5, 6 and 8: corrected AIC/BIC counts, regime-
standardized residual battery, duration realism, and the 2006-2011 window test
of whether post-hoc regime relabelling is needed in practice.

The repo spec under test is src/jump_model.py's fit_jump_model(): a plain
MarkovRegression with k_regimes=2, switching_trend=True, switching_variance=True
and NO parameter restrictions. Six free parameters. Regime identification is
post-hoc (larger fitted variance == jump regime), so the jump index is
data-dependent and is never hardcoded here either -- it comes back from
fit_jump_model().

AIC/BIC are still computed here with an explicit free-parameter count rather
than read off res.aic/res.bic (MATH-REFERENCE 5.1 / 8.2). With nothing pinned,
the corrected count and statsmodels' own count should now agree for every spec;
section B verifies that rather than assuming it.

res.bse / res.pvalues / res.conf_int() / res.summary() ARE valid for this spec
and are reported. They were unusable for the previous constrained specification
because a pinned transition probability and an ordering imposed inside
transform_params left the reported surface un-fitted (MATH-REFERENCE 3.5, which
still documents the deleted constrained class and is now stale).

Downloaded data is cached to data/spy_weekly.csv so reruns need no network.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.diagnostic import acorr_ljungbox, het_arch
from statsmodels.stats.stattools import jarque_bera
from statsmodels.tsa.regime_switching.markov_regression import MarkovRegression

import data_loader as dl
import jump_model as jm

REPO_ROOT = Path(__file__).parent
CACHE_PATH = REPO_ROOT / "data" / "spy_weekly.csv"
START = "1993-01-01"
END = "2026-08-12"
WEEKS_PER_YEAR = 52
LJUNG_BOX_LAGS = (4, 8, 12, 26)
ARCH_LAGS = (4, 12)
QQ_PERCENTILES = (1.0, 2.5, 5.0, 10.0, 25.0, 50.0, 75.0, 90.0, 95.0, 97.5, 99.0)
RELABEL_WINDOW = ("2006-01-01", "2011-12-31")
REPO_SPEC_LABEL = "3. k=2 repo spec (switch mu)"
CRISIS_WINDOWS = (
    ("1998 LTCM", "1998-07-01", "1998-12-31"),
    ("2000-2002 dotcom", "2000-01-01", "2002-12-31"),
    ("2008-2009 GFC", "2008-01-01", "2009-12-31"),
    ("2010 flash crash", "2010-04-01", "2010-07-31"),
    ("2011 US downgrade", "2011-07-01", "2011-10-31"),
    ("2015-08 China", "2015-08-01", "2015-09-30"),
    ("2018-02 volmageddon", "2018-01-15", "2018-03-15"),
    ("2018-Q4", "2018-10-01", "2018-12-31"),
    ("2020-02/03 COVID", "2020-02-01", "2020-03-31"),
    ("2022 full year", "2022-01-01", "2022-12-31"),
    ("2023-03 SVB", "2023-03-01", "2023-04-15"),
)


def rule(title: str) -> None:
    print()
    print("=" * 78)
    print(title)
    print("=" * 78)


def sub(title: str) -> None:
    print()
    print(f"-- {title}")


def load_returns() -> pd.Series:
    if CACHE_PATH.exists():
        frame = pd.read_csv(CACHE_PATH, index_col=0, parse_dates=True)
        returns = frame.iloc[:, 0].astype("float64")
        returns.name = "weekly_log_return"
        print(f"data source: cache {CACHE_PATH}")
        return returns

    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    try:
        returns = dl.load_weekly_log_returns(dl.DEFAULT_TICKER, start=START, end=END)
    except Exception as first_error:
        print(f"yfinance download failed ({first_error!r}) -- retrying once.")
        returns = dl.load_weekly_log_returns(dl.DEFAULT_TICKER, start=START, end=END)
    returns.to_csv(CACHE_PATH)
    print(f"data source: yfinance download, cached to {CACHE_PATH}")
    return returns


def fit_markov(returns, k_regimes, switching_trend=False):
    model = MarkovRegression(
        returns,
        k_regimes=k_regimes,
        trend="c",
        switching_trend=switching_trend,
        switching_variance=True,
    )
    with jm._seeded_numpy_random(jm.DEFAULT_RANDOM_SEED):
        results = model.fit(
            search_reps=jm.DEFAULT_SEARCH_REPS, maxiter=jm.DEFAULT_MAXITER, disp=False
        )
    return model, results


def high_variance_index(model, results) -> int:
    params = dict(zip(model.param_names, results.params))
    return int(
        np.argmax([params[f"sigma2[{j}]"] for j in range(model.k_regimes)])
    )


def regime_means(model, results) -> np.ndarray:
    params = dict(zip(model.param_names, results.params))
    if "const" in params:
        return np.full(model.k_regimes, float(params["const"]))
    return np.array([float(params[f"const[{j}]"]) for j in range(model.k_regimes)])


def gaussian_iid_llf(returns) -> tuple[float, float, float]:
    values = np.asarray(returns, dtype=float)
    n = values.size
    mu = values.mean()
    sigma2 = ((values - mu) ** 2).mean()
    llf = -0.5 * n * (np.log(2.0 * np.pi * sigma2) + 1.0)
    return float(llf), float(mu), float(sigma2)


def corrected_information_criteria(llf: float, k_free: int, nobs: int) -> tuple[float, float]:
    return -2.0 * llf + 2.0 * k_free, -2.0 * llf + k_free * np.log(nobs)


def regime_report(model, results, label: str) -> None:
    params = dict(zip(model.param_names, results.params))
    transition = model.regime_transition_matrix(results.params)[:, :, 0]
    ergodic = np.asarray(model.initial_probabilities(results.params), dtype=float)
    k = model.k_regimes
    sigma2 = np.array([params[f"sigma2[{j}]"] for j in range(k)])
    durations = np.asarray(results.expected_durations, dtype=float)

    print(f"{label}")
    print(f"  converged           : {results.mle_retvals.get('converged')}")
    print(f"  llf                 : {results.llf:.6f}")
    print("  param vector        :")
    for name, value in params.items():
        print(f"      {name:<12s} = {value: .10g}")
    print("  transition matrix Pi (left-stochastic, Pi[i,j] = P(S_t=i | S_(t-1)=j)):")
    for row in transition:
        print("      " + "  ".join(f"{v: .8f}" for v in row))
    mu = regime_means(model, results)
    high = high_variance_index(model, results)
    print("  per-regime summary:")
    print(
        f"      {'regime':<8s}{'mu/wk':>12s}{'sigma2':>14s}{'sigma/wk':>12s}"
        f"{'ann.vol':>11s}{'p_ii':>11s}{'E[D] wks':>11s}{'ergodic':>10s}{'':>8s}"
    )
    for j in range(k):
        sigma = float(np.sqrt(sigma2[j]))
        print(
            f"      {j:<8d}{mu[j] * 100:>11.4f}%{sigma2[j]:>14.8e}{sigma * 100:>11.4f}%"
            f"{sigma * np.sqrt(WEEKS_PER_YEAR) * 100:>10.2f}%"
            f"{transition[j, j]:>11.6f}{durations[j]:>11.4f}{ergodic[j]:>10.6f}"
            f"{'  <- JUMP' if j == high else '':>8s}"
        )


def filtered_jump_probability(results, jump_regime: int) -> pd.Series:
    filtered = results.filtered_marginal_probabilities
    series = filtered.iloc[:, jump_regime].astype("float64")
    series.name = "filtered_jump_probability"
    return series


def standard_error_table(model, results, label: str) -> None:
    # Valid for this spec: nothing is pinned and the variance ordering is applied
    # after fitting, so the reported information matrix belongs to the surface
    # that was actually optimized.
    params = np.asarray(results.params, dtype=float)
    bse = np.asarray(results.bse, dtype=float)
    pvalues = np.asarray(results.pvalues, dtype=float)
    conf = np.asarray(results.conf_int(), dtype=float)
    print(f"    {label}")
    print(
        f"      {'param':<12s}{'estimate':>16s}{'std err':>14s}{'z':>10s}"
        f"{'p-value':>12s}{'ci lo':>16s}{'ci hi':>16s}"
    )
    for i, name in enumerate(model.param_names):
        z = params[i] / bse[i] if bse[i] > 0 else np.nan
        print(
            f"      {name:<12s}{params[i]:>16.8g}{bse[i]:>14.6g}{z:>10.3f}"
            f"{pvalues[i]:>12.4g}{conf[i, 0]:>16.8g}{conf[i, 1]:>16.8g}"
        )


def ljung_box_table(values, label: str) -> None:
    result = acorr_ljungbox(np.asarray(values, dtype=float), lags=list(LJUNG_BOX_LAGS))
    print(f"    {label}")
    print(f"      {'lag':>5s}{'Q stat':>14s}{'p-value':>14s}")
    for lag in LJUNG_BOX_LAGS:
        row = result.loc[lag]
        print(f"      {lag:>5d}{row['lb_stat']:>14.4f}{row['lb_pvalue']:>14.6g}")


def arch_lm_table(values, label: str) -> None:
    array = np.asarray(values, dtype=float)
    print(f"    {label}")
    print(f"      {'lags':>5s}{'LM stat':>14s}{'p-value':>14s}")
    for lag in ARCH_LAGS:
        lm_stat, lm_pvalue, _, _ = het_arch(array, nlags=lag)
        print(f"      {lag:>5d}{lm_stat:>14.4f}{lm_pvalue:>14.6g}")


def normality_line(values, label: str) -> None:
    array = np.asarray(values, dtype=float)
    jb_stat, jb_pvalue, skew, kurtosis = jarque_bera(array)
    print(
        f"    {label:<28s} n={array.size:<6d} mean={array.mean(): .6f} sd={array.std(ddof=1):.6f}"
    )
    print(
        f"      JB={jb_stat:.4f}  p={jb_pvalue:.6g}  skew={skew: .6f}  "
        f"excess kurt={kurtosis - 3.0: .6f}"
    )


def qq_table(values, label: str) -> None:
    array = np.asarray(values, dtype=float)
    print(f"    QQ table ({label}) -- empirical quantile vs N(0,1) quantile")
    print(f"      {'pct':>6s}{'empirical':>14s}{'theoretical':>14s}{'diff':>12s}")
    for percentile in QQ_PERCENTILES:
        empirical = float(np.percentile(array, percentile))
        theoretical = float(stats.norm.ppf(percentile / 100.0))
        print(
            f"      {percentile:>6.1f}{empirical:>14.6f}{theoretical:>14.6f}"
            f"{empirical - theoretical:>12.6f}"
        )


def run_lengths(flags) -> list[int]:
    lengths: list[int] = []
    current = 0
    for flag in flags:
        if flag:
            current += 1
        elif current:
            lengths.append(current)
            current = 0
    if current:
        lengths.append(current)
    return lengths


def describe_runs(lengths: list[int], label: str) -> None:
    if not lengths:
        print(f"    {label:<24s} episodes=0")
        return
    array = np.array(lengths, dtype=float)
    print(
        f"    {label:<24s} episodes={array.size:<5d} mean={array.mean():.4f}  "
        f"median={np.median(array):.4f}  max={int(array.max())}  "
        f"total weeks={int(array.sum())}"
    )


def section_a(returns: pd.Series) -> None:
    rule("A. DESCRIPTIVE STATS -- raw SPY weekly log returns")
    values = returns.to_numpy()
    n = values.size
    mean = values.mean()
    std = values.std(ddof=1)
    jb_stat, jb_pvalue, skew, kurtosis = jarque_bera(values)

    print(f"  n observations        : {n}")
    print(f"  date range            : {returns.index[0].date()} .. {returns.index[-1].date()}")
    print(f"  NaNs                  : {int(returns.isna().sum())}")
    print(f"  non-finite            : {int((~np.isfinite(values)).sum())}")
    spacing = returns.index.to_series().diff().dt.days.dropna()
    print(
        f"  index spacing (days)  : min={int(spacing.min())} max={int(spacing.max())} "
        f"mode={int(spacing.mode().iloc[0])} "
        f"non-7-day gaps={int((spacing != 7).sum())}"
    )
    print(f"  mean                  : {mean: .8f}")
    print(f"  std (ddof=1)          : {std: .8f}")
    print(f"  annualized vol        : {std * np.sqrt(WEEKS_PER_YEAR) * 100: .4f}%")
    print(f"  annualized mean       : {mean * WEEKS_PER_YEAR * 100: .4f}%")
    print(f"  skew                  : {skew: .6f}")
    print(f"  excess kurtosis       : {kurtosis - 3.0: .6f}")
    print(f"  min                   : {values.min(): .6f}  on {returns.idxmin().date()}")
    print(f"  max                   : {values.max(): .6f}  on {returns.idxmax().date()}")
    for percentile in (1, 5, 95, 99):
        print(f"  p{percentile:<20d} : {np.percentile(values, percentile): .6f}")
    print(f"  Jarque-Bera stat      : {jb_stat:.4f}")
    print(f"  Jarque-Bera p-value   : {jb_pvalue:.6g}")

    for threshold in (-0.05, -0.10):
        count = int((values < threshold).sum())
        print(
            f"  weeks below {threshold * 100:>5.1f}%    : {count} "
            f"({count / n * 100:.4f}% of weeks, 1 in {n / max(count, 1):.1f})"
        )


def section_b(returns: pd.Series) -> dict:
    rule("B. SPEC COMPARISON -- corrected AIC/BIC on full real history")
    nobs = len(returns)
    rows = []
    fits = {}

    llf_k1, mu_k1, sigma2_k1 = gaussian_iid_llf(returns)
    print(
        f"  spec 1 (k=1 Gaussian iid, analytic MLE): mu={mu_k1: .8f} "
        f"sigma2={sigma2_k1:.8e} sigma={np.sqrt(sigma2_k1) * 100:.4f}%/wk"
    )
    rows.append(("1. k=1 Gaussian iid", llf_k1, None, 2, None, None, "n/a (analytic)"))

    specs = (
        ("2. k=2 non-switching mean", dict(k_regimes=2), 5),
        (REPO_SPEC_LABEL, None, 6),
        ("4. k=3 non-switching mean", dict(k_regimes=3), 10),
    )

    for label, kwargs, k_free in specs:
        try:
            if kwargs is None:
                model, results, jump_regime = jm.fit_jump_model(returns)
            else:
                model, results = fit_markov(returns, **kwargs)
                jump_regime = high_variance_index(model, results)
        except Exception as error:
            print(f"  {label}: FIT RAISED {error!r}")
            rows.append((label, None, None, k_free, None, None, "RAISED"))
            continue
        converged = bool(results.mle_retvals.get("converged"))
        rows.append(
            (
                label,
                float(results.llf),
                int(model.k_params),
                k_free,
                float(results.aic),
                float(results.bic),
                "yes" if converged else "NO",
            )
        )
        fits[label] = (model, results, jump_regime)

    print()
    print(
        f"  {'spec':<28s}{'llf':>13s}{'k_sm':>6s}{'k_free':>8s}"
        f"{'AIC_sm':>13s}{'BIC_sm':>13s}{'AIC_corr':>13s}{'BIC_corr':>13s}{'conv':>6s}"
    )
    scored = []
    counts_agree = []
    for row in rows:
        label, llf, k_sm, k_free, aic_sm, bic_sm, converged = row
        if llf is None:
            print(f"  {label:<28s}{'--':>13s}{'--':>6s}{k_free:>8d}" + " " * 52 + f"{converged:>6s}")
            continue
        aic_corr, bic_corr = corrected_information_criteria(llf, k_free, nobs)
        k_sm_text = "--" if k_sm is None else str(k_sm)
        aic_sm_text = "--" if aic_sm is None else f"{aic_sm:.4f}"
        bic_sm_text = "--" if bic_sm is None else f"{bic_sm:.4f}"
        print(
            f"  {label:<28s}{llf:>13.4f}{k_sm_text:>6s}{k_free:>8d}"
            f"{aic_sm_text:>13s}{bic_sm_text:>13s}{aic_corr:>13.4f}{bic_corr:>13.4f}"
            f"{converged:>6s}"
        )
        scored.append((label, aic_corr, bic_corr, llf, k_free))
        if k_sm is not None:
            counts_agree.append(
                (
                    label,
                    k_sm,
                    k_free,
                    abs(aic_sm - aic_corr),
                    abs(bic_sm - bic_corr),
                )
            )

    sub("parameter-count reconciliation (statsmodels k_params vs corrected k_free)")
    print(f"    {'spec':<28s}{'k_sm':>6s}{'k_free':>8s}{'|dAIC|':>12s}{'|dBIC|':>12s}{'agree':>8s}")
    all_agree = True
    for label, k_sm, k_free, d_aic, d_bic in counts_agree:
        agree = k_sm == k_free and d_aic < 1e-6 and d_bic < 1e-6
        all_agree = all_agree and agree
        print(
            f"    {label:<28s}{k_sm:>6d}{k_free:>8d}{d_aic:>12.2e}{d_bic:>12.2e}"
            f"{'yes' if agree else 'NO':>8s}"
        )
    print(
        f"    every spec's counts agree? {'YES' if all_agree else 'NO'} "
        "-- nothing is pinned any more, so statsmodels' count is the honest one."
    )

    best_aic = min(scored, key=lambda item: item[1])
    best_bic = min(scored, key=lambda item: item[2])
    print()
    print(f"  WINNER corrected AIC : {best_aic[0]}  (AIC={best_aic[1]:.4f})")
    print(f"  WINNER corrected BIC : {best_bic[0]}  (BIC={best_bic[2]:.4f})")

    non_switching = next((r for r in scored if r[0].startswith("2.")), None)
    repo = next((r for r in scored if r[0] == REPO_SPEC_LABEL), None)
    k3 = next((r for r in scored if r[0].startswith("4.")), None)

    if non_switching and repo:
        # const[0]=const[1] is a single interior-point restriction on an identified
        # parameter, so the LR statistic is chi2_1 (MATH-REFERENCE 5.3). This is
        # NOT a test of the number of regimes, which would be non-standard.
        lr = 2.0 * (repo[3] - non_switching[3])
        print()
        print(
            f"  LR test of the switching mean, const[0]=const[1] (chi2_1, crit 3.841): "
            f"stat={lr:.4f} p={stats.chi2.sf(max(lr, 0.0), 1):.6g}"
        )

    if repo and k3:
        print()
        print(
            f"  repo spec vs k=3: dAIC={repo[1] - k3[1]:+.4f}  dBIC={repo[2] - k3[2]:+.4f} "
            f"(negative favours the repo spec)"
        )

    for label in [row[0] for row in specs]:
        if label in fits:
            model, results, _ = fits[label]
            sub(f"spec detail: {label}")
            regime_report(model, results, label=label)

    if REPO_SPEC_LABEL in fits:
        model, results, _ = fits[REPO_SPEC_LABEL]
        sub("standard errors, z, p-values and 95% CIs -- repo spec")
        standard_error_table(model, results, REPO_SPEC_LABEL)

    return fits


def section_c(returns: pd.Series) -> None:
    rule(
        "C. IS POST-HOC RELABELLING ACTUALLY NEEDED ON REAL DATA?"
        f"\n   window {RELABEL_WINDOW[0]} .. {RELABEL_WINDOW[1]}"
    )
    window = returns.loc[RELABEL_WINDOW[0] : RELABEL_WINDOW[1]]
    print(f"  window n = {len(window)}  ({window.index[0].date()} .. {window.index[-1].date()})")
    print(
        "  Two questions, both label-free until the last one:\n"
        "    1. does the fit pair HIGH variance with LOW persistence here?\n"
        "    2. which INDEX does the high-variance regime land on? If it is not\n"
        "       always index 1, post-hoc relabelling is load-bearing, not cosmetic."
    )

    summary = {}
    for label, kwargs in (
        ("repo spec (switch mu)", dict(k_regimes=2, switching_trend=True)),
        ("k=2 non-switching mu", dict(k_regimes=2)),
    ):
        sub(label)
        try:
            model, results = fit_markov(window, **kwargs)
        except Exception as error:
            print(f"  FIT RAISED {error!r}")
            continue
        regime_report(model, results, label=label)
        params = dict(zip(model.param_names, results.params))
        sigma2 = np.array([params["sigma2[0]"], params["sigma2[1]"]])
        durations = np.asarray(results.expected_durations, dtype=float)
        high = high_variance_index(model, results)
        low = 1 - high
        summary[label] = dict(
            high_var_regime=high,
            high_var_duration=durations[high],
            low_var_duration=durations[low],
            sigma2_high=sigma2[high],
            sigma2_low=sigma2[low],
            llf=float(results.llf),
            ergodic_high=float(
                np.asarray(model.initial_probabilities(results.params), dtype=float)[high]
            ),
        )

    sub("VERDICT")
    print(
        f"  {'fit':<24s}{'hi-var idx':>11s}{'E[D] hi-var':>13s}{'E[D] lo-var':>13s}"
        f"{'var ratio':>12s}{'ergodic hi-var':>16s}{'llf':>12s}"
    )
    for label, info in summary.items():
        print(
            f"  {label:<24s}{info['high_var_regime']:>11d}"
            f"{info['high_var_duration']:>13.4f}{info['low_var_duration']:>13.4f}"
            f"{info['sigma2_high'] / info['sigma2_low']:>12.4f}"
            f"{info['ergodic_high']:>16.6f}{info['llf']:>12.4f}"
        )

    for label, info in summary.items():
        print()
        print(f"  {label}:")
        print(
            f"    high variance paired with LOWER persistence? "
            f"{'YES' if info['high_var_duration'] < info['low_var_duration'] else 'NO'} "
            f"(E[D] hi-var={info['high_var_duration']:.4f} wks vs "
            f"lo-var={info['low_var_duration']:.4f} wks)"
        )
        print(
            f"    high variance landed on index {info['high_var_regime']}, so relabelling was "
            f"{'REQUIRED' if info['high_var_regime'] == 0 else 'a no-op'} on this window"
        )


def section_d(returns: pd.Series, model, results, jump_regime: int) -> pd.Series:
    rule("D. REGIME-STANDARDIZED RESIDUAL DIAGNOSTICS -- repo-spec full-history fit")
    mu = regime_means(model, results)
    params = dict(zip(model.param_names, results.params))
    sigma2 = np.array([params["sigma2[0]"], params["sigma2[1]"]])
    filtered = np.asarray(results.filtered_marginal_probabilities, dtype=float)
    values = returns.to_numpy()
    calm_regime = 1 - jump_regime

    print(f"  jump regime index (larger fitted variance) = {jump_regime}")
    for j in range(2):
        tag = "JUMP" if j == jump_regime else "calm"
        print(
            f"  regime {j} ({tag}): mu_hat = {mu[j]: .10g}  ({mu[j] * 100: .4f}%/wk, "
            f"{mu[j] * WEEKS_PER_YEAR * 100: .2f}%/yr)"
        )
        print(
            f"             sigma2_hat = {sigma2[j]:.10e}   sigma_hat = "
            f"{np.sqrt(sigma2[j]) * 100:.4f}%/wk   ann = "
            f"{np.sqrt(sigma2[j] * WEEKS_PER_YEAR) * 100:.2f}%"
        )
    print(
        f"  variance ratio (jump/calm) = {sigma2[jump_regime] / sigma2[calm_regime]:.4f}   "
        f"sigma ratio = {np.sqrt(sigma2[jump_regime] / sigma2[calm_regime]):.4f}"
    )
    print(f"  mean spread (jump - calm) = {mu[jump_regime] - mu[calm_regime]: .8f}")

    hard_state = np.argmax(filtered, axis=1)
    z_hard = (values - mu[hard_state]) / np.sqrt(sigma2[hard_state])
    # Mixture moments, not just the mixture of variances: with a switching mean the
    # spread between the two means is itself part of the conditional variance.
    mixture_mean = filtered @ mu
    mixture_variance = filtered @ (sigma2 + mu**2) - mixture_mean**2
    z_weighted = (values - mixture_mean) / np.sqrt(mixture_variance)
    raw = values - values.mean()

    print(
        f"  hard-assignment regime counts (filtered argmax): "
        f"calm={int((hard_state == calm_regime).sum())} "
        f"jump={int((hard_state == jump_regime).sum())} "
        f"({(hard_state == jump_regime).mean() * 100:.4f}% jump)"
    )
    p_jump = filtered[:, jump_regime]
    rcm = 400.0 / len(values) * float((p_jump * (1.0 - p_jump)).sum())
    print(f"  RCM (Ang-Bekaert, filtered; 0=sharp, 100=uninformative): {rcm:.4f}")

    series = {
        "z (hard assignment)": z_hard,
        "z (mixture moments)": z_weighted,
        "raw returns (r - rbar)": raw,
    }

    sub("D.1 normality")
    for label, array in series.items():
        normality_line(array, label)

    sub("D.2 QQ tables")
    for label, array in series.items():
        qq_table(array, label)
        print()

    sub("D.3 Ljung-Box on the level")
    for label, array in series.items():
        ljung_box_table(array, label)

    sub("D.4 Ljung-Box on squares")
    for label, array in series.items():
        ljung_box_table(np.asarray(array) ** 2, f"{label} squared")

    sub("D.5 ARCH-LM")
    for label, array in series.items():
        arch_lm_table(array, label)

    return filtered_jump_probability(results, jump_regime)


def section_e(model, results, jump_probability: pd.Series, jump_regime: int) -> None:
    rule("E. DURATION REALISM -- repo-spec full-history fit")
    transition = model.regime_transition_matrix(results.params)[:, :, 0]
    durations = np.asarray(results.expected_durations, dtype=float)
    ergodic = np.asarray(model.initial_probabilities(results.params), dtype=float)
    calm_regime = 1 - jump_regime

    print(f"  jump regime index = {jump_regime}, calm regime index = {calm_regime}")
    print(f"  p_calm-stay = {transition[calm_regime, calm_regime]:.8f}   model E[D_calm] = "
          f"{durations[calm_regime]:.4f} weeks")
    print(f"  p_jump-stay = {transition[jump_regime, jump_regime]:.8f}   model E[D_jump] = "
          f"{durations[jump_regime]:.4f} weeks")
    print(f"  model ergodic P(jump) = {ergodic[jump_regime]:.6f}   "
          f"P(calm) = {ergodic[calm_regime]:.6f}")

    jump_flags = (jump_probability > 0.5).to_numpy()
    calm_flags = ~jump_flags
    empirical_jump_share = float(jump_flags.mean())
    print(
        f"  empirical share of weeks with filtered P(jump) > 0.5 = "
        f"{empirical_jump_share:.6f}  ({int(jump_flags.sum())} of {jump_flags.size} weeks)"
    )
    print(
        f"  ergodic vs empirical gap = {ergodic[jump_regime] - empirical_jump_share:+.6f} "
        f"(ratio empirical/ergodic = {empirical_jump_share / ergodic[jump_regime]:.4f})"
    )

    sub("observed run lengths of filtered-probability episodes (weeks)")
    jump_runs = run_lengths(jump_flags)
    calm_runs = run_lengths(calm_flags)
    describe_runs(jump_runs, "jump (P>0.5)")
    describe_runs(calm_runs, "calm (P<=0.5)")
    print(f"    model E[D_jump] = {durations[jump_regime]:.4f} vs empirical mean jump run = "
          f"{np.mean(jump_runs):.4f}, max = {max(jump_runs)}")
    print(f"    model E[D_calm] = {durations[calm_regime]:.4f} vs empirical mean calm run = "
          f"{np.mean(calm_runs):.4f}, max = {max(calm_runs)}")

    sub("longest 10 jump episodes")
    starts = []
    index = jump_probability.index
    position = 0
    while position < len(jump_flags):
        if jump_flags[position]:
            start = position
            while position < len(jump_flags) and jump_flags[position]:
                position += 1
            starts.append((index[start], index[position - 1], position - start))
        else:
            position += 1
    for first, last, length in sorted(starts, key=lambda item: -item[2])[:10]:
        print(f"    {first.date()} .. {last.date()}   {length:>3d} weeks")


def section_f(jump_probability: pd.Series) -> None:
    rule("F. HISTORICAL SANITY CHECK -- filtered jump probability, repo-spec full-history fit")
    sub("mean filtered jump probability by calendar year")
    print(f"    {'year':>6s}{'weeks':>7s}{'mean P(jump)':>15s}{'max P(jump)':>14s}"
          f"{'weeks P>0.5':>13s}")
    grouped = jump_probability.groupby(jump_probability.index.year)
    for year, group in grouped:
        print(
            f"    {year:>6d}{len(group):>7d}{group.mean():>15.6f}{group.max():>14.6f}"
            f"{int((group > 0.5).sum()):>13d}"
        )

    sub("max filtered jump probability by named window")
    print(f"    {'window':<22s}{'weeks':>6s}{'max P(jump)':>14s}{'date of max':>14s}"
          f"{'mean P(jump)':>14s}{'weeks P>0.5':>13s}")
    for label, start, end in CRISIS_WINDOWS:
        window = jump_probability.loc[start:end]
        if window.empty:
            print(f"    {label:<22s}{'0':>6s}  (no observations)")
            continue
        print(
            f"    {label:<22s}{len(window):>6d}{window.max():>14.6f}"
            f"{str(window.idxmax().date()):>14s}{window.mean():>14.6f}"
            f"{int((window > 0.5).sum()):>13d}"
        )


def section_g(returns: pd.Series, jump_probability: pd.Series) -> None:
    rule("G. MELT-UP ASYMMETRY -- does the switching mean make the signal sign-aware?")
    frame = pd.DataFrame({"ret": returns, "p": jump_probability})
    top20 = frame.sort_values("p", ascending=False).head(20)

    sub("20 weeks with the highest filtered jump probability")
    print(f"    {'#':>3s}{'date':>13s}{'weekly ret':>13s}{'P(jump)':>12s}{'sign':>7s}")
    for rank, (timestamp, row) in enumerate(top20.iterrows(), start=1):
        print(
            f"    {rank:>3d}{str(timestamp.date()):>13s}{row['ret']:>13.6f}"
            f"{row['p']:>12.8f}{'POS' if row['ret'] > 0 else 'neg':>7s}"
        )
    positives = int((top20["ret"] > 0).sum())
    print()
    print(f"    POSITIVE-return weeks among the top 20: {positives} of 20 "
          f"({positives / 20 * 100:.1f}%)")
    print(f"    mean return of the 20: {top20['ret'].mean(): .6f}   "
          f"mean |return|: {top20['ret'].abs().mean():.6f}")

    sub("mean filtered jump probability by return tail")
    top_cut = float(np.percentile(returns, 95))
    bottom_cut = float(np.percentile(returns, 5))
    top_mask = returns >= top_cut
    bottom_mask = returns <= bottom_cut
    top_mean = float(jump_probability[top_mask].mean())
    bottom_mean = float(jump_probability[bottom_mask].mean())
    print(f"    top 5% cutoff (p95)    = {top_cut: .6f}   n={int(top_mask.sum())}")
    print(f"    bottom 5% cutoff (p5)  = {bottom_cut: .6f}   n={int(bottom_mask.sum())}")
    print(f"    mean P(jump) | top 5% big UP weeks      = {top_mean:.6f}")
    print(f"    mean P(jump) | bottom 5% big DOWN weeks = {bottom_mean:.6f}")
    print(f"    mean P(jump) | middle 90%               = "
          f"{jump_probability[~(top_mask | bottom_mask)].mean():.6f}")
    print(f"    mean P(jump) | all weeks                = {jump_probability.mean():.6f}")
    print(
        f"    UP/DOWN ratio (1.0 = fully sign-blind, 0.0 = fully sign-aware) = "
        f"{top_mean / bottom_mean:.4f}"
    )

    sub("mean filtered jump probability by absolute-return cutoff")
    print(f"    {'cutoff':>8s}{'up n':>7s}{'mean P up':>13s}{'down n':>8s}"
          f"{'mean P down':>13s}{'up/down':>10s}")
    for threshold in (0.03, 0.05, 0.07):
        up = returns >= threshold
        down = returns <= -threshold
        up_mean = float(jump_probability[up].mean())
        down_mean = float(jump_probability[down].mean())
        print(
            f"    {threshold * 100:>7.0f}%{int(up.sum()):>7d}{up_mean:>13.6f}"
            f"{int(down.sum()):>8d}{down_mean:>13.6f}{up_mean / down_mean:>10.4f}"
        )


def main() -> None:
    rule("SETUP")
    returns = load_returns()
    print(
        "AIC/BIC are still recomputed here from an explicit k_free; res.bse/pvalues/"
        "conf_int\nARE read, and are valid, because the repo spec pins nothing."
    )

    section_a(returns)
    fits = section_b(returns)
    section_c(returns)

    if REPO_SPEC_LABEL not in fits:
        print("\nRepo-spec full-history fit unavailable; sections D-G skipped.")
        sys.exit(1)

    model, results, jump_regime = fits[REPO_SPEC_LABEL]
    jump_probability = section_d(returns, model, results, jump_regime)
    section_e(model, results, jump_probability, jump_regime)
    section_f(jump_probability)
    section_g(returns, jump_probability)

    # estimate_jump_regimes() now returns filtered probabilities, so smoothed is no
    # longer something the model hands out. Kept because the size of the gap is the
    # measure of how much look-ahead the old smoothed return leaked into the signal.
    rule("SMOOTHED-VS-FILTERED GAP (reported only here, per the look-ahead rule)")
    smoothed = results.smoothed_marginal_probabilities.iloc[:, jump_regime]
    gap = (jump_probability - smoothed).abs()
    print(f"  max |filtered - smoothed| = {gap.max():.6f} on {gap.idxmax().date()}")
    print(f"  mean |filtered - smoothed| = {gap.mean():.6f}")
    print(f"  weeks where the two disagree about the 0.5 threshold: "
          f"{int(((jump_probability > 0.5) != (smoothed > 0.5)).sum())}")
    print(f"  mean filtered = {jump_probability.mean():.6f}   "
          f"mean smoothed = {smoothed.mean():.6f}")
    print()


if __name__ == "__main__":
    main()
