# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["DocumentQueryCreateParams"]


class DocumentQueryCreateParams(TypedDict, total=False):
    bucket: Required[str]
    """The storage bucket ID containing the target document.

    Must be an accessible Smart Bucket
    """

    input: Required[str]
    """User's input or question about the document.

    Can be natural language questions, commands, or requests
    """

    object_id: Required[str]
    """Document identifier within the bucket.

    Typically matches the storage path or key
    """

    request_id: Required[str]
    """Client-provided conversation session identifier.

    Required for maintaining context in follow-up questions. We recommend using a
    UUID or ULID for this value.
    """
