# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["V2GetAsyncResultResponse"]


class V2GetAsyncResultResponse(BaseModel):
    status: Literal["pending", "success", "failed"]
    """The status of the async job."""

    inputs: Optional[object] = None
    """The inputs of the async job."""

    result: Optional[object] = None
    """The result of the async job. May be undefined if the job is pending or failed."""
