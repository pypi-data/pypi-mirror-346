# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["SummarizePageCreateParams"]


class SummarizePageCreateParams(TypedDict, total=False):
    request_id: Required[str]
    """Client-provided search session identifier from the original search"""

    page: int
    """Target page number (1-based)"""

    page_size: int
    """Results per page. Affects how many documents are included in the summary"""
