"""Repository for web channel data."""

import logging
from typing import Any
from sqlalchemy import select, Select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy.dialects.mysql import insert as mysql_insert
from bingefriend.shows.core.models.web_channel import WebChannel


# noinspection PyMethodMayBeStatic
class WebChannelRepository:
    """Repository to interact with web channel."""

    def get_web_channel_by_maze_id(self, maze_id: int, db: Session) -> WebChannel | None:
        """Get a web channel by its TV Maze ID.

        Args:
            maze_id (int): The ID of the web channel in TV Maze.
            db (Session): The database session to use.

        Returns:
            WebChannel | None: The web channel object if found, else None.
        """
        try:
            query: Select = select(WebChannel).where(WebChannel.maze_id == maze_id)
            return db.execute(query).scalars().first()
        except SQLAlchemyError as e:
            logging.error(f"Error fetching web channel by maze_id {maze_id}: {e}")
            return None

    def upsert_web_channel(self, web_channel_data: dict[str, Any], db: Session) -> WebChannel | None:
        """
        Create a new web channel or update an existing one based on maze_id.

        Args:
            web_channel_data (dict): Data of the web channel. Must include 'id' for maze_id.
            db (Session): The database session to use.

        Returns:
            WebChannel | None: The created or updated web channel object if successful, else None.
        """
        maze_id = web_channel_data.get('id')
        if not maze_id:
            logging.error("Cannot upsert web_channel: 'id' (maze_id) is missing from web_channel_data.")
            return None

        try:
            country_data = web_channel_data.get('country') or {}
            insert_values = {
                'maze_id': maze_id,
                'name': web_channel_data.get('name'),
                'country_name': country_data.get('name'),
                'country_code': country_data.get('code'),
                'country_timezone': country_data.get('timezone'),
                'official_site': web_channel_data.get('officialSite'),
            }

            update_on_conflict = {
                key: value for key, value in insert_values.items() if key != 'maze_id'
            }

            stmt = mysql_insert(WebChannel).values(insert_values)
            stmt = stmt.on_duplicate_key_update(**update_on_conflict)

            db.execute(stmt)
            db.flush()

            logging.info(f"WebChannel with maze_id {maze_id} upserted successfully.")

            db.expire_all()

            return self.get_web_channel_by_maze_id(maze_id, db)

        except SQLAlchemyError as e:
            logging.error(f"Database error during upsert of web_channel with maze_id {maze_id}: {e}")
            return None
        except Exception as e:
            logging.error(f"Unexpected error during upsert of web_channel maze_id {maze_id}: {e}")
            return None
