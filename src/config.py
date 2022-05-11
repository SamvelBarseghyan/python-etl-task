from pydantic import BaseSettings


class DevelopmentSettings(BaseSettings):
    recent_matches_api: str = "https://api.opendota.com/api/players/{}/" \
                              "recentMatches"
    match_info_api: str = "https://api.opendota.com/api/matches/{}"
    log_format: str = "%(ascctime)s:%(levelname)s:%(filename)s:%(funcName)s" \
                      ":%(message)s"
    log_filename: str = "logs.txt"
    debug: bool = True


class TestingSettings(BaseSettings):
    recent_matches_api: str = "https://api.opendota.com/api/players/{}/" \
                              "recentMatches"
    match_info_api: str = "https://api.opendota.com/api/matches/{}"
    log_format: str = "%(ascctime)s:%(levelname)s:%(filename)s:%(funcName)s" \
                      ":%(message)s"
    log_filename: str = "logs.txt"
    testing: bool = True
    debug: bool = True


class ProductionSettings(BaseSettings):
    recent_matches_api: str = "https://api.opendota.com/api/players/{}/" \
                              "recentMatches"
    match_info_api: str = "https://api.opendota.com/api/matches/{}"
    log_format: str = "%(ascctime)s:%(levelname)s:%(filename)s:%(funcName)s" \
                      ":%(message)s"
    log_filename: str = "logs.txt"
    debug: bool = False


config_by_name = dict(
    dev=DevelopmentSettings,
    test=TestingSettings,
    prod=ProductionSettings
)
