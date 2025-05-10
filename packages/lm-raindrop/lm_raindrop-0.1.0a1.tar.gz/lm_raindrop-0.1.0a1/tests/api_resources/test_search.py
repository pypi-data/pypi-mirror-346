# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from lm_raindrop import Raindrop, AsyncRaindrop
from tests.utils import assert_matches_type
from lm_raindrop.types import SearchResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestSearch:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create(self, client: Raindrop) -> None:
        search = client.search.create(
            bucket_ids=["string"],
            input="input",
            request_id="request_id",
        )
        assert_matches_type(SearchResponse, search, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create(self, client: Raindrop) -> None:
        response = client.search.with_raw_response.create(
            bucket_ids=["string"],
            input="input",
            request_id="request_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        search = response.parse()
        assert_matches_type(SearchResponse, search, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create(self, client: Raindrop) -> None:
        with client.search.with_streaming_response.create(
            bucket_ids=["string"],
            input="input",
            request_id="request_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            search = response.parse()
            assert_matches_type(SearchResponse, search, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve(self, client: Raindrop) -> None:
        search = client.search.retrieve(
            request_id="request_id",
        )
        assert_matches_type(SearchResponse, search, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve_with_all_params(self, client: Raindrop) -> None:
        search = client.search.retrieve(
            request_id="request_id",
            page=0,
            page_size=0,
        )
        assert_matches_type(SearchResponse, search, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve(self, client: Raindrop) -> None:
        response = client.search.with_raw_response.retrieve(
            request_id="request_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        search = response.parse()
        assert_matches_type(SearchResponse, search, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve(self, client: Raindrop) -> None:
        with client.search.with_streaming_response.retrieve(
            request_id="request_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            search = response.parse()
            assert_matches_type(SearchResponse, search, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncSearch:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create(self, async_client: AsyncRaindrop) -> None:
        search = await async_client.search.create(
            bucket_ids=["string"],
            input="input",
            request_id="request_id",
        )
        assert_matches_type(SearchResponse, search, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncRaindrop) -> None:
        response = await async_client.search.with_raw_response.create(
            bucket_ids=["string"],
            input="input",
            request_id="request_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        search = await response.parse()
        assert_matches_type(SearchResponse, search, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncRaindrop) -> None:
        async with async_client.search.with_streaming_response.create(
            bucket_ids=["string"],
            input="input",
            request_id="request_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            search = await response.parse()
            assert_matches_type(SearchResponse, search, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncRaindrop) -> None:
        search = await async_client.search.retrieve(
            request_id="request_id",
        )
        assert_matches_type(SearchResponse, search, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncRaindrop) -> None:
        search = await async_client.search.retrieve(
            request_id="request_id",
            page=0,
            page_size=0,
        )
        assert_matches_type(SearchResponse, search, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncRaindrop) -> None:
        response = await async_client.search.with_raw_response.retrieve(
            request_id="request_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        search = await response.parse()
        assert_matches_type(SearchResponse, search, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncRaindrop) -> None:
        async with async_client.search.with_streaming_response.retrieve(
            request_id="request_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            search = await response.parse()
            assert_matches_type(SearchResponse, search, path=["response"])

        assert cast(Any, response.is_closed) is True
