"""Does the model's MEMORY match the data's? Exponential against power law.

The first test in this repo that scores the model on what it actually claims to
know. Every previous test -- including the D3 encompassing regression -- collapsed
the model to a LEVEL (a VaR or ES scalar) and compared it to VIX's level. VIX is a
point-in-time price with no memory structure, so a level-vs-level test structurally
cannot see the model's content. That content is in P.

DEDUCTIVE, not fitted. For a two-state switching-variance model with regime
variances v[j], stationary weights pi, and second eigenvalue lam = p00 + p11 - 1:

    Cov(r[t]^2, r[t+k]^2) = pi_0 * pi_1 * (v_0 - v_1)^2 * lam^k        for k >= 1
    Var(r[t]^2)           = 3*(pi_0*v_0^2 + pi_1*v_1^2) - (pi_0*v_0 + pi_1*v_1)^2

so

    ACF_model(k) = pi_0*pi_1*(v_0-v_1)^2 * lam^k / Var(r^2)

The lam^k is the entire point. A finite-state Markov chain's squared-return
autocorrelation decays GEOMETRICALLY -- for any k, any number of regimes, any
parameters. That is algebra. Volatility in real markets decays as a POWER LAW,
k^(2H-2). Those are different shapes, not different speeds, and no amount of
tuning P turns one into the other.

Known since Ryden, Terasvirta & Asbrink (1998): a hidden Markov model reproduces
most stylized facts of daily returns and fails specifically on the slow decay of
squared-return autocorrelation. Protocol 11 lists it as [UNREAD] and flags it as
the paper that would have prevented a wasted run. This script is that paper's
finding, measured on this repo's own fitted parameters.

THE DISCRIMINATOR is which functional form fits the EMPIRICAL acf better:

    log ACF ~ k          straight line  =>  exponential (what the model can do)
    log ACF ~ log k      straight line  =>  power law   (what the model cannot)

Reported as two R-squared values on the same lags. Also reported: the implied
Hurst exponent H = 1 + slope/2 from the power-law fit, and sum of ACF over 104
lags -- finite for geometric decay, divergent for long memory, which is the formal
statement of the difference.

Approximation stated: the closed form assumes a common within-regime mean. The
fitted switching means (~0.3% and ~0.07% weekly) are an order of magnitude below
the regime sigmas (1.4% and 2.8%), so their contribution to the squared-return
autocovariance is negligible. Returns are demeaned empirically before the ACF.

Run: .venv\\Scripts\\python.exe memory_diagnostic.py [SPY]
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import acf

ROOT = Path(__file__).parent
DATA_DIR = ROOT / "data"
MAX_LAG = 104
FIT_LAGS = 52
REPORT_LAGS = (1, 2, 4, 8, 13, 26, 52, 104)


def load_vintages(ticker: str) -> pd.DataFrame:
    path = DATA_DIR / f"walkforward_{ticker.lower()}.csv"
    if not path.exists():
        raise FileNotFoundError(f"{path} missing. Run walkforward.py {ticker} first.")
    return pd.read_csv(path, index_col=0, parse_dates=True)


def load_returns(ticker: str) -> pd.Series:
    path = DATA_DIR / f"{ticker.lower()}_weekly.csv"
    return pd.read_csv(path, index_col=0, parse_dates=True).iloc[:, 0].astype("float64")


def model_acf(p00: float, p10: float, v0: float, v1: float, lags) -> np.ndarray:
    """Closed-form squared-return ACF. Label-invariant by construction."""
    p01 = 1.0 - p00
    denom = p01 + p10
    pi0 = p10 / denom
    pi1 = p01 / denom
    lam = p00 + (1.0 - p10) - 1.0

    numerator = pi0 * pi1 * (v0 - v1) ** 2
    variance = 3.0 * (pi0 * v0**2 + pi1 * v1**2) - (pi0 * v0 + pi1 * v1) ** 2
    return numerator * lam ** np.asarray(lags, dtype="float64") / variance, lam


def fit_shape(lags, values):
    """R^2 of log(acf) on lag (exponential) and on log(lag) (power law)."""
    mask = values > 0
    x_lin, y = np.asarray(lags)[mask], np.log(values[mask])
    if len(y) < 5:
        return float("nan"), float("nan"), float("nan")

    def r2_and_slope(x):
        slope, intercept = np.polyfit(x, y, 1)
        predicted = slope * x + intercept
        ss_res = ((y - predicted) ** 2).sum()
        ss_tot = ((y - y.mean()) ** 2).sum()
        return 1.0 - ss_res / ss_tot, slope

    r2_exp, _ = r2_and_slope(x_lin)
    r2_pow, slope_pow = r2_and_slope(np.log(x_lin))
    return r2_exp, r2_pow, slope_pow


def report(ticker: str = "SPY") -> None:
    vintages = load_vintages(ticker)
    returns = load_returns(ticker)
    squared = ((returns - returns.mean()) ** 2).to_numpy()

    empirical = acf(squared, nlags=MAX_LAG, fft=True)[1:]
    lags = np.arange(1, MAX_LAG + 1)
    band = 1.96 / np.sqrt(len(squared))

    lam_all = vintages["p[0->0]"] - vintages["p[1->0]"]
    median_idx = (lam_all - lam_all.median()).abs().idxmin()
    row = vintages.loc[median_idx]
    implied, lam = model_acf(
        row["p[0->0]"], row["p[1->0]"], row["sigma2[0]"], row["sigma2[1]"], lags
    )

    print(f"MEMORY DIAGNOSTIC -- {ticker}, {len(returns)} weekly returns "
          f"{returns.index[0].date()} to {returns.index[-1].date()}")
    print(f"median vintage {median_idx.date()}: lambda2 = {lam:.4f}, "
          f"half-life {np.log(0.5)/np.log(lam):.1f} weeks")
    print(f"white-noise band +/- {band:.4f}\n")

    print("  lag   empirical   model    ratio   emp sig?")
    for lag in REPORT_LAGS:
        e, m = empirical[lag - 1], implied[lag - 1]
        ratio = e / m if m > 1e-12 else float("inf")
        print(f"  {lag:4d}    {e:+7.4f}  {m:+7.4f}  {ratio:7.1f}"
              f"     {'yes' if abs(e) > band else 'no'}")

    r2_exp, r2_pow, slope = fit_shape(lags[:FIT_LAGS], empirical[:FIT_LAGS])
    hurst = 1.0 + slope / 2.0
    print(f"\nSHAPE OF THE EMPIRICAL DECAY, lags 1-{FIT_LAGS}")
    print(f"  exponential  log(acf) ~ lag        R2 = {r2_exp:.4f}")
    print(f"  power law    log(acf) ~ log(lag)   R2 = {r2_pow:.4f}   "
          f"slope {slope:+.3f} -> H = {hurst:.3f}")
    better = "POWER LAW" if r2_pow > r2_exp else "EXPONENTIAL"
    print(f"  -> empirical decay is better described as {better}")

    tail_e = empirical[:MAX_LAG].sum()
    tail_m = implied[:MAX_LAG].sum()
    print(f"\nACCUMULATED MEMORY, sum of acf over {MAX_LAG} lags")
    print(f"  empirical {tail_e:6.2f}   model {tail_m:6.2f}   "
          f"model retains {tail_m/tail_e:.1%} of the data's memory")

    lam_lo, lam_hi = lam_all.quantile(0.10), lam_all.quantile(0.90)
    print(f"\nvintage envelope: lambda2 in [{lam_lo:.4f}, {lam_hi:.4f}] across "
          f"{len(lam_all)} refits")
    print(f"  even at lambda2 = {lam_hi:.4f} the decay is still geometric --")
    print(f"  the shape is fixed by the model class, not by the parameters.")


def load_daily_returns(ticker: str) -> pd.Series:
    """Cached so repeat runs are offline."""
    import data_loader as dl

    path = DATA_DIR / f"{ticker.lower()}_daily.csv"
    if path.exists():
        return pd.read_csv(path, index_col=0, parse_dates=True).iloc[:, 0].astype("float64")

    returns = dl.load_daily_log_returns(ticker=ticker, start=dl.DEFAULT_START)
    returns.to_frame().to_csv(path)
    return returns


def report_daily(ticker: str = "SPY", max_lag: int = 250) -> None:
    """The shape question, at the frequency that can resolve it.

    No fitted model is needed. A two-state Markov chain's squared-return ACF is
    EXACTLY A * lam^k -- so the best-fitting single exponential is an upper
    bound on how well ANY two-state Markov model could match this memory, the
    same way the clairvoyant program bounds any trigger. Fit both shapes to the
    empirical daily ACF and let the residuals decide.
    """
    returns = load_daily_returns(ticker)
    squared = ((returns - returns.mean()) ** 2).to_numpy()
    n = len(squared)
    band = 1.96 / np.sqrt(n)

    empirical = acf(squared, nlags=max_lag, fft=True)[1:]
    lags = np.arange(1, max_lag + 1)

    print(f"MEMORY DIAGNOSTIC (DAILY) -- {ticker}, {n} daily returns "
          f"{returns.index[0].date()} to {returns.index[-1].date()}")
    print(f"white-noise band +/- {band:.4f}   (weekly was +/-0.0469 at n=1750)\n")

    significant = lags[np.abs(empirical) > band]
    last_sig = significant.max() if len(significant) else 0
    frac = (np.abs(empirical) > band).mean()
    print(f"  empirical ACF exceeds the band out to lag {last_sig} "
          f"({frac:.0%} of lags 1-{max_lag} significant)")
    print(f"  weekly equivalent of lag {last_sig} is {last_sig/5:.0f} weeks\n")

    print("  lag   empirical   sig?")
    for lag in (1, 5, 10, 21, 63, 126, 250):
        if lag <= max_lag:
            e = empirical[lag - 1]
            print(f"  {lag:4d}    {e:+7.4f}    {'yes' if abs(e) > band else 'no'}")

    r2_exp, r2_pow, slope = fit_shape(lags, empirical)
    hurst = 1.0 + slope / 2.0
    print(f"\nSHAPE OF THE DECAY, lags 1-{max_lag}, n={n}")
    print(f"  best exponential   log(acf) ~ lag       R2 = {r2_exp:.4f}"
          f"   <- ceiling for ANY 2-state Markov chain")
    print(f"  best power law     log(acf) ~ log(lag)  R2 = {r2_pow:.4f}"
          f"   slope {slope:+.3f} -> H = {hurst:.3f}")
    gap = r2_pow - r2_exp
    winner = "POWER LAW" if gap > 0 else "EXPONENTIAL"
    print(f"  -> {winner} by {abs(gap):.4f} of R2")

    for window in (63, 126, 250):
        if window <= max_lag:
            e_r2, p_r2, _ = fit_shape(lags[:window], empirical[:window])
            print(f"     lags 1-{window:3d}: exponential {e_r2:.4f}  "
                  f"power law {p_r2:.4f}  ({'power' if p_r2 > e_r2 else 'exp'})")

    print(f"\nACCUMULATED MEMORY, sum of acf over {max_lag} lags")
    print(f"  empirical {empirical.sum():.2f}")
    print(f"  a geometric decay matching lag 1 ({empirical[0]:.4f}) with the "
          f"weekly-implied\n  half-life would sum to far less -- that gap is the "
          f"memory a single\n  timescale cannot hold.")


def main() -> None:
    args = [a for a in sys.argv[1:] if a != "--daily"]
    ticker = args[0].upper() if args else "SPY"
    if "--daily" in sys.argv:
        report_daily(ticker)
    else:
        report(ticker)


if __name__ == "__main__":
    main()
