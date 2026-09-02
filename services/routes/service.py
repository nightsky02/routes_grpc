from services.routes.routes_service_pb2_grpc import RoutesServicer
from services.routes import routes_service_pb2 as service_messages
from services.routes.db import api as route_db
import grpc

class RouteService(RoutesServicer):
    def AddRoute(self, request, context):
        try:
            route_db.add_route_to_db(
                number=request.number,
                start=request.route_start,
                end=request.route_end,
                list_of_stop_ids=request.stop_ids
            )

            return service_messages.RouteOperationResponse(
                error=False, 
                msg="Successfully added the route"
            )
        
        except Exception:
            return service_messages.RouteOperationResponse(
                error=True,
                msg="Couldn't add the new route"
            )


    def ListRoutes(self, request, context):
        data = route_db.get_all_routes()

        try:
            return service_messages.RouteListResponse(
                routes=[
                    service_messages.Route(
                        number=i.number,
                        route_start=i.start_point,
                        route_end=i.end_point,
                        stop_ids=i.stops
                    ) for i in data
                ]
            )
        except Exception:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Something has happened during processing your request")
            return service_messages.RouteOperationResponse()