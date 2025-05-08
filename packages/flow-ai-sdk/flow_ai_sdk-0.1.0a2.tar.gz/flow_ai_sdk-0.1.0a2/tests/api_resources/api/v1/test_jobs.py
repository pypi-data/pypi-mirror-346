# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from flow_ai_sdk import FlowAISDK, AsyncFlowAISDK
from tests.utils import assert_matches_type

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestJobs:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_cancel(self, client: FlowAISDK) -> None:
        job = client.api.v1.jobs.cancel(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(object, job, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_cancel(self, client: FlowAISDK) -> None:
        response = client.api.v1.jobs.with_raw_response.cancel(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        job = response.parse()
        assert_matches_type(object, job, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_cancel(self, client: FlowAISDK) -> None:
        with client.api.v1.jobs.with_streaming_response.cancel(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            job = response.parse()
            assert_matches_type(object, job, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_cancel(self, client: FlowAISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `job_id` but received ''"):
            client.api.v1.jobs.with_raw_response.cancel(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_generate_batch(self, client: FlowAISDK) -> None:
        job = client.api.v1.jobs.generate_batch(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(object, job, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_generate_batch(self, client: FlowAISDK) -> None:
        response = client.api.v1.jobs.with_raw_response.generate_batch(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        job = response.parse()
        assert_matches_type(object, job, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_generate_batch(self, client: FlowAISDK) -> None:
        with client.api.v1.jobs.with_streaming_response.generate_batch(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            job = response.parse()
            assert_matches_type(object, job, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_generate_batch(self, client: FlowAISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `job_id` but received ''"):
            client.api.v1.jobs.with_raw_response.generate_batch(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_generate_dataset(self, client: FlowAISDK) -> None:
        job = client.api.v1.jobs.generate_dataset(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(object, job, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_generate_dataset(self, client: FlowAISDK) -> None:
        response = client.api.v1.jobs.with_raw_response.generate_dataset(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        job = response.parse()
        assert_matches_type(object, job, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_generate_dataset(self, client: FlowAISDK) -> None:
        with client.api.v1.jobs.with_streaming_response.generate_dataset(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            job = response.parse()
            assert_matches_type(object, job, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_generate_dataset(self, client: FlowAISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `job_id` but received ''"):
            client.api.v1.jobs.with_raw_response.generate_dataset(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_get_details(self, client: FlowAISDK) -> None:
        job = client.api.v1.jobs.get_details(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(object, job, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_get_details(self, client: FlowAISDK) -> None:
        response = client.api.v1.jobs.with_raw_response.get_details(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        job = response.parse()
        assert_matches_type(object, job, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_get_details(self, client: FlowAISDK) -> None:
        with client.api.v1.jobs.with_streaming_response.get_details(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            job = response.parse()
            assert_matches_type(object, job, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_get_details(self, client: FlowAISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `job_id` but received ''"):
            client.api.v1.jobs.with_raw_response.get_details(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_list_batches(self, client: FlowAISDK) -> None:
        job = client.api.v1.jobs.list_batches(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(object, job, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list_batches(self, client: FlowAISDK) -> None:
        response = client.api.v1.jobs.with_raw_response.list_batches(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        job = response.parse()
        assert_matches_type(object, job, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list_batches(self, client: FlowAISDK) -> None:
        with client.api.v1.jobs.with_streaming_response.list_batches(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            job = response.parse()
            assert_matches_type(object, job, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_list_batches(self, client: FlowAISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `job_id` but received ''"):
            client.api.v1.jobs.with_raw_response.list_batches(
                "",
            )


class TestAsyncJobs:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_cancel(self, async_client: AsyncFlowAISDK) -> None:
        job = await async_client.api.v1.jobs.cancel(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(object, job, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_cancel(self, async_client: AsyncFlowAISDK) -> None:
        response = await async_client.api.v1.jobs.with_raw_response.cancel(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        job = await response.parse()
        assert_matches_type(object, job, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_cancel(self, async_client: AsyncFlowAISDK) -> None:
        async with async_client.api.v1.jobs.with_streaming_response.cancel(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            job = await response.parse()
            assert_matches_type(object, job, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_cancel(self, async_client: AsyncFlowAISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `job_id` but received ''"):
            await async_client.api.v1.jobs.with_raw_response.cancel(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_generate_batch(self, async_client: AsyncFlowAISDK) -> None:
        job = await async_client.api.v1.jobs.generate_batch(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(object, job, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_generate_batch(self, async_client: AsyncFlowAISDK) -> None:
        response = await async_client.api.v1.jobs.with_raw_response.generate_batch(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        job = await response.parse()
        assert_matches_type(object, job, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_generate_batch(self, async_client: AsyncFlowAISDK) -> None:
        async with async_client.api.v1.jobs.with_streaming_response.generate_batch(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            job = await response.parse()
            assert_matches_type(object, job, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_generate_batch(self, async_client: AsyncFlowAISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `job_id` but received ''"):
            await async_client.api.v1.jobs.with_raw_response.generate_batch(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_generate_dataset(self, async_client: AsyncFlowAISDK) -> None:
        job = await async_client.api.v1.jobs.generate_dataset(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(object, job, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_generate_dataset(self, async_client: AsyncFlowAISDK) -> None:
        response = await async_client.api.v1.jobs.with_raw_response.generate_dataset(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        job = await response.parse()
        assert_matches_type(object, job, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_generate_dataset(self, async_client: AsyncFlowAISDK) -> None:
        async with async_client.api.v1.jobs.with_streaming_response.generate_dataset(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            job = await response.parse()
            assert_matches_type(object, job, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_generate_dataset(self, async_client: AsyncFlowAISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `job_id` but received ''"):
            await async_client.api.v1.jobs.with_raw_response.generate_dataset(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_get_details(self, async_client: AsyncFlowAISDK) -> None:
        job = await async_client.api.v1.jobs.get_details(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(object, job, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_get_details(self, async_client: AsyncFlowAISDK) -> None:
        response = await async_client.api.v1.jobs.with_raw_response.get_details(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        job = await response.parse()
        assert_matches_type(object, job, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_get_details(self, async_client: AsyncFlowAISDK) -> None:
        async with async_client.api.v1.jobs.with_streaming_response.get_details(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            job = await response.parse()
            assert_matches_type(object, job, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_get_details(self, async_client: AsyncFlowAISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `job_id` but received ''"):
            await async_client.api.v1.jobs.with_raw_response.get_details(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_list_batches(self, async_client: AsyncFlowAISDK) -> None:
        job = await async_client.api.v1.jobs.list_batches(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(object, job, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list_batches(self, async_client: AsyncFlowAISDK) -> None:
        response = await async_client.api.v1.jobs.with_raw_response.list_batches(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        job = await response.parse()
        assert_matches_type(object, job, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list_batches(self, async_client: AsyncFlowAISDK) -> None:
        async with async_client.api.v1.jobs.with_streaming_response.list_batches(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            job = await response.parse()
            assert_matches_type(object, job, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_list_batches(self, async_client: AsyncFlowAISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `job_id` but received ''"):
            await async_client.api.v1.jobs.with_raw_response.list_batches(
                "",
            )
