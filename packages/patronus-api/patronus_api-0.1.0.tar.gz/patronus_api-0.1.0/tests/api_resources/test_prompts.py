# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from patronus_api import PatronusAPI, AsyncPatronusAPI
from patronus_api.types import (
    PromptListResponse,
    PromptCreateResponse,
    PromptCreateRevisionResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestPrompts:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: PatronusAPI) -> None:
        prompt = client.prompts.create(
            body="body",
            name="name",
        )
        assert_matches_type(PromptCreateResponse, prompt, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: PatronusAPI) -> None:
        prompt = client.prompts.create(
            body="body",
            name="name",
            description="description",
            labels=["string"],
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            project_name="project_name",
        )
        assert_matches_type(PromptCreateResponse, prompt, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: PatronusAPI) -> None:
        response = client.prompts.with_raw_response.create(
            body="body",
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        prompt = response.parse()
        assert_matches_type(PromptCreateResponse, prompt, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: PatronusAPI) -> None:
        with client.prompts.with_streaming_response.create(
            body="body",
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            prompt = response.parse()
            assert_matches_type(PromptCreateResponse, prompt, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_update(self, client: PatronusAPI) -> None:
        prompt = client.prompts.update(
            path_name="name",
        )
        assert_matches_type(object, prompt, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: PatronusAPI) -> None:
        prompt = client.prompts.update(
            path_name="name",
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            project_name="project_name",
            description="description",
            body_name="name",
        )
        assert_matches_type(object, prompt, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: PatronusAPI) -> None:
        response = client.prompts.with_raw_response.update(
            path_name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        prompt = response.parse()
        assert_matches_type(object, prompt, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: PatronusAPI) -> None:
        with client.prompts.with_streaming_response.update(
            path_name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            prompt = response.parse()
            assert_matches_type(object, prompt, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: PatronusAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `path_name` but received ''"):
            client.prompts.with_raw_response.update(
                path_name="",
            )

    @parametrize
    def test_method_list(self, client: PatronusAPI) -> None:
        prompt = client.prompts.list()
        assert_matches_type(PromptListResponse, prompt, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: PatronusAPI) -> None:
        prompt = client.prompts.list(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            label="label",
            name="name",
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            project_name="project_name",
            version=0,
        )
        assert_matches_type(PromptListResponse, prompt, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: PatronusAPI) -> None:
        response = client.prompts.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        prompt = response.parse()
        assert_matches_type(PromptListResponse, prompt, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: PatronusAPI) -> None:
        with client.prompts.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            prompt = response.parse()
            assert_matches_type(PromptListResponse, prompt, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: PatronusAPI) -> None:
        prompt = client.prompts.delete(
            name="name",
        )
        assert_matches_type(object, prompt, path=["response"])

    @parametrize
    def test_method_delete_with_all_params(self, client: PatronusAPI) -> None:
        prompt = client.prompts.delete(
            name="name",
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            project_name="project_name",
        )
        assert_matches_type(object, prompt, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: PatronusAPI) -> None:
        response = client.prompts.with_raw_response.delete(
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        prompt = response.parse()
        assert_matches_type(object, prompt, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: PatronusAPI) -> None:
        with client.prompts.with_streaming_response.delete(
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            prompt = response.parse()
            assert_matches_type(object, prompt, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: PatronusAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `name` but received ''"):
            client.prompts.with_raw_response.delete(
                name="",
            )

    @parametrize
    def test_method_create_revision(self, client: PatronusAPI) -> None:
        prompt = client.prompts.create_revision(
            name="name",
            body="body",
        )
        assert_matches_type(PromptCreateRevisionResponse, prompt, path=["response"])

    @parametrize
    def test_method_create_revision_with_all_params(self, client: PatronusAPI) -> None:
        prompt = client.prompts.create_revision(
            name="name",
            body="body",
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            project_name="project_name",
        )
        assert_matches_type(PromptCreateRevisionResponse, prompt, path=["response"])

    @parametrize
    def test_raw_response_create_revision(self, client: PatronusAPI) -> None:
        response = client.prompts.with_raw_response.create_revision(
            name="name",
            body="body",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        prompt = response.parse()
        assert_matches_type(PromptCreateRevisionResponse, prompt, path=["response"])

    @parametrize
    def test_streaming_response_create_revision(self, client: PatronusAPI) -> None:
        with client.prompts.with_streaming_response.create_revision(
            name="name",
            body="body",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            prompt = response.parse()
            assert_matches_type(PromptCreateRevisionResponse, prompt, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_create_revision(self, client: PatronusAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `name` but received ''"):
            client.prompts.with_raw_response.create_revision(
                name="",
                body="body",
            )

    @parametrize
    def test_method_set_labels(self, client: PatronusAPI) -> None:
        prompt = client.prompts.set_labels(
            name="name",
            labels=["string"],
            version=0,
        )
        assert prompt is None

    @parametrize
    def test_method_set_labels_with_all_params(self, client: PatronusAPI) -> None:
        prompt = client.prompts.set_labels(
            name="name",
            labels=["string"],
            version=0,
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            project_name="project_name",
        )
        assert prompt is None

    @parametrize
    def test_raw_response_set_labels(self, client: PatronusAPI) -> None:
        response = client.prompts.with_raw_response.set_labels(
            name="name",
            labels=["string"],
            version=0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        prompt = response.parse()
        assert prompt is None

    @parametrize
    def test_streaming_response_set_labels(self, client: PatronusAPI) -> None:
        with client.prompts.with_streaming_response.set_labels(
            name="name",
            labels=["string"],
            version=0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            prompt = response.parse()
            assert prompt is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_set_labels(self, client: PatronusAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `name` but received ''"):
            client.prompts.with_raw_response.set_labels(
                name="",
                labels=["string"],
                version=0,
            )


class TestAsyncPrompts:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncPatronusAPI) -> None:
        prompt = await async_client.prompts.create(
            body="body",
            name="name",
        )
        assert_matches_type(PromptCreateResponse, prompt, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncPatronusAPI) -> None:
        prompt = await async_client.prompts.create(
            body="body",
            name="name",
            description="description",
            labels=["string"],
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            project_name="project_name",
        )
        assert_matches_type(PromptCreateResponse, prompt, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncPatronusAPI) -> None:
        response = await async_client.prompts.with_raw_response.create(
            body="body",
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        prompt = await response.parse()
        assert_matches_type(PromptCreateResponse, prompt, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncPatronusAPI) -> None:
        async with async_client.prompts.with_streaming_response.create(
            body="body",
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            prompt = await response.parse()
            assert_matches_type(PromptCreateResponse, prompt, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_update(self, async_client: AsyncPatronusAPI) -> None:
        prompt = await async_client.prompts.update(
            path_name="name",
        )
        assert_matches_type(object, prompt, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncPatronusAPI) -> None:
        prompt = await async_client.prompts.update(
            path_name="name",
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            project_name="project_name",
            description="description",
            body_name="name",
        )
        assert_matches_type(object, prompt, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncPatronusAPI) -> None:
        response = await async_client.prompts.with_raw_response.update(
            path_name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        prompt = await response.parse()
        assert_matches_type(object, prompt, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncPatronusAPI) -> None:
        async with async_client.prompts.with_streaming_response.update(
            path_name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            prompt = await response.parse()
            assert_matches_type(object, prompt, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncPatronusAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `path_name` but received ''"):
            await async_client.prompts.with_raw_response.update(
                path_name="",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncPatronusAPI) -> None:
        prompt = await async_client.prompts.list()
        assert_matches_type(PromptListResponse, prompt, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncPatronusAPI) -> None:
        prompt = await async_client.prompts.list(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            label="label",
            name="name",
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            project_name="project_name",
            version=0,
        )
        assert_matches_type(PromptListResponse, prompt, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncPatronusAPI) -> None:
        response = await async_client.prompts.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        prompt = await response.parse()
        assert_matches_type(PromptListResponse, prompt, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncPatronusAPI) -> None:
        async with async_client.prompts.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            prompt = await response.parse()
            assert_matches_type(PromptListResponse, prompt, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncPatronusAPI) -> None:
        prompt = await async_client.prompts.delete(
            name="name",
        )
        assert_matches_type(object, prompt, path=["response"])

    @parametrize
    async def test_method_delete_with_all_params(self, async_client: AsyncPatronusAPI) -> None:
        prompt = await async_client.prompts.delete(
            name="name",
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            project_name="project_name",
        )
        assert_matches_type(object, prompt, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncPatronusAPI) -> None:
        response = await async_client.prompts.with_raw_response.delete(
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        prompt = await response.parse()
        assert_matches_type(object, prompt, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncPatronusAPI) -> None:
        async with async_client.prompts.with_streaming_response.delete(
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            prompt = await response.parse()
            assert_matches_type(object, prompt, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncPatronusAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `name` but received ''"):
            await async_client.prompts.with_raw_response.delete(
                name="",
            )

    @parametrize
    async def test_method_create_revision(self, async_client: AsyncPatronusAPI) -> None:
        prompt = await async_client.prompts.create_revision(
            name="name",
            body="body",
        )
        assert_matches_type(PromptCreateRevisionResponse, prompt, path=["response"])

    @parametrize
    async def test_method_create_revision_with_all_params(self, async_client: AsyncPatronusAPI) -> None:
        prompt = await async_client.prompts.create_revision(
            name="name",
            body="body",
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            project_name="project_name",
        )
        assert_matches_type(PromptCreateRevisionResponse, prompt, path=["response"])

    @parametrize
    async def test_raw_response_create_revision(self, async_client: AsyncPatronusAPI) -> None:
        response = await async_client.prompts.with_raw_response.create_revision(
            name="name",
            body="body",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        prompt = await response.parse()
        assert_matches_type(PromptCreateRevisionResponse, prompt, path=["response"])

    @parametrize
    async def test_streaming_response_create_revision(self, async_client: AsyncPatronusAPI) -> None:
        async with async_client.prompts.with_streaming_response.create_revision(
            name="name",
            body="body",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            prompt = await response.parse()
            assert_matches_type(PromptCreateRevisionResponse, prompt, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_create_revision(self, async_client: AsyncPatronusAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `name` but received ''"):
            await async_client.prompts.with_raw_response.create_revision(
                name="",
                body="body",
            )

    @parametrize
    async def test_method_set_labels(self, async_client: AsyncPatronusAPI) -> None:
        prompt = await async_client.prompts.set_labels(
            name="name",
            labels=["string"],
            version=0,
        )
        assert prompt is None

    @parametrize
    async def test_method_set_labels_with_all_params(self, async_client: AsyncPatronusAPI) -> None:
        prompt = await async_client.prompts.set_labels(
            name="name",
            labels=["string"],
            version=0,
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            project_name="project_name",
        )
        assert prompt is None

    @parametrize
    async def test_raw_response_set_labels(self, async_client: AsyncPatronusAPI) -> None:
        response = await async_client.prompts.with_raw_response.set_labels(
            name="name",
            labels=["string"],
            version=0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        prompt = await response.parse()
        assert prompt is None

    @parametrize
    async def test_streaming_response_set_labels(self, async_client: AsyncPatronusAPI) -> None:
        async with async_client.prompts.with_streaming_response.set_labels(
            name="name",
            labels=["string"],
            version=0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            prompt = await response.parse()
            assert prompt is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_set_labels(self, async_client: AsyncPatronusAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `name` but received ''"):
            await async_client.prompts.with_raw_response.set_labels(
                name="",
                labels=["string"],
                version=0,
            )
