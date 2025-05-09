# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Union, Iterable
from typing_extensions import Required, Annotated, TypedDict

from ...._utils import PropertyInfo

__all__ = ["DocumentGenerateCsvParams", "Options"]


class DocumentGenerateCsvParams(TypedDict, total=False):
    file_name: Required[Annotated[str, PropertyInfo(alias="fileName")]]

    rows: Required[Iterable[Dict[str, Union[str, float]]]]

    options: Options


class Options(TypedDict, total=False):
    column_order: Annotated[List[str], PropertyInfo(alias="columnOrder")]

    export_as_excel: Annotated[bool, PropertyInfo(alias="exportAsExcel")]
