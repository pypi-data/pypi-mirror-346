"""Utility functions for building database queries."""

from typing import Optional

from sqlmodel import Session
from sqlmodel.sql.expression import SelectOfScalar

from lightly_purple.server.models import (
    AnnotationLabel,
    Sample,
    Tag,
)
from lightly_purple.server.models.samples_filter import SampleFilterParams


class SamplesFilter:
    """Data class for filtering samples."""

    def __init__(
        self,
        query: SelectOfScalar[Sample],
        filters: SampleFilterParams,
        session: Optional[Session] = None,
    ):
        """Initialize the SamplesFilter object."""
        self.filters = filters
        self.query = query
        self.session = session

    def apply_filters(self) -> SelectOfScalar[Sample]:
        """Apply all filters to the query."""
        query = self.apply_dimensions_filters()
        if self.filters.annotation_labels_ids:
            query = self.apply_annotation_filters(query)
        if self.filters.tag_ids:
            query = self.apply_tag_filters(query)
        return query

    def apply_dimensions_filters(
        self,
    ) -> SelectOfScalar[Sample]:
        """Apply dimension-based filters to the query."""
        width = self.filters.width
        height = self.filters.height
        query = self.query

        if width:
            if width.min is not None:
                query = query.where(Sample.width >= width.min)
            if width.max is not None:
                query = query.where(Sample.width <= width.max)
        if height:
            if height.min is not None:
                query = query.where(Sample.height >= height.min)
            if height.max is not None:
                query = query.where(Sample.height <= height.max)
        return query

    def apply_annotation_filters(
        self, query: SelectOfScalar[Sample]
    ) -> SelectOfScalar[Sample]:
        """Apply annotation label filters to the query."""
        return (
            query.join(Sample.annotations)  # type: ignore[arg-type]
            .join(AnnotationLabel)
            .where(
                AnnotationLabel.annotation_label_id.in_(  # type: ignore[attr-defined]
                    self.filters.annotation_labels_ids
                )
            )
        )

    def apply_tag_filters(
        self, query: SelectOfScalar[Sample]
    ) -> SelectOfScalar[Sample]:
        """Apply tag filters to the query."""
        return query.join(Sample.tags).where(  # type: ignore[arg-type]
            Tag.tag_id.in_(self.filters.tag_ids)  # type: ignore[attr-defined]
        )
