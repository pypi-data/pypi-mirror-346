"""Service to manage network-related operations."""

from typing import Any # Import Any
from sqlalchemy.orm import Session
from bingefriend.shows.application.repositories.network_repo import NetworkRepository
from bingefriend.shows.core.models import Network


# noinspection PyMethodMayBeStatic
class NetworkService:
    """Service to manage network-related operations."""

    def get_or_create_network(self, network_data: dict[str, Any], db: Session) -> Network | None:
        """
        Get or create a network. If it exists, its data is updated. (This is now an upsert)

        Args:
            network_data (dict): Data of the network. Must include 'id' for maze_id.
            db (Session): The database session to use.

        Returns:
            Network | None: The network object if found/created/updated, else None.
        """
        network_repo: NetworkRepository = NetworkRepository()
        return network_repo.upsert_network(network_data, db)
