from pydantic import BaseSettings


class DevelopmentSettings(BaseSettings):
    recent_matches_api: str = "https://api.opendota.com/api/players/{}/" \
                              "recentMatches"
    match_info_api: str = "https://api.opendota.com/api/matches/{}"
    debug: bool = True


class TestingSettings(BaseSettings):
    recent_matches_api: str = "https://api.opendota.com/api/players/{}/" \
                              "recentMatches"
    match_info_api: str = "https://api.opendota.com/api/matches/{}"
    debug: bool = True
    testing: bool = True


class ProductionSettings(BaseSettings):
    recent_matches_api: str = "https://api.opendota.com/api/players/{}/" \
                              "recentMatches"
    match_info_api: str = "https://api.opendota.com/api/matches/{}"
    debug: bool = False


config_by_name = dict(
    dev=DevelopmentSettings,
    test=TestingSettings,
    prod=ProductionSettings
)
