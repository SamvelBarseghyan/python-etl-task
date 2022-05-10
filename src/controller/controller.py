import logging

from fastapi import APIRouter
from src.service import DataManipulation
from src.dto import QueryParams, ResponseModel
from src.exception import EmptyRecentMatchesException

router = APIRouter()


@router.get('/players', response_model=ResponseModel, tags=["players"])
def get_kpis(account_id: int, name: str, count: int = 10):
    query_params = QueryParams(account_id, name, count)
    try:
        service = DataManipulation()
        return service(query_params)
    except EmptyRecentMatchesException as err:
        return {
            "code": 500,
            "message": err.message
        }
    except Exception as err:
        return {
            "code": 500,
            "message": "Internal Error"
        }
