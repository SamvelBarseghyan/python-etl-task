from typing import List, Dict


class Matches:
    def __init__(self):
        ...

    @staticmethod
    def get_player_info(match_info: Dict):
        return match_info["players"]


class RecentMatches:
    def __init__(self, recent_matches: List[Dict]):
        self.total_games = len(recent_matches)
        self.recent_matches = []
