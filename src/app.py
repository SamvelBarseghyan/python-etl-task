import io
import yaml
import logger
import logging
import functools
import traceback
from exception import *
from fastapi import FastAPI, Request
from controller.controller import router
from fastapi.responses import Response, JSONResponse
log = logging.getLogger(__name__)

app = FastAPI(
    title="ETL Project",
    description="API provides functionality to calculate KPIs of "
                "Dota player",
    version="0.1"
)
app.include_router(router)
log.info("APP was created")


@app.get('/openapi.yaml', include_in_schema=False)
@functools.lru_cache()
def read_openapi_yaml() -> Response:
    """ Exports yaml openapi definition"""
    openapi_json = app.openapi()
    yaml_s = io.StringIO()
    yaml.dump(openapi_json, yaml_s)
    return Response(yaml_s.getvalue(), media_type='text/yaml')


@app.exception_handler(Exception)
def exception_handler(request: Request, err: Exception):

    log.error("An exception was thrown during the calculation of KPI.")
    log.error(err)

    if isinstance(err, EmptyRecentMatchesException):
        return JSONResponse(
            status_code=403,
            content={
                "message": err.message,
                "account_id": err.account_id
            }
        )
    if isinstance(err, MissingPlayerInfoException):
        return JSONResponse(
            status_code=400,
            content={
                "message": err.message,
                "account_id": err.account_id,
                "match_id": err.match_id
            },
        )
    if isinstance(err, MissingKeyError):
        return JSONResponse(
            status_code=510,
            content={
                "message": err.message,
                "missing_field": err.missing_field
            },
        )

    return JSONResponse(
        status_code=500,
        content={
            "message": "Internal Server Error",
            "detailed_message": traceback.format_exc()
        },
    )
