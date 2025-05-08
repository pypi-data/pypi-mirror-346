"""Service to manage show-genre associations."""

import logging  # Add logging
from typing import List, Set  # For type hinting
from sqlalchemy.orm import Session

from bingefriend.shows.application.repositories.show_genre_repo import ShowGenreRepository
from bingefriend.shows.core.models import ShowGenre


# noinspection PyMethodMayBeStatic
class ShowGenreService:
    """Service to manage show-genre associations effectively."""

    def sync_show_genres(self, show_id: int, new_api_genre_ids: List[int], db: Session) -> None:
        """
        Synchronizes the genres for a given show with a new list of genre IDs.
        Adds missing associations and removes outdated ones.

        Args:
            show_id (int): The ID of the show.
            new_api_genre_ids (List[int]): A list of all current genre IDs for the show from the API.
            db (Session): The database session to use.
        """
        if not show_id:
            logging.warning("show_id not provided for genre synchronization.")
            return

        show_genre_repo: ShowGenreRepository = ShowGenreRepository()

        # 1. Get current genre IDs linked to the show from the DB
        current_db_genre_ids: Set[int] = set(show_genre_repo.get_genre_ids_for_show(show_id, db))
        new_api_genre_ids_set: Set[int] = set(new_api_genre_ids)

        # 2. Determine genres to add: present in new API list but not in DB
        genres_to_add: Set[int] = new_api_genre_ids_set - current_db_genre_ids
        added_count = 0
        for genre_id_to_add in genres_to_add:
            # Use the more atomic ensure_show_genre_link_exists
            if show_genre_repo.ensure_show_genre_link_exists(show_id, genre_id_to_add, db):
                added_count += 1
            else:
                logging.error(f"Failed to ensure link for show_id {show_id}, genre_id {genre_id_to_add}")

        # 3. Determine genres to remove: present in DB but not in new API list
        genres_to_remove: Set[int] = current_db_genre_ids - new_api_genre_ids_set
        removed_count = 0
        for genre_id_to_remove in genres_to_remove:
            if show_genre_repo.remove_show_genre(show_id, genre_id_to_remove, db):
                removed_count += 1
            else:
                logging.warning(f"Failed to remove or find link for show_id {show_id}, genre_id {genre_id_to_remove}")

        if genres_to_add or genres_to_remove:
            logging.info(
                f"Synced genres for show_id {show_id}. Links ensured/created: {added_count} (attempted "
                f"{len(genres_to_add)}). Links removed: {removed_count} (attempted {len(genres_to_remove)})."
            )
        else:
            logging.debug(f"No genre changes for show_id {show_id}.")

    # The original create_show_genre from the service might still be useful
    # if you have use cases to add a single link explicitly and want the ShowGenre object back.
    # However, for synchronization, sync_show_genres is more comprehensive.
    # If using ensure_show_genre_link_exists in sync, the service method below
    # might just call that.
    def add_show_genre_link(self, show_id: int, genre_id: int, db: Session) -> ShowGenre | None:
        """
        Ensures a single show-genre link exists, returning the ShowGenre object.
        This uses the repository's atomic "ensure" method.
        """
        if not show_id or not genre_id:
            logging.warning("show_id and genre_id must be provided to add link.")
            return None

        show_genre_repo: ShowGenreRepository = ShowGenreRepository()
        # ensure_show_genre_link_exists returns the ShowGenre object or None
        return show_genre_repo.ensure_show_genre_link_exists(show_id, genre_id, db)
