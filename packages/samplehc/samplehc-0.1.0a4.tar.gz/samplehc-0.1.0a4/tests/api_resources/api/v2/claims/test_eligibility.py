# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from samplehc import SampleHealthcare, AsyncSampleHealthcare
from tests.utils import assert_matches_type
from samplehc.types.api.v2.claims import EligibilityCheckResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestEligibility:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_check(self, client: SampleHealthcare) -> None:
        eligibility = client.api.v2.claims.eligibility.check(
            provider_identifier="providerIdentifier",
            provider_name="providerName",
            service_type_codes=["string"],
            subscriber_date_of_birth="subscriberDateOfBirth",
            subscriber_first_name="subscriberFirstName",
            subscriber_last_name="subscriberLastName",
            subscriber_member_id="subscriberMemberId",
            trading_partner_service_id="tradingPartnerServiceId",
        )
        assert_matches_type(EligibilityCheckResponse, eligibility, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_check(self, client: SampleHealthcare) -> None:
        response = client.api.v2.claims.eligibility.with_raw_response.check(
            provider_identifier="providerIdentifier",
            provider_name="providerName",
            service_type_codes=["string"],
            subscriber_date_of_birth="subscriberDateOfBirth",
            subscriber_first_name="subscriberFirstName",
            subscriber_last_name="subscriberLastName",
            subscriber_member_id="subscriberMemberId",
            trading_partner_service_id="tradingPartnerServiceId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        eligibility = response.parse()
        assert_matches_type(EligibilityCheckResponse, eligibility, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_check(self, client: SampleHealthcare) -> None:
        with client.api.v2.claims.eligibility.with_streaming_response.check(
            provider_identifier="providerIdentifier",
            provider_name="providerName",
            service_type_codes=["string"],
            subscriber_date_of_birth="subscriberDateOfBirth",
            subscriber_first_name="subscriberFirstName",
            subscriber_last_name="subscriberLastName",
            subscriber_member_id="subscriberMemberId",
            trading_partner_service_id="tradingPartnerServiceId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            eligibility = response.parse()
            assert_matches_type(EligibilityCheckResponse, eligibility, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncEligibility:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_check(self, async_client: AsyncSampleHealthcare) -> None:
        eligibility = await async_client.api.v2.claims.eligibility.check(
            provider_identifier="providerIdentifier",
            provider_name="providerName",
            service_type_codes=["string"],
            subscriber_date_of_birth="subscriberDateOfBirth",
            subscriber_first_name="subscriberFirstName",
            subscriber_last_name="subscriberLastName",
            subscriber_member_id="subscriberMemberId",
            trading_partner_service_id="tradingPartnerServiceId",
        )
        assert_matches_type(EligibilityCheckResponse, eligibility, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_check(self, async_client: AsyncSampleHealthcare) -> None:
        response = await async_client.api.v2.claims.eligibility.with_raw_response.check(
            provider_identifier="providerIdentifier",
            provider_name="providerName",
            service_type_codes=["string"],
            subscriber_date_of_birth="subscriberDateOfBirth",
            subscriber_first_name="subscriberFirstName",
            subscriber_last_name="subscriberLastName",
            subscriber_member_id="subscriberMemberId",
            trading_partner_service_id="tradingPartnerServiceId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        eligibility = await response.parse()
        assert_matches_type(EligibilityCheckResponse, eligibility, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_check(self, async_client: AsyncSampleHealthcare) -> None:
        async with async_client.api.v2.claims.eligibility.with_streaming_response.check(
            provider_identifier="providerIdentifier",
            provider_name="providerName",
            service_type_codes=["string"],
            subscriber_date_of_birth="subscriberDateOfBirth",
            subscriber_first_name="subscriberFirstName",
            subscriber_last_name="subscriberLastName",
            subscriber_member_id="subscriberMemberId",
            trading_partner_service_id="tradingPartnerServiceId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            eligibility = await response.parse()
            assert_matches_type(EligibilityCheckResponse, eligibility, path=["response"])

        assert cast(Any, response.is_closed) is True
