# this is model for the bus, it contains all the information about the bus from PostgreSQL database

from . import db
import re

# Proper regex pattern definition
LICENSE_PLATE_PATTERN = r'^[A-Z]{3}\s?[0-9]{3}[A-Z]$'


class Bus(db.Model):
    __tablename__ = 'buses'

    '''
    The bus contains the following information:
    - bus_id: the unique identifier for the bus
    - bus_code: the code of bus which is made by the system and includes the id
    - license_plate: the license plate of the bus
    - bus_capacity: the capacity of the bus
    - bus_status: the status of the bus (e.g. active, maintenance, decommissioned)
    '''

    # Assuming ORM fields (adjust if already defined elsewhere)
    bus_id = db.Column(db.Integer, primary_key=True)
    bus_code = db.Column(db.String(50), unique=True)
    license_plate = db.Column(db.String(20), unique=True, nullable=False)
    bus_capacity = db.Column(db.Integer, nullable=False)
    bus_status = db.Column(db.String(20), nullable=False)
    route_id = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f'<Bus {self.license_plate}>'

    def __init__(self, license_plate, bus_capacity, bus_status, route_id=None):
        self.license_plate = license_plate
        self.bus_capacity = bus_capacity
        self.bus_status = bus_status
        self.route_id = route_id

    def to_dict(self):
        return {
            'bus_id': self.bus_id,
            'bus_code': self.bus_code,
            'license_plate': self.license_plate,
            'bus_capacity': self.bus_capacity,
            'bus_status': self.bus_status,
            'route_id': self.route_id
        }

    # Check if bus is assigned to a route
    def is_assigned_to_route(self):
        return self.route_id is not None

    # Check if bus is active
    def is_active(self):
        return self.bus_status == 'active'

    # Check if bus is full
    def is_full(self, current_passengers):
        return current_passengers >= self.bus_capacity

    # Validate bus data
    def is_valid(self):
        if not re.match(LICENSE_PLATE_PATTERN, self.license_plate):
            return "Invalid license plate format. Expected format: 'ABC 123D'"

        if self.bus_capacity <= 0:
            return "Bus capacity must be greater than 0."

        if self.bus_status not in ['active', 'maintenance', 'decommissioned']:
            return "Invalid bus status. Expected values: 'active', 'maintenance', 'decommissioned'."

        return True

    # Get assigned route
    def get_assigned_route(self):
        if self.route_id is not None:
            return f"Bus {self.license_plate} is assigned to route {self.route_id}."
        return f"Bus {self.license_plate} is not assigned to any route."

    # Assign bus to route
    def assign_to_route(self, route_id):
        if not self.is_active():
            return f"Bus {self.license_plate} is not active and cannot be assigned to a route."

        if self.is_assigned_to_route():
            return f"Bus {self.license_plate} is already assigned to a route."

        self.route_id = route_id
        return f"Bus {self.license_plate} has been assigned to route {route_id}."

    # Unassign bus from route
    def unassign_from_route(self):
        if self.is_assigned_to_route():
            self.route_id = None
            return f"Bus {self.license_plate} has been unassigned from its route."

        return f"Bus {self.license_plate} is not assigned to any route and cannot be unassigned."

    # Update bus status
    def update_status(self, new_status):
        if new_status in ['active', 'maintenance', 'decommissioned']:
            self.bus_status = new_status
            return f"Bus {self.license_plate} status has been updated to {new_status}."

        return "Invalid bus status. Expected values: 'active', 'maintenance', 'decommissioned'."