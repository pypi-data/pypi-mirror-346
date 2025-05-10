"""Service for episode-related operations."""

import logging
from datetime import datetime
from typing import Any, Dict, List
from sqlalchemy.orm import Session
from bingefriend.shows.core.models import Episode, Season
from bingefriend.shows.client_tvmaze.tvmaze_api import TVMazeAPI
from bingefriend.shows.application.repositories.episode_repo import EpisodeRepository
from bingefriend.shows.application.services.season_service import SeasonService


# noinspection PyMethodMayBeStatic
class EpisodeService:
    """Service for episode-related operations."""

    def fetch_episode_index_page(self, show_id: int) -> List[Dict[str, Any]] | None:
        """Fetch all episodes for a given show_id from the external API.

        Args:
            show_id (int): The ID of the show to fetch episodes for.

        Returns:
            List[Dict[str, Any]] | None: A list of episode data, or None if an error occurs or API returns no data.
        """
        try:
            tvmaze_api = TVMazeAPI()
            show_episodes: List[Dict[str, Any]] | None = tvmaze_api.get_episodes(show_id)

            if show_episodes is None:
                logging.info(f"API returned no episode data for show ID {show_id} (possibly 404 or no episodes).")
                return None

            if not show_episodes:
                logging.info(f"No episodes found for show ID {show_id} (empty list from API).")
                return []

            logging.info(f"Retrieved {len(show_episodes)} episodes for show ID {show_id}.")
            return show_episodes

        except Exception as e:
            logging.exception(f"Error retrieving episode index page for show ID {show_id}: {e}")
            return None

    def process_episode_record(self, episode_data: Dict[str, Any], show_id: int, db: Session) -> Episode | None:
        """
        Process a single episode record: clean data, resolve related entities, and upsert.

        Args:
            episode_data (Dict[str, Any]): The episode record to process.
            show_id (int): The ID of the show to associate with the episode.
            db (Session): The database session to use.

        Returns:
            Episode | None: The processed (upserted) Episode object, or None on error.
        """
        if not episode_data or not show_id:
            logging.warning("Invalid episode_data or show_id provided to process_episode_record.")
            return None

        episode_data["show_id"] = show_id

        for key in ['type', 'airdate', 'airtime']:
            if episode_data.get(key) == '':
                episode_data[key] = None

        if episode_data.get('summary') == '':
            episode_data['summary'] = None

        airstamp_str = episode_data.get('airstamp')
        parsed_airstamp: datetime | None = None
        if airstamp_str:
            try:
                parsed_airstamp = datetime.fromisoformat(airstamp_str)
            except (ValueError, TypeError) as e:
                logging.warning(
                    f"Could not parse airstamp '{airstamp_str}' for episode_id {episode_data.get('id')}: {e}")
        episode_data['airstamp'] = parsed_airstamp

        season_number: int | None = episode_data.get("season")
        if season_number is not None:
            season_service = SeasonService()
            season: Season | None = season_service.get_season_by_show_id_and_season_number(show_id, season_number, db)
            if season and season.id is not None:
                episode_data["season_id"] = season.id
            else:
                logging.warning(f"Could not find or get ID for season number {season_number} of show_id {show_id} "
                                f"while processing episode_id {episode_data.get('id')}. Setting season_id to None.")
                episode_data["season_id"] = None
        else:
            logging.warning(f"Season number not provided in episode_data for episode_id {episode_data.get('id')}. "
                            f"Setting season_id to None.")
            episode_data["season_id"] = None

        episode_repo = EpisodeRepository()
        processed_episode: Episode | None = episode_repo.upsert_episode(episode_data, db)

        return processed_episode
