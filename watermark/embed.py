"""Deterministic RGB least-significant-bit embedding."""
from __future__ import annotations

import numpy as np


class CapacityError(ValueError):
    """Raised when an image cannot hold a complete frame."""


def capacity_bits(rgb_array: np.ndarray) -> int:
    """Return the usable RGB-bit capacity for an H x W x 3 uint8 array."""
    _validate_array(rgb_array)
    return int(rgb_array.size)


def _validate_array(rgb_array: np.ndarray) -> None:
    if not isinstance(rgb_array, np.ndarray) or rgb_array.ndim != 3 or rgb_array.shape[2] != 3:
        raise ValueError("Expected an RGB image array with shape (height, width, 3).")
    if rgb_array.dtype != np.uint8:
        raise ValueError("Expected uint8 RGB image data.")


def embed_frame(rgb_array: np.ndarray, frame: bytes) -> np.ndarray:
    """Return a copy of an RGB image with frame bits in row-major channel LSBs."""
    _validate_array(rgb_array)
    needed = len(frame) * 8
    available = capacity_bits(rgb_array)
    if needed > available:
        raise CapacityError(f"Image capacity is {available} bits; watermark needs {needed} bits.")
    output = rgb_array.copy()
    bits = np.unpackbits(np.frombuffer(frame, dtype=np.uint8))
    flat = output.reshape(-1)
    flat[:needed] = (flat[:needed] & 0xFE) | bits
    return output
