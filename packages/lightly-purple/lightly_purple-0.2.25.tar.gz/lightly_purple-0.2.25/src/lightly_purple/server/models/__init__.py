"""This module contains models with shared type dependencies."""

from datetime import datetime, timezone
from typing import List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel
from sqlalchemy import UniqueConstraint
from sqlmodel import Field, Relationship, SQLModel, String

from lightly_purple.server.models.annotation_label import AnnotationLabelBase
from lightly_purple.server.models.annotation_task import (
    AnnotationTask,  # noqa: F401 needed for SQL model generation
    AnnotationType,  # noqa: F401 needed for SQL model generation
)
from lightly_purple.server.models.bounding_box_annotation import (
    BoundingBoxAnnotationBase,
)
from lightly_purple.server.models.dataset import DatasetBase
from lightly_purple.server.models.embedding_model import EmbeddingModelBase
from lightly_purple.server.models.sample import (
    SampleBase,
    SampleViewForAnnotation,
)
from lightly_purple.server.models.sample_embedding import SampleEmbeddingBase
from lightly_purple.server.models.samples_filter import SampleFilterParams
from lightly_purple.server.models.settings import SettingBase
from lightly_purple.server.models.tag import TagBase, TagKind, TagView


class AnnotationTagLink(SQLModel, table=True):
    """AnnotationTagLink links Annotation and Tag Many-to-Many."""

    annotation_id: Optional[UUID] = Field(
        default=None,
        foreign_key="bounding_box_annotations.annotation_id",
        primary_key=True,
    )
    tag_id: Optional[UUID] = Field(
        default=None, foreign_key="tags.tag_id", primary_key=True
    )


class BoundingBoxAnnotation(BoundingBoxAnnotationBase, table=True):
    """This class defines the BoundingBoxAnnotation model."""

    __tablename__ = "bounding_box_annotations"
    annotation_id: UUID = Field(default_factory=uuid4, primary_key=True)
    annotation_label: "AnnotationLabel" = Relationship(
        back_populates="annotations",
        sa_relationship_kwargs={"lazy": "select"},
    )
    sample: Optional["Sample"] = Relationship(
        back_populates="annotations",
        sa_relationship_kwargs={"lazy": "select"},
    )

    """The tag ids associated with the sample."""
    tags: List["Tag"] = Relationship(
        back_populates="annotations", link_model=AnnotationTagLink
    )


class AnnotationLabel(AnnotationLabelBase, table=True):
    """This class defines the AnnotationLabel model."""

    __tablename__ = "annotation_labels"
    annotation_label_id: UUID = Field(default_factory=uuid4, primary_key=True)
    annotations: List["BoundingBoxAnnotation"] = Relationship(
        back_populates="annotation_label",
    )


class SampleTagLink(SQLModel, table=True):
    """SampleTagLink links Sample and Tag Many-to-Many."""

    sample_id: Optional[UUID] = Field(
        default=None, foreign_key="samples.sample_id", primary_key=True
    )
    tag_id: Optional[UUID] = Field(
        default=None, foreign_key="tags.tag_id", primary_key=True
    )


class Sample(SampleBase, table=True):
    """This class defines the Sample model."""

    __tablename__ = "samples"
    sample_id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
    )
    annotations: List["BoundingBoxAnnotation"] = Relationship(
        back_populates="sample",
    )

    """The tag ids associated with the sample."""
    tags: List["Tag"] = Relationship(
        back_populates="samples", link_model=SampleTagLink
    )
    embeddings: List["SampleEmbedding"] = Relationship(back_populates="sample")


class Tag(TagBase, table=True):
    """This class defines the Tag model."""

    __tablename__ = "tags"
    # ensure there can only be one tag named "purple" per dataset
    __table_args__ = (
        UniqueConstraint(
            "dataset_id", "kind", "name", name="unique_name_constraint"
        ),
    )
    tag_id: UUID = Field(default_factory=uuid4, primary_key=True)
    dataset_id: UUID
    kind: TagKind = Field(sa_type=String)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
    )

    """The sample ids associated with the tag."""
    samples: List["Sample"] = Relationship(
        back_populates="tags",
        link_model=SampleTagLink,
    )
    """The annotation ids associated with the tag."""
    annotations: List["BoundingBoxAnnotation"] = Relationship(
        back_populates="tags",
        link_model=AnnotationTagLink,
    )


class Dataset(DatasetBase, table=True):
    """This class defines the Dataset model."""

    __tablename__ = "datasets"
    dataset_id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
    )


class AnnotationView(SQLModel):
    """Annotation view model."""

    x: float
    y: float
    width: float
    height: float
    sample_id: UUID
    dataset_id: UUID
    annotation_id: UUID
    annotation_label: "AnnotationLabelView"
    annotation_task_id: UUID
    confidence: Optional[float] = None
    segmentation__binary_mask__rle_row_wise: Optional[List[int]]


class AnnotationViewForAnnotationLabel(SQLModel):
    """Annotation view model for annotation."""

    annotation_id: UUID
    x: float
    y: float
    width: float
    height: float
    sample: "SampleViewForAnnotation"
    annotation_label: "AnnotationLabelView"
    annotation_task_id: UUID
    confidence: Optional[float] = None
    segmentation__binary_mask__rle_row_wise: Optional[List[int]]


class AnnotationLabelView(AnnotationLabelBase):
    """AnnotationLabel class when retrieving."""

    annotation_label_id: UUID


class SampleView(SQLModel):
    """Sample class when retrieving."""

    """The name of the image file."""
    file_name: str
    file_path_abs: str
    sample_id: UUID
    dataset_id: UUID
    annotations: List["AnnotationView"] = Field([])
    tags: List["TagView"] = Field([])
    width: int
    height: int


class SampleAdjacentsView(SQLModel):
    """View class for adjacent samples."""

    next: Optional["SampleView"] = None
    previous: Optional["SampleView"] = None


class SampleAdjacentsParams(BaseModel):
    """Parameters for getting adjacent samples."""

    filters: Optional["SampleFilterParams"] = None
    text_embedding: Optional[List[float]] = None


class EmbeddingModel(EmbeddingModelBase, table=True):
    """This class defines the EmbeddingModel model."""

    __tablename__ = "embedding_models"
    embedding_model_id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
    )


class SampleEmbedding(SampleEmbeddingBase, table=True):
    """This class defines the SampleEmbedding model."""

    __tablename__ = "sample_embeddings"
    sample: "Sample" = Relationship(back_populates="embeddings")


class Setting(SettingBase, table=True):
    """This class defines the Setting model."""

    __tablename__ = "settings"
    setting_id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
    )
