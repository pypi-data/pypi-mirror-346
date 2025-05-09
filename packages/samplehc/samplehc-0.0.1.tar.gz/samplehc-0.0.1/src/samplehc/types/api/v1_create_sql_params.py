# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Required, Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["V1CreateSqlParams"]


class V1CreateSqlParams(TypedDict, total=False):
    params: Required[Iterable[object]]

    query: Required[str]

    array_mode: Annotated[bool, PropertyInfo(alias="arrayMode")]
