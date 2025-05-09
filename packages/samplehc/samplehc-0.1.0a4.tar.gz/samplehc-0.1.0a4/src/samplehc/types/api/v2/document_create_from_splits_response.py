# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from pydantic import Field as FieldInfo

from ...._models import BaseModel

__all__ = ["DocumentCreateFromSplitsResponse", "CreatedDocument"]


class CreatedDocument(BaseModel):
    id: str

    end_page_inclusive: float = FieldInfo(alias="endPageInclusive")
    """The 1-indexed end page (inclusive) of this split document segment."""

    file_name: str = FieldInfo(alias="fileName")

    start_page_inclusive: float = FieldInfo(alias="startPageInclusive")
    """The 1-indexed start page (inclusive) of this split document segment."""


class DocumentCreateFromSplitsResponse(BaseModel):
    created_documents: List[CreatedDocument] = FieldInfo(alias="createdDocuments")
    """An array of newly created documents from the splits."""
