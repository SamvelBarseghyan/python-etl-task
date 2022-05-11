import os
import json
import requests
from typing import List, Dict
from functools import lru_cache
from src.entity import PlayerInfo
from src.config import config_by_name
from src.dto import QueryParams, ResponseContent
from src.exception import *

config_type = os.getenv("CONFIG_TYPE", "dev")
settings = config_by_name[config_type]()


class DataManipulation:

    def __call__(self, query_params: QueryParams) -> ResponseContent:
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
    @lru_cache(maxsize=10)
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
        recent_matches_api_response = requests.get(
            settings.recent_matches_api.format(account_id)
        )

        recent_matches = json.loads(recent_matches_api_response.content)
        if not recent_matches:
            err_msg = f"Matches for account: {account_id} not found."
            raise EmptyRecentMatchesException(err_msg)

        return recent_matches

    def get_player_info(self, query_params: QueryParams) -> PlayerInfo:
        """
        Function will parse list with recent matches info and
            will create PlayerInfo object that will have all
            needed data about matches
        :type query_params: QueryParams
        :param query_params:
        :rtype: PlayerInfo
        :return:
        """
        recent_matches = self.get_recent_matches(query_params.account_id)
        if query_params.count > len(recent_matches):
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
    @lru_cache(maxsize=10)
    def get_match_detailed_info(match_id: int) -> Dict:
        """

        :type match_id: int
        :param match_id:
        :rtype: Dict
        :return:
        """
        match_info_api_response = requests.get(
            settings.match_info_api.format(match_id)
        )
        detailed_match_info = json.loads(match_info_api_response.content)
        if not detailed_match_info:
            err_msg = ""
            raise MissingMatchInfoException(err_msg, match_id)

        return detailed_match_info
