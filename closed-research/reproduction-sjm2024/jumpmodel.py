from __future__ import annotations

import numpy as np


def _squared_distances(X: np.ndarray, centroids: np.ndarray) -> np.ndarray:
    diff = X[:, None, :] - centroids[None, :, :]
    return np.einsum("tkd,tkd->tk", diff, diff)


def viterbi_path(D: np.ndarray, jump_penalty: float) -> np.ndarray:
    """Least-cost state path under a fixed per-switch toll.

    The transition cost is 0 on the diagonal and `jump_penalty` everywhere off
    it, so the inner minimisation collapses:

        min_j [ V(t-1,j) + p*1{j != k} ]  =  min( V(t-1,k), p + min_j V(t-1,j) )

    which is why this is O(T*K) and not O(T*K^2). When the global argmin is k
    itself the stay branch is already the smaller of the two, so using the
    global minimum rather than the minimum over j != k is exact, not an
    approximation.
    """
    T, K = D.shape
    V = np.empty((T, K))
    back = np.zeros((T, K), dtype=np.int64)
    V[0] = D[0]

    for t in range(1, T):
        prev = V[t - 1]
        g = int(np.argmin(prev))
        switch = prev[g] + jump_penalty
        stay_wins = prev <= switch
        V[t] = D[t] + np.where(stay_wins, prev, switch)
        back[t] = np.where(stay_wins, np.arange(K), g)

    states = np.empty(T, dtype=np.int64)
    states[-1] = int(np.argmin(V[-1]))
    for t in range(T - 1, 0, -1):
        states[t - 1] = back[t, states[t]]
    return states


def forward_costs(D: np.ndarray, jump_penalty: float) -> np.ndarray:
    """Cost-to-arrive at each state, forward pass only.

    The final state of the optimal path is argmin_k V(T,k), so a causal
    decision needs no backtracking -- which is what makes the online form of
    this model cheap and, more importantly, honest: the state assigned to t is
    never revised by data after t.
    """
    T, K = D.shape
    V = np.empty((T, K))
    V[0] = D[0]
    for t in range(1, T):
        prev = V[t - 1]
        switch = prev.min() + jump_penalty
        V[t] = D[t] + np.minimum(prev, switch)
    return V


def _init_centroids(X: np.ndarray, k: int, rng: np.random.Generator) -> np.ndarray:
    # k-means++ seeding: first centre uniform, the rest favoured by squared distance.
    idx = [int(rng.integers(len(X)))]
    for _ in range(1, k):
        d = _squared_distances(X, X[idx]).min(axis=1)
        total = d.sum()
        if total <= 0:
            idx.append(int(rng.integers(len(X))))
            continue
        idx.append(int(rng.choice(len(X), p=d / total)))
    return X[idx].copy()


def fit_jump_model(
    X: np.ndarray,
    k: int = 2,
    jump_penalty: float = 50.0,
    n_init: int = 10,
    max_iter: int = 50,
    seed: int = 0,
) -> tuple[np.ndarray, np.ndarray, float]:
    """Coordinate descent on

        sum_t ||x_t - theta_{s_t}||^2  +  jump_penalty * sum_t 1{s_t != s_{t-1}}

    Alternates the exact minimiser of each block: the state path given the
    centroids (dynamic programme above), and the centroids given the path
    (cluster means, exactly the k-means update). jump_penalty = 0 is k-means;
    large jump_penalty collapses to one state.
    """
    X = np.asarray(X, dtype=np.float64)
    if X.ndim != 2:
        raise ValueError("X must be 2-D (observations, features).")
    if len(X) < k:
        raise ValueError("Fewer observations than states.")

    rng = np.random.default_rng(seed)
    best: tuple[np.ndarray, np.ndarray, float] | None = None

    for _ in range(n_init):
        centroids = _init_centroids(X, k, rng)
        states = np.zeros(len(X), dtype=np.int64)

        for _ in range(max_iter):
            new_states = viterbi_path(_squared_distances(X, centroids), jump_penalty)
            if np.array_equal(new_states, states):
                break
            states = new_states
            for j in range(k):
                members = X[states == j]
                if len(members):
                    centroids[j] = members.mean(axis=0)
                else:
                    # Empty cluster: hand it the point currently worst explained.
                    far = int(np.argmax(_squared_distances(X, centroids).min(axis=1)))
                    centroids[j] = X[far]

        D = _squared_distances(X, centroids)
        objective = float(
            D[np.arange(len(X)), states].sum()
            + jump_penalty * np.count_nonzero(np.diff(states))
        )
        if best is None or objective < best[2]:
            best = (states, centroids.copy(), objective)

    assert best is not None
    return best


def order_states_by(centroids: np.ndarray, feature: int) -> np.ndarray:
    """Permutation putting states in ascending order of one feature's centroid.

    A state's index is an arbitrary label out of the fit; naming it must be
    mechanical or the labelling itself becomes a researcher choice.
    """
    return np.argsort(centroids[:, feature], kind="stable")


def online_states(
    X: np.ndarray,
    centroids: np.ndarray,
    jump_penalty: float,
    start: int = 0,
) -> np.ndarray:
    """State at each t from a forward pass begun at `start`, never revised.

    Returns argmin_k V(t,k) for every t >= start: the terminal state of the
    optimal path ending at t, which is a function of data up to t only.
    """
    D = _squared_distances(X[start:], centroids)
    V = forward_costs(D, jump_penalty)
    return np.argmin(V, axis=1)
