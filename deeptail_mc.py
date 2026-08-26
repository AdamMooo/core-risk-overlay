r"""Deep-tail inference for the SJM reproduction -- Monte Carlo under three named nulls.

VERIFICATION RUN, NOT A STRATEGY (the 0/1 rule is F9, PARKED section 4).

Design preregistered in docs/REPRO-SJM2024-FINDINGS.md ("Preregistered for the
inference run", 2026-08-26) before first execution.

Why this file is not a bootstrap. MaxDD and CDaR at 1-5% on this sample are
produced by two episodes (2000-02, 2007-09), so their effective sample size is
the number of independent deep episodes -- 2 -- and not 8,560 days. A block
bootstrap's resample-to-resample variation in a maximum drawdown is dominated by
how often the resampler happens to concatenate blocks drawn from those two
episodes, and that frequency is a property of the block length b. Reporting such
a p-value is reporting the knob. MATH-REFERENCE section 3 states the single-path
version of this ("effective n = 1"); the difference of two of them inherits it.

So the deep half asks a different question, which simulation can answer honestly:
GIVEN A WORLD, how big a deep-tail gap do these two rules open on each other by
construction? Three worlds, run in this order:

  N3  i.i.d. resampling of the observed returns. No clustering, no ordering.
      THE CONTROL, scored first. Neither rule has information here, so any gap
      must be attributable to their different TIME IN MARKET -- the rule holding
      cash more often shows the shallower tail. A gap whose sign contradicts its
      exposure difference means the pipeline manufactures one, and BOTH halves of
      the run are void. A non-zero centre is expected and is not a failure: see
      the Z0 amendment in the preregistration.
  N1  GARCH(1,1) with Student-t innovations. Volatility clusters and tails are
      fat, but there is no discrete state for the jump model to find. THE MAIN
      NULL. If the observed gap sits inside this distribution, the deep-tail
      residual is what two volatility-reactive rules do to each other on a
      clustered path -- not evidence that the fitted state carries information
      the band lacks.
  N2  2-state Markov-switching Gaussian with state-dependent variance: a world
      where the jump model's own premise is TRUE BY CONSTRUCTION. A POWER CHECK,
      not a null. If the jump model's edge is wide and overlapping zero even
      here, then no sample of this length could distinguish the two rules even
      when regimes are real -- a stronger closure than "not significant".

Both rules are run END TO END on every simulated path: same 3000-day training
window, same 126-day refit schedule, same 60-day realized-volatility measure,
same 10bp cost, same one-day execution lag, the historical risk-free path and
trading calendar reused.

Identification, declared before the run and binding on every sentence after it:
the deep-tail CDaR difference is NOT identified in magnitude. Only the width of
a distribution and whether it contains the observed value may be reported.

Run: .venv\Scripts\python.exe deeptail_mc.py                 all three nulls
     .venv\Scripts\python.exe deeptail_mc.py --paths 20      a smoke run
     .venv\Scripts\python.exe deeptail_mc.py --null N3
"""
from __future__ import annotations

import argparse
import os
import sys
import time
from functools import partial
from multiprocessing import Pool
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import minimize
from scipy.special import gammaln

sys.path.insert(0, str(Path(__file__).resolve().parent))

from repro_sjm2024 import (
    CACHE,
    TRADING_DAYS,
    TRAIN_DAYS,
    VOL_WINDOW,
    backtest,
    daily_riskfree,
    load_prices,
    load_riskfree,
    run_jump_model,
)
from src.pathfunctionals import cdar, drawdown
from src.sjm_features import build_features
from volthreshold import PAIRS, threshold_signal

DEEP_ALPHAS = (0.01, 0.05)
N_PATHS = 200
LAMBDA_PAPER = 25.0
BENCHMARK = f"JM fixed paper-{LAMBDA_PAPER:g}"
PAPER_END = "2023-12-29"
NULLS = ("N3", "N1", "N2")
OUT = CACHE / "deeptail_mc.csv"


# ---------------------------------------------------------------------------
# N1 -- GARCH(1,1) with standardized Student-t innovations, by hand.
#
#   r_t      = mu + eps_t,      eps_t = sigma_t z_t,      z_t ~ t_nu / sqrt(nu/(nu-2))
#   sigma2_t = omega + alpha eps2_{t-1} + beta sigma2_{t-1}
#
# The persistence alpha + beta is kept strictly below 1 by construction: with
# s = sigmoid(x_s)*0.999 and p = sigmoid(x_p), alpha = s*p and beta = s*(1-p),
# so the optimiser cannot wander into an unconditionally-infinite-variance model
# and no penalty term is needed.
# ---------------------------------------------------------------------------


def _sigmoid(x: float) -> float:
    return 1.0 / (1.0 + np.exp(-x))


def _garch_unpack(theta: np.ndarray) -> tuple[float, float, float, float, float]:
    mu, log_omega, x_s, x_p, log_nu = theta
    persistence = _sigmoid(x_s) * 0.999
    weight = _sigmoid(x_p)
    return (mu, np.exp(log_omega), persistence * weight,
            persistence * (1.0 - weight), np.exp(log_nu) + 2.05)


def _garch_variances(eps: np.ndarray, omega: float, alpha: float, beta: float) -> np.ndarray:
    sigma2 = np.empty(len(eps))
    sigma2[0] = eps.var()
    for t in range(1, len(eps)):
        sigma2[t] = omega + alpha * eps[t - 1] ** 2 + beta * sigma2[t - 1]
    return sigma2


def _garch_nll(theta: np.ndarray, r: np.ndarray) -> float:
    mu, omega, alpha, beta, nu = _garch_unpack(theta)
    if omega <= 0 or nu <= 2.05:
        return 1e12
    eps = r - mu
    sigma2 = _garch_variances(eps, omega, alpha, beta)
    if not np.all(np.isfinite(sigma2)) or np.any(sigma2 <= 0):
        return 1e12
    z2 = eps**2 / sigma2
    const = gammaln((nu + 1) / 2) - gammaln(nu / 2) - 0.5 * np.log(np.pi * (nu - 2))
    loglik = np.sum(const - 0.5 * np.log(sigma2) - (nu + 1) / 2 * np.log1p(z2 / (nu - 2)))
    return -float(loglik) if np.isfinite(loglik) else 1e12


def fit_garch_t(r: np.ndarray) -> dict:
    scale = 100.0
    x = r * scale
    start = np.array([x.mean(), np.log(x.var() * 0.05), 2.5, -1.5, np.log(4.0)])
    fit = minimize(_garch_nll, start, args=(x,), method="Nelder-Mead",
                   options={"maxiter": 4000, "xatol": 1e-6, "fatol": 1e-6})
    mu, omega, alpha, beta, nu = _garch_unpack(fit.x)
    return {"mu": mu / scale, "omega": omega / scale**2, "alpha": alpha, "beta": beta,
            "nu": nu, "scale": scale, "nll": float(fit.fun), "converged": bool(fit.success)}


def simulate_garch_t(params: dict, n_obs: int, rng: np.random.Generator) -> np.ndarray:
    burn = 1000
    nu = params["nu"]
    z = rng.standard_t(nu, size=n_obs + burn) / np.sqrt(nu / (nu - 2.0))
    omega, alpha, beta = params["omega"], params["alpha"], params["beta"]
    sigma2 = omega / max(1.0 - alpha - beta, 1e-6)
    out = np.empty(n_obs + burn)
    for t in range(n_obs + burn):
        eps = np.sqrt(sigma2) * z[t]
        out[t] = params["mu"] + eps
        sigma2 = omega + alpha * eps**2 + beta * sigma2
    return out[burn:]


# ---------------------------------------------------------------------------
# N2 -- 2-state Markov-switching Gaussian with state-dependent variance.
# ---------------------------------------------------------------------------


def fit_markov_variance(r: np.ndarray) -> dict:
    from statsmodels.tsa.regime_switching.markov_regression import MarkovRegression

    fit = MarkovRegression(r * 100.0, k_regimes=2, trend="c", switching_variance=True).fit(
        search_reps=20, disp=False
    )
    transition = np.asarray(fit.regime_transition)[:, :, 0]
    transition = transition / transition.sum(axis=0, keepdims=True)
    means = np.array([fit.params[f"const[{k}]"] for k in range(2)]) / 100.0
    variances = np.array([fit.params[f"sigma2[{k}]"] for k in range(2)]) / 100.0**2
    order = np.argsort(variances)  # 0 = quiet
    return {"transition": transition[np.ix_(order, order)], "means": means[order],
            "variances": variances[order], "llf": float(fit.llf)}


def simulate_markov(params: dict, n_obs: int, rng: np.random.Generator) -> np.ndarray:
    transition, means = params["transition"], params["means"]
    sigma = np.sqrt(params["variances"])
    state = 0
    out = np.empty(n_obs)
    draws = rng.random(n_obs)
    shocks = rng.standard_normal(n_obs)
    for t in range(n_obs):
        state = 0 if draws[t] < transition[0, state] else 1
        out[t] = means[state] + sigma[state] * shocks[t]
    return out


def simulate_iid(r: np.ndarray, n_obs: int, rng: np.random.Generator) -> np.ndarray:
    return rng.choice(r, size=n_obs, replace=True)


# ---------------------------------------------------------------------------
# The pipeline, identical for real and simulated returns.
# ---------------------------------------------------------------------------


def deep_statistics(result: dict) -> dict:
    """Deep-tail depths, plus time-in-market -- which is not decoration.

    Two rules holding the market for different fractions of the sample have
    different drawdowns with zero information between them. The observed
    comparison carries exactly that confound (JM 62% against bands at 62-73%),
    so exposure is recorded on every path and the N3 control is read against it
    rather than against zero. See the Z0 amendment in the preregistration.
    """
    curve = result["curve"]
    stats = {f"cdar{a:.2f}": float(cdar(curve, a)) for a in DEEP_ALPHAS}
    stats["maxdd"] = float(drawdown(curve).max())
    stats["timein"] = float(result["TimeIn"])
    return stats


def run_pipeline(returns: np.ndarray, dates: pd.DatetimeIndex, rf: np.ndarray) -> dict:
    """Both rules, end to end, on one return path. Returns deep statistics per rule."""
    r = pd.Series(returns, index=dates)
    rf_series = pd.Series(rf, index=dates)
    features = build_features((r - rf_series).dropna())
    r, rf_series = r.reindex(features.index), rf_series.reindex(features.index)
    realized = r.rolling(VOL_WINDOW).std().mul(np.sqrt(TRADING_DAYS))

    signal = run_jump_model(features, features.index[TRAIN_DAYS], 2.0 * LAMBDA_PAPER).dropna()
    oos = signal.index
    r_oos, rf_oos = r.reindex(oos), rf_series.reindex(oos)

    out = {BENCHMARK: deep_statistics(backtest(r_oos, signal, rf_oos))}
    for p_exit, p_reenter in PAIRS:
        band = threshold_signal(realized, oos, p_exit, p_reenter)
        out[f"RV band ({p_exit},{p_reenter})"] = deep_statistics(
            backtest(r_oos, band, rf_oos)
        )
    return out


def gaps(stats: dict) -> dict:
    """JM minus band, per band and per statistic. Positive = the JM ran deeper."""
    out = {}
    for name, values in stats.items():
        if name == BENCHMARK:
            continue
        for key, value in values.items():
            out[f"{name}|{key}"] = stats[BENCHMARK][key] - value
    return out


def one_path(seed: int, null: str, params: dict, dates, rf: np.ndarray,
             observed_returns: np.ndarray) -> dict:
    os.environ.setdefault("OMP_NUM_THREADS", "1")
    rng = np.random.default_rng(seed)
    n_obs = len(dates)
    if null == "N1":
        returns = simulate_garch_t(params, n_obs, rng)
    elif null == "N2":
        returns = simulate_markov(params, n_obs, rng)
    else:
        returns = simulate_iid(observed_returns, n_obs, rng)
    row = gaps(run_pipeline(returns, dates, rf))
    row["seed"] = seed
    row["null"] = null
    return row


# ---------------------------------------------------------------------------


def historical(ticker: str, start: str, oos_start: str):
    """The real series, and the observed gaps the nulls are compared against."""
    prices = load_prices(ticker, start)
    returns = prices.pct_change().dropna()
    rf = daily_riskfree(load_riskfree(), returns.index)
    features = build_features((returns - rf).dropna())
    returns, rf = returns.reindex(features.index), rf.reindex(features.index)

    first = max(int(features.index.searchsorted(pd.Timestamp(oos_start))), TRAIN_DAYS)
    end = int(features.index.searchsorted(pd.Timestamp(PAPER_END), side="right"))
    keep = slice(first - TRAIN_DAYS, end)
    return returns.iloc[keep], rf.iloc[keep]


def summarise(draws: pd.DataFrame, observed: dict, null: str) -> None:
    print(f"\n{'='*86}\n{null} -- {len(draws)} paths\n{'='*86}")
    header = f"{'gap (JM minus band)':<34s}{'observed':>10s}{'null mean':>11s}" \
             f"{'null 2.5%':>11s}{'null 97.5%':>11s}{'pctile':>8s}{'':>10s}"
    print(header)
    print("-" * len(header))
    for column in sorted(c for c in draws.columns if "|" in c):
        values = draws[column].to_numpy(dtype=float)
        point = observed[column]
        lo, hi = np.percentile(values, [2.5, 97.5])
        pct = float((values < point).mean())
        verdict = "inside" if lo <= point <= hi else "OUTSIDE"
        if column.endswith("timein"):
            verdict = "exposure"
        print(f"{column:<34s}{point:>10.2%}{values.mean():>11.2%}{lo:>11.2%}{hi:>11.2%}"
              f"{pct:>8.1%}{verdict:>10s}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ticker", default="^GSPC")
    parser.add_argument("--start", default="1970-01-01")
    parser.add_argument("--oos-start", default="1990-01-01")
    parser.add_argument("--paths", type=int, default=N_PATHS)
    parser.add_argument("--null", choices=NULLS, action="append")
    parser.add_argument("--workers", type=int, default=max(1, (os.cpu_count() or 2) - 2))
    args = parser.parse_args()

    returns, rf = historical(args.ticker, args.start, args.oos_start)
    dates = returns.index
    observed = gaps(run_pipeline(returns.to_numpy(), dates, rf.to_numpy()))
    print(f"observed path: {dates[0].date()} to {dates[-1].date()}   "
          f"{len(dates)} days ({TRAIN_DAYS} training + {len(dates)-TRAIN_DAYS} out of sample)")
    print("\nobserved gaps (JM minus band; positive = the jump model ran deeper):")
    for key in sorted(observed):
        print(f"  {key:<34s}{observed[key]:>9.2%}")

    fitted = {"N3": {}}
    for null in args.null or NULLS:
        if null == "N1":
            fitted["N1"] = fit_garch_t(returns.to_numpy())
            print(f"\nN1 GARCH(1,1)-t: alpha={fitted['N1']['alpha']:.4f} "
                  f"beta={fitted['N1']['beta']:.4f} "
                  f"persistence={fitted['N1']['alpha']+fitted['N1']['beta']:.4f} "
                  f"nu={fitted['N1']['nu']:.2f} converged={fitted['N1']['converged']}")
        elif null == "N2":
            fitted["N2"] = fit_markov_variance(returns.to_numpy())
            transition = fitted["N2"]["transition"]
            print(f"\nN2 Markov-switching: annualised vol "
                  f"{np.sqrt(fitted['N2']['variances']*TRADING_DAYS)} "
                  f"stay probabilities {np.diag(transition)}")

    rows = []
    for null in args.null or NULLS:
        started = time.time()
        worker = partial(one_path, null=null, params=fitted[null], dates=dates,
                         rf=rf.to_numpy(), observed_returns=returns.to_numpy())
        seeds = [20260826 + i for i in range(args.paths)]
        with Pool(args.workers) as pool:
            done = pool.map(worker, seeds)
        rows.extend(done)
        pd.DataFrame(rows).to_csv(OUT, index=False)
        draws = pd.DataFrame(done)
        summarise(draws, observed, null)
        print(f"({time.time()-started:.0f}s on {args.workers} workers; "
              f"appended to {OUT.name})")

    print(f"\n{'='*86}")
    print("Y2 -- intersection-union. The claim is that the jump model beats EVERY band, so")
    print("its null is a union: the statistic is the MAXIMUM of the three percentiles and")
    print("the claim stands only if all three clear alpha=0.05. No Bonferroni: that would")
    print("correct the opposite claim.")
    print("\nNo magnitude may be quoted from anything above -- field 7 of the preregistration")
    print("declares the deep-tail difference unidentified, before this run.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
