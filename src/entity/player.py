from typing import List, Dict
from .matches import RecentMatches


class PlayerInfo:
    def __init__(self, account_id: int, name: str,
                 recent_matches: List[Dict], total_games: int):
        """
        Constructor of the class: PlayerInfo
        :param account_id:
        :param name:
        :param recent_matches:
        :param total_games:
        """
        self.account_id = account_id
        self.name = name
        self.recent_matches = RecentMatches(recent_matches, account_id)
        self.total_games = total_games
