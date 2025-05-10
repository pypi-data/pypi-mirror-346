# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .._models import BaseModel

__all__ = ["SummarizePageCreateResponse"]


class SummarizePageCreateResponse(BaseModel):
    summary: str
    """
    AI-generated summary including key themes and topics, content type distribution,
    important findings, and document relationships
    """
