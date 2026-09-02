import grpc
from concurrent.futures import ThreadPoolExecutor
from services.routes import routes_service_pb2_grpc
from services.routes.service import RouteService
from services._utils.scope_interceptor import ScopeInterceptor
import app_settings


if __name__ == "__main__":
    server = grpc.server(ThreadPoolExecutor(max_workers=10), interceptors=[ScopeInterceptor()])
    server.add_insecure_port(f"[::]:{app_settings.ROUTE_SERVICE_PORT}")

    routes_service_pb2_grpc.add_RoutesServicer_to_server(RouteService(), server)

    server.start()
    server.wait_for_termination()
