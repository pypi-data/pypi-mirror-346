# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from privy import PrivyAPI, AsyncPrivyAPI
from tests.utils import assert_matches_type
from privy.types.fiat import OfframpCreateResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestOfframp:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create(self, client: PrivyAPI) -> None:
        offramp = client.fiat.offramp.create(
            user_id="user_id",
            amount="x",
            destination={
                "currency": "usd",
                "external_account_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "payment_rail": "sepa",
            },
            provider="bridge",
            source={
                "chain": "ethereum",
                "currency": "usdc",
                "from_address": "from_address",
            },
        )
        assert_matches_type(OfframpCreateResponse, offramp, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create(self, client: PrivyAPI) -> None:
        response = client.fiat.offramp.with_raw_response.create(
            user_id="user_id",
            amount="x",
            destination={
                "currency": "usd",
                "external_account_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "payment_rail": "sepa",
            },
            provider="bridge",
            source={
                "chain": "ethereum",
                "currency": "usdc",
                "from_address": "from_address",
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        offramp = response.parse()
        assert_matches_type(OfframpCreateResponse, offramp, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create(self, client: PrivyAPI) -> None:
        with client.fiat.offramp.with_streaming_response.create(
            user_id="user_id",
            amount="x",
            destination={
                "currency": "usd",
                "external_account_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "payment_rail": "sepa",
            },
            provider="bridge",
            source={
                "chain": "ethereum",
                "currency": "usdc",
                "from_address": "from_address",
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            offramp = response.parse()
            assert_matches_type(OfframpCreateResponse, offramp, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_create(self, client: PrivyAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `user_id` but received ''"):
            client.fiat.offramp.with_raw_response.create(
                user_id="",
                amount="x",
                destination={
                    "currency": "usd",
                    "external_account_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    "payment_rail": "sepa",
                },
                provider="bridge",
                source={
                    "chain": "ethereum",
                    "currency": "usdc",
                    "from_address": "from_address",
                },
            )


class TestAsyncOfframp:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create(self, async_client: AsyncPrivyAPI) -> None:
        offramp = await async_client.fiat.offramp.create(
            user_id="user_id",
            amount="x",
            destination={
                "currency": "usd",
                "external_account_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "payment_rail": "sepa",
            },
            provider="bridge",
            source={
                "chain": "ethereum",
                "currency": "usdc",
                "from_address": "from_address",
            },
        )
        assert_matches_type(OfframpCreateResponse, offramp, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncPrivyAPI) -> None:
        response = await async_client.fiat.offramp.with_raw_response.create(
            user_id="user_id",
            amount="x",
            destination={
                "currency": "usd",
                "external_account_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "payment_rail": "sepa",
            },
            provider="bridge",
            source={
                "chain": "ethereum",
                "currency": "usdc",
                "from_address": "from_address",
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        offramp = await response.parse()
        assert_matches_type(OfframpCreateResponse, offramp, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncPrivyAPI) -> None:
        async with async_client.fiat.offramp.with_streaming_response.create(
            user_id="user_id",
            amount="x",
            destination={
                "currency": "usd",
                "external_account_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "payment_rail": "sepa",
            },
            provider="bridge",
            source={
                "chain": "ethereum",
                "currency": "usdc",
                "from_address": "from_address",
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            offramp = await response.parse()
            assert_matches_type(OfframpCreateResponse, offramp, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_create(self, async_client: AsyncPrivyAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `user_id` but received ''"):
            await async_client.fiat.offramp.with_raw_response.create(
                user_id="",
                amount="x",
                destination={
                    "currency": "usd",
                    "external_account_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    "payment_rail": "sepa",
                },
                provider="bridge",
                source={
                    "chain": "ethereum",
                    "currency": "usdc",
                    "from_address": "from_address",
                },
            )
