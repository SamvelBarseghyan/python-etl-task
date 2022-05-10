import io
import yaml
import functools
from controller.controller import router
from fastapi import FastAPI, HTTPException
from fastapi.responses import Response


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


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)
