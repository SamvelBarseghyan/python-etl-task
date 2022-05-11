from fastapi import APIRouter
from src.dto import QueryParams
from src.service import DataManipulation
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get(
    '/players',
    tags=["players"]
)
def get_kpis(account_id: int, name: str, count: int = 10):
    query_params = QueryParams(account_id, name, count)
    service = DataManipulation()
    response = service(query_params)

    return JSONResponse(
        status_code=200,
        content=response.__dict__
    )
