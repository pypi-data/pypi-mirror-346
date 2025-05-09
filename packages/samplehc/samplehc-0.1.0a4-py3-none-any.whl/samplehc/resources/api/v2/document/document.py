# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Iterable
from typing_extensions import Literal

import httpx

from .legacy import (
    LegacyResource,
    AsyncLegacyResource,
    LegacyResourceWithRawResponse,
    AsyncLegacyResourceWithRawResponse,
    LegacyResourceWithStreamingResponse,
    AsyncLegacyResourceWithStreamingResponse,
)
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
from .....types.api.v2 import (
    document_split_params,
    document_search_params,
    document_extract_params,
    document_classify_params,
    document_generate_params,
    document_extraction_params,
    document_generate_csv_params,
    document_create_from_splits_params,
    document_get_presigned_upload_url_params,
)
from .....types.api.v2.document_split_response import DocumentSplitResponse
from .....types.api.v2.document_search_response import DocumentSearchResponse
from .....types.api.v2.document_extract_response import DocumentExtractResponse
from .....types.api.v2.document_classify_response import DocumentClassifyResponse
from .....types.api.v2.document_generate_response import DocumentGenerateResponse
from .....types.api.v2.document_retrieve_response import DocumentRetrieveResponse
from .....types.api.v2.document_extraction_response import DocumentExtractionResponse
from .....types.api.v2.document_generate_csv_response import DocumentGenerateCsvResponse
from .....types.api.v2.document_get_metadata_response import DocumentGetMetadataResponse
from .....types.api.v2.document_get_csv_content_response import DocumentGetCsvContentResponse
from .....types.api.v2.document_create_from_splits_response import DocumentCreateFromSplitsResponse
from .....types.api.v2.document_get_presigned_upload_url_response import DocumentGetPresignedUploadURLResponse

__all__ = ["DocumentResource", "AsyncDocumentResource"]


class DocumentResource(SyncAPIResource):
    @cached_property
    def legacy(self) -> LegacyResource:
        return LegacyResource(self._client)

    @cached_property
    def with_raw_response(self) -> DocumentResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/samplehc/samplehc-python#accessing-raw-response-data-eg-headers
        """
        return DocumentResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> DocumentResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/samplehc/samplehc-python#with_streaming_response
        """
        return DocumentResourceWithStreamingResponse(self)

    def retrieve(
        self,
        document_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DocumentRetrieveResponse:
        """
        Retrieves full document details including OCR response for PDFs

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not document_id:
            raise ValueError(f"Expected a non-empty value for `document_id` but received {document_id!r}")
        return self._get(
            f"/api/v2/document/{document_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DocumentRetrieveResponse,
        )

    def classify(
        self,
        *,
        document: document_classify_params.Document,
        label_schemas: Iterable[document_classify_params.LabelSchema],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DocumentClassifyResponse:
        """
        Initiates an asynchronous document classification task against provided label
        schemas

        Args:
          document: The document to be classified.

          label_schemas: An array of label schemas to classify against.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/api/v2/document/classify",
            body=maybe_transform(
                {
                    "document": document,
                    "label_schemas": label_schemas,
                },
                document_classify_params.DocumentClassifyParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DocumentClassifyResponse,
        )

    def create_from_splits(
        self,
        *,
        document: document_create_from_splits_params.Document,
        splits: Iterable[float],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DocumentCreateFromSplitsResponse:
        """
        Creates new documents from specified split points in an existing document

        Args:
          document: The original document from which splits are being created.

          splits: An array of page numbers (1-indexed) where the document should be split. Each
              number indicates the end of a new document segment.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/api/v2/document/create-from-splits",
            body=maybe_transform(
                {
                    "document": document,
                    "splits": splits,
                },
                document_create_from_splits_params.DocumentCreateFromSplitsParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DocumentCreateFromSplitsResponse,
        )

    def extract(
        self,
        *,
        documents: Iterable[document_extract_params.Document],
        prompt: str,
        response_json_schema: Dict[str, object],
        reasoning_effort: Literal["low", "medium", "high"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DocumentExtractResponse:
        """
        Initiates an asynchronous extraction task using a JSON schema and prompt to
        guide the extraction

        Args:
          documents: An array of documents from which to extract information.

          prompt: The prompt guiding the extraction process.

          response_json_schema: A JSON schema defining the structure of the desired extraction response.

          reasoning_effort: The level of reasoning effort to apply for the extraction. Defaults to medium if
              not specified.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/api/v2/document/extract",
            body=maybe_transform(
                {
                    "documents": documents,
                    "prompt": prompt,
                    "response_json_schema": response_json_schema,
                    "reasoning_effort": reasoning_effort,
                },
                document_extract_params.DocumentExtractParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DocumentExtractResponse,
        )

    def extraction(
        self,
        *,
        answer_schemas: Iterable[document_extraction_params.AnswerSchema],
        documents: Iterable[document_extraction_params.Document],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DocumentExtractionResponse:
        """
        Initiates an asynchronous legacy extraction task to extract information from
        documents based on answer schemas

        Args:
          answer_schemas: An array of answer schemas defining the information to extract.

          documents: An array of documents from which to extract information.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/api/v2/document/extraction",
            body=maybe_transform(
                {
                    "answer_schemas": answer_schemas,
                    "documents": documents,
                },
                document_extraction_params.DocumentExtractionParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DocumentExtractionResponse,
        )

    def generate(
        self,
        *,
        slug: str,
        type: Literal["pdf", "report"],
        variables: Dict[str, str],
        file_name: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DocumentGenerateResponse:
        """
        Initiates an asynchronous task to generate a document from a template (PDF or
        report) with provided variables

        Args:
          slug: The slug of the template (either PDF or report) to use for generation.

          type: The type of document to generate: 'pdf' for PDF templates, 'report' for report
              templates.

          variables: An object where keys are variable names and values are their corresponding
              string values to be injected into the template.

          file_name: Optional desired file name for the generated document.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/api/v2/document/generate",
            body=maybe_transform(
                {
                    "slug": slug,
                    "type": type,
                    "variables": variables,
                    "file_name": file_name,
                },
                document_generate_params.DocumentGenerateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DocumentGenerateResponse,
        )

    def generate_csv(
        self,
        *,
        file_name: str,
        rows: Iterable[Dict[str, Union[str, float]]],
        options: document_generate_csv_params.Options | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DocumentGenerateCsvResponse:
        """
        Generates a new CSV document from provided data rows

        Args:
          file_name: The desired file name for the generated CSV.

          rows: An array of objects, where each object represents a row in the CSV. Keys are
              column headers and values are cell content.

          options: Optional settings for CSV generation.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/api/v2/document/generate-csv",
            body=maybe_transform(
                {
                    "file_name": file_name,
                    "rows": rows,
                    "options": options,
                },
                document_generate_csv_params.DocumentGenerateCsvParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DocumentGenerateCsvResponse,
        )

    def get_csv_content(
        self,
        document_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DocumentGetCsvContentResponse:
        """
        Retrieves the parsed content of a CSV document as structured data

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not document_id:
            raise ValueError(f"Expected a non-empty value for `document_id` but received {document_id!r}")
        return self._get(
            f"/api/v2/document/{document_id}/csv-content",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DocumentGetCsvContentResponse,
        )

    def get_metadata(
        self,
        document_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DocumentGetMetadataResponse:
        """
        Retrieves metadata and a presigned URL for a specific document

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not document_id:
            raise ValueError(f"Expected a non-empty value for `document_id` but received {document_id!r}")
        return self._get(
            f"/api/v2/document/{document_id}/metadata",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DocumentGetMetadataResponse,
        )

    def get_presigned_upload_url(
        self,
        *,
        file_name: str,
        mime_type: Literal[
            "application/zip",
            "application/x-zip-compressed",
            "multipart/x-zip",
            "application/x-compress",
            "application/pdf",
            "text/csv",
            "application/javascript",
            "text/css",
            "image/png",
            "video/mp4",
            "application/msword",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DocumentGetPresignedUploadURLResponse:
        """
        Generates a presigned URL for uploading a new document

        Args:
          file_name: The name of the file to be uploaded.

          mime_type: The MIME type of the file to be uploaded.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/api/v2/document/presigned-upload-url",
            body=maybe_transform(
                {
                    "file_name": file_name,
                    "mime_type": mime_type,
                },
                document_get_presigned_upload_url_params.DocumentGetPresignedUploadURLParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DocumentGetPresignedUploadURLResponse,
        )

    def search(
        self,
        *,
        documents: Iterable[document_search_params.Document],
        query: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DocumentSearchResponse:
        """
        Searches through specified documents for content matching the query

        Args:
          documents: An array of documents to search within.

          query: The search query string.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/api/v2/document/search",
            body=maybe_transform(
                {
                    "documents": documents,
                    "query": query,
                },
                document_search_params.DocumentSearchParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DocumentSearchResponse,
        )

    def split(
        self,
        *,
        document: document_split_params.Document,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DocumentSplitResponse:
        """
        Initiates an asynchronous task to split a document into multiple parts

        Args:
          document: The document to be split.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/api/v2/document/split",
            body=maybe_transform({"document": document}, document_split_params.DocumentSplitParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DocumentSplitResponse,
        )


class AsyncDocumentResource(AsyncAPIResource):
    @cached_property
    def legacy(self) -> AsyncLegacyResource:
        return AsyncLegacyResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncDocumentResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/samplehc/samplehc-python#accessing-raw-response-data-eg-headers
        """
        return AsyncDocumentResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncDocumentResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/samplehc/samplehc-python#with_streaming_response
        """
        return AsyncDocumentResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        document_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DocumentRetrieveResponse:
        """
        Retrieves full document details including OCR response for PDFs

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not document_id:
            raise ValueError(f"Expected a non-empty value for `document_id` but received {document_id!r}")
        return await self._get(
            f"/api/v2/document/{document_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DocumentRetrieveResponse,
        )

    async def classify(
        self,
        *,
        document: document_classify_params.Document,
        label_schemas: Iterable[document_classify_params.LabelSchema],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DocumentClassifyResponse:
        """
        Initiates an asynchronous document classification task against provided label
        schemas

        Args:
          document: The document to be classified.

          label_schemas: An array of label schemas to classify against.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/api/v2/document/classify",
            body=await async_maybe_transform(
                {
                    "document": document,
                    "label_schemas": label_schemas,
                },
                document_classify_params.DocumentClassifyParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DocumentClassifyResponse,
        )

    async def create_from_splits(
        self,
        *,
        document: document_create_from_splits_params.Document,
        splits: Iterable[float],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DocumentCreateFromSplitsResponse:
        """
        Creates new documents from specified split points in an existing document

        Args:
          document: The original document from which splits are being created.

          splits: An array of page numbers (1-indexed) where the document should be split. Each
              number indicates the end of a new document segment.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/api/v2/document/create-from-splits",
            body=await async_maybe_transform(
                {
                    "document": document,
                    "splits": splits,
                },
                document_create_from_splits_params.DocumentCreateFromSplitsParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DocumentCreateFromSplitsResponse,
        )

    async def extract(
        self,
        *,
        documents: Iterable[document_extract_params.Document],
        prompt: str,
        response_json_schema: Dict[str, object],
        reasoning_effort: Literal["low", "medium", "high"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DocumentExtractResponse:
        """
        Initiates an asynchronous extraction task using a JSON schema and prompt to
        guide the extraction

        Args:
          documents: An array of documents from which to extract information.

          prompt: The prompt guiding the extraction process.

          response_json_schema: A JSON schema defining the structure of the desired extraction response.

          reasoning_effort: The level of reasoning effort to apply for the extraction. Defaults to medium if
              not specified.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/api/v2/document/extract",
            body=await async_maybe_transform(
                {
                    "documents": documents,
                    "prompt": prompt,
                    "response_json_schema": response_json_schema,
                    "reasoning_effort": reasoning_effort,
                },
                document_extract_params.DocumentExtractParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DocumentExtractResponse,
        )

    async def extraction(
        self,
        *,
        answer_schemas: Iterable[document_extraction_params.AnswerSchema],
        documents: Iterable[document_extraction_params.Document],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DocumentExtractionResponse:
        """
        Initiates an asynchronous legacy extraction task to extract information from
        documents based on answer schemas

        Args:
          answer_schemas: An array of answer schemas defining the information to extract.

          documents: An array of documents from which to extract information.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/api/v2/document/extraction",
            body=await async_maybe_transform(
                {
                    "answer_schemas": answer_schemas,
                    "documents": documents,
                },
                document_extraction_params.DocumentExtractionParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DocumentExtractionResponse,
        )

    async def generate(
        self,
        *,
        slug: str,
        type: Literal["pdf", "report"],
        variables: Dict[str, str],
        file_name: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DocumentGenerateResponse:
        """
        Initiates an asynchronous task to generate a document from a template (PDF or
        report) with provided variables

        Args:
          slug: The slug of the template (either PDF or report) to use for generation.

          type: The type of document to generate: 'pdf' for PDF templates, 'report' for report
              templates.

          variables: An object where keys are variable names and values are their corresponding
              string values to be injected into the template.

          file_name: Optional desired file name for the generated document.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/api/v2/document/generate",
            body=await async_maybe_transform(
                {
                    "slug": slug,
                    "type": type,
                    "variables": variables,
                    "file_name": file_name,
                },
                document_generate_params.DocumentGenerateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DocumentGenerateResponse,
        )

    async def generate_csv(
        self,
        *,
        file_name: str,
        rows: Iterable[Dict[str, Union[str, float]]],
        options: document_generate_csv_params.Options | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DocumentGenerateCsvResponse:
        """
        Generates a new CSV document from provided data rows

        Args:
          file_name: The desired file name for the generated CSV.

          rows: An array of objects, where each object represents a row in the CSV. Keys are
              column headers and values are cell content.

          options: Optional settings for CSV generation.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/api/v2/document/generate-csv",
            body=await async_maybe_transform(
                {
                    "file_name": file_name,
                    "rows": rows,
                    "options": options,
                },
                document_generate_csv_params.DocumentGenerateCsvParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DocumentGenerateCsvResponse,
        )

    async def get_csv_content(
        self,
        document_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DocumentGetCsvContentResponse:
        """
        Retrieves the parsed content of a CSV document as structured data

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not document_id:
            raise ValueError(f"Expected a non-empty value for `document_id` but received {document_id!r}")
        return await self._get(
            f"/api/v2/document/{document_id}/csv-content",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DocumentGetCsvContentResponse,
        )

    async def get_metadata(
        self,
        document_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DocumentGetMetadataResponse:
        """
        Retrieves metadata and a presigned URL for a specific document

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not document_id:
            raise ValueError(f"Expected a non-empty value for `document_id` but received {document_id!r}")
        return await self._get(
            f"/api/v2/document/{document_id}/metadata",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DocumentGetMetadataResponse,
        )

    async def get_presigned_upload_url(
        self,
        *,
        file_name: str,
        mime_type: Literal[
            "application/zip",
            "application/x-zip-compressed",
            "multipart/x-zip",
            "application/x-compress",
            "application/pdf",
            "text/csv",
            "application/javascript",
            "text/css",
            "image/png",
            "video/mp4",
            "application/msword",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DocumentGetPresignedUploadURLResponse:
        """
        Generates a presigned URL for uploading a new document

        Args:
          file_name: The name of the file to be uploaded.

          mime_type: The MIME type of the file to be uploaded.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/api/v2/document/presigned-upload-url",
            body=await async_maybe_transform(
                {
                    "file_name": file_name,
                    "mime_type": mime_type,
                },
                document_get_presigned_upload_url_params.DocumentGetPresignedUploadURLParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DocumentGetPresignedUploadURLResponse,
        )

    async def search(
        self,
        *,
        documents: Iterable[document_search_params.Document],
        query: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DocumentSearchResponse:
        """
        Searches through specified documents for content matching the query

        Args:
          documents: An array of documents to search within.

          query: The search query string.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/api/v2/document/search",
            body=await async_maybe_transform(
                {
                    "documents": documents,
                    "query": query,
                },
                document_search_params.DocumentSearchParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DocumentSearchResponse,
        )

    async def split(
        self,
        *,
        document: document_split_params.Document,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DocumentSplitResponse:
        """
        Initiates an asynchronous task to split a document into multiple parts

        Args:
          document: The document to be split.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/api/v2/document/split",
            body=await async_maybe_transform({"document": document}, document_split_params.DocumentSplitParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DocumentSplitResponse,
        )


class DocumentResourceWithRawResponse:
    def __init__(self, document: DocumentResource) -> None:
        self._document = document

        self.retrieve = to_raw_response_wrapper(
            document.retrieve,
        )
        self.classify = to_raw_response_wrapper(
            document.classify,
        )
        self.create_from_splits = to_raw_response_wrapper(
            document.create_from_splits,
        )
        self.extract = to_raw_response_wrapper(
            document.extract,
        )
        self.extraction = to_raw_response_wrapper(
            document.extraction,
        )
        self.generate = to_raw_response_wrapper(
            document.generate,
        )
        self.generate_csv = to_raw_response_wrapper(
            document.generate_csv,
        )
        self.get_csv_content = to_raw_response_wrapper(
            document.get_csv_content,
        )
        self.get_metadata = to_raw_response_wrapper(
            document.get_metadata,
        )
        self.get_presigned_upload_url = to_raw_response_wrapper(
            document.get_presigned_upload_url,
        )
        self.search = to_raw_response_wrapper(
            document.search,
        )
        self.split = to_raw_response_wrapper(
            document.split,
        )

    @cached_property
    def legacy(self) -> LegacyResourceWithRawResponse:
        return LegacyResourceWithRawResponse(self._document.legacy)


class AsyncDocumentResourceWithRawResponse:
    def __init__(self, document: AsyncDocumentResource) -> None:
        self._document = document

        self.retrieve = async_to_raw_response_wrapper(
            document.retrieve,
        )
        self.classify = async_to_raw_response_wrapper(
            document.classify,
        )
        self.create_from_splits = async_to_raw_response_wrapper(
            document.create_from_splits,
        )
        self.extract = async_to_raw_response_wrapper(
            document.extract,
        )
        self.extraction = async_to_raw_response_wrapper(
            document.extraction,
        )
        self.generate = async_to_raw_response_wrapper(
            document.generate,
        )
        self.generate_csv = async_to_raw_response_wrapper(
            document.generate_csv,
        )
        self.get_csv_content = async_to_raw_response_wrapper(
            document.get_csv_content,
        )
        self.get_metadata = async_to_raw_response_wrapper(
            document.get_metadata,
        )
        self.get_presigned_upload_url = async_to_raw_response_wrapper(
            document.get_presigned_upload_url,
        )
        self.search = async_to_raw_response_wrapper(
            document.search,
        )
        self.split = async_to_raw_response_wrapper(
            document.split,
        )

    @cached_property
    def legacy(self) -> AsyncLegacyResourceWithRawResponse:
        return AsyncLegacyResourceWithRawResponse(self._document.legacy)


class DocumentResourceWithStreamingResponse:
    def __init__(self, document: DocumentResource) -> None:
        self._document = document

        self.retrieve = to_streamed_response_wrapper(
            document.retrieve,
        )
        self.classify = to_streamed_response_wrapper(
            document.classify,
        )
        self.create_from_splits = to_streamed_response_wrapper(
            document.create_from_splits,
        )
        self.extract = to_streamed_response_wrapper(
            document.extract,
        )
        self.extraction = to_streamed_response_wrapper(
            document.extraction,
        )
        self.generate = to_streamed_response_wrapper(
            document.generate,
        )
        self.generate_csv = to_streamed_response_wrapper(
            document.generate_csv,
        )
        self.get_csv_content = to_streamed_response_wrapper(
            document.get_csv_content,
        )
        self.get_metadata = to_streamed_response_wrapper(
            document.get_metadata,
        )
        self.get_presigned_upload_url = to_streamed_response_wrapper(
            document.get_presigned_upload_url,
        )
        self.search = to_streamed_response_wrapper(
            document.search,
        )
        self.split = to_streamed_response_wrapper(
            document.split,
        )

    @cached_property
    def legacy(self) -> LegacyResourceWithStreamingResponse:
        return LegacyResourceWithStreamingResponse(self._document.legacy)


class AsyncDocumentResourceWithStreamingResponse:
    def __init__(self, document: AsyncDocumentResource) -> None:
        self._document = document

        self.retrieve = async_to_streamed_response_wrapper(
            document.retrieve,
        )
        self.classify = async_to_streamed_response_wrapper(
            document.classify,
        )
        self.create_from_splits = async_to_streamed_response_wrapper(
            document.create_from_splits,
        )
        self.extract = async_to_streamed_response_wrapper(
            document.extract,
        )
        self.extraction = async_to_streamed_response_wrapper(
            document.extraction,
        )
        self.generate = async_to_streamed_response_wrapper(
            document.generate,
        )
        self.generate_csv = async_to_streamed_response_wrapper(
            document.generate_csv,
        )
        self.get_csv_content = async_to_streamed_response_wrapper(
            document.get_csv_content,
        )
        self.get_metadata = async_to_streamed_response_wrapper(
            document.get_metadata,
        )
        self.get_presigned_upload_url = async_to_streamed_response_wrapper(
            document.get_presigned_upload_url,
        )
        self.search = async_to_streamed_response_wrapper(
            document.search,
        )
        self.split = async_to_streamed_response_wrapper(
            document.split,
        )

    @cached_property
    def legacy(self) -> AsyncLegacyResourceWithStreamingResponse:
        return AsyncLegacyResourceWithStreamingResponse(self._document.legacy)
