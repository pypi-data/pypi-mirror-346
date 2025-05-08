"""Repository for network data."""

import logging
from typing import Any
from sqlalchemy import select, Select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy.dialects.mysql import insert as mysql_insert

from bingefriend.shows.core.models.network import Network


# noinspection PyMethodMayBeStatic
class NetworkRepository:
    """Repository for network data."""

    def get_network_by_maze_id(self, maze_id: int, db: Session) -> Network | None:
        """Get a network by its TV Maze ID.
        Args:
            maze_id (int): The TV Maze ID of the network.
            db (Session): The database session to use.
        Returns:
            Network | None: The network object if found, else None.
        """
        try:
            query: Select = select(Network).where(Network.maze_id == maze_id)
            return db.execute(query).scalars().first()
        except SQLAlchemyError as e:
            logging.error(f"Error fetching network by maze_id {maze_id}: {e}")
            return None

    def upsert_network(self, network_data: dict[str, Any], db: Session) -> Network | None:
        """
        Create a new network or update an existing one based on maze_id.
        Args:
            network_data (dict): Data of the network to be created or updated.
                                 Must include 'id' for maze_id.
            db (Session): The database session to use.
        Returns:
            Network | None: The created or updated network object if successful, else None.
        """
        maze_id = network_data.get('id')
        if not maze_id:
            logging.error("Cannot upsert network: 'id' (maze_id) is missing from network_data.")
            return None

        try:
            country_data = network_data.get('country') or {}
            insert_values = {
                'maze_id': maze_id,
                'name': network_data.get('name'),
                'country_name': country_data.get('name'),
                'country_code': country_data.get('code'),
                'country_timezone': country_data.get('timezone'),
            }

            update_on_conflict = {
                key: value for key, value in insert_values.items() if key != 'maze_id'
            }

            stmt = mysql_insert(Network).values(insert_values)
            stmt = stmt.on_duplicate_key_update(**update_on_conflict)

            db.execute(stmt)
            db.flush()

            logging.info(f"Network with maze_id {maze_id} upserted successfully.")

            db.expire_all()
            return self.get_network_by_maze_id(maze_id, db)

        except SQLAlchemyError as e:
            logging.error(f"Database error during upsert of network with maze_id {maze_id}: {e}")
            return None
        except Exception as e:
            logging.error(f"Unexpected error during upsert of network maze_id {maze_id}: {e}")
            return None
