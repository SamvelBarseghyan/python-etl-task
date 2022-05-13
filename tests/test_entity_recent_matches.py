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

    def test_init(self):
        matches_list = [self.match_info_1, self.match_info_2]
        recent_matches_obj = RecentMatches(matches_list, self.account_id)

        self.assertEqual(4.14, recent_matches_obj.min_kda)
        self.assertEqual(7.4, recent_matches_obj.avg_kda)
        self.assertEqual(10.67, recent_matches_obj.max_kda)
        self.assertEqual("241.67%", recent_matches_obj.min_kp)
        self.assertEqual("243.91%", recent_matches_obj.avg_kp)
        self.assertEqual("246.15%", recent_matches_obj.max_kp)

    def test_get_min_avg_max_of_list_kda(self):
        list_of_nums = [4.4, 1, 14, 0.5, 1.23]
        expected_tuple = 0.5, 4.23, 14

        @dataclass()
        class MockClass:
            kda: float

        matches_list = [self.match_info_1, self.match_info_2]
        recent_matches_obj = RecentMatches(matches_list, self.account_id)

        recent_matches_obj.recent_matches = list()
        for num in list_of_nums:
            recent_matches_obj.recent_matches.append(MockClass(num))
        self.assertEqual(
            expected_tuple,
            recent_matches_obj.get_min_avg_max_of_list(True)
        )

    def test_get_min_avg_max_of_list_kp(self):
        list_of_nums = [4.4, 1, 14, 0.5, 1.23]
        expected_tuple = "0.5%", "4.23%", "14%"

        @dataclass()
        class MockClass:
            kp: float

        matches_list = [self.match_info_1, self.match_info_2]
        recent_matches_obj = RecentMatches(matches_list, self.account_id)
        recent_matches_obj.recent_matches = list()
        for num in list_of_nums:
            recent_matches_obj.recent_matches.append(MockClass(num))
        self.assertEqual(
            expected_tuple,
            recent_matches_obj.get_min_avg_max_of_list(False)
        )
