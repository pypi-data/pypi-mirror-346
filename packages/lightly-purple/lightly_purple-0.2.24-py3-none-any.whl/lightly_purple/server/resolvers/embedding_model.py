"""Handler for database operations related to embedding models."""

from __future__ import annotations

from uuid import UUID

from sqlmodel import Session, select

from lightly_purple.server.models import (
    EmbeddingModel,
)
from lightly_purple.server.models.embedding_model import (
    EmbeddingModelInput,
)


class EmbeddingModelResolver:
    """Resolver for the EmbeddingModel model."""

    def __init__(self, session: Session):
        """Initialize the EmbeddingModelResolver."""
        self.session = session

    def create(self, embedding_model: EmbeddingModelInput) -> EmbeddingModel:
        """Create a new EmbeddingModel in the database."""
        db_embedding_model = EmbeddingModel.model_validate(embedding_model)
        self.session.add(db_embedding_model)
        self.session.commit()
        self.session.refresh(db_embedding_model)
        return db_embedding_model

    def get_all_by_dataset_id(self, dataset_id: UUID) -> list[EmbeddingModel]:
        """Retrieve all embedding models."""
        embedding_models = self.session.exec(
            select(EmbeddingModel).where(
                EmbeddingModel.dataset_id == dataset_id
            )
        ).all()
        return list(embedding_models)

    def get_by_id(self, embedding_model_id: UUID) -> EmbeddingModel | None:
        """Retrieve a single embedding model by ID."""
        return self.session.exec(
            select(EmbeddingModel).where(
                EmbeddingModel.embedding_model_id == embedding_model_id
            )
        ).one_or_none()

    def delete(self, embedding_model_id: UUID) -> bool:
        """Delete an embedding model."""
        embedding_model = self.get_by_id(embedding_model_id)
        if not embedding_model:
            return False

        self.session.delete(embedding_model)
        self.session.commit()
        return True
