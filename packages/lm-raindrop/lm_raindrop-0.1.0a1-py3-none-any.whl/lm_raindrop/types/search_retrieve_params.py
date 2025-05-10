# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["SearchRetrieveParams"]


class SearchRetrieveParams(TypedDict, total=False):
    request_id: Required[str]
    """Client-provided search session identifier from the initial search"""

    page: int
    """Requested page number"""

    page_size: int
    """Results per page"""
