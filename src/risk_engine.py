from __future__ import annotations

from typing import Final

# Structural placeholder only. Not implemented yet — see README.md Module 3.
# No smoothing or tiering logic will be written here until the audit of
# data_loader.py and jump_model.py, and the accompanying math reference
# sheet, are both complete.

CALM_TIER: Final[str] = "calm"
BUILDING_STRESS_TIER: Final[str] = "building_stress"
HYSTERIA_TIER: Final[str] = "hysteria"

CALM_UPPER_BOUND: Final[float] = 0.20
BUILDING_STRESS_UPPER_BOUND: Final[float] = 0.60


def smooth_jump_probabilities(jump_probabilities: "object", span: int) -> "object":
    """Apply an EWMA shock absorber to raw smoothed regime probabilities.

    Intended signature per README.md Module 3. Not implemented.
    """
    raise NotImplementedError("risk_engine.smooth_jump_probabilities is not implemented yet.")


def classify_risk_tier(smoothed_probability: float) -> str:
    """Map a smoothed panic probability to a Risk Tier Matrix action band.

    Bands per README.md section 4: calm [0, 0.20], building_stress
    (0.20, 0.60], hysteria (0.60, 1.0]. Not implemented.
    """
    raise NotImplementedError("risk_engine.classify_risk_tier is not implemented yet.")
