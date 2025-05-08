# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from flow_ai_sdk import FlowAISDK, AsyncFlowAISDK
from tests.utils import assert_matches_type
from flow_ai_sdk.types.api.v1.users import UserRead

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestMe:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve(self, client: FlowAISDK) -> None:
        me = client.api.v1.users.me.retrieve()
        assert_matches_type(UserRead, me, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve(self, client: FlowAISDK) -> None:
        response = client.api.v1.users.me.with_raw_response.retrieve()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        me = response.parse()
        assert_matches_type(UserRead, me, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve(self, client: FlowAISDK) -> None:
        with client.api.v1.users.me.with_streaming_response.retrieve() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            me = response.parse()
            assert_matches_type(UserRead, me, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_update(self, client: FlowAISDK) -> None:
        me = client.api.v1.users.me.update()
        assert_matches_type(UserRead, me, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_update_with_all_params(self, client: FlowAISDK) -> None:
        me = client.api.v1.users.me.update(
            email="dev@stainless.com",
            first_name="first_name",
            image_url="image_url",
            is_active=True,
            last_name="last_name",
            preferences={"foo": "bar"},
            role="role",
            username="username",
        )
        assert_matches_type(UserRead, me, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_update(self, client: FlowAISDK) -> None:
        response = client.api.v1.users.me.with_raw_response.update()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        me = response.parse()
        assert_matches_type(UserRead, me, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_update(self, client: FlowAISDK) -> None:
        with client.api.v1.users.me.with_streaming_response.update() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            me = response.parse()
            assert_matches_type(UserRead, me, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_get_basic_info(self, client: FlowAISDK) -> None:
        me = client.api.v1.users.me.get_basic_info()
        assert_matches_type(object, me, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_get_basic_info(self, client: FlowAISDK) -> None:
        response = client.api.v1.users.me.with_raw_response.get_basic_info()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        me = response.parse()
        assert_matches_type(object, me, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_get_basic_info(self, client: FlowAISDK) -> None:
        with client.api.v1.users.me.with_streaming_response.get_basic_info() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            me = response.parse()
            assert_matches_type(object, me, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncMe:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncFlowAISDK) -> None:
        me = await async_client.api.v1.users.me.retrieve()
        assert_matches_type(UserRead, me, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncFlowAISDK) -> None:
        response = await async_client.api.v1.users.me.with_raw_response.retrieve()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        me = await response.parse()
        assert_matches_type(UserRead, me, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncFlowAISDK) -> None:
        async with async_client.api.v1.users.me.with_streaming_response.retrieve() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            me = await response.parse()
            assert_matches_type(UserRead, me, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_update(self, async_client: AsyncFlowAISDK) -> None:
        me = await async_client.api.v1.users.me.update()
        assert_matches_type(UserRead, me, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncFlowAISDK) -> None:
        me = await async_client.api.v1.users.me.update(
            email="dev@stainless.com",
            first_name="first_name",
            image_url="image_url",
            is_active=True,
            last_name="last_name",
            preferences={"foo": "bar"},
            role="role",
            username="username",
        )
        assert_matches_type(UserRead, me, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_update(self, async_client: AsyncFlowAISDK) -> None:
        response = await async_client.api.v1.users.me.with_raw_response.update()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        me = await response.parse()
        assert_matches_type(UserRead, me, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncFlowAISDK) -> None:
        async with async_client.api.v1.users.me.with_streaming_response.update() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            me = await response.parse()
            assert_matches_type(UserRead, me, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_get_basic_info(self, async_client: AsyncFlowAISDK) -> None:
        me = await async_client.api.v1.users.me.get_basic_info()
        assert_matches_type(object, me, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_get_basic_info(self, async_client: AsyncFlowAISDK) -> None:
        response = await async_client.api.v1.users.me.with_raw_response.get_basic_info()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        me = await response.parse()
        assert_matches_type(object, me, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_get_basic_info(self, async_client: AsyncFlowAISDK) -> None:
        async with async_client.api.v1.users.me.with_streaming_response.get_basic_info() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            me = await response.parse()
            assert_matches_type(object, me, path=["response"])

        assert cast(Any, response.is_closed) is True
