import pytest
from watermark.payload import PayloadError, build_frame, parse_frame


def test_payload_round_trip():
    payload = parse_frame(build_frame("FH-001", "IMG-0001"))
    assert payload.business_code == "FH-001"
    assert payload.asset_id == "IMG-0001"


def test_checksum_failure_is_rejected():
    frame = bytearray(build_frame("FH-001", "IMG-0001"))
    frame[10] ^= 1
    with pytest.raises(PayloadError, match="checksum"):
        parse_frame(bytes(frame))


def test_empty_identifier_is_rejected():
    with pytest.raises(PayloadError): build_frame("", "IMG-1")
