'''
this is the model for the passenger, it will be used to store and check for invalid passenger data
the table looks like this:
CREATE TABLE passengers (
    passenger_id SERIAL PRIMARY KEY,
    passenger_code TEXT GENERATED ALWAYS AS ('passenger-' || id) STORED user_id INT NOT NULL REFERENCES users (user_id) ON DELETE CASCADE,
    tap_go_number VARCHAR(50) UNIQUE -- transit card / tap-and-go identifier
);
this will be used later when we integrate the prepayment on the bus stops, but on bus requests 
doesn't really need to be used, their will be anonymous passengers, for us to 
count how many request are made on the stops
'''

from . import db
from .user import User

class Passenger(db.Model):
    __tablename__ = 'passengers'

    passenger_id = db.Column(db.Integer, primary_key=True)
    passenger_code = db.Column(db.String(50), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    tap_go_number = db.Column(db.String(50), unique=True)

    def __init__(self, user_id, tap_go_number=None):
        self.user_id = user_id
        self.tap_go_number = tap_go_number

    def to_dict(self):
        return {
            'passenger_id': self.passenger_id,
            'passenger_code': self.passenger_code,
            'user_id': self.user_id,
            'tap_go_number': self.tap_go_number
        }
    
    # check for the validity of the tap_go_number, it should be unique and not null
    def is_valid_tap_go_number(self):
        if self.tap_go_number is None:
            return "Invalid tap_go_number. It cannot be null."
        existing_passenger = Passenger.query.filter_by(tap_go_number=self.tap_go_number).first()
        if existing_passenger and existing_passenger.passenger_id != self.passenger_id:
            return "Invalid tap_go_number. It must be unique."
        return True
    
    # check the validity of the user_id, it should exist in the users table
    def is_valid_user_id(self):
        user = User.query.get(self.user_id)
        if user is None:
            return "Invalid user_id. It must reference an existing user."
        return True
    
    # check if the passenger is anonymous (no tap_go_number)
    def is_anonymous(self):
        return self.tap_go_number is None
    
    # check if the passenger is registered (has a tap_go_number)
    def is_registered(self):
        return self.tap_go_number is not None
    
    # check if the passenger is valid, which means it has a valid user_id and a valid tap_go_number (if not anonymous)
    def is_valid_passenger(self):
        user_check = self.is_valid_user_id()
        if user_check is not True:
            return "Invalid passenger. The user_id is not valid."

        if not self.is_anonymous():
            tap_check = self.is_valid_tap_go_number()
            if tap_check is not True:
                return "Invalid passenger. The tap_go_number is not valid."

        return True
    
    # check if the passenger is eligible for prepayment, which means it is registered and has a valid tap_go_number
    def is_eligible_for_prepayment(self):
        if self.is_registered() and self.is_valid_tap_go_number() is True:
            return True
        return False
    
    # check if the passenger is eligible for on bus requests, which means it is either anonymous or registered with a valid tap_go_number
    def is_eligible_for_on_bus_requests(self):
        if self.is_anonymous() or (self.is_registered() and self.is_valid_tap_go_number() is True):
            return True
        return False
    
    # check if the passenger is eligible for both prepayment and on bus requests, which means it is registered with a valid tap_go_number
    def is_eligible_for_both_prepayment_and_on_bus_requests(self):
        if self.is_registered() and self.is_valid_tap_go_number() is True:
            return True
        return False
    
    # get the full passenger information as a string
    def get_full_passenger_info(self):
        return f"Passenger {self.passenger_code} (ID: {self.passenger_id}) is associated with user ID {self.user_id} and has tap_go_number: {self.tap_go_number}"