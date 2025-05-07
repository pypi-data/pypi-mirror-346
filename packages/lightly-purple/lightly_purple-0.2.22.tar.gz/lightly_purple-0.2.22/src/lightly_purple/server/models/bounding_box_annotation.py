"""This module defines the BoundingBoxAnnotation model."""

from typing import List, Optional
from uuid import UUID

from sqlalchemy import ARRAY, Column, Integer
from sqlmodel import Field, SQLModel


class BoundingBoxAnnotationBase(SQLModel):
    """Base class for the BoundingBoxAnnotation model."""

    x: float
    y: float
    width: float
    height: float
    annotation_label_id: UUID = Field(
        foreign_key="annotation_labels.annotation_label_id"
    )
    dataset_id: UUID = Field(foreign_key="datasets.dataset_id")
    sample_id: UUID = Field(foreign_key="samples.sample_id")

    annotation_task_id: UUID = Field(
        foreign_key="annotation_tasks.annotation_task_id",
    )

    confidence: Optional[float] = None

    segmentation__binary_mask__rle_row_wise: Optional[List[int]] = Field(
        default=None,
        sa_column=Column(ARRAY(Integer), nullable=True),
    )


class BoundingBoxAnnotationInput(BoundingBoxAnnotationBase):
    """Bounding box annotation input model for creation."""
