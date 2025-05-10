# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .._models import BaseModel

__all__ = ["DocumentQueryCreateResponse"]


class DocumentQueryCreateResponse(BaseModel):
    answer: str
    """
    AI-generated response that may include direct document quotes, content
    summaries, contextual explanations, references to specific sections, and related
    content suggestions
    """
