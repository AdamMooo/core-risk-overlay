"""D4, third leg: src/jumpmodel.py against the authors' `jumpmodels` package.

Shu, Yu & Mulvey (2024)'s reference implementation is the `jumpmodels` package
(PyPI, Yizhan Shu). This script checks that the two implementations solve the
same problem exactly, and pins down the one convention difference:

    THE LAMBDA CONVENTION. jumpmodels/jump.py computes the loss matrix as
    0.5 * ||x - theta||^2 (do_E_step); src/jumpmodel.py uses ||x - theta||^2.
    Minimising 0.5*D + lam*J is minimising D + 2*lam*J, so

        lambda_ours = 2 * lambda_package.

    Every lambda quoted in this repository's reproduction is therefore worth
    HALF its face value in the paper's units: the lambda=50 run reproduces the
    paper's lambda=25.

Four comparisons, first three exact and the fourth statistical:
  1. Offline paths with centroids held fixed -- their dp() against our
     viterbi_path() at the matched penalty. Exact equality expected.
  2. Online states with centroids held fixed -- their forward value matrix
     against our forward_costs(). Exact equality expected.
  3. The convention demonstration: the SAME face-value lambda fed to both
     produces DIFFERENT paths, and matched lambdas produce identical ones.
  4. Free fits on synthetic SJM-style features -- both packages fit from their
     own initialisations; near-total label agreement expected, exactness not.

Run: .venv\\Scripts\\python.exe d4_crosscheck.py
Exits non-zero on failure. Requires `pip install jumpmodels`.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))

import jumpmodel as jm
import sjm_features as sf
from jumpmodels.jump import JumpModel, do_E_step, dp, jump_penalty_to_mx

FAILURES: list[str] = []


def check(description: str, condition: bool) -> None:
    status = "PASS" if condition else "FAIL"
    print(f"[{status}] {description}")
    if not condition:
        FAILURES.append(description)


def _sqdist(X: np.ndarray, centroids: np.ndarray) -> np.ndarray:
    diff = X[:, None, :] - centroids[None, :, :]
    return np.einsum("tkd,tkd->tk", diff, diff)


def _path_cost(D: np.ndarray, path: np.ndarray, lam: float) -> float:
    return float(D[np.arange(len(D)), path].sum() + lam * np.count_nonzero(np.diff(path)))


def _best_perm_agreement(a: np.ndarray, b: np.ndarray) -> float:
    direct = float((a == b).mean())
    return max(direct, 1.0 - direct)


def synthetic_features(rng: np.random.Generator) -> tuple[np.ndarray, np.ndarray]:
    blocks = [(0, 500), (1, 150), (0, 600), (1, 250), (0, 700),
              (1, 120), (0, 800), (1, 200), (0, 680)]
    truth = np.concatenate([np.full(n, s, dtype=np.int64) for s, n in blocks])
    returns = pd.Series(
        np.where(truth == 0,
                 rng.normal(4e-4, 0.007, len(truth)),
                 rng.normal(-8e-4, 0.02, len(truth))),
        index=pd.bdate_range("2000-01-03", periods=len(truth)),
    )
    X = sf.build_features(returns).to_numpy()
    return (X - X.mean(axis=0)) / X.std(axis=0), truth


def check_fixed_centroid_equivalence(Xs: np.ndarray) -> None:
    rng = np.random.default_rng(1)
    for k in (2, 3):
        centroids = Xs[rng.choice(len(Xs), size=k, replace=False)] + rng.normal(0, 0.1, (k, Xs.shape[1]))
        D = _sqdist(Xs, centroids)
        for lam_pkg in (5.0, 25.0, 50.0, 100.0):
            penalty_mx = jump_penalty_to_mx(lam_pkg, k)
            theirs_path, theirs_val = dp(0.5 * D, penalty_mx)
            ours_path = jm.viterbi_path(D, 2.0 * lam_pkg)
            check(f"offline path identical, K={k} lambda_pkg={lam_pkg:g} (ours={2*lam_pkg:g})",
                  bool(np.array_equal(ours_path, theirs_path)))
            check(f"objective relation val_pkg = ours/2, K={k} lambda_pkg={lam_pkg:g}",
                  np.isclose(2.0 * theirs_val, _path_cost(D, ours_path, 2.0 * lam_pkg)))

            theirs_value_mx = do_E_step(Xs, centroids, penalty_mx, return_value_mx=True)
            ours_online = jm.online_states(Xs, centroids, 2.0 * lam_pkg)
            check(f"online states identical, K={k} lambda_pkg={lam_pkg:g}",
                  bool(np.array_equal(ours_online, theirs_value_mx.argmin(axis=1))))


def check_convention_matters(Xs: np.ndarray) -> None:
    # Same face value on both sides must NOT reproduce: at lambda=50 raw, ours
    # penalises switches twice as hard as theirs. If the paths agreed anyway
    # the factor of two would be immaterial and the finding would be wrong.
    rng = np.random.default_rng(2)
    centroids = Xs[rng.choice(len(Xs), size=2, replace=False)] + rng.normal(0, 0.1, (2, 3))
    D = _sqdist(Xs, centroids)
    differs = False
    for lam_face in (5.0, 15.0, 35.0, 50.0):
        theirs_path, _ = dp(0.5 * D, jump_penalty_to_mx(lam_face, 2))
        ours_path = jm.viterbi_path(D, lam_face)
        differs |= not np.array_equal(ours_path, theirs_path)
    check("the factor of two is material: same face-value lambda gives different paths "
          "for at least one lambda on the paper's grid", differs)


def check_free_fit_agreement(Xs: np.ndarray, truth: np.ndarray) -> None:
    lam_pkg = 25.0
    ours_states, ours_centroids, _ = jm.fit_jump_model(Xs, k=2, jump_penalty=2.0 * lam_pkg, seed=0)
    theirs = JumpModel(n_components=2, jump_penalty=lam_pkg, cont=False, random_state=0)
    theirs.fit(Xs)
    theirs_states = np.asarray(theirs.labels_)

    agreement = _best_perm_agreement(ours_states, theirs_states)
    check(f"free fits agree on the label path (agreement {agreement:.4f} >= 0.99)",
          agreement >= 0.99)

    ours_sw = int(np.count_nonzero(np.diff(ours_states)))
    theirs_sw = int(np.count_nonzero(np.diff(theirs_states)))
    check(f"free fits agree on switch count (ours {ours_sw}, theirs {theirs_sw})",
          abs(ours_sw - theirs_sw) <= 2)

    acc = _best_perm_agreement(ours_states, truth[-len(ours_states):] if len(truth) != len(ours_states) else truth)
    print(f"       (context: our fit matches the known truth at {acc:.4f})")


def check_real_data() -> None:
    cache = Path(__file__).resolve().parent.parent.parent / "data" / "sjm_gspc_daily.csv"
    if not cache.exists():
        print("       (real-data leg skipped: data/sjm_gspc_daily.csv not cached)")
        return
    prices = pd.read_csv(cache, index_col=0, parse_dates=True).iloc[:, 0]
    returns = prices.pct_change().dropna()
    X = sf.build_features(returns).to_numpy()[-3000:]
    Xs = (X - X.mean(axis=0)) / X.std(axis=0)

    lam_pkg = 25.0
    ours_states, _, _ = jm.fit_jump_model(Xs, k=2, jump_penalty=2.0 * lam_pkg, seed=0)
    theirs = JumpModel(n_components=2, jump_penalty=lam_pkg, cont=False, random_state=0)
    theirs.fit(Xs)
    agreement = _best_perm_agreement(ours_states, np.asarray(theirs.labels_))
    check(f"real ^GSPC window, free fits agree (agreement {agreement:.4f} >= 0.99)",
          agreement >= 0.99)


def main() -> int:
    rng = np.random.default_rng(11)
    Xs, truth = synthetic_features(rng)
    truth = truth[-len(Xs):]

    check_fixed_centroid_equivalence(Xs)
    check_convention_matters(Xs)
    check_free_fit_agreement(Xs, truth)
    check_real_data()

    print()
    if FAILURES:
        print(f"{len(FAILURES)} check(s) FAILED:")
        for failure in FAILURES:
            print(f"  - {failure}")
        return 1
    print("All cross-checks passed. lambda_ours = 2 * lambda_package is confirmed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
