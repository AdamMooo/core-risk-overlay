from __future__ import annotations

import numpy as np
import pandas as pd

# Shu, Yu & Mulvey (2024), Table 1: three features from the excess return series.
DOWNSIDE_HALFLIFE = 10
SORTINO_HALFLIFES = (20, 60)


def downside_deviation(returns: pd.Series, halflife: int) -> pd.Series:
    negative_part = returns.clip(upper=0.0)
    return (negative_part**2).ewm(halflife=halflife, adjust=True).mean() ** 0.5


def sortino_ratio(returns: pd.Series, halflife: int) -> pd.Series:
    mean = returns.ewm(halflife=halflife, adjust=True).mean()
    dd = downside_deviation(returns, halflife)
    # A window with no negative return has dd = 0; the ratio is undefined there
    # rather than infinite, and the warm-up drops it.
    return mean / dd.replace(0.0, np.nan)


def build_features(excess_returns: pd.Series) -> pd.DataFrame:
    features = {
        f"dd_{DOWNSIDE_HALFLIFE}": downside_deviation(excess_returns, DOWNSIDE_HALFLIFE),
    }
    for halflife in SORTINO_HALFLIFES:
        features[f"sortino_{halflife}"] = sortino_ratio(excess_returns, halflife)
    return pd.DataFrame(features).astype("float64").dropna()


DOWNSIDE_FEATURE = 0
