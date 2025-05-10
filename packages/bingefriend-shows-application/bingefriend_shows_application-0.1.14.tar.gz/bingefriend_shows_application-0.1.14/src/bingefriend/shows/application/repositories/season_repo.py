"""Repository for managing seasons in the database."""

import logging
from typing import Any, Dict
from sqlalchemy import Select, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy.dialects.mysql import insert as mysql_insert

from bingefriend.shows.core.models.season import Season


# noinspection PyMethodMayBeStatic
class SeasonRepository:
    """Repository to handle season-related database operations."""

    def upsert_season(self, season_data: Dict[str, Any], db: Session) -> Season | None:
        """
        Create a new season or update an existing one based on its TVMaze ID (maze_id).

        Args:
            season_data (Dict[str, Any]): A dictionary containing season data.
                                          Expected keys include 'id' (for maze_id), 'show_id',
                                          and other season attributes.
            db (Session): The database session to use.

        Returns:
            Season | None: The created or updated season object, or None on error.
        """
        maze_id = season_data.get("id")
        if not maze_id:
            logging.error("Cannot upsert season: 'id' (maze_id) is missing from season_data.")
            return None

        try:
            image_data = season_data.get("image") or {}

            insert_values = {
                'maze_id': maze_id,
                'number': season_data.get("number"),
                'name': season_data.get("name"),
                'episodeOrder': season_data.get("episodeOrder"),
                'premiereDate': season_data.get("premiereDate"),
                'endDate': season_data.get("endDate"),
                'network_id': season_data.get("network_id"),
                'webChannel_id': season_data.get("webChannel_id"),
                'image_medium': image_data.get("medium"),
                'image_original': image_data.get("original"),
                'summary': season_data.get("summary"),
                'show_id': season_data.get("show_id")
            }

            update_on_conflict = {
                key: value for key, value in insert_values.items() if key != 'maze_id'
            }

            stmt = mysql_insert(Season).values(insert_values)
            stmt = stmt.on_duplicate_key_update(**update_on_conflict)

            db.execute(stmt)
            db.flush()

            logging.info(f"Season with maze_id {maze_id} upserted successfully.")

            db.expire_all()
            return self.get_season_by_maze_id(maze_id, db)

        except SQLAlchemyError as e:
            logging.error(f"Database error during upsert of season with maze_id {maze_id}: {e}")
            return None
        except Exception as e:
            logging.error(f"Unexpected error during upsert of season with maze_id {maze_id}: {e}")
            return None

    def get_season_by_maze_id(self, maze_id: int, db: Session) -> Season | None:
        """Get a season by its TVMaze ID. (Helper for re-fetching after upsert)"""
        try:
            query: Select = select(Season).where(Season.maze_id == maze_id)
            return db.execute(query).scalars().first()
        except SQLAlchemyError as e:
            logging.error(f"Error fetching season by maze_id {maze_id}: {e}")
            return None

    def get_season_by_show_id_and_season_number(self, show_id: int, season_number: int, db: Session) -> Season | None:
        """Get the season object for a given show ID and season number.

        Args:
            show_id (int): The ID of the show.
            season_number (int): The season number.
            db (Session): The database session to use.

        Returns:
            Season | None: The season object if found, otherwise None.
        """
        try:
            query: Select = select(Season).filter(Season.show_id == show_id, Season.number == season_number)
            return db.execute(query).scalars().first()
        except SQLAlchemyError as e:
            logging.error(f"Error fetching season {season_number} for show_id {show_id}: {e}")
            return None
