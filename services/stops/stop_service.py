from services.stops.stops_pb2_grpc import StopsServicer
from services.stops.stops_pb2 import StopNameResponse


class StopService(StopsServicer):
    def AddStop(self, request, context):
        # Implement the logic to add a stop
        # For example, you can access the stop name using request.name
        # and return an OperationResponse indicating success or failure.
        pass

    def GetStop(self, request, context):
        # Implement the logic to get a stop by its ID
        # You can access the stop ID using request.stop_id
        # and return a StopNameResponse with the stop name.
        return StopNameResponse(name="Example Stop Name")

    def UpdateStop(self, request, context):
        # Implement the logic to update a stop by its ID
        # You can access the stop ID using request.stop_id
        # and return an OperationResponse indicating success or failure.
        pass

    def DeleteStop(self, request, context):
        # Implement the logic to delete a stop by its ID
        # You can access the stop ID using request.stop_id
        # and return an OperationResponse indicating success or failure.
        pass

    def TransformStops(self, request, context):
        # Implement the logic to transform a list of stop IDs into their corresponding names
        # You can access the list of stop IDs using request.stop_ids
        # and return a StopNameListResponse with the list of stop names.
        pass