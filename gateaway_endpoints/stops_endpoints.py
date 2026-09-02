from fastapi import APIRouter, Path, HTTPException, Depends, Body
from fastapi.responses import PlainTextResponse, JSONResponse
from services.stops import stops_pb2_grpc
from services.stops import stops_pb2 as stops_messages
from pydantic import BaseModel, Field
from app_utils import extract_token
import grpc

stops_router = APIRouter(prefix="/stops")

error_table = {
    grpc.StatusCode.UNAUTHENTICATED : 401,
    grpc.StatusCode.PERMISSION_DENIED : 403
}

class UpdateStopInfo(BaseModel):
    stop_id: int = Field(ge=0)
    new_name: str


@stops_router.get("/{id}")
def get_transport_stop(token: str = Depends(extract_token), id: int = Path(ge=0)) -> PlainTextResponse:
    
    with grpc.insecure_channel("localhost:5000") as channel:
        try:
            stub = stops_pb2_grpc.StopsStub(channel)
            result = stub.GetStop(stops_messages.StopIdRequest(stop_id=id), metadata=[("authorization", token)])

            if result.error.error:
                raise HTTPException(status_code=404, detail=result.error.msg)
            
        except grpc.RpcError as err:
            raise HTTPException(
                status_code=error_table[err.code()],
                detail=err.details()
            )

        return PlainTextResponse(
            content=result.stop_name
        )

@stops_router.post("/add")
def add_transport_stop(stop_name: str = Body(), token: str = Depends(extract_token)) -> JSONResponse:
    with grpc.insecure_channel("localhost:5000") as channel:
        stub = stops_pb2_grpc.StopsStub(channel)

        try:
            result = stub.AddStop(
                stops_messages.AddStopRequest(name=stop_name),
                metadata=[("authorization", token)]
            )
        except grpc.RpcError as err:
            raise HTTPException(status_code=error_table[err.code()], detail=err.details())
        return JSONResponse(
            content={
                "is_error" : result.error,
                "message" : result.msg
            }
        )

@stops_router.put("/update", response_class=JSONResponse, description="Update a stop name by id")
def update_transport_stop(info: UpdateStopInfo, token: str = Depends(extract_token)) -> JSONResponse:
    with grpc.insecure_channel("localhost:5000") as channel:
        stub = stops_pb2_grpc.StopsStub(channel)

        try:
            response = stub.UpdateStop(
                stops_messages.UpdateStopRequest(
                    stop_id=info.stop_id,
                    new_name=info.new_name
                ),
                metadata=[("authorization", token)]
            )

        except grpc.RpcError as err:
            if err.code() in error_table:
                raise HTTPException(status_code=error_table[err.code()], detail=err.details())
            raise HTTPException(status_code=501, detail=err.details())


        return JSONResponse(
            content={
                "error" : response.error,
                "message" : response.msg
            }
        )

@stops_router.delete("/delete/{stop_id}", response_class=JSONResponse, description="Delete a stop name by id")
def update_transport_stop(stop_id: int = Path(ge=0), token: str = Depends(extract_token)) -> JSONResponse:
    with grpc.insecure_channel("localhost:5000") as channel:
        stub = stops_pb2_grpc.StopsStub(channel)

        try:
            response = stub.DeleteStop(
                stops_messages.StopIdRequest(
                    stop_id=stop_id
                ),
                metadata=[("authorization", token)]
            )

        except grpc.RpcError as err:
            if err.code() in error_table:
                raise HTTPException(status_code=error_table[err.code()], detail=err.details())
            raise HTTPException(status_code=501, detail=err.details())


        return JSONResponse(
            content={
                "error" : response.error,
                "message" : response.msg
            }
        )        

@stops_router.post("/transform", response_class=JSONResponse, description="Transform stop ids to its name")
def update_transport_stop(stop_ids: list[int] = Body(), token: str = Depends(extract_token)) -> JSONResponse:

    for v in stop_ids:
        if v < 0:
            raise HTTPException(
                status_code=422,
                detail="One negative id is found"
            )


    with grpc.insecure_channel("localhost:5000") as channel:
        stub = stops_pb2_grpc.StopsStub(channel)

        try:
            response = stub.TransformStops(
                stops_messages.StopIdTransformRequest(
                    stop_ids=stop_ids
                ),
                metadata=[("authorization", token)]
            )

        except grpc.RpcError as err:
            if err.code() in error_table:
                raise HTTPException(status_code=error_table[err.code()], detail=err.details())
            raise HTTPException(status_code=501, detail=err.details())


        base_content = {
            "error" : response.error.error,
            "message" : response.error.msg
        }

        if not response.error.error:
            base_content["result"] = dict(response.result.names.items())


        return JSONResponse(
            content=base_content
        )        
        