# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Required, Annotated, TypedDict

from ...._utils import PropertyInfo

__all__ = ["DocumentCreateFromSplitsParams", "Document"]


class DocumentCreateFromSplitsParams(TypedDict, total=False):
    document: Required[Document]

    splits: Required[Iterable[float]]


class Document(TypedDict, total=False):
    id: Required[str]

    file_name: Required[Annotated[str, PropertyInfo(alias="fileName")]]
