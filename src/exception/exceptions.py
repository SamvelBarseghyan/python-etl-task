from dataclasses import dataclass


@dataclass()
class EmptyRecentMatchesException(Exception):
    message: str
    account_id: str


@dataclass()
class MissingMatchInfoException(Exception):
    message: str
    match_id: int


@dataclass()
class MissingPlayerInfoException(Exception):
    message: str
    account_id: int
    match_id:int


@dataclass()
class MissingKeyError(Exception):
    message: str
    missing_field: str
