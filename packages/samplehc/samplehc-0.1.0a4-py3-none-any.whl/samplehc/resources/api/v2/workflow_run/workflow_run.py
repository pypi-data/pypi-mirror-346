# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from .step import (
    StepResource,
    AsyncStepResource,
    StepResourceWithRawResponse,
    AsyncStepResourceWithRawResponse,
    StepResourceWithStreamingResponse,
    AsyncStepResourceWithStreamingResponse,
)
from ....._types import NOT_GIVEN, Body, Query, Headers, NoneType, NotGiven
from ....._utils import maybe_transform, async_maybe_transform
from ....._compat import cached_property
from ....._resource import SyncAPIResource, AsyncAPIResource
from ....._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ....._base_client import make_request_options
from .....types.api.v2 import workflow_run_resume_when_complete_params

__all__ = ["WorkflowRunResource", "AsyncWorkflowRunResource"]


class WorkflowRunResource(SyncAPIResource):
    @cached_property
    def step(self) -> StepResource:
        return StepResource(self._client)

    @cached_property
    def with_raw_response(self) -> WorkflowRunResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/samplehc/samplehc-python#accessing-raw-response-data-eg-headers
        """
        return WorkflowRunResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> WorkflowRunResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/samplehc/samplehc-python#with_streaming_response
        """
        return WorkflowRunResourceWithStreamingResponse(self)

    def resume_when_complete(
        self,
        *,
        async_result_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            "/api/v2/workflow-run/resume-when-complete",
            body=maybe_transform(
                {"async_result_id": async_result_id},
                workflow_run_resume_when_complete_params.WorkflowRunResumeWhenCompleteParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class AsyncWorkflowRunResource(AsyncAPIResource):
    @cached_property
    def step(self) -> AsyncStepResource:
        return AsyncStepResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncWorkflowRunResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/samplehc/samplehc-python#accessing-raw-response-data-eg-headers
        """
        return AsyncWorkflowRunResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncWorkflowRunResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/samplehc/samplehc-python#with_streaming_response
        """
        return AsyncWorkflowRunResourceWithStreamingResponse(self)

    async def resume_when_complete(
        self,
        *,
        async_result_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            "/api/v2/workflow-run/resume-when-complete",
            body=await async_maybe_transform(
                {"async_result_id": async_result_id},
                workflow_run_resume_when_complete_params.WorkflowRunResumeWhenCompleteParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class WorkflowRunResourceWithRawResponse:
    def __init__(self, workflow_run: WorkflowRunResource) -> None:
        self._workflow_run = workflow_run

        self.resume_when_complete = to_raw_response_wrapper(
            workflow_run.resume_when_complete,
        )

    @cached_property
    def step(self) -> StepResourceWithRawResponse:
        return StepResourceWithRawResponse(self._workflow_run.step)


class AsyncWorkflowRunResourceWithRawResponse:
    def __init__(self, workflow_run: AsyncWorkflowRunResource) -> None:
        self._workflow_run = workflow_run

        self.resume_when_complete = async_to_raw_response_wrapper(
            workflow_run.resume_when_complete,
        )

    @cached_property
    def step(self) -> AsyncStepResourceWithRawResponse:
        return AsyncStepResourceWithRawResponse(self._workflow_run.step)


class WorkflowRunResourceWithStreamingResponse:
    def __init__(self, workflow_run: WorkflowRunResource) -> None:
        self._workflow_run = workflow_run

        self.resume_when_complete = to_streamed_response_wrapper(
            workflow_run.resume_when_complete,
        )

    @cached_property
    def step(self) -> StepResourceWithStreamingResponse:
        return StepResourceWithStreamingResponse(self._workflow_run.step)


class AsyncWorkflowRunResourceWithStreamingResponse:
    def __init__(self, workflow_run: AsyncWorkflowRunResource) -> None:
        self._workflow_run = workflow_run

        self.resume_when_complete = async_to_streamed_response_wrapper(
            workflow_run.resume_when_complete,
        )

    @cached_property
    def step(self) -> AsyncStepResourceWithStreamingResponse:
        return AsyncStepResourceWithStreamingResponse(self._workflow_run.step)
