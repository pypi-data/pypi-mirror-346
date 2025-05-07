"""This module defines the SampleEmbedding model for the application."""

from __future__ import annotations

from uuid import UUID

from sqlalchemy import ARRAY, Float
from sqlmodel import Column, Field, SQLModel


class EmbeddingBase(SQLModel):
    """Base class for the Embedding."""

    embedding_model_id: UUID = Field(
        foreign_key="embedding_models.embedding_model_id", primary_key=True
    )
    embedding: list[float] = Field(sa_column=Column(ARRAY(Float)))


class SampleEmbeddingBase(EmbeddingBase):
    """Base class for the Embeddings used for Samples."""

    sample_id: UUID = Field(foreign_key="samples.sample_id", primary_key=True)


class SampleEmbeddingInput(SampleEmbeddingBase):
    """Sample class when inserting."""
