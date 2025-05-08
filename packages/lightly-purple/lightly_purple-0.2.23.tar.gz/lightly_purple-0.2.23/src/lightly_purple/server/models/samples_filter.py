"""Models for filtering samples."""

from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel


class FilterDimensions(BaseModel):
    """Encapsulates dimension-based filter parameters for querying samples."""

    min: Optional[int] = None
    max: Optional[int] = None


class SampleFilterParams(BaseModel):
    """Encapsulates filter parameters for querying samples."""

    dataset_id: Optional[UUID] = None
    width: Optional[FilterDimensions] = None
    height: Optional[FilterDimensions] = None
    annotation_labels_ids: Optional[List[UUID]] = None
    tag_ids: Optional[List[UUID]] = None
