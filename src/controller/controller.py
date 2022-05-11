import logging
from typing import Union
from fastapi import APIRouter
from src.service import DataManipulation
from fastapi.responses import JSONResponse
from src.dto import QueryParams, ResponseContent

router = APIRouter()


@router.get(
    '/players',
    tags=["players"]
)
def get_kpis(account_id: int, name: str, count: int = 10):
    query_params = QueryParams(account_id, name, count)
    service = DataManipulation()
    response = service(query_params)
    return response
