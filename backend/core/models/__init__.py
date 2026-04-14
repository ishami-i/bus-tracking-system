from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import models after db is defined to avoid circular imports
from .user import User
from .bus import Bus
from .route import Route
from .stop import Stop
from .route_stop import RouteStop
from .driver import Driver
from .passenger import Passenger
from .trip import Trip
from .passenger_events import PassengerEvent
from .gps_log import GPSLog
from .bus_request import BusRequest

__all__ = [
    'db',
    'User',
    'Bus',
    'Route',
    'Stop',
    'RouteStop',
    'Driver',
    'Passenger',
    'Trip',
    'PassengerEvent',
    'GPSLog',
    'BusRequest',
]
