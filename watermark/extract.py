"""Watermark extraction with explicit outcome states."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import numpy as np

from .payload import CRC_SIZE, HEADER_SIZE, MAGIC, MAX_PAYLOAD_BYTES, PayloadError, WatermarkPayload, parse_frame

ExtractionStatus = Literal["valid", "not_found", "corrupted"]


@dataclass(frozen=True)
class ExtractionResult:
    status: ExtractionStatus
    payload: WatermarkPayload | None = None
    details: str | None = None


def _read_bytes(rgb_array: np.ndarray, byte_count: int) -> bytes:
    bits_needed = byte_count * 8
    flat = rgb_array.reshape(-1)
    if flat.size < bits_needed:
        raise PayloadError("Image is too small for a complete watermark frame.")
    return np.packbits(flat[:bits_needed] & 1).tobytes()


def extract_frame(rgb_array: np.ndarray) -> ExtractionResult:
    """Extract and validate the first LSB frame from an RGB uint8 image array."""
    if not isinstance(rgb_array, np.ndarray) or rgb_array.ndim != 3 or rgb_array.shape[2] != 3 or rgb_array.dtype != np.uint8:
        return ExtractionResult("corrupted", details="Expected a uint8 RGB image array.")
    if rgb_array.size < HEADER_SIZE * 8:
        return ExtractionResult("not_found", details="Image is too small to contain a header.")
    header = _read_bytes(rgb_array, HEADER_SIZE)
    if header[:4] != MAGIC:
        return ExtractionResult("not_found", details="ShopGuard header is absent.")
    payload_length = int.from_bytes(header[5:9], "big")
    if header[4] != 1:
        return ExtractionResult("corrupted", details=f"Unsupported watermark version: {header[4]}.")
    if payload_length > MAX_PAYLOAD_BYTES:
        return ExtractionResult("corrupted", details="Declared payload length is unreasonable.")
    frame_length = HEADER_SIZE + payload_length + CRC_SIZE
    try:
        payload = parse_frame(_read_bytes(rgb_array, frame_length))
    except PayloadError as exc:
        return ExtractionResult("corrupted", details=str(exc))
    return ExtractionResult("valid", payload=payload, details="CRC32 and payload structure are valid.")
