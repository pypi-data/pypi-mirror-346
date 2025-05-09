# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union
from typing_extensions import Literal, TypeAlias

from pydantic import Field as FieldInfo

from ...._models import BaseModel

__all__ = [
    "DocumentSplitResponse",
    "UnionMember0",
    "UnionMember0Inputs",
    "UnionMember0Result",
    "UnionMember0ResultSplits",
    "UnionMember0ResultSplitsValue",
    "UnionMember1",
    "UnionMember1Inputs",
    "UnionMember1Result",
]


class UnionMember0Inputs(BaseModel):
    document_id: str = FieldInfo(alias="documentId")


class UnionMember0ResultSplitsValue(BaseModel):
    page: float

    probability: float


class UnionMember0ResultSplits(BaseModel):
    values: List[UnionMember0ResultSplitsValue]


class UnionMember0Result(BaseModel):
    splits: UnionMember0ResultSplits


class UnionMember0(BaseModel):
    inputs: UnionMember0Inputs

    result: UnionMember0Result

    status: Literal["success"]


class UnionMember1Inputs(BaseModel):
    document_id: str = FieldInfo(alias="documentId")


class UnionMember1Result(BaseModel):
    error: str


class UnionMember1(BaseModel):
    inputs: UnionMember1Inputs

    result: UnionMember1Result

    status: Literal["failed"]


DocumentSplitResponse: TypeAlias = Union[UnionMember0, UnionMember1]
