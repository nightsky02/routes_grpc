from services.routes.db.base_settings import engine
from services.routes import base_models
from services.routes.db.models import Route
from sqlalchemy import select, insert
from sqlalchemy.orm import Session
from sqlalchemy.exc import MultipleResultsFound
import random


def add_route_to_db(number: int, start: str,
                     end: str, list_of_stop_ids: list[int]) -> int:

    """
        Adds a new route into db and returns its id
    """

    with Session(engine) as session:
        route_id = random.randint(1, 1000)

        for stop_id in list_of_stop_ids:
            session.add(Route(
                route_id=route_id,
                number=number,
                start_point=start,
                end_point=end,
                stop_id=stop_id
            ))

        session.commit()
        return route_id


def get_all_routes() -> list[base_models.Route]:
    select_all_routes_ids = (
        select(Route.route_id.distinct())
    )

    result = []

    with Session(engine) as session:
        ids = session.execute(select_all_routes_ids).scalars()

        for route_id in ids:
            select_current_route = (
                select(Route)
                .where(Route.route_id == route_id)
            )

            data = session.execute(select_current_route)

            route_data = data.scalars().all()

            if not route_data:
                return []

            result.append(
                base_models.Route(
                    number=route_data[0].number,
                    start_point=route_data[0].start_point,
                    end_point=route_data[0].end_point,
                    stops=[i.stop_id for i in route_data]
                )
            )
    return result
          