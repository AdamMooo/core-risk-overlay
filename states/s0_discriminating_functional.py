"""S0 -- what would constitute evidence that the return-generating environment has changed.

Preregistration: docs/STUB-S0-WHAT-COUNTS-AS-EVIDENCE.md, committed before this file, with the
sweep, the functionals and the matching declared in its section 5.

NO MARKET DATA IS READ HERE. Everything is simulated from two model classes at declared parameters,
because a power study run on the real series would let the answer be chosen by looking at the data.
S0 therefore cannot produce a finding about equities; if a result feels like one, that is the error.

The question: is there a functional T and a horizon h at which a persistent two-state switching
process and a smoothly-reverting continuous-scale process (GARCH(1,1), the charter's null N1) differ
-- AFTER being matched so the easy differences are gone -- by enough to be seen in one history of
8,300 daily observations?

Run: .venv\\Scripts\\python.exe states/s0_discriminating_functional.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import numpy as np

import pathfunctionals as pf
import pandas as pd

# ---------------------------------------------------------------- declared in the stub, section 5.5
KAPPAS = (2.0, 4.0, 6.5)          # variance ratio; 6.5 ~ this repo's own fitted regime ratio
PI2S = (0.15, 0.30)               # stationary occupancy of the wide state
LAMBDAS = (0.95, 0.98, 0.995)     # second eigenvalue of P -- the persistence
N = 8300                          # SPY daily, 1993-2026
REPLICATIONS = 400
SEED = 20260818
HORIZONS = (1, 5, 21, 63)
BLOCKS = (21, 63)
CDAR_Q = 0.05
DPRIME_THRESHOLD = 2.0            # stub section 5.4
DAILY_SD = 0.01                   # stub section 5.6. ~16% annualised. T1-T3 are scale-invariant;
                                  # T4 is not, and at unit variance drawdown saturates at 1.0


# ---------------------------------------------------------------------------------- the two classes
def switching_moments(kappa: float, pi2: float, lam: float) -> dict:
    """Analytic moments of r_t = sigma(S_t) z_t, unconditional variance normalised to 1.

    The squared-return autocovariance is Cov(v(S_t), v(S_{t-k})) = pi1 pi2 (v1-v2)^2 lambda^k --
    geometric in k for any k and any parameters. That is Timmermann (2000) Prop. 5, E6 in this
    repository, and it is what makes the exact match in `match_garch` possible.
    """
    pi1 = 1.0 - pi2
    v1 = 1.0 / (pi1 + pi2 * kappa)
    v2 = kappa * v1
    kurtosis = 3.0 * (pi1 * v1 ** 2 + pi2 * v2 ** 2)      # E[r^4], since E[r^2] = 1
    rho1 = pi1 * pi2 * (v1 - v2) ** 2 * lam / (kurtosis - 1.0)
    return {
        "v1": v1, "v2": v2, "pi1": pi1, "pi2": pi2,
        "p11": 1.0 - pi2 * (1.0 - lam), "p22": lam + pi2 * (1.0 - lam),
        "kurtosis": kurtosis, "rho1": rho1, "lambda": lam,
    }


def garch_rho1(alpha: float, beta: float) -> float:
    psi = alpha + beta
    denominator = 1.0 - 2.0 * alpha * beta - beta ** 2
    if denominator <= 0.0:
        return np.nan
    return alpha * (1.0 - beta * psi) / denominator


def garch_kurtosis(alpha: float, psi: float) -> float:
    denominator = 1.0 - psi ** 2 - 2.0 * alpha ** 2
    if denominator <= 0.0:
        return np.nan                                      # fourth moment does not exist
    return 3.0 * (1.0 - psi ** 2) / denominator


def match_garch(target_rho1: float, lam: float) -> dict | None:
    """Find the GARCH(1,1) that matches the switching model's WHOLE squared-return ACF.

    Both ACFs are geometric from lag 1, so fixing persistence psi = lambda matches every decay
    ratio, and one free parameter (alpha) then has to hit rho(1). Bisection on alpha, which is
    monotone increasing in rho(1) over the admissible range.

    Returns None when the target is unattainable or GARCH's fourth moment does not exist -- both
    are reported as infeasible cells rather than skipped.
    """
    lo, hi = 1e-6, lam - 1e-6
    if garch_rho1(hi, lam - hi) < target_rho1 or garch_rho1(lo, lam - lo) > target_rho1:
        return None
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if garch_rho1(mid, lam - mid) < target_rho1:
            lo = mid
        else:
            hi = mid
    alpha = 0.5 * (lo + hi)
    beta = lam - alpha
    if 3.0 * alpha ** 2 + 2.0 * alpha * beta + beta ** 2 >= 1.0:
        return None
    return {"alpha": alpha, "beta": beta, "omega": 1.0 - lam,
            "kurtosis": garch_kurtosis(alpha, lam), "rho1": garch_rho1(alpha, beta)}


def simulate_switching(params: dict, reps: int, n: int, rng) -> np.ndarray:
    """(reps, n) returns, scaled to DAILY_SD. The chain is stepped jointly across replications."""
    stay = np.array([params["p11"], params["p22"]])
    state = (rng.random(reps) > params["pi1"]).astype(np.int8)
    variance = np.empty((reps, n))
    draws = rng.random((reps, n))
    for t in range(n):
        variance[:, t] = np.where(state == 0, params["v1"], params["v2"])
        state = np.where(draws[:, t] < stay[state], state, 1 - state)
    return DAILY_SD * np.sqrt(variance) * rng.standard_normal((reps, n))


def simulate_garch(params: dict, reps: int, n: int, rng, burn: int = 2000) -> np.ndarray:
    omega, alpha, beta = params["omega"], params["alpha"], params["beta"]
    z = rng.standard_normal((reps, n + burn))
    sigma2 = np.ones(reps)
    r_prev = z[:, 0]
    out = np.empty((reps, n + burn))
    for t in range(n + burn):
        sigma2 = omega + alpha * r_prev ** 2 + beta * sigma2
        out[:, t] = np.sqrt(sigma2) * z[:, t]
        r_prev = out[:, t]
    return DAILY_SD * out[:, burn:]


# ------------------------------------------------------------------- the functionals, stub sec. 5.3
def t1_squared_acf(returns: np.ndarray, lag: int) -> np.ndarray:
    """T1: sample ACF of squared returns. Matched exactly by construction -- a correctness check."""
    x = returns ** 2
    x = x - x.mean(axis=1, keepdims=True)
    numerator = (x[:, lag:] * x[:, :-lag]).mean(axis=1)
    return numerator / x.var(axis=1)


def t2_aggregate_kurtosis(returns: np.ndarray, horizon: int) -> np.ndarray:
    """T2: excess kurtosis of h-day summed returns. At h=1 this IS the residual mismatch."""
    reps, n = returns.shape
    usable = (n // horizon) * horizon
    blocks = returns[:, :usable].reshape(reps, -1, horizon).sum(axis=2)
    centred = blocks - blocks.mean(axis=1, keepdims=True)
    m2 = (centred ** 2).mean(axis=1)
    m4 = (centred ** 4).mean(axis=1)
    return m4 / m2 ** 2 - 3.0


def t3_block_variance_dispersion(returns: np.ndarray, block: int) -> np.ndarray:
    """T3: sd of log realized variance over non-overlapping blocks -- persistence-of-persistence."""
    reps, n = returns.shape
    usable = (n // block) * block
    realized = (returns[:, :usable].reshape(reps, -1, block) ** 2).sum(axis=2)
    return np.log(realized).std(axis=1)


def t4_path_geometry(returns: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """T4: max drawdown, CDaR(worst 5%), and the excursion count -- the effective n of the row."""
    max_dd = np.empty(len(returns))
    cdar = np.empty(len(returns))
    excursions = np.empty(len(returns))
    index = pd.RangeIndex(returns.shape[1])
    for i, row in enumerate(returns):
        wealth = pd.Series(np.exp(np.cumsum(row)), index=index)
        max_dd[i] = pf.drawdown(wealth).max()
        cdar[i] = pf.cdar(wealth, CDAR_Q)
        excursions[i] = len(pf.excursions(wealth, threshold=0.10))
    return max_dd, cdar, excursions


def dprime(a: np.ndarray, b: np.ndarray) -> float:
    """Standardised separation of two sampling distributions at n. Stub section 5.4."""
    pooled = np.sqrt((a.var(ddof=1) + b.var(ddof=1)) / 2.0)
    if pooled == 0.0:
        return 0.0
    return abs(a.mean() - b.mean()) / pooled


# ------------------------------------------------------------------------------------------- report
def run_cell(kappa: float, pi2: float, lam: float, rng) -> dict | None:
    ms = switching_moments(kappa, pi2, lam)
    garch = match_garch(ms["rho1"], lam)
    if garch is None:
        return None

    r_ms = simulate_switching(ms, REPLICATIONS, N, rng)
    r_g = simulate_garch(garch, REPLICATIONS, N, rng)

    row = {
        "kappa": kappa, "pi2": pi2, "lambda": lam,
        "alpha": garch["alpha"], "beta": garch["beta"],
        "rho1_ms": ms["rho1"], "rho1_garch": garch["rho1"],
        "kurt_ms": ms["kurtosis"], "kurt_garch": garch["kurtosis"],
    }
    for h in HORIZONS:
        row[f"T1_h{h}"] = dprime(t1_squared_acf(r_ms, h), t1_squared_acf(r_g, h))
        row[f"T2_h{h}"] = dprime(t2_aggregate_kurtosis(r_ms, h), t2_aggregate_kurtosis(r_g, h))
    for b in BLOCKS:
        row[f"T3_b{b}"] = dprime(t3_block_variance_dispersion(r_ms, b),
                                 t3_block_variance_dispersion(r_g, b))
    dd_ms, cdar_ms, exc_ms = t4_path_geometry(r_ms)
    dd_g, cdar_g, exc_g = t4_path_geometry(r_g)
    row["T4_maxdd"] = dprime(dd_ms, dd_g)
    row["T4_cdar"] = dprime(cdar_ms, cdar_g)
    row["T4_excursions_ms"] = exc_ms.mean()
    row["T4_maxdd_ms"] = dd_ms.mean()
    row["T4_maxdd_g"] = dd_g.mean()
    return row


def block_1_matching(grid: pd.DataFrame, infeasible: list) -> None:
    print("=" * 100)
    print("BLOCK 1 -- MATCHING QUALITY.  Reported FIRST, before any separation number (stub sec. 4).")
    print("=" * 100)
    print("  Matched EXACTLY by construction: unconditional variance, and the whole squared-return")
    print("  ACF at every lag (both are geometric -- E6 -- so psi = lambda plus one alpha suffices).")
    print("  Residual mismatch: kurtosis. Three GARCH parameters cannot also match a fourth moment.")
    print()
    print(f"  {'kappa':>6} {'pi2':>6} {'lambda':>7} | {'alpha':>7} {'beta':>7} | "
          f"{'rho1 MS':>9} {'rho1 GJR':>9} {'d rho1':>9} | {'kurt MS':>8} {'kurt G':>8} {'mismatch':>9}")
    print("  " + "-" * 96)
    for _, r in grid.iterrows():
        drho = abs(r["rho1_ms"] - r["rho1_garch"])
        mism = (r["kurt_garch"] - r["kurt_ms"]) / r["kurt_ms"] * 100.0
        print(f"  {r['kappa']:>6.1f} {r['pi2']:>6.2f} {r['lambda']:>7.3f} | "
              f"{r['alpha']:>7.4f} {r['beta']:>7.4f} | "
              f"{r['rho1_ms']:>9.5f} {r['rho1_garch']:>9.5f} {drho:>9.2e} | "
              f"{r['kurt_ms']:>8.2f} {r['kurt_garch']:>8.2f} {mism:>8.1f}%")
    print()
    print(f"  cells run: {len(grid)} of {len(KAPPAS) * len(PI2S) * len(LAMBDAS)}   "
          f"infeasible: {len(infeasible)}")
    for cell in infeasible:
        print(f"    INFEASIBLE (no admissible alpha, or GARCH 4th moment undefined): {cell}")


def block_2_separation(grid: pd.DataFrame) -> None:
    print()
    print("=" * 100)
    print(f"BLOCK 2 -- DISCRIMINABILITY d' AT n = {N:,}.  Threshold {DPRIME_THRESHOLD}, preregistered.")
    print("=" * 100)
    cols = ([f"T1_h{h}" for h in HORIZONS] + [f"T2_h{h}" for h in HORIZONS]
            + [f"T3_b{b}" for b in BLOCKS] + ["T4_maxdd", "T4_cdar"])
    print(f"  {'kappa':>5} {'pi2':>5} {'lam':>6} | " + " ".join(f"{c.replace('_',''):>8}" for c in cols))
    print("  " + "-" * (25 + 9 * len(cols)))
    for _, r in grid.iterrows():
        cells = " ".join(f"{r[c]:>8.2f}" for c in cols)
        print(f"  {r['kappa']:>5.1f} {r['pi2']:>5.2f} {r['lambda']:>6.3f} | {cells}")
    print()
    print("  T1 = squared-return ACF at lag h (CORRECTNESS CHECK -- must be ~0)")
    print("  T2 = excess kurtosis of h-day sums (T2h1 IS the mismatch; h>1 counts only in excess)")
    print("  T3 = sd of log block realized variance (persistence-of-persistence)")
    print("  T4 = max drawdown / CDaR(worst 5%) of the path")


def block_3_verdict(grid: pd.DataFrame) -> None:
    print()
    print("=" * 100)
    print("BLOCK 3 -- VERDICT AGAINST THE PREREGISTERED FALSIFICATION CRITERION")
    print("=" * 100)

    t1_max = max(grid[f"T1_h{h}"].max() for h in HORIZONS)
    print(f"\n  CORRECTNESS.  max d' on T1 across every cell and horizon = {t1_max:.3f}")
    print(f"                predicted ~0. {'OK' if t1_max < DPRIME_THRESHOLD else 'IMPLEMENTATION IS WRONG'}"
          " -- the matching holds in simulation, not only in algebra.")

    print("\n  T2, and the mismatch rule.  A separation at h>1 counts only in EXCESS of T2 at h=1.")
    survivors = []
    for _, r in grid.iterrows():
        floor = r["T2_h1"]
        for h in HORIZONS[1:]:
            if r[f"T2_h{h}"] >= DPRIME_THRESHOLD and r[f"T2_h{h}"] > floor:
                survivors.append((r["kappa"], r["pi2"], r["lambda"], h,
                                  r[f"T2_h{h}"], floor))
    print(f"                cells where T2 at some h>1 clears BOTH the threshold and its own "
          f"h=1 floor: {len(survivors)} of {len(grid)}")
    for k, p, l, h, d, f in survivors:
        print(f"                  kappa={k:.1f} pi2={p:.2f} lambda={l:.3f}  h={h:>2}  "
              f"d'={d:.2f}  (floor {f:.2f})")

    print("\n  T3.  Predicted to die at the matching step (stub sec. 5.2, deductively).")
    t3_max = max(grid[f"T3_b{b}"].max() for b in BLOCKS)
    t3_clear = sum(int((grid[f"T3_b{b}"] >= DPRIME_THRESHOLD).sum()) for b in BLOCKS)
    print(f"       max d' = {t3_max:.3f}; cells clearing the threshold: {t3_clear} of {2 * len(grid)}")

    print("\n  T4.  Predicted to separate in expectation and be unestimable on one history.")
    print(f"       max d' on max drawdown = {grid['T4_maxdd'].max():.3f}; on CDaR(5%) = "
          f"{grid['T4_cdar'].max():.3f}")
    print(f"       mean excursions past 10% per path (the effective n of this row): "
          f"{grid['T4_excursions_ms'].mean():.1f}")
    print(f"       mean max drawdown, switching {grid['T4_maxdd_ms'].mean():.3f} vs "
          f"null {grid['T4_maxdd_g'].mean():.3f}")

    all_functionals = ([f"T2_h{h}" for h in HORIZONS[1:]] + [f"T3_b{b}" for b in BLOCKS]
                       + ["T4_maxdd", "T4_cdar"])
    best = {c: grid[c].max() for c in all_functionals}
    winner = max(best, key=best.get)
    any_clear = best[winner] >= DPRIME_THRESHOLD

    print("\n" + "-" * 100)
    if not any_clear:
        print("  H(S0) IS FALSIFIED.  No candidate functional reaches d' = 2 at any horizon in any")
        print(f"  cell of the declared sweep. Best anywhere: {winner} at d' = {best[winner]:.3f}.")
        print("  Charter section 6: the programme ends as INDETERMINATE -- the question cannot be")
        print("  asked on this history, which is not the same as the answer being no.")
        print("  This does NOT license a search for a better functional after the fact.")
    else:
        print(f"  H(S0) SURVIVES on {winner} at d' = {best[winner]:.3f}.")
        extreme = grid.loc[grid[winner].idxmax()]
        corner = (extreme["kappa"] == max(KAPPAS)) and (extreme["lambda"] == max(LAMBDAS))
        print(f"  Best cell: kappa={extreme['kappa']:.1f} pi2={extreme['pi2']:.2f} "
              f"lambda={extreme['lambda']:.3f}")
        clearing = grid[grid[winner] >= DPRIME_THRESHOLD]
        only_corner = bool((clearing["kappa"] == max(KAPPAS)).all()
                           and (clearing["lambda"] == max(LAMBDAS)).all())
        print(f"  cells clearing the threshold: {len(clearing)} of {len(grid)}")
        if corner and only_corner:
            print("  ANTI-FLATTERY RULE FIRES (stub sec. 5.5): it survives only in the extreme")
            print("  corner, so it is measuring the PARAMETERS, not the structure. Reported as")
            print("  NOT DISCRIMINATING.")


def report() -> None:
    rng = np.random.default_rng(SEED)
    rows, infeasible = [], []
    for kappa in KAPPAS:
        for pi2 in PI2S:
            for lam in LAMBDAS:
                row = run_cell(kappa, pi2, lam, rng)
                if row is None:
                    infeasible.append(f"kappa={kappa} pi2={pi2} lambda={lam}")
                else:
                    rows.append(row)
    grid = pd.DataFrame(rows)

    print()
    print("S0 -- WHAT WOULD CONSTITUTE EVIDENCE THAT THE RETURN-GENERATING ENVIRONMENT HAS CHANGED")
    print(f"Preregistered: docs/STUB-S0-WHAT-COUNTS-AS-EVIDENCE.md   seed {SEED}   "
          f"{REPLICATIONS} replications/class/cell")
    print("NO MARKET DATA. This experiment cannot produce a finding about equities.")
    print()
    block_1_matching(grid, infeasible)
    block_2_separation(grid)
    block_3_verdict(grid)
    print()


if __name__ == "__main__":
    report()
