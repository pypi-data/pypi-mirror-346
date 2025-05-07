"""Handler for database operations related to sample embeddings."""

from __future__ import annotations

from sqlmodel import Session

from lightly_purple.server.models import SampleEmbedding
from lightly_purple.server.models.sample_embedding import SampleEmbeddingInput


class SampleEmbeddingResolver:
    """Resolver for the sample embedding model."""

    def __init__(self, session: Session):
        """Initializes the SampleEmbeddingResolver."""
        self.session = session

    def create(self, sample_embedding: SampleEmbeddingInput) -> SampleEmbedding:
        """Create a new SampleEmbedding in the database."""
        db_sample_embedding = SampleEmbedding.model_validate(sample_embedding)
        self.session.add(db_sample_embedding)
        self.session.commit()
        self.session.refresh(db_sample_embedding)
        return db_sample_embedding

    def create_many(
        self, sample_embeddings: list[SampleEmbeddingInput]
    ) -> None:
        """Create many sample embeddings in a single database commit."""
        db_sample_embeddings = [
            SampleEmbedding.model_validate(e) for e in sample_embeddings
        ]
        self.session.bulk_save_objects(db_sample_embeddings)
        self.session.commit()
