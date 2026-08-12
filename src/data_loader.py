from __future__ import annotations

from typing import Final


DEFAULT_TICKER: Final[str] = "SPY"
DEFAULT_PRICE_COLUMN: Final[str] = "Close"
_DEPS: tuple[object, object, object] | None = None


def _require_dependencies():
    """Load and cache optional third-party dependencies for the data loader."""
    global _DEPS

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


def download_weekly_prices(
    ticker: str = DEFAULT_TICKER,
    start: str | None = None,
    end: str | None = None,
    price_column: str = DEFAULT_PRICE_COLUMN,
) -> "pd.Series":
    _, pd, yf = _require_dependencies()
    data = yf.download(
        ticker,
        start=start,
        end=end,
        interval="1wk",
        auto_adjust=True,
        progress=False,
    )

    if data.empty:
        raise ValueError(f"No weekly price data returned for ticker '{ticker}'.")

    if isinstance(data.columns, pd.MultiIndex):
        ticker_level = next(
            (
                level
                for level in range(data.columns.nlevels)
                if ticker in data.columns.get_level_values(level)
            ),
            None,
        )
        if ticker_level is None:
            available_columns = ", ".join(map(str, data.columns))
            raise ValueError(
                f"Ticker '{ticker}' not found in downloaded data. "
                f"Available columns: {available_columns}"
            )
        data = data.xs(ticker, axis=1, level=ticker_level)

    if price_column not in data.columns:
        available_columns = ", ".join(map(str, data.columns))
        raise ValueError(
            f"Column '{price_column}' not found for ticker '{ticker}'. "
            f"Available columns: {available_columns}"
        )

    prices = data[price_column].copy()
    prices = prices.rename("weekly_close").sort_index()
    prices.index = pd.to_datetime(prices.index)
    prices = prices.dropna().astype("float64")

    if prices.empty:
        raise ValueError(f"No valid weekly closing prices available for ticker '{ticker}'.")

    return prices


def compute_weekly_log_returns(prices: "pd.Series") -> "pd.Series":
    np, _, _ = _require_dependencies()
    if prices.empty:
        raise ValueError("Price series is empty.")

    if (prices <= 0).any():
        raise ValueError("Weekly prices must be strictly positive to compute log returns.")

    log_returns = np.log(prices / prices.shift(1))
    log_returns = log_returns.replace([np.inf, -np.inf], np.nan).dropna()
    log_returns = log_returns.rename("weekly_log_return").astype("float64")

    if log_returns.empty:
        raise ValueError("Log-return series is empty after cleaning.")

    return log_returns


def load_weekly_log_returns(
    ticker: str = DEFAULT_TICKER,
    start: str | None = None,
    end: str | None = None,
    price_column: str = DEFAULT_PRICE_COLUMN,
) -> "pd.Series":
    prices = download_weekly_prices(
        ticker=ticker,
        start=start,
        end=end,
        price_column=price_column,
    )
    return compute_weekly_log_returns(prices)
