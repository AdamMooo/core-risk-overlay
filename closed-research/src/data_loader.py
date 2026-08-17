from __future__ import annotations

from threading import Lock
from typing import Final


DEFAULT_TICKER: Final[str] = "SPY"
DEFAULT_VIX_TICKER: Final[str] = "^VIX"
DEFAULT_PRICE_COLUMN: Final[str] = "Close"
DEFAULT_START: Final[str] = "1990-01-01"
WEEKLY_RULE: Final[str] = "W-FRI"
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
            import yfinance as yf
        except ModuleNotFoundError as exc:
            raise ModuleNotFoundError(
                "data_loader.py requires numpy, pandas, and yfinance to be installed."
            ) from exc

        _DEPS = (np, pd, yf)

    return _DEPS


def _download_daily_closes(
    ticker: str = DEFAULT_TICKER,
    start: str | None = None,
    end: str | None = None,
    price_column: str = DEFAULT_PRICE_COLUMN,
) -> "pd.Series":
    """Download and clean the daily close series. Shared by both frequencies.

    `start` defaults rather than passing None through: yfinance silently
    returns only a recent window when no start is given, which looks like valid
    data and is not.
    """
    _, pd, yf = _require_dependencies()
    data = yf.download(
        ticker,
        start=start or DEFAULT_START,
        end=end,
        interval="1d",
        auto_adjust=True,
        progress=False,
    )

    if data.empty:
        raise ValueError(f"No daily price data returned for ticker '{ticker}'.")

    if isinstance(data.columns, pd.MultiIndex):
        matched_data = None

        for level in range(data.columns.nlevels):
            if ticker not in data.columns.get_level_values(level):
                continue

            candidate = data.xs(ticker, axis=1, level=level)
            if isinstance(candidate, pd.Series):
                candidate = candidate.to_frame()

            if isinstance(candidate, pd.DataFrame) and price_column in candidate.columns:
                matched_data = candidate
                break

        if matched_data is None:
            available_columns = ", ".join(map(str, data.columns))
            raise ValueError(
                f"Ticker '{ticker}' not found in downloaded data. "
                f"Available columns: {available_columns}"
            )

        data = matched_data

    if price_column not in data.columns:
        available_columns = ", ".join(map(str, data.columns))
        raise ValueError(
            f"Column '{price_column}' not found for ticker '{ticker}'. "
            f"Available columns: {available_columns}"
        )

    prices = data[price_column].copy()
    prices.index = pd.to_datetime(prices.index)
    prices = prices.sort_index().dropna().astype("float64")

    if prices.empty:
        raise ValueError(f"No valid daily closing prices available for ticker '{ticker}'.")

    return prices.rename("daily_close")


def download_daily_prices(
    ticker: str = DEFAULT_TICKER,
    start: str | None = None,
    end: str | None = None,
    price_column: str = DEFAULT_PRICE_COLUMN,
) -> "pd.Series":
    """Daily closes on the trading-day calendar. No fills, no synthetic bars.

    The unit of observation protocol 1.3 specifies: ~8,400 SPY observations
    rather than 1,750. Volatility memory is a daily phenomenon and the weekly
    series lacks the resolution to measure it -- at n=1750 the white-noise ACF
    band is +/-0.047 and the empirical squared-return ACF falls inside it by
    lag 8, so decay SHAPE cannot be identified there at all.
    """
    return _download_daily_closes(ticker, start, end, price_column)


def download_weekly_prices(
    ticker: str = DEFAULT_TICKER,
    start: str | None = None,
    end: str | None = None,
    price_column: str = DEFAULT_PRICE_COLUMN,
) -> "pd.Series":
    """Daily closes resampled onto a fixed weekly grid.

    Deliberately does NOT use yfinance's interval="1wk". That anchors weekly
    bars on each series' own first observation, which makes the grid depend on
    the request: SPY from 1993-01-01 comes back Monday-anchored, SPY from
    2010-01-01 comes back Friday-anchored, and the two share zero bars. Two
    tickers with different inception dates never align at all. Resampling daily
    closes onto an explicit W-FRI grid is start-date invariant and consistent
    across tickers, and W-FRI is the actual trading week the strategy runs on.
    """
    _, pd, _ = _require_dependencies()
    prices = _download_daily_closes(ticker, start, end, price_column)
    prices = prices.resample(WEEKLY_RULE).last().dropna().rename("weekly_close")

    if prices.empty:
        raise ValueError(f"No valid weekly closing prices available for ticker '{ticker}'.")

    return prices


def compute_weekly_log_returns(prices: "pd.Series") -> "pd.Series":
    """Compute weekly log returns, which are one observation shorter than the price series."""
    np, _, _ = _require_dependencies()
    prices = prices.dropna().astype("float64")

    if prices.empty:
        raise ValueError("Price series is empty.")

    if len(prices) < 2:
        raise ValueError("At least two weekly prices are required to compute log returns.")

    if (not np.isfinite(prices).all()) or (prices <= 0).any():
        raise ValueError("Weekly prices must be finite and strictly positive.")

    log_returns = np.log(prices / prices.shift(1)).dropna()
    log_returns = log_returns.rename("weekly_log_return").astype("float64")

    if log_returns.empty:
        raise ValueError("Log-return series is empty after cleaning.")

    return log_returns


def compute_daily_log_returns(prices: "pd.Series") -> "pd.Series":
    """Daily log returns. Same validation as the weekly path, different label.

    Gaps across weekends and holidays are NOT filled: the return spanning a
    three-day weekend is a genuine three-calendar-day return and inventing a
    Sunday bar would fabricate an observation. Trading-day indexing is the
    calendar protocol 2 specifies.
    """
    returns = compute_weekly_log_returns(prices)
    return returns.rename("daily_log_return")


def load_weekly_log_returns(
    ticker: str = DEFAULT_TICKER,
    start: str | None = None,
    end: str | None = None,
    price_column: str = DEFAULT_PRICE_COLUMN,
) -> "pd.Series":
    """Return weekly log returns ready for statsmodels MarkovRegression input."""
    prices = download_weekly_prices(
        ticker=ticker,
        start=start,
        end=end,
        price_column=price_column,
    )
    return compute_weekly_log_returns(prices)


def load_daily_log_returns(
    ticker: str = DEFAULT_TICKER,
    start: str | None = None,
    end: str | None = None,
    price_column: str = DEFAULT_PRICE_COLUMN,
) -> "pd.Series":
    """Return daily log returns. ~8,400 SPY observations rather than 1,750."""
    prices = download_daily_prices(
        ticker=ticker,
        start=start,
        end=end,
        price_column=price_column,
    )
    return compute_daily_log_returns(prices)


def download_daily_vix(
    start: str | None = None,
    end: str | None = None,
) -> "pd.Series":
    """Daily VIX close as an annualized volatility in percent."""
    return download_daily_prices(ticker=DEFAULT_VIX_TICKER, start=start, end=end).rename(
        "daily_vix"
    )


def download_weekly_vix(
    start: str | None = None,
    end: str | None = None,
) -> "pd.Series":
    """Download the weekly VIX close as an annualized volatility in percent."""
    vix = download_weekly_prices(ticker=DEFAULT_VIX_TICKER, start=start, end=end)
    return vix.rename("weekly_vix")


def align_vix_to_returns(vix: "pd.Series", returns: "pd.Series") -> "pd.Series":
    """Align VIX onto a weekly return index by exact date match.

    Deliberately does NOT forward-fill. Both series are resampled onto the same
    explicit WEEKLY_RULE grid and every SPY week from 1993 has an exact VIX bar,
    so a fill would never be a legitimate repair -- it would only mask a data
    defect by silently carrying a stale quote.
    """
    np, pd, _ = _require_dependencies()

    vix = pd.Series(vix, copy=True).dropna().astype("float64")
    aligned = vix.reindex(returns.index)

    missing = aligned.index[aligned.isna()]
    if len(missing):
        raise ValueError(
            f"{len(missing)} return week(s) have no matching VIX observation "
            f"(first: {missing[0].date()}, last: {missing[-1].date()}). "
            "Refusing to forward-fill; investigate the source data instead."
        )

    if (aligned <= 0).any():
        raise ValueError("VIX values must be strictly positive.")

    aligned.name = "weekly_vix"
    return aligned


def to_log_vix(vix: "pd.Series") -> "pd.Series":
    """Convert VIX to logs, which is the appropriate modelling scale.

    Measured on real weekly data 1993-2026: raw VIX has skew 2.22 and excess
    kurtosis 8.57 (Jarque-Bera 6789); log(VIX) has skew 0.68 and excess kurtosis
    0.47 (Jarque-Bera 150). Both reject exact normality, but the log scale is
    dramatically closer and is the standard treatment in the literature.
    """
    np, _, _ = _require_dependencies()

    vix = vix.dropna().astype("float64")
    if (vix <= 0).any():
        raise ValueError("VIX values must be strictly positive to take logs.")

    log_vix = np.log(vix)
    log_vix.name = "weekly_log_vix"
    return log_vix
