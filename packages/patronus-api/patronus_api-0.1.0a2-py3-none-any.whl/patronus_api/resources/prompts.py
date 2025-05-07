# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Optional

import httpx

from ..types import (
    prompt_list_params,
    prompt_create_params,
    prompt_delete_params,
    prompt_update_params,
    prompt_set_labels_params,
    prompt_create_revision_params,
)
from .._types import NOT_GIVEN, Body, Query, Headers, NoneType, NotGiven
from .._utils import maybe_transform, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.prompt_list_response import PromptListResponse
from ..types.prompt_create_response import PromptCreateResponse
from ..types.prompt_create_revision_response import PromptCreateRevisionResponse

__all__ = ["PromptsResource", "AsyncPromptsResource"]


class PromptsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> PromptsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/patronus-ai/patronus-api-python#accessing-raw-response-data-eg-headers
        """
        return PromptsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> PromptsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/patronus-ai/patronus-api-python#with_streaming_response
        """
        return PromptsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        body: str,
        name: str,
        description: Optional[str] | NotGiven = NOT_GIVEN,
        labels: List[str] | NotGiven = NOT_GIVEN,
        project_id: Optional[str] | NotGiven = NOT_GIVEN,
        project_name: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PromptCreateResponse:
        """
        Create a new prompt.

        Creates the first version of a prompt in the specified project. Either
        project_id or project_name must be provided in the request. Prompts are
        versioned, with the first version starting at 1.

        To create additional versions of an existing prompt, use the Create Prompt
        Revision endpoint.

        Naming recommendations: For organizing related prompts (e.g., system, user
        prompts), we recommend following a convention:

        - `<name>/<role>[/<number>]`
        - Examples: `"my-agent/system/1"`, `"my-agent/system/2"`, `"my-agent/user"`

        For simple templating needs, we recommend using Python format strings:

        - Example: `"You're an agent that is a specialist in {subject} subject"`
        - Client usage: `prompt.body.format(subject="Astronomy")`

        Args:
          body: Content of the prompt

          name: Name for the prompt, must contain only alphanumeric characters, hyphens, and
              underscores

          description: Optional description of the prompt's purpose or usage

          labels: Optional labels to associate with this prompt version

          project_id: ID of the project to create the prompt in

          project_name: Name of the project to create the prompt in

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v1/prompts",
            body=maybe_transform(
                {
                    "body": body,
                    "name": name,
                    "description": description,
                    "labels": labels,
                    "project_id": project_id,
                    "project_name": project_name,
                },
                prompt_create_params.PromptCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PromptCreateResponse,
        )

    def update(
        self,
        path_name: str,
        *,
        project_id: Optional[str] | NotGiven = NOT_GIVEN,
        project_name: Optional[str] | NotGiven = NOT_GIVEN,
        description: Optional[str] | NotGiven = NOT_GIVEN,
        body_name: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """Update prompt metadata.

        Updates the name and/or description of a prompt.

        This affects all versions of
        the prompt. Either project_id or project_name must be provided to identify the
        project.

        Important: This endpoint does not update the prompt's body content. To create a
        new version with updated content, use the Create Prompt Revision endpoint.

        Args:
          path_name: Name of the prompt to update

          project_id: Project ID containing the prompt

          project_name: Project name containing the prompt

          description: New description for the prompt

          body_name: New name for the prompt, must contain only alphanumeric characters, hyphens, and
              underscores

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not path_name:
            raise ValueError(f"Expected a non-empty value for `path_name` but received {path_name!r}")
        return self._patch(
            f"/v1/prompts/{path_name}",
            body=maybe_transform(
                {
                    "description": description,
                    "body_name": body_name,
                },
                prompt_update_params.PromptUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "project_id": project_id,
                        "project_name": project_name,
                    },
                    prompt_update_params.PromptUpdateParams,
                ),
            ),
            cast_to=object,
        )

    def list(
        self,
        *,
        id: Optional[str] | NotGiven = NOT_GIVEN,
        label: Optional[str] | NotGiven = NOT_GIVEN,
        name: Optional[str] | NotGiven = NOT_GIVEN,
        project_id: Optional[str] | NotGiven = NOT_GIVEN,
        project_name: Optional[str] | NotGiven = NOT_GIVEN,
        version: Optional[int] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PromptListResponse:
        """
        List prompts with optional filtering.

        Returns a list of prompt versions that match the provided filter criteria.
        Either project_id or project_name must be provided, but not both. Results can be
        further filtered by name, id, version, or label.

        Args:
          id: Filter prompts by specific UUID

          label: Filter prompts by label

          name: Filter prompts by name

          project_id: Filter prompts by project ID

          project_name: Filter prompts by project name

          version: Filter prompts by version number

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/v1/prompts",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "id": id,
                        "label": label,
                        "name": name,
                        "project_id": project_id,
                        "project_name": project_name,
                        "version": version,
                    },
                    prompt_list_params.PromptListParams,
                ),
            ),
            cast_to=PromptListResponse,
        )

    def delete(
        self,
        name: str,
        *,
        project_id: Optional[str] | NotGiven = NOT_GIVEN,
        project_name: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """
        Delete Prompt

        Args:
          name: Name of the prompt to create a revision for

          project_id: Project ID containing the prompt

          project_name: Project name containing the prompt

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not name:
            raise ValueError(f"Expected a non-empty value for `name` but received {name!r}")
        return self._delete(
            f"/v1/prompts/{name}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "project_id": project_id,
                        "project_name": project_name,
                    },
                    prompt_delete_params.PromptDeleteParams,
                ),
            ),
            cast_to=object,
        )

    def create_revision(
        self,
        name: str,
        *,
        body: str,
        project_id: Optional[str] | NotGiven = NOT_GIVEN,
        project_name: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PromptCreateRevisionResponse:
        """
        Create a new revision of an existing prompt.

        Creates a new version of the prompt with an updated body. The version number is
        automatically incremented. Either project_id or project_name must be provided to
        identify the project.

        Use this endpoint to update the content of an existing prompt rather than
        creating a new prompt with the Create Prompt endpoint.

        Args:
          name: Name of the prompt to create a revision for

          body: New content for the prompt revision

          project_id: Project ID containing the prompt

          project_name: Project name containing the prompt

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not name:
            raise ValueError(f"Expected a non-empty value for `name` but received {name!r}")
        return self._post(
            f"/v1/prompts/{name}/revision",
            body=maybe_transform({"body": body}, prompt_create_revision_params.PromptCreateRevisionParams),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "project_id": project_id,
                        "project_name": project_name,
                    },
                    prompt_create_revision_params.PromptCreateRevisionParams,
                ),
            ),
            cast_to=PromptCreateRevisionResponse,
        )

    def set_labels(
        self,
        name: str,
        *,
        labels: List[str],
        version: int,
        project_id: Optional[str] | NotGiven = NOT_GIVEN,
        project_name: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Set Labels

        Args:
          name: Name of the prompt to create a revision for

          labels: List of labels to set on the prompt version

          version: The version number of the prompt to set labels on

          project_id: Project ID containing the prompt

          project_name: Project name containing the prompt

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not name:
            raise ValueError(f"Expected a non-empty value for `name` but received {name!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            f"/v1/prompts/{name}/set-labels",
            body=maybe_transform(
                {
                    "labels": labels,
                    "version": version,
                },
                prompt_set_labels_params.PromptSetLabelsParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "project_id": project_id,
                        "project_name": project_name,
                    },
                    prompt_set_labels_params.PromptSetLabelsParams,
                ),
            ),
            cast_to=NoneType,
        )


class AsyncPromptsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncPromptsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/patronus-ai/patronus-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncPromptsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncPromptsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/patronus-ai/patronus-api-python#with_streaming_response
        """
        return AsyncPromptsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        body: str,
        name: str,
        description: Optional[str] | NotGiven = NOT_GIVEN,
        labels: List[str] | NotGiven = NOT_GIVEN,
        project_id: Optional[str] | NotGiven = NOT_GIVEN,
        project_name: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PromptCreateResponse:
        """
        Create a new prompt.

        Creates the first version of a prompt in the specified project. Either
        project_id or project_name must be provided in the request. Prompts are
        versioned, with the first version starting at 1.

        To create additional versions of an existing prompt, use the Create Prompt
        Revision endpoint.

        Naming recommendations: For organizing related prompts (e.g., system, user
        prompts), we recommend following a convention:

        - `<name>/<role>[/<number>]`
        - Examples: `"my-agent/system/1"`, `"my-agent/system/2"`, `"my-agent/user"`

        For simple templating needs, we recommend using Python format strings:

        - Example: `"You're an agent that is a specialist in {subject} subject"`
        - Client usage: `prompt.body.format(subject="Astronomy")`

        Args:
          body: Content of the prompt

          name: Name for the prompt, must contain only alphanumeric characters, hyphens, and
              underscores

          description: Optional description of the prompt's purpose or usage

          labels: Optional labels to associate with this prompt version

          project_id: ID of the project to create the prompt in

          project_name: Name of the project to create the prompt in

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v1/prompts",
            body=await async_maybe_transform(
                {
                    "body": body,
                    "name": name,
                    "description": description,
                    "labels": labels,
                    "project_id": project_id,
                    "project_name": project_name,
                },
                prompt_create_params.PromptCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PromptCreateResponse,
        )

    async def update(
        self,
        path_name: str,
        *,
        project_id: Optional[str] | NotGiven = NOT_GIVEN,
        project_name: Optional[str] | NotGiven = NOT_GIVEN,
        description: Optional[str] | NotGiven = NOT_GIVEN,
        body_name: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """Update prompt metadata.

        Updates the name and/or description of a prompt.

        This affects all versions of
        the prompt. Either project_id or project_name must be provided to identify the
        project.

        Important: This endpoint does not update the prompt's body content. To create a
        new version with updated content, use the Create Prompt Revision endpoint.

        Args:
          path_name: Name of the prompt to update

          project_id: Project ID containing the prompt

          project_name: Project name containing the prompt

          description: New description for the prompt

          body_name: New name for the prompt, must contain only alphanumeric characters, hyphens, and
              underscores

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not path_name:
            raise ValueError(f"Expected a non-empty value for `path_name` but received {path_name!r}")
        return await self._patch(
            f"/v1/prompts/{path_name}",
            body=await async_maybe_transform(
                {
                    "description": description,
                    "body_name": body_name,
                },
                prompt_update_params.PromptUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "project_id": project_id,
                        "project_name": project_name,
                    },
                    prompt_update_params.PromptUpdateParams,
                ),
            ),
            cast_to=object,
        )

    async def list(
        self,
        *,
        id: Optional[str] | NotGiven = NOT_GIVEN,
        label: Optional[str] | NotGiven = NOT_GIVEN,
        name: Optional[str] | NotGiven = NOT_GIVEN,
        project_id: Optional[str] | NotGiven = NOT_GIVEN,
        project_name: Optional[str] | NotGiven = NOT_GIVEN,
        version: Optional[int] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PromptListResponse:
        """
        List prompts with optional filtering.

        Returns a list of prompt versions that match the provided filter criteria.
        Either project_id or project_name must be provided, but not both. Results can be
        further filtered by name, id, version, or label.

        Args:
          id: Filter prompts by specific UUID

          label: Filter prompts by label

          name: Filter prompts by name

          project_id: Filter prompts by project ID

          project_name: Filter prompts by project name

          version: Filter prompts by version number

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/v1/prompts",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "id": id,
                        "label": label,
                        "name": name,
                        "project_id": project_id,
                        "project_name": project_name,
                        "version": version,
                    },
                    prompt_list_params.PromptListParams,
                ),
            ),
            cast_to=PromptListResponse,
        )

    async def delete(
        self,
        name: str,
        *,
        project_id: Optional[str] | NotGiven = NOT_GIVEN,
        project_name: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """
        Delete Prompt

        Args:
          name: Name of the prompt to create a revision for

          project_id: Project ID containing the prompt

          project_name: Project name containing the prompt

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not name:
            raise ValueError(f"Expected a non-empty value for `name` but received {name!r}")
        return await self._delete(
            f"/v1/prompts/{name}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "project_id": project_id,
                        "project_name": project_name,
                    },
                    prompt_delete_params.PromptDeleteParams,
                ),
            ),
            cast_to=object,
        )

    async def create_revision(
        self,
        name: str,
        *,
        body: str,
        project_id: Optional[str] | NotGiven = NOT_GIVEN,
        project_name: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PromptCreateRevisionResponse:
        """
        Create a new revision of an existing prompt.

        Creates a new version of the prompt with an updated body. The version number is
        automatically incremented. Either project_id or project_name must be provided to
        identify the project.

        Use this endpoint to update the content of an existing prompt rather than
        creating a new prompt with the Create Prompt endpoint.

        Args:
          name: Name of the prompt to create a revision for

          body: New content for the prompt revision

          project_id: Project ID containing the prompt

          project_name: Project name containing the prompt

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not name:
            raise ValueError(f"Expected a non-empty value for `name` but received {name!r}")
        return await self._post(
            f"/v1/prompts/{name}/revision",
            body=await async_maybe_transform({"body": body}, prompt_create_revision_params.PromptCreateRevisionParams),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "project_id": project_id,
                        "project_name": project_name,
                    },
                    prompt_create_revision_params.PromptCreateRevisionParams,
                ),
            ),
            cast_to=PromptCreateRevisionResponse,
        )

    async def set_labels(
        self,
        name: str,
        *,
        labels: List[str],
        version: int,
        project_id: Optional[str] | NotGiven = NOT_GIVEN,
        project_name: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Set Labels

        Args:
          name: Name of the prompt to create a revision for

          labels: List of labels to set on the prompt version

          version: The version number of the prompt to set labels on

          project_id: Project ID containing the prompt

          project_name: Project name containing the prompt

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not name:
            raise ValueError(f"Expected a non-empty value for `name` but received {name!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            f"/v1/prompts/{name}/set-labels",
            body=await async_maybe_transform(
                {
                    "labels": labels,
                    "version": version,
                },
                prompt_set_labels_params.PromptSetLabelsParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "project_id": project_id,
                        "project_name": project_name,
                    },
                    prompt_set_labels_params.PromptSetLabelsParams,
                ),
            ),
            cast_to=NoneType,
        )


class PromptsResourceWithRawResponse:
    def __init__(self, prompts: PromptsResource) -> None:
        self._prompts = prompts

        self.create = to_raw_response_wrapper(
            prompts.create,
        )
        self.update = to_raw_response_wrapper(
            prompts.update,
        )
        self.list = to_raw_response_wrapper(
            prompts.list,
        )
        self.delete = to_raw_response_wrapper(
            prompts.delete,
        )
        self.create_revision = to_raw_response_wrapper(
            prompts.create_revision,
        )
        self.set_labels = to_raw_response_wrapper(
            prompts.set_labels,
        )


class AsyncPromptsResourceWithRawResponse:
    def __init__(self, prompts: AsyncPromptsResource) -> None:
        self._prompts = prompts

        self.create = async_to_raw_response_wrapper(
            prompts.create,
        )
        self.update = async_to_raw_response_wrapper(
            prompts.update,
        )
        self.list = async_to_raw_response_wrapper(
            prompts.list,
        )
        self.delete = async_to_raw_response_wrapper(
            prompts.delete,
        )
        self.create_revision = async_to_raw_response_wrapper(
            prompts.create_revision,
        )
        self.set_labels = async_to_raw_response_wrapper(
            prompts.set_labels,
        )


class PromptsResourceWithStreamingResponse:
    def __init__(self, prompts: PromptsResource) -> None:
        self._prompts = prompts

        self.create = to_streamed_response_wrapper(
            prompts.create,
        )
        self.update = to_streamed_response_wrapper(
            prompts.update,
        )
        self.list = to_streamed_response_wrapper(
            prompts.list,
        )
        self.delete = to_streamed_response_wrapper(
            prompts.delete,
        )
        self.create_revision = to_streamed_response_wrapper(
            prompts.create_revision,
        )
        self.set_labels = to_streamed_response_wrapper(
            prompts.set_labels,
        )


class AsyncPromptsResourceWithStreamingResponse:
    def __init__(self, prompts: AsyncPromptsResource) -> None:
        self._prompts = prompts

        self.create = async_to_streamed_response_wrapper(
            prompts.create,
        )
        self.update = async_to_streamed_response_wrapper(
            prompts.update,
        )
        self.list = async_to_streamed_response_wrapper(
            prompts.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            prompts.delete,
        )
        self.create_revision = async_to_streamed_response_wrapper(
            prompts.create_revision,
        )
        self.set_labels = async_to_streamed_response_wrapper(
            prompts.set_labels,
        )
