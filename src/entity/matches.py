from statistics import mean
from typing import Union, Tuple, List, Dict
from src.exception import EmptyPlayerInfoException


class Match:
    def __init__(self, match_info: Dict, account_id: int):
        """
        Constructor of the class: Match
        :type match_info: Dict
        :param match_info: Dict that contains data about match
        :type account_id: int
        :param account_id: Account ID of the player
        :raises:
            :exception EmptyPlayerInfoException:
                if player's account id not found in the
                list of players of current match
        """
        self.match_id: int = match_info["match_id"]

        players_info = self.get_player_info(match_info)
        curr_player = dict()
        for player in players_info:
            if account_id == player.get("account_id"):
                curr_player = player
                break
        if not curr_player:
            err_msg = f"Player: {account_id} not found in the list of " \
                      f"players of match {self.match_id}."
            raise EmptyPlayerInfoException(
                message=err_msg, account_id=account_id
            )
        self.assists: int = curr_player.get("assists", 0)
        self.deaths: int = curr_player.get("deaths") if curr_player.get(
            "deaths") else 1
        self.kills: int = curr_player.get("kills", 1)
        self.is_radiant: bool = curr_player.get("isRadiant")
        self.team_kills: int = self.get_team_kills(players_info,
                                                   self.is_radiant)
        self.kda: float = self.get_kda()
        self.kp: float = self.get_kp()

    @staticmethod
    def get_player_info(match_info: Dict) -> List[Dict]:
        """
        Function returns list of dicts. Each dict contains info about
            players that was played that match
        :type match_info: Dict
        :param match_info: data of the match
        :rtype: List[Dict]
        :return: return list of data of each player that played in the match
        """
        return match_info["players"]

    @staticmethod
    def get_team_kills(match_data: List[Dict], is_radiant: bool) -> int:
        """
        Function calculates kills for the team that player was played
        :type match_data: List[Dict]
        :param match_data: List of data of the players that played
                            current match
        :type is_radiant: bool
        :param is_radiant: True if the team of the player is Radiant
                            and False if team is Dire
        :rtype: int
        :return: count of team kills
        """
        team_kills = 0
        for player_info in match_data:
            if player_info["isRadiant"] == is_radiant:
                team_kills += player_info.get("kills", 0)
        return team_kills

    def get_kda(self) -> float:
        """
        Function calculates KDA - Kills/Deaths/Assists ratio of
            a player in current match
            Formula - (K + A) / D
        :rtype: float
        :return: KDA
        """
        return round((self.kills + self.assists) / self.deaths, 2)

    def get_kp(self) -> float:
        """
        Function calculates KP - Kill Participation of a player
            in the team
            Formula - (K + A) * 100 / TK
        :rtype: float
        :return: KP
        """
        kp = (self.kills + self.assists) * 100 / self.team_kills
        return round(kp, 2)


class RecentMatches:
    def __init__(self, recent_matches: List[Dict], account_id: int):
        """
        Constructor of the class: RecentMatches
        :type recent_matches: List[Dict]
        :param recent_matches: List of the dicts that contains info/data
                                about matches
        :type account_id: int
        :param account_id: Account ID of the player
        """
        self.recent_matches = [
            Match(match, account_id) for match in recent_matches
        ]
        self.min_kda, self.avg_kda, self.max_kda = \
            self.get_min_avg_max_of_list(True)
        self.min_kp, self.avg_kp, self.max_kp = \
            self.get_min_avg_max_of_list(False)

    def get_min_avg_max_of_list(self, is_kda_list: bool = False) \
            -> Union[Tuple[float], Tuple[str]]:
        """
        Function returns MIN, AVG and MAX values of the KDA/KP of matches
        :type is_kda_list: bool
        :param is_kda_list:
        :rtype: Union[Tuple[float], Tuple[str]]
        :return:
        """
        kpi_type = "kda" if is_kda_list else "kp"
        list_of_kpi_values = [
            getattr(match, kpi_type) for match in self.recent_matches
        ]
        kpi_values = (
            round(min(list_of_kpi_values), 2),
            round(mean(list_of_kpi_values), 2),
            round(max(list_of_kpi_values), 2)
        )
        if not is_kda_list:
            kpi_values = tuple(map(lambda x: str(x) + '%', kpi_values))
        return kpi_values
