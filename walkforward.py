"""Walk-forward correctness harness for the Markov-switching model.

Answers the question the rest of the repo has not: is this usable as a LIVE
weekly estimator? Everything prior fits parameters once and applies them
across the whole evaluation period, which is still parameter look-ahead --
the parameters saw data that had not happened yet.

Here, at each refit point r the model is fitted on returns[:r] only, and the
signal for weeks r..next_refit is produced with those parameters. Nothing from
the future enters at any point.

Measured, in order of how badly each would sink the model:
  1. does the HIGH-VARIANCE LABEL flip between refits (the signal inverts)
  2. do fits converge at every refit
  3. how much does the estimate for week t get REVISED by later refits
  4. how far the honest live signal sits from the full-sample signal
  5. how long the burn-in is before parameters stabilise

Run: .venv\\Scripts\\python.exe walkforward.py [SPY|QQQ]
Results cache to data/walkforward_<ticker>.csv so reruns are cheap.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

import numpy as np
import pandas as pd
from statsmodels.tsa.regime_switching.markov_regression import MarkovRegression

import data_loader as dl
import evaluation as ev
import markov_switching as ms
import predictive as pr

TICKERS = ("SPY", "QQQ")
ALPHAS = (0.10, 0.05, 0.01)    # RESEARCH-PROTOCOL section 5.2
MIN_TRAIN_WEEKS = 520          # 10 years; see markov_switching.RELIABLE_MIN_OBSERVATIONS
REFIT_EVERY_WEEKS = 13         # quarterly, a realistic operational cadence
STATE_THRESHOLD = 0.50        # the 0.5 convention used throughout the docs;
                              # tiering is out of scope (RESEARCH-PROTOCOL section 9)
DATA_DIR = Path(__file__).parent / "data"


def load_returns(ticker: str) -> pd.Series:
    cache = DATA_DIR / f"{ticker.lower()}_weekly.csv"
    if cache.exists():
        s = pd.read_csv(cache, index_col=0, parse_dates=True).iloc[:, 0]
        return s.astype("float64").dropna()
    returns = dl.load_weekly_log_returns(ticker=ticker, start=dl.DEFAULT_START)
    if len(returns) < MIN_TRAIN_WEEKS + REFIT_EVERY_WEEKS:
        raise ValueError(
            f"{ticker}: only {len(returns)} weekly returns available; need at least "
            f"{MIN_TRAIN_WEEKS + REFIT_EVERY_WEEKS} for a walk-forward run."
        )
    DATA_DIR.mkdir(exist_ok=True)
    returns.to_csv(cache)
    return returns


def filter_with(returns: pd.Series, params: np.ndarray) -> np.ndarray:
    """Filtered marginal probabilities over the full series at fixed params.

    Slicing this is legitimate: the Hamilton filter is a forward recursion, so
    the value at week t depends only on returns up to t. Running it over the
    whole series and reading position t gives exactly what was knowable at t.
    """
    model = MarkovRegression(returns, k_regimes=ms.N_REGIMES, trend="c",
                             switching_trend=True, switching_variance=True)
    return np.asarray(model.filter(params).filtered_marginal_probabilities)


def walk_forward(returns: pd.Series) -> pd.DataFrame:
    refit_points = list(range(MIN_TRAIN_WEEKS, len(returns), REFIT_EVERY_WEEKS))
    rows, failures = [], 0

    for n, start in enumerate(refit_points):
        window = returns.iloc[:start]
        try:
            model, results, hv_regime = ms.fit_markov_switching(window)
        except (RuntimeError, ValueError) as exc:
            failures += 1
            rows.append({"refit_end": returns.index[start - 1], "n_obs": start,
                         "converged": False, "hv_regime": np.nan,
                         "error": type(exc).__name__})
            continue

        params = np.asarray(results.params, dtype=float)
        names = model.param_names
        probs = filter_with(returns, params)[:, hv_regime]
        stop = refit_points[n + 1] if n + 1 < len(refit_points) else len(returns)

        rows.append({
            "refit_end": returns.index[start - 1],
            "n_obs": start,
            "converged": True,
            "hv_regime": hv_regime,
            "llf": results.llf,
            "live_from": returns.index[start],
            "live_to": returns.index[stop - 1],
            **{name: params[names.index(name)] for name in names},
            "live_probs": probs[start:stop],
            "live_index": returns.index[start:stop],
            "hindsight_probs_at_live": probs,
        })

    print(f"  refits attempted: {len(refit_points)}   failures: {failures}")
    return pd.DataFrame(rows)


def walk_forward_density(returns: pd.Series) -> pd.DataFrame:
    """Vintage-correct one-step-ahead VaR, ES and PIT for every live week.

    RESEARCH-PROTOCOL step 5. The alignment discipline, stated because this is
    exactly where look-ahead hides. For a live week t served by the refit made
    at `start`:

      parameters   fitted on returns[:start]     -- data through week start-1
      state        filtered[t-1]                 -- data through week t-1
      weights      w = filtered[t-1] @ P         -- the forward step
      density      mixture(w, means, sigmas)     -- formed BEFORE r_t exists
      scored on    returns[t]                    -- the realized week

    Nothing on the right of "known at t-1" appears on the left. Running the
    Hamilton filter over the whole series and reading position t-1 is legitimate
    for the same reason `filter_with` documents: it is a forward recursion, so
    position t-1 depends only on returns up to t-1.

    Note the label-flip defect that dogs the probability signal is IRRELEVANT
    here. The mixture sums over all regimes, so which index is called
    high-variance never enters. That is a real advantage of scoring the density
    rather than the state.
    """
    refit_points = list(range(MIN_TRAIN_WEEKS, len(returns), REFIT_EVERY_WEEKS))
    values = returns.to_numpy(dtype=float)
    rows, failures = [], 0

    for n, start in enumerate(refit_points):
        try:
            model, results, _ = ms.fit_markov_switching(returns.iloc[:start])
        except (RuntimeError, ValueError):
            failures += 1
            continue

        means, sigmas = pr.regime_parameters(model, results)
        transition = pr.transition_matrix(results)
        filtered = filter_with(returns, np.asarray(results.params, dtype=float))
        stop = refit_points[n + 1] if n + 1 < len(refit_points) else len(returns)

        # Index of the wider regime, for reporting the weight only. The density
        # itself never needs it -- see the docstring.
        wide = int(np.argmax(sigmas))

        for t in range(start, stop):
            weights = pr.state_prediction(filtered[t - 1], transition)
            row = {
                "date": returns.index[t],
                "realized": values[t],
                "refit_end": returns.index[start - 1],
                "w_wide": float(weights[wide]),
                "sigma_wide": float(sigmas[wide]),
                "sigma_calm": float(sigmas[1 - wide]),
                "pit": pr.mixture_cdf(values[t], weights, means, sigmas),
            }
            for alpha in ALPHAS:
                risk = pr.mixture_tail_risk(weights, means, sigmas, alpha)
                row[f"var_{alpha}"] = risk.var
                row[f"es_{alpha}"] = risk.expected_shortfall
            rows.append(row)

    if failures:
        print(f"  WARNING: {failures} refit(s) failed and were skipped")
    return pd.DataFrame(rows).set_index("date")


def report_density(ticker: str) -> None:
    print("=" * 76)
    print(f"WALK-FORWARD PREDICTIVE DENSITY — {ticker}")
    print("=" * 76)

    returns = load_returns(ticker)
    print(f"  weeks: {len(returns)}  {returns.index[0].date()} .. {returns.index[-1].date()}")
    print(f"  first fit at week {MIN_TRAIN_WEEKS}, refit every {REFIT_EVERY_WEEKS} weeks")
    print("  NO look-ahead: parameters and state at t use only data through t-1.")

    frame = walk_forward_density(returns)
    print(f"\n  out-of-sample forecasts: {len(frame)}  "
          f"{frame.index[0].date()} .. {frame.index[-1].date()}")

    print()
    print("TABLE 3 — QUANTILE COVERAGE")
    print(f"  {'alpha':>6s} {'breaches':>9s} {'rate':>8s} {'Kupiec p':>10s} "
          f"{'indep p':>9s} {'CC p':>9s}")
    for alpha in ALPHAS:
        hits = frame["realized"] < frame[f"var_{alpha}"]
        c = ev.coverage_tests(hits, alpha)
        print(f"  {alpha:6.2f} {c.exceedances:9d} {c.observed_rate:8.4f} "
              f"{c.p_uc:10.4f} {c.p_ind:9.4f} {c.p_cc:9.4f}")

    print()
    print("TABLE 2 — DENSITY CALIBRATION (primary)")
    full = ev.berkowitz_test(frame["pit"])
    print(f"  Berkowitz full   LR {full.lr:8.2f}  df {full.df}  p {full.p_value:.4f}")
    print(f"    mu {full.mu:+.4f}   rho {full.rho:+.4f}   sigma2 {full.sigma2:.4f}"
          f"   clipped {full.n_clipped}")
    for alpha in (0.10, 0.05):
        try:
            tail = ev.censored_berkowitz_test(frame["pit"], alpha)
            print(f"  Berkowitz tail alpha={alpha:.2f}  LR {tail.lr:8.2f}  df {tail.df}  "
                  f"p {tail.p_value:.4f}   mu {tail.mu:+.4f}  sigma2 {tail.sigma2:.4f}"
                  f"  n_tail {tail.n_tail}")
        except ValueError as exc:
            print(f"  Berkowitz tail alpha={alpha:.2f}  not run: {exc}")

    diagnostics = ev.pit_diagnostics(frame["pit"])
    print(f"  PIT uniformity chi2 {diagnostics.uniformity_chi2:.2f} "
          f"p {diagnostics.uniformity_p:.4f}")
    print(f"  Ljung-Box  u      Q {diagnostics.ljung_box_level:8.2f} "
          f"p {diagnostics.ljung_box_level_p:.4f}")
    print(f"  Ljung-Box (u-.5)^2 Q {diagnostics.ljung_box_squared:8.2f} "
          f"p {diagnostics.ljung_box_squared_p:.4f}   <- unabsorbed vol dynamics")

    print()
    print("TABLE 4 — ES BREACH SEVERITY (point estimate; bootstrap not yet built)")
    print(f"  {'alpha':>6s} {'n':>5s} {'mean realized':>14s} {'mean predicted ES':>18s} "
          f"{'ratio':>7s}")
    for alpha in ALPHAS:
        breached = frame[frame["realized"] < frame[f"var_{alpha}"]]
        if breached.empty:
            continue
        realized_mean = float(breached["realized"].mean())
        predicted_mean = float(breached[f"es_{alpha}"].mean())
        print(f"  {alpha:6.2f} {len(breached):5d} {realized_mean:14.4f} "
              f"{predicted_mean:18.4f} {realized_mean / predicted_mean:7.3f}")
    print("  ratio > 1 means the model UNDERSTATES how bad the bad weeks are.")

    out = DATA_DIR / f"density_{ticker.lower()}.csv"
    frame.to_csv(out)
    print(f"\n  series written to {out.relative_to(Path(__file__).parent)}")


def report(ticker: str) -> None:
    print("=" * 76)
    print(f"WALK-FORWARD CORRECTNESS — {ticker}")
    print("=" * 76)

    returns = load_returns(ticker)
    print(f"  weeks: {len(returns)}  {returns.index[0].date()} .. {returns.index[-1].date()}")
    print(f"  first fit at week {MIN_TRAIN_WEEKS}, refit every {REFIT_EVERY_WEEKS} weeks")

    wf = walk_forward(returns)
    ok = wf[wf.converged].copy()

    print()
    print("1. REGIME LABEL STABILITY (a flip inverts the signal)")
    labels = ok.hv_regime.astype(int)
    flips = int((labels.diff().fillna(0) != 0).sum())
    print(f"   high-variance regime index by refit: {sorted(labels.unique().tolist())}")
    print(f"   label flips across {len(labels)} refits: {flips}")
    if flips:
        f = ok.loc[labels.diff().fillna(0) != 0, "refit_end"]
        print(f"   flip dates: {[str(d.date()) for d in f][:8]}")
        print("   *** post-hoc relabelling is doing real work every refit ***")

    print()
    print("2. CONVERGENCE")
    print(f"   converged {len(ok)}/{len(wf)} refits ({len(ok)/len(wf):.1%})")

    print()
    print("3. LIVE SIGNAL vs LATER REVISION (the usability question)")
    live = pd.concat([pd.Series(r.live_probs, index=r.live_index)
                      for r in ok.itertuples()])
    final_params = ok.iloc[-1]
    final = pd.Series(
        filter_with(returns, np.asarray(
            [final_params[n] for n in
             ["p[0->0]", "p[1->0]", "const[0]", "const[1]", "sigma2[0]", "sigma2[1]"]]
        ))[:, int(final_params.hv_regime)], index=returns.index)
    common = live.index.intersection(final.index)
    d = (live.loc[common] - final.loc[common]).abs()
    print(f"   weeks with a live estimate: {len(common)}")
    print(f"   |live - latest-params| : mean {d.mean():.4f}  median {d.median():.4f}  "
          f"p95 {d.quantile(0.95):.4f}  max {d.max():.4f}")

    def state(x):
        return (np.asarray(x) > STATE_THRESHOLD).astype(int)

    sl, sf = state(live.loc[common]), state(final.loc[common])
    print(f"   weeks whose STATE flips under revision (at {STATE_THRESHOLD}): "
          f"{int((sl != sf).sum())} ({(sl != sf).mean():.1%})")

    print()
    print("4. LIVE vs FULL-SAMPLE FIT (what the leaky version would have shown)")
    _, fs_res, fs_jr = ms.fit_markov_switching(returns)
    fs = pd.Series(filter_with(returns, np.asarray(fs_res.params, dtype=float))[:, fs_jr],
                   index=returns.index)
    d2 = (live.loc[common] - fs.loc[common]).abs()
    print(f"   |live - full-sample| : mean {d2.mean():.4f}  p95 {d2.quantile(0.95):.4f}  "
          f"max {d2.max():.4f}")
    s2 = state(fs.loc[common])
    print(f"   weeks whose STATE differs from the full-sample version: "
          f"{int((sl != s2).sum())} ({(sl != s2).mean():.1%})")
    print(f"   mean live {live.loc[common].mean():.4f} vs full-sample "
          f"{fs.loc[common].mean():.4f}")

    print()
    print("5. PARAMETER PATHS (burn-in and drift)")
    pnames = ["p[0->0]", "p[1->0]", "const[0]", "const[1]", "sigma2[0]", "sigma2[1]"]
    print(f"   {'param':12s} {'first':>12s} {'last':>12s} {'min':>12s} {'max':>12s} "
          f"{'last-half sd':>13s}")
    half = len(ok) // 2
    for p in pnames:
        v = ok[p].astype(float)
        print(f"   {p:12s} {v.iloc[0]:12.6f} {v.iloc[-1]:12.6f} {v.min():12.6f} "
              f"{v.max():12.6f} {v.iloc[half:].std():13.6f}")

    out = DATA_DIR / f"walkforward_{ticker.lower()}.csv"
    ok[["refit_end", "n_obs", "hv_regime", "llf", *pnames]].to_csv(out, index=False)
    print(f"\n   parameter path written to {out.relative_to(Path(__file__).parent)}")


def main() -> None:
    args = sys.argv[1:]
    density = bool(args) and args[0].lower() == "density"
    tickers = [t.upper() for t in (args[1:] if density else args)] or list(TICKERS)
    for ticker in tickers:
        (report_density if density else report)(ticker)
        print()


if __name__ == "__main__":
    main()
