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
    
    # Check if bus is under maintenance
    def is_under_maintenance(self):
        return self.bus_status == 'maintenance'
    
    # Check if bus is decommissioned
    def is_decommissioned(self):
        return self.bus_status == 'decommissioned'
    
    # Check if bus is available for assignment
    def is_available_for_assignment(self):
        return self.is_active() and not self.is_assigned_to_route()
    
    # Check if bus can be assigned to a route
    def can_be_assigned_to_route(self):
        if not self.is_active():
            return f"Bus {self.license_plate} is not active and cannot be assigned to a route."
        
        if self.is_assigned_to_route():
            return f"Bus {self.license_plate} is already assigned to a {self.route_name}."
        return True
    
    # Check if bus can be unassigned from a route
    def can_be_unassigned_from_route(self):
        if self.is_assigned_to_route():
            return True
        return f"Bus {self.license_plate} is not assigned to any route and cannot be unassigned."
    
    # Check if bus can be updated to a new status
    def can_be_updated_to_status(self, new_status):
        if new_status not in ['active', 'maintenance', 'decommissioned']:
            return "Invalid bus status. Expected values: 'active', 'maintenance', 'decommissioned'."
        return True
    
    # update bus information
    def update_bus_info(self, license_plate=None, bus_capacity=None, bus_status=None, route_id=None):
        if license_plate is not None:
            if not re.match(LICENSE_PLATE_PATTERN, license_plate):
                return "Invalid license plate format. Expected format: 'ABC 123D'"
            self.license_plate = license_plate
        
        if bus_capacity is not None:
            if bus_capacity <= 0:
                return "Bus capacity must be greater than 0."
            self.bus_capacity = bus_capacity
        
        if bus_status is not None:
            if bus_status not in ['active', 'maintenance', 'decommissioned']:
                return "Invalid bus status. Expected values: 'active', 'maintenance', 'decommissioned'."
            self.bus_status = bus_status
        
        if route_id is not None:
            self.route_id = route_id
        
        return f"Bus {self.license_plate} information has been updated."
    
    # update bus capacity
    def update_bus_capacity(self, new_capacity):
        if new_capacity <= 0:
            return "Bus capacity must be greater than 0."
        self.bus_capacity = new_capacity
        return f"Bus {self.license_plate} capacity has been updated to {new_capacity}."
    
    # update bus license plate
    def update_bus_license_plate(self, new_license_plate):
        if not re.match(LICENSE_PLATE_PATTERN, new_license_plate):
            return "Invalid license plate format. Expected format: 'ABC 123D'"
        self.license_plate = new_license_plate
        return f"Bus {self.license_plate} license plate has been updated to {new_license_plate}."
    
    # update bus status
    def update_bus_status(self, new_status):
        if new_status not in ['active', 'maintenance', 'decommissioned']:
            return "Invalid bus status. Expected values: 'active', 'maintenance', 'decommissioned'."
        self.bus_status = new_status
        return f"Bus {self.license_plate} status has been updated to {new_status}."
    
    # update bus route assignment
    def update_bus_route_assignment(self, new_route_id):
        self.route_id = new_route_id
        return f"Bus {self.license_plate} route assignment has been updated to route {new_route_id}."
    
    # delete bus
    def delete_bus(self):
        db.session.delete(self)
        db.session.commit()
        return f"Bus {self.license_plate} has been deleted from the system."
    
    # check if bus can be deleted
    def can_be_deleted(self):
        if self.is_assigned_to_route():
            return f"Bus {self.license_plate} is currently assigned to a route and cannot be deleted."
        return True
    
    # check if bus can be updated
    def can_be_updated(self):
        if self.is_assigned_to_route():
            return f"Bus {self.license_plate} is currently assigned to a route and cannot be updated."
        return True
    
    # check if bus can be assigned to a route
    def can_be_assigned_to_route(self):
        if not self.is_active():
            return f"Bus {self.license_plate} is not active and cannot be assigned to a route."
        
        if self.is_assigned_to_route():
            return f"Bus {self.license_plate} is already assigned to {self.route_name} route."
        return True
    
    # check if bus can be unassigned from a route
    def can_be_unassigned_from_route(self):
        if self.is_assigned_to_route():
            return True
        return f"Bus {self.license_plate} is not assigned to any route and cannot be unassigned."
    
    # check if bus can be updated to a new status
    def can_be_updated_to_status(self, new_status):
        if new_status not in ['active', 'maintenance', 'decommissioned']:
            return "Invalid bus status. Expected values: 'active', 'maintenance', 'decommissioned'."
        return True
    
    # check if bus can be updated to a new capacity
    def can_be_updated_to_capacity(self, new_capacity):
        if new_capacity <= 0:
            return "Bus capacity must be greater than 0."
        return True