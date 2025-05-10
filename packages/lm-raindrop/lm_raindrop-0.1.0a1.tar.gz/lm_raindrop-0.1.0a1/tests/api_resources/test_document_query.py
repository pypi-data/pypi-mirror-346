# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from lm_raindrop import Raindrop, AsyncRaindrop
from tests.utils import assert_matches_type
from lm_raindrop.types import DocumentQueryCreateResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestDocumentQuery:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create(self, client: Raindrop) -> None:
        document_query = client.document_query.create(
            bucket="bucket",
            input="input",
            object_id="object_id",
            request_id="request_id",
        )
        assert_matches_type(DocumentQueryCreateResponse, document_query, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create(self, client: Raindrop) -> None:
        response = client.document_query.with_raw_response.create(
            bucket="bucket",
            input="input",
            object_id="object_id",
            request_id="request_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        document_query = response.parse()
        assert_matches_type(DocumentQueryCreateResponse, document_query, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create(self, client: Raindrop) -> None:
        with client.document_query.with_streaming_response.create(
            bucket="bucket",
            input="input",
            object_id="object_id",
            request_id="request_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            document_query = response.parse()
            assert_matches_type(DocumentQueryCreateResponse, document_query, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncDocumentQuery:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create(self, async_client: AsyncRaindrop) -> None:
        document_query = await async_client.document_query.create(
            bucket="bucket",
            input="input",
            object_id="object_id",
            request_id="request_id",
        )
        assert_matches_type(DocumentQueryCreateResponse, document_query, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncRaindrop) -> None:
        response = await async_client.document_query.with_raw_response.create(
            bucket="bucket",
            input="input",
            object_id="object_id",
            request_id="request_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        document_query = await response.parse()
        assert_matches_type(DocumentQueryCreateResponse, document_query, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncRaindrop) -> None:
        async with async_client.document_query.with_streaming_response.create(
            bucket="bucket",
            input="input",
            object_id="object_id",
            request_id="request_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            document_query = await response.parse()
            assert_matches_type(DocumentQueryCreateResponse, document_query, path=["response"])

        assert cast(Any, response.is_closed) is True
