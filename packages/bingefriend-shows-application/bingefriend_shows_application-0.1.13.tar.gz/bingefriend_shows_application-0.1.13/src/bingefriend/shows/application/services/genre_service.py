"""Service to manage genre-related operations."""

from sqlalchemy.orm import Session
from bingefriend.shows.application.repositories.genre_repo import GenreRepository
from bingefriend.shows.core.models import Genre


# noinspection PyMethodMayBeStatic
class GenreService:
    """Service to manage genre-related operations."""

    def get_or_create_genre(self, genre_name: str, db: Session) -> Genre | None:
        """Get or create a genre entry in the database.
        Args:
            genre_name (str): Name of the genre to be created or fetched.
            db (Session): The database session to use.

        Returns:
            Genre | None: The genre object if it exists or is created, else None.
        """
        genre_repo: GenreRepository = GenreRepository()
        return genre_repo.upsert_genre(genre_name, db)
