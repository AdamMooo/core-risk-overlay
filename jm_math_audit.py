"""Computational half of the jump-model mathematical audit.

Uses the repository's own implementation (src/jumpmodel.py) throughout, so every
result is about the code that actually runs, not a reimplementation.
"""
from __future__ import annotations

import sys
from itertools import product

import numpy as np

sys.path.insert(0, r"C:\dev\systematic-investing-research\core-risk-overlay")
from src.jumpmodel import (  # noqa: E402
    _squared_distances,
    fit_jump_model,
    forward_costs,
    viterbi_path,
)

rng_global = np.random.default_rng(20260827)
LINE = "=" * 78


def brute_force(D: np.ndarray, lam: float) -> tuple[tuple[int, ...], float]:
    T, K = D.shape
    best_path, best_val = None, np.inf
    for path in product(range(K), repeat=T):
        val = sum(D[t, path[t]] for t in range(T)) + lam * sum(
            path[t] != path[t - 1] for t in range(1, T)
        )
        if val < best_val:
            best_path, best_val = path, val
    return best_path, best_val


# ---------------------------------------------------------------- experiment 1
print(LINE)
print("EXPERIMENT 1 -- exactness: viterbi_path vs brute force, random instances")
print(LINE)
fails = 0
for trial in range(200):
    T = int(rng_global.integers(2, 9))
    K = int(rng_global.integers(2, 4))
    D = rng_global.exponential(1.0, size=(T, K))
    lam = float(rng_global.exponential(1.0))
    bf_path, bf_val = brute_force(D, lam)
    vp = viterbi_path(D, lam)
    vp_val = D[np.arange(T), vp].sum() + lam * np.count_nonzero(np.diff(vp))
    if not np.isclose(vp_val, bf_val, rtol=0, atol=1e-12):
        fails += 1
print(f"200 random instances (T in [2,8], K in [2,3]): value mismatches = {fails}")

# online form: argmin_k V(t,k) must equal terminal state of the optimal prefix path
fails = 0
for trial in range(100):
    T, K = int(rng_global.integers(2, 9)), 2
    D = rng_global.exponential(1.0, size=(T, K))
    lam = float(rng_global.exponential(1.0))
    V = forward_costs(D, lam)
    for t in range(T):
        _, prefix_val = brute_force(D[: t + 1], lam)
        if not np.isclose(V[t].min(), prefix_val, atol=1e-12):
            fails += 1
print(f"100 instances, every prefix: forward value vs brute-force prefix optimum, mismatches = {fails}")

# ---------------------------------------------------------------- experiment 2
print()
print(LINE)
print("EXPERIMENT 2 -- the lambda solution path on a worked T=5 example")
print(LINE)
# 1-D data, centroids FIXED at 0 and 1. Fit costs are exact squares.
x = np.array([0.0, 0.9, 1.0, 0.2, 0.0])
centroids = np.array([[0.0], [1.0]])
D = _squared_distances(x[:, None], centroids)
print(f"data x = {x.tolist()}, centroids fixed at 0 and 1")
print("per-day fit costs D(t,k) = (x_t - theta_k)^2:")
for t in range(5):
    print(f"  t={t}: state0 {D[t,0]:.2f}   state1 {D[t,1]:.2f}")

# lower envelope over all 32 paths of  fit(path) + lambda * switches(path)
cands = {}
for path in product(range(2), repeat=5):
    fit = sum(D[t, path[t]] for t in range(5))
    sw = sum(path[t] != path[t - 1] for t in range(1, 5))
    if sw not in cands or fit < cands[sw][0]:
        cands[sw] = (fit, path)
print("\ncheapest path at each switch count:")
for sw in sorted(cands):
    fit, path = cands[sw]
    print(f"  {sw} switches: fit {fit:.2f}  path {''.join(map(str, path))}")

# breakpoints = crossings of the lower envelope lines fit + lambda*sw
sws = sorted(cands)
print("\nanalytic breakpoints (envelope crossings) and verification:")
kept = [(cands[sw][0], sw) for sw in sws]
for (f1, s1), (f2, s2) in zip(kept[1:], kept[:-1]):
    if s1 == s2:
        continue
    lam_star = (f2 - f1) / (s1 - s2) if s1 != s2 else np.inf
    below = viterbi_path(D, lam_star - 1e-9)
    above = viterbi_path(D, lam_star + 1e-9)
    print(
        f"  lambda* = {lam_star:.6f}: just below -> {''.join(map(str, below))} "
        f"({np.count_nonzero(np.diff(below))} switches), "
        f"just above -> {''.join(map(str, above))} "
        f"({np.count_nonzero(np.diff(above))} switches)"
    )

# ---------------------------------------------------------------- experiment 3
print()
print(LINE)
print("EXPERIMENT 3 -- switch count vs lambda: fixed centroids, then joint fit")
print(LINE)
# fixed centroids: monotone by the envelope argument; verify on a long instance
T = 2000
true_z = np.zeros(T, dtype=int)
q = 0.02
rng = np.random.default_rng(7)
for t in range(1, T):
    true_z[t] = true_z[t - 1] if rng.random() > q else 1 - true_z[t - 1]
xsim = np.where(true_z == 0, -1.0, 1.0)[:, None] + rng.normal(0, 1, (T, 1))
Dsim = _squared_distances(xsim, np.array([[-1.0], [1.0]]))
lams = np.concatenate([[0.0], np.geomspace(0.01, 200, 40)])
sw_fixed = [int(np.count_nonzero(np.diff(viterbi_path(Dsim, l)))) for l in lams]
mono = all(a >= b for a, b in zip(sw_fixed, sw_fixed[1:]))
print(f"fixed centroids: switch counts monotone non-increasing in lambda: {mono}")
print(f"  counts along the grid: {sw_fixed}")

sw_joint = []
for l in lams:
    st, _, _ = fit_jump_model(xsim, k=2, jump_penalty=float(l), n_init=10, seed=0)
    sw_joint.append(int(np.count_nonzero(np.diff(st))))
viol = [
    (float(lams[i]), sw_joint[i], float(lams[i + 1]), sw_joint[i + 1])
    for i in range(len(lams) - 1)
    if sw_joint[i + 1] > sw_joint[i]
]
print(f"joint fit (centroids re-estimated): monotone: {len(viol) == 0}")
if viol:
    for a, b, c, d in viol:
        print(f"  VIOLATION: lambda {a:.4g} -> {b} switches, lambda {c:.4g} -> {d} switches")

# ---------------------------------------------------------------- experiment 4
print()
print(LINE)
print("EXPERIMENT 4 -- MAP correspondence and hard-assignment bias, K=2 HMM data")
print(LINE)
# generative truth: z_t sticky with switch prob q, x_t | z_t ~ N(+-mu, 1), d=1
# MAP lambda in THIS repo's convention (loss without the 1/2): 2*sigma^2*log((1-q)/q)
q = 0.02
lam_map = 2 * np.log((1 - q) / q)
print(f"switch prob q = {q}  ->  lambda_MAP (repo convention) = {lam_map:.3f}")
print(f"(the repo's production lambda = 50 implies q = 1/(1+exp(25)) = {1/(1+np.exp(25)):.2e})")
print()
print(f"{'mu':>5} {'acc(kmeans)':>12} {'acc(JM)':>9} {'acc(oracle)':>12} "
      f"{'|theta_hat|(JM)':>16} {'|theta_hat|(km)':>16}")
for mu in (0.5, 1.0, 2.0):
    accs_km, accs_jm, accs_or, seps_jm, seps_km = [], [], [], [], []
    for rep in range(20):
        rr = np.random.default_rng(100 + rep)
        z = np.zeros(3000, dtype=int)
        for t in range(1, 3000):
            z[t] = z[t - 1] if rr.random() > q else 1 - z[t - 1]
        xs = np.where(z == 0, -mu, mu)[:, None] + rr.normal(0, 1, (3000, 1))

        def acc(est: np.ndarray) -> float:
            a = (est == z).mean()
            return max(a, 1 - a)  # label switching

        st_km, cen_km, _ = fit_jump_model(xs, k=2, jump_penalty=0.0, n_init=10, seed=0)
        st_jm, cen_jm, _ = fit_jump_model(xs, k=2, jump_penalty=lam_map, n_init=10, seed=0)
        st_or = viterbi_path(_squared_distances(xs, np.array([[-mu], [mu]])), lam_map)
        accs_km.append(acc(st_km)); accs_jm.append(acc(st_jm)); accs_or.append(acc(st_or))
        seps_jm.append(np.abs(cen_jm).mean()); seps_km.append(np.abs(cen_km).mean())
    print(f"{mu:>5} {np.mean(accs_km):>12.3f} {np.mean(accs_jm):>9.3f} "
          f"{np.mean(accs_or):>12.3f} {np.mean(seps_jm):>16.3f} {np.mean(seps_km):>16.3f}")
print(f"(true |theta| = mu in every row; oracle = Viterbi with true centroids at lambda_MAP)")

# ---------------------------------------------------------------- experiment 5
print()
print(LINE)
print("EXPERIMENT 5 -- autocorrelated noise: the lambda that recovers states best")
print(LINE)
# same regimes, but noise is AR(1) with rho -- the i.i.d. emission assumption breaks,
# and the state-recovery-optimal lambda should move far above lambda_MAP.
q = 0.02
mu = 1.0
lam_grid = np.geomspace(0.5, 400, 25)
for rho in (0.0, 0.9, 0.97):
    best = []
    for rep in range(10):
        rr = np.random.default_rng(500 + rep)
        z = np.zeros(3000, dtype=int)
        for t in range(1, 3000):
            z[t] = z[t - 1] if rr.random() > q else 1 - z[t - 1]
        eps = np.empty(3000)
        eps[0] = rr.normal(0, 1)
        innov_sd = np.sqrt(1 - rho**2)  # stationary variance 1 for every rho
        for t in range(1, 3000):
            eps[t] = rho * eps[t - 1] + rr.normal(0, innov_sd)
        xs = (np.where(z == 0, -mu, mu) + eps)[:, None]
        accs = []
        for l in lam_grid:
            st, _, _ = fit_jump_model(xs, k=2, jump_penalty=float(l), n_init=5, seed=0)
            a = (st == z).mean()
            accs.append(max(a, 1 - a))
        best.append(lam_grid[int(np.argmax(accs))])
    print(f"rho = {rho:>4}: recovery-optimal lambda (median over 10 reps) = "
          f"{np.median(best):8.2f}   (lambda_MAP for iid noise = {2*np.log((1-q)/q):.2f})")

# ---------------------------------------------------------------- experiment 6
print()
print(LINE)
print("EXPERIMENT 6 -- scale equivariance: fit(c*X, lambda) == fit(X, lambda/c^2)")
print(LINE)
rr = np.random.default_rng(9)
xs = rr.normal(0, 1, (800, 3))
xs[300:500] += 1.5
c = 3.0
for lam in (5.0, 50.0):
    st_a, _, _ = fit_jump_model(c * xs, k=2, jump_penalty=lam, n_init=10, seed=0)
    st_b, _, _ = fit_jump_model(xs, k=2, jump_penalty=lam / c**2, n_init=10, seed=0)
    same = np.array_equal(st_a, st_b) or np.array_equal(st_a, 1 - st_b)
    print(f"lambda = {lam:>5}: identical state paths (up to label swap): {same}")
print("(k-means++ seeding probabilities are scale-invariant, so with the same seed")
print(" the entire trajectory of the optimizer maps exactly)")
print()
print("done.")


# ---------------------------------------------------------------- follow-up
# Two checks run after the first pass: the exact T=5 breakpoint, and the
# rho=0.97 accuracy profile that explains experiment 5's flat ridge.
import sys

import numpy as np

sys.path.insert(0, r"C:\dev\systematic-investing-research\core-risk-overlay")
from src.jumpmodel import _squared_distances, fit_jump_model, viterbi_path

# --- check 1: the T=5 breakpoint is exactly 0.9, and switch count 1 is skipped
x = np.array([0.0, 0.9, 1.0, 0.2, 0.0])
D = _squared_distances(x[:, None], np.array([[0.0], [1.0]]))
for lam in (0.85, 0.899, 0.901, 0.95, 1.5):
    p = viterbi_path(D, lam)
    print(f"lambda={lam:6.3f}: path {''.join(map(str,p))}  switches {np.count_nonzero(np.diff(p))}")

# --- check 2: rho=0.97 accuracy profile across lambda (is the curve flat/degraded?)
q, mu = 0.02, 1.0
for rho in (0.9, 0.97):
    print(f"\nrho={rho}: accuracy by lambda (5 reps)")
    lams = [1.0, 3.0, 8.0, 19.0, 50.0, 120.0]
    rows = []
    for rep in range(5):
        rr = np.random.default_rng(500 + rep)
        z = np.zeros(3000, dtype=int)
        for t in range(1, 3000):
            z[t] = z[t - 1] if rr.random() > q else 1 - z[t - 1]
        eps = np.empty(3000)
        eps[0] = rr.normal(0, 1)
        s = np.sqrt(1 - rho**2)
        for t in range(1, 3000):
            eps[t] = rho * eps[t - 1] + rr.normal(0, s)
        xs = (np.where(z == 0, -mu, mu) + eps)[:, None]
        accs = []
        for l in lams:
            st, _, _ = fit_jump_model(xs, k=2, jump_penalty=l, n_init=5, seed=0)
            a = (st == z).mean()
            accs.append(max(a, 1 - a))
        rows.append(accs)
    m = np.mean(rows, axis=0)
    for l, a in zip(lams, m):
        print(f"  lambda {l:6.1f}: mean acc {a:.3f}")
