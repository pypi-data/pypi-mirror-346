"""Repository for show-genre data."""

import logging
from typing import List
from sqlalchemy import select, delete, exc as sqlalchemy_exc, and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy.dialects.mysql import insert as mysql_insert
from bingefriend.shows.core.models.show_genre import ShowGenre


# noinspection PyMethodMayBeStatic
class ShowGenreRepository:
    """Repository for show-genre data associations."""

    def ensure_show_genre_link_exists(self, show_id: int, genre_id: int,
                                      db: Session) -> ShowGenre | None:
        """
        Ensures a show-genre link exists, creating it if necessary using an atomic operation.
        Returns the ShowGenre object if the link exists or was successfully created.
        """
        if not show_id or not genre_id:
            logging.warning("show_id and genre_id must be provided to ensure link.")
            return None

        try:
            stmt = mysql_insert(ShowGenre).values(show_id=show_id, genre_id=genre_id)
            stmt = stmt.on_duplicate_key_update(genre_id=stmt.inserted.genre_id)
            db.execute(stmt)

            get_stmt = select(ShowGenre).where(
                and_(ShowGenre.show_id == show_id, ShowGenre.genre_id == genre_id)
            )
            show_genre_instance = db.execute(get_stmt).scalars().first()

            if show_genre_instance:
                logging.debug(
                    f"Show-genre link ensured for show_id {show_id} and genre_id {genre_id} (ID: "
                    f"{show_genre_instance.id})"
                )
            else:
                logging.warning(
                    f"Show-genre link for show_id {show_id} and genre_id {genre_id} not found after upsert attempt.")

            return show_genre_instance

        except SQLAlchemyError as e:
            logging.error(
                f"Database error with ensure_show_genre_link_exists for show_id {show_id}, genre_id {genre_id}: {e}"
            )
            return None
        except Exception as e:
            logging.error(
                f"Unexpected error in ensure_show_genre_link_exists for show_id {show_id}, genre_id {genre_id}: {e}"
            )
            return None

    def get_genre_ids_for_show(self, show_id: int, db: Session) -> List[int]:
        """
        Fetches all genre_ids currently linked to a given show_id.

        Args:
            show_id (int): The ID of the show.
            db (Session): The database session to use.

        Returns:
            List[int]: A list of genre IDs associated with the show.
        """
        if not isinstance(show_id, int):
            logging.warning("Invalid show_id for get_genre_ids_for_show.")
            return []
        try:
            stmt = select(ShowGenre.genre_id).where(ShowGenre.show_id == show_id)
            result = db.execute(stmt).scalars().all()
            return list(result)
        except sqlalchemy_exc.SQLAlchemyError as e:
            logging.error(f"SQLAlchemyError fetching genre_ids for show_id {show_id}: {e}")
            return []
        except Exception as e:
            logging.error(f"Unexpected error fetching genre_ids for show_id {show_id}: {e}")
            return []

    def remove_show_genre(self, show_id: int, genre_id: int, db: Session) -> bool:
        """
        Deletes a specific show-genre link.

        Args:
            show_id (int): The ID of the show.
            genre_id (int): The ID of the genre.
            db (Session): The database session to use.

        Returns:
            bool: True if the link was successfully deleted, False otherwise.
        """
        if not all([isinstance(show_id, int), isinstance(genre_id, int)]):
            logging.warning("Invalid show_id or genre_id for remove_show_genre.")
            return False
        try:
            stmt = delete(ShowGenre).where(
                ShowGenre.show_id == show_id,
                ShowGenre.genre_id == genre_id
            )
            result = db.execute(stmt)
            db.flush()

            # noinspection PyTypeChecker
            if result.rowcount is not None and result.rowcount > 0:
                logging.info(f"Removed genre_id {genre_id} from show_id {show_id}")
                return True
            logging.debug(f"No link found to remove for show_id {show_id}, genre_id {genre_id}")
            return False
        except sqlalchemy_exc.SQLAlchemyError as e:
            logging.error(f"SQLAlchemyError removing show_genre for show_id {show_id}, genre_id {genre_id}: {e}")
            return False
        except Exception as e:
            logging.error(f"Unexpected error removing show_genre for show_id {show_id}, genre_id {genre_id}: {e}")
            return False

    def create_show_genre_with_integrity_check(self, show_id: int, genre_id: int, db: Session) -> ShowGenre | None:
        """
        Create a new show-genre entry in the database, handling IntegrityError.
        This is the original approach.

        Args:
            show_id (int): The ID of the show.
            genre_id (int): The ID of the genre.
            db (Session): The database session to use.

        Returns:
            ShowGenre | None: The created show-genre object if successful,
                              None if it already exists or on other error.
        """
        # noinspection PyUnusedLocal
        show_genre: ShowGenre | None = None
        if not all([isinstance(show_id, int), isinstance(genre_id, int)]):
            logging.warning("Invalid show_id or genre_id for create_show_genre_with_integrity_check.")
            return None
        try:
            show_genre = ShowGenre(show_id=show_id, genre_id=genre_id)
            db.add(show_genre)
            db.flush()
            logging.info(f"Show-genre created with (PK ID {show_genre.id}) for show {show_id}, genre {genre_id}")
            return show_genre
        except sqlalchemy_exc.IntegrityError as e:
            logging.warning(
                f"Show-genre link already exists for show_id {show_id} and genre_id {genre_id} (IntegrityError): {e}"
            )
            stmt = select(ShowGenre).where(ShowGenre.show_id == show_id, ShowGenre.genre_id == genre_id)
            return db.execute(stmt).scalars().first()
        except sqlalchemy_exc.SQLAlchemyError as e:
            logging.error(
                f"SQLAlchemyError creating show-genre for show_id {show_id} and genre_id {genre_id}: {e}"
            )
            return None
        except Exception as e:
            logging.error(
                f"Unexpected error creating show-genre for show_id {show_id} and genre_id {genre_id}: {e}"
            )
            return None
