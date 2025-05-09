# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Iterable
from typing_extensions import Literal, Required, Annotated, TypedDict

from ...._utils import PropertyInfo

__all__ = ["DocumentExtractParams", "Document"]


class DocumentExtractParams(TypedDict, total=False):
    documents: Required[Iterable[Document]]

    prompt: Required[str]

    response_json_schema: Required[Annotated[Dict[str, object], PropertyInfo(alias="responseJsonSchema")]]

    reasoning_effort: Annotated[Literal["low", "medium", "high"], PropertyInfo(alias="reasoningEffort")]


class Document(TypedDict, total=False):
    id: Required[str]

    file_name: Required[Annotated[str, PropertyInfo(alias="fileName")]]
