import logging
from fastapi import APIRouter
from src.dto import QueryParams
from src.service import DataManipulation
from fastapi.responses import JSONResponse

router = APIRouter()
log = logging.getLogger(__name__)


@router.get(
    '/players',
    tags=["players"]
)
def get_kpis(account_id: int, name: str, count: int = 10):
    """
    Function returns response for API call of path "players"
    :type account_id: int
    :param account_id: Account ID of the player
    :type name: str
    :param name: Name of the player
    :type count: int
    :param count: count of the matches for which KDA/KP should be calculated
    :return: Returns response that include KDA/KP or error message
    """
    log.info(f"Started to handle request to calculate KPI for user: {name}")
    log.debug(f"Query params of the request: {account_id}, {name}, {count}")
    query_params = QueryParams(account_id, name, count)
    service = DataManipulation()
    response = service(query_params)
    log.info("Response ready.")
    log.debug(f"Response: {str(response.__dict__)}")
    return JSONResponse(
        status_code=200,
        content=response.__dict__
    )
