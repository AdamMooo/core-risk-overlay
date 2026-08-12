from __future__ import annotations

from typing import Final

import numpy as np
import pandas as pd
import yfinance as yf


DEFAULT_TICKER: Final[str] = "SPY"
DEFAULT_PRICE_COLUMN: Final[str] = "Close"


def download_weekly_prices(
    ticker: str = DEFAULT_TICKER,
    start: str | None = None,
    end: str | None = None,
    price_column: str = DEFAULT_PRICE_COLUMN,
) -> pd.Series:
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


def compute_weekly_log_returns(prices: pd.Series) -> pd.Series:
    if prices.empty:
        raise ValueError("Price series is empty.")

    if (prices <= 0).any():
        raise ValueError("Weekly prices must be strictly positive to compute log returns.")

    log_returns = np.log(prices).diff()
    log_returns = log_returns.replace([np.inf, -np.inf], np.nan).dropna()
    log_returns = log_returns.rename("weekly_log_return").astype("float64")
    log_returns.index = pd.to_datetime(log_returns.index)

    if log_returns.empty:
        raise ValueError("Log-return series is empty after cleaning.")

    return log_returns


def load_weekly_log_returns(
    ticker: str = DEFAULT_TICKER,
    start: str | None = None,
    end: str | None = None,
    price_column: str = DEFAULT_PRICE_COLUMN,
) -> pd.Series:
    prices = download_weekly_prices(
        ticker=ticker,
        start=start,
        end=end,
        price_column=price_column,
    )
    return compute_weekly_log_returns(prices)

