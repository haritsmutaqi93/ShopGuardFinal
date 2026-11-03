"""Image quality metrics."""
from __future__ import annotations

import math
import numpy as np


def mse_and_psnr(original: np.ndarray, modified: np.ndarray) -> tuple[float, float]:
    """Calculate MSE and PSNR for equal-sized RGB arrays; infinity PSNR means no change."""
    if original.shape != modified.shape:
        raise ValueError("Images must have identical dimensions for comparison.")
    if original.ndim != 3 or original.shape[2] != 3:
        raise ValueError("Expected RGB image arrays.")
    mse = float(np.mean((original.astype(np.float64) - modified.astype(np.float64)) ** 2))
    return mse, math.inf if mse == 0 else float(10 * math.log10((255.0**2) / mse))
