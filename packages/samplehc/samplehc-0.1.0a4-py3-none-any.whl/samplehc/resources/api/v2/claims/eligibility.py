# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List

import httpx

from ....._types import NOT_GIVEN, Body, Query, Headers, NotGiven
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
from .....types.api.v2.claims import eligibility_check_params
from .....types.api.v2.claims.eligibility_check_response import EligibilityCheckResponse

__all__ = ["EligibilityResource", "AsyncEligibilityResource"]


class EligibilityResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> EligibilityResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/samplehc/samplehc-python#accessing-raw-response-data-eg-headers
        """
        return EligibilityResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> EligibilityResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/samplehc/samplehc-python#with_streaming_response
        """
        return EligibilityResourceWithStreamingResponse(self)

    def check(
        self,
        *,
        provider_identifier: str,
        provider_name: str,
        service_type_codes: List[str],
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
    ) -> EligibilityCheckResponse:
        """Args:
          provider_identifier: The provider identifier.

        This is usually your NPI.

          provider_name: The provider name.

          service_type_codes: The service type codes.

          subscriber_date_of_birth: The date of birth of the subscriber.

          subscriber_first_name: The first name of the subscriber.

          subscriber_last_name: The last name of the subscriber.

          subscriber_member_id: The member ID of the subscriber.

          trading_partner_service_id: The trading partner service ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/api/v2/claims/eligibility/check",
            body=maybe_transform(
                {
                    "provider_identifier": provider_identifier,
                    "provider_name": provider_name,
                    "service_type_codes": service_type_codes,
                    "subscriber_date_of_birth": subscriber_date_of_birth,
                    "subscriber_first_name": subscriber_first_name,
                    "subscriber_last_name": subscriber_last_name,
                    "subscriber_member_id": subscriber_member_id,
                    "trading_partner_service_id": trading_partner_service_id,
                },
                eligibility_check_params.EligibilityCheckParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EligibilityCheckResponse,
        )


class AsyncEligibilityResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncEligibilityResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/samplehc/samplehc-python#accessing-raw-response-data-eg-headers
        """
        return AsyncEligibilityResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncEligibilityResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/samplehc/samplehc-python#with_streaming_response
        """
        return AsyncEligibilityResourceWithStreamingResponse(self)

    async def check(
        self,
        *,
        provider_identifier: str,
        provider_name: str,
        service_type_codes: List[str],
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
    ) -> EligibilityCheckResponse:
        """Args:
          provider_identifier: The provider identifier.

        This is usually your NPI.

          provider_name: The provider name.

          service_type_codes: The service type codes.

          subscriber_date_of_birth: The date of birth of the subscriber.

          subscriber_first_name: The first name of the subscriber.

          subscriber_last_name: The last name of the subscriber.

          subscriber_member_id: The member ID of the subscriber.

          trading_partner_service_id: The trading partner service ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/api/v2/claims/eligibility/check",
            body=await async_maybe_transform(
                {
                    "provider_identifier": provider_identifier,
                    "provider_name": provider_name,
                    "service_type_codes": service_type_codes,
                    "subscriber_date_of_birth": subscriber_date_of_birth,
                    "subscriber_first_name": subscriber_first_name,
                    "subscriber_last_name": subscriber_last_name,
                    "subscriber_member_id": subscriber_member_id,
                    "trading_partner_service_id": trading_partner_service_id,
                },
                eligibility_check_params.EligibilityCheckParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EligibilityCheckResponse,
        )


class EligibilityResourceWithRawResponse:
    def __init__(self, eligibility: EligibilityResource) -> None:
        self._eligibility = eligibility

        self.check = to_raw_response_wrapper(
            eligibility.check,
        )


class AsyncEligibilityResourceWithRawResponse:
    def __init__(self, eligibility: AsyncEligibilityResource) -> None:
        self._eligibility = eligibility

        self.check = async_to_raw_response_wrapper(
            eligibility.check,
        )


class EligibilityResourceWithStreamingResponse:
    def __init__(self, eligibility: EligibilityResource) -> None:
        self._eligibility = eligibility

        self.check = to_streamed_response_wrapper(
            eligibility.check,
        )


class AsyncEligibilityResourceWithStreamingResponse:
    def __init__(self, eligibility: AsyncEligibilityResource) -> None:
        self._eligibility = eligibility

        self.check = async_to_streamed_response_wrapper(
            eligibility.check,
        )
