from dataclasses import dataclass


@dataclass()
class EmptyRecentMatchesException(Exception):
    """
    EmptyRecentMatchesException: Recent Matches for current user is empty.
    """
    message: str
    account_id: int

    def __repr__(self):
        return {
            "message": self.message,
            "details": self.__doc__,
            "account_id": self.account_id
        }


@dataclass()
class MissingMatchInfoException(Exception):
    message: str
    match_id: int

    def __repr__(self):
        return {
            "message": self.message,
            "details": self.__doc__,
            "match_id": self.match_id
        }


@dataclass()
class MissingPlayerInfoException(Exception):
    message: str
    account_id: int
    match_id:int

    def __repr__(self):
        return {
            "message": self.message,
            "details": self.__doc__,
            "account_id": self.account_id,
            "match_id": self.match_id
        }


@dataclass()
class MissingKeyError(Exception):
    message: str
    missing_field: str

    def __repr__(self):
        return {
            "message": self.message,
            "details": self.__doc__,
            "missing_field": self.missing_field
        }
