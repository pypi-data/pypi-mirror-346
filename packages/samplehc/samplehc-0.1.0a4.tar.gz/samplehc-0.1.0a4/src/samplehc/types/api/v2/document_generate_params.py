# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict
from typing_extensions import Literal, Required, Annotated, TypedDict

from ...._utils import PropertyInfo

__all__ = ["DocumentGenerateParams"]


class DocumentGenerateParams(TypedDict, total=False):
    slug: Required[str]
    """The slug of the template (either PDF or report) to use for generation."""

    type: Required[Literal["pdf", "report"]]
    """
    The type of document to generate: 'pdf' for PDF templates, 'report' for report
    templates.
    """

    variables: Required[Dict[str, str]]
    """
    An object where keys are variable names and values are their corresponding
    string values to be injected into the template.
    """

    file_name: Annotated[str, PropertyInfo(alias="fileName")]
    """Optional desired file name for the generated document."""
