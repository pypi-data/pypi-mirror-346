"""This module contains the resolvers for user settings."""

from sqlmodel import Session, select

from lightly_purple.server.models import Setting
from lightly_purple.server.models.settings import SettingView


class SettingsResolver:
    """Resolver for user settings."""

    def __init__(self, session: Session):
        """Initialize the resolver with a database session.

        Args:
            session: The database session.
        """
        self.session = session

    def get_settings(self) -> SettingView:
        """Get current settings.

        Returns:
            The current settings.
        """
        statement = select(Setting)
        result = self.session.exec(statement).first()

        # If no settings exist, create default settings
        if result is None:
            result = Setting()
            self.session.add(result)
            self.session.commit()
            self.session.refresh(result)

        return SettingView.model_validate(result)

    def set_settings(self, settings: SettingView) -> SettingView:
        """Update settings.

        Args:
            settings: New settings to apply.

        Returns:
            Updated settings.
        """
        current_settings = self.session.exec(select(Setting)).first()
        if current_settings is None:
            current_settings = Setting()
            self.session.add(current_settings)

        # Update grid view sample rendering
        if settings.grid_view_sample_rendering is not None:
            current_settings.grid_view_sample_rendering = (
                settings.grid_view_sample_rendering
            )

        # Update keyboard shortcut mapping
        if settings.keyboard_shortcut_mapping is not None:
            current_settings.keyboard_shortcut_mapping = (
                settings.keyboard_shortcut_mapping
            )

        self.session.commit()
        self.session.refresh(current_settings)

        return SettingView.model_validate(current_settings)
