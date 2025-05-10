"""Repository for genre data."""

import logging
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy.dialects.mysql import insert as mysql_insert
from sqlalchemy import select

from bingefriend.shows.core.models.genre import Genre


# noinspection PyMethodMayBeStatic
class GenreRepository:
    """Repository for genre data."""

    def get_genre_by_name(self, name: str, db: Session) -> Genre | None:
        """Get a genre by its name.

        Args:
            name (str): The name of the genre.
            db (Session): The database session to use.

        Returns:
            Genre | None: The genre object if found, otherwise None.
        """
        try:
            stmt = select(Genre).where(Genre.name == name)
            return db.execute(stmt).scalars().first()
        except SQLAlchemyError as e:
            logging.error(f"Error fetching genre by name '{name}': {e}")
            return None

    def upsert_genre(self, name: str, db: Session) -> Genre | None:
        """
        Get an existing genre by name, or create it if it doesn't exist.
        If the Genre model had other fields, this would update them.

        Args:
            name (str): The name of the genre.
            db (Session): The database session to use.

        Returns:
            Genre | None: The genre object if found/created, else None.
        """
        if not name or not isinstance(name, str) or name.strip() == "":
            logging.warning("Cannot upsert genre: name is invalid.")
            return None

        try:
            insert_values = {
                'name': name.strip()
            }

            stmt = mysql_insert(Genre).values(insert_values)

            stmt = stmt.on_duplicate_key_update(
                name=stmt.inserted.name
            )

            db.execute(stmt)
            db.flush()

            logging.info(f"Genre '{name}' upserted successfully.")

            db.expire_all()
            return self.get_genre_by_name(name.strip(), db)

        except SQLAlchemyError as e:
            logging.error(f"Database error during upsert of genre '{name}': {e}")
            return None
        except Exception as e:
            logging.error(f"Unexpected error during upsert of genre '{name}': {e}")
            return None
