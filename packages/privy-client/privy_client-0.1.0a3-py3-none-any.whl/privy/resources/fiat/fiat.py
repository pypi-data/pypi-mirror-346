# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from .kyc import (
    KYCResource,
    AsyncKYCResource,
    KYCResourceWithRawResponse,
    AsyncKYCResourceWithRawResponse,
    KYCResourceWithStreamingResponse,
    AsyncKYCResourceWithStreamingResponse,
)
from .onramp import (
    OnrampResource,
    AsyncOnrampResource,
    OnrampResourceWithRawResponse,
    AsyncOnrampResourceWithRawResponse,
    OnrampResourceWithStreamingResponse,
    AsyncOnrampResourceWithStreamingResponse,
)
from .offramp import (
    OfframpResource,
    AsyncOfframpResource,
    OfframpResourceWithRawResponse,
    AsyncOfframpResourceWithRawResponse,
    OfframpResourceWithStreamingResponse,
    AsyncOfframpResourceWithStreamingResponse,
)
from .accounts import (
    AccountsResource,
    AsyncAccountsResource,
    AccountsResourceWithRawResponse,
    AsyncAccountsResourceWithRawResponse,
    AccountsResourceWithStreamingResponse,
    AsyncAccountsResourceWithStreamingResponse,
)
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource

__all__ = ["FiatResource", "AsyncFiatResource"]


class FiatResource(SyncAPIResource):
    @cached_property
    def accounts(self) -> AccountsResource:
        return AccountsResource(self._client)

    @cached_property
    def kyc(self) -> KYCResource:
        return KYCResource(self._client)

    @cached_property
    def onramp(self) -> OnrampResource:
        return OnrampResource(self._client)

    @cached_property
    def offramp(self) -> OfframpResource:
        return OfframpResource(self._client)

    @cached_property
    def with_raw_response(self) -> FiatResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/privy-io/python-sdk#accessing-raw-response-data-eg-headers
        """
        return FiatResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> FiatResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/privy-io/python-sdk#with_streaming_response
        """
        return FiatResourceWithStreamingResponse(self)


class AsyncFiatResource(AsyncAPIResource):
    @cached_property
    def accounts(self) -> AsyncAccountsResource:
        return AsyncAccountsResource(self._client)

    @cached_property
    def kyc(self) -> AsyncKYCResource:
        return AsyncKYCResource(self._client)

    @cached_property
    def onramp(self) -> AsyncOnrampResource:
        return AsyncOnrampResource(self._client)

    @cached_property
    def offramp(self) -> AsyncOfframpResource:
        return AsyncOfframpResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncFiatResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/privy-io/python-sdk#accessing-raw-response-data-eg-headers
        """
        return AsyncFiatResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncFiatResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/privy-io/python-sdk#with_streaming_response
        """
        return AsyncFiatResourceWithStreamingResponse(self)


class FiatResourceWithRawResponse:
    def __init__(self, fiat: FiatResource) -> None:
        self._fiat = fiat

    @cached_property
    def accounts(self) -> AccountsResourceWithRawResponse:
        return AccountsResourceWithRawResponse(self._fiat.accounts)

    @cached_property
    def kyc(self) -> KYCResourceWithRawResponse:
        return KYCResourceWithRawResponse(self._fiat.kyc)

    @cached_property
    def onramp(self) -> OnrampResourceWithRawResponse:
        return OnrampResourceWithRawResponse(self._fiat.onramp)

    @cached_property
    def offramp(self) -> OfframpResourceWithRawResponse:
        return OfframpResourceWithRawResponse(self._fiat.offramp)


class AsyncFiatResourceWithRawResponse:
    def __init__(self, fiat: AsyncFiatResource) -> None:
        self._fiat = fiat

    @cached_property
    def accounts(self) -> AsyncAccountsResourceWithRawResponse:
        return AsyncAccountsResourceWithRawResponse(self._fiat.accounts)

    @cached_property
    def kyc(self) -> AsyncKYCResourceWithRawResponse:
        return AsyncKYCResourceWithRawResponse(self._fiat.kyc)

    @cached_property
    def onramp(self) -> AsyncOnrampResourceWithRawResponse:
        return AsyncOnrampResourceWithRawResponse(self._fiat.onramp)

    @cached_property
    def offramp(self) -> AsyncOfframpResourceWithRawResponse:
        return AsyncOfframpResourceWithRawResponse(self._fiat.offramp)


class FiatResourceWithStreamingResponse:
    def __init__(self, fiat: FiatResource) -> None:
        self._fiat = fiat

    @cached_property
    def accounts(self) -> AccountsResourceWithStreamingResponse:
        return AccountsResourceWithStreamingResponse(self._fiat.accounts)

    @cached_property
    def kyc(self) -> KYCResourceWithStreamingResponse:
        return KYCResourceWithStreamingResponse(self._fiat.kyc)

    @cached_property
    def onramp(self) -> OnrampResourceWithStreamingResponse:
        return OnrampResourceWithStreamingResponse(self._fiat.onramp)

    @cached_property
    def offramp(self) -> OfframpResourceWithStreamingResponse:
        return OfframpResourceWithStreamingResponse(self._fiat.offramp)


class AsyncFiatResourceWithStreamingResponse:
    def __init__(self, fiat: AsyncFiatResource) -> None:
        self._fiat = fiat

    @cached_property
    def accounts(self) -> AsyncAccountsResourceWithStreamingResponse:
        return AsyncAccountsResourceWithStreamingResponse(self._fiat.accounts)

    @cached_property
    def kyc(self) -> AsyncKYCResourceWithStreamingResponse:
        return AsyncKYCResourceWithStreamingResponse(self._fiat.kyc)

    @cached_property
    def onramp(self) -> AsyncOnrampResourceWithStreamingResponse:
        return AsyncOnrampResourceWithStreamingResponse(self._fiat.onramp)

    @cached_property
    def offramp(self) -> AsyncOfframpResourceWithStreamingResponse:
        return AsyncOfframpResourceWithStreamingResponse(self._fiat.offramp)
