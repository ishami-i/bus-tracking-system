'''
this file contans the driver model which is used to store the driver information in the database
thew table looks like this:
CREATE TABLE drivers (
    driver_id SERIAL PRIMARY KEY,
    driver_code TEXT GENERATED ALWAYS AS ('driver-' || id) STORED user_id INT NOT NULL REFERENCES users (user_id) ON DELETE CASCADE,
    bus_id INT REFERENCES buses (bus_id) ON DELETE SET NULL
);
'''

from . import db
from .user import User
from .bus import Bus

class Driver(db.Model):
    __tablename__ = 'drivers'

    driver_id = db.Column(db.Integer, primary_key=True)
    driver_code = db.Column(db.String(50), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    bus_id = db.Column(db.Integer, db.ForeignKey('buses.bus_id', ondelete='SET NULL'))

    def __init__(self, user_id, bus_id=None):
        self.user_id = user_id
        self.bus_id = bus_id
        self.driver_code = f'driver-{self.driver_id}'

    def to_dict(self):
        return {
            'driver_id': self.driver_id,
            'driver_code': self.driver_code,
            'user_id': self.user_id,
            'bus_id': self.bus_id
        }
    
    # check if the user_id is valid, it should exist in the users table
    def is_valid_user_id(self):
        user = User.query.get(self.user_id)
        if user is None:
            return "Invalid user_id. It must reference an existing user."
        return True
    
    # check if the bus_id is valid, it should exist in the buses table
    def is_valid_bus_id(self):
        if self.bus_id is None:
            return True  # bus_id can be null
        bus = Bus.query.get(self.bus_id)
        if bus is None:
            return "Invalid bus_id. It must reference an existing bus."
        return True
    
    # check if the driver is assigned to a bus
    def is_assigned_to_bus(self):
        return self.bus_id is not None
    
    # check if the driver is unassigned to a bus
    def is_unassigned_to_bus(self):
        return self.bus_id is None
    
    # check if the driver is active, it is active if it is assigned to a bus
    def is_active(self):
        return self.is_assigned_to_bus()
    
    # check if the driver is inactive, it is inactive if it is unassigned to a bus
    def is_inactive(self):
        return self.is_unassigned_to_bus()
    
    # assign the driver to a bus
    def assign_to_bus(self, bus_id):
        if not self.is_valid_bus_id():
            return "Cannot assign driver to bus. The bus_id is not valid."
        self.bus_id = bus_id
        return f"Driver {self.driver_code} has been assigned to bus {bus_id}."
    
    # unassign the driver from a bus
    def unassign_from_bus(self):
        self.bus_id = None
        return f"Driver {self.driver_code} has been unassigned from the bus."
    
    # check if the driver is valid, which means it has a valid user_id and a valid bus_id (if assigned to a bus)
    def is_valid_driver(self):
        if not self.is_valid_user_id():
            return "Invalid driver. The user_id is not valid."
        if self.is_assigned_to_bus() and not self.is_valid_bus_id():
            return "Invalid driver. The bus_id is not valid."
        return True
    
    # check if the driver is eligible for assignment to a bus, which means it is not currently assigned to any bus
    def is_eligible_for_assignment_to_bus(self):
        return self.is_unassigned_to_bus()
    
    # check if the driver is eligible for unassignment from a bus, which means it is currently assigned to a bus
    def is_eligible_for_unassignment_from_bus(self):
        return self.is_assigned_to_bus()
    
    # check if the driver is eligible for both assignment and unassignment to/from a bus, which means it is valid and can be either assigned or unassigned to/from a bus
    def is_eligible_for_both_assignment_and_unassignment_to_from_bus(self):
        return self.is_valid_driver() and (self.is_eligible_for_assignment_to_bus() or self.is_eligible_for_unassignment_from_bus())
    
