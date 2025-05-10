# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import httpx
import pytest
from respx import MockRouter

from lm_raindrop import Raindrop, AsyncRaindrop
from tests.utils import assert_matches_type
from lm_raindrop.types import (
    StorageObjectListResponse,
    StorageObjectDeleteResponse,
    StorageObjectUploadResponse,
)
from lm_raindrop._response import (
    BinaryAPIResponse,
    AsyncBinaryAPIResponse,
    StreamedBinaryAPIResponse,
    AsyncStreamedBinaryAPIResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestStorageObject:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_list(self, client: Raindrop) -> None:
        storage_object = client.storage_object.list(
            "bucket",
        )
        assert_matches_type(StorageObjectListResponse, storage_object, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list(self, client: Raindrop) -> None:
        response = client.storage_object.with_raw_response.list(
            "bucket",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        storage_object = response.parse()
        assert_matches_type(StorageObjectListResponse, storage_object, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list(self, client: Raindrop) -> None:
        with client.storage_object.with_streaming_response.list(
            "bucket",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            storage_object = response.parse()
            assert_matches_type(StorageObjectListResponse, storage_object, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_list(self, client: Raindrop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bucket` but received ''"):
            client.storage_object.with_raw_response.list(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_delete(self, client: Raindrop) -> None:
        storage_object = client.storage_object.delete(
            key="my-key",
            bucket="01jtgtrd37acrqf7k24dggg31s",
        )
        assert_matches_type(StorageObjectDeleteResponse, storage_object, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_delete(self, client: Raindrop) -> None:
        response = client.storage_object.with_raw_response.delete(
            key="my-key",
            bucket="01jtgtrd37acrqf7k24dggg31s",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        storage_object = response.parse()
        assert_matches_type(StorageObjectDeleteResponse, storage_object, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_delete(self, client: Raindrop) -> None:
        with client.storage_object.with_streaming_response.delete(
            key="my-key",
            bucket="01jtgtrd37acrqf7k24dggg31s",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            storage_object = response.parse()
            assert_matches_type(StorageObjectDeleteResponse, storage_object, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_delete(self, client: Raindrop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bucket` but received ''"):
            client.storage_object.with_raw_response.delete(
                key="my-key",
                bucket="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `key` but received ''"):
            client.storage_object.with_raw_response.delete(
                key="",
                bucket="01jtgtrd37acrqf7k24dggg31s",
            )

    @pytest.mark.skip()
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_download(self, client: Raindrop, respx_mock: MockRouter) -> None:
        respx_mock.get("/v1/object/01jtgtrd37acrqf7k24dggg31s/my-key").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        storage_object = client.storage_object.download(
            key="my-key",
            bucket="01jtgtrd37acrqf7k24dggg31s",
        )
        assert storage_object.is_closed
        assert storage_object.json() == {"foo": "bar"}
        assert cast(Any, storage_object.is_closed) is True
        assert isinstance(storage_object, BinaryAPIResponse)

    @pytest.mark.skip()
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_download(self, client: Raindrop, respx_mock: MockRouter) -> None:
        respx_mock.get("/v1/object/01jtgtrd37acrqf7k24dggg31s/my-key").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        storage_object = client.storage_object.with_raw_response.download(
            key="my-key",
            bucket="01jtgtrd37acrqf7k24dggg31s",
        )

        assert storage_object.is_closed is True
        assert storage_object.http_request.headers.get("X-Stainless-Lang") == "python"
        assert storage_object.json() == {"foo": "bar"}
        assert isinstance(storage_object, BinaryAPIResponse)

    @pytest.mark.skip()
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_download(self, client: Raindrop, respx_mock: MockRouter) -> None:
        respx_mock.get("/v1/object/01jtgtrd37acrqf7k24dggg31s/my-key").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.storage_object.with_streaming_response.download(
            key="my-key",
            bucket="01jtgtrd37acrqf7k24dggg31s",
        ) as storage_object:
            assert not storage_object.is_closed
            assert storage_object.http_request.headers.get("X-Stainless-Lang") == "python"

            assert storage_object.json() == {"foo": "bar"}
            assert cast(Any, storage_object.is_closed) is True
            assert isinstance(storage_object, StreamedBinaryAPIResponse)

        assert cast(Any, storage_object.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_download(self, client: Raindrop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bucket` but received ''"):
            client.storage_object.with_raw_response.download(
                key="my-key",
                bucket="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `key` but received ''"):
            client.storage_object.with_raw_response.download(
                key="",
                bucket="01jtgtrd37acrqf7k24dggg31s",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_upload(self, client: Raindrop) -> None:
        storage_object = client.storage_object.upload(
            key="my-key",
            bucket="01jtgtrd37acrqf7k24dggg31s",
            body=b"raw file contents",
        )
        assert_matches_type(StorageObjectUploadResponse, storage_object, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_upload(self, client: Raindrop) -> None:
        response = client.storage_object.with_raw_response.upload(
            key="my-key",
            bucket="01jtgtrd37acrqf7k24dggg31s",
            body=b"raw file contents",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        storage_object = response.parse()
        assert_matches_type(StorageObjectUploadResponse, storage_object, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_upload(self, client: Raindrop) -> None:
        with client.storage_object.with_streaming_response.upload(
            key="my-key",
            bucket="01jtgtrd37acrqf7k24dggg31s",
            body=b"raw file contents",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            storage_object = response.parse()
            assert_matches_type(StorageObjectUploadResponse, storage_object, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_upload(self, client: Raindrop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bucket` but received ''"):
            client.storage_object.with_raw_response.upload(
                key="my-key",
                bucket="",
                body=b"raw file contents",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `key` but received ''"):
            client.storage_object.with_raw_response.upload(
                key="",
                bucket="01jtgtrd37acrqf7k24dggg31s",
                body=b"raw file contents",
            )


class TestAsyncStorageObject:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_list(self, async_client: AsyncRaindrop) -> None:
        storage_object = await async_client.storage_object.list(
            "bucket",
        )
        assert_matches_type(StorageObjectListResponse, storage_object, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncRaindrop) -> None:
        response = await async_client.storage_object.with_raw_response.list(
            "bucket",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        storage_object = await response.parse()
        assert_matches_type(StorageObjectListResponse, storage_object, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncRaindrop) -> None:
        async with async_client.storage_object.with_streaming_response.list(
            "bucket",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            storage_object = await response.parse()
            assert_matches_type(StorageObjectListResponse, storage_object, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_list(self, async_client: AsyncRaindrop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bucket` but received ''"):
            await async_client.storage_object.with_raw_response.list(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_delete(self, async_client: AsyncRaindrop) -> None:
        storage_object = await async_client.storage_object.delete(
            key="my-key",
            bucket="01jtgtrd37acrqf7k24dggg31s",
        )
        assert_matches_type(StorageObjectDeleteResponse, storage_object, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncRaindrop) -> None:
        response = await async_client.storage_object.with_raw_response.delete(
            key="my-key",
            bucket="01jtgtrd37acrqf7k24dggg31s",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        storage_object = await response.parse()
        assert_matches_type(StorageObjectDeleteResponse, storage_object, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncRaindrop) -> None:
        async with async_client.storage_object.with_streaming_response.delete(
            key="my-key",
            bucket="01jtgtrd37acrqf7k24dggg31s",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            storage_object = await response.parse()
            assert_matches_type(StorageObjectDeleteResponse, storage_object, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_delete(self, async_client: AsyncRaindrop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bucket` but received ''"):
            await async_client.storage_object.with_raw_response.delete(
                key="my-key",
                bucket="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `key` but received ''"):
            await async_client.storage_object.with_raw_response.delete(
                key="",
                bucket="01jtgtrd37acrqf7k24dggg31s",
            )

    @pytest.mark.skip()
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_download(self, async_client: AsyncRaindrop, respx_mock: MockRouter) -> None:
        respx_mock.get("/v1/object/01jtgtrd37acrqf7k24dggg31s/my-key").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        storage_object = await async_client.storage_object.download(
            key="my-key",
            bucket="01jtgtrd37acrqf7k24dggg31s",
        )
        assert storage_object.is_closed
        assert await storage_object.json() == {"foo": "bar"}
        assert cast(Any, storage_object.is_closed) is True
        assert isinstance(storage_object, AsyncBinaryAPIResponse)

    @pytest.mark.skip()
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_download(self, async_client: AsyncRaindrop, respx_mock: MockRouter) -> None:
        respx_mock.get("/v1/object/01jtgtrd37acrqf7k24dggg31s/my-key").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        storage_object = await async_client.storage_object.with_raw_response.download(
            key="my-key",
            bucket="01jtgtrd37acrqf7k24dggg31s",
        )

        assert storage_object.is_closed is True
        assert storage_object.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await storage_object.json() == {"foo": "bar"}
        assert isinstance(storage_object, AsyncBinaryAPIResponse)

    @pytest.mark.skip()
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_download(self, async_client: AsyncRaindrop, respx_mock: MockRouter) -> None:
        respx_mock.get("/v1/object/01jtgtrd37acrqf7k24dggg31s/my-key").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.storage_object.with_streaming_response.download(
            key="my-key",
            bucket="01jtgtrd37acrqf7k24dggg31s",
        ) as storage_object:
            assert not storage_object.is_closed
            assert storage_object.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await storage_object.json() == {"foo": "bar"}
            assert cast(Any, storage_object.is_closed) is True
            assert isinstance(storage_object, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, storage_object.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_download(self, async_client: AsyncRaindrop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bucket` but received ''"):
            await async_client.storage_object.with_raw_response.download(
                key="my-key",
                bucket="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `key` but received ''"):
            await async_client.storage_object.with_raw_response.download(
                key="",
                bucket="01jtgtrd37acrqf7k24dggg31s",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_upload(self, async_client: AsyncRaindrop) -> None:
        storage_object = await async_client.storage_object.upload(
            key="my-key",
            bucket="01jtgtrd37acrqf7k24dggg31s",
            body=b"raw file contents",
        )
        assert_matches_type(StorageObjectUploadResponse, storage_object, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_upload(self, async_client: AsyncRaindrop) -> None:
        response = await async_client.storage_object.with_raw_response.upload(
            key="my-key",
            bucket="01jtgtrd37acrqf7k24dggg31s",
            body=b"raw file contents",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        storage_object = await response.parse()
        assert_matches_type(StorageObjectUploadResponse, storage_object, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_upload(self, async_client: AsyncRaindrop) -> None:
        async with async_client.storage_object.with_streaming_response.upload(
            key="my-key",
            bucket="01jtgtrd37acrqf7k24dggg31s",
            body=b"raw file contents",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            storage_object = await response.parse()
            assert_matches_type(StorageObjectUploadResponse, storage_object, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_upload(self, async_client: AsyncRaindrop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bucket` but received ''"):
            await async_client.storage_object.with_raw_response.upload(
                key="my-key",
                bucket="",
                body=b"raw file contents",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `key` but received ''"):
            await async_client.storage_object.with_raw_response.upload(
                key="",
                bucket="01jtgtrd37acrqf7k24dggg31s",
                body=b"raw file contents",
            )
