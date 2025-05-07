"""Embedding manager for dataset processing."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from uuid import UUID

from sqlmodel import Session

from lightly_purple.dataset.embedding_generator import EmbeddingGenerator
from lightly_purple.server.models import (
    EmbeddingModel,
)
from lightly_purple.server.models.sample_embedding import SampleEmbeddingInput
from lightly_purple.server.resolvers.embedding_model import (
    EmbeddingModelResolver,
)
from lightly_purple.server.resolvers.sample import SampleResolver
from lightly_purple.server.resolvers.sample_embedding import (
    SampleEmbeddingResolver,
)


class EmbeddingManagerProvider:
    """Provider for the EmbeddingManager singleton instance."""

    _instance: EmbeddingManager | None = None

    @classmethod
    def get_embedding_manager(cls, session: Session | None) -> EmbeddingManager:
        """Get the singleton instance of EmbeddingManager.

        Args:
            session: A valid database session. Required if the instance is not
                     yet created.

        Returns:
            The singleton instance of EmbeddingManager.

        Raises:
            ValueError: If no instance exists and no session is provided.
        """
        if cls._instance is None:
            if session is None:
                raise ValueError(
                    "A valid session is required to create an EmbeddingManager."
                )
            cls._instance = EmbeddingManager(session)
        return cls._instance


@dataclass
class TextEmbedQuery:
    """Parameters for text embedding generation."""

    text: str
    embedding_model_id: UUID | None = None


class EmbeddingManager:
    """Manages embedding models and handles embedding generation and storage."""

    def __init__(
        self,
        session: Session,
    ) -> None:
        """Initialize the embedding manager.

        Args:
            session: Database session for resolver operations.
        """
        self._embedding_model_resolver = EmbeddingModelResolver(session)
        self._sample_embedding_resolver = SampleEmbeddingResolver(session)
        self._sample_resolver = SampleResolver(session)
        self._models: dict[UUID, EmbeddingGenerator] = {}
        self._default_model_id: UUID | None = None

    def register_embedding_model(
        self,
        dataset_id: UUID,
        embedding_generator: EmbeddingGenerator,
        set_as_default: bool = False,
    ) -> EmbeddingModel:
        """Register an embedding model in the database.

        The model is stored in an internal dictionary for later use.
        The model is set as default if requested or if it's the first model.

        Args:
            dataset_id: The ID of the dataset to associate with the model.
            embedding_generator: The model implementation used for embeddings.
            set_as_default: Whether to set this model as the default.

        Returns:
            The created EmbeddingModel.
        """
        # Create embedding model record in the database.
        created_model = self._embedding_model_resolver.create(
            embedding_generator.get_embedding_model_input(dataset_id=dataset_id)
        )
        model_id = created_model.embedding_model_id

        # Store the model in our dictionary
        self._models[model_id] = embedding_generator

        # Set as default if requested or if it's the first model
        if set_as_default or self._default_model_id is None:
            self._default_model_id = model_id

        return created_model

    def embed_text(self, text_query: TextEmbedQuery) -> list[float]:
        """Generate an embedding for a text sample.

        Args:
            text_query: Text embedding query containing text and model ID.

        Returns:
            A list of floats representing the generated embedding.
        """
        model_id = text_query.embedding_model_id or self._default_model_id
        if model_id is None:
            raise ValueError(
                "No embedding model specified and no default model set."
            )

        model = self._models.get(model_id)
        if model is None:
            raise ValueError(f"Embedding model with ID {model_id} not found.")

        return model.embed_text(text_query.text)

    def embed_images(
        self,
        sample_ids: list[UUID],
        embedding_model_id: UUID | None = None,
    ) -> None:
        """Generate and store embeddings for samples.

        Args:
            sample_ids: List of sample IDs to generate embeddings for.
            embedding_model_id: ID of the model to use. Uses default if None.

        Raises:
            ValueError: If no embedding model is registered or provided model
            ID doesn't exist.
        """
        model_id = embedding_model_id or self._default_model_id
        if not model_id:
            raise ValueError("No default embedding model registered.")

        if model_id not in self._models:
            raise ValueError(f"No embedding model found with ID {model_id}")

        # Query image filenames from the database.
        sample_id_to_filepath = {
            sample.sample_id: Path(sample.file_path_abs)
            for sample in self._sample_resolver.get_many_by_id(
                sample_ids=sample_ids
            )
        }

        # Extract filepaths in the same order as sample_ids.
        filepaths = [
            sample_id_to_filepath[sample_id] for sample_id in sample_ids
        ]

        # Generate embeddings for the samples.
        embeddings = self._models[model_id].embed_images(filepaths=filepaths)

        # Convert to SampleEmbeddingInput objects.
        sample_embeddings = [
            SampleEmbeddingInput(
                sample_id=sample_id,
                embedding_model_id=model_id,
                embedding=embedding,
            )
            for sample_id, embedding in zip(sample_ids, embeddings)
        ]

        # Store the embeddings in the database.
        self._sample_embedding_resolver.create_many(sample_embeddings)
