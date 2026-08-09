class PStopServiceDbException(Exception):
    pass

class StopExistsError(PStopServiceDbException):
    "Raises when a stop (stop name) already exists in the database"
    pass