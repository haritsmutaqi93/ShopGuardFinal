import math
import numpy as np
import pytest
from backend.evaluation import mse_and_psnr


def test_metrics_for_identical_arrays():
    mse, psnr = mse_and_psnr(np.zeros((2, 2, 3), dtype=np.uint8), np.zeros((2, 2, 3), dtype=np.uint8))
    assert mse == 0 and math.isinf(psnr)


def test_metrics_for_one_unit_difference():
    mse, psnr = mse_and_psnr(np.zeros((1, 1, 3), dtype=np.uint8), np.ones((1, 1, 3), dtype=np.uint8))
    assert mse == 1 and psnr > 40


def test_different_shapes_rejected():
    with pytest.raises(ValueError): mse_and_psnr(np.zeros((1, 1, 3)), np.zeros((2, 1, 3)))
