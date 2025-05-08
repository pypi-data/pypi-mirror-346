# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.asset_list_response import AssetListResponse
from ..types.asset_list_metrics_response import AssetListMetricsResponse

__all__ = ["AssetResource", "AsyncAssetResource"]


class AssetResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AssetResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/Artemis-xyz/artemis#accessing-raw-response-data-eg-headers
        """
        return AssetResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AssetResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/Artemis-xyz/artemis#with_streaming_response
        """
        return AssetResourceWithStreamingResponse(self)

    def list(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AssetListResponse:
        """List supported assets"""
        return self._get(
            "/asset",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AssetListResponse,
        )

    def list_metrics(
        self,
        artemis_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AssetListMetricsResponse:
        """
        List available metrics for asset

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not artemis_id:
            raise ValueError(f"Expected a non-empty value for `artemis_id` but received {artemis_id!r}")
        return self._get(
            f"/asset/{artemis_id}/metric",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AssetListMetricsResponse,
        )


class AsyncAssetResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncAssetResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/Artemis-xyz/artemis#accessing-raw-response-data-eg-headers
        """
        return AsyncAssetResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncAssetResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/Artemis-xyz/artemis#with_streaming_response
        """
        return AsyncAssetResourceWithStreamingResponse(self)

    async def list(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AssetListResponse:
        """List supported assets"""
        return await self._get(
            "/asset",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AssetListResponse,
        )

    async def list_metrics(
        self,
        artemis_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AssetListMetricsResponse:
        """
        List available metrics for asset

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not artemis_id:
            raise ValueError(f"Expected a non-empty value for `artemis_id` but received {artemis_id!r}")
        return await self._get(
            f"/asset/{artemis_id}/metric",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AssetListMetricsResponse,
        )


class AssetResourceWithRawResponse:
    def __init__(self, asset: AssetResource) -> None:
        self._asset = asset

        self.list = to_raw_response_wrapper(
            asset.list,
        )
        self.list_metrics = to_raw_response_wrapper(
            asset.list_metrics,
        )


class AsyncAssetResourceWithRawResponse:
    def __init__(self, asset: AsyncAssetResource) -> None:
        self._asset = asset

        self.list = async_to_raw_response_wrapper(
            asset.list,
        )
        self.list_metrics = async_to_raw_response_wrapper(
            asset.list_metrics,
        )


class AssetResourceWithStreamingResponse:
    def __init__(self, asset: AssetResource) -> None:
        self._asset = asset

        self.list = to_streamed_response_wrapper(
            asset.list,
        )
        self.list_metrics = to_streamed_response_wrapper(
            asset.list_metrics,
        )


class AsyncAssetResourceWithStreamingResponse:
    def __init__(self, asset: AsyncAssetResource) -> None:
        self._asset = asset

        self.list = async_to_streamed_response_wrapper(
            asset.list,
        )
        self.list_metrics = async_to_streamed_response_wrapper(
            asset.list_metrics,
        )
