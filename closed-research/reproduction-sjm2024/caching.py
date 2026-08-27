"""Disk cache for a single-column series, shared by repro_sjm2024.py and screen0.py."""
from __future__ import annotations

from pathlib import Path

import pandas as pd


def cached_series(cache_dir: Path, name: str, build) -> pd.Series:
    cache_dir.mkdir(exist_ok=True)
    path = cache_dir / name
    if path.exists():
        frame = pd.read_csv(path, index_col=0, parse_dates=True)
        return frame.iloc[:, 0]
    series = build()
    series.to_frame().to_csv(path)
    return series
