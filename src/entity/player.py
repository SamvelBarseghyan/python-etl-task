import logging
from typing import List, Dict
from .matches import RecentMatches

log = logging.getLogger(__name__)


class PlayerInfo:
    def __init__(self, account_id: int, name: str,
                 recent_matches: List[Dict], total_games: int):
        """
        Constructor of the class: PlayerInfo
        :type account_id: int
        :param account_id: Account ID of the player
        :type name: str
        :param name: Name of the player
        :type recent_matches: RecentMatches
        :param recent_matches: Object that has all the data of recent
                                matches of the player
        :type total_games: int
        :param total_games: count of the matches that player was played
        """
        self.account_id = account_id
        self.name = name
        self.recent_matches = RecentMatches(recent_matches, account_id)
        self.total_games = total_games
        log.info("Info about the player successfully parsed/calculated.")
        log.debug(self.__dict__)
