import unittest
from src.exception import *
from unittest.mock import patch
from src.entity.matches import RecentMatches, Match


class TestRecentMatches(unittest.TestCase):
    def setUp(self) -> None:
        self.account_id = 318351912
        self.match_info_1 = {
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
                }
            ]
        }

        self.match_info_2 = {
            "match_id": 6467715186,
            "players": [
                {
                    "match_id": 6467715186,
                    "account_id": None,
                    "assists": 8,
                    "deaths": 3,
                    "kills": 21,
                    "isRadiant": True
                },
                {
                    "match_id": 6467715186,
                    "account_id": 318351912,
                    "assists": 19,
                    "deaths": 3,
                    "kills": 13,
                    "isRadiant": False
                }
            ]
        }
        self.match_obj_1 = Match(self.match_info_1, self.account_id)
        self.match_obj_2 = Match(self.match_info_2, self.account_id)

    def test_init(self):
        matches_list = [self.match_info_1, self.match_info_2]
        recent_matches_obj = RecentMatches(matches_list, self.account_id)
        match_obj_list = [
            self.match_obj_1,
            self.match_obj_2
        ]
        self.assertEqual(match_obj_list, recent_matches_obj.recent_matches)
        # self.assertEqual()
        # self.assertEqual()
        # self.assertEqual()
        # self.assertEqual()
        # self.assertEqual()
        # self.assertEqual()
