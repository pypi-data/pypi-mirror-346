# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["TextResult"]


class TextResult(BaseModel):
    chunk_signature: str
    """Unique identifier for this text segment"""

    payload_signature: Optional[str] = None
    """Parent document identifier"""

    score: Optional[float] = None
    """Relevance score (0.0 to 1.0)"""

    source: Optional[str] = None
    """Source document information in JSON format"""

    text: Optional[str] = None
    """The actual content of the result"""

    type: Optional[Literal["text/plain", "application/pdf", "image/jpeg", "image/png"]] = None
    """Content MIME type"""
