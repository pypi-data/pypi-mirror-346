"""Service to manage season-related operations."""

from typing import Any, Dict, List
from sqlalchemy.orm import Session
from bingefriend.shows.application.services.network_service import NetworkService
from bingefriend.shows.application.services.web_channel_service import WebChannelService
from bingefriend.shows.application.repositories.season_repo import SeasonRepository
from bingefriend.shows.core.models import Network, WebChannel, Season
from bingefriend.shows.client_tvmaze.tvmaze_api import TVMazeAPI
import logging


# noinspection PyMethodMayBeStatic
class SeasonService:
    """Service to handle season-related operations."""

    def fetch_season_index_page(self, show_id: int) -> List[Dict[str, Any]] | None:
        """Fetch a page of seasons for a given show_id from the external API.

        Args:
            show_id (int): The ID of the show to fetch seasons for.

        Returns:
            List[Dict[str, Any]] | None: A list of dictionaries containing season data, or None on error/no data.
        """
        try:
            tvmaze_api: TVMazeAPI = TVMazeAPI()
            seasons: List[Dict[str, Any]] | None = tvmaze_api.get_seasons(show_id)
            if seasons is None:
                logging.info(f"No seasons data returned from API for show_id {show_id} (possibly 404).")
                return None
            if not seasons:
                logging.info(f"Empty season list returned from API for show_id {show_id}.")
                return []
            return seasons
        except Exception as e:
            logging.error(f"Error fetching seasons for show_id {show_id} from TVMaze API: {e}")
            return None

    def process_season_record(self, season_data: Dict[str, Any], show_id: int, db: Session) -> Season | None:
        """
        Process a single season record: clean data, resolve related entities, and upsert.

        Args:
            season_data (Dict[str, Any]): The season record to process.
            show_id (int): The ID of the show to associate with the season.
            db (Session): The database session to use.

        Returns:
            Season | None: The processed (upserted) Season object, or None on error.
        """
        if not season_data or not show_id:
            logging.warning("Invalid season_data or show_id provided to process_season_record.")
            return None

        season_data["show_id"]: int = show_id

        for key in ['premiereDate', 'endDate']:
            if season_data.get(key) == "":
                season_data[key] = None

        network_info: Dict[str, Any] | None = season_data.get("network")
        if network_info:
            network_service: NetworkService = NetworkService()
            network: Network | None = network_service.get_or_create_network(network_info, db)
            season_data["network_id"]: int | None = network.id if network else None
        else:
            season_data["network_id"] = None

        web_channel_info: Dict[str, Any] | None = season_data.get("webChannel")
        if web_channel_info:
            web_channel_service: WebChannelService = WebChannelService()
            web_channel: WebChannel | None = web_channel_service.get_or_create_web_channel(web_channel_info, db)
            season_data["web_channel_id"]: int | None = web_channel.id if web_channel else None
        else:
            season_data["web_channel_id"] = None

        season_repo: SeasonRepository = SeasonRepository()
        processed_season: Season | None = season_repo.upsert_season(season_data, db)

        return processed_season

    def get_season_by_show_id_and_season_number(self, show_id: int, season_number: int, db: Session) -> Season | None:
        """Get the season object for a given show ID and season number.

        Args:
            show_id (int): The ID of the show.
            season_number (int): The season number.
            db (Session): The database session to use.

        Returns:
            Season | None: The season object if found, otherwise None.
        """
        season_repo = SeasonRepository()
        season: Season | None = season_repo.get_season_by_show_id_and_season_number(show_id, season_number, db)
        return season
