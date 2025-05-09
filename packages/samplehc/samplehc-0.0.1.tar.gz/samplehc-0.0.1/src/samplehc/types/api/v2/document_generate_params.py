# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict
from typing_extensions import Literal, Required, Annotated, TypedDict

from ...._utils import PropertyInfo

__all__ = ["DocumentGenerateParams"]


class DocumentGenerateParams(TypedDict, total=False):
    slug: Required[str]

    type: Required[Literal["pdf", "report"]]

    variables: Required[Dict[str, str]]

    file_name: Annotated[str, PropertyInfo(alias="fileName")]
