from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from app_utils import extract_token
from services.routes import routes_service_pb2_grpc, routes_service_pb2
from services.stops import stops_pb2_grpc, stops_pb2
from pydantic import BaseModel
from google.protobuf.empty_pb2 import Empty
import grpc
import app_settings


route_api_router = APIRouter(prefix="/routes")


class RouteResult(BaseModel):
    number: int
    start_point: str
    end_point: str
    stops: list[str]


@route_api_router.get("/list", description="Get all the routes storaged in db")
def get_all_routes(token: str = Depends(extract_token)) -> JSONResponse:
    with grpc.insecure_channel(app_settings.ROUTES_SERVICE_HOST) as channel:
        try:
            stub = routes_service_pb2_grpc.RoutesStub(channel)

            response = stub.ListRoutes(
                Empty(), metadata=[("authorization", token)])
        except grpc.RpcError as err:
            raise HTTPException(
                status_code=504,
                detail=err.details()
            )

        result = []
        errors = []
        with grpc.insecure_channel(app_settings.STOP_SERVICE_HOST) as ss_channel:
            ss_stub = stops_pb2_grpc.StopsStub(ss_channel)

            for route in response.routes:
                try:
                    transformed_stops = ss_stub.TransformStops(
                        stops_pb2.StopIdTransformRequest(
                            stop_ids=route.stop_ids
                        ),
                        metadata=[("authorization", token)]
                    )

                    if transformed_stops.error.error:
                        errors.append(
                            f"{route.number} - {route.route_start} - {route.route_end}: {transformed_stops.error.msg}")
                        continue

                except grpc.RpcError as err:
                    raise HTTPException(
                        status_code=504,
                        detail=err.details()
                    )

                result.append(RouteResult(
                    number=route.number,
                    start_point=route.route_start,
                    end_point=route.route_end,
                    stops=list(transformed_stops.result.names.values())
                ))

        return {
            "routes": result,
            "errors": errors
        }
        

