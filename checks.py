r"""Regression checks for active infrastructure.

Covers src/data_loader.py, src/pathfunctionals.py, and -- since D4 -- the
Shu-Yu-Mulvey reproduction modules src/jumpmodel.py and src/sjm_features.py;
and verifies the data cache against data/MANIFEST.md. There is no active
research programme; the three closed programmes carry their own suites, frozen
with the code they guard: closed-research/checks.py (prediction) and
closed-research/intervention/checks.py (rolled-put / tenor).

The jump-model checks are the in-repo half of D4: the dynamic programme
verified against brute-force enumeration (deductive), and state recovery on
synthetic data with known regimes (statistical). The third leg -- exact
equivalence against the authors' `jumpmodels` package, including the lambda
convention -- needs the third-party package and lives in d4_crosscheck.py.

Plain-script smoke test (no pytest). Synthetic data, no network, deterministic.
Exits non-zero on failure.

Run: .venv\Scripts\python.exe checks.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

import numpy as np
import pandas as pd

import itertools

import data_loader as dl
import jumpmodel as jm
import ledoitwolf as lw
import manifest as mf
import pathfunctionals as pf
import sjm_features as sf

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


def _path_cost(D: np.ndarray, path: np.ndarray, lam: float) -> float:
    T = len(D)
    return float(D[np.arange(T), path].sum() + lam * np.count_nonzero(np.diff(path)))


def _brute_force(D: np.ndarray, lam: float) -> tuple[float, np.ndarray]:
    """Minimum cost over ALL K^T state paths, and the per-(t, k) prefix costs.

    Exponential and therefore only usable at toy sizes -- which is the point:
    it shares no code and no idea with the dynamic programme it certifies.
    """
    T, K = D.shape
    best_cost = np.inf
    prefix = np.full((T, K), np.inf)
    for path in itertools.product(range(K), repeat=T):
        p = np.asarray(path)
        running = D[0, p[0]]
        prefix[0, p[0]] = min(prefix[0, p[0]], running)
        for t in range(1, T):
            running += D[t, p[t]] + (lam if p[t] != p[t - 1] else 0.0)
            prefix[t, p[t]] = min(prefix[t, p[t]], running)
        best_cost = min(best_cost, running)
    return best_cost, prefix


def check_jumpmodel_dp() -> None:
    """Deductive half of D4: the optimizer solves the problem it claims to."""
    rng = np.random.default_rng(42)

    # Endpoints of the penalty. At lambda=0 the path is the per-row argmin
    # (k-means assignment); at lambda=inf it is one state for the whole sample,
    # the one with the smallest column sum.
    D = rng.uniform(0.0, 4.0, size=(40, 3))
    check("jumpmodel: viterbi at lambda=0 is the per-row argmin",
          bool(np.array_equal(jm.viterbi_path(D, 0.0), D.argmin(axis=1))))
    huge = jm.viterbi_path(D, 1e9)
    check("jumpmodel: viterbi at huge lambda is constant at the best column",
          len(set(huge.tolist())) == 1 and huge[0] == int(D.sum(axis=0).argmin()))

    # The gold-standard check: against enumeration of every path, at penalties
    # where the switch decision is genuinely contested.
    exact_path, exact_prefix, exact_online = True, True, True
    for trial in range(5):
        D = rng.uniform(0.0, 4.0, size=(7, 3))
        for lam in (0.3, 1.0, 3.0):
            best_cost, prefix = _brute_force(D, lam)
            vp = jm.viterbi_path(D, lam)
            exact_path &= np.isclose(_path_cost(D, vp, lam), best_cost)
            V = jm.forward_costs(D, lam)
            exact_prefix &= bool(np.allclose(V, prefix))
            exact_online &= bool(np.array_equal(V.argmin(axis=1), prefix.argmin(axis=1)))
    check("jumpmodel: viterbi cost equals brute-force optimum (15 instances)", exact_path)
    check("jumpmodel: forward costs equal brute-force prefix costs", exact_prefix)
    check("jumpmodel: online state equals brute-force prefix argmin", exact_online)

    # Fit self-consistency at lambda=0: the fixed point of coordinate descent
    # is exactly a k-means fixed point -- states are nearest-centroid and
    # centroids are member means.
    X = np.concatenate([rng.normal(-2.0, 0.5, (60, 2)), rng.normal(2.0, 0.5, (60, 2))])
    states, centroids, _ = jm.fit_jump_model(X, k=2, jump_penalty=0.0, seed=1)
    nearest = np.array([((X - c) ** 2).sum(axis=1) for c in centroids]).argmin(axis=0)
    means_ok = all(
        np.allclose(centroids[j], X[states == j].mean(axis=0)) for j in range(2)
    )
    check("jumpmodel: fit at lambda=0 is a k-means fixed point",
          bool(np.array_equal(states, nearest)) and means_ok)


def _simulate_states(rng: np.random.Generator, T: int, p_stay: tuple[float, float]) -> np.ndarray:
    states = np.empty(T, dtype=np.int64)
    s = 0
    for t in range(T):
        states[t] = s
        if rng.random() > p_stay[s]:
            s = 1 - s
    return states


def _best_permutation_accuracy(found: np.ndarray, truth: np.ndarray) -> float:
    direct = float((found == truth).mean())
    return max(direct, 1.0 - direct)


def check_jumpmodel_recovery() -> None:
    """Statistical half of D4: known states in, same states out."""
    rng = np.random.default_rng(7)

    # Directly in feature space: two persistent states, Gaussian emissions
    # separated by ~3 sigma. This verifies the optimizer as an estimator,
    # with no feature pipeline in the loop.
    T = 1500
    truth = _simulate_states(rng, T, (0.99, 0.99))
    means = np.array([[0.0, 0.0, 0.0], [1.8, 1.8, 1.8]])
    X = rng.standard_normal((T, 3)) + means[truth]
    Xs = (X - X.mean(axis=0)) / X.std(axis=0)
    states, centroids, _ = jm.fit_jump_model(Xs, k=2, jump_penalty=30.0, seed=0)
    order = jm.order_states_by(centroids, 0)
    relabeled = np.argsort(order)[states]
    acc = _best_permutation_accuracy(relabeled, truth)
    check(f"jumpmodel: recovers known states in feature space (acc {acc:.3f} >= 0.95)",
          acc >= 0.95)

    # End to end through the SJM feature pipeline: regime-switching returns ->
    # build_features -> standardize -> fit. The state path is deterministic
    # blocks rather than a simulated chain, because two resolution constraints
    # bound the pipeline, not the code: the EWM features lag a switch (accuracy
    # is scored away from switch dates) and cannot resolve regimes shorter than
    # their own memory (the 60d Sortino halflife). A random chain that happens
    # to draw short bear segments blurs the centroids together and the check
    # would then measure the draw, not the implementation.
    blocks = [(0, 500), (1, 150), (0, 600), (1, 250), (0, 700),
              (1, 120), (0, 800), (1, 200), (0, 680)]
    truth = np.concatenate([np.full(n, s, dtype=np.int64) for s, n in blocks])
    T = len(truth)
    returns = pd.Series(
        np.where(truth == 0,
                 rng.normal(4e-4, 0.007, T),
                 rng.normal(-8e-4, 0.02, T)),
        index=pd.bdate_range("2000-01-03", periods=T),
    )
    features = sf.build_features(returns)
    truth_series = pd.Series(truth, index=returns.index).reindex(features.index)

    Xf = features.to_numpy()
    Xs = (Xf - Xf.mean(axis=0)) / Xf.std(axis=0)
    states, centroids, _ = jm.fit_jump_model(Xs, k=2, jump_penalty=50.0, seed=0)
    order = jm.order_states_by(centroids, sf.DOWNSIDE_FEATURE)
    relabeled = np.argsort(order)[states]  # 0 = low downside deviation = calm

    check("jumpmodel: mechanical naming puts the high-downside state last",
          centroids[order][1, sf.DOWNSIDE_FEATURE] > centroids[order][0, sf.DOWNSIDE_FEATURE])

    switch_dates = truth_series.index[truth_series.diff().abs() > 0]
    away = pd.Series(True, index=truth_series.index)
    for d in switch_dates:
        i = truth_series.index.get_loc(d)
        away.iloc[max(0, i - 20): i + 21] = False
    mask = away.to_numpy()
    acc = float((relabeled[mask] == truth_series.to_numpy()[mask]).mean())
    check(f"jumpmodel: recovers known states through the feature pipeline "
          f"(acc {acc:.3f} >= 0.93 away from switches)", acc >= 0.93)

    # Online inference: equality of the online state with the offline path's
    # last state is a theorem (both are argmin_k V(T,k)) and is checked exactly.
    # Agreement along the path is NOT a theorem -- the online label sequence is
    # not itself a single path and can chatter where the offline optimum holds
    # steady -- so mid-path agreement is a sanity band, not an identity.
    online = jm.online_states(Xs, centroids, 50.0)
    offline = jm.viterbi_path(
        ((Xs[:, None, :] - centroids[None, :, :]) ** 2).sum(axis=2), 50.0
    )
    check("jumpmodel: online state at the sample end equals the offline optimum",
          online[-1] == offline[-1])
    check(f"jumpmodel: online tracks offline along the path "
          f"({(online == offline).mean():.3f} >= 0.90, sanity band)",
          float((online == offline).mean()) >= 0.90)


def check_sjm_features() -> None:
    index = pd.bdate_range("2024-01-01", periods=5)
    up = pd.Series([0.01, 0.02, 0.01, 0.03, 0.02], index=index)
    check("sjm_features: downside deviation of an all-positive series is zero",
          bool((sf.downside_deviation(up, 10) == 0.0).all()))
    check("sjm_features: sortino is NaN (not inf) when downside is zero",
          bool(sf.sortino_ratio(up, 10).isna().all()))

    # Hand computation, adjust=True EWM: dd^2(t) = sum w_i r_i^2 1{r_i<0} / sum w_i
    # with w_i = alpha_decay^(t-i) and alpha_decay = (1/2)^(1/halflife).
    r = pd.Series([-0.02, 0.01, -0.01], index=index[:3])
    decay = 0.5 ** (1.0 / 10)
    num = (decay**2) * 0.02**2 + 0.01**2
    den = decay**2 + decay + 1.0
    check("sjm_features: downside deviation matches the hand-computed EWM",
          np.isclose(sf.downside_deviation(r, 10).iloc[-1], np.sqrt(num / den)))


def check_ledoitwolf_grad() -> None:
    """The delta-method gradient, against a numerical derivative of f itself.

    This is the check that catches a transcribed sign. A gradient that is wrong
    in one entry still produces a plausible-looking standard error.
    """
    v = np.array([5.0e-4, 3.0e-4, 1.0e-4, 9.0e-5])
    grad = lw.sharpe_grad(v)
    check("ledoitwolf: gradient has shape (4,)", np.shape(grad) == (4,))

    numerical = np.empty(4)
    for k in range(4):
        step = 1.0e-6 * abs(v[k])
        up, down = v.copy(), v.copy()
        up[k] += step
        down[k] -= step
        numerical[k] = (lw.sharpe_difference(up) - lw.sharpe_difference(down)) / (2.0 * step)
    check("ledoitwolf: gradient matches a central difference of f",
          bool(np.allclose(grad, numerical, rtol=1e-4)))

    same = np.array([5.0e-4, 5.0e-4, 1.0e-4, 1.0e-4])
    g = lw.sharpe_grad(same)
    check("ledoitwolf: identical moments give equal-and-opposite mean terms",
          bool(np.isclose(g[0], -g[1]) and np.isclose(g[2], -g[3])))


def check_ledoitwolf_block_psi() -> None:
    """Their footnote 9: at b = 1 the block estimator IS the sample covariance."""
    rng = np.random.default_rng(0)
    y = rng.standard_normal((600, 4))
    y = y - y.mean(axis=0)

    psi1 = lw.block_psi(y, 1)
    check("ledoitwolf: block_psi at b=1 is the sample covariance",
          bool(np.allclose(psi1, np.cov(y.T, bias=True), atol=1e-12)))

    psi5 = lw.block_psi(y, 5)
    check("ledoitwolf: block_psi is symmetric", bool(np.allclose(psi5, psi5.T)))
    check("ledoitwolf: block_psi is positive semi-definite",
          bool(np.linalg.eigvalsh(psi5).min() > -1e-10))
    check("ledoitwolf: block_psi discards the ragged tail, not wraps it",
          bool(np.allclose(lw.block_psi(y[:600], 7), lw.block_psi(y[: 7 * (600 // 7)], 7))))


def check_ledoitwolf_resampler() -> None:
    rng = np.random.default_rng(0)
    idx = lw.circular_block_indices(100, 7, rng)
    check("ledoitwolf: resample has the sample's length", len(idx) == 100)
    check("ledoitwolf: resample indices stay in range",
          bool(idx.min() >= 0 and idx.max() < 100))

    wrapped = lw.circular_block_indices(20, 20, np.random.default_rng(1))
    check("ledoitwolf: a full-length block is a rotation (the circular part)",
          sorted(wrapped.tolist()) == list(range(20)))

    a = lw.circular_block_indices(50, 5, np.random.default_rng(3))
    b = lw.circular_block_indices(50, 5, np.random.default_rng(3))
    check("ledoitwolf: the resampler is deterministic given the generator",
          bool(np.array_equal(a, b)))

    counts = np.zeros(40)
    for seed in range(400):
        counts += np.bincount(lw.circular_block_indices(40, 6, np.random.default_rng(seed)),
                              minlength=40)
    check("ledoitwolf: every observation is equally likely (no edge effect)",
          bool(counts.std() / counts.mean() < 0.06))


def check_ledoitwolf_test() -> None:
    """Behaviour of the whole test on constructed data, both directions."""
    rng = np.random.default_rng(7)
    base = rng.standard_normal(2000) * 0.01 + 5.0e-4

    same = lw.studentized_pvalue(base, rng.standard_normal(2000) * 0.01 + 5.0e-4,
                                 block=5, n_boot=199, rng=np.random.default_rng(1))
    check("ledoitwolf: p-value is a probability",
          0.0 < same["pvalue"] <= 1.0)
    check("ledoitwolf: p-value granularity is 1/(M+1)",
          bool(np.isclose(same["pvalue"] * 200.0, round(same["pvalue"] * 200.0))))
    check("ledoitwolf: equal-Sharpe series are not distinguished",
          same["pvalue"] > 0.05)

    shifted = lw.studentized_pvalue(base, base - 4.0e-4,
                                    block=5, n_boot=199, rng=np.random.default_rng(1))
    check("ledoitwolf: a deterministic mean shift IS distinguished",
          shifted["pvalue"] < 0.05)
    check("ledoitwolf: Delta_hat matches the two sample Sharpe ratios",
          bool(np.isclose(shifted["delta"],
                          lw.sharpe_difference(lw.moments(base, base - 4.0e-4)))))
    lo, hi = shifted["ci"]
    check("ledoitwolf: the interval is centred on Delta_hat",
          bool(np.isclose((lo + hi) / 2.0, shifted["delta"])))
    check("ledoitwolf: a rejected null has an interval excluding zero", lo > 0.0 or hi < 0.0)


def check_ledoitwolf_hac() -> None:
    """The HAC estimator, against the two cases where the answer is known."""
    rng = np.random.default_rng(11)
    white = rng.standard_normal((4000, 4))
    white = white - white.mean(axis=0)
    psi = lw.hac_psi(white)
    check("ledoitwolf: HAC of white noise is the contemporaneous covariance",
          bool(np.allclose(psi, np.eye(4), atol=0.15)))

    persistent = np.zeros((4000, 4))
    shock = rng.standard_normal((4000, 4))
    for t in range(1, 4000):
        persistent[t] = 0.7 * persistent[t - 1] + shock[t]
    persistent = persistent - persistent.mean(axis=0)
    long_run = lw.hac_psi(persistent)
    check("ledoitwolf: HAC of an AR(1) recovers sigma^2/(1-rho)^2, not sigma^2",
          bool(np.allclose(np.diag(long_run), 1.0 / (1.0 - 0.7) ** 2, rtol=0.30)))


def _run_unwritten_ok(suite) -> None:
    """Run a suite whose subject may still be a stub.

    src/ledoitwolf.py ships four unimplemented contracts. An unwritten one is a
    FAIL, not a crash -- the other checks must still run while it is being
    written.
    """
    try:
        suite()
    except NotImplementedError as unwritten:
        check(f"ledoitwolf: {unwritten}", False)


def main() -> None:
    check_manifest()
    check_data_loader()
    check_vix_alignment()
    check_pathfunctionals()
    check_sjm_features()
    check_jumpmodel_dp()
    check_jumpmodel_recovery()
    for name in ("grad", "block_psi", "resampler", "test", "hac"):
        _run_unwritten_ok(globals()[f"check_ledoitwolf_{name}"])

    print()
    if FAILURES:
        print(f"{len(FAILURES)} check(s) FAILED:")
        for failure in FAILURES:
            print(f"  - {failure}")
        sys.exit(1)

    print("All checks passed.")


if __name__ == "__main__":
    main()
