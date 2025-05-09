"""Handler for database operations related to annotations."""

from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, Field
from sqlmodel import Session, func, select

from lightly_purple.server.models import (
    AnnotationLabel,
    BoundingBoxAnnotation,
    Sample,
    Tag,
)
from lightly_purple.server.models.bounding_box_annotation import (
    BoundingBoxAnnotationInput,
)
from lightly_purple.server.routes.api.validators import Paginated


class AnnotationsFilterParams(BaseModel):
    """Encapsulates filter parameters for querying annotations."""

    dataset_ids: list[UUID] | None = Field(
        default=None, description="List of dataset UUIDs"
    )
    annotation_label_ids: list[UUID] | None = Field(
        default=None, description="List of annotation label UUIDs"
    )
    annotation_tag_ids: list[UUID] | None = Field(
        default=None, description="List of tag UUIDs"
    )
    sample_tag_ids: list[UUID] | None = Field(
        default=None,
        description="List of sample tag UUIDs to filter annotations by",
    )
    annotation_task_ids: list[UUID] | None = Field(
        default=None, description="List of annotation task UUIDs"
    )


class BoundingBoxAnnotationResolver:
    """Resolver for the BoundingBoxAnnotation model."""

    def __init__(self, session: Session):  # noqa: D107
        self.session = session

    def create(
        self, annotation: BoundingBoxAnnotationInput
    ) -> BoundingBoxAnnotation:
        """Create a new annotation in the database."""
        db_annotation = BoundingBoxAnnotation.model_validate(annotation)
        self.session.add(db_annotation)
        self.session.commit()
        self.session.refresh(db_annotation)
        return db_annotation

    def create_many(
        self, annotations: list[BoundingBoxAnnotationInput]
    ) -> None:
        """Create many annotations in a single commit. No return values."""
        db_annotations = [
            BoundingBoxAnnotation.model_validate(a) for a in annotations
        ]
        self.session.bulk_save_objects(db_annotations)
        self.session.commit()

    def get_all(  # noqa: C901, PLR0912
        self,
        pagination: dict | Paginated | None = None,
        filters: AnnotationsFilterParams | None = None,
    ) -> list[BoundingBoxAnnotation]:
        """Retrieve all annotations from the database."""
        # Determine pagination parameters
        if pagination is None:
            offset = None
            limit = None
        elif isinstance(pagination, dict):
            pag = Paginated(**pagination)
            offset = pag.offset
            limit = pag.limit
        else:
            offset = pagination.offset
            limit = pagination.limit

        if filters is None:
            filters = AnnotationsFilterParams()
        elif isinstance(filters, dict):
            filters = AnnotationsFilterParams(**filters)

        query = select(BoundingBoxAnnotation)

        # Apply filters if provided
        if filters:
            if filters.dataset_ids:
                query = query.where(
                    BoundingBoxAnnotation.dataset_id.in_(filters.dataset_ids)
                )

            if filters.annotation_task_ids:
                query = query.where(
                    BoundingBoxAnnotation.annotation_task_id.in_(
                        filters.annotation_task_ids
                    )
                )

            if filters.annotation_label_ids:
                query = query.where(
                    BoundingBoxAnnotation.annotation_label_id.in_(
                        filters.annotation_label_ids
                    )
                )

            # Filter by annotation tags
            if filters.annotation_tag_ids:
                query = (
                    query.join(BoundingBoxAnnotation.tags)
                    .where(
                        BoundingBoxAnnotation.tags.any(
                            Tag.tag_id.in_(filters.annotation_tag_ids)
                        )
                    )
                    .distinct()
                )

            # Filter by sample tags
            if filters.sample_tag_ids:
                query = (
                    query.join(
                        Sample,
                        BoundingBoxAnnotation.sample_id == Sample.sample_id,
                    )
                    .join(Sample.tags)
                    .where(
                        Sample.tags.any(Tag.tag_id.in_(filters.sample_tag_ids))
                    )
                    .distinct()
                )

        # Apply pagination if specified
        if offset is not None:
            query = query.offset(offset)
        if limit is not None:
            query = query.limit(limit)

        results = self.session.exec(query).all()
        return results or []

    def get_by_id(self, annotation_id: UUID) -> BoundingBoxAnnotation | None:
        """Retrieve a single annotation by ID."""
        return self.session.exec(
            select(BoundingBoxAnnotation).where(
                BoundingBoxAnnotation.annotation_id == annotation_id
            )
        ).one_or_none()

    def update(
        self, annotation_id: UUID, annotation_data: BoundingBoxAnnotationInput
    ) -> BoundingBoxAnnotation | None:
        """Update an existing annotation."""
        annotation = self.get_by_id(annotation_id)
        if not annotation:
            return None

        annotation.x = annotation_data.x
        annotation.y = annotation_data.y
        annotation.width = annotation_data.width
        annotation.height = annotation_data.height

        # Update new fields if they're provided
        if (
            hasattr(annotation_data, "confidence")
            and annotation_data.confidence is not None
        ):
            annotation.confidence = annotation_data.confidence

        if (
            hasattr(annotation_data, "annotation_task_id")
            and annotation_data.annotation_task_id is not None
        ):
            annotation.annotation_task_id = annotation_data.annotation_task_id

        if (
            hasattr(annotation_data, "segmentation__binary_mask__rle_row_wise")
            and annotation_data.segmentation__binary_mask__rle_row_wise
            is not None
        ):
            annotation.segmentation__binary_mask__rle_row_wise = (
                annotation_data.segmentation__binary_mask__rle_row_wise
            )

        self.session.commit()
        self.session.refresh(annotation)
        return annotation

    def delete(self, annotation_id: UUID) -> bool:
        """Delete an annotation."""
        annotation = self.get_by_id(annotation_id)
        if not annotation:
            return False

        self.session.delete(annotation)
        self.session.commit()
        return True

    def count_annotations_by_dataset(  # noqa: PLR0913 // FIXME: refactor to use proper pydantic
        self,
        dataset_id: UUID,
        filtered_labels: list[str] | None = None,
        min_width: int | None = None,
        max_width: int | None = None,
        min_height: int | None = None,
        max_height: int | None = None,
        tag_ids: list[UUID] | None = None,
    ) -> list[tuple[str, int, int]]:
        """Count annotations for a specific dataset.

        Annotations for a specific dataset are grouped by annotation
        label name and counted for total and filtered.
        """
        # Query for total counts (unfiltered)
        total_counts_query = (
            select(
                AnnotationLabel.annotation_label_name,
                func.count(BoundingBoxAnnotation.annotation_id).label(
                    "total_count"
                ),
            )
            .join(
                BoundingBoxAnnotation,
                BoundingBoxAnnotation.annotation_label_id
                == AnnotationLabel.annotation_label_id,
            )
            .join(Sample, Sample.sample_id == BoundingBoxAnnotation.sample_id)
            .where(Sample.dataset_id == dataset_id)
            .group_by(AnnotationLabel.annotation_label_name)
            .order_by(AnnotationLabel.annotation_label_name.asc())
        )

        total_counts = {
            row[0]: row[1]
            for row in self.session.exec(total_counts_query).all()
        }

        # Build filtered query for current counts
        filtered_query = (
            select(
                AnnotationLabel.annotation_label_name,
                func.count(BoundingBoxAnnotation.annotation_id).label(
                    "current_count"
                ),
            )
            .join(
                BoundingBoxAnnotation,
                BoundingBoxAnnotation.annotation_label_id
                == AnnotationLabel.annotation_label_id,
            )
            .join(Sample, Sample.sample_id == BoundingBoxAnnotation.sample_id)
            .where(Sample.dataset_id == dataset_id)
        )

        # Add dimension filters
        if min_width is not None:
            filtered_query = filtered_query.where(Sample.width >= min_width)
        if max_width is not None:
            filtered_query = filtered_query.where(Sample.width <= max_width)
        if min_height is not None:
            filtered_query = filtered_query.where(Sample.height >= min_height)
        if max_height is not None:
            filtered_query = filtered_query.where(Sample.height <= max_height)

        # Add label filter if specified
        if filtered_labels:
            filtered_query = filtered_query.where(
                Sample.sample_id.in_(
                    select(Sample.sample_id)
                    .join(
                        BoundingBoxAnnotation,
                        Sample.sample_id == BoundingBoxAnnotation.sample_id,
                    )
                    .join(
                        AnnotationLabel,
                        BoundingBoxAnnotation.annotation_label_id
                        == AnnotationLabel.annotation_label_id,
                    )
                    .where(
                        AnnotationLabel.annotation_label_name.in_(
                            filtered_labels
                        )
                    )
                )
            )

        # filter by tag_ids
        if tag_ids:
            filtered_query = (
                filtered_query.join(BoundingBoxAnnotation.tags)
                .where(BoundingBoxAnnotation.tags.any(Tag.tag_id.in_(tag_ids)))
                .distinct()
            )

        # Group by label name and sort
        filtered_query = filtered_query.group_by(
            AnnotationLabel.annotation_label_name
        ).order_by(AnnotationLabel.annotation_label_name.asc())

        _rows = self.session.exec(filtered_query).all()

        current_counts = {row[0]: row[1] for row in _rows}

        return [
            (label, current_counts.get(label, 0), total_count)
            for label, total_count in total_counts.items()
        ]
