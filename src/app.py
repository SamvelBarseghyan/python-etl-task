import io
import yaml
import functools
import traceback
from src.exception import *
from fastapi import FastAPI, Request
from controller.controller import router
from fastapi.responses import Response, JSONResponse

app = FastAPI(
    title="ETL Project",
    description="API provides functionality to calculate KPIs of "
                "Dota player",
    version="0.1"
)
app.include_router(router)


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

    if isinstance(err, ConnectionError):
        return JSONResponse(
            status_code=500,
            content={
                "message": "Internal Server Error",
                "detailed_message": err.args[0].args[0]
            },
        )
    return JSONResponse(
        status_code=500,
        content={
            "message": "Internal Server Error",
            "detailed_message": traceback.format_exc()
        },
    )


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)
