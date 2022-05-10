from dataclasses import dataclass


@dataclass()
class QueryParams:
    """
    DTO to save data of the query parameters from the request
    """
    account_id: int
    name: str
    count: int
