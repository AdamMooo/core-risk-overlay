"""Context rungs: is the model's one-step conditioning honest?

NOT "does the model beat a moving average." At h=1 the MS model and a tuned
EWMA are near-identical by construction, so a null here is what theory
predicts, not evidence about the model. RiskMetrics EWMA is IGARCH -- its
multi-step variance forecast is a martingale, E[sigma2[t+h]] = sigma2[t+1] for
every h, so it never reverts. MS(2) reverts toward the stationary regime mix at
a rate set by the second eigenvalue of P. That is the entire difference between
the two models and it is invisible at one step ahead. Read these rungs as a
sanity check on the harness, never as a ranking.

RESEARCH-PROTOCOL step 3. Two deliberately trivial estimators are scored by the
IDENTICAL battery as the model, on the IDENTICAL sample:

  constant  expanding-window mean and sd, normal. Unconditional -- it does not
            react to anything. Passes Kupiec trivially by construction, which
            is exactly why coverage alone cannot settle anything.
  ewma      expanding mean, RiskMetrics exponentially-weighted variance,
            normal. sigma2[t] = lam*sigma2[t-1] + (1-lam)*r[t-1]^2

Both are strictly point-in-time: every quantity at week t uses data through
t-1 only, enforced by an explicit .shift(1).

lam is reported as a SWEEP, never a single tuned value. Picking the lam that
loses to the model would be the cheapest way to fake a result.

Run: .venv\\Scripts\\python.exe baselines.py [SPY]
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

import numpy as np
import pandas as pd
from scipy import stats

import evaluation as ev

ROOT = Path(__file__).parent
DATA_DIR = ROOT / "data"
ALPHAS = (0.10, 0.05, 0.01)
LAMBDAS = (0.90, 0.94, 0.97)
HEADLINE_LAMBDA = 0.94          # RiskMetrics. Fixed before seeing any result.


def load(ticker: str) -> tuple[pd.Series, pd.DataFrame]:
    returns = pd.read_csv(DATA_DIR / f"{ticker.lower()}_weekly.csv",
                          index_col=0, parse_dates=True).iloc[:, 0].astype(float).dropna()
    model = pd.read_csv(DATA_DIR / f"density_{ticker.lower()}.csv",
                        index_col=0, parse_dates=True)
    return returns, model


def constant_density(returns: pd.Series) -> pd.DataFrame:
    """Expanding mean and sd, both lagged one week. No reaction to anything."""
    mu = returns.expanding(min_periods=52).mean().shift(1)
    sd = returns.expanding(min_periods=52).std().shift(1)
    return pd.DataFrame({"mu": mu, "sigma": sd}).dropna()


def ewma_density(returns: pd.Series, lam: float) -> pd.DataFrame:
    mu = returns.expanding(min_periods=52).mean().shift(1)
    # ewm on squared returns then shift: variance at t uses r[t-1] and earlier.
    variance = returns.pow(2).ewm(alpha=1.0 - lam, adjust=False).mean().shift(1)
    return pd.DataFrame({"mu": mu, "sigma": np.sqrt(variance)}).dropna()


def score(name: str, realized: pd.Series, mu, sigma=None, var_frame=None,
          pit=None) -> dict:
    """Run the battery. Takes either (mu, sigma) for a normal or a model frame."""
    out = {"name": name, "n": len(realized)}

    if pit is None:
        pit = pd.Series(stats.norm.cdf((realized - mu) / sigma), index=realized.index)
    out["pit"] = pit

    berk = ev.berkowitz_test(pit)
    out["berkowitz_p"] = berk.p_value
    out["berkowitz_sigma2"] = berk.sigma2

    for alpha in ALPHAS:
        var = (var_frame[f"var_{alpha}"] if var_frame is not None
               else mu + sigma * stats.norm.ppf(alpha))
        hits = realized < var
        cover = ev.coverage_tests(hits, alpha)
        out[f"rate_{alpha}"] = cover.observed_rate
        out[f"kupiec_{alpha}"] = cover.p_uc
        out[f"ind_{alpha}"] = cover.p_ind
        out[f"var_{alpha}"] = var
        out[f"tick_{alpha}"] = ev.tick_loss(realized, var, alpha)
    return out


def report(ticker: str = "SPY") -> tuple[list[dict], pd.Series]:
    returns, model = load(ticker)
    window = model.index                      # score everything on the model's sample
    realized = returns.loc[window]

    results = [score("MS model", realized, None, var_frame=model, pit=model["pit"])]

    const = constant_density(returns).loc[window]
    results.append(score("constant", realized, const["mu"], const["sigma"]))

    for lam in LAMBDAS:
        e = ewma_density(returns, lam).loc[window]
        results.append(score(f"EWMA {lam}", realized, e["mu"], e["sigma"]))

    print("=" * 78)
    print(f"CONTEXT RUNGS — {ticker}, {len(realized)} out-of-sample weeks, "
          f"{window[0].date()} .. {window[-1].date()}")
    print("=" * 78)
    print("\nHOW OFTEN EACH WAS WRONG  (promised rate in brackets)")
    print(f"  {'':12s}" + "".join(f"{f'{a:.0%} [{a:.0%}]':>16s}" for a in ALPHAS))
    for r in results:
        cells = "".join(f"{r[f'rate_{a}']:>10.4f}{'  ' if r[f'kupiec_{a}']>=0.05 else ' *'}"
                        f"{'':>4s}" for a in ALPHAS)
        print(f"  {r['name']:12s}" + cells)
    print("  * = Kupiec rejects at 5%")

    print("\nDENSITY CALIBRATION (Berkowitz)")
    print(f"  {'':12s} {'p':>8s} {'sigma2':>8s}")
    for r in results:
        print(f"  {r['name']:12s} {r['berkowitz_p']:8.4f} {r['berkowitz_sigma2']:8.4f}")

    print("\nRANKING — mean tick loss x1e4 (lower is better; only differences mean anything)")
    print(f"  {'':12s}" + "".join(f"{f'alpha={a:.0%}':>12s}" for a in ALPHAS))
    for r in results:
        print(f"  {r['name']:12s}"
              + "".join(f"{r[f'tick_{a}'].mean()*1e4:12.4f}" for a in ALPHAS))

    print(f"\nDIEBOLD-MARIANO vs the MS model (negative favours the MS model)")
    base = results[0]
    print(f"  {'':12s}" + "".join(f"{f'alpha={a:.0%}':>22s}" for a in ALPHAS))
    for r in results[1:]:
        cells = ""
        for a in ALPHAS:
            dm = ev.diebold_mariano(base[f"tick_{a}"], r[f"tick_{a}"],
                                    label_a="MS model", label_b=r["name"])
            mark = "*" if dm.p_value < 0.05 else " "
            cells += f"{dm.statistic:>13.2f}  p={dm.p_value:.3f}{mark}"
        print(f"  {r['name']:12s}" + cells)
    print("  * = significant at 5%")

    return results, realized


def figures(results: list[dict], realized: pd.Series, ticker: str) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    keep = [r for r in results if r["name"] in
            ("MS model", "constant", f"EWMA {HEADLINE_LAMBDA}")]
    colors = {"MS model": "#c1440e", "constant": "#9a9a9a",
              f"EWMA {HEADLINE_LAMBDA}": "#2b6cb0"}

    fig, axes = plt.subplots(1, 3, figsize=(14, 4.4))
    for ax, alpha in zip(axes, ALPHAS):
        names = [r["name"] for r in keep]
        rates = [r[f"rate_{alpha}"] for r in keep]
        ax.bar(names, rates, color=[colors[n] for n in names], alpha=0.9, width=0.6)
        ax.axhline(alpha, color="black", linestyle="--", linewidth=1.5)
        ax.text(-0.55, alpha, f"promised {alpha:.0%}", va="center", ha="left",
                fontsize=10, backgroundcolor="white")
        for i, v in enumerate(rates):
            ax.text(i, v, f"{v:.1%}", ha="center", va="bottom", fontsize=13, weight="bold")
        ax.set_title(f"The \"{alpha:.0%} worst week\" line", fontsize=13, pad=14)
        ax.set_ylabel("how often it was actually breached" if alpha == 0.10 else "")
        ax.set_ylim(0, max(rates + [alpha]) * 1.45)
        ax.spines[["top", "right"]].set_visible(False)
        ax.tick_params(labelsize=11)
    fig.suptitle(f"One-step coverage, all three estimators   {ticker}, "
                 f"{len(realized)} weeks, no look-ahead", fontsize=15, y=1.02)
    fig.tight_layout()
    out = ROOT / "figures" / f"rungs_scorecard_{ticker.lower()}.png"
    out.parent.mkdir(exist_ok=True)
    fig.savefig(out, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"\n  wrote {out.relative_to(ROOT)}")

    fig, ax = plt.subplots(figsize=(15, 5.5))
    ax.bar(realized.index, realized.values, width=6,
           color="#d8d8d8", label="what actually happened each week")
    for r in keep:
        ax.plot(r["var_0.01"].index, r["var_0.01"], linewidth=1.8,
                color=colors[r["name"]], label=f"{r['name']} — its 1% worst case")
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_ylabel("weekly return", fontsize=12)
    ax.set_ylim(-0.26, 0.14)
    ax.legend(fontsize=11, frameon=False, loc="lower left", ncol=2)
    ax.set_title(f"When each one says risk is high — {ticker}, 2003-2026.  "
                 f"Lower line = claiming more danger.", fontsize=14)
    ax.spines[["top", "right"]].set_visible(False)
    ax.tick_params(labelsize=11)
    ax.grid(alpha=0.15)
    ax.set_axisbelow(True)
    fig.tight_layout()
    out = ROOT / "figures" / f"rungs_paths_{ticker.lower()}.png"
    fig.savefig(out, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  wrote {out.relative_to(ROOT)}")


def main() -> None:
    ticker = (sys.argv[1] if len(sys.argv) > 1 else "SPY").upper()
    results, realized = report(ticker)
    figures(results, realized, ticker)


if __name__ == "__main__":
    main()
