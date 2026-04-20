'''
this is repository for all actions involving the fetching and uploading to the database
the route postgresql table looks like this:
CREATE TABLE routes (
    route_id SERIAL PRIMARY KEY,
    route_code TEXT GENERATED ALWAYS AS ('route-' || route_id) STORED,
    name VARCHAR(100) NOT NULL,
    starting_address VARCHAR(255),
    starting_longitude DECIMAL(10, 7),
    starting_latitude DECIMAL(10, 7),
    ending_address VARCHAR(255),
    ending_longitude DECIMAL(10, 7),
    ending_latitude DECIMAL(10, 7)
);
'''

import logging
from typing import List, Optional
from sqlalchemy import text
from core.models.route import Route
from core.database import get_db

logger = logging.getLogger(__name__)

# constants from the database
ROUTE_TABLE = 'routes'

class RouteRepository:
    def __init__(self):
        self.db = get_db()
    
    # create a new route in the database
    def create_route(self, route: Route) -> Optional[Route]:
        try:
            query = text(f"""
                INSERT INTO {ROUTE_TABLE} (name, starting_address, starting_longitude, starting_latitude, ending_address, ending_longitude, ending_latitude)
                VALUES (:name, :starting_address, :starting_longitude, :starting_latitude, :ending_address, :ending_longitude, :ending_latitude)
                RETURNING route_id, route_code
            """)
            result = self.db.execute(query, {
                'name': route.name,
                'starting_address': route.starting_address,
                'starting_longitude': route.starting_longitude,
                'starting_latitude': route.starting_latitude,
                'ending_address': route.ending_address,
                'ending_longitude': route.ending_longitude,
                'ending_latitude': route.ending_latitude
            })
            self.db.commit()
            row = result.fetchone()
            if row:
                return Route(
                    route_id=row['route_id'],
                    route_code=row['route_code'],
                    name=route.name,
                    starting_address=route.starting_address,
                    starting_longitude=route.starting_longitude,
                    starting_latitude=route.starting_latitude,
                    ending_address=route.ending_address,
                    ending_longitude=route.ending_longitude,
                    ending_latitude=route.ending_latitude
                )
        except Exception as e:
            logger.error(f"Error creating route: {e}")
            self.db.rollback()
        return None
    
    # update an existing route in the database, with the given data unless not given no change
    def update_route(self, route_id: int, route: Route) -> Optional[Route]:
        try:
            query = text(f"""
                UPDATE {ROUTE_TABLE}
                SET name = COALESCE(:name, name),
                    starting_address = COALESCE(:starting_address, starting_address),
                    starting_longitude = COALESCE(:starting_longitude, starting_longitude),
                    starting_latitude = COALESCE(:starting_latitude, starting_latitude),
                    ending_address = COALESCE(:ending_address, ending_address),
                    ending_longitude = COALESCE(:ending_longitude, ending_longitude),
                    ending_latitude = COALESCE(:ending_latitude, ending_latitude)
                WHERE route_id = :route_id
                RETURNING route_id, route_code
            """)
            result = self.db.execute(query, {
                'route_id': route_id,
                'name': route.name,
                'starting_address': route.starting_address,
                'starting_longitude': route.starting_longitude,
                'starting_latitude': route.starting_latitude,
                'ending_address': route.ending_address,
                'ending_longitude': route.ending_longitude,
                'ending_latitude': route.ending_latitude
            })
            self.db.commit()
            row = result.fetchone()
            if row:
                return Route(
                    route_id=row['route_id'],
                    route_code=row['route_code'],
                    name=route.name,
                    starting_address=route.starting_address,
                    starting_longitude=route.starting_longitude,
                    starting_latitude=route.starting_latitude,
                    ending_address=route.ending_address,
                    ending_longitude=route.ending_longitude,
                    ending_latitude=route.ending_latitude
                )
        except Exception as e:
            logger.error(f"Error updating route: {e}")
            self.db.rollback()
        return None
    
    # get the route with the given id from the database
    def get_route_by_id(self, route_id: int) -> Optional[Route]:
        try:
            query = text(f"SELECT * FROM {ROUTE_TABLE} WHERE route_id = :route_id")
            result = self.db.execute(query, {'route_id': route_id})
            row = result.fetchone()
            if row:
                return Route(
                    route_id=row['route_id'],
                    route_code=row['route_code'],
                    name=row['name'],
                    starting_address=row['starting_address'],
                    starting_longitude=row['starting_longitude'],
                    starting_latitude=row['starting_latitude'],
                    ending_address=row['ending_address'],
                    ending_longitude=row['ending_longitude'],
                    ending_latitude=row['ending_latitude']
                )
        except Exception as e:
            logger.error(f"Error fetching route by id: {e}")
        return None
    
    # get all routes from the database
    def get_all_routes(self) -> List[Route]:
        routes = []
        try:
            query = text(f"SELECT * FROM {ROUTE_TABLE}")
            result = self.db.execute(query)
            for row in result:
                routes.append(Route(
                    route_id=row['route_id'],
                    route_code=row['route_code'],
                    name=row['name'],
                    starting_address=row['starting_address'],
                    starting_longitude=row['starting_longitude'],
                    starting_latitude=row['starting_latitude'],
                    ending_address=row['ending_address'],
                    ending_longitude=row['ending_longitude'],
                    ending_latitude=row['ending_latitude']
                ))
        except Exception as e:
            logger.error(f"Error fetching all routes: {e}")
        return routes
    
    # delete the route with the given id from the database
    def delete_route(self, route_id: int) -> bool:
        try:
            query = text(f"DELETE FROM {ROUTE_TABLE} WHERE route_id = :route_id")
            self.db.execute(query, {'route_id': route_id})
            self.db.commit()
            return True
        except Exception as e:
            logger.error(f"Error deleting route: {e}")
            self.db.rollback()
        return False
    
    # delete all routes from the database
    def delete_all_routes(self) -> bool:
        try:
            query = text(f"DELETE FROM {ROUTE_TABLE}")
            self.db.execute(query)
            self.db.commit()
            return True
        except Exception as e:
            logger.error(f"Error deleting all routes: {e}")
            self.db.rollback()
        return False
    
    # count the number of routes in the database
    def count_routes(self) -> int:
        try:
            query = text(f"SELECT COUNT(*) FROM {ROUTE_TABLE}")
            result = self.db.execute(query)
            count = result.scalar()
            return count if count is not None else 0
        except Exception as e:
            logger.error(f"Error counting routes: {e}")
        return 0
    
    # check if a route with the given id exists in the database
    def route_exists(self, route_id: int) -> bool:
        try:
            query = text(f"SELECT 1 FROM {ROUTE_TABLE} WHERE route_id = :route_id")
            result = self.db.execute(query, {'route_id': route_id})
            return result.fetchone() is not None
        except Exception as e:
            logger.error(f"Error checking if route exists: {e}")
        return False
    
    # check if a route with the given code exists in the database
    def route_code_exists(self, route_code: str) -> bool:
        try:
            query = text(f"SELECT 1 FROM {ROUTE_TABLE} WHERE route_code = :route_code")
            result = self.db.execute(query, {'route_code': route_code})
            return result.fetchone() is not None
        except Exception as e:
            logger.error(f"Error checking if route code exists: {e}")
        return False