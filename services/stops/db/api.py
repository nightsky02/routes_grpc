from .base_settings import engine
from .models import TransportStop
from .exceptions import StopExistsError, PStopServiceDbException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, DBAPIError
from sqlalchemy import select, update, delete


def add_stop(stop_name: str) -> int:
    with Session(engine) as session:
        try:
            ts = TransportStop(name=stop_name)
            session.add(ts)
            session.commit()
            return ts.id
        except IntegrityError:
            raise StopExistsError(f"The public transport stop {stop_name!r} already exists")


def get_stop_name(stop_id: int) -> str | None:
    with Session(engine) as session:
        query = (
            select(TransportStop)
            .where(TransportStop.id == stop_id)
        )

        try:
            result = session.execute(query).scalar()
            if result is None:
                return None
            return result.name
        except DBAPIError as err:
            raise PStopServiceDbException(err.orig)


def update_stop_name(stop_id: int, new_name: str) -> int:
    query = (
        update(TransportStop)
        .where(TransportStop.id == stop_id)
        .values(name=new_name)
    )

    with Session(engine) as session:
        try:
            r = session.execute(query)
            session.commit()
            return r.rowcount
        except DBAPIError as err:
            raise PStopServiceDbException(err.orig)

def delete_stop(stop_id: int) -> bool:
    query = (
        delete(TransportStop)
        .where(TransportStop.id == stop_id)
    )

    with Session(engine) as session:
        try:
            r = session.execute(query)
            session.commit()
            return r.rowcount > 0
        except DBAPIError as err:
            raise PStopServiceDbException(err.orig)


def select_stops(stops_id: list[int]) -> dict[int, str]: # id -> name
    query = (
        select(TransportStop)
        .where(TransportStop.id.in_(stops_id))
    )

    try:
        with Session(engine) as session:
            result = session.execute(query).scalars().all()
            return {s.id : s.name for s in result}
    except DBAPIError as err:
        raise PStopServiceDbException(err)
