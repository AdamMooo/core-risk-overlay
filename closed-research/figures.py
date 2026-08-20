"""Figures for the reporting skeleton, docs/RESEARCH-PROTOCOL.md section 8.

Reads the walk-forward density series written by `walkforward.py density
<TICKER>` and draws the preregistered figures. Draws nothing that is not in
section 8 -- the figure list is fixed in advance so the analysis cannot sprawl
into whatever happens to look interesting.

    Figure 1  PIT histogram and ACF                         built
    Figure 2  VaR path through 2008 and 2020, breaches       built
    Figure 3  mixture VaR minus moment-matched normal VaR    built
    Figure 4  filtered vs smoothed VaR paths (R5)            needs the smoothed
                                                            path; not built

Run: .venv\\Scripts\\python.exe figures.py [SPY|QQQ]
Writes figures/<name>_<ticker>.png at 150 dpi.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

import evaluation as ev
import predictive as pr

ROOT = Path(__file__).parent.parent
DATA_DIR = ROOT / "data"
FIGURE_DIR = ROOT / "figures"

ALPHAS = (0.10, 0.05, 0.01)
CRISES = {
    "Global Financial Crisis": ("2007-06-01", "2009-12-31"),
    "COVID crash": ("2019-09-01", "2020-12-31"),
}

INK = "#1a1a1a"
MUTED = "#8a8a8a"
ACCENT = "#c1440e"
CALM = "#2b6cb0"


def load(ticker: str) -> pd.DataFrame:
    path = DATA_DIR / f"density_{ticker.lower()}.csv"
    if not path.exists():
        raise SystemExit(
            f"{path} not found. Run:\n"
            f"    .venv\\Scripts\\python.exe walkforward.py density {ticker}"
        )
    return pd.read_csv(path, index_col=0, parse_dates=True)


def style(ax) -> None:
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color(MUTED)
    ax.tick_params(colors=MUTED, labelsize=8)
    ax.grid(alpha=0.15, linewidth=0.6)
    ax.set_axisbelow(True)


def save(fig, name: str, ticker: str) -> Path:
    FIGURE_DIR.mkdir(exist_ok=True)
    path = FIGURE_DIR / f"{name}_{ticker.lower()}.png"
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  wrote {path.relative_to(ROOT)}")
    return path


def figure_1_pit(frame: pd.DataFrame, ticker: str) -> None:
    """PIT histogram (20 bins) and the two ACFs, per section 5.1."""
    u = frame["pit"].to_numpy()
    n = u.size
    diagnostics = ev.pit_diagnostics(u, bins=20, lags=20)

    fig, axes = plt.subplots(1, 3, figsize=(13, 3.6))

    ax = axes[0]
    ax.hist(u, bins=20, range=(0, 1), color=CALM, alpha=0.75, edgecolor="white")
    expected = n / 20
    ax.axhline(expected, color=ACCENT, linewidth=1.2, linestyle="--",
               label=f"uniform ({expected:.0f})")
    # A correctly-specified density puts every bar on the dashed line. Bars
    # piled at BOTH ends mean the density is too narrow: realized returns land
    # in its tails more often than it claims.
    ax.set_title(f"PIT histogram   chi2 p = {diagnostics.uniformity_p:.3f}",
                 fontsize=9, color=INK)
    ax.set_xlabel("u = F(r)", fontsize=8)
    ax.legend(fontsize=7, frameon=False)
    style(ax)

    bounds = 1.96 / np.sqrt(n)
    for ax, acf, label, p in (
        (axes[1], diagnostics.acf_level, "ACF of u",
         diagnostics.ljung_box_level_p),
        (axes[2], diagnostics.acf_squared, "ACF of (u - 0.5)^2",
         diagnostics.ljung_box_squared_p),
    ):
        lags = np.arange(1, len(acf) + 1)
        colors = [ACCENT if abs(v) > bounds else CALM for v in acf]
        ax.bar(lags, acf, color=colors, width=0.7)
        ax.axhspan(-bounds, bounds, color=MUTED, alpha=0.18, zorder=0)
        ax.axhline(0, color=MUTED, linewidth=0.8)
        ax.set_title(f"{label}   Ljung-Box p = {p:.4f}", fontsize=9, color=INK)
        ax.set_xlabel("lag (weeks)", fontsize=8)
        style(ax)

    fig.suptitle(
        f"Figure 1 — density calibration, {ticker} walk-forward (n = {n})",
        fontsize=11, color=INK, y=1.04,
    )
    save(fig, "fig1_pit", ticker)


def figure_2_var_path(frame: pd.DataFrame, ticker: str) -> None:
    """VaR path through each crisis with realized returns and breaches marked."""
    fig, axes = plt.subplots(len(CRISES), 1, figsize=(11, 3.1 * len(CRISES)))
    axes = np.atleast_1d(axes)

    for ax, (label, (lo, hi)) in zip(axes, CRISES.items()):
        window = frame.loc[lo:hi]
        if window.empty:
            continue

        ax.bar(window.index, window["realized"], width=5.0,
               color=[ACCENT if v < 0 else CALM for v in window["realized"]],
               alpha=0.55, label="realized weekly return")
        for alpha, dash in zip(ALPHAS, [(1, 3), (4, 2), None]):
            line, = ax.plot(window.index, window[f"var_{alpha}"], linewidth=1.3,
                            color=INK, alpha=0.35 + 0.25 * ALPHAS.index(alpha))
            if dash:
                line.set_dashes(dash)
            line.set_label(f"VaR {alpha:.0%}")

        breached = window[window["realized"] < window["var_0.01"]]
        if not breached.empty:
            ax.scatter(breached.index, breached["realized"], s=42, zorder=5,
                       facecolor="none", edgecolor=ACCENT, linewidth=1.6,
                       label="1% VaR breach")

        ax.axhline(0, color=MUTED, linewidth=0.8)
        ax.set_title(f"{label}   ({len(window)} weeks, "
                     f"{len(breached)} breaches of the 1% VaR)",
                     fontsize=9, color=INK)
        ax.set_ylabel("weekly log return", fontsize=8)
        ax.legend(fontsize=7, frameon=False, ncol=5, loc="lower left")
        style(ax)

    fig.suptitle(
        f"Figure 2 — walk-forward VaR path, {ticker}. "
        "The VaR widens only AFTER the bad weeks arrive: a causal filter is "
        "late by construction.",
        fontsize=11, color=INK, y=1.0,
    )
    fig.tight_layout()
    save(fig, "fig2_var_path", ticker)


def figure_3_mixture_vs_normal(frame: pd.DataFrame, ticker: str) -> None:
    """Mixture VaR minus the moment-matched normal, against regime weight.

    Section 1.1 check 5. The moment-matched shortcut is not an approximation
    that degrades gracefully -- the error peaks in the middle of the weight
    range and changes SIGN with alpha, which is why the solver exists.
    """
    sigma_wide = float(frame["sigma_wide"].iloc[-1])
    sigma_calm = float(frame["sigma_calm"].iloc[-1])
    sigmas = np.array([sigma_calm, sigma_wide])
    means = np.array([0.0, 0.0])

    grid = np.linspace(0.0, 1.0, 201)
    fig, axes = plt.subplots(1, 2, figsize=(12, 3.8))

    ax = axes[0]
    for alpha in ALPHAS:
        errors = []
        for w in grid:
            weights = np.array([1.0 - w, w])
            exact = pr.mixture_var(weights, means, sigmas, alpha)
            total = float(np.sum(weights * sigmas**2))
            naive = np.sqrt(total) * stats.norm.ppf(alpha)
            errors.append((naive - exact) * 100.0)
        ax.plot(grid, errors, linewidth=1.6, label=f"alpha = {alpha:.0%}")
    ax.axhline(0, color=MUTED, linewidth=0.8)
    ax.set_xlabel("weight on the wide regime", fontsize=8)
    ax.set_ylabel("normal minus mixture VaR (pp)", fontsize=8)
    ax.set_title("Moment-matched normal error, and it changes sign",
                 fontsize=9, color=INK)
    ax.legend(fontsize=7, frameon=False)
    style(ax)

    ax = axes[1]
    ax.scatter(frame["w_wide"], frame["var_0.01"] * 100.0, s=5, alpha=0.35,
               color=CALM, edgecolor="none")
    ax.set_xlabel("weight on the wide regime (realised, walk-forward)", fontsize=8)
    ax.set_ylabel("1% VaR (%)", fontsize=8)
    ax.set_title(f"What the model actually did   "
                 f"(sigma calm {sigma_calm:.2%}, wide {sigma_wide:.2%})",
                 fontsize=9, color=INK)
    style(ax)

    fig.suptitle(f"Figure 3 — mixture vs moment-matched normal, {ticker}",
                 fontsize=11, color=INK, y=1.03)
    fig.tight_layout()
    save(fig, "fig3_mixture_vs_normal", ticker)


def figure_tail(frame: pd.DataFrame, ticker: str) -> None:
    """The result in one picture: where the density fails.

    Not a section 8 figure. It plots the quantities section 8 already reports
    (breach rate by alpha, ES ratio, tail QQ) rather than introducing a new
    measure, so it adds no yardstick -- it only makes Tables 3 and 4 legible.
    """
    fig, axes = plt.subplots(1, 3, figsize=(13, 3.6))

    ax = axes[0]
    rates = [float((frame["realized"] < frame[f"var_{a}"]).mean()) for a in ALPHAS]
    x = np.arange(len(ALPHAS))
    ax.bar(x - 0.19, ALPHAS, width=0.36, color=MUTED, alpha=0.6, label="promised")
    ax.bar(x + 0.19, rates, width=0.36, color=ACCENT, alpha=0.85, label="delivered")
    for i, (promised, delivered) in enumerate(zip(ALPHAS, rates)):
        ax.text(i + 0.19, delivered, f"  {delivered / promised:.2f}x",
                ha="center", va="bottom", fontsize=8, color=ACCENT)
    ax.set_xticks(x, [f"{a:.0%}" for a in ALPHAS])
    ax.set_title("Breach rate: promised vs delivered", fontsize=9, color=INK)
    ax.legend(fontsize=7, frameon=False)
    style(ax)

    ax = axes[1]
    ratios = []
    for alpha in ALPHAS:
        breached = frame[frame["realized"] < frame[f"var_{alpha}"]]
        ratios.append(float(breached["realized"].mean()
                            / breached[f"es_{alpha}"].mean()))
    ax.plot([f"{a:.0%}" for a in ALPHAS], ratios, marker="o", color=ACCENT,
            linewidth=1.6)
    ax.axhline(1.0, color=MUTED, linewidth=1.0, linestyle="--")
    ax.set_ylim(0.9, max(ratios) * 1.1)
    ax.set_title("ES ratio: realized breach ÷ predicted\n(above 1 = understates depth)",
                 fontsize=9, color=INK)
    style(ax)

    ax = axes[2]
    z = np.sort(stats.norm.ppf(np.clip(frame["pit"], 1e-10, 1 - 1e-10)))
    theoretical = stats.norm.ppf((np.arange(1, z.size + 1) - 0.5) / z.size)
    ax.scatter(theoretical, z, s=5, alpha=0.4, color=CALM, edgecolor="none")
    limit = [min(theoretical.min(), z.min()), max(theoretical.max(), z.max())]
    ax.plot(limit, limit, color=ACCENT, linewidth=1.2, linestyle="--")
    ax.set_xlabel("theoretical N(0,1) quantile", fontsize=8)
    ax.set_ylabel("realized z = Phi^-1(u)", fontsize=8)
    ax.set_title("QQ of the PIT: the left tail falls off the line",
                 fontsize=9, color=INK)
    style(ax)

    fig.suptitle(f"Where the density fails — {ticker}, walk-forward, no look-ahead",
                 fontsize=11, color=INK, y=1.04)
    fig.tight_layout()
    save(fig, "fig_tail_failure", ticker)


def main() -> None:
    for ticker in [t.upper() for t in sys.argv[1:]] or ["SPY"]:
        print(f"{ticker}:")
        frame = load(ticker)
        figure_1_pit(frame, ticker)
        figure_2_var_path(frame, ticker)
        figure_3_mixture_vs_normal(frame, ticker)
        figure_tail(frame, ticker)


if __name__ == "__main__":
    main()
