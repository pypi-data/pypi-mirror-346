# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from .._models import BaseModel
from .text_result import TextResult

__all__ = ["SearchResponse", "Pagination"]


class Pagination(BaseModel):
    has_more: bool
    """Indicates more results available"""

    page: int
    """Current page number (1-based)"""

    page_size: int
    """Results per page"""

    total: int
    """Total number of available results"""

    total_pages: int
    """Total available pages"""


class SearchResponse(BaseModel):
    pagination: Pagination

    results: List[TextResult]
    """Matched results with metadata"""
