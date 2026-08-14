"""D3 / protocol 5.5: does the model carry downside-risk information beyond VIX?

The cheapest decisive test in the protocol, and the one that was scheduled last.
VIX is free, forward-looking, aligned 1750/1750 weeks, and is the market's own
estimate of the quantity the model estimates -- without the model's detection
lag, because it prices anticipation rather than reacting to realized returns.
If the model adds nothing to it, no amount of specification work matters.

    RV[t, t+h] = a + b * IV[t] + c * X[t] + e[t]

  RV  forward downside semi-volatility, sqrt(SUM min(r,0)^2) over h weeks
  IV  log VIX at the same information time, rescaled to horizon-matched vol
  X   the model's own stated downside risk, -ES(0.05), walk-forward vintage

D3 reads c. c ~ 0 means no capital is committed and the overlay should be built
on VIX directly.

--- protocol 0 stub, fixed before the run -------------------------------------

1. CLAIM TUPLE   weekly * h=4 * forward downside semivariance * SPY, 2003-2026
                 walk-forward OOS. h=13 is a sensitivity DECLARED HERE, not a
                 second primary. No claim outside this tuple.

2. PREDICTION    Genuinely uncertain, which is why it runs. VIX subsumes most
                 realized-vol predictors in the published literature
                 (Christensen-Prabhala; Blair, Poon & Taylor), so the honest
                 prior is c small. But those regress SYMMETRIC realized vol,
                 and X here is a downside measure from a switching mean --
                 the one place an increment is plausible.

3. LITERATURE    Sec 5.5's three papers are [UNREAD] and paywalled. They bear on
                 the interpretation of a null, not on whether this regression is
                 correctly specified. Recorded, not treated as a block --
                 blocking a built one-afternoon test on paywalled 1998 journal
                 access is how the horizon program deadlocked.

4. MECHANISM     VIX is a 30-day risk-neutral expectation and reprices on
                 anticipation. The Hamilton filter conditions on realized
                 returns only and is late by construction. The two therefore
                 carry different information at the SAME information time, and
                 the difference is observable at any h -- unlike the h=1 EWMA
                 comparison, this one is not void by construction.

5. SURPRISE      c significant with the right sign would justify every
                 specification item on the build order. c ~ 0 fires D3 and stops
                 the program. Both outcomes move a decision, so it runs.

-------------------------------------------------------------------------------

ALIGNMENT IS THE WHOLE RISK. In density_{ticker}.csv, row d holds the forecast
FORMED BEFORE r[d] exists -- so its information set ends at d-1. The window it
predicts therefore BEGINS at d and covers r[d]..r[d+h-1], and the matching VIX
observation is the one at d-1, not d. Getting either backwards manufactures a
result. Three variants are run and printed: leaky (window starts at d-1, so it
contains a return already in the filter), true, and stale (starts at d+1). Only
the true and stale readings may be sane; leaky must look better than both.

Overlapping windows are used for DESCRIPTION only (protocol 1.2). Primary
inference is the non-overlapping stride-h subsample.

Levels, not logs: ~10% of 4-week windows contain no negative return at all, so
RV is exactly zero there and log(RV) would drop a tenth of the sample on the
outcome variable. Newey-West is heteroskedasticity-consistent, so levels are
sound; c's significance is the object, not an elasticity.

Run: .venv\\Scripts\\python.exe encompassing.py [SPY]
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

import numpy as np
import pandas as pd

import data_loader as dl
import evaluation as ev

ROOT = Path(__file__).parent
DATA_DIR = ROOT / "data"

PRIMARY_HORIZON = 4
SENSITIVITY_HORIZONS = (13,)
MEASURE_COLUMN = "es_0.05"
WEEKS_PER_YEAR = 52


def load_returns(ticker: str) -> "pd.Series":
    path = DATA_DIR / f"{ticker.lower()}_weekly.csv"
    if not path.exists():
        raise FileNotFoundError(
            f"{path} missing. Run walkforward.py to populate the cache first."
        )
    frame = pd.read_csv(path, index_col=0, parse_dates=True)
    return frame.iloc[:, 0].astype("float64").rename("weekly_log_return")


def load_density(ticker: str) -> "pd.DataFrame":
    path = DATA_DIR / f"density_{ticker.lower()}.csv"
    if not path.exists():
        raise FileNotFoundError(
            f"{path} missing. Run: .venv\\Scripts\\python.exe walkforward.py "
            f"density {ticker}"
        )
    return pd.read_csv(path, index_col=0, parse_dates=True)


def load_log_vix(returns: "pd.Series") -> "pd.Series":
    """Cached so a repeat run is offline. The cache is the aligned series."""
    path = DATA_DIR / "vix_weekly.csv"
    if path.exists():
        vix = pd.read_csv(path, index_col=0, parse_dates=True).iloc[:, 0]
    else:
        vix = dl.download_weekly_vix()
        vix.to_frame().to_csv(path)
    aligned = dl.align_vix_to_returns(vix, returns)
    return dl.to_log_vix(aligned)


def forward_downside_semivol(returns: "pd.Series", horizon: int) -> "pd.Series":
    """sqrt(SUM min(r,0)^2) over the horizon weeks BEGINNING at each row.

    rolling(h).sum() at index i covers i-h+1..i; shifting back by h-1 relabels
    it onto i-h+1, so the value at row j covers j..j+h-1. That is the window a
    forecast whose information set ends at j-1 is predicting.
    """
    squared_downside = np.minimum(returns, 0.0) ** 2
    window = squared_downside.rolling(horizon).sum().shift(-(horizon - 1))
    return np.sqrt(window).rename(f"rv_{horizon}w")


def build_frame(
    returns: "pd.Series",
    density: "pd.DataFrame",
    log_vix: "pd.Series",
    horizon: int,
    rv_offset: int = 0,
) -> "pd.DataFrame":
    """One row per forecast date d, aligned to information time d-1.

    rv_offset shifts the realized window for the adversarial check: 0 is the
    true alignment, -1 leaks a return the filter has already absorbed, +1 is
    harmlessly stale.
    """
    rv = forward_downside_semivol(returns, horizon)
    if rv_offset:
        rv = rv.shift(-rv_offset)

    # X is known at d-1 by construction (the density row is formed before r[d]).
    model_measure = -density[MEASURE_COLUMN].astype("float64")
    # IV must be read at the same information time, so lag it by one week.
    implied = log_vix.shift(1)
    # Horizon-matched vol in return units, so b is readable near 1. A linear
    # rescaling cannot move any p-value.
    implied_scaled = np.exp(implied) / 100.0 * np.sqrt(horizon / WEEKS_PER_YEAR)

    frame = pd.concat(
        [
            rv.rename("rv"),
            implied_scaled.rename("iv"),
            model_measure.rename("x"),
        ],
        axis=1,
    )
    return frame.reindex(density.index).dropna()


def run(frame: "pd.DataFrame", horizon: int, overlapping: bool) -> ev.EncompassingResult:
    if overlapping:
        return ev.encompassing_regression(
            frame["rv"], frame["iv"], frame["x"], horizon=horizon
        )
    stride = frame.iloc[::horizon]
    return ev.encompassing_regression(
        stride["rv"], stride["iv"], stride["x"], horizon=horizon, hac_lags=0
    )


def univariate_r_squared(frame: "pd.DataFrame", column: str, hac_lags: int) -> float:
    import statsmodels.api as sm

    design = sm.add_constant(frame[[column]].to_numpy(), has_constant="add")
    fitted = sm.OLS(frame["rv"].to_numpy(), design).fit(
        cov_type="HAC", cov_kwds={"maxlags": hac_lags}
    )
    return float(fitted.rsquared)


def format_result(label: str, result: ev.EncompassingResult) -> str:
    return (
        f"  {label:<22s} n={result.n:>5d}  "
        f"b_vix={result.beta_implied:+.4f} (p={result.p_implied:.4f})  "
        f"c_model={result.gamma_model:+.4f} (p={result.p_model:.4f})  "
        f"R2={result.r_squared:.4f}"
    )


def report(ticker: str = "SPY") -> None:
    returns = load_returns(ticker)
    density = load_density(ticker)
    log_vix = load_log_vix(returns)

    print(f"D3 / protocol 5.5 -- encompassing regression, {ticker}")
    print(f"weekly * forward downside semi-volatility * X = -{MEASURE_COLUMN}")
    print(f"sample {density.index[0].date()} to {density.index[-1].date()}, "
          f"{len(density)} walk-forward forecasts")

    for horizon in (PRIMARY_HORIZON, *SENSITIVITY_HORIZONS):
        tag = "PRIMARY" if horizon == PRIMARY_HORIZON else "sensitivity (declared)"
        print(f"\n{'=' * 78}\nh = {horizon} weeks   [{tag}]\n{'=' * 78}")

        frame = build_frame(returns, density, log_vix, horizon)

        print("\nnon-overlapping stride-h -- PRIMARY INFERENCE (protocol 1.2)")
        primary = run(frame, horizon, overlapping=False)
        print(format_result("model + vix", primary))

        stride = frame.iloc[::horizon]
        print(f"  {'vix alone':<22s} R2={univariate_r_squared(stride, 'iv', 0):.4f}")
        print(f"  {'model alone':<22s} R2={univariate_r_squared(stride, 'x', 0):.4f}")

        print("\noverlapping + Newey-West -- DESCRIPTION ONLY, not inference")
        print(format_result("model + vix", run(frame, horizon, overlapping=True)))

        print("\nadversarial alignment check -- leaky must beat true and stale")
        for offset, name in ((-1, "leaky (starts d-1)"), (0, "true (starts d)"),
                             (1, "stale (starts d+1)")):
            shifted = build_frame(returns, density, log_vix, horizon, rv_offset=offset)
            print(format_result(name, run(shifted, horizon, overlapping=False)))

        verdict = "FIRES D3" if primary.p_model > 0.05 else "c is significant"
        print(f"\nD3 reads c: p={primary.p_model:.4f} -> {verdict}")

    out = build_frame(returns, density, log_vix, PRIMARY_HORIZON)
    out.to_csv(DATA_DIR / f"encompassing_{ticker.lower()}.csv")
    print(f"\nwrote data/encompassing_{ticker.lower()}.csv ({len(out)} rows)")


def main() -> None:
    report(sys.argv[1].upper() if len(sys.argv) > 1 else "SPY")


if __name__ == "__main__":
    main()
