"""The dynamics test: does P carry risk information beyond VIX's level?

The first experiment in this repo whose INPUT matches what the model actually
claims to know. Every prior test -- D3 included -- fed the regression a LEVEL (a
VaR or ES scalar) and raced it against VIX's level. VIX is a spot price; the
model's content is persistence. A level-vs-level test structurally cannot see it.

THE INPUT IS SCALE-FREE BY CONSTRUCTION, which is the whole design:

    X[t] = Var_h(t) / Var_1(t)

the model's h-step predictive variance divided by its 1-step predictive
variance. Dividing out the level leaves nothing but dynamics. X > 1 means the
model expects risk to RISE from here; X < 1 means it expects reversion. The
quantity is literally

    w_1 = xi[t]' P                  (already in density_{ticker}.csv as w_wide)
    w_h = w_1 P^(h-1)               (vintage P from walkforward_{ticker}.csv)

so no rescaling of VIX can reproduce it. That satisfies the hub's own test: if a
test could be passed by a constant rescaling of VIX, it is not testing this model.

--- protocol 0 stub, fixed before the run -------------------------------------

1. CLAIM TUPLE   weekly * h=4 * forward downside semivolatility * SPY 2003-2026,
                 n=307 non-overlapping. ONE input. No variants, no sweep.

2. PREDICTION    c is insignificant. Two reasons, both stated before running:
                 spot VIX is a 30-day measure and already spans the h=4 horizon,
                 and the model's persistence was measured ~35% too short against
                 the data (memory_diagnostic.py, 138 days against 212). I expect
                 this to fail.

3. LITERATURE    Sec 5.5's encompassing literature is [UNREAD] and paywalled. It
                 bears on interpreting a null, not on whether the regression is
                 correctly specified. Recorded, not treated as a block.

4. MECHANISM     Spot VIX gives ONE horizon's level. X gives the RATIO between
                 two horizons. Genuinely different information -- but narrower
                 than earlier claimed in this session, because a 30-day implied
                 vol does embed some view of how volatility behaves over a month.
                 The clean control would be the VIX term structure; ^VIX3M
                 returns a single row from Yahoo, so it is unavailable.

5. SURPRISE      c significant says regime persistence carries risk information
                 the option market does not price at 30 days -- a finding about
                 how market risk behaves, which is the stated deliverable, and
                 reportable either way. c insignificant closes the model class on
                 BOTH axes and the program stops.

HARKING GUARD. There are a dozen candidate persistence quantities (expected
duration, decay rate, second eigenvalue, posterior entropy, path shape). Running
them until one clears is the failure mode this repo exists to avoid. ONE is
specified above, chosen on theory. If it fails, that is the answer -- not a
prompt to try the next one.

POWER IS REPORTED, NOT ASSUMED. X moves slowly, so effective n is well below
307. An insignificant c can mean underpowered rather than absent, and the two
are distinguishable only if X's own variation is on the page. It is printed.

Run: .venv\\Scripts\\python.exe dynamics_test.py [SPY]
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

import numpy as np
import pandas as pd

import evaluation as ev
from encompassing import (
    WEEKS_PER_YEAR,
    forward_downside_semivol,
    load_density,
    load_log_vix,
    load_returns,
    univariate_r_squared,
)

ROOT = Path(__file__).parent
DATA_DIR = ROOT / "data"
HORIZON = 4


def load_vintages(ticker: str) -> pd.DataFrame:
    path = DATA_DIR / f"walkforward_{ticker.lower()}.csv"
    return pd.read_csv(path, index_col=0, parse_dates=True)


def variance_ratio(density: pd.DataFrame, vintages: pd.DataFrame, horizon: int):
    """X = Var_h / Var_1 from vintage P, with an orientation cross-check.

    statsmodels stores p[i->j] = Pr(s[t+1]=j | s[t]=i), so the row-stochastic
    matrix is [[p00, 1-p00], [p10, 1-p10]] and weights propagate as w P.
    Getting that backwards inverts the model silently, so sigma_wide from the
    density file is re-derived from the vintage index and compared.
    """
    density = density.assign(refit_end=pd.to_datetime(density["refit_end"]))
    joined = density.join(vintages, on="refit_end", rsuffix="_v")
    ratios, checks = [], []

    for _, row in joined.iterrows():
        p00, p10 = row["p[0->0]"], row["p[1->0]"]
        transition = np.array([[p00, 1.0 - p00], [p10, 1.0 - p10]])

        wide = int(row["jump_regime"])
        calm = 1 - wide
        w1 = np.empty(2)
        w1[wide] = row["w_wide"]
        w1[calm] = 1.0 - row["w_wide"]

        variances = np.array([row["sigma2[0]"], row["sigma2[1]"]])
        means = np.array([row["const[0]"], row["const[1]"]])
        checks.append(np.sqrt(variances[wide]) - row["sigma_wide"])

        wh = w1 @ np.linalg.matrix_power(transition, horizon - 1)

        def mixture_variance(w):
            second = float(w @ (variances + means**2))
            return second - float(w @ means) ** 2

        ratios.append(mixture_variance(wh) / mixture_variance(w1))

    orientation_error = float(np.abs(checks).max())
    if orientation_error > 1e-8:
        raise ValueError(
            f"Regime orientation mismatch: sigma_wide from the vintage index "
            f"differs from the density file by {orientation_error:.2e}. "
            "Refusing to run -- this would silently invert the model."
        )

    return pd.Series(ratios, index=joined.index, name="x")


def build_frame(returns, density, log_vix, x, horizon, rv_offset=0):
    rv = forward_downside_semivol(returns, horizon)
    if rv_offset:
        rv = rv.shift(-rv_offset)
    implied = np.exp(log_vix.shift(1)) / 100.0 * np.sqrt(horizon / WEEKS_PER_YEAR)
    frame = pd.concat(
        [rv.rename("rv"), implied.rename("iv"), x.rename("x")], axis=1
    )
    return frame.reindex(density.index).dropna()


def report(ticker: str = "SPY") -> None:
    returns = load_returns(ticker)
    density = load_density(ticker)
    vintages = load_vintages(ticker)
    log_vix = load_log_vix(returns)

    x = variance_ratio(density, vintages, HORIZON)
    frame = build_frame(returns, density, log_vix, x, HORIZON)
    stride = frame.iloc[::HORIZON]

    print(f"DYNAMICS TEST -- {ticker}, h={HORIZON}, X = Var_{HORIZON} / Var_1")
    print(f"sample {density.index[0].date()} to {density.index[-1].date()}, "
          f"{len(frame)} rows, {len(stride)} non-overlapping\n")

    print("POWER -- does X actually move?")
    print(f"  X   min {x.min():.4f}   p10 {x.quantile(0.10):.4f}   "
          f"median {x.median():.4f}   p90 {x.quantile(0.90):.4f}   max {x.max():.4f}")
    print(f"      sd {x.std():.4f}   coefficient of variation {x.std()/x.mean():.4f}")
    print(f"  weeks with X > 1 (model expects risk to rise): {(x > 1).mean():.1%}")
    print(f"  corr(X, VIX level)  {frame['x'].corr(frame['iv']):+.4f}"
          f"   (high |corr| would mean X is just VIX in disguise)\n")

    result = ev.encompassing_regression(
        stride["rv"], stride["iv"], stride["x"], horizon=HORIZON, hac_lags=0
    )
    print("PRIMARY -- non-overlapping stride-h inference")
    print(f"  n = {result.n}")
    print(f"  VIX     b = {result.beta_implied:+.4f}  (p = {result.p_implied:.4f})")
    print(f"  model   c = {result.gamma_model:+.4f}  (p = {result.p_model:.4f})")
    print(f"  R2 both {result.r_squared:.4f}"
          f"   VIX alone {univariate_r_squared(stride, 'iv', 0):.4f}"
          f"   X alone {univariate_r_squared(stride, 'x', 0):.4f}\n")

    print("adversarial alignment -- leaky must beat true and stale")
    for offset, name in ((-1, "leaky"), (0, "true"), (1, "stale")):
        shifted = build_frame(
            returns, density, log_vix, x, HORIZON, rv_offset=offset
        ).iloc[::HORIZON]
        check = ev.encompassing_regression(
            shifted["rv"], shifted["iv"], shifted["x"], horizon=HORIZON, hac_lags=0
        )
        print(f"  {name:<8s} R2 {check.r_squared:.4f}  "
              f"c {check.gamma_model:+.4f} (p {check.p_model:.4f})")

    print()
    if result.p_model > 0.05:
        print("c IS NOT SIGNIFICANT. As predicted. The model class is closed on")
        print("BOTH axes -- level (D3) and dynamics (here). Read the power block")
        print("above before calling it absent rather than undetected.")
    else:
        print("c IS SIGNIFICANT. Regime persistence carries risk information not")
        print("priced in 30-day implied volatility. This was predicted to fail, so")
        print("treat it as a hypothesis for an independent sample, not a result.")


def main() -> None:
    report(sys.argv[1].upper() if len(sys.argv) > 1 else "SPY")


if __name__ == "__main__":
    main()
