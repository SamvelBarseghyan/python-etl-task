import os
from pydantic import BaseSettings


class DevelopmentSettings(BaseSettings):
    recent_matches_api: str = "https://api.opendota.com/api/players/{}/" \
                              "recentMatches"
    match_info_api: str = "https://api.opendota.com/api/matches/{}"
    log_format: str = "%(asctime)s:%(levelname)s:%(filename)s:%(funcName)s" \
                      ":%(message)s"
    debug: bool = True


class TestingSettings(BaseSettings):
    recent_matches_api: str = "https://api.opendota.com/api/players/{}/" \
                              "recentMatches"
    match_info_api: str = "https://api.opendota.com/api/matches/{}"
    log_format: str = "%(asctime)s:%(levelname)s:%(filename)s:%(funcName)s" \
                      ":%(message)s"
    testing: bool = True
    debug: bool = True


class ProductionSettings(BaseSettings):
    recent_matches_api: str = "https://api.opendota.com/api/players/{}/" \
                              "recentMatches"
    match_info_api: str = "https://api.opendota.com/api/matches/{}"
    log_format: str = "%(asctime)s:%(levelname)s:%(filename)s:%(funcName)s" \
                      ":%(message)s"
    debug: bool = False


config_by_name = dict(
    dev=DevelopmentSettings,
    test=TestingSettings,
    prod=ProductionSettings
)

config_type = os.getenv("CONFIG_TYPE", "dev")
settings = config_by_name[config_type]()
