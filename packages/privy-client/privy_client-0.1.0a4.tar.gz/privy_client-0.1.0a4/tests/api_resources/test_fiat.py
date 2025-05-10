# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from privy import PrivyAPI, AsyncPrivyAPI
from privy.types import FiatConfigureAppResponse
from tests.utils import assert_matches_type

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestFiat:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_configure_app(self, client: PrivyAPI) -> None:
        fiat = client.fiat.configure_app(
            app_id="app_id",
            api_key="x",
            provider="bridge",
        )
        assert_matches_type(FiatConfigureAppResponse, fiat, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_configure_app(self, client: PrivyAPI) -> None:
        response = client.fiat.with_raw_response.configure_app(
            app_id="app_id",
            api_key="x",
            provider="bridge",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        fiat = response.parse()
        assert_matches_type(FiatConfigureAppResponse, fiat, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_configure_app(self, client: PrivyAPI) -> None:
        with client.fiat.with_streaming_response.configure_app(
            app_id="app_id",
            api_key="x",
            provider="bridge",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            fiat = response.parse()
            assert_matches_type(FiatConfigureAppResponse, fiat, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_configure_app(self, client: PrivyAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `app_id` but received ''"):
            client.fiat.with_raw_response.configure_app(
                app_id="",
                api_key="x",
                provider="bridge",
            )


class TestAsyncFiat:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_configure_app(self, async_client: AsyncPrivyAPI) -> None:
        fiat = await async_client.fiat.configure_app(
            app_id="app_id",
            api_key="x",
            provider="bridge",
        )
        assert_matches_type(FiatConfigureAppResponse, fiat, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_configure_app(self, async_client: AsyncPrivyAPI) -> None:
        response = await async_client.fiat.with_raw_response.configure_app(
            app_id="app_id",
            api_key="x",
            provider="bridge",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        fiat = await response.parse()
        assert_matches_type(FiatConfigureAppResponse, fiat, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_configure_app(self, async_client: AsyncPrivyAPI) -> None:
        async with async_client.fiat.with_streaming_response.configure_app(
            app_id="app_id",
            api_key="x",
            provider="bridge",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            fiat = await response.parse()
            assert_matches_type(FiatConfigureAppResponse, fiat, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_configure_app(self, async_client: AsyncPrivyAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `app_id` but received ''"):
            await async_client.fiat.with_raw_response.configure_app(
                app_id="",
                api_key="x",
                provider="bridge",
            )
