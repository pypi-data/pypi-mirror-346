# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from ..._models import BaseModel

__all__ = ["V1CreateSqlResponse"]


class V1CreateSqlResponse(BaseModel):
    rows: List[object]
    """The result rows from the SQL query"""
