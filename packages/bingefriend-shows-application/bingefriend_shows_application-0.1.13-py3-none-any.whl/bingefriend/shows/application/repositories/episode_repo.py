"""Repository for managing episodes in the database."""
import logging
from typing import Any, Dict
from sqlalchemy import select, Select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy.dialects.mysql import insert as mysql_insert
from bingefriend.shows.core.models.episode import Episode


# noinspection PyMethodMayBeStatic
class EpisodeRepository:
    """Repository for managing episodes in the database."""

    def upsert_episode(self, episode_data: Dict[str, Any], db: Session) -> Episode | None:
        """
        Create a new episode or update an existing one based on its TVMaze ID (maze_id).

        Args:
            episode_data (Dict[str, Any]): A dictionary containing episode data.
                                           Expected keys include 'id' (for maze_id),
                                           'show_id', 'season_id', and other episode attributes.
                                           'airstamp' should be a datetime object if processed by service.
            db (Session): The database session to use.

        Returns:
            Episode | None: The created or updated episode object, or None on error.
        """
        maze_id = episode_data.get("id")
        if not maze_id:
            logging.error("Cannot upsert episode: 'id' (maze_id) is missing from episode_data.")
            return None

        try:
            image_data = episode_data.get("image") or {}

            insert_values = {
                'maze_id': maze_id,
                'name': episode_data.get("name"),
                'number': episode_data.get("number"),
                'type': episode_data.get("type"),
                'airdate': episode_data.get("airdate"),
                'airtime': episode_data.get("airtime"),
                'airstamp': episode_data.get("airstamp"),
                'runtime': episode_data.get("runtime"),
                'image_medium': image_data.get("medium"),
                'image_original': image_data.get("original"),
                'summary': episode_data.get("summary"),
                'season_id': episode_data.get("season_id"),
                'show_id': episode_data.get("show_id")
            }

            update_on_conflict = {
                key: value for key, value in insert_values.items() if key != 'maze_id'
            }

            stmt = mysql_insert(Episode).values(insert_values)
            stmt = stmt.on_duplicate_key_update(**update_on_conflict)

            db.execute(stmt)
            db.flush()

            logging.info(f"Episode with maze_id {maze_id} upserted successfully.")

            db.expire_all()
            return self.get_episode_by_maze_id(maze_id, db)

        except SQLAlchemyError as e:
            logging.error(f"Database error during upsert of episode with maze_id {maze_id}: {e}")
            return None
        except Exception as e:
            logging.error(f"Unexpected error during upsert of episode with maze_id {maze_id}: {e}")
            return None

    def get_episode_by_maze_id(self, maze_id: int, db: Session) -> Episode | None:
        """Get an episode by its TVMaze ID. (Helper for re-fetching after upsert)"""
        try:
            query: Select = select(Episode).where(Episode.maze_id == maze_id)
            return db.execute(query).scalars().first()
        except SQLAlchemyError as e:
            logging.error(f"Error fetching episode by maze_id {maze_id}: {e}")
            return None
