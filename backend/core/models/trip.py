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
            return "The {self.trip_code} is completed."
        elif self.status == 'in_progress':
            return "The {self.trip_code} is in progress."
        elif self.status == 'cancelled':
            return "The {self.trip_code} is cancelled."
        elif self.status == 'scheduled':
            return "The {self.trip_code} is scheduled."
        else:
            return "The {self.trip_code} has an unknown status."
        
    # check the credibility of the trip time, if the starting time is in the past, then the trip is shceduled or in progress, if the starting time is in the future, then the trip is scheduled, if the starting time is in the past and the status is not completed, then the trip is cancelled
    def check_time_credibility(self):
        from datetime import datetime
        now = datetime.now()
        if self.starting_time < now and self.status in ['scheduled', 'in_progress']:
            return "The {self.trip_code} is scheduled or in progress, but the starting time is in the past."
        elif self.starting_time > now and self.status == 'scheduled':
            return "The {self.trip_code} is scheduled, but the starting time is in the future."
        elif self.starting_time < now and self.status != 'completed':
            return "The {self.trip_code} is cancelled, but the starting time is in the past."
        else:
            return "The {self.trip_code} has a credible starting time."
        

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