'''
this the table which connects the routes and the stops.
the postgresql table looks like this:
CREATE TABLE route_stops (
    route_stop_id SERIAL PRIMARY KEY,
    route_id INT NOT NULL REFERENCES routes (route_id) ON DELETE CASCADE,
    stop_id INT NOT NULL REFERENCES stops (stop_id) ON DELETE CASCADE,
    stop_order INT NOT NULL,
    UNIQUE (route_id, stop_order)
);
'''

from typing import List
from sqlalchemy import select, delete
from core.models.route_stop import RouteStop
from core.repositories.base_repository import BaseRepository
import logging

logger = logging.getLogger(__name__)

class RouteStopRepository(BaseRepository):
    def __(init__(self, session)):
        super().__init__(session)

    # add new route stop connection
    def add_route_stop(self, route_id: int, stop_id: int, stop_order: int) -> RouteStop:
        try:
            new_route_stop = RouteStop(route_id=route_id, stop_id=stop_id, stop_order=stop_order)
            self.session.add(new_route_stop)
            self.session.commit()
            self.session.refresh(new_route_stop)
            return new_route_stop
        except Exception as e:
            logger.error(f"Error adding route stop: {e}")
            self.session.rollback()
            raise
    
    # get all stops that belongs to the route
    def get_stops_by_route_id(self, route_id: int) -> List[RouteStop]:
        try:
            stmt = select(RouteStop).where(RouteStop.route_id == route_id).order_by(RouteStop.stop_order)
            result = self.session.execute(stmt).scalars().all()
            return result
        except Exception as e:
            logger.error(f"Error fetching stops for route {route_id}: {e}")
            raise

    # delete all stops that belongs to the route
    def delete_stops_by_route_id(self, route_id: int) -> None:
        try:
            stmt = delete(RouteStop).where(RouteStop.route_id == route_id)
            self.session.execute(stmt)
            self.session.commit()
        except Exception as e:
            logger.error(f"Error deleting stops for route {route_id}: {e}")
            self.session.rollback()
            raise
    
    # delete all routes that belongs to the stop
    def delete_routes_by_stop_id(self, stop_id: int) -> None:
        try:
            stmt = delete(RouteStop).where(RouteStop.stop_id == stop_id)
            self.session.execute(stmt)
            self.session.commit()
        except Exception as e:
            logger.error(f"Error deleting routes for stop {stop_id}: {e}")
            self.session.rollback()
            raise

    # get all routes that belongs to the stop
    def get_routes_by_stop_id(self, stop_id: int) -> List[RouteStop]:
        try:
            stmt = select(RouteStop).where(RouteStop.stop_id == stop_id).order_by(RouteStop.stop_order)
            result = self.session.execute(stmt).scalars().all()
            return result
        except Exception as e:
            logger.error(f"Error fetching routes for stop {stop_id}: {e}")
            raise
    
    # get all route stop connections
    def get_all_route_stops(self) -> List[RouteStop]:
        try:
            stmt = select(RouteStop)
            result = self.session.execute(stmt).scalars().all()
            return result
        except Exception as e:
            logger.error(f"Error fetching all route stops: {e}")
            raise
    
    # delete route stop connection by id
    def delete_route_stop_by_id(self, route_stop_id: int) -> None:
        try:
            stmt = delete(RouteStop).where(RouteStop.route_stop_id == route_stop_id)
            self.session.execute(stmt)
            self.session.commit()
        except Exception as e:
            logger.error(f"Error deleting route stop with id {route_stop_id}: {e}")
            self.session.rollback()
            raise
    # update route stop connection by id
    def update_route_stop_by_id(self, route_stop_id: int, route_id: int, stop_id: int, stop_order: int) -> RouteStop:
        try:
            route_stop = self.session.get(RouteStop, route_stop_id)
            if route_stop is None:
                raise ValueError(f"Route stop with id {route_stop_id} not found")
            route_stop.route_id = route_id
            route_stop.stop_id = stop_id
            route_stop.stop_order = stop_order
            self.session.commit()
            self.session.refresh(route_stop)
            return route_stop
        except Exception as e:
            logger.error(f"Error updating route stop with id {route_stop_id}: {e}")
            self.session.rollback()
            raise

    # get route stop connection by id
    def get_route_stop_by_id(self, route_stop_id: int) -> RouteStop:
        try:
            route_stop = self.session.get(RouteStop, route_stop_id)
            if route_stop is None:
                raise ValueError(f"Route stop with id {route_stop_id} not found")
            return route_stop
        except Exception as e:
            logger.error(f"Error fetching route stop with id {route_stop_id}: {e}")
            raise

    # serialize route stop connection to dict
    @staticmethod
    def serialize_route_stop(route_stop: RouteStop) -> dict:
        return {
            "route_stop_id": route_stop.route_stop_id,
            "route_id": route_stop.route_id,
            "stop_id": route_stop.stop_id,
            "stop_order": route_stop.stop_order
        }
    
    # serialize list of route stop connections to list of dicts
    @staticmethod
    def serialize_route_stops(route_stops: List[RouteStop]) -> List[dict]:
        return [RouteStopRepository.serialize_route_stop(route_stop) for route_stop in route_stops]
    
    # serialize route stop connection to dict with route and stop details
    @staticmethod
    def serialize_route_stop_with_details(route_stop: RouteStop) -> dict:
        return {
            "route_stop_id": route_stop.route_stop_id,
            "route_id": route_stop.route_id,
            "stop_id": route_stop.stop_id,
            "stop_order": route_stop.stop_order,
            "route": RouteRepository.serialize_route(route_stop.route),
            "stop": StopRepository.serialize_stop(route_stop.stop)
        }
    
    # serialize list of route stop connections to list of dicts with route and stop details
    @staticmethod
    def serialize_route_stops_with_details(route_stops: List[RouteStop]) -> List[dict]:
        return [RouteStopRepository.serialize_route_stop_with_details(route_stop) for route_stop in route_stops]

    # get route stop connection by route id and stop id
    @staticmethod
    def get_route_stop_by_route_id_and_stop_id(route_id: int, stop_id: int) -> RouteStop:
        try:
            stmt = select(RouteStop).where(RouteStop.route_id == route_id, RouteStop.stop_id == stop_id)
            result = self.session.execute(stmt).scalars().first()
            if result is None:
                raise ValueError(f"Route stop with route id {route_id} and stop id {stop_id} not found")
            return result
        except Exception as e:
            logger.error(f"Error fetching route stop with route id {route_id} and stop id {stop_id}: {e}")
            raise 