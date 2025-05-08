"""Repository for managing shows."""
import logging
from typing import Any
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy.dialects.mysql import insert as mysql_insert
from bingefriend.shows.core.models.show import Show


# noinspection PyMethodMayBeStatic
class ShowRepository:
    """Repository for managing shows."""

    def get_show_by_maze_id(self, maze_id: int, db: Session) -> Show | None:
        """Get a show by its TV Maze ID.
        Args:
            maze_id (int): The ID of the show in TV Maze.
            db (Session): The database session to use.
        Returns:
            Show | None: The show object if found, else None.
        """
        try:
            return db.query(Show).filter(Show.maze_id == maze_id).first()
        except SQLAlchemyError as e:
            logging.error(f"Error fetching show by maze_id {maze_id}: {e}")
            return None

    def upsert_show(self, show_data: dict[str, Any], db: Session) -> Show | None:
        """
        Create a new show or update an existing one based on maze_id
        using MySQL's INSERT ... ON DUPLICATE KEY UPDATE.

        Args:
            show_data (dict): Data of the show to be created or updated.
                               Must include 'id' for maze_id.
            db (Session): The database session to use.

        Returns:
            Show | None: The created or updated show object if successful (re-fetched), else None.
        """
        maze_id = show_data.get('id')
        if not maze_id:
            logging.error("Cannot upsert show: 'id' (maze_id) is missing from show_data.")
            return None

        try:
            schedule_data = show_data.get('schedule') or {}
            image_data = show_data.get('image') or {}
            externals_data = show_data.get('externals') or {}

            insert_values = {
                'maze_id': maze_id,
                'name': show_data.get('name'),
                'type': show_data.get('type'),
                'language': show_data.get('language'),
                'status': show_data.get('status'),
                'runtime': show_data.get('runtime'),
                'averageRuntime': show_data.get('averageRuntime'),
                'premiered': show_data.get('premiered'),
                'ended': show_data.get('ended'),
                'schedule_time': schedule_data.get('time'),
                'schedule_days': ",".join(schedule_data.get('days', [])),
                'network_id': show_data.get('network_id'),
                'webChannel_id': show_data.get('webChannel_id'),
                'externals_imdb': externals_data.get('imdb'),
                'image_medium': image_data.get('medium'),
                'image_original': image_data.get('original'),
                'summary': show_data.get('summary'),
                'updated': show_data.get('updated')
            }

            update_values = {
                key: value for key, value in insert_values.items() if key != 'maze_id'
            }

            stmt = mysql_insert(Show).values(insert_values)
            stmt = stmt.on_duplicate_key_update(**update_values)

            db.execute(stmt)
            db.flush()

            logging.info(f"Show with maze_id {maze_id} upserted successfully.")

            db.expire_all()
            show = self.get_show_by_maze_id(maze_id, db)
            return show

        except SQLAlchemyError as e:
            logging.error(f"Database error during upsert of show with maze_id {maze_id}: {e}")
            return None
        except Exception as e:
            logging.error(f"Unexpected error during upsert of show with maze_id {maze_id}: {e}")
            return None
