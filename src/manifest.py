"""The data cache's manifest: what is on disk, and what produced it.

`data/` is gitignored -- the caches are large, and two of them are derived
artifacts from long refit loops rather than downloads. So "the archived results
reproduce" was an assertion resting on files git does not track. This module
turns it into something checkable: the manifest IS tracked, so a re-download
that differs from what produced a published number is detected rather than
silently used.

    .venv\\Scripts\\python.exe src/manifest.py --write    regenerate
    .venv\\Scripts\\python.exe src/manifest.py            verify

`verify` is also called from checks.py. MISSING is reported, never failed: the
manifest cannot conjure a cache, and a fresh clone legitimately has none. A file
that is PRESENT and does not match is a failure, because that is drift.
"""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
MANIFEST = DATA_DIR / "MANIFEST.md"

# What produced each file. Written by hand because provenance is not derivable
# from the bytes, and a manifest that cannot say where a file came from records
# the wrong thing.
PROVENANCE = {
    "spy_daily.csv": "src/data_loader.py -- yfinance daily closes, auto_adjust",
    "spy_weekly.csv": "src/data_loader.py -- daily resampled to an explicit W-FRI grid",
    "qqq_weekly.csv": "src/data_loader.py -- same",
    "vix_weekly.csv": "src/data_loader.py -- ^VIX on the same W-FRI grid",
    "panel_daily.csv": "closed-research/systemic_state.py -- SPY/QQQ/EFA/EEM daily panel",
    "density_spy.csv": "DERIVED. closed-research/walkforward.py -- quarterly refit walk-forward "
                       "density vintages. Expensive to regenerate; D3 and F2 are computed from it",
    "density_qqq.csv": "DERIVED. closed-research/walkforward.py -- same, QQQ",
    "density_spy_k3.csv": "DERIVED. closed-research/walkforward.py at k=3. Sensitivity only",
    "k3.log": "run log for density_spy_k3.csv. Not an input to any result",
    "encompassing_spy.csv": "DERIVED. closed-research/encompassing.py -- D3's regression frame",
    "walkforward_spy.csv": "DERIVED. closed-research/walkforward.py -- state vintages",
    "walkforward_qqq.csv": "DERIVED. closed-research/walkforward.py -- same, QQQ",
    "gspc_e4_weekly.csv": "closed-research/intervention/anchoring.py -- ^GSPC 1927+, E4",
    "n225_e4_weekly.csv": "closed-research/intervention/anchoring.py -- ^N225, E4",
    "ftse_e4_weekly.csv": "closed-research/intervention/anchoring.py -- ^FTSE, E4",
    "gdaxi_e4_weekly.csv": "closed-research/intervention/anchoring.py -- ^GDAXI, E4",
    "sjm_gspc_daily.csv": "repro_sjm2024.py -- ^GSPC daily closes, price index (no dividends: declared deviation D2)",
    "sjm_qqq_daily.csv": "repro_sjm2024.py -- QQQ daily closes, auto_adjust total return",
    "sjm_dtb3.csv": "repro_sjm2024.py -- FRED DTB3 3-month T-bill, the risk-free leg and the excess-return basis",
    "ofr_fsi.csv": "screen0.py -- OFR Financial Stress Index daily CSV from financialresearch.gov",
    "vix3m_cboe.csv": "screen0.py -- CBOE VIX3M daily closes from cdn.cboe.com (history begins 2009-09-18)",
    "s0_vix_daily.csv": "screen0.py -- ^VIX daily closes via src/data_loader.py",
    "s0_spy_daily.csv": "screen0.py -- SPY daily closes (prices; distinct from spy_daily.csv, which holds log returns)",
    "s0_efa_daily.csv": "screen0.py -- EFA daily closes, turbulence panel",
    "s0_tlt_daily.csv": "screen0.py -- TLT daily closes, turbulence panel",
    "s0_gld_daily.csv": "screen0.py -- GLD daily closes, turbulence panel",
    "deeptail_mc.csv": "DERIVED. deeptail_mc.py -- one row per simulated path: the deep-tail and exposure gaps between the jump model and each band under N1/N2/N3. ~2h of refit loops to regenerate",
    "deeptail_nulls.json": "DERIVED. deeptail_mc.py -- the fitted GARCH(1,1)-t and Markov-switching null parameters, cached so a rerun does not repeat the MLE",
    "infer_nets_gspc.csv": "DERIVED. inference.py -- daily net returns of the jump-model and volatility-band rules, the input series to the Ledoit-Wolf test. Costs a full refit loop to regenerate: inference.py --refresh",
    "inference.log": "run log -- the corrected shallow-half execution (Z1/Z2 tables, leave-one-episode-out display), 2026-08-26, after the four audit amendments",
    "inference.err.log": "stderr of the same; empty on the clean run",
    "inference.superseded.log": "the first shallow-half execution's output, renamed UNREAD before the four audit amendments -- kept as the record that no interval was read pre-amendment",
    "inference.superseded.err.log": "stderr of the same; empty",
    "deeptail_mc.N3.csv": "DERIVED. backup copy of the first execution's 200 N3 rows, taken 2026-08-26 before the resume-safe writer fix; superseded by deeptail_mc.csv",
    "deeptail_nulls.backup.json": "backup of the two cached null fits, taken 2026-08-26 21:22 before the resume",
    "deeptail_mc.N1.log": "run log, 2026-08-26 21:29 attempt; empty -- the process died before stdout flushed",
    "deeptail_mc.N1.err.log": "stderr of the same; empty",
    "deeptail_mc.resume.log": "run log, 2026-08-26 21:41 resume (--null N1 --null N2); empty -- died at session close before stdout flushed",
    "deeptail_mc.resume.err.log": "stderr of the same; empty",
    "deeptail_mc.N1N2.log": "run log, 2026-08-27 detached relaunch: N1's 200 paths and scored table (5,490s, 12 workers); ends where the 12:34 reboot killed N2",
    "deeptail_mc.N1N2.err.log": "stderr of the same: seven pool-worker respawn failures (WinError 5) as the reboot tore down the parent",
    "deeptail_mc.N2.log": "run log, 2026-08-27 12:43 relaunch (--null N2); empty -- died ~13:16 before stdout flushed, third terminal-tied death (the provenance line here originally claimed 200 paths; that was written ahead of the run and was wrong)",
    "deeptail_mc.N2.err.log": "stderr of the same: one pool-worker spawn failure (WinError 5) as the parent vanished",
    "deeptail_mc.N2retry.log": "run log, 2026-08-27 13:28 relaunch (--null N2), detached via Start-Process like the successful N1 run",
    "deeptail_mc.N2retry.err.log": "stderr of the same",
}


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def describe(path: Path) -> dict:
    text = path.read_text(encoding="utf-8", errors="replace").splitlines()
    rows = max(len(text) - 1, 0) if path.suffix == ".csv" else len(text)
    first = last = "-"
    if path.suffix == ".csv" and rows > 0:
        first = text[1].split(",")[0]
        last = text[-1].split(",")[0]
    return {
        "name": path.name,
        "sha256": digest(path),
        "bytes": path.stat().st_size,
        "rows": rows,
        "first": first,
        "last": last,
        "produced_by": PROVENANCE.get(path.name, "UNRECORDED -- add it to src/manifest.py"),
    }


def scan() -> list[dict]:
    return [describe(p) for p in sorted(DATA_DIR.iterdir())
            if p.is_file() and p.name != MANIFEST.name]


def render(entries: list[dict]) -> str:
    header = (
        "# Data manifest\n\n"
        "**Generated by `src/manifest.py`. Do not edit by hand.**\n\n"
        "`data/` is gitignored; this file is not. It exists so that \"the archived results\n"
        "reproduce\" is checkable rather than asserted: a cache that differs from the one that\n"
        "produced a published number is detected instead of silently used.\n\n"
        "Two of these are **derived artifacts from long refit loops**, not downloads. Regenerating\n"
        "them is not free, and a `yfinance` re-download years from now is not guaranteed to return\n"
        "the same history -- which is the whole reason for the hashes.\n\n"
        "Regenerate after any deliberate cache change:\n\n"
        "```\n.venv\\Scripts\\python.exe src/manifest.py --write\n```\n\n"
        "| file | sha256 | bytes | rows | first | last | produced by |\n"
        "|---|---|---|---|---|---|---|\n"
    )
    body = "".join(
        f"| `{e['name']}` | `{e['sha256']}` | {e['bytes']} | {e['rows']} | "
        f"{e['first']} | {e['last']} | {e['produced_by']} |\n"
        for e in entries
    )
    return header + body


def parse() -> dict[str, dict]:
    if not MANIFEST.exists():
        return {}
    recorded = {}
    for line in MANIFEST.read_text(encoding="utf-8").splitlines():
        if not line.startswith("| `"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if cells[1].startswith("sha256"):
            continue
        recorded[cells[0].strip("`")] = {
            "sha256": cells[1].strip("`"), "bytes": int(cells[2]), "rows": int(cells[3]),
        }
    return recorded


def verify() -> tuple[list[str], list[str], list[str]]:
    """Returns (matched, missing, mismatched). Only mismatched is a failure."""
    recorded = parse()
    matched, missing, mismatched = [], [], []
    for name, entry in sorted(recorded.items()):
        path = DATA_DIR / name
        if not path.exists():
            missing.append(name)
        elif digest(path) == entry["sha256"]:
            matched.append(name)
        else:
            mismatched.append(name)
    untracked = sorted({p.name for p in DATA_DIR.iterdir()
                        if p.is_file() and p.name != MANIFEST.name} - set(recorded))
    mismatched.extend(f"{n} (present but not in the manifest)" for n in untracked)
    return matched, missing, mismatched


def main() -> None:
    if "--write" in sys.argv:
        entries = scan()
        MANIFEST.write_text(render(entries), encoding="utf-8")
        print(f"wrote {MANIFEST} -- {len(entries)} files")
        return
    matched, missing, mismatched = verify()
    print(f"matched:    {len(matched)}")
    print(f"MISSING:    {len(missing)}  {missing if missing else ''}")
    print(f"MISMATCHED: {len(mismatched)}  {mismatched if mismatched else ''}")
    sys.exit(1 if mismatched else 0)


if __name__ == "__main__":
    main()
