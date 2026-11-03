"""Versioned binary payload framing for ShopGuard."""
from __future__ import annotations

import json
import struct
import zlib
from dataclasses import dataclass

MAGIC = b"SGWM"
VERSION = 1
HEADER_SIZE = 9  # magic (4) + version (1) + payload length (4)
CRC_SIZE = 4
MAX_PAYLOAD_BYTES = 16_384


class PayloadError(ValueError):
    """Raised when a framed watermark payload is invalid."""


@dataclass(frozen=True)
class WatermarkPayload:
    business_code: str
    asset_id: str
    version: int = VERSION


def _validate_identifiers(business_code: str, asset_id: str) -> None:
    if not isinstance(business_code, str) or not business_code.strip():
        raise PayloadError("Business code must be a non-empty string.")
    if not isinstance(asset_id, str) or not asset_id.strip():
        raise PayloadError("Asset ID must be a non-empty string.")


def build_frame(business_code: str, asset_id: str) -> bytes:
    """Build a deterministic v1 frame with a CRC32 over JSON payload bytes."""
    _validate_identifiers(business_code, asset_id)
    body = json.dumps(
        {"business_code": business_code.strip(), "asset_id": asset_id.strip()},
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    if len(body) > MAX_PAYLOAD_BYTES:
        raise PayloadError(f"Payload is too large (maximum {MAX_PAYLOAD_BYTES} bytes).")
    header = MAGIC + bytes([VERSION]) + struct.pack(">I", len(body))
    return header + body + struct.pack(">I", zlib.crc32(body) & 0xFFFFFFFF)


def parse_frame(frame: bytes) -> WatermarkPayload:
    """Validate a complete frame and return its safe identifier fields."""
    if len(frame) < HEADER_SIZE:
        raise PayloadError("Incomplete watermark header.")
    if frame[:4] != MAGIC:
        raise PayloadError("Watermark header not found.")
    version = frame[4]
    if version != VERSION:
        raise PayloadError(f"Unsupported watermark version: {version}.")
    payload_length = struct.unpack(">I", frame[5:9])[0]
    if payload_length > MAX_PAYLOAD_BYTES:
        raise PayloadError("Declared payload length is unreasonable.")
    expected_length = HEADER_SIZE + payload_length + CRC_SIZE
    if len(frame) != expected_length:
        raise PayloadError("Incomplete or malformed watermark frame.")
    body = frame[HEADER_SIZE : HEADER_SIZE + payload_length]
    expected_crc = struct.unpack(">I", frame[-CRC_SIZE:])[0]
    if zlib.crc32(body) & 0xFFFFFFFF != expected_crc:
        raise PayloadError("Watermark checksum does not match.")
    try:
        data = json.loads(body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise PayloadError("Watermark payload is not valid UTF-8 JSON.") from exc
    if not isinstance(data, dict) or set(data) != {"business_code", "asset_id"}:
        raise PayloadError("Watermark payload has an invalid structure.")
    _validate_identifiers(data["business_code"], data["asset_id"])
    return WatermarkPayload(data["business_code"].strip(), data["asset_id"].strip(), version)
