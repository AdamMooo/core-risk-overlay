r"""Ledoit & Wolf (2008) inference for the difference of two Sharpe ratios.

Ledoit, O. and Wolf, M. (2008), "Robust performance hypothesis testing with the
Sharpe ratio", Journal of Empirical Finance 15(5):850-859. PDF local in
docs/literature/. Equation numbers below are theirs.

Why not Jobson-Korkie / Memmel: their Omega assumes i.i.d. bivariate normal
pairs. It puts zeros where Cov(mu_hat, sigma2_hat) belongs and 2*sigma^4 where
E[(r-mu)^4] - sigma^4 belongs. The standard error of a Sharpe ratio is a
fourth-moment object, and fourth moments are exactly where volatility
clustering lives, so on daily equity returns that formula is not merely
inefficient -- it is wrong (their section 2).

The fix, in three moves:

  1. Write the difference as a smooth function of four means,
     Delta = f(mu_i, mu_n, gamma_i, gamma_n) with gamma = E[r^2] and
     f(a,b,c,d) = a/sqrt(c - a^2) - b/sqrt(d - b^2)              (their Eq. 2)
     so that the delta method applies.
  2. Estimate Psi, the LONG-RUN covariance of the four moment conditions, by a
     prewhitened QS kernel (Andrews 1991; Andrews & Monahan 1992). This is the
     term that carries serial dependence.
  3. Studentize, and bootstrap the studentized statistic with a circular block
     bootstrap. A NON-studentized bootstrap buys nothing over asymptotic
     normality; the accuracy gain comes from resampling a pivot (Hall 1992).
     Their Remark 3.3 pins this error on Vinod & Morey (1999), together with
     the second error of reusing one standard error across all resamples.

Scale note: annualisation multiplies Delta and s(Delta) by the same sqrt(252),
so the studentized statistic and its p-value are invariant to it. Everything
here is computed on the daily scale; annualise for reporting only.
"""
from __future__ import annotations

import numpy as np

MOMENT_DIM = 4


def moments(r_i: np.ndarray, r_n: np.ndarray) -> np.ndarray:
    """v_hat = (mu_i, mu_n, gamma_i, gamma_n), the four means Delta is a function of."""
    return np.array([r_i.mean(), r_n.mean(), (r_i**2).mean(), (r_n**2).mean()])


def sharpe_difference(v: np.ndarray) -> float:
    """f(v) of their Eq. (2) -- the Sharpe difference implied by four moments.

    Note c - a^2 is the variance of series i, so this is the ordinary Sharpe
    difference written in uncentered moments.
    """
    a, b, c, d = v
    return a / np.sqrt(c - a**2) - b / np.sqrt(d - b**2)


def moment_conditions(r_i: np.ndarray, r_n: np.ndarray, v: np.ndarray) -> np.ndarray:
    """y_hat_t of their section 3.1, shape (T, 4).

    Row t is (r_ti - mu_i, r_tn - mu_n, r_ti^2 - gamma_i, r_tn^2 - gamma_n).
    Psi is the long-run covariance of THIS process, not of the returns.
    """
    a, b, c, d = v
    return np.column_stack([r_i - a, r_n - b, r_i**2 - c, r_n**2 - d])


def standard_error(v: np.ndarray, psi: np.ndarray, n_obs: int) -> float:
    """s(Delta_hat) of their Eq. (5): sqrt( grad' Psi grad / T )."""
    grad = sharpe_grad(v)
    return float(np.sqrt(grad @ psi @ grad / n_obs))


# ---------------------------------------------------------------------------
# The four pieces that carry the method's content. Written by hand, against
# these contracts, before inference.py can run. Each is checked in checks.py.
# ---------------------------------------------------------------------------


def sharpe_grad(v: np.ndarray) -> np.ndarray:
    """The gradient of f at v = (a, b, c, d). Shape (4,).

    Their section 3, immediately after Eq. (4):

        grad_f(a,b,c,d) = (  c / (c - a^2)^1.5 ,
                            -d / (d - b^2)^1.5 ,
                            -0.5 * a / (c - a^2)^1.5 ,
                             0.5 * b / (d - b^2)^1.5 )

    Worth deriving rather than transcribing: differentiate
    a / sqrt(c - a^2) with respect to a and to c and the four terms fall out,
    and the sign pattern then tells you which way each moment moves the
    difference. Note the first two entries are NOT symmetric in sign with the
    last two -- that asymmetry is the whole delta-method content.

    Contract:
      - returns a float64 array of shape (4,)
      - sharpe_grad(v) with v from a series and its own copy must give a
        gradient whose first and second entries are equal and opposite
    """
    a, b, c, d = v
    var_i, var_n = c - a**2, d - b**2
    return np.array([c / var_i**1.5, -d / var_n**1.5,
                     -0.5 * a / var_i**1.5, 0.5 * b / var_n**1.5])


def block_psi(y_star: np.ndarray, block: int) -> np.ndarray:
    """Psi_hat* from BOOTSTRAP data, using the block structure (their 3.2.2).

    In the bootstrap world the dependence structure is known -- the resample was
    built from independent blocks -- so the long-run covariance does not need a
    kernel estimate. Sum each block, scale by 1/sqrt(b), and take the sample
    covariance of those l block sums:

        zeta_j = b^(-1/2) * sum_{t=1..b} y*_{(j-1)b + t}     j = 1..l
        Psi_hat* = (1/l) * sum_j zeta_j zeta_j'
        l = floor(T / b)

    This is the Goetze & Kuensch (1996) 'natural' bootstrap standard error, and
    computing it per resample -- rather than reusing s(Delta_hat) -- is the
    second thing Remark 3.3 says Vinod & Morey got wrong.

    Note their footnote 9: at b = 1 this must reduce to the plain sample
    covariance of the rows of y_star. That is a free unit test.

    Args:
      y_star: (T, 4) moment conditions computed from the RESAMPLE, centred on
              the RESAMPLE's own moments v_hat*.
      block:  b >= 1. Trailing rows beyond l*b are discarded, not wrapped.

    Contract:
      - returns (4, 4), symmetric, positive semi-definite
      - block=1 equals np.cov(y_star.T, bias=True) up to floating point
    """
    n_blocks = y_star.shape[0] // block
    zeta = y_star[: n_blocks * block].reshape(n_blocks, block, -1).sum(axis=1)
    zeta /= np.sqrt(block)
    return zeta.T @ zeta / n_blocks


def circular_block_indices(n_obs: int, block: int, rng: np.random.Generator) -> np.ndarray:
    """Row indices for one circular-block-bootstrap resample. Shape (n_obs,).

    Politis & Romano (1992), used by LW in preference to Kuensch's moving-blocks
    bootstrap to avoid its edge effects (their footnote 7): every observation
    must have the same probability of appearing, which is achieved by letting a
    block that runs past the end WRAP AROUND to the start.

    Draw ceil(n_obs / block) start points uniformly from 0..n_obs-1, expand each
    into block consecutive indices modulo n_obs, concatenate, truncate to n_obs.

    The one thing to get right: it is the same index sequence for BOTH series.
    Resampling the two strategies independently would destroy the contemporaneous
    correlation that makes the difference of Sharpe ratios estimable at all --
    LW resample PAIRS.

    Contract:
      - returns int array of shape (n_obs,), all values in [0, n_obs)
      - block >= n_obs returns a single wrapped block (a rotation of the sample)
      - block=1 is the i.i.d. bootstrap
      - deterministic given rng
    """
    n_starts = -(-n_obs // block)
    starts = rng.integers(0, n_obs, size=n_starts)
    idx = (starts[:, None] + np.arange(block)) % n_obs
    return idx.ravel()[:n_obs]


def studentized_pvalue(
    r_i: np.ndarray,
    r_n: np.ndarray,
    block: int,
    n_boot: int,
    rng: np.random.Generator,
    psi_hat: np.ndarray | None = None,
) -> dict:
    """The test. Their Eq. (6) for the pivot and Eq. (9) for the p-value.

    Null: H0: Delta = 0, two-sided.

        d       = |Delta_hat| / s(Delta_hat)                    from the data
        d*_m    = |Delta*_m - Delta_hat| / s(Delta*_m)          from resample m
        p-value = ( #{ d*_m >= d } + 1 ) / (M + 1)                    Eq. (9)

    Three things the arithmetic depends on and that are easy to get wrong:

      - d*_m is centred on Delta_hat, not on 0. The bootstrap world's true
        parameter is the sample's estimate; that is what makes the statistic a
        pivot and the whole exercise higher-order accurate.
      - s(Delta*_m) is recomputed from resample m via block_psi. Reusing
        s(Delta_hat) is the Vinod-Morey error.
      - the +1 in numerator and denominator is not a continuity fudge; it makes
        the p-value exact-valid by including the observed statistic in its own
        reference distribution.

    Args:
      psi_hat: the data-side long-run covariance. Pass hac_psi(...) output;
               None recomputes it here.

    Returns a dict with at least:
      delta      float, Delta_hat on the DAILY scale
      se         float, s(Delta_hat)
      d          float, the studentized statistic
      pvalue     float, Eq. (9)
      ci         (lo, hi), the symmetric studentized interval of their Eq. (7),
                 Delta_hat +/- z*_{|.|,0.95} * s(Delta_hat), daily scale
    """
    n_obs = len(r_i)
    v_hat = moments(r_i, r_n)
    delta_hat = sharpe_difference(v_hat)
    if psi_hat is None:
        psi_hat = hac_psi(moment_conditions(r_i, r_n, v_hat))
    se_hat = standard_error(v_hat, psi_hat, n_obs)
    d = abs(delta_hat) / se_hat

    d_star = np.empty(n_boot)
    for m in range(n_boot):
        idx = circular_block_indices(n_obs, block, rng)
        ri_star, rn_star = r_i[idx], r_n[idx]
        v_star = moments(ri_star, rn_star)
        y_star = moment_conditions(ri_star, rn_star, v_star)
        se_star = standard_error(v_star, block_psi(y_star, block), n_obs)
        d_star[m] = abs(sharpe_difference(v_star) - delta_hat) / se_star

    z_crit = float(np.quantile(d_star, 0.95))
    return {
        "delta": float(delta_hat),
        "se": se_hat,
        "d": float(d),
        "pvalue": float((np.sum(d_star >= d) + 1.0) / (n_boot + 1.0)),
        "ci": (float(delta_hat - z_crit * se_hat), float(delta_hat + z_crit * se_hat)),
    }


# ---------------------------------------------------------------------------
# Mechanical: the Andrews (1991) / Andrews & Monahan (1992) HAC recipe.
# Implemented here because it is bookkeeping from a different paper, not the
# content of this one.
# ---------------------------------------------------------------------------


def _qs_kernel(x: np.ndarray) -> np.ndarray:
    """Quadratic-spectral kernel. k(0) = 1, characteristic exponent q = 2."""
    x = np.asarray(x, dtype=float)
    out = np.ones_like(x)
    nz = x != 0.0
    z = 6.0 * np.pi * x[nz] / 5.0
    out[nz] = 25.0 / (12.0 * np.pi**2 * x[nz] ** 2) * (np.sin(z) / z - np.cos(z))
    return out


def _andrews_bandwidth(e: np.ndarray) -> float:
    """Andrews (1991) automatic bandwidth for the QS kernel, from AR(1) fits.

    alpha(2) = sum_a 4 rho_a^2 sigma_a^4 / (1-rho_a)^8
               / sum_a sigma_a^4 / (1-rho_a)^4
    S_T = 1.3221 * (alpha(2) * T)^(1/5)
    """
    n_obs = e.shape[0]
    num = den = 0.0
    for col in range(e.shape[1]):
        x = e[:, col]
        denom = float(x[:-1] @ x[:-1])
        rho = float(x[:-1] @ x[1:] / denom) if denom > 0 else 0.0
        rho = float(np.clip(rho, -0.97, 0.97))
        resid = x[1:] - rho * x[:-1]
        sigma2 = float(resid @ resid / len(resid))
        num += 4.0 * rho**2 * sigma2**2 / (1.0 - rho) ** 8
        den += sigma2**2 / (1.0 - rho) ** 4
    alpha2 = num / den if den > 0 else 0.0
    return 1.3221 * (alpha2 * n_obs) ** 0.2 if alpha2 > 0 else 1.0


def hac_psi(y: np.ndarray, max_lag: int | None = None) -> np.ndarray:
    """Prewhitened QS-kernel estimate of the long-run covariance of y. (T,4) -> (4,4).

    VAR(1)-prewhiten, kernel-estimate the residual spectrum at zero, recolour:

        y_t = A y_{t-1} + e_t
        Psi_e = Gamma_e(0) + sum_j k(j/S_T) [Gamma_e(j) + Gamma_e(j)']
        Psi   = (I - A)^-1 Psi_e (I - A)^-T

    Prewhitening exists because a kernel estimator is badly biased when the
    process is persistent; the VAR removes the persistence a kernel handles
    worst, and the recolouring puts it back analytically. The eigenvalues of A
    are shrunk to 0.97 to keep (I - A) invertible (Andrews & Monahan 1992).

    The T/(T-4) factor is LW's small-sample adjustment for having estimated the
    4-vector v (their section 3.1). QS support is infinite, so lags are
    truncated where the kernel weight is negligible.
    """
    y = np.asarray(y, dtype=float)
    n_obs = y.shape[0]

    lhs, rhs = y[1:], y[:-1]
    coef = np.linalg.lstsq(rhs, lhs, rcond=None)[0].T
    values, vectors = np.linalg.eig(coef)
    if np.max(np.abs(values)) > 0.97:
        values = values * (0.97 / np.max(np.abs(values)))
        coef = np.real(vectors @ np.diag(values) @ np.linalg.inv(vectors))
    resid = lhs - rhs @ coef.T

    bandwidth = _andrews_bandwidth(resid)
    if max_lag is None:
        max_lag = int(min(len(resid) - 1, np.ceil(50.0 * max(bandwidth, 1.0))))

    psi_e = resid.T @ resid / len(resid)
    weights = _qs_kernel(np.arange(1, max_lag + 1) / bandwidth)
    for lag, weight in enumerate(weights, start=1):
        if abs(weight) < 1e-10:
            break
        gamma = resid[lag:].T @ resid[:-lag] / len(resid)
        psi_e += weight * (gamma + gamma.T)

    unwhiten = np.linalg.inv(np.eye(MOMENT_DIM) - coef)
    psi = unwhiten @ psi_e @ unwhiten.T
    return psi * (n_obs / (n_obs - MOMENT_DIM))


def politis_white_block(x: np.ndarray) -> float:
    """Politis & White (2004) automatic block length for the STATIONARY bootstrap.

    Reported as a reference point only. The preregistration fixes the block-size
    rule as max-p over a declared grid, precisely so that no block length is
    selected after an outcome is seen -- see docs/REPRO-SJM2024-FINDINGS.md,
    "Preregistered for the inference run".

    Implements their b_opt = (2 * G^2 / D_SB)^(1/3) * T^(1/3) with the flat-top
    lag-window correlogram rule of their section 3 and the Patton, Politis &
    White (2009) corrected constant.
    """
    x = np.asarray(x, dtype=float)
    n_obs = len(x)
    x = x - x.mean()
    k_n = max(5, int(np.ceil(np.sqrt(np.log10(n_obs)))))
    m_max = int(np.ceil(np.sqrt(n_obs))) + k_n
    gamma = np.array([x[lag:] @ x[: n_obs - lag] / n_obs for lag in range(m_max + 1)])
    rho = gamma / gamma[0]

    threshold = 2.0 * np.sqrt(np.log10(n_obs) / n_obs)
    m_hat = 1
    for lag in range(1, m_max - k_n + 1):
        if np.all(np.abs(rho[lag : lag + k_n]) < threshold):
            m_hat = lag - 1
            break
        m_hat = lag
    m_star = max(1, min(2 * max(m_hat, 1), int(np.sqrt(n_obs))))

    lags = np.arange(-m_star, m_star + 1)
    flat_top = np.clip(2.0 * (1.0 - np.abs(lags) / (2.0 * m_star)), 0.0, 1.0)
    g_hat = float(np.sum(flat_top * np.abs(lags) * gamma[np.abs(lags)]))
    d_hat = 2.0 * float(np.sum(flat_top * gamma[np.abs(lags)])) ** 2
    if d_hat <= 0 or g_hat == 0:
        return 1.0
    return float(min((2.0 * g_hat**2 / d_hat) ** (1.0 / 3.0) * n_obs ** (1.0 / 3.0), n_obs / 3.0))
