# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Required, Annotated, TypedDict

from ...._utils import PropertyInfo

__all__ = ["CommunicationSendEmailParams", "Attachment"]


class CommunicationSendEmailParams(TypedDict, total=False):
    body: Required[str]

    subject: Required[str]

    to: Required[str]

    attachments: Iterable[Attachment]

    enable_encryption: Annotated[bool, PropertyInfo(alias="enableEncryption")]

    zip_attachments: Annotated[bool, PropertyInfo(alias="zipAttachments")]


class Attachment(TypedDict, total=False):
    id: Required[str]
