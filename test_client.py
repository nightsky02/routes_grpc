import grpc

# stops
from services.stops.stops_pb2_grpc import StopsStub
from services.stops import stops_pb2 as ts_messages

# routes
from services.routes.routes_service_pb2_grpc import RoutesStub
from services.routes import routes_service_pb2 as ts_routes_messages
from google.protobuf.empty_pb2 import Empty
from datetime import datetime, timedelta
import app_settings
import jwt


def test_stop_service():
    with grpc.insecure_channel("localhost:5000") as channel:
        ts_stops_stub = StopsStub(channel)
        try:
            response = ts_stops_stub.AddStop(ts_messages.AddStopRequest(
                name="Andreya Saharova iela 19"
            ),
            metadata=[
                ("authorization", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzY29wZXMiOlsic3RvcHMudHJhbnNmb3Jtc3RvcHMiXSwiaWF0IjoxNzg3MDQzMDMxLCJleHAiOjE3ODcwNDMxNTF9.3GrcjPiYhCggIE_EDc9o7Hqny8g8eStxX6cNgSQtY9s"),
            ])
        except grpc.RpcError as err:
            print(err.code(), err.details())

            if err.code() == grpc.StatusCode.UNAUTHENTICATED:
                print("You need to log in or check your scopes")


def test_route_service():
    with grpc.insecure_channel("localhost:5002") as channel:
        t_route_stub = RoutesStub(channel)

        try:
            response = t_route_stub.ListRoutes(Empty(), metadata=[("authorization", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzY29wZXMiOlsic3RvcHMudHJhbnNmb3Jtc3RvcHMiLCJyb3V0ZXMubGlzdHJvdXRlcyJdLCJpYXQiOjE3ODcwNzA2MTUsImV4cCI6MTc4NzA3MDczNX0.oasRRm30UbS9a3sLUnP09vKc_lX9TZsrBXw4ijLV_UE")])

            for route in response.routes:
                print(route.stop_ids)
        except grpc.RpcError as err:
            print("Some error occured:", err.details()) 

if __name__ == "__main__":
    # test_route_service()
    # generate tokens for all GRPC services
    print(
        jwt.encode(
            payload={
                "scopes" : ["stops.getstop", "stops.addstop", "stops.updatestop", "stops.deletestop", "stops.transformstops", "routes.listroutes"],
                "iat" : datetime.now().utcnow(),
                "exp" : datetime.now().utcnow() + timedelta(minutes=20)
            },
            key=app_settings.JWT_SIGN_KEY,
            algorithm=app_settings.JWT_ALG
        )
    )


  