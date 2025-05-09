# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Union, Iterable
from typing_extensions import Required, Annotated, TypedDict

from ...._utils import PropertyInfo

__all__ = ["DocumentGenerateCsvParams", "Options"]


class DocumentGenerateCsvParams(TypedDict, total=False):
    file_name: Required[Annotated[str, PropertyInfo(alias="fileName")]]
    """The desired file name for the generated CSV."""

    rows: Required[Iterable[Dict[str, Union[str, float]]]]
    """An array of objects, where each object represents a row in the CSV.

    Keys are column headers and values are cell content.
    """

    options: Options
    """Optional settings for CSV generation."""


class Options(TypedDict, total=False):
    column_order: Annotated[List[str], PropertyInfo(alias="columnOrder")]
    """An array of strings specifying the exact order of columns in the output file.

    If omitted, column order is based on the first row's keys.
    """

    export_as_excel: Annotated[bool, PropertyInfo(alias="exportAsExcel")]
    """If true, exports the file in Excel (.xlsx) format instead of CSV.

    Defaults to false.
    """
