'''
this is contains event happening with passengers, which are boarding, and outboarding, and counting number of 
passengers on the board.
the table contains these: 
CREATE TABLE passenger_events (
    event_id SERIAL PRIMARY KEY,
    event_code TEXT GENERATED ALWAYS AS ('event-' || id) STORED trip_id INT NOT NULL REFERENCES trips (trip_id) ON DELETE CASCADE,
    passenger_id INT NOT NULL REFERENCES passengers (passenger_id) ON DELETE CASCADE,
    event_type VARCHAR(50) NOT NULL, -- e.g. 'tap_on', 'tap_off'
    event_time TIMESTAMP NOT NULL
);
'''

import datetime
from . import db
from .passenger import Passenger
from .trip import Trip 

class PassengerEvent(db.Model):
    __tablename__ = 'passenger_events'

    event_id = db.Column(db.Integer, primary_key=True)
    event_code = db.Column(db.String(50), unique=True, nullable=False)
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.trip_id', ondelete='CASCADE'), nullable=False)
    passenger_id = db.Column(db.Integer, db.ForeignKey('passengers.passenger_id', ondelete='CASCADE'), nullable=False)
    event_type = db.Column(db.String(50), nullable=False)  # e.g. 'tap_on', 'tap_off'
    event_time = db.Column(db.DateTime, nullable=False)

    def __init__(self, trip_id, passenger_id, event_type):
        self.trip_id = trip_id
        self.passenger_id = passenger_id
        self.event_type = event_type
        self.event_time = datetime.datetime.now()
    
    def to_dict(self):
        return {
            'event_id': self.event_id,
            'event_code': self.event_code,
            'trip_id': self.trip_id,
            'passenger_id': self.passenger_id,
            'event_type': self.event_type,
            'event_time': self.event_time.isoformat()
        }
    
    # check if the event type is valid, it should be either 'tap_on' or 'tap_off'
    def is_valid_event_type(self):
        if self.event_type not in ['tap_on', 'tap_off']:
            return "Invalid event type. It must be either 'tap_on' or 'tap_off'."
        return True
    
    # check if the passenger is valid, it should exist in the passengers table
    def is_valid_passenger(self):
        passenger = Passenger.query.get(self.passenger_id)
        if passenger is None:
            return "Invalid passenger_id. It must reference an existing passenger."
        return True
    
    # check if the trip is valid, it should exist in the trips table
    def is_valid_trip(self):
        trip = Trip.query.get(self.trip_id)
        if trip is None:
            return "Invalid trip_id. It must reference an existing trip."
        return True
    
    # check if the event is a tap on event
    def is_tap_on(self):
        return self.event_type == 'tap_on'
    
    # check if the event is a tap off event
    def is_tap_off(self):
        return self.event_type == 'tap_off'
    
    # check if the event is valid, which means it has a valid event type, a valid passenger_id, and a valid trip_id
    def is_valid_event(self):
        if self.is_valid_event_type() is not True:
            return "Invalid event. The event type is not valid."
        if self.is_valid_passenger() is not True:
            return "Invalid event. The passenger_id is not valid."
        if self.is_valid_trip() is not True:
            return "Invalid event. The trip_id is not valid."
        return True
    # check if the event is a boarding event, which means it is a tap on event
    def is_boarding_event(self):
        return self.is_tap_on()
    
    # check if the event is an outboarding event, which means it is a tap off event
    def is_outboarding_event(self):
        return self.is_tap_off()
    
    # check if the event is a valid boarding or outboarding event, which means it is either a tap on or tap off event
    def is_valid_boarding_or_outboarding_event(self):
        if self.is_valid_event_type() is not True:
            return "Invalid event. The event type is not valid."
        if self.is_valid_passenger() is not True:
            return "Invalid event. The passenger_id is not valid."
        if self.is_valid_trip() is not True:
            return "Invalid event. The trip_id is not valid."
        return True
    
    # check if the event is a valid boarding event, which means it is a tap on event and it has a valid passenger_id and a valid trip_id
    def is_valid_boarding_event(self):
        if not self.is_tap_on():
            return "Invalid boarding event. The event type must be 'tap_on'."
        if self.is_valid_passenger() is not True:
            return "Invalid boarding event. The passenger_id is not valid."
        if self.is_valid_trip() is not True:
            return "Invalid boarding event. The trip_id is not valid."
        return True