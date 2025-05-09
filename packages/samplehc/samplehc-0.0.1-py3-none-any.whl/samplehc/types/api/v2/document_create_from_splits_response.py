# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from pydantic import Field as FieldInfo

from ...._models import BaseModel

__all__ = ["DocumentCreateFromSplitsResponse", "CreatedDocument"]


class CreatedDocument(BaseModel):
    id: str

    end_page_inclusive: float = FieldInfo(alias="endPageInclusive")

    file_name: str = FieldInfo(alias="fileName")

    start_page_inclusive: float = FieldInfo(alias="startPageInclusive")


class DocumentCreateFromSplitsResponse(BaseModel):
    created_documents: List[CreatedDocument] = FieldInfo(alias="createdDocuments")
