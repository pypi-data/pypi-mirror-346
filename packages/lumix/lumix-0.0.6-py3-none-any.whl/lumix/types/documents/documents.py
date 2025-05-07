import numpy as np
from PIL import Image
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field, ConfigDict


__all__ = [
    "PageMetadata",
    "DocumentPage",
    "SearchedImage",
]


class PageMetadata(BaseModel):
    """"""
    model_config = ConfigDict(arbitrary_types_allowed=True)
    images: Optional[List[Image.Image]] = None
    vector: Optional[Union[List[float], np.ndarray]] = None
    path: Optional[str] = None
    type: Optional[str] = None
    kwargs: Optional[Any] = None
    page_number: Optional[int] = None


class DocumentPage(BaseModel):
    """"""
    model_config = ConfigDict(arbitrary_types_allowed=True)
    """Class for storing a piece of text and associated metadata."""

    page_content: Optional[str] = Field(default=None)
    """String text."""

    metadata: Optional[Union[dict, PageMetadata]] = Field(default_factory=dict)
    """Arbitrary metadata about the page content (e.g., source, relationships to other
        documents, etc.).
    """

    def __init__(
            self,
            page_content: Optional[str] = None,
            metadata: Optional[Union[dict, PageMetadata]] = None,
            **kwargs: Any
    ) -> None:
        """Pass page_content in as positional or named arg."""
        super().__init__(page_content=page_content, metadata=metadata, **kwargs)


class SearchedImage(BaseModel):
    """"""
    model_config = ConfigDict(arbitrary_types_allowed=True)
    image: Image.Image
    metadata: Dict
