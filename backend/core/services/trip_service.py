"""
this is the service layer for trip which get and update the trip data from database,
using the trip repository to interact with the database, after being checked by 
the trip model and the trip schema, the trip service will return the data to the controller layer to be sent to the client.

this will  be used in calculating the eta of the trip, and the update the status of the trip.
"""

from datetime import datetime
from typing import List
from core.models.trip import Trip
from core.repositories.trip_repository import TripRepository
from core.models.route_stop import RouteStop
from core.repositories.route_stop_repository import RouteStopRepository
from haversine import haversine, Unit
from math import radians, cos, sin, asin, sqrt
from core.schemas.trip_schema import TripSchema

class TripService:
    # initialize the trip repository
    def __init__(self, trip_repository: TripRepository):
        self.trip_repository = trip_repository
    
    # get the trip by id
    def get_trip_by_id(self, trip_id: int) -> Trip:
        return self.trip_repository.get_trip_by_id(trip_id)
    
    # get bus location and timestamp by trip id
    #Use last 3–5 GPS points to calculate the speed of the bus, then use that information to predict the ETA of the trip.
    def get_bus_location_by_trip_id(self, trip_id: int) -> dict:
        trip = self.trip_repository.get_trip_by_id(trip_id)
        if not trip:
            return {"error": "Trip not found"}
        # get the last 3-5 GPS points of the bus
        gps_points = self.trip_repository.get_gps_points_by_trip_id(trip_id, limit=5)
        if not gps_points:
            return {"error": "No GPS points found for this trip"}
        # calculate the speed of the bus
        speed = self.calculate_speed_by_trip_id(trip_id)
        # predict the ETA of the trip
        eta = self.predict_eta(trip_id, speed)
        return {
            "location": gps_points[-1].location,
            "timestamp": gps_points[-1].timestamp,
            "speed": speed,
            "eta": eta
        }
    # calcalate the speed of the bus by trip id
    def calculate_speed_by_trip_id(self, trip_id: int) -> float:
        trip = self.trip_repository.get_trip_by_id(trip_id)
         # calculate distance with haversine formula then speed.
        gps_points = self.trip_repository.get_gps_points_by_trip_id(trip_id, limit=5)
        if len(gps_points) < 2:
            return 0.0
        total_distance = 0.0
        total_time = 0.0
        for i in range(1, len(gps_points)):
            point1 = gps_points[i-1]
            point2 = gps_points[i]
            distance = haversine((point1.latitude, point1.longitude), (point2.latitude, point2.longitude), unit=Unit.KILOMETERS)
            time_diff = (point2.timestamp - point1.timestamp).total_seconds() / 3600.0  # convert to hours
            total_distance += distance
            total_time += time_diff
        if total_time == 0:
            return 0.0
        speed = total_distance / total_time  # speed in km/h
        return speed
    
    # get a position of the bus on the route by trip id(order_stop table, get nearest stop and all remaining stops)
    def get_bus_position_on_route_by_trip_id(self, trip_id: int) -> dict:
        # get the trip by id
        trip = self.trip_repository.get_trip_by_id(trip_id)

        # get the position of the bus on the route and count the remaining stops
        route_stops = RouteStopRepository().get_route_stops_by_route_id(trip.route_id)
        gps_points = self.trip_repository.get_gps_points_by_trip_id(trip_id, limit=5)
        if not gps_points:
            return {"error": "No GPS points found for this trip"}
        bus_location = (gps_points[-1].latitude, gps_points[-1].longitude)
        nearest_stop = None
        min_distance = float('inf')
        remaining_stops = 0
        for route_stop in route_stops:
            stop_location = (route_stop.latitude, route_stop.longitude)
            distance = haversine(bus_location, stop_location, unit=Unit.KILOMETERS)
            if distance < min_distance:
                min_distance = distance
                nearest_stop = route_stop
        for route_stop in route_stops:
            stop_location = (route_stop.latitude, route_stop.longitude)
            distance = haversine(bus_location, stop_location, unit=Unit.KILOMETERS)
            if distance < min_distance:
                remaining_stops += 1
        return {
            "nearest_stop": nearest_stop.stop_name,
            "remaining_stops": remaining_stops
        }
    # calculate the ETA of the trip by trip id and speed
    def predict_eta(self, trip_id: int, speed: float) -> str:
        trip = self.trip_repository.get_trip_by_id(trip_id)
        if not trip:
            return "Trip not found"
        route_stops = RouteStopRepository().get_route_stops_by_route_id(trip.route_id)
        gps_points = self.trip_repository.get_gps_points_by_trip_id(trip_id, limit=5)
        if not gps_points:
            return "No GPS points found for this trip"
        bus_location = (gps_points[-1].latitude, gps_points[-1].longitude)
        nearest_stop = None
        min_distance = float('inf')
        for route_stop in route_stops:
            stop_location = (route_stop.latitude, route_stop.longitude)
            distance = haversine(bus_location, stop_location, unit=Unit.KILOMETERS)
            if distance < min_distance:
                min_distance = distance
                nearest_stop = route_stop
        if speed == 0:
            return "Speed is zero, cannot predict ETA"
        eta_hours = min_distance / speed
        eta_time = datetime.now() + timedelta(hours=eta_hours)         
        
        