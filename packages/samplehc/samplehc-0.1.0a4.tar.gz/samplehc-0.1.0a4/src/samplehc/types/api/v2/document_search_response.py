# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List

from ...._models import BaseModel

__all__ = ["DocumentSearchResponse", "Result", "ResultBlock"]


class ResultBlock(BaseModel):
    bbox: Dict[str, float]
    """Bounding box coordinates of the block."""

    content: str
    """The text content of the block."""

    type: str
    """The type of the block."""


class Result(BaseModel):
    id: str
    """The ID of the search result item."""

    blocks: List[ResultBlock]
    """Array of content blocks within the search result."""

    file_metadata_id: str
    """The ID of the file metadata associated with this result."""

    file_name: str
    """The name of the file associated with this result."""

    highlighted_content: str
    """Content snippet with search terms highlighted."""

    match_score: float
    """The relevance score of this search result."""


class DocumentSearchResponse(BaseModel):
    results: List[Result]
    """A list of search results."""
