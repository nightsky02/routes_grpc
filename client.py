import grpc
from services.stops.stops_pb2_grpc import StopsStub
from services.stops import stops_pb2 as ts_messages

if __name__ == "__main__":
    with grpc.insecure_channel("localhost:5000") as channel:
        ts_stops_stub = StopsStub(channel)
        response = ts_stops_stub.TransformStops(ts_messages.StopIdTransformRequest(
            stop_ids=[7,8,9, 100, -2]
        ))

        print(response.result.names, response.error.msg)