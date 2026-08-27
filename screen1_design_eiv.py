"""Thread B design study: errors-in-variables and the level-conditional decay profile.

Settles the question flagged in ASSESSMENT-PRESENT-STATE-RISK 12d before the form
is chosen: does measurement noise in range-based volatility flatten the
level-dependence differentially (corrupting kill condition 1), and how much true
effect survives at a realistic sample size?

Synthetic only. No market data is touched. Nothing here is a Thread B run.

Truth: log-vol AR(1) with level-dependent persistence
    x_{t+1} = mu + phi(x_t) * (x_t - mu) + sigma_e * eps_t
    phi(x)  = PHI_LOW - DPHI * Phi((x - mu) / sd_x)     (faster decay from high levels)
calibrated so persistence runs 0.99 (quiet) to 0.97 (stressed) -- the magnitude the
VIX term structure prices as an established regularity.

Observed: x*_t = x_t + u_t, u_t iid N(0, s_u^2). Parkinson on daily OHLC carries
relative variance ~0.41 for the variance estimate; by the delta method that is
sd(log sigma) ~ 0.32, the middle noise level below.

Estimator (candidate summary form): per horizon h, OLS of x*_{t+h} on [1, z, z^2]
with z = standardized x*_t. The quadratic coefficient c_h is the level-dependence
summary: the fitted local slope is b_h + 2 c_h z, so c_h < 0 means faster decay
from high levels. Monte Carlo dispersion across replications gives the sampling
sd directly (the design question needs detectability, not an in-sample HAC).
"""
from __future__ import annotations

import numpy as np
from scipy.stats import norm

MU = -4.6          # log daily vol ~ 1% -- location is irrelevant to slopes
SD_X = 0.5         # stationary sd of log vol (empirical ballpark)
PHI_LOW = 0.99     # persistence at the quiet end (half-life ~69d)
DPHI = 0.02        # minus persistence at the stressed end -> 0.97 (half-life ~23d)
SIGMA_E = SD_X * np.sqrt(1 - 0.98**2)  # keeps stationary sd near SD_X at mid phi
T = 14000          # ~55 years of trading days, the full daily history
HORIZONS = (1, 5, 21, 63)
NOISE = (0.0, 0.32, 0.50)
REPS = 200


def simulate(T_: int, rng: np.random.Generator) -> np.ndarray:
    x = np.empty(T_)
    x[0] = MU
    e = rng.normal(0.0, SIGMA_E, T_)
    for t in range(1, T_):
        phi = PHI_LOW - DPHI * norm.cdf((x[t - 1] - MU) / SD_X)
        x[t] = MU + phi * (x[t - 1] - MU) + e[t]
    return x


def quad_coefs(xobs: np.ndarray, h: int) -> tuple[float, float]:
    z = (xobs[:-h] - xobs[:-h].mean()) / xobs[:-h].std()
    y = xobs[h:]
    X = np.column_stack([np.ones_like(z), z, z * z])
    beta = np.linalg.lstsq(X, y, rcond=None)[0]
    return float(beta[1]), float(beta[2])   # b_h, c_h


def flat_truth(T_: int, rng: np.random.Generator) -> np.ndarray:
    # the kill-condition-1 world: one AR(1), no level dependence
    x = np.empty(T_)
    x[0] = MU
    e = rng.normal(0.0, SIGMA_E, T_)
    phi = PHI_LOW - DPHI / 2
    for t in range(1, T_):
        x[t] = MU + phi * (x[t - 1] - MU) + e[t]
    return x


def run(gen, label: str) -> dict:
    out = {}
    for s_u in NOISE:
        acc = {h: [] for h in HORIZONS}
        for rep in range(REPS):
            rng = np.random.default_rng(1000 * int(s_u * 100 + 1) + rep + (0 if label == "sloped" else 7_000_000))
            x = gen(T + max(HORIZONS), rng)
            xo = x + rng.normal(0.0, s_u, len(x)) if s_u > 0 else x
            for h in HORIZONS:
                acc[h].append(quad_coefs(xo, h))
        out[s_u] = {h: (np.mean([a[1] for a in acc[h]]),
                        np.std([a[1] for a in acc[h]]))
                    for h in HORIZONS}
    return out


print(f"level-dependent truth: phi 0.99 (quiet) -> 0.97 (stressed), T = {T}, {REPS} reps")
print(f"{'noise s_u':>10} {'h':>4} {'mean c_h':>10} {'MC sd':>8} {'atten.':>8} {'|c|/sd':>7}")
sloped = run(simulate, "sloped")
for s_u in NOISE:
    for h in HORIZONS:
        m, s = sloped[s_u][h]
        m0 = sloped[0.0][h][0]
        att = m / m0 if m0 != 0 else float("nan")
        print(f"{s_u:>10} {h:>4} {m:>10.4f} {s:>8.4f} {att:>8.2f} {abs(m)/s:>7.1f}")
    print()

print("flat truth (kill-condition world): same table -- c_h should be ~0 at every noise level")
flat = run(flat_truth, "flat")
print(f"{'noise s_u':>10} {'h':>4} {'mean c_h':>10} {'MC sd':>8} {'|c|/sd':>7}")
for s_u in NOISE:
    for h in HORIZONS:
        m, s = flat[s_u][h]
        print(f"{s_u:>10} {h:>4} {m:>10.4f} {s:>8.4f} {abs(m)/s:>7.1f}")
    print()
print("Reading: 'atten.' is c_h(noise)/c_h(clean) -- 1.0 would mean shape survives untouched.")
print("'|c|/sd' >= ~2 means the effect is detectable at this T; the flat rows size the false-fire risk.")
