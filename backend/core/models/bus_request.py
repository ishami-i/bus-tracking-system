''' 
This is the bus request moidels which contains s
request_id SERIAL PRIMARY KEY,
    request_code TEXT GENERATED ALWAYS AS ('request-' || id) STORED stop_id INT REFERENCES stops (stop_id) ON DELETE SET NULL,
    trip_id INT REFERENCES trips (trip_id) ON DELETE CASCADE,
    passenger_id INT REFERENCES passengers (passenger_id) ON DELETE CASCADE,
    passenger_status VARCHAR(50), -- e.g. 'pending', 'picked_up', 'cancelled'
    request_time TIMESTAMP NOT NULL DEFAULT NOW()
'''
from . import db

class BusRequest(db.Model):
    __tablename__ = 'bus_requests'

    request_id = db.Column(db.Integer, primary_key=True)
    request_code = db.Column(db.String, nullable=False, unique=True)
    stop_id = db.Column(db.Integer, db.ForeignKey('stops.stop_id', ondelete='SET NULL'))
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.trip_id', ondelete='CASCADE'))
    passenger_id = db.Column(db.Integer, db.ForeignKey('passengers.passenger_id', ondelete='CASCADE'))
    passenger_status = db.Column(db.String(50), nullable=False)  # e.g. 'pending', 'picked_up', 'cancelled'
    request_time = db.Column(db.DateTime, nullable=False, default=db.func.now())

    def __init__(self, stop_id, trip_id, passenger_id, passenger_status):
        self.stop_id = stop_id
        self.trip_id = trip_id
        self.passenger_id = passenger_id
        self.passenger_status = passenger_status
        self.request_code = f'request-{self.request_id}'  # This will be set after the object is added to the session and committed


    # check if every required field is provided if not raise an error, and provide field to be provided with data 

    def validate(self):
        if not self.trip_id:
            raise ValueError("Trip ID is required.")
        if not self.passenger_id:
            raise ValueError("Passenger ID is required.")
        if not self.passenger_status:
            raise ValueError("Passenger status is required.")
        else:
            valid_statuses = ['pending', 'picked_up', 'cancelled']
            if self.passenger_status not in valid_statuses:
                raise ValueError(f"Passenger status must be one of {valid_statuses}.")
    
    def __repr__(self):
        return f"<BusRequest(request_id={self.request_id}, request_code='{self.request_code}', stop_id={self.stop_id}, trip_id={self.trip_id}, passenger_id={self.passenger_id}, passenger_status='{self.passenger_status}', request_time='{self.request_time}')>"
    
    # check for credibility of the data provided for the bus request, for example if the trip_id provided is not exist in the trips table then raise an error, and provide the field to be provided with data
    def check_credibility(self):
        from .trip import Trip
        from .passenger import Passenger
        from .stop import Stop

        if not Trip.query.get(self.trip_id):
            raise ValueError(f"Trip with ID {self.trip_code} does not exist.")
        if not Passenger.query.get(self.passenger_id):
            raise ValueError(f"Passenger with ID {self.passenger_id} does not exist.")
        if self.stop_id and not Stop.query.get(self.stop_id):
            raise ValueError(f"Stop with ID {self.stop_id} does not exist.")
        
    # check if the bus request is valid for the trip, for example if the trip is already completed then raise an error, and provide the field to be provided with data
    def check_validity(self):
        from .trip import Trip

        trip = Trip.query.get(self.trip_id)
        if trip.status == 'completed' or trip.status == 'cancelled':
            raise ValueError(f"Trip with ID {self.trip_code} is already completed. Cannot create a bus request for a completed trip.")
        else:
            valid_statuses = ['pending', 'picked_up']
            if self.passenger_status not in valid_statuses:
                raise ValueError(f"Passenger status must be one of {valid_statuses}.")
            
    # check if the bus request is valid for the passenger, for example if the passenger is already picked up then raise an error, and provide the field to be provided with data
    def check_passenger_validity(self):
        from .passenger import Passenger

        passenger = Passenger.query.get(self.passenger_id)
        if passenger.status == 'picked_up' or passenger.status == 'cancelled':
            raise ValueError(f"Passenger with ID {self.passenger_id} is already picked up. Cannot create a bus request for a passenger who is already picked up.")
        else:
            valid_statuses = ['pending', 'picked_up']
            if self.passenger_status not in valid_statuses:
                raise ValueError(f"Passenger status must be one of {valid_statuses}.")
            

    # create a bus request and save it to the database, and return the bus request object
    @staticmethod
    def create_bus_request(stop_id, trip_id, passenger_id, passenger_status):
        bus_request = BusRequest(stop_id=stop_id, trip_id=trip_id, passenger_id=passenger_id, passenger_status=passenger_status)
        bus_request.validate()
        bus_request.check_credibility()
        bus_request.check_validity()
        bus_request.check_passenger_validity()
        db.session.add(bus_request)
        db.session.commit()
        return bus_request
    # update the bus request status, for example if the passenger is picked up then update the passenger status to picked up, and return the updated bus request object
    def update_bus_request_status(self, new_status):
        valid_statuses = ['pending', 'picked_up', 'cancelled']
        if new_status not in valid_statuses:
            raise ValueError(f"New status must be one of {valid_statuses}.")
        self.passenger_status = new_status
        db.session.commit()
        return self
    # create a method to delete the bus request from the database, and return a message that the bus request has been deleted
    def delete_bus_request(self):
        db.session.delete(self)
        db.session.commit()
        return f"Bus request with ID {self.request_id} has been deleted."
    
    # create a method to get all bus requests for a specific trip, and return a list of bus request objects
    @staticmethod
    def get_bus_requests_by_trip(trip_id):
        return BusRequest.query.filter_by(trip_id=trip_id).all()
    
    # create a method to get all bus requests for a specific passenger, and return a list of bus request objects
    @staticmethod
    def get_bus_requests_by_passenger(passenger_id):
        return BusRequest.query.filter_by(passenger_id=passenger_id).all()
    
    # create a method to get all bus requests for a specific stop, and return a list of bus request objects
    @staticmethod
    def get_bus_requests_by_stop(stop_id):
        return BusRequest.query.filter_by(stop_id=stop_id).all()
    
    # create a method to get all bus requests, and return a list of bus request objects
    @staticmethod
    def get_all_bus_requests():
        return BusRequest.query.all()
    
    # create a method to get a bus request by its ID, and return the bus request object
    @staticmethod
    def get_bus_request_by_id(request_id):
        return BusRequest.query.get(request_id)
    
    # create a method to get a bus request by its request code, and return the bus request object
    @staticmethod
    def get_bus_request_by_code(request_code):
        return BusRequest.query.filter_by(request_code=request_code).first()
    
    # create a method to get the number of bus requests for a specific trip, and return the number of bus requests
    @staticmethod
    def get_bus_request_count_by_trip(trip_id):
        return BusRequest.query.filter_by(trip_id=trip_id).count()
    # create a method to get the number of bus requests for a specific passenger, and return the number of bus requests
    @staticmethod
    def get_bus_request_count_by_passenger(passenger_id):
        return BusRequest.query.filter_by(passenger_id=passenger_id).count()
    # create a method to get the number of bus requests for a specific stop, and return the number of bus requests
    @staticmethod
    def get_bus_request_count_by_stop(stop_id):
        return BusRequest.query.filter_by(stop_id=stop_id).count()
    # create a method to get the number of bus requests, and return the number of bus requests
    @staticmethod
    def get_total_bus_request_count():
        return BusRequest.query.count()
    
    # create a method to get the number of bus requests for a specific trip and passenger, and return the number of bus requests
    @staticmethod
    def get_bus_request_count_by_trip_and_passenger(trip_id, passenger_id):
        return BusRequest.query.filter_by(trip_id=trip_id, passenger_id=passenger_id).count()
    
    # create a method to get the number of bus requests for a specific trip and stop, and return the number of bus requests
    @staticmethod
    def get_bus_request_count_by_trip_and_stop(trip_id, stop_id):
        return BusRequest.query.filter_by(trip_id=trip_id, stop_id=stop_id).count()
    
    # create a method to get the number of bus requests for a specific passenger and stop, and return the number of bus requests
    @staticmethod
    def get_bus_request_count_by_passenger_and_stop(passenger_id, stop_id):
        return BusRequest.query.filter_by(passenger_id=passenger_id, stop_id=stop_id).count()
    
    # create a method to get the number of bus requests for a specific trip, passenger, and stop, and return the number of bus requests
    @staticmethod
    def get_bus_request_count_by_trip_passenger_and_stop(trip_id, passenger_id, stop_id):
        return BusRequest.query.filter_by(trip_id=trip_id, passenger_id=passenger_id, stop_id=stop_id).count()
    
    # create a method to get the bus request status for a specific trip and passenger, and return the bus request status
    @staticmethod
    def get_bus_request_status_by_trip_and_passenger(trip_id, passenger_id):
        bus_request = BusRequest.query.filter_by(trip_id=trip_id, passenger_id=passenger_id).first()
        if bus_request:
            return bus_request.passenger_status
        else:
            return None
        

    # create a method for clasifying the most request by passenger
    @staticmethod
    def get_most_requested_passenger():
        from .passenger import Passenger
        from sqlalchemy import func

        most_requested_passenger = db.session.query(
            BusRequest.passenger_id,
            func.count(BusRequest.request_id).label('request_count')
        ).group_by(BusRequest.passenger_id).order_by(func.count(BusRequest.request_id).desc()).first()

        if most_requested_passenger:
            passenger = Passenger.query.get(most_requested_passenger.passenger_id)
            return passenger, most_requested_passenger.request_count
        else:
            return None, 0
        
    # create a method for clasifying the most request by trip
    @staticmethod
    def get_most_requested_trip():
        from .trip import Trip
        from sqlalchemy import func

        most_requested_trip = db.session.query(
            BusRequest.trip_id,
            func.count(BusRequest.request_id).label('request_count')
        ).group_by(BusRequest.trip_id).order_by(func.count(BusRequest.request_id).desc()).first()

        if most_requested_trip:
            trip = Trip.query.get(most_requested_trip.trip_id)
            return trip, most_requested_trip.request_count
        else:
            return None, 0
        
    # create a method for clasifying the most request by stop
    @staticmethod
    def get_most_requested_stop():
        from .stop import Stop
        from sqlalchemy import func

        most_requested_stop = db.session.query(
            BusRequest.stop_id,
            func.count(BusRequest.request_id).label('request_count')
        ).group_by(BusRequest.stop_id).order_by(func.count(BusRequest.request_id).desc()).first()

        if most_requested_stop:
            stop = Stop.query.get(most_requested_stop.stop_id)
            return stop, most_requested_stop.request_count
        else:
            return None, 0
        
    # create a method for clasifying the most request by passenger status
    @staticmethod
    def get_most_requested_passenger_status():
        from sqlalchemy import func

        most_requested_passenger_status = db.session.query(
            BusRequest.passenger_status,
            func.count(BusRequest.request_id).label('request_count')
        ).group_by(BusRequest.passenger_status).order_by(func.count(BusRequest.request_id).desc()).first()

        if most_requested_passenger_status:
            return most_requested_passenger_status.passenger_status, most_requested_passenger_status.request_count
        else:
            return None, 0
        
    # create a method for clasifying the most request by time of day
    @staticmethod
    def get_most_requested_time_of_day():
        from sqlalchemy import func

        most_requested_time_of_day = db.session.query(
            func.date_part('hour', BusRequest.request_time).label('hour'),
            func.count(BusRequest.request_id).label('request_count')
        ).group_by(func.date_part('hour', BusRequest.request_time)).order_by(func.count(BusRequest.request_id).desc()).first()

        if most_requested_time_of_day:
            return int(most_requested_time_of_day.hour), most_requested_time_of_day.request_count
        else:
            return None, 0
    
    # create a method for clasifying the most request by day of week
    @staticmethod
    def get_most_requested_day_of_week():
        from sqlalchemy import func

        most_requested_day_of_week = db.session.query(
            func.date_part('dow', BusRequest.request_time).label('day_of_week'),
            func.count(BusRequest.request_id).label('request_count')
        ).group_by(func.date_part('dow', BusRequest.request_time)).order_by(func.count(BusRequest.request_id).desc()).first()

        if most_requested_day_of_week:
            return int(most_requested_day_of_week.day_of_week), most_requested_day_of_week.request_count
        else:
            return None, 0
    
    # create a method for clasifying the most request by month
    @staticmethod
    def get_most_requested_month():
        from sqlalchemy import func

        most_requested_month = db.session.query(
            func.date_part('month', BusRequest.request_time).label('month'),
            func.count(BusRequest.request_id).label('request_count')
        ).group_by(func.date_part('month', BusRequest.request_time)).order_by(func.count(BusRequest.request_id).desc()).first()

        if most_requested_month:
            return int(most_requested_month.month), most_requested_month.request_count
        else:
            return None, 0