# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ....._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ....._utils import maybe_transform, async_maybe_transform
from ....._compat import cached_property
from .eligibility import (
    EligibilityResource,
    AsyncEligibilityResource,
    EligibilityResourceWithRawResponse,
    AsyncEligibilityResourceWithRawResponse,
    EligibilityResourceWithStreamingResponse,
    AsyncEligibilityResourceWithStreamingResponse,
)
from ....._resource import SyncAPIResource, AsyncAPIResource
from ....._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ....._base_client import make_request_options
from .....types.api.v2 import claim_submit_params, claim_coordinate_benefits_params
from .....types.api.v2.claim_submit_response import ClaimSubmitResponse

__all__ = ["ClaimsResource", "AsyncClaimsResource"]


class ClaimsResource(SyncAPIResource):
    @cached_property
    def eligibility(self) -> EligibilityResource:
        return EligibilityResource(self._client)

    @cached_property
    def with_raw_response(self) -> ClaimsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/samplehc/samplehc-python#accessing-raw-response-data-eg-headers
        """
        return ClaimsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ClaimsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/samplehc/samplehc-python#with_streaming_response
        """
        return ClaimsResourceWithStreamingResponse(self)

    def coordinate_benefits(
        self,
        *,
        dependent_date_of_birth: str,
        dependent_first_name: str,
        dependent_last_name: str,
        encounter_date_of_service: str,
        encounter_service_type_code: str,
        provider_name: str,
        provider_npi: str,
        subscriber_date_of_birth: str,
        subscriber_first_name: str,
        subscriber_last_name: str,
        subscriber_member_id: str,
        trading_partner_service_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """
        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/api/v2/claims/coordination-of-benefits",
            body=maybe_transform(
                {
                    "dependent_date_of_birth": dependent_date_of_birth,
                    "dependent_first_name": dependent_first_name,
                    "dependent_last_name": dependent_last_name,
                    "encounter_date_of_service": encounter_date_of_service,
                    "encounter_service_type_code": encounter_service_type_code,
                    "provider_name": provider_name,
                    "provider_npi": provider_npi,
                    "subscriber_date_of_birth": subscriber_date_of_birth,
                    "subscriber_first_name": subscriber_first_name,
                    "subscriber_last_name": subscriber_last_name,
                    "subscriber_member_id": subscriber_member_id,
                    "trading_partner_service_id": trading_partner_service_id,
                },
                claim_coordinate_benefits_params.ClaimCoordinateBenefitsParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    def submit(
        self,
        *,
        input: claim_submit_params.Input,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ClaimSubmitResponse:
        """
        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/api/v2/claims/submission",
            body=maybe_transform({"input": input}, claim_submit_params.ClaimSubmitParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ClaimSubmitResponse,
        )


class AsyncClaimsResource(AsyncAPIResource):
    @cached_property
    def eligibility(self) -> AsyncEligibilityResource:
        return AsyncEligibilityResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncClaimsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/samplehc/samplehc-python#accessing-raw-response-data-eg-headers
        """
        return AsyncClaimsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncClaimsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/samplehc/samplehc-python#with_streaming_response
        """
        return AsyncClaimsResourceWithStreamingResponse(self)

    async def coordinate_benefits(
        self,
        *,
        dependent_date_of_birth: str,
        dependent_first_name: str,
        dependent_last_name: str,
        encounter_date_of_service: str,
        encounter_service_type_code: str,
        provider_name: str,
        provider_npi: str,
        subscriber_date_of_birth: str,
        subscriber_first_name: str,
        subscriber_last_name: str,
        subscriber_member_id: str,
        trading_partner_service_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """
        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/api/v2/claims/coordination-of-benefits",
            body=await async_maybe_transform(
                {
                    "dependent_date_of_birth": dependent_date_of_birth,
                    "dependent_first_name": dependent_first_name,
                    "dependent_last_name": dependent_last_name,
                    "encounter_date_of_service": encounter_date_of_service,
                    "encounter_service_type_code": encounter_service_type_code,
                    "provider_name": provider_name,
                    "provider_npi": provider_npi,
                    "subscriber_date_of_birth": subscriber_date_of_birth,
                    "subscriber_first_name": subscriber_first_name,
                    "subscriber_last_name": subscriber_last_name,
                    "subscriber_member_id": subscriber_member_id,
                    "trading_partner_service_id": trading_partner_service_id,
                },
                claim_coordinate_benefits_params.ClaimCoordinateBenefitsParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    async def submit(
        self,
        *,
        input: claim_submit_params.Input,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ClaimSubmitResponse:
        """
        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/api/v2/claims/submission",
            body=await async_maybe_transform({"input": input}, claim_submit_params.ClaimSubmitParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ClaimSubmitResponse,
        )


class ClaimsResourceWithRawResponse:
    def __init__(self, claims: ClaimsResource) -> None:
        self._claims = claims

        self.coordinate_benefits = to_raw_response_wrapper(
            claims.coordinate_benefits,
        )
        self.submit = to_raw_response_wrapper(
            claims.submit,
        )

    @cached_property
    def eligibility(self) -> EligibilityResourceWithRawResponse:
        return EligibilityResourceWithRawResponse(self._claims.eligibility)


class AsyncClaimsResourceWithRawResponse:
    def __init__(self, claims: AsyncClaimsResource) -> None:
        self._claims = claims

        self.coordinate_benefits = async_to_raw_response_wrapper(
            claims.coordinate_benefits,
        )
        self.submit = async_to_raw_response_wrapper(
            claims.submit,
        )

    @cached_property
    def eligibility(self) -> AsyncEligibilityResourceWithRawResponse:
        return AsyncEligibilityResourceWithRawResponse(self._claims.eligibility)


class ClaimsResourceWithStreamingResponse:
    def __init__(self, claims: ClaimsResource) -> None:
        self._claims = claims

        self.coordinate_benefits = to_streamed_response_wrapper(
            claims.coordinate_benefits,
        )
        self.submit = to_streamed_response_wrapper(
            claims.submit,
        )

    @cached_property
    def eligibility(self) -> EligibilityResourceWithStreamingResponse:
        return EligibilityResourceWithStreamingResponse(self._claims.eligibility)


class AsyncClaimsResourceWithStreamingResponse:
    def __init__(self, claims: AsyncClaimsResource) -> None:
        self._claims = claims

        self.coordinate_benefits = async_to_streamed_response_wrapper(
            claims.coordinate_benefits,
        )
        self.submit = async_to_streamed_response_wrapper(
            claims.submit,
        )

    @cached_property
    def eligibility(self) -> AsyncEligibilityResourceWithStreamingResponse:
        return AsyncEligibilityResourceWithStreamingResponse(self._claims.eligibility)
