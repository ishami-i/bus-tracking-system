# this is model for the bus, it contains all the information about the bus

from .sql import db
import re
licence_plate.pattern = r'^[A-Z]{3}\s?[0-9]{3}[A-Z]$'

class Bus(db.Model):
    __tablename__ = 'buses'
    '''
    the bus contains the following information:
    - bus_id: the unique identifier for the bus
    - bus_code: the code of bus which is made by the bus- and add the id of the bus and is aoto generated when the bus is created
    - license_plate: the license plate of the bus
    - bus_capacity: the capacity of the bus
    - bus_status: the status of the bus (e.g. active, maintenance, decommissioned)
    '''
    

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
    # the bus code and id is generated in the database when the bus is created, so we don't need to include them in the constructor
    # checking is bus is available for assigniment to a route or not, if available it should be active and not assigned to any route
    def is_assigned_to_route(self):
        if self.route_id is not None:
            return True
        else:
            return False
    
    # checking if the bus is active or not
    def is_active(self):
        if (self.bus_status == 'active'):
            return True
        elif(self.bus_status == 'miaintenace'):
            return "ths {self.license_plate} is under maintenance"
        elif(self.bus_status == 'decommissioned'):
            return "ths {self.license_plate} is decommissioned"
        else:
            return "ths {self.license_plate} has an unknown status"
        
    # checking if bus is full or not
    def is_full(self, current_passengers):
        if current_passengers >= self.bus_capacity:
            return True
        else:
            return False
        

    # check if every field of the bus is valid or not
    def is_valid(self):
        if not re.match(licence_plate.pattern, self.license_plate):
            return "Invalid license plate format. Expected format: 'ABC 123D'"
        if self.bus_capacity <= 0:
            return "Bus capacity must above 0."
        if self.bus_status not in ['active', 'maintenance', 'decommissioned']:
            return "Invalid bus status. Expected values: 'active', 'maintenance', 'decommissioned'."
        return True
    
    # check the route is the bus is ssigned to
    def get_assigned_route(self):
        if self.route_id is not None:
            return f"Bus {self.license_plate} is assigned to route {self.route_id}."
        else:
            print(f"Bus {self.license_plate} is not assigned to any route.")
            # get route assigning from the route assigning table
            # return the route assigning information
            