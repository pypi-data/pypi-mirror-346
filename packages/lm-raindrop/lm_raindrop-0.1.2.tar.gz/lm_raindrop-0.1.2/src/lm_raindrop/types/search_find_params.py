# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Required, TypedDict

__all__ = ["SearchFindParams"]


class SearchFindParams(TypedDict, total=False):
    bucket_ids: Required[List[str]]
    """Optional list of specific bucket IDs to search in.

    If not provided, searches the latest version of all buckets
    """

    input: Required[str]
    """Natural language search query that can include complex criteria"""

    request_id: Required[str]
    """Client-provided search session identifier.

    Required for pagination and result tracking. We recommend using a UUID or ULID
    for this value.
    """
