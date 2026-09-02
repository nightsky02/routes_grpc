import grpc, os
import services.stops.stops_pb2_grpc as stops_grpc
from services.stops.stop_service import StopService
from services._utils.scope_interceptor import ScopeInterceptor
from concurrent.futures import ThreadPoolExecutor

if __name__ == "__main__":
    server = grpc.server(ThreadPoolExecutor(max_workers=10), interceptors=[ScopeInterceptor()])
    stops_grpc.add_StopsServicer_to_server(StopService(), server)
    server.add_insecure_port(os.getenv("STOP_SERVICE_PORT") or "[::]:5000") # "[::]:5000"
    server.start()

    print("StopService has been successfully started at 5000th port")
    server.wait_for_termination()