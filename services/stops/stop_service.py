from services.stops.stops_pb2_grpc import StopsServicer
from services.stops import stops_pb2 as grpc_messages
from services.stops.db import api as db_api
from services.stops.db import exceptions as db_exc
from services.stops.utils import validate_list_of_ids


class StopService(StopsServicer):
    def AddStop(self, request, context):
        # Implement the logic to add a stop
        # For example, you can access the stop name using request.name
        # and return an OperationResponse indicating success or failure.
        try:
            stop_id = db_api.add_stop(request.name)

            return grpc_messages.OperationResponse(
                error=False,
                msg="Successfully added the transport stop",
                stop_id=stop_id
            )

        except db_exc.StopExistsError as err:
            return grpc_messages.OperationResponse(
                error=True,
                msg=str(err),
            )

    def GetStop(self, request, context):
        # Implement the logic to get a stop by its ID
        # You can access the stop ID using request.stop_id
        # and return a StopNameResponse with the stop name.

        stop_name = db_api.get_stop_name(stop_id=request.stop_id)

        if stop_name:
            return grpc_messages.GetStopNameResponse(
                stop_name=stop_name
            )

        return grpc_messages.GetStopNameResponse(
            error_response=grpc_messages.OperationResponse(
                error=True,
                msg="There is no a stop with the following id"
            )
        )

    def UpdateStop(self, request, context):
        # Implement the logic to update a stop by its ID
        # You can access the stop ID using request.stop_id
        # and return an OperationResponse indicating success or failure.

        if request.new_name is None or len(request.new_name) <= 0:
            return grpc_messages.OperationResponse(
                error=True,
                msg="The name of a bus stop must be passed"
            )

        if request.stop_id <= 0:
            return grpc_messages.OperationResponse(
                error=True,
                msg='Invalid stop id. It should be > 0'
            )

        try:
            updated_count = db_api.update_stop_name(
                stop_id=request.stop_id,
                new_name=request.new_name
            )

            if updated_count == 0:
                return grpc_messages.OperationResponse(
                    error=True,
                    msg="No found the stop"
                )

            return grpc_messages.OperationResponse(
                error=False,
                msg="Successfully updated a stop by id"
            )
        except db_exc.PStopServiceDbException as err:
            return grpc_messages.OperationResponse(
                error=True,
                msg=str(err)
            )

    def DeleteStop(self, request, context):
        # Implement the logic to delete a stop by its ID
        # You can access the stop ID using request.stop_id
        # and return an OperationResponse indicating success or failure.
        if request.stop_id <= 0:
            return grpc_messages.OperationResponse(
                error=True,
                msg="Invalid id"
            )

        try:
            result = db_api.delete_stop(request.stop_id)
            return grpc_messages.OperationResponse(
                error=not result,
                msg="Success" if result else "No bus stop with the following id"
            )

        except db_exc.PStopServiceDbException as err:
            return grpc_messages.OperationResponse(
                error=True,
                msg=err
            )

    def TransformStops(self, request, context):
        # Implement the logic to transform a list of stop IDs into their corresponding names
        # You can access the list of stop IDs using request.stop_ids
        # and return a StopNameListResponse with the list of stop names.
        if not validate_list_of_ids(request.stop_ids):
            return grpc_messages.StopNameTransformResponse(
                error=grpc_messages.OperationResponse(
                    error=True,
                    msg="Some of given ids is/are invalid"
                ))

        
        try:
            data = db_api.select_stops(request.stop_ids)
            no_found_stops_ids = set(request.stop_ids).difference(set(data.keys()))

            for id in no_found_stops_ids:
                data[id] = ""

            return grpc_messages.StopNameTransformResponse(
                result=grpc_messages.StopNameMap(names=data)
            )
        
        except db_exc.PStopServiceDbException as err:
            return grpc_messages.StopNameTransformResponse(
                error=grpc_messages.OperationResponse(
                    error=True,
                    msg=err
                ))
