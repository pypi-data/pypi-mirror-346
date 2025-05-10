# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .._models import BaseModel

__all__ = ["StorageObjectUploadResponse"]


class StorageObjectUploadResponse(BaseModel):
    bucket: str

    key: str

    success: bool
