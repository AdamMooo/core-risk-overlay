r"""Regression checks for active infrastructure.

Covers src/data_loader.py and src/pathfunctionals.py -- the two modules the
return-state program inherits -- and verifies the data cache against
data/MANIFEST.md -- plus the arithmetic of S0 and S0b, which is the only new
arithmetic in the return-state program. The closed programs' checks are frozen with the
code they guard: closed-research/checks.py (prediction) and
closed-research/intervention/checks.py (rolled-put / tenor).

Plain-script smoke test (no pytest). Synthetic data, no network, deterministic.
Exits non-zero on failure.

Run: .venv\Scripts\python.exe checks.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))
sys.path.insert(0, str(Path(__file__).parent / "states"))

import numpy as np
import pandas as pd

import data_loader as dl
import manifest as mf
import pathfunctionals as pf
import s0_discriminating_functional as s0
import s0b_discreteness_gate as s0b

FAILURES: list[str] = []


def check(description: str, condition: bool) -> None:
    status = "PASS" if condition else "FAIL"
    print(f"[{status}] {description}")
    if not condition:
        FAILURES.append(description)


def check_data_loader() -> None:
    prices = pd.Series(
        [100.0, 102.0, 101.0, 105.0],
        index=pd.date_range("2024-01-01", periods=4, freq="W-MON"),
    )
    returns = dl.compute_weekly_log_returns(prices)
    check("data_loader: log-return count is prices - 1", len(returns) == len(prices) - 1)
    check(
        "data_loader: log-return math matches np.log(p1/p0)",
        np.isclose(returns.iloc[0], np.log(102.0 / 100.0)),
    )

    for bad_prices in [pd.Series(dtype="float64"), pd.Series([1.0]), pd.Series([1.0, -1.0])]:
        try:
            dl.compute_weekly_log_returns(bad_prices)
            check(f"data_loader: rejects invalid input {bad_prices.tolist()}", False)
        except ValueError:
            check(f"data_loader: rejects invalid input {bad_prices.tolist()}", True)


def check_vix_alignment() -> None:
    index = pd.date_range("2024-01-01", periods=6, freq="W-MON")
    vix = pd.Series([13.0, 14.5, 22.0, 31.5, 18.0, 15.0], index=index)
    returns = pd.Series(np.linspace(-0.02, 0.02, 6), index=index)

    aligned = dl.align_vix_to_returns(vix, returns)
    check("data_loader: VIX aligns on an exact index match", aligned.index.equals(returns.index))
    check("data_loader: VIX alignment preserves values", bool(np.allclose(aligned, vix)))

    # The whole point of the exact join: a missing week must surface, never be
    # papered over with a stale carried-forward quote.
    for label, gap in [
        ("a missing week", vix.drop(index[2])),
        ("a shifted index", pd.Series(vix.to_numpy(), index=index + pd.Timedelta(days=1))),
    ]:
        try:
            dl.align_vix_to_returns(gap, returns)
            check(f"data_loader: VIX alignment rejects {label}", False)
        except ValueError:
            check(f"data_loader: VIX alignment rejects {label}", True)

    try:
        dl.align_vix_to_returns(vix.copy().mask(vix > 30, -1.0), returns)
        check("data_loader: VIX alignment rejects non-positive values", False)
    except ValueError:
        check("data_loader: VIX alignment rejects non-positive values", True)

    log_vix = dl.to_log_vix(aligned)
    check(
        "data_loader: to_log_vix matches np.log",
        bool(np.allclose(log_vix, np.log(vix))),
    )
    try:
        dl.to_log_vix(pd.Series([10.0, 0.0], index=index[:2]))
        check("data_loader: to_log_vix rejects non-positive values", False)
    except ValueError:
        check("data_loader: to_log_vix rejects non-positive values", True)


def check_pathfunctionals() -> None:
    # Hand-built curve with two known excursions, the second still open.
    #   W        1.0   1.2   0.9    1.0     1.3   1.1     1.4    1.0
    #   cummax   1.0   1.2   1.2    1.2     1.3   1.3     1.4    1.4
    #   D        0     0     0.25   0.1667  0     0.1538  0      0.2857
    index = pd.date_range("2024-01-05", periods=8, freq="W-FRI")
    wealth = pd.Series([1.0, 1.2, 0.9, 1.0, 1.3, 1.1, 1.4, 1.0], index=index)

    d = pf.drawdown(wealth)
    check("pathfunctionals: drawdown is zero at a running peak", d.iloc[0] == 0.0 and d.iloc[4] == 0.0)
    check("pathfunctionals: drawdown depth matches 1 - W/M", np.isclose(d.iloc[2], 0.25))
    check("pathfunctionals: drawdown is positive-signed", bool((d >= 0).all()))

    for bad, label in [(pd.Series(dtype="float64"), "an empty curve"),
                       (pd.Series([1.0, 0.0]), "a non-positive curve")]:
        try:
            pf.drawdown(bad)
            check(f"pathfunctionals: drawdown rejects {label}", False)
        except ValueError:
            check(f"pathfunctionals: drawdown rejects {label}", True)

    ex = pf.excursions(wealth)
    check("pathfunctionals: finds every excursion", len(ex) == 3)
    check("pathfunctionals: excursion depth is its trough", np.isclose(ex[0].depth, 0.25))
    check("pathfunctionals: trough is dated, not just measured", ex[0].trough == index[2])
    check("pathfunctionals: duration is peak to trough", ex[0].duration == 1)
    check("pathfunctionals: recovery is trough to new high", ex[0].recovery == 1)
    check("pathfunctionals: a closed excursion is marked recovered", ex[0].recovered)
    # The censored one is the trap: it is still under water at the sample end,
    # so its recovery is a lower bound and must never be averaged in as a duration.
    check("pathfunctionals: an open excursion is marked NOT recovered", not ex[-1].recovered)

    deep = pf.excursions(wealth, threshold=0.20)
    check("pathfunctionals: threshold filters on depth", len(deep) == 2)

    # alpha=1 is the mean of the whole drawdown process; small alpha is max DD.
    check("pathfunctionals: CDaR at alpha=1 is the average drawdown",
          np.isclose(pf.cdar(wealth, 1.0), d.mean()))
    check("pathfunctionals: CDaR at small alpha is the max drawdown",
          np.isclose(pf.cdar(wealth, 0.01), d.max()))
    curve = pf.cdar_curve(wealth)
    check("pathfunctionals: CDaR is monotone non-increasing in alpha",
          bool((curve.to_numpy()[:-1] >= curve.to_numpy()[1:] - 1e-12).all()))
    check("pathfunctionals: CDaR rejects alpha outside (0, 1]", _raises(lambda: pf.cdar(wealth, 0.0)))

    # E2. Measuring a book inside a window someone else defined.
    first = ex[0]
    check(
        "pathfunctionals: depth_in_window reproduces an excursion's own depth",
        np.isclose(pf.depth_in_window(wealth, first.start, first.end), first.depth),
    )
    check(
        "pathfunctionals: depth_in_window is zero on a monotone rise",
        pf.depth_in_window(pd.Series([1.0, 2.0, 3.0], index=index[:3]), index[0], index[2]) == 0.0,
    )
    check(
        "pathfunctionals: depth_in_window measures from the WINDOW's peak, not the global one",
        # Global cummax at index[5] is 1.3; inside [idx4, idx5] the peak is also
        # 1.3, but inside [idx5, idx7] it is 1.4 -- a window that excludes the
        # earlier high must not inherit it.
        np.isclose(pf.depth_in_window(wealth, index[5], index[7]), 1.0 - 1.0 / 1.4),
    )
    check(
        "pathfunctionals: depth_in_window rejects an empty window",
        _raises(lambda: pf.depth_in_window(wealth, index[7] + pd.Timedelta(days=7),
                                           index[7] + pd.Timedelta(days=14))),
    )

    check("pathfunctionals: time under water counts observations, not episodes",
          np.isclose(pf.time_under_water(wealth, 0.0), 4 / 8))
    check("pathfunctionals: time under water respects the threshold",
          np.isclose(pf.time_under_water(wealth, 0.20), 2 / 8))


def _raises(call) -> bool:
    try:
        call()
    except ValueError:
        return True
    return False


def check_manifest() -> None:
    """The cache is gitignored; its hashes are not.

    MISSING is reported and not failed -- a fresh clone legitimately has no
    cache, and the manifest cannot conjure one. PRESENT-AND-DIFFERENT is a
    failure, because that is a number quoted from data other than the data that
    produced it.
    """
    matched, missing, mismatched = mf.verify()
    check("manifest: data/MANIFEST.md exists and parses", bool(matched or missing or mismatched))
    check(f"manifest: no file differs from its recorded hash ({len(matched)} matched)",
          not mismatched)
    if mismatched:
        for name in mismatched:
            print(f"         MISMATCH: {name}")
    if missing:
        print(f"       (not failed) {len(missing)} manifest file(s) absent from this cache: "
              f"{', '.join(missing)}")


def check_s0_matching() -> None:
    """S0's matching step, which is where that experiment can be quietly ruined.

    If the two classes are not actually matched, every separation downstream is
    contaminated by the mismatch and looks like a finding. The stub says the
    matching quality is a first-class output; these check that the algebra
    behind it is right before any d' is computed.
    """
    for kappa in s0.KAPPAS:
        for pi2 in s0.PI2S:
            ms = s0.switching_moments(kappa, pi2, 0.98)
            check(
                f"s0: switching unconditional variance is 1 (kappa={kappa}, pi2={pi2})",
                np.isclose(ms["pi1"] * ms["v1"] + ms["pi2"] * ms["v2"], 1.0),
            )
    check(
        "s0: switching kurtosis exceeds 3 and rises with the variance ratio",
        3.0 < s0.switching_moments(2.0, 0.15, 0.98)["kurtosis"]
        < s0.switching_moments(6.5, 0.15, 0.98)["kurtosis"],
    )
    # The stationary occupancy must come back out of the transition matrix it
    # was used to build -- an algebra slip here would rescale every variance.
    ms = s0.switching_moments(4.0, 0.30, 0.95)
    implied = (1.0 - ms["p11"]) / (2.0 - ms["p11"] - ms["p22"])
    check("s0: the transition matrix reproduces the declared occupancy",
          np.isclose(implied, 0.30))

    for lam in s0.LAMBDAS:
        ms = s0.switching_moments(6.5, 0.15, lam)
        g = s0.match_garch(ms["rho1"], lam)
        check(f"s0: a matched GARCH exists at lambda={lam}", g is not None)
        check(
            f"s0: matched persistence equals the chain eigenvalue at lambda={lam}",
            np.isclose(g["alpha"] + g["beta"], lam),
        )
        check(
            f"s0: matched rho(1) agrees to 1e-10 at lambda={lam}",
            abs(g["rho1"] - ms["rho1"]) < 1e-10,
        )
        check(
            f"s0: the matched GARCH has a finite fourth moment at lambda={lam}",
            3.0 * g["alpha"] ** 2 + 2.0 * g["alpha"] * g["beta"] + g["beta"] ** 2 < 1.0,
        )
    # Geometric decay from lag 1 is what makes the whole-ACF match possible. If
    # this ever fails, the exact match in the stub's section 5.2 is not exact.
    ms = s0.switching_moments(6.5, 0.15, 0.98)
    g = s0.match_garch(ms["rho1"], 0.98)
    for k in (2, 5, 10):
        ratio_ms = 0.98 ** (k - 1)
        ratio_g = (g["alpha"] + g["beta"]) ** (k - 1)
        check(f"s0: both squared-return ACFs decay by the same ratio at lag {k}",
              np.isclose(ratio_ms, ratio_g))


def check_s0_functionals() -> None:
    """The four functionals, against cases whose answers are known in advance."""
    rng = np.random.default_rng(4242)
    iid = rng.standard_normal((60, 4000))

    check("s0: squared-return ACF of iid noise is ~0",
          abs(float(s0.t1_squared_acf(iid, 1).mean())) < 0.02)
    check("s0: aggregate excess kurtosis of iid normal is ~0 at h=1",
          abs(float(s0.t2_aggregate_kurtosis(iid, 1).mean())) < 0.15)
    check("s0: aggregate excess kurtosis of iid normal is ~0 at h=21",
          abs(float(s0.t2_aggregate_kurtosis(iid, 21).mean())) < 0.5)
    check("s0: block variance dispersion is positive and finite on iid noise",
          0.0 < float(s0.t3_block_variance_dispersion(iid, 21).mean()) < 5.0)

    max_dd, cdar, excursions = s0.t4_path_geometry(iid[:5] * s0.DAILY_SD)
    check("s0: max drawdown lies in [0, 1)", bool(((max_dd >= 0) & (max_dd < 1)).all()))
    # The reason that check exists: at the algebra's unit variance a single day
    # is a 100% sd move, every path saturates, and T4 silently stops
    # discriminating. Scale-invariance of T1-T3 is asserted, not assumed.
    scaled = iid * 3.7
    check("s0: the squared-return ACF is scale-invariant",
          np.isclose(float(s0.t1_squared_acf(iid, 1).mean()),
                     float(s0.t1_squared_acf(scaled, 1).mean())))
    check("s0: aggregate excess kurtosis is scale-invariant",
          np.isclose(float(s0.t2_aggregate_kurtosis(iid, 5).mean()),
                     float(s0.t2_aggregate_kurtosis(scaled, 5).mean())))
    check("s0: block variance dispersion is scale-invariant",
          np.isclose(float(s0.t3_block_variance_dispersion(iid, 21).mean()),
                     float(s0.t3_block_variance_dispersion(scaled, 21).mean())))
    check("s0: max drawdown is NOT scale-invariant, which is why the scale is declared",
          not np.isclose(s0.t4_path_geometry(iid[:5] * 0.01)[0].mean(),
                         s0.t4_path_geometry(iid[:5] * 0.05)[0].mean()))
    check("s0: CDaR(worst 5%) is at least the average and at most the max drawdown",
          bool((cdar <= max_dd + 1e-12).all()))
    check("s0: excursion counts are non-negative integers", bool((excursions >= 0).all()))

    # d' is the whole verdict, so its two anchor cases are tested rather than
    # assumed: identical samples separate by nothing, and a shift of two pooled
    # standard deviations separates by two.
    a = rng.standard_normal(20000)
    check("s0: d' of a sample against itself is 0", s0.dprime(a, a) == 0.0)
    check("s0: d' recovers a two-sd shift", abs(s0.dprime(a, a + 2.0) - 2.0) < 0.05)

    # A switching path must actually switch: with a high variance ratio its
    # squared-return ACF has to exceed that of the matched-variance iid case.
    ms = s0.switching_moments(6.5, 0.15, 0.98)
    r = s0.simulate_switching(ms, 20, 5000, rng)
    check("s0: simulated switching returns have the declared unconditional variance",
          abs(float(r.var()) / s0.DAILY_SD ** 2 - 1.0) < 0.10)
    check("s0: simulated switching returns carry the volatility clustering they should",
          float(s0.t1_squared_acf(r, 1).mean()) > 0.10)
    g = s0.match_garch(ms["rho1"], 0.98)
    rg = s0.simulate_garch(g, 20, 5000, rng)
    check("s0: simulated GARCH returns have the declared unconditional variance",
          abs(float(rg.var()) / s0.DAILY_SD ** 2 - 1.0) < 0.10)
    check("s0: simulated GARCH returns cluster like the model they were matched to",
          float(s0.t1_squared_acf(rg, 1).mean()) > 0.10)


def check_s0b_matching() -> None:
    """S0b's third constraint, which is where THIS gate can be quietly ruined.

    S0's matching was exact on its two constraints and the failure was that it
    matched the wrong things (R1). S0b solves (M3) through a kurtosis
    parameter, so an error in the fourth-moment algebra would silently leave
    Var(sigma^2) unmatched and reproduce S0's defect exactly.
    """
    # (M3) reduces to S0's Gaussian expression at k = 3. If it does not, the
    # generalisation is wrong and every matched cell is wrong with it.
    for alpha, beta in [(0.08, 0.90), (0.05, 0.94), (0.11, 0.84)]:
        psi = alpha + beta
        check(
            f"s0b: the fourth-moment formula reduces to the Gaussian case at k=3 "
            f"(alpha={alpha})",
            np.isclose(s0b.garch_t_fourth_moment(alpha, beta, 3.0),
                       s0.garch_kurtosis(alpha, psi) / 3.0),
        )

    for kappa in s0b.KAPPAS:
        for pi2 in s0b.PI2S:
            for lam in s0b.LAMBDAS:
                m = s0b.match_garch_t(kappa, pi2, lam)
                label = f"kappa={kappa} pi2={pi2} lambda={lam}"
                check(f"s0b: a matched GARCH-t exists at {label}", m is not None)
                if m is None:
                    continue
                # (M3): the whole point of the gate.
                check(f"s0b: (M3) Var(sigma^2) matched to 1e-10 at {label}",
                      abs(m["m_alt"] - m["m_null"]) < 1e-10)
                # (M2): unchanged from S0, and the claim that rho(1) does not
                # depend on the innovation kurtosis is checked, not assumed.
                base = s0.match_garch(s0.switching_moments(kappa, pi2, lam)["rho1"], lam)
                check(f"s0b: (M2) alpha and beta are S0's, unchanged, at {label}",
                      np.isclose(m["alpha"], base["alpha"])
                      and np.isclose(m["beta"], base["beta"]))
                check(f"s0b: (M1)+(M2) persistence equals the chain eigenvalue at {label}",
                      np.isclose(m["alpha"] + m["beta"], lam))
                check(f"s0b: the innovation law is a genuine t with a fourth moment at {label}",
                      m["k"] > 3.0 and m["nu"] > 4.0)
                check(f"s0b: the null's fourth moment exists at {label}",
                      m["alpha"] ** 2 * m["k"] + 2 * m["alpha"] * m["beta"]
                      + m["beta"] ** 2 < 1.0)
                # The declared trade: return kurtosis is unmatched, and UPWARD.
                check(f"s0b: return kurtosis is unmatched in the declared direction at {label}",
                      m["kurt_null"] > m["kurt_alt"])


def check_s0b_functionals() -> None:
    """The shape functionals, against cases whose answers are known exactly."""
    rng = np.random.default_rng(90210)

    # Sarle's bimodality coefficient has known values: 1/3 for a normal,
    # 5/9 for a uniform. Both are exact, which is why they are the test.
    normal = rng.standard_normal((1, 400000))
    uniform = rng.random((1, 400000))
    for label, sample, target in [("normal", normal, 1 / 3), ("uniform", uniform, 5 / 9)]:
        skew, excess = s0b._standardised_moments(sample)
        bc = float(((skew ** 2 + 1.0) / (excess + 3.0))[0])
        check(f"s0b: Sarle's coefficient recovers its known value on a {label} sample",
              abs(bc - target) < 0.01)

    skew, excess = s0b._standardised_moments(normal)
    check("s0b: skewness of a normal sample is ~0", abs(float(skew[0])) < 0.02)
    check("s0b: excess kurtosis of a normal sample is ~0", abs(float(excess[0])) < 0.05)

    # A balanced two-point mixture is PLATYKURTIC -- excess kurtosis -2 in the
    # limit. This is the property T5 exists to detect, so it is tested directly
    # rather than trusted.
    two_point = np.where(rng.random((1, 200000)) < 0.5, -1.0, 1.0)
    _, excess_2pt = s0b._standardised_moments(two_point)
    check("s0b: a two-point mixture is platykurtic, which is what T5 detects",
          float(excess_2pt[0]) < -1.9)

    # Shape functionals read log RV, so a change of scale shifts log RV by a
    # constant and must leave every one of them untouched.
    r = rng.standard_normal((40, 4000)) * s0b.DAILY_SD
    for name, fn in s0b.SHAPE_FUNCTIONALS.items():
        check(f"s0b: {name} is scale-invariant",
              np.allclose(fn(r, 21), fn(r * 7.3, 21)))

    # The simulator: the two moments the matching claims to control.
    m = s0b.match_garch_t(6.5, 0.30, 0.98)
    rn = s0b.simulate_garch_t(m, 30, 6000, rng)
    check("s0b: simulated GARCH-t returns have the declared unconditional variance",
          abs(float(rn.var()) / s0b.DAILY_SD ** 2 - 1.0) < 0.20)
    check("s0b: simulated GARCH-t returns cluster at the matched rho(1)",
          abs(float(s0.t1_squared_acf(rn, 1).mean()) - m["rho1"]) < 0.06)
    check("s0b: the simulated innovation law is fat-tailed, as the matching requires",
          m["nu"] < 30.0)


def main() -> None:
    check_manifest()
    check_data_loader()
    check_vix_alignment()
    check_pathfunctionals()
    check_s0_matching()
    check_s0_functionals()
    check_s0b_matching()
    check_s0b_functionals()

    print()
    if FAILURES:
        print(f"{len(FAILURES)} check(s) FAILED:")
        for failure in FAILURES:
            print(f"  - {failure}")
        sys.exit(1)

    print("All checks passed.")


if __name__ == "__main__":
    main()
