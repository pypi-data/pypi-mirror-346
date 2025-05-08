"""Handler for database operations related to samples."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from sqlmodel import Session, func, select
from sqlmodel.sql.expression import SelectOfScalar, asc, desc

from lightly_purple.server.models import (
    EmbeddingModel,
    Sample,
    SampleEmbedding,
)
from lightly_purple.server.models.samples_filter import SampleFilterParams
from lightly_purple.server.resolvers.samples_filter import (
    SamplesFilter,
)


class SampleAdjacents:
    """Data class for adjacent samples."""

    def __init__(
        self, next_sample: Sample | None, previous_sample: Sample | None
    ):
        """Initialize the SampleAdjacents object."""
        self.next = next_sample
        self.previous = previous_sample


class SampleAdjacentsResolver:
    """Resolver for the Sample model."""

    def __init__(self, session: Session):  # noqa: D107
        self.session = session

    def _apply_filters(
        self,
        query: SelectOfScalar[Sample],
        dataset_id: UUID,
        filters: SampleFilterParams | None = None,
    ) -> SelectOfScalar[Sample]:
        """Apply filters to the query.

        Args:
            query: The base query to apply filters to
            dataset_id: The dataset ID to apply to the filters
            filters: Optional filters to apply

        Returns:
            The query with filters applied
        """
        if not filters:
            return query

        # Create a copy of filters with dataset_id set
        filter_params = SampleFilterParams(**filters.model_dump())
        filter_params.dataset_id = dataset_id
        samples_filter = SamplesFilter(query=query, filters=filter_params)
        return samples_filter.apply_filters()

    def _apply_embedding_search(
        self,
        query: SelectOfScalar[Sample],
        text_embedding: list[float],
        dataset_id: UUID | None = None,
        is_desc: bool = False,
    ) -> SelectOfScalar[Sample]:
        """Apply embedding search filters to the query.

        Args:
            query: The base query to apply filters to
            text_embedding: The text embedding to search for
            dataset_id: The dataset ID to apply to the filters
            is_desc: Whether to apply descending order

        Returns:
            The query with embedding search applied
        """
        # Fetch the first embedding_model_id for the given dataset_id
        embedding_model_id = self.session.exec(
            select(EmbeddingModel.embedding_model_id)
            .where(EmbeddingModel.dataset_id == dataset_id)
            .limit(1)
        ).first()

        if not embedding_model_id:
            return query

        # Join with SampleEmbedding table to access embeddings
        return (
            query.join(
                SampleEmbedding,
                Sample.sample_id == SampleEmbedding.sample_id,  # type: ignore[arg-type]
            )
            .where(SampleEmbedding.embedding_model_id == embedding_model_id)
            .order_by(
                func.list_cosine_distance(
                    SampleEmbedding.embedding,
                    text_embedding,
                ).desc()
                if is_desc
                else func.list_cosine_distance(
                    SampleEmbedding.embedding,
                    text_embedding,
                ).asc(),
                desc(Sample.created_at) if is_desc else asc(Sample.created_at),
            )
        )

    def get_adjacent_samples_by_sample_id(
        self,
        sample_id: UUID,
        filters: SampleFilterParams | None = None,
        text_embedding: list[float] | None = None,
    ) -> SampleAdjacents:
        """Get the next and previous samples based on the sample ID.

        Args:
            sample_id: The sample ID to find adjacent samples for
            filters: Optional filters to apply to the query
            text_embedding: Optional text embedding for search

        Returns:
            A SampleAdjacents object with the next and previous samples
        """
        current_sample = self.session.get(Sample, sample_id)
        if current_sample is None:
            return SampleAdjacents(next_sample=None, previous_sample=None)

        # TODO(Kondrat 06/05/2024): use lead/lag window functions
        # to get the next and previous samples
        return SampleAdjacents(
            next_sample=self._get_next_sample(
                current_sample.created_at,
                current_sample.dataset_id,
                filters,
                text_embedding,
            ),
            previous_sample=self._get_previous_sample(
                current_sample.created_at,
                current_sample.dataset_id,
                filters,
                text_embedding,
            ),
        )

    def _get_next_sample(
        self,
        created_at: datetime,
        dataset_id: UUID,
        filters: SampleFilterParams | None = None,
        text_embedding: list[float] | None = None,
    ) -> Sample | None:
        """Get the next sample in the dataset.

        Args:
            created_at: The creation time of the current sample
            dataset_id: The dataset ID to which the sample belongs
            filters: Optional filters to apply to the query
            text_embedding: Optional text embedding for search

        Returns:
            The next sample or None if there is no next sample
        """
        # Start with base query for the dataset
        query = select(Sample).where(Sample.dataset_id == dataset_id)

        # Apply filters first
        query = self._apply_filters(query, dataset_id, filters)

        # For text embedding search, the ordering is handled by the filter
        if text_embedding:
            query = self._apply_embedding_search(
                query, text_embedding, is_desc=False
            )
            return self.session.exec(query).first()

        # Otherwise use created_at ordering
        query = query.where(Sample.created_at > created_at).order_by(
            asc(Sample.created_at)
        )
        return self.session.exec(query).first()

    def _get_previous_sample(
        self,
        created_at: datetime,
        dataset_id: UUID,
        filters: SampleFilterParams | None = None,
        text_embedding: list[float] | None = None,
    ) -> Sample | None:
        """Get the previous sample in the dataset.

        Args:
            created_at: The creation time of the current sample
            dataset_id: The dataset ID to which the sample belongs
            filters: Optional filters to apply to the query
            text_embedding: Optional text embedding for search

        Returns:
            The previous sample or None if there is no previous sample
        """
        # Start with base query for the dataset
        query = select(Sample).where(Sample.dataset_id == dataset_id)

        # Apply filters first
        query = self._apply_filters(query, dataset_id, filters)

        # For text embedding search, the ordering is handled by the filter
        if text_embedding:
            query = self._apply_embedding_search(
                query, text_embedding, is_desc=True
            )
            return self.session.exec(query).first()

        # Otherwise use created_at ordering
        query = query.where(Sample.created_at < created_at).order_by(
            desc(Sample.created_at)
        )
        return self.session.exec(query).first()
