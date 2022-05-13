import sys
import json
import logging
import requests
from src.exception import *
from typing import List, Dict
from src.config import settings
from functools import lru_cache
from src.entity import PlayerInfo
from src.dto import QueryParams, ResponseContent

log = logging.getLogger(__name__)


class DataManipulation:

    def __call__(self, query_params: QueryParams) -> ResponseContent:
        """
        Function prepares response
        :type query_params: QueryParams
        :param query_params: query parameters from request
        :rtype: ResponseContent
        :return: Returns object that contains all the data
                    needed to construct response
        """
        player_info = self.get_player_info(query_params)
        response = ResponseContent(
            player_name=player_info.name,
            total_games=player_info.total_games,
            min_kda=player_info.recent_matches.min_kda,
            avg_kda=player_info.recent_matches.avg_kda,
            max_kda=player_info.recent_matches.max_kda,
            min_kp=player_info.recent_matches.min_kp,
            avg_kp=player_info.recent_matches.avg_kp,
            max_kp=player_info.recent_matches.max_kp,
        )
        return response

    @staticmethod
    @lru_cache(maxsize=settings.cache_size)
    def get_recent_matches(account_id: int) -> List[Dict]:
        """
        Function get list of the recent matches for account id sent
            in request as query param

        :type account_id: string
        :param account_id: ID of the account that will be used to
                            get matches info
        :rtype: List[Dict]
        :return: list of dicts that contains data about matches
        :raises:
            :exception EmptyRecentMatchesException:
                if current user don't have recent matches
        """
        log.info(f"To get list of recent matches of the player: {account_id} "
                 f"will be used API: "
                 f"{settings.recent_matches_api.format(account_id)}")
        recent_matches_api_response = requests.get(
            settings.recent_matches_api.format(account_id)
        )

        recent_matches = json.loads(recent_matches_api_response.content)
        if not recent_matches:
            err_msg = f"Matches for account: {account_id} not found."
            raise EmptyRecentMatchesException(err_msg, account_id)
        log.info(f"Data about recent matches of the player: {account_id} "
                 f"was successfully parsed.")
        log.debug(recent_matches)
        return recent_matches

    def get_player_info(self, query_params: QueryParams) -> PlayerInfo:
        """
        Function will parse list with recent matches info and
            will create PlayerInfo object that will have all
            needed data about matches, calculated KDA/KP
        :type query_params: QueryParams
        :param query_params:
        :rtype: PlayerInfo
        :return: Returns object of PlayerInfo with all needed/calculated data
        """
        recent_matches = self.get_recent_matches(query_params.account_id)
        if query_params.count > len(recent_matches):
            log.info("Count of the recent matches requested by client "
                     "for which KDA/KP should be calculated was changed "
                     "because user's total game count less than requested one")
            query_params.count = len(recent_matches)
        recent_matches_info = list(
            map(
                lambda x: self.get_match_detailed_info(x["match_id"]),
                recent_matches[:query_params.count]
            )
        )
        return PlayerInfo(
            query_params.account_id,
            query_params.name,
            recent_matches_info,
            len(recent_matches)
        )

    @staticmethod
    @lru_cache(maxsize=settings.cache_size)
    def get_match_detailed_info(match_id: int) -> Dict:
        """

        :type match_id: int
        :param match_id: id of the match for which need to get detailed date
        :rtype: Dict
        :return: Detailed data of the match
        :raises:
            :exception: MissingMatchInfoException:
                if data for the match not found/is empty
        """
        log.info(f"To get match info for match: {match_id} will be used API:"
                 f"{settings.match_info_api.format(match_id)}")

        match_info_api_response = requests.get(
            settings.match_info_api.format(match_id)
        )
        detailed_match_info = json.loads(match_info_api_response.content)
        if not detailed_match_info:
            err_msg = f"Missing: {match_id} not found."
            raise MissingMatchInfoException(err_msg, match_id)
        log.info(f"Match info for match: {match_id} was successfully parsed.")
        log.debug(detailed_match_info)
        return detailed_match_info
