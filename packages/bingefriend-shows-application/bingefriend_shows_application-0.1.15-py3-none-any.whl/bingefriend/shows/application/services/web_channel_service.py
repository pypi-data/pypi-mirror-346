"""Service to interact with the web channel."""

from typing import Any
from sqlalchemy.orm import Session
from bingefriend.shows.application.repositories.web_channel_repo import WebChannelRepository
from bingefriend.shows.core.models import WebChannel


# noinspection PyMethodMayBeStatic
class WebChannelService:
    """Service to manage web channel-related operations."""

    def get_or_create_web_channel(self, web_channel_data: dict[str, Any], db: Session) -> WebChannel | None:
        """
        Get or create a web channel. If it exists, its data is updated. (This is now an upsert)

        Args:
            web_channel_data (dict): Data of the web channel to be created or fetched.
            db (Session): The database session to use.

        Returns:
            WebChannel | None: The web channel object if it exists or is created/updated, else None.
        """
        web_channel_repo: WebChannelRepository = WebChannelRepository()
        return web_channel_repo.upsert_web_channel(web_channel_data, db)
