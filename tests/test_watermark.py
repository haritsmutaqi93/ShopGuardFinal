import numpy as np
import pytest
from watermark.embed import CapacityError, embed_frame
from watermark.extract import extract_frame
from watermark.payload import build_frame


def test_embed_extract_round_trip():
    source = np.full((100, 100, 3), 128, dtype=np.uint8)
    output = embed_frame(source, build_frame("SHOP", "ASSET-1"))
    result = extract_frame(output)
    assert result.status == "valid"
    assert result.payload.business_code == "SHOP"
    assert result.payload.asset_id == "ASSET-1"


def test_unrelated_image_is_not_found():
    result = extract_frame(np.zeros((50, 50, 3), dtype=np.uint8))
    assert result.status == "not_found"


def test_small_image_capacity_error():
    with pytest.raises(CapacityError):
        embed_frame(np.zeros((2, 2, 3), dtype=np.uint8), build_frame("SHOP", "ASSET-1"))


def test_corrupted_bit_is_rejected():
    output = embed_frame(np.zeros((100, 100, 3), dtype=np.uint8), build_frame("SHOP", "ASSET-1"))
    output.reshape(-1)[80] ^= 1
    assert extract_frame(output).status == "corrupted"
