# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Required, Annotated, TypedDict

from ...._utils import PropertyInfo

__all__ = ["DocumentCreateFromSplitsParams", "Document"]


class DocumentCreateFromSplitsParams(TypedDict, total=False):
    document: Required[Document]
    """The original document from which splits are being created."""

    splits: Required[Iterable[float]]
    """An array of page numbers (1-indexed) where the document should be split.

    Each number indicates the end of a new document segment.
    """


class Document(TypedDict, total=False):
    id: Required[str]

    file_name: Required[Annotated[str, PropertyInfo(alias="fileName")]]
