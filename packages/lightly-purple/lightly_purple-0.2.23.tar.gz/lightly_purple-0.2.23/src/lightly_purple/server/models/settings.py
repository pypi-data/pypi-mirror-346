"""This module contains settings model for user preferences."""

from __future__ import annotations

import json
from datetime import datetime
from enum import Enum
from typing import Any  # Keep Any for compatibility
from uuid import UUID

from pydantic import field_validator
from sqlmodel import JSON, Column, Field, SQLModel


class GridViewSampleRenderingType(str, Enum):
    """Defines how samples are rendered in the grid view."""

    COVER = "cover"
    CONTAIN = "contain"


class KeyboardShortcutMapping(SQLModel):
    """Defines the keyboard shortcuts for the application."""

    hide_annotations: str = Field(
        default="v",
        description="Key to temporarily hide annotations while pressed",
    )
    go_back: str = Field(
        default="Escape",
        description="Key to navigate back from detail view to grid view",
    )


class SettingBase(SQLModel):
    """Base class for Settings model."""

    grid_view_sample_rendering: GridViewSampleRenderingType = Field(
        default=GridViewSampleRenderingType.CONTAIN,
        description="Controls how samples are rendered in the grid view",
    )

    # Store keyboard shortcut mapping as JSON
    keyboard_shortcut_mapping: KeyboardShortcutMapping | None = Field(
        default=None,
        sa_column=Column(JSON),
        description="Keyboard shortcut mappings for various actions",
    )

    @field_validator("keyboard_shortcut_mapping", mode="before")
    @classmethod
    def validate_keyboard_shortcuts(
        cls, value: KeyboardShortcutMapping | dict[str, Any] | str | None
    ) -> KeyboardShortcutMapping:
        """Validate and convert keyboard shortcuts to/from JSON format."""
        if value is None:
            return KeyboardShortcutMapping()
        if isinstance(value, KeyboardShortcutMapping):
            return value
        if isinstance(value, dict):
            return KeyboardShortcutMapping(**value)
        if isinstance(value, str):
            return KeyboardShortcutMapping(**json.loads(value))
        return KeyboardShortcutMapping()


class SettingView(SettingBase):
    """View class for Settings model."""

    setting_id: UUID
    created_at: datetime
    updated_at: datetime
