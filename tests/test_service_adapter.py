import json
import requests
import unittest
from unittest import mock
from src.exception import *
from unittest.mock import patch
from src.dto import QueryParams
from requests.models import Response
from src.service import DataManipulation


detailed_match_info = {
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
            "account_id": 639740,
            "assists": 7,
            "deaths": 5,
            "kills": 8,
            "isRadiant": True
        }
    ]
}

recent_matches_info = [
    {
        "match_id": 6467715185,
        "player_slot": 130,
        "radiant_win": True,
        "duration": 1939,
        "game_mode": 22,
        "lobby_type": 7,
        "hero_id": 55,
        "start_time": 1646816947,
        "version": None,
        "kills": 6,
        "deaths": 10,
        "assists": 11,
        "skill": None,
        "xp_per_min": 521,
        "gold_per_min": 442,
        "hero_damage": 14770,
        "tower_damage": 539,
        "hero_healing": 1273,
        "last_hits": 159,
        "lane": None,
        "lane_role": None,
        "is_roaming": None,
        "cluster": 186,
        "leaver_status": 0,
        "party_size": 2
    }
]


def mocked_requests_get(*args, **kwargs):
    request_url = args[0]
    if request_url == "https://api.opendota.com/api/players/" \
                      "639740/recentMatches":
        response_content = json.dumps(recent_matches_info)
    else:
        response_content = json.dumps(detailed_match_info)
    response = Response()
    response.status_code = 200
    response._content = str.encode(response_content)
    return response


def mocked_requests_get_none(*args, **kwargs):
    response = Response()
    response.status_code = 200
    response._content = str.encode(json.dumps(None))
    return response


class TestDataManipulation(unittest.TestCase):
    def setUp(self) -> None:
        self.adapter = DataManipulation()
        self.query_params = QueryParams(639740, "YrikGood", 1)

    def test_get_match_detailed_info(self):
        with patch.object(requests, 'get', side_effect=mocked_requests_get):
            self.assertEqual(
                detailed_match_info,
                self.adapter.get_match_detailed_info(6467715185)
            )

    def test_get_match_detailed_info_exception(self):
        with patch.object(
                requests, 'get', side_effect=mocked_requests_get_none):
            with self.assertRaises(MissingMatchInfoException) as err:
                self.adapter.get_match_detailed_info(6467715185)
            err_msg = "Missing: 6467715185 not found."
            self.assertEqual(err_msg, err.exception.message)
            self.assertEqual(6467715185, err.exception.match_id)

    def test_get_recent_matches(self):
        with patch.object(requests, 'get', side_effect=mocked_requests_get):
            self.assertEqual(
                recent_matches_info,
                self.adapter.get_recent_matches(639740)
            )

    def test_get_recent_matches_exception(self):
        with patch.object(
                requests, 'get', side_effect=mocked_requests_get_none):
            with self.assertRaises(EmptyRecentMatchesException) as err:
                self.adapter.get_recent_matches(639740)
            err_msg = f"Matches for account: 639740 not found."
            self.assertEqual(err_msg, err.exception.message)
            self.assertEqual(639740, err.exception.account_id)

    def test_player_info(self):
        with patch.object(requests, 'get', side_effect=mocked_requests_get):
            player_info = self.adapter.get_player_info(self.query_params)
            self.assertEqual(
                self.query_params.account_id, player_info.account_id
            )
            self.assertEqual(
                self.query_params.name, player_info.name
            )
            self.assertEqual(
                len(recent_matches_info), player_info.total_games
            )
