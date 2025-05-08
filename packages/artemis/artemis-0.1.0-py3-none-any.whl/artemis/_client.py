# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, Union, Mapping
from datetime import date
from typing_extensions import Self, override

import httpx

from . import _exceptions
from ._qs import Querystring
from .types import (
    client_fetch_metrics_params,
    client_fetch_weekly_commits_params,
    client_fetch_weekly_active_devs_params,
)
from ._types import (
    NOT_GIVEN,
    Body,
    Omit,
    Query,
    Headers,
    Timeout,
    NotGiven,
    Transport,
    ProxiesTypes,
    RequestOptions,
)
from ._utils import (
    is_given,
    maybe_transform,
    get_async_library,
    async_maybe_transform,
)
from ._version import __version__
from ._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .resources import asset
from ._streaming import Stream as Stream, AsyncStream as AsyncStream
from ._exceptions import APIStatusError
from ._base_client import (
    DEFAULT_MAX_RETRIES,
    SyncAPIClient,
    AsyncAPIClient,
    make_request_options,
)
from .types.fetch_metrics_response import FetchMetricsResponse
from .types.list_ecosystems_response import ListEcosystemsResponse
from .types.fetch_weekly_commits_response import FetchWeeklyCommitsResponse
from .types.fetch_weekly_active_devs_response import FetchWeeklyActiveDevsResponse

__all__ = ["Timeout", "Transport", "ProxiesTypes", "RequestOptions", "Artemis", "AsyncArtemis", "Client", "AsyncClient"]


class Artemis(SyncAPIClient):
    asset: asset.AssetResource
    with_raw_response: ArtemisWithRawResponse
    with_streaming_response: ArtemisWithStreamedResponse

    # client options
    api_key: str | None

    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: Union[float, Timeout, None, NotGiven] = NOT_GIVEN,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client.
        # We provide a `DefaultHttpxClient` class that you can pass to retain the default values we use for `limits`, `timeout` & `follow_redirects`.
        # See the [httpx documentation](https://www.python-httpx.org/api/#client) for more details.
        http_client: httpx.Client | None = None,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new synchronous Artemis client instance.

        This automatically infers the `api_key` argument from the `ARTEMIS_API_KEY` environment variable if it is not provided.
        """
        if api_key is None:
            api_key = os.environ.get("ARTEMIS_API_KEY")
        self.api_key = api_key

        if base_url is None:
            base_url = os.environ.get("ARTEMIS_BASE_URL")
        if base_url is None:
            base_url = f"https://api.artemisxyz.com"

        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            http_client=http_client,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )

        self.asset = asset.AssetResource(self)
        self.with_raw_response = ArtemisWithRawResponse(self)
        self.with_streaming_response = ArtemisWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": "false",
            **self._custom_headers,
        }

    @property
    @override
    def default_query(self) -> dict[str, object]:
        return {
            **super().default_query,
            "APIKey": self.api_key if self.api_key is not None else Omit(),
            **self._custom_query,
        }

    def copy(
        self,
        *,
        api_key: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = NOT_GIVEN,
        http_client: httpx.Client | None = None,
        max_retries: int | NotGiven = NOT_GIVEN,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.
        """
        if default_headers is not None and set_default_headers is not None:
            raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")

        if default_query is not None and set_default_query is not None:
            raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")

        headers = self._custom_headers
        if default_headers is not None:
            headers = {**headers, **default_headers}
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        http_client = http_client or self._client
        return self.__class__(
            api_key=api_key or self.api_key,
            base_url=base_url or self.base_url,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            **_extra_kwargs,
        )

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    def fetch_metrics(
        self,
        metric_names: str,
        *,
        symbols: str,
        end_date: Union[str, date] | NotGiven = NOT_GIVEN,
        start_date: Union[str, date] | NotGiven = NOT_GIVEN,
        summarize: bool | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> FetchMetricsResponse:
        """
        Fetch metrics for assets

        Args:
          symbols: Symbols, comma-separated

          end_date: End date for time range

          start_date: Start date for time range

          summarize: When true, will calculate the percent change for a metric from startDate to
              endDate

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not metric_names:
            raise ValueError(f"Expected a non-empty value for `metric_names` but received {metric_names!r}")
        return self.get(
            f"/data/{metric_names}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "symbols": symbols,
                        "end_date": end_date,
                        "start_date": start_date,
                        "summarize": summarize,
                    },
                    client_fetch_metrics_params.ClientFetchMetricsParams,
                ),
            ),
            cast_to=FetchMetricsResponse,
        )

    def fetch_weekly_active_devs(
        self,
        *,
        days_back: int | NotGiven = NOT_GIVEN,
        ecosystem: str | NotGiven = NOT_GIVEN,
        include_forks: bool | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> FetchWeeklyActiveDevsResponse:
        """
        Get weekly active developers (ie, the number of developers who have made at
        least one commit to the specified ecosystem) for the given week.

        Our response breaks up weekly developer activity into two segments: _Core_ &
        _Sub-Ecosystems_: _Core_ refers to activity for Github repos associated directly
        with the chain/protocol. E.g., if pulling data for Ethereum, Core activity would
        be developer activity for Geth. _Sub-Ecosystem_ refers to a project that's built
        on top of Ethereum, such as Aave.

        Args:
          days_back: How many days back from today to pull data for. Data is weekly

          ecosystem: Name of of the ecosystem (ie chain/protocol). The full list of names is
              available from /dev-ecosystems. Omit to fetch data for all ecosystems

          include_forks: If true, count forks in addition to the original repos

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self.get(
            "/weekly-active-devs",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "days_back": days_back,
                        "ecosystem": ecosystem,
                        "include_forks": include_forks,
                    },
                    client_fetch_weekly_active_devs_params.ClientFetchWeeklyActiveDevsParams,
                ),
            ),
            cast_to=FetchWeeklyActiveDevsResponse,
        )

    def fetch_weekly_commits(
        self,
        *,
        days_back: int | NotGiven = NOT_GIVEN,
        ecosystem: str | NotGiven = NOT_GIVEN,
        include_forks: bool | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> FetchWeeklyCommitsResponse:
        """
        Get weekly commits by developers for all or a specific chain/protocol over time.

        Our response breaks up weekly developer activity into two segments: _Core_ &
        _Sub-Ecosystems_: _Core_ refers to activity for Github repos associated directly
        with the chain/protocol. E.g., if pulling data for Ethereum, Core activity would
        be developer activity for Geth. _Sub-Ecosystem_ refers to a project that's built
        on top of Ethereum, such as Aave.

        Args:
          days_back: How many days back from today to pull data for. Data is weekly

          ecosystem: Name of of the ecosystem (ie chain/protocol). The full list of names is
              available from /dev-ecosystems. Omit to fetch data for all ecosystems

          include_forks: If true, count forks in addition to the original repos

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self.get(
            "/weekly-commits",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "days_back": days_back,
                        "ecosystem": ecosystem,
                        "include_forks": include_forks,
                    },
                    client_fetch_weekly_commits_params.ClientFetchWeeklyCommitsParams,
                ),
            ),
            cast_to=FetchWeeklyCommitsResponse,
        )

    def list_ecosystems(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ListEcosystemsResponse:
        """
        We pull developer activity data from Github once a week for all the ecosystems
        (chains/protocols) mapped by
        [Electric Capital's crypto-ecosystems project](https://github.com/electric-capital/crypto-ecosystems).
        This API provides a comprehensive view into how active developers are in web3.

        Only open-source public Github repositories are counted.
        """
        return self.get(
            "/dev-ecosystems",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ListEcosystemsResponse,
        )

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx.Response,
    ) -> APIStatusError:
        if response.status_code == 400:
            return _exceptions.BadRequestError(err_msg, response=response, body=body)

        if response.status_code == 401:
            return _exceptions.AuthenticationError(err_msg, response=response, body=body)

        if response.status_code == 403:
            return _exceptions.PermissionDeniedError(err_msg, response=response, body=body)

        if response.status_code == 404:
            return _exceptions.NotFoundError(err_msg, response=response, body=body)

        if response.status_code == 409:
            return _exceptions.ConflictError(err_msg, response=response, body=body)

        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(err_msg, response=response, body=body)

        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=body)

        if response.status_code >= 500:
            return _exceptions.InternalServerError(err_msg, response=response, body=body)
        return APIStatusError(err_msg, response=response, body=body)


class AsyncArtemis(AsyncAPIClient):
    asset: asset.AsyncAssetResource
    with_raw_response: AsyncArtemisWithRawResponse
    with_streaming_response: AsyncArtemisWithStreamedResponse

    # client options
    api_key: str | None

    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: Union[float, Timeout, None, NotGiven] = NOT_GIVEN,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client.
        # We provide a `DefaultAsyncHttpxClient` class that you can pass to retain the default values we use for `limits`, `timeout` & `follow_redirects`.
        # See the [httpx documentation](https://www.python-httpx.org/api/#asyncclient) for more details.
        http_client: httpx.AsyncClient | None = None,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new async AsyncArtemis client instance.

        This automatically infers the `api_key` argument from the `ARTEMIS_API_KEY` environment variable if it is not provided.
        """
        if api_key is None:
            api_key = os.environ.get("ARTEMIS_API_KEY")
        self.api_key = api_key

        if base_url is None:
            base_url = os.environ.get("ARTEMIS_BASE_URL")
        if base_url is None:
            base_url = f"https://api.artemisxyz.com"

        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            http_client=http_client,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )

        self.asset = asset.AsyncAssetResource(self)
        self.with_raw_response = AsyncArtemisWithRawResponse(self)
        self.with_streaming_response = AsyncArtemisWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": f"async:{get_async_library()}",
            **self._custom_headers,
        }

    @property
    @override
    def default_query(self) -> dict[str, object]:
        return {
            **super().default_query,
            "APIKey": self.api_key if self.api_key is not None else Omit(),
            **self._custom_query,
        }

    def copy(
        self,
        *,
        api_key: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = NOT_GIVEN,
        http_client: httpx.AsyncClient | None = None,
        max_retries: int | NotGiven = NOT_GIVEN,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.
        """
        if default_headers is not None and set_default_headers is not None:
            raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")

        if default_query is not None and set_default_query is not None:
            raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")

        headers = self._custom_headers
        if default_headers is not None:
            headers = {**headers, **default_headers}
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        http_client = http_client or self._client
        return self.__class__(
            api_key=api_key or self.api_key,
            base_url=base_url or self.base_url,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            **_extra_kwargs,
        )

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    async def fetch_metrics(
        self,
        metric_names: str,
        *,
        symbols: str,
        end_date: Union[str, date] | NotGiven = NOT_GIVEN,
        start_date: Union[str, date] | NotGiven = NOT_GIVEN,
        summarize: bool | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> FetchMetricsResponse:
        """
        Fetch metrics for assets

        Args:
          symbols: Symbols, comma-separated

          end_date: End date for time range

          start_date: Start date for time range

          summarize: When true, will calculate the percent change for a metric from startDate to
              endDate

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not metric_names:
            raise ValueError(f"Expected a non-empty value for `metric_names` but received {metric_names!r}")
        return await self.get(
            f"/data/{metric_names}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "symbols": symbols,
                        "end_date": end_date,
                        "start_date": start_date,
                        "summarize": summarize,
                    },
                    client_fetch_metrics_params.ClientFetchMetricsParams,
                ),
            ),
            cast_to=FetchMetricsResponse,
        )

    async def fetch_weekly_active_devs(
        self,
        *,
        days_back: int | NotGiven = NOT_GIVEN,
        ecosystem: str | NotGiven = NOT_GIVEN,
        include_forks: bool | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> FetchWeeklyActiveDevsResponse:
        """
        Get weekly active developers (ie, the number of developers who have made at
        least one commit to the specified ecosystem) for the given week.

        Our response breaks up weekly developer activity into two segments: _Core_ &
        _Sub-Ecosystems_: _Core_ refers to activity for Github repos associated directly
        with the chain/protocol. E.g., if pulling data for Ethereum, Core activity would
        be developer activity for Geth. _Sub-Ecosystem_ refers to a project that's built
        on top of Ethereum, such as Aave.

        Args:
          days_back: How many days back from today to pull data for. Data is weekly

          ecosystem: Name of of the ecosystem (ie chain/protocol). The full list of names is
              available from /dev-ecosystems. Omit to fetch data for all ecosystems

          include_forks: If true, count forks in addition to the original repos

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self.get(
            "/weekly-active-devs",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "days_back": days_back,
                        "ecosystem": ecosystem,
                        "include_forks": include_forks,
                    },
                    client_fetch_weekly_active_devs_params.ClientFetchWeeklyActiveDevsParams,
                ),
            ),
            cast_to=FetchWeeklyActiveDevsResponse,
        )

    async def fetch_weekly_commits(
        self,
        *,
        days_back: int | NotGiven = NOT_GIVEN,
        ecosystem: str | NotGiven = NOT_GIVEN,
        include_forks: bool | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> FetchWeeklyCommitsResponse:
        """
        Get weekly commits by developers for all or a specific chain/protocol over time.

        Our response breaks up weekly developer activity into two segments: _Core_ &
        _Sub-Ecosystems_: _Core_ refers to activity for Github repos associated directly
        with the chain/protocol. E.g., if pulling data for Ethereum, Core activity would
        be developer activity for Geth. _Sub-Ecosystem_ refers to a project that's built
        on top of Ethereum, such as Aave.

        Args:
          days_back: How many days back from today to pull data for. Data is weekly

          ecosystem: Name of of the ecosystem (ie chain/protocol). The full list of names is
              available from /dev-ecosystems. Omit to fetch data for all ecosystems

          include_forks: If true, count forks in addition to the original repos

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self.get(
            "/weekly-commits",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "days_back": days_back,
                        "ecosystem": ecosystem,
                        "include_forks": include_forks,
                    },
                    client_fetch_weekly_commits_params.ClientFetchWeeklyCommitsParams,
                ),
            ),
            cast_to=FetchWeeklyCommitsResponse,
        )

    async def list_ecosystems(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ListEcosystemsResponse:
        """
        We pull developer activity data from Github once a week for all the ecosystems
        (chains/protocols) mapped by
        [Electric Capital's crypto-ecosystems project](https://github.com/electric-capital/crypto-ecosystems).
        This API provides a comprehensive view into how active developers are in web3.

        Only open-source public Github repositories are counted.
        """
        return await self.get(
            "/dev-ecosystems",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ListEcosystemsResponse,
        )

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx.Response,
    ) -> APIStatusError:
        if response.status_code == 400:
            return _exceptions.BadRequestError(err_msg, response=response, body=body)

        if response.status_code == 401:
            return _exceptions.AuthenticationError(err_msg, response=response, body=body)

        if response.status_code == 403:
            return _exceptions.PermissionDeniedError(err_msg, response=response, body=body)

        if response.status_code == 404:
            return _exceptions.NotFoundError(err_msg, response=response, body=body)

        if response.status_code == 409:
            return _exceptions.ConflictError(err_msg, response=response, body=body)

        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(err_msg, response=response, body=body)

        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=body)

        if response.status_code >= 500:
            return _exceptions.InternalServerError(err_msg, response=response, body=body)
        return APIStatusError(err_msg, response=response, body=body)


class ArtemisWithRawResponse:
    def __init__(self, client: Artemis) -> None:
        self.asset = asset.AssetResourceWithRawResponse(client.asset)

        self.fetch_metrics = to_raw_response_wrapper(
            client.fetch_metrics,
        )
        self.fetch_weekly_active_devs = to_raw_response_wrapper(
            client.fetch_weekly_active_devs,
        )
        self.fetch_weekly_commits = to_raw_response_wrapper(
            client.fetch_weekly_commits,
        )
        self.list_ecosystems = to_raw_response_wrapper(
            client.list_ecosystems,
        )


class AsyncArtemisWithRawResponse:
    def __init__(self, client: AsyncArtemis) -> None:
        self.asset = asset.AsyncAssetResourceWithRawResponse(client.asset)

        self.fetch_metrics = async_to_raw_response_wrapper(
            client.fetch_metrics,
        )
        self.fetch_weekly_active_devs = async_to_raw_response_wrapper(
            client.fetch_weekly_active_devs,
        )
        self.fetch_weekly_commits = async_to_raw_response_wrapper(
            client.fetch_weekly_commits,
        )
        self.list_ecosystems = async_to_raw_response_wrapper(
            client.list_ecosystems,
        )


class ArtemisWithStreamedResponse:
    def __init__(self, client: Artemis) -> None:
        self.asset = asset.AssetResourceWithStreamingResponse(client.asset)

        self.fetch_metrics = to_streamed_response_wrapper(
            client.fetch_metrics,
        )
        self.fetch_weekly_active_devs = to_streamed_response_wrapper(
            client.fetch_weekly_active_devs,
        )
        self.fetch_weekly_commits = to_streamed_response_wrapper(
            client.fetch_weekly_commits,
        )
        self.list_ecosystems = to_streamed_response_wrapper(
            client.list_ecosystems,
        )


class AsyncArtemisWithStreamedResponse:
    def __init__(self, client: AsyncArtemis) -> None:
        self.asset = asset.AsyncAssetResourceWithStreamingResponse(client.asset)

        self.fetch_metrics = async_to_streamed_response_wrapper(
            client.fetch_metrics,
        )
        self.fetch_weekly_active_devs = async_to_streamed_response_wrapper(
            client.fetch_weekly_active_devs,
        )
        self.fetch_weekly_commits = async_to_streamed_response_wrapper(
            client.fetch_weekly_commits,
        )
        self.list_ecosystems = async_to_streamed_response_wrapper(
            client.list_ecosystems,
        )


Client = Artemis

AsyncClient = AsyncArtemis
