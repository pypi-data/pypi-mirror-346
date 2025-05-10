# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List

import httpx

from ..types import search_find_params, search_retrieve_params
from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .._utils import maybe_transform, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..pagination import SyncSearchPage, AsyncSearchPage
from .._base_client import AsyncPaginator, make_request_options
from ..types.text_result import TextResult
from ..types.search_response import SearchResponse

__all__ = ["SearchResource", "AsyncSearchResource"]


class SearchResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> SearchResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/LiquidMetal-AI/lm-raindrop-python-sdk#accessing-raw-response-data-eg-headers
        """
        return SearchResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SearchResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/LiquidMetal-AI/lm-raindrop-python-sdk#with_streaming_response
        """
        return SearchResourceWithStreamingResponse(self)

    def retrieve(
        self,
        *,
        request_id: str,
        page: int | NotGiven = NOT_GIVEN,
        page_size: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SyncSearchPage[TextResult]:
        """Retrieve additional pages from a previous search.

        This endpoint enables
        navigation through large result sets while maintaining search context and result
        relevance. Retrieving paginated results requires a valid `request_id` from a
        previously completed search.

        Args:
          request_id: Client-provided search session identifier from the initial search

          page: Requested page number

          page_size: Results per page

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v1/search",
            page=SyncSearchPage[TextResult],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "request_id": request_id,
                        "page": page,
                        "page_size": page_size,
                    },
                    search_retrieve_params.SearchRetrieveParams,
                ),
            ),
            model=TextResult,
        )

    def find(
        self,
        *,
        bucket_ids: List[str],
        input: str,
        request_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SearchResponse:
        """
        Primary search endpoint that provides advanced search capabilities across all
        document types stored in SmartBuckets.

        Supports recursive object search within objects, enabling nested content search
        like embedded images, text content, and personally identifiable information
        (PII).

        The system supports complex queries like:

        - 'Show me documents containing credit card numbers or social security numbers'
        - 'Find images of landscapes taken during sunset'
        - 'Get documents mentioning revenue forecasts from Q4 2023'
        - 'Find me all PDF documents that contain pictures of a cat'
        - 'Find me all audio files that contain infomration about the weather in SF in
          2024'

        Key capabilities:

        - Natural language query understanding
        - Content-based search across text, images, and audio
        - Automatic PII detection
        - Multi-modal search (text, images, audio)

        Args:
          bucket_ids: Optional list of specific bucket IDs to search in. If not provided, searches the
              latest version of all buckets

          input: Natural language search query that can include complex criteria

          request_id: Client-provided search session identifier. Required for pagination and result
              tracking. We recommend using a UUID or ULID for this value.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v1/search",
            body=maybe_transform(
                {
                    "bucket_ids": bucket_ids,
                    "input": input,
                    "request_id": request_id,
                },
                search_find_params.SearchFindParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SearchResponse,
        )


class AsyncSearchResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncSearchResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/LiquidMetal-AI/lm-raindrop-python-sdk#accessing-raw-response-data-eg-headers
        """
        return AsyncSearchResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSearchResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/LiquidMetal-AI/lm-raindrop-python-sdk#with_streaming_response
        """
        return AsyncSearchResourceWithStreamingResponse(self)

    def retrieve(
        self,
        *,
        request_id: str,
        page: int | NotGiven = NOT_GIVEN,
        page_size: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncPaginator[TextResult, AsyncSearchPage[TextResult]]:
        """Retrieve additional pages from a previous search.

        This endpoint enables
        navigation through large result sets while maintaining search context and result
        relevance. Retrieving paginated results requires a valid `request_id` from a
        previously completed search.

        Args:
          request_id: Client-provided search session identifier from the initial search

          page: Requested page number

          page_size: Results per page

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v1/search",
            page=AsyncSearchPage[TextResult],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "request_id": request_id,
                        "page": page,
                        "page_size": page_size,
                    },
                    search_retrieve_params.SearchRetrieveParams,
                ),
            ),
            model=TextResult,
        )

    async def find(
        self,
        *,
        bucket_ids: List[str],
        input: str,
        request_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SearchResponse:
        """
        Primary search endpoint that provides advanced search capabilities across all
        document types stored in SmartBuckets.

        Supports recursive object search within objects, enabling nested content search
        like embedded images, text content, and personally identifiable information
        (PII).

        The system supports complex queries like:

        - 'Show me documents containing credit card numbers or social security numbers'
        - 'Find images of landscapes taken during sunset'
        - 'Get documents mentioning revenue forecasts from Q4 2023'
        - 'Find me all PDF documents that contain pictures of a cat'
        - 'Find me all audio files that contain infomration about the weather in SF in
          2024'

        Key capabilities:

        - Natural language query understanding
        - Content-based search across text, images, and audio
        - Automatic PII detection
        - Multi-modal search (text, images, audio)

        Args:
          bucket_ids: Optional list of specific bucket IDs to search in. If not provided, searches the
              latest version of all buckets

          input: Natural language search query that can include complex criteria

          request_id: Client-provided search session identifier. Required for pagination and result
              tracking. We recommend using a UUID or ULID for this value.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v1/search",
            body=await async_maybe_transform(
                {
                    "bucket_ids": bucket_ids,
                    "input": input,
                    "request_id": request_id,
                },
                search_find_params.SearchFindParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SearchResponse,
        )


class SearchResourceWithRawResponse:
    def __init__(self, search: SearchResource) -> None:
        self._search = search

        self.retrieve = to_raw_response_wrapper(
            search.retrieve,
        )
        self.find = to_raw_response_wrapper(
            search.find,
        )


class AsyncSearchResourceWithRawResponse:
    def __init__(self, search: AsyncSearchResource) -> None:
        self._search = search

        self.retrieve = async_to_raw_response_wrapper(
            search.retrieve,
        )
        self.find = async_to_raw_response_wrapper(
            search.find,
        )


class SearchResourceWithStreamingResponse:
    def __init__(self, search: SearchResource) -> None:
        self._search = search

        self.retrieve = to_streamed_response_wrapper(
            search.retrieve,
        )
        self.find = to_streamed_response_wrapper(
            search.find,
        )


class AsyncSearchResourceWithStreamingResponse:
    def __init__(self, search: AsyncSearchResource) -> None:
        self._search = search

        self.retrieve = async_to_streamed_response_wrapper(
            search.retrieve,
        )
        self.find = async_to_streamed_response_wrapper(
            search.find,
        )
