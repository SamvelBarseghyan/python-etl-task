import unittest
from src.exception import *
from unittest.mock import patch
from src.entity.matches import Match


class TestMatch(unittest.TestCase):
    def setUp(self) -> None:
        self.account_id = 318351912
        self.match_id = 6467715185
        self.match_info = {
            "match_id": 6467715185,
            "players": [
                {
                    "match_id": 6467715185,
                    "account_id": 318351912,
                    "assists": 25,
                    "deaths": 7,
                    "kills": 4,
                    "isRadiant": True
                },
                {
                    "match_id": 6467715185,
                    "account_id": 98506622,
                    "assists": 7,
                    "deaths": 5,
                    "kills": 8,
                    "isRadiant": True
                },
                {
                    "match_id": 6467715185,
                    "account_id": None,
                    "assists": 8,
                    "deaths": 3,
                    "kills": 21,
                    "isRadiant": True
                },
                {
                    "match_id": 6467715185,
                    "account_id": None,
                    "assists": 19,
                    "deaths": 3,
                    "kills": 13,
                    "isRadiant": False
                }
            ]
        }

    def test_init(self):
        match = Match(self.match_info, self.account_id)
        self.assertEqual(match.match_id, self.match_id)
        self.assertEqual(match.assists, 25)
        self.assertEqual(match.deaths, 7)
        self.assertEqual(match.kills, 4)
        self.assertEqual(match.is_radiant, True)
        self.assertEqual(match.team_kills, 33)
        self.assertEqual(match.kda, 4.14)
        self.assertEqual(match.kp, 87.88)

    def test_init_missing_player_info(self):
        err_msg = f"Player: {self.account_id} not found in the list of " \
                  f"players of match {self.match_id}"
        match_info = self.match_info
        match_info["players"] = match_info["players"][2:]
        with self.assertRaises(MissingPlayerInfoException) as err:
            Match(match_info, self.account_id)
        self.assertEqual(err_msg, err.exception.message)
        self.assertEqual(self.account_id, err.exception.account_id)
        self.assertEqual(self.match_id, err.exception.match_id)

    def test_init_key_error(self):
        err_msg = f"Match: {self.match_id} doesn't contain property " \
                  f"\"players\" for computing the KPI."
        match_info = dict(match_id=self.match_id)
        with self.assertRaises(MissingKeyError) as err:
            Match(match_info, self.match_id)
        self.assertEqual(err_msg, err.exception.message)
        self.assertEqual("players", err.exception.missing_field)

    def test_get_kp_team_kills_0(self):
        with patch.object(Match, "get_team_kills") as mock_method:
            mock_method.return_value = 0
            match = Match(self.match_info, self.account_id)
            self.assertEqual(0, match.get_kp())

    def test_get_kp(self):
        match = Match(self.match_info, self.account_id)
        self.assertEqual(87.88, match.get_kp())

    def test_kda(self):
        match = Match(self.match_info, self.account_id)
        self.assertEqual(4.14, match.get_kda())
