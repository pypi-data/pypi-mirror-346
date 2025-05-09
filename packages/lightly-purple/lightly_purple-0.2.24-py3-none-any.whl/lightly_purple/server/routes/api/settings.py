"""This module contains the API routes for user settings."""

from fastapi import APIRouter, Depends
from sqlmodel import Session
from typing_extensions import Annotated

from lightly_purple.server.db import get_session
from lightly_purple.server.models.settings import SettingView
from lightly_purple.server.resolvers.settings import SettingsResolver

settings_router = APIRouter(tags=["settings"])

SessionDep = Annotated[Session, Depends(get_session)]


def get_settings_resolver(session: SessionDep) -> SettingsResolver:
    """Create an instance of the SettingsResolver."""
    return SettingsResolver(session)


@settings_router.get("/settings")
def get_settings(
    handler: Annotated[SettingsResolver, Depends(get_settings_resolver)],
) -> SettingView:
    """Get the current settings.

    Args:
        handler: Settings resolver instance for database operations.

    Returns:
        The current settings.
    """
    return handler.get_settings()


@settings_router.post("/settings")
def set_settings(
    settings: SettingView,
    handler: Annotated[SettingsResolver, Depends(get_settings_resolver)],
) -> SettingView:
    """Update user settings.

    Args:
        settings: New settings to apply.
        handler: Settings resolver instance for database operations.

    Returns:
        Updated settings.
    """
    return handler.set_settings(settings)
