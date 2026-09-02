from fastapi import FastAPI
from gateaway_endpoints import stops_endpoints, routes_endpoint
import uvicorn

app = FastAPI()
app.include_router(stops_endpoints.stops_router)
app.include_router(routes_endpoint.route_api_router)


if __name__ == "__main__":
    uvicorn.run("gateaway:app", reload=True)

