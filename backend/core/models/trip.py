'''
this is the model for the trip, it contains all the information about the trip from PostgreSQL database

this entity contains these attributse:
trip_id SERIAL PRIMARY KEY,
    trip_code TEXT GENERATED ALWAYS AS ('trip-' || id) STORED route_id INT REFERENCES routes (route_id) ON DELETE SET NULL,
    driver_id INT REFERENCES drivers (driver_id) ON DELETE SET NULL,
    event_id INT, -- FK to passenger_events (set after table creation)
    starting_time TIMESTAMP NOT NULL,
    status VARCHAR(50) NOT NULL 
'''

from . import db
from datetime import datetime


class Trip(db.Model):
    __tablename__ = 'trips'

    trip_id = db.Column(db.Integer, primary_key=True)
    trip_code = db.Column(db.String, nullable=False, unique=True)
    route_id = db.Column(db.Integer, db.ForeignKey('routes.route_id', ondelete='SET NULL'))
    driver_id = db.Column(db.Integer, db.ForeignKey('drivers.driver_id', ondelete='SET NULL'))
    event_id = db.Column(db.Integer)  # FK to passenger_events (set after table creation)
    starting_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50), nullable=False)

    def __init__(self, route_id, driver_id, event_id, starting_time, status):
        self.route_id = route_id
        self.driver_id = driver_id
        self.event_id = event_id
        self.starting_time = starting_time
        self.status = status

    def to_dict(self):
        return {
            'trip_id': self.trip_id,
            'trip_code': self.trip_code,
            'route_id': self.route_id,
            'driver_id': self.driver_id,
            'event_id': self.event_id,
            'starting_time': self.starting_time.isoformat(),
            'status': self.status
        }
    
    # checkign if the trip is status of the trip is xo0mpleted, in_progress, cancelled, or scheduled, and return the status of the trip
   def check_status(self):
        if self.status == 'completed':
            return f"The {self.trip_code} is completed."
        elif self.status == 'in_progress':
            return f"The {self.trip_code} is in progress."
        elif self.status == 'cancelled':
            return f"The {self.trip_code} is cancelled."
        elif self.status == 'scheduled':
            return f"The {self.trip_code} is scheduled."
        else:
            return f"The {self.trip_code} has an unknown status."
        
    # check the credibility of the trip time, if the starting time is in the past, then the trip is shceduled or in progress, if the starting time is in the future, then the trip is scheduled, if the starting time is in the past and the status is not completed, then the trip is cancelled
    def check_time_credibility(self):
        now = datetime.now()
        if self.starting_time < now and self.status in ['scheduled', 'in_progress']:
            return f"The {self.trip_code} is scheduled or in progress, but the starting time is in the past."
        elif self.starting_time > now and self.status == 'scheduled':
            return f"The {self.trip_code} is scheduled, but the starting time is in the future."
        elif self.starting_time < now and self.status != 'completed':
            return f"The {self.trip_code} is cancelled, but the starting time is in the past."
        else:
            return f"The {self.trip_code} has a credible starting time."
        

    # check if the trip is completed, if the status is completed and the starting time is in the past, then the trip is completed, otherwise, it is not completed
    def is_completed(self):
        from datetime import datetime
        now = datetime.now()
        if self.status == 'completed' and self.starting_time < now:
            return True
        else:
            return False
    
    # check if the trip is in progress, if the status is in progress and the starting time is in the past, then the trip is in progress, otherwise, it is not in progress
    def is_in_progress(self):
        from datetime import datetime
        now = datetime.now()
        if self.status == 'in_progress' and self.starting_time < now:
            return True
        else:
            return False
        
    # check if the trip is cancelled, if the status is cancelled and the starting time is in the past, then the trip is cancelled, otherwise, it is not cancelled
    def is_cancelled(self):
        from datetime import datetime
        now = datetime.now()
        if self.status == 'cancelled' and self.starting_time < now:
            return True
        else:
            return False
        
    # check if the trip is scheduled, if the status is scheduled and the starting time is in the future, then the trip is scheduled, otherwise, it is not scheduled
    def is_scheduled(self):
        from datetime import datetime
        now = datetime.now()
        if self.status == 'scheduled' and self.starting_time > now:
            return True
        else:
            return False
        
    # check if the trip is valid, if the status is one of the valid statuses and the starting time is a valid datetime, then the trip is valid, otherwise, it is not valid
    def is_valid(self):
        from datetime import datetime
        valid_statuses = ['completed', 'in_progress', 'cancelled', 'scheduled']
        if self.status not in valid_statuses:
            return "Invalid status. Expected values: 'completed', 'in_progress', 'cancelled', 'scheduled'."
        
        if not isinstance(self.starting_time, datetime):
            return "Invalid starting time. It must be a valid datetime object."
        
        return True
    
    # get the assigned driver, if the driver_id is not None, then return the driver_id, otherwise, return a message that the trip is not assigned to any driver
    def get_assigned_driver(self):
        if self.driver_id is not None:
            return f"Trip {self.trip_code} is assigned to driver {self.driver_id}."
        return f"Trip {self.trip_code} is not assigned to any driver."
    
    # assign a driver to the trip, if the trip is not completed, then assign the driver to the trip, otherwise, return a message that the trip is completed and cannot be assigned to any driver
    def assign_driver(self, driver_id):
        if self.is_completed():
            return f"Trip {self.trip_code} is completed and cannot be assigned to any driver."
        
        self.driver_id = driver_id
        return f"Driver {driver_id} has been assigned to trip {self.trip_code}."
    
    # unassign a driver from the trip, if the trip is not completed, then unassign the driver from the trip, otherwise, return a message that the trip is completed and cannot be unassigned from any driver
    def unassign_driver(self):
        if self.is_completed():
            return f"Trip {self.trip_code} is completed and cannot be unassigned from any driver."
        
        self.driver_id = None
        return f"Driver has been unassigned from trip {self.trip_code}."
    
    # update the status of the trip, if the new status is one of the valid statuses, then update the status of the trip, otherwise, return a message that the new status is invalid
    def update_status(self, new_status):
        valid_statuses = ['completed', 'in_progress', 'cancelled', 'scheduled']
        if new_status not in valid_statuses:
            return "Invalid status. Expected values: 'completed', 'in_progress', 'cancelled', 'scheduled'."
        
        self.status = new_status
        return f"Trip {self.trip_code} status has been updated to {new_status}."
    
    # update the starting time of the trip, if the new starting time is a valid datetime, then update the starting time of the trip, otherwise, return a message that the new starting time is invalid
    def update_starting_time(self, new_starting_time):
        from datetime import datetime
        if not isinstance(new_starting_time, datetime):
            return "Invalid starting time. It must be a valid datetime object."
        
        self.starting_time = new_starting_time
        return f"Trip {self.trip_code} starting time has been updated to {new_starting_time}."
    
    # get the full trip information as a string
    def get_full_trip_info(self):
        # count the number of events that happened during the trip, if the event_id is not None, then return the number of events, otherwise, return a message that no events happened during the trip
        if self.event_id is not None:
            events_count = 1  # This is a placeholder. You would need to query the passenger_events table to get the actual count of events for this trip.
            events_info = f"{events_count} event(s) happened during the trip."
        else:
            events_info = "No events happened during the trip."

        # return the full trip information as a string no ids included
        return f"Trip Code: {self.trip_code}, Route name: {self.route_name}, Starting Time: {self.starting_time}, Status: {self.status}. {events_info}"
    
    # get the trip's route name, if the route_id is not None, then return the route name, otherwise, return a message that the trip is not assigned to any route
    @property
    def route_name(self):
        if self.route_id is not None:
            # This is a placeholder. You would need to query the routes table to get the actual route name for this trip.
            return f"Route {self.route_id}"
        return f"Trip {self.trip_code} is not assigned to any route."