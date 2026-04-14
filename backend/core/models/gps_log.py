'''
this is the model for real time tracking of the bus. 
the table is like this:
CREATE TABLE gps_logs (
    log_id SERIAL PRIMARY KEY,
    log_code TEXT GENERATED ALWAYS AS ('gpslog-' || id) STORED longitude DECIMAL(10, 7) NOT NULL,
    latitude DECIMAL(10, 7) NOT NULL,
    timestamps TIMESTAMP NOT NULL DEFAULT NOW(),
    bus_id INT REFERENCES buses (bus_id) ON DELETE SET NULL,
    trip_id INT REFERENCES trips (trip_id) ON DELETE SET NULL
);
'''

import datetime
from . import db
from .trip import Trip

class GPSLog(db.Model):
    __tablename__ = 'gps_logs'

    log_id = db.Column(db.Integer, primary_key=True)
    log_code = db.Column(db.String(50), unique=True, nullable=False)
    longitude = db.Column(db.Numeric(10, 7), nullable=False)
    latitude = db.Column(db.Numeric(10, 7), nullable=False)
    timestamps = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    bus_id = db.Column(db.Integer, db.ForeignKey('buses.bus_id', ondelete='SET NULL'))
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.trip_id', ondelete='SET NULL'))

    def __init__(self, longitude, latitude, bus_id=None, trip_id=None):
        self.longitude = longitude
        self.latitude = latitude
        self.bus_id = bus_id
        self.trip_id = trip_id
        self.log_code = f'gpslog-{self.log_id}'
    
    def to_dict(self):
        return {
            'log_id': self.log_id,
            'log_code': self.log_code,
            'longitude': str(self.longitude),
            'latitude': str(self.latitude),
            'timestamps': self.timestamps.isoformat(),
            'bus_id': self.bus_id,
            'trip_id': self.trip_id
        }
    
    # validity of the longitude and latitude, they should be within the valid range of -180 to 180 for longitude and -90 to 90 for latitude
   def is_valid_coordinates(self):
        lon = float(self.longitude)
        lat = float(self.latitude)
        if not (-180 <= lon <= 180):
            return "Invalid longitude. It must be between -180 and 180."
        if not (-90 <= lat <= 90):
            return "Invalid latitude. It must be between -90 and 90."
        return True
        # check if the bus_id is valid, it should exist in the buses table
        def is_valid_bus_id(self):
            from .bus import Bus
            bus = Bus.query.get(self.bus_id)
            if bus is None:
                return "Invalid bus_id. It must reference an existing bus."
            return True
    
    # check if the trip_id is valid, it should exist in the trips table
    def is_valid_trip_id(self):
        from .trip import Trip
        trip = Trip.query.get(self.trip_id)
        if trip is None:
            return "Invalid trip_id. It must reference an existing trip."
        return True
    
    # check if the GPS log is valid, which means it has valid coordinates and valid bus_id and trip_id (if not null)
    def is_valid_gps_log(self):
        if not self.is_valid_coordinates():
            return "Invalid GPS log. The coordinates are not valid."
        if self.bus_id is not None and not self.is_valid_bus_id():
            return "Invalid GPS log. The bus_id is not valid."
        if self.trip_id is not None and not self.is_valid_trip_id():
            return "Invalid GPS log. The trip_id is not valid."
        return True
    

    # check for recentness of the GPS log, it should be within the last 5 minutes
    def is_recent(self):
        now = datetime.datetime.now()
        if (now - self.timestamps).total_seconds() > 300:
            return "The GPS log is not recent. It should be within the last 5 minutes."
        return True
    
    # check if the timestamps is not in future or before the trip starting time, if the trip_id is not null
    def is_valid_timestamp(self):
        now = datetime.datetime.now()
        if self.timestamps > now:
            return "Invalid timestamp. It cannot be in the future."
        if self.trip_id is not None:
            trip = Trip.query.get(self.trip_id)
            if trip and self.timestamps < trip.starting_time:
                return "Invalid timestamp. It cannot be before the trip starting time."
        return True
    
    # check if the GPS log is valid, which means it has valid coordinates, valid bus_id and trip_id (if not null), and valid timestamp
    def is_valid(self):
        if not self.is_valid_coordinates():
            return "Invalid GPS log. The coordinates are not valid."
        if self.bus_id is not None and not self.is_valid_bus_id():
            return "Invalid GPS log. The bus_id is not valid."
        if self.trip_id is not None and not self.is_valid_trip_id():
            return "Invalid GPS log. The trip_id is not valid."
        if not self.is_valid_timestamp():
            return "Invalid GPS log. The timestamp is not valid."
        return True
    
    # check if the GPS log is associated with an active trip, which means the trip_id is not null and the trip is in progress
    def is_associated_with_active_trip(self):
        if self.trip_id is None:
            return False
        trip = Trip.query.get(self.trip_id)
        if trip and trip.is_in_progress():
            return True
        return False
    
    # check if the GPS log is associated with a completed trip, which means the trip_id is not null and the trip is completed
    def is_associated_with_completed_trip(self):
        if self.trip_id is None:
            return False
        trip = Trip.query.get(self.trip_id)
        if trip and trip.is_completed():
            return True
        return False
    
    # check if the GPS log is associated with a cancelled trip, which means the trip_id is not null and the trip is cancelled, return concelled trip if the trip is cancelled, otherwise return a message that the GPS log is not associated with a cancelled trip
    def is_associated_with_cancelled_trip(self):
        if self.trip_id is None:
            return False
        trip = Trip.query.get(self.trip_id)
        if trip and trip.is_cancelled():
            return True
        return False
    
    # check if the GPS log is associated with a scheduled trip, which means the trip_id is not null and the trip is scheduled, return scheduled trip if the trip is scheduled, otherwise return a message that the GPS log is not associated with a scheduled trip
    def is_associated_with_scheduled_trip(self):
        if self.trip_id is None:
            return False
        trip = Trip.query.get(self.trip_id)
        if trip and trip.is_scheduled():
            return True
        return False
    
    # check if the GPS log is associated with a trip that has a credible starting time, which means the trip_id is not null and the trip has a credible starting time, return the trip if it has a credible starting time, otherwise return a message that the GPS log is not associated with a trip that has a credible starting time
    def is_associated_with_trip_with_credible_starting_time(self):
        if self.trip_id is None:
            return False
        trip = Trip.query.get(self.trip_id)
        if trip and trip.has_credible_starting_time():
            return True
        return False
    
