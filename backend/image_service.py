"""Safe upload decoding, normalization, and PNG serialization."""
from __future__ import annotations

from io import BytesIO

import numpy as np
from PIL import Image, UnidentifiedImageError

ALLOWED_FORMATS = {"PNG", "JPEG"}
DEFAULT_MAX_UPLOAD_MB = 10
MAX_DIMENSION = 10_000


class ImageValidationError(ValueError):
    """Raised for uploads ShopGuard cannot safely process."""


def load_rgb_image(uploaded_file, max_upload_mb: int = DEFAULT_MAX_UPLOAD_MB) -> tuple[Image.Image, str]:
    """Validate a Streamlit upload/file-like object and normalize it to RGB."""
    raw = uploaded_file.getvalue() if hasattr(uploaded_file, "getvalue") else uploaded_file.read()
    if not raw:
        raise ImageValidationError("The uploaded file is empty.")
    if len(raw) > max_upload_mb * 1024 * 1024:
        raise ImageValidationError(f"Upload exceeds the {max_upload_mb} MB limit.")
    try:
        with Image.open(BytesIO(raw)) as source:
            image_format = source.format
            source.verify()
        with Image.open(BytesIO(raw)) as source:
            if source.format not in ALLOWED_FORMATS:
                raise ImageValidationError("Only PNG and JPEG images are supported.")
            if source.width < 1 or source.height < 1 or source.width > MAX_DIMENSION or source.height > MAX_DIMENSION:
                raise ImageValidationError(f"Image dimensions must be between 1 and {MAX_DIMENSION} pixels.")
            return source.convert("RGB"), image_format or "unknown"
    except (UnidentifiedImageError, OSError) as exc:
        raise ImageValidationError("The file is not a readable PNG or JPEG image.") from exc


def image_to_png_bytes(image: Image.Image) -> bytes:
    """Serialize an RGB image as lossless PNG bytes."""
    output = BytesIO()
    image.convert("RGB").save(output, format="PNG")
    return output.getvalue()


def to_array(image: Image.Image) -> np.ndarray:
    """Return a contiguous uint8 RGB array."""
    return np.array(image.convert("RGB"), dtype=np.uint8)
