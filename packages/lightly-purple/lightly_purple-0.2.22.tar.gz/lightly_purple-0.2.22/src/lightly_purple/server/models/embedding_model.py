"""This module defines the Embedding_Model model for the application."""

from __future__ import annotations

from uuid import UUID

from sqlmodel import CHAR, Column, Field, SQLModel


class EmbeddingModelBase(SQLModel):
    """Base class for the EmbeddingModel."""

    name: str
    parameter_count_in_mb: int | None = None
    embedding_model_hash: str | None = Field(
        default=None, sa_column=Column(CHAR(128))
    )
    embedding_dimension: int
    dataset_id: UUID = Field(default=None, foreign_key="datasets.dataset_id")


class EmbeddingModelInput(EmbeddingModelBase):
    """EmbeddingModel class when inserting."""
