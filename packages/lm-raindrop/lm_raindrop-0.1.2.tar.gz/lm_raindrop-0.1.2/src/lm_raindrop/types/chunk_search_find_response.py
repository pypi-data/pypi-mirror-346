# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from .._models import BaseModel
from .text_result import TextResult

__all__ = ["ChunkSearchFindResponse"]


class ChunkSearchFindResponse(BaseModel):
    results: List[TextResult]
    """Semantically relevant results with metadata and relevance scoring"""
