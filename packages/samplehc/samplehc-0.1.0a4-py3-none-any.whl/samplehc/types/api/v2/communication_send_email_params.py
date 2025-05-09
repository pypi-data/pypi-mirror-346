# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Required, Annotated, TypedDict

from ...._utils import PropertyInfo

__all__ = ["CommunicationSendEmailParams", "Attachment"]


class CommunicationSendEmailParams(TypedDict, total=False):
    body: Required[str]
    """Email body content in plain text or HTML format"""

    subject: Required[str]
    """Email subject line"""

    to: Required[str]
    """
    Comma-separated list of recipient email addresses (e.g., 'john@example.com,
    jane@example.com')
    """

    attachments: Iterable[Attachment]
    """Array of file metadata IDs to attach (as a link) to the email"""

    enable_encryption: Annotated[bool, PropertyInfo(alias="enableEncryption")]
    """
    If true, the email body will be encrypted and a secure link will be sent instead
    """

    zip_attachments: Annotated[bool, PropertyInfo(alias="zipAttachments")]
    """If true, all attachments will be combined into a single zip file"""


class Attachment(TypedDict, total=False):
    id: Required[str]
    """ID of the file metadata to attach"""
