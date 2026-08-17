r"""Path functionals of a wealth curve. The objective space of the active program.

ACTIVE. Charter: ../CHARTER.md.

The closed program's mathematics lived in the space of conditional densities.
The objective has always lived in the space of path functionals, and nothing in
the repo ever computed one beyond a single max drawdown. This module is that
space, kept deliberately small: it implements only what E0-E2 need, and it grows
when an experiment demonstrates a need, never in anticipation of one.

Given marked wealth W(t) with running maximum M(t) = sup_{s<=t} W(s):

    D(t) = 1 - W(t) / M(t)          the drawdown process, in [0, 1)

Everything here is a functional of D or of the excursions of D.

WHY CDaR AND NOT MAX DRAWDOWN. `max(D)` is an extreme-value functional; on one
path it has effective n = 1 and no useful sampling distribution. Conditional
Drawdown-at-Risk (Chekhlov, Uryasev & Zabarankin 2005) is the mean of the worst
alpha-fraction of the drawdown process under its occupation measure. It is
coherent, convex, and computed from the WHOLE path, so its effective sample is
the number of distinct excursions rather than one.

    alpha -> 1    average drawdown (the pain index): well sampled
    alpha -> 0    max drawdown: n = 1

So CDaR is a one-parameter family interpolating from a well-sampled statistic to
the unidentified one, and REPORTING IT AS A CURVE IN alpha turns the sample-size
problem into an output: the alpha at which the estimate destabilises measures how
much of a claim rests on a single episode.

LEAK WARNING (POINT-IN-TIME-DISCIPLINE rows 10-11). `alpha` and the excursion
threshold are researcher degrees of freedom. Choosing either after seeing which
value gives the answer is selection on outcome. Both are declared in an
experiment's stub before it runs.
"""
from __future__ import annotations

from typing import NamedTuple

import numpy as np
import pandas as pd


class Excursion(NamedTuple):
    """One peak-to-recovery drawdown episode.

    `recovered` is False for an excursion still under water at the end of the
    sample; its `recovery` is then a censored lower bound, not a duration.
    """

    start: pd.Timestamp
    trough: pd.Timestamp
    end: pd.Timestamp
    depth: float
    duration: int
    recovery: int
    recovered: bool


def drawdown(wealth: pd.Series) -> pd.Series:
    """D(t) = 1 - W(t)/M(t), reported as a POSITIVE depth in [0, 1)."""
    if wealth.empty:
        raise ValueError("wealth curve is empty")
    if (wealth <= 0).any():
        raise ValueError("wealth curve must be strictly positive")
    return 1.0 - wealth / wealth.cummax()


def excursions(wealth: pd.Series, threshold: float = 0.0) -> list[Excursion]:
    """Maximal intervals where D > 0, keeping those reaching `threshold`.

    `duration` is peak to trough, `recovery` is trough to new high. Both are in
    observations, not calendar time -- the caller owns the period length.
    """
    if not 0.0 <= threshold < 1.0:
        raise ValueError(f"threshold must be in [0, 1), got {threshold}")

    d = drawdown(wealth)
    under = (d > 0.0).to_numpy()
    idx = wealth.index
    out: list[Excursion] = []

    start = None
    for i, wet in enumerate(under):
        if wet and start is None:
            start = i
        elif not wet and start is not None:
            out.append(_build(d, idx, start, i - 1, recovered=True))
            start = None
    if start is not None:
        out.append(_build(d, idx, start, len(under) - 1, recovered=False))

    return [e for e in out if e.depth >= threshold]


def _build(d: pd.Series, idx, lo: int, hi: int, recovered: bool) -> Excursion:
    window = d.iloc[lo : hi + 1]
    t = int(np.argmax(window.to_numpy()))
    return Excursion(
        start=idx[lo - 1] if lo > 0 else idx[lo],
        trough=idx[lo + t],
        end=idx[hi],
        depth=float(window.iloc[t]),
        duration=t + 1,
        recovery=hi - (lo + t),
        recovered=recovered,
    )


def cdar(wealth: pd.Series, alpha: float) -> float:
    """Conditional Drawdown-at-Risk: mean of the worst `alpha` fraction of D.

    alpha = 1.0 is the average drawdown (pain index). As alpha -> 0 this tends to
    max drawdown and its effective sample size tends to one.
    """
    if not 0.0 < alpha <= 1.0:
        raise ValueError(f"alpha must be in (0, 1], got {alpha}")

    d = np.sort(drawdown(wealth).to_numpy())[::-1]
    k = max(1, int(np.ceil(alpha * len(d))))
    return float(d[:k].mean())


def cdar_curve(wealth: pd.Series, alphas=(0.01, 0.05, 0.10, 0.25, 0.50, 1.00)) -> pd.Series:
    """CDaR across alpha. The shape is the point -- see the module docstring."""
    return pd.Series({a: cdar(wealth, a) for a in alphas}, name="cdar")


def time_under_water(wealth: pd.Series, threshold: float) -> float:
    """Fraction of observations with D(t) > threshold. The Ulcer/pain family."""
    if not 0.0 <= threshold < 1.0:
        raise ValueError(f"threshold must be in [0, 1), got {threshold}")
    return float((drawdown(wealth) > threshold).mean())
