"""C1 data pull — pins the three FRED credit series into data/ cache.

Gated by STUB-C1-CREDIT-SATURATION. Does NOT run any regression; only fetches and caches.
Re-running is idempotent (cached_series skips the download if the file exists).

After this runs, re-run src/manifest.py --write to pin sha256 hashes.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.caching import cached_series


REPO_ROOT = Path(__file__).resolve().parent
CACHE = REPO_ROOT / "data"


FRED_SERIES = {
    "BAMLH0A0HYM2": "ICE BofA US High Yield Index OAS, daily, percent",
    "BAMLC0A0CM": "ICE BofA US Corporate Index OAS, daily, percent",
}


def _fred_csv(series_id: str) -> pd.Series:
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}"
    raw = pd.read_csv(url)
    raw.columns = ["date", "value"]
    raw["date"] = pd.to_datetime(raw["date"])
    raw["value"] = pd.to_numeric(raw["value"], errors="coerce")
    return raw.dropna().set_index("date")["value"].rename(series_id)


def load_fred_series(series_id: str) -> pd.Series:
    return cached_series(CACHE, f"c1_{series_id.lower()}.csv", lambda: _fred_csv(series_id))


def main() -> None:
    for series_id, label in FRED_SERIES.items():
        print(f"Fetching {series_id} ({label}) ...", flush=True)
        s = load_fred_series(series_id)
        print(f"  {series_id}: {len(s)} rows, {s.index.min().date()} to {s.index.max().date()}")


if __name__ == "__main__":
    main()
