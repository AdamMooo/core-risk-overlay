"""S0b -- the discreteness gate. THE FINAL SYNTHETIC IDENTIFICATION GATE.

Preregistration: closed-research/return-states/STUB-S0B-DISCRETENESS-GATE.md, committed before this file, with the null, the
three matching constraints, the functionals, the predictions and all three disqualifying tells fixed
in advance.

NO MARKET DATA IS READ HERE.

S0 matched the unconditional variance and the whole squared-return ACF, and its surviving functional
turned out to measure the one thing that matching left free -- the dispersion of the variance process
(R1). S0b closes that degree of freedom with a third constraint and asks whether the SHAPE of the
variance distribution can still be seen.

The alternative is imported from S0 unchanged, deliberately: the two gates must be comparable cell by
cell, and a re-implementation would put a second copy of the chain in the tree.

Run: .venv\\Scripts\\python.exe states/s0b_discreteness_gate.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import numpy as np
import pandas as pd

import s0_discriminating_functional as s0

# --------------------------------------------------------------- declared in the stub, sections 2.5/5
KAPPAS = s0.KAPPAS                # the sweep is S0's, not re-chosen
PI2S = s0.PI2S
LAMBDAS = s0.LAMBDAS
N = s0.N
REPLICATIONS = s0.REPLICATIONS
DAILY_SD = s0.DAILY_SD
BLOCKS = (21, 63)
DPRIME_THRESHOLD = s0.DPRIME_THRESHOLD
SEED = 20260819                   # S0b's own seed, declared in the stub


# ------------------------------------------------------------------- the null, stub section 2.4 (M3)
def garch_t_fourth_moment(alpha: float, beta: float, k: float) -> float:
    """E[sigma^4] for GARCH(1,1) with innovation kurtosis k, given E[sigma^2] = 1.

    sigma2_t = omega + (alpha z2_{t-1} + beta) sigma2_{t-1}, and sigma2_{t-1} is independent of
    z_{t-1}, so E[sigma^4] (1 - E[(alpha z2 + beta)^2]) = omega(omega + 2 psi), with omega = 1 - psi.
    At k = 3 this reduces to the Gaussian expression S0 used.
    """
    psi = alpha + beta
    denominator = 1.0 - alpha ** 2 * k - 2.0 * alpha * beta - beta ** 2
    if denominator <= 0.0:
        return np.nan                                  # fourth moment does not exist
    return (1.0 - psi ** 2) / denominator


def match_garch_t(kappa: float, pi2: float, lam: float) -> dict | None:
    """Impose (M1), (M2) and (M3). Returns None on any declared infeasibility.

    (M2) fixes alpha and beta EXACTLY as S0 fixed them: rho(1) for GARCH(1,1) is a ratio of two
    autocovariances that both carry the innovation-kurtosis factor, so it does not depend on k.
    (M3) then has one free parameter left -- the innovation kurtosis -- and is solved in closed form.
    """
    ms = s0.switching_moments(kappa, pi2, lam)
    base = s0.match_garch(ms["rho1"], lam)             # alpha, beta from (M1) + (M2)
    if base is None:
        return None
    alpha, beta = base["alpha"], base["beta"]
    m = ms["kurtosis"] / 3.0                           # E[sigma^4] of the alternative

    k = (1.0 - 2.0 * alpha * beta - beta ** 2 - (1.0 - lam ** 2) / m) / alpha ** 2
    if not np.isfinite(k) or k <= 3.0:
        return None                                    # no t distribution is thinner than a normal
    nu = (4.0 * k - 6.0) / (k - 3.0)
    if nu <= 4.0:
        return None                                    # no fourth moment
    if alpha ** 2 * k + 2.0 * alpha * beta + beta ** 2 >= 1.0:
        return None                                    # the null's fourth moment does not exist

    return {
        "alpha": alpha, "beta": beta, "omega": 1.0 - lam, "k": k, "nu": nu,
        "m_null": garch_t_fourth_moment(alpha, beta, k), "m_alt": m,
        "rho1": base["rho1"], "rho1_ms": ms["rho1"],
        "kurt_null": k * garch_t_fourth_moment(alpha, beta, k),
        "kurt_alt": ms["kurtosis"],
        "ms": ms,
    }


def simulate_garch_t(params: dict, reps: int, n: int, rng, burn: int = 2000) -> np.ndarray:
    omega, alpha, beta, nu = params["omega"], params["alpha"], params["beta"], params["nu"]
    z = rng.standard_t(nu, size=(reps, n + burn)) / np.sqrt(nu / (nu - 2.0))
    sigma2 = np.ones(reps)
    r_prev = z[:, 0]
    out = np.empty((reps, n + burn))
    for t in range(n + burn):
        sigma2 = omega + alpha * r_prev ** 2 + beta * sigma2
        out[:, t] = np.sqrt(sigma2) * z[:, t]
        r_prev = out[:, t]
    return DAILY_SD * out[:, burn:]


# ----------------------------------------------------------- the shape functionals, stub section 3
def _log_block_variance(returns: np.ndarray, block: int) -> np.ndarray:
    reps, n = returns.shape
    usable = (n // block) * block
    realized = (returns[:, :usable].reshape(reps, -1, block) ** 2).sum(axis=2)
    return np.log(realized)


def _standardised_moments(x: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    centred = x - x.mean(axis=1, keepdims=True)
    m2 = (centred ** 2).mean(axis=1)
    skew = (centred ** 3).mean(axis=1) / m2 ** 1.5
    excess_kurtosis = (centred ** 4).mean(axis=1) / m2 ** 2 - 3.0
    return skew, excess_kurtosis


def t5_log_rv_excess_kurtosis(returns: np.ndarray, block: int) -> np.ndarray:
    return _standardised_moments(_log_block_variance(returns, block))[1]


def t6_log_rv_skewness(returns: np.ndarray, block: int) -> np.ndarray:
    return _standardised_moments(_log_block_variance(returns, block))[0]


def t7_bimodality_coefficient(returns: np.ndarray, block: int) -> np.ndarray:
    """Sarle's coefficient (g1^2 + 1) / (g2 + 3). Bounded below by 1/(g2+3) with g2 >= -2."""
    skew, excess = _standardised_moments(_log_block_variance(returns, block))
    return (skew ** 2 + 1.0) / (excess + 3.0)


SHAPE_FUNCTIONALS = {"T5": t5_log_rv_excess_kurtosis,
                     "T6": t6_log_rv_skewness,
                     "T7": t7_bimodality_coefficient}


# ------------------------------------------------------------------------------------------- report
def run_cell(kappa: float, pi2: float, lam: float, rng) -> dict | None:
    matched = match_garch_t(kappa, pi2, lam)
    if matched is None:
        return None

    r_alt = s0.simulate_switching(matched["ms"], REPLICATIONS, N, rng)
    r_null = simulate_garch_t(matched, REPLICATIONS, N, rng)

    row = {"kappa": kappa, "pi2": pi2, "lambda": lam,
           "alpha": matched["alpha"], "beta": matched["beta"],
           "k": matched["k"], "nu": matched["nu"],
           "m_alt": matched["m_alt"], "m_null": matched["m_null"],
           "kurt_alt": matched["kurt_alt"], "kurt_null": matched["kurt_null"],
           "rho1_alt": matched["rho1_ms"], "rho1_null": matched["rho1"]}

    # The mismatch floor: return kurtosis, now with its sign flipped (stub section 2.5).
    row["floor"] = s0.dprime(s0.t2_aggregate_kurtosis(r_alt, 1),
                             s0.t2_aggregate_kurtosis(r_null, 1))
    for b in BLOCKS:
        # T3 is the CONTROL. With Var(sigma^2) matched its d' must return to ~0.
        row[f"T3_b{b}"] = s0.dprime(s0.t3_block_variance_dispersion(r_alt, b),
                                    s0.t3_block_variance_dispersion(r_null, b))
        for name, fn in SHAPE_FUNCTIONALS.items():
            a, g = fn(r_alt, b), fn(r_null, b)
            row[f"{name}_b{b}"] = s0.dprime(a, g)
            row[f"{name}_b{b}_alt"] = float(a.mean())
            row[f"{name}_b{b}_null"] = float(g.mean())
    return row


def block_1_matching(grid: pd.DataFrame, infeasible: list) -> None:
    print("=" * 108)
    print("BLOCK 1 -- FEASIBILITY AND MATCHING QUALITY.  Reported first (stub sec. 4).")
    print("=" * 108)
    print("  (M1) unconditional variance   (M2) squared-return ACF at every lag   (M3) Var(sigma^2)")
    print("  Deliberately unmatched, in the OPPOSITE direction from S0: return kurtosis (sec. 2.5).")
    print()
    print(f"  {'kappa':>6}{'pi2':>6}{'lam':>7} | {'alpha':>7}{'beta':>7}{'k':>7}{'nu':>7} | "
          f"{'d rho1':>9}{'d E[s4]':>9} | {'Var(s2)':>8} | {'K alt':>7}{'K null':>7}{'floor%':>8}")
    print("  " + "-" * 104)
    for _, r in grid.iterrows():
        drho = abs(r["rho1_alt"] - r["rho1_null"])
        dm = abs(r["m_alt"] - r["m_null"])
        mism = (r["kurt_null"] - r["kurt_alt"]) / r["kurt_alt"] * 100.0
        print(f"  {r['kappa']:>6.1f}{r['pi2']:>6.2f}{r['lambda']:>7.3f} | "
              f"{r['alpha']:>7.4f}{r['beta']:>7.4f}{r['k']:>7.2f}{r['nu']:>7.2f} | "
              f"{drho:>9.2e}{dm:>9.2e} | {r['m_alt'] - 1.0:>8.3f} | "
              f"{r['kurt_alt']:>7.2f}{r['kurt_null']:>7.2f}{mism:>7.1f}%")
    total = len(KAPPAS) * len(PI2S) * len(LAMBDAS)
    print()
    print(f"  cells run: {len(grid)} of {total}   INFEASIBLE: {len(infeasible)}")
    for cell in infeasible:
        print(f"    {cell}")


def block_2_control(grid: pd.DataFrame) -> bool:
    print()
    print("=" * 108)
    print("BLOCK 2 -- THE CONTROL.  T3 was S0's survivor. With Var(sigma^2) matched it must die.")
    print("=" * 108)
    t3_max = max(grid[f"T3_b{b}"].max() for b in BLOCKS)
    print(f"  {'kappa':>6}{'pi2':>6}{'lam':>7} | {'T3 b21':>9}{'T3 b63':>9}   (S0's T3_b21 for the "
          f"same cell, for contrast)")
    print("  " + "-" * 70)
    s0_t3 = {(2.0,0.15,0.950):0.16,(2.0,0.15,0.980):0.52,(2.0,0.15,0.995):0.65,
             (2.0,0.30,0.950):1.39,(2.0,0.30,0.980):0.65,(2.0,0.30,0.995):0.19,
             (4.0,0.15,0.950):1.15,(4.0,0.15,0.980):0.17,(4.0,0.15,0.995):0.26,
             (4.0,0.30,0.950):5.76,(4.0,0.30,0.980):3.74,(4.0,0.30,0.995):1.74,
             (6.5,0.15,0.950):3.58,(6.5,0.15,0.980):1.56,(6.5,0.15,0.995):0.51,
             (6.5,0.30,0.950):10.22,(6.5,0.30,0.980):6.66,(6.5,0.30,0.995):3.24}
    for _, r in grid.iterrows():
        was = s0_t3.get((r["kappa"], r["pi2"], r["lambda"]))
        print(f"  {r['kappa']:>6.1f}{r['pi2']:>6.2f}{r['lambda']:>7.3f} | "
              f"{r['T3_b21']:>9.2f}{r['T3_b63']:>9.2f}   was {was:>5.2f}")
    ok = t3_max < DPRIME_THRESHOLD
    print()
    print(f"  max d' on the control across every cell and block = {t3_max:.3f}")
    print(f"  {'OK -- (M3) holds in simulation, not only in algebra.' if ok else 'THE RUN IS VOID: (M3) is not holding. Not a finding.'}")
    return ok


def block_3_separation(grid: pd.DataFrame) -> None:
    print()
    print("=" * 108)
    print(f"BLOCK 3 -- SHAPE FUNCTIONALS, d' AT n = {N:,}.  Threshold {DPRIME_THRESHOLD}, "
          "preregistered.")
    print("=" * 108)
    cols = [f"{n}_b{b}" for b in BLOCKS for n in SHAPE_FUNCTIONALS]
    print(f"  {'kappa':>6}{'pi2':>6}{'lam':>7} | {'floor':>7} | " +
          " ".join(f"{c:>8}" for c in cols))
    print("  " + "-" * (40 + 9 * len(cols)))
    for _, r in grid.iterrows():
        print(f"  {r['kappa']:>6.1f}{r['pi2']:>6.2f}{r['lambda']:>7.3f} | {r['floor']:>7.2f} | " +
              " ".join(f"{r[c]:>8.2f}" for c in cols))
    print()
    print("  T5 = excess kurtosis of log RV   T6 = skewness of log RV")
    print("  T7 = Sarle bimodality coefficient of log RV")
    print("  floor = d' on return kurtosis, the residual mismatch. Sign is FLIPPED versus S0.")


def block_4_verdict(grid: pd.DataFrame, control_ok: bool) -> None:
    print()
    print("=" * 108)
    print("BLOCK 4 -- VERDICT AGAINST THE PREREGISTERED CRITERIA")
    print("=" * 108)

    if not control_ok:
        print("\n  THE RUN IS VOID. The control failed, so (M3) is not holding and no separation")
        print("  below is interpretable. This is not a FAIL and not a PASS -- it is a defect report.")
        return

    survivors = []
    for _, r in grid.iterrows():
        for b in BLOCKS:
            for name in SHAPE_FUNCTIONALS:
                d = r[f"{name}_b{b}"]
                if d >= DPRIME_THRESHOLD and d > r["floor"]:
                    survivors.append({"f": name, "B": b, "kappa": r["kappa"], "pi2": r["pi2"],
                                      "lambda": r["lambda"], "d": d, "floor": r["floor"]})

    raw = sum(int((grid[f"{n}_b{b}"] >= DPRIME_THRESHOLD).sum())
              for b in BLOCKS for n in SHAPE_FUNCTIONALS)
    print(f"\n  THE VOID RULE (stub sec. 2.7).  Threshold alone: {raw} pairs.  "
          f"Also clearing their own mismatch floor: {len(survivors)}.")
    if survivors:
        print()
        print(f"     {'func':>5}{'B':>4}{'kappa':>7}{'pi2':>6}{'lambda':>8}{'d prime':>9}{'floor':>8}")
        for s in sorted(survivors, key=lambda x: -x["d"]):
            print(f"     {s['f']:>5}{s['B']:>4}{s['kappa']:>7.1f}{s['pi2']:>6.2f}"
                  f"{s['lambda']:>8.3f}{s['d']:>9.2f}{s['floor']:>8.2f}")

    print("\n  TELL 1 -- ANTI-FLATTERY (stub sec. 7.1).")
    if survivors:
        cells = {(s["kappa"], s["lambda"]) for s in survivors}
        corner = all(k == max(KAPPAS) and l == max(LAMBDAS) for k, l in cells)
        print(f"     survival confined to kappa={max(KAPPAS)} and lambda={max(LAMBDAS)}? "
              f"{'YES -- DISQUALIFIED' if corner else 'no'}")
    else:
        corner = False
        print("     n/a -- nothing survived")

    print("\n  TELL 2 -- THE DISPERSION TELL (stub sec. 7.2 and sec. 3).")
    print("     PREDICTED: discreteness is HARDEST at low lambda, EASIEST at high lambda -- the")
    print("     OPPOSITE of S0's T3. A functional whose d' rises as lambda FALLS is suspected of")
    print("     measuring dispersion again.")
    direction = {}
    for name in SHAPE_FUNCTIONALS:
        for b in BLOCKS:
            rising, falling, flat = 0, 0, 0
            for kappa in KAPPAS:
                for pi2 in PI2S:
                    sub = grid[(grid["kappa"] == kappa) & (grid["pi2"] == pi2)].sort_values("lambda")
                    if len(sub) < 2:
                        continue
                    lo, hi = sub.iloc[0][f"{name}_b{b}"], sub.iloc[-1][f"{name}_b{b}"]
                    if hi > lo * 1.10:
                        rising += 1
                    elif lo > hi * 1.10:
                        falling += 1
                    else:
                        flat += 1
            direction[f"{name}_b{b}"] = (rising, falling, flat)
            print(f"     {name} B={b:>2}:  d' rises with lambda in {rising} rows (PREDICTED), "
                  f"falls in {falling} (dispersion tell), flat in {flat}")

    print("\n  TELL 3 -- THE NOISE TELL (stub sec. 2.7 and 7.3).")
    print("     A separation that STRENGTHENS from B=21 to B=63 reads variance shape; one that")
    print("     WEAKENS reads estimation noise.")
    for name in SHAPE_FUNCTIONALS:
        stronger = int((grid[f"{name}_b63"] > grid[f"{name}_b21"]).sum())
        print(f"     {name}: stronger at B=63 in {stronger} of {len(grid)} cells")

    print("\n  THE LAMBDA-DIRECTION PREDICTION, stated as a single verdict per functional:")
    for name in SHAPE_FUNCTIONALS:
        r21, f21, _ = direction[f"{name}_b21"]
        r63, f63, _ = direction[f"{name}_b63"]
        verdict = ("HELD" if (r21 + r63) > (f21 + f63)
                   else "CONTRADICTED -- behaves like S0's T3" if (f21 + f63) > (r21 + r63)
                   else "INDETERMINATE")
        print(f"     {name}: {verdict}")

    print("\n" + "-" * 108)
    if not survivors:
        best = max((grid[f"{n}_b{b}"].max(), f"{n}_b{b}")
                   for b in BLOCKS for n in SHAPE_FUNCTIONALS)
        print("  H(S0b) IS FALSIFIED.  No shape functional clears the threshold and its own mismatch")
        print(f"  floor anywhere in the declared sweep. Best raw: {best[1]} at d' = {best[0]:.2f}.")
        print()
        print("  ==> FAIL.  CHARTER section 6: the programme TERMINATES as INDETERMINATE.")
        print("      There is no S0c. No market data is read. The negative that stands is:")
        print("      the discreteness of the return-generating environment is not identifiable from")
        print("      a single daily history at this sample size, once every easier difference is")
        print("      matched away.")
        return

    by_functional = {}
    for s in survivors:
        by_functional.setdefault(s["f"], []).append(s)
    winner = max(survivors, key=lambda x: x["d"])
    cells = {(s["kappa"], s["pi2"], s["lambda"]) for s in survivors}
    if corner:
        print("  ==> FAIL (disqualified by tell 1).  Survival is confined to the extreme corner, so")
        print("      the functional measures the PARAMETERS, not the structure.")
        print("      CHARTER section 6: the programme TERMINATES as INDETERMINATE.")
        return

    print(f"  H(S0b) SURVIVES on {winner['f']} at B={winner['B']}, d' = {winner['d']:.2f}")
    print(f"  (kappa={winner['kappa']:.1f}, pi2={winner['pi2']:.2f}, lambda={winner['lambda']:.3f}).")
    print(f"  Surviving functionals: {sorted(by_functional)}   distinct cells: {len(cells)} "
          f"of {len(grid)}")
    print()
    print("  ==> PASS, subject to the tells above being read together with it.")
    print("      CHARTER section 6 / stub section 8.1: this licenses THE DESIGN OF Q1 AND NOTHING")
    print("      ELSE. Not its execution. Q1 inherits this null, this functional, this block length,")
    print("      this void rule and the power clause, and may not reopen the identification")
    print("      question. Structural breaks and long memory remain outside the null.")


def report() -> None:
    rng = np.random.default_rng(SEED)
    rows, infeasible = [], []
    for kappa in KAPPAS:
        for pi2 in PI2S:
            for lam in LAMBDAS:
                row = run_cell(kappa, pi2, lam, rng)
                if row is None:
                    infeasible.append(f"INFEASIBLE  kappa={kappa} pi2={pi2} lambda={lam}")
                else:
                    rows.append(row)

    print()
    print("S0b -- THE DISCRETENESS GATE.  THE FINAL SYNTHETIC IDENTIFICATION GATE.")
    print(f"Preregistered: closed-research/return-states/STUB-S0B-DISCRETENESS-GATE.md   seed {SEED}   "
          f"{REPLICATIONS} replications/class/cell")
    print("NO MARKET DATA. This experiment cannot produce a finding about equities.")
    print()

    if not rows:
        print("EVERY CELL IS INFEASIBLE. The null family cannot reach the alternative's variance")
        print("dispersion anywhere in the declared sweep.")
        for cell in infeasible:
            print(f"  {cell}")
        print("\n  ==> FAIL. CHARTER section 6: the programme TERMINATES as INDETERMINATE.")
        return

    grid = pd.DataFrame(rows)
    block_1_matching(grid, infeasible)
    control_ok = block_2_control(grid)
    block_3_separation(grid)
    block_4_verdict(grid, control_ok)
    print()


if __name__ == "__main__":
    report()
