'''
this is file for checking and dealing with every rout data and also error handling for the route data from PostgreSQL database

rout entity contains:
route_id SERIAL PRIMARY KEY,
    route_code TEXT GENERATED ALWAYS AS ('route-' || id) STORED name VARCHAR(100) NOT NULL,
    starting_address VARCHAR(255),
    starting_longitude DECIMAL(10, 7),
    starting_latitude DECIMAL(10, 7),
    ending_address VARCHAR(255),
    ending_longitude DECIMAL(10, 7),
    ending_latitude DECIMAL(10, 7)
'''

import . from db

class Route(db.Model):
    __tablename__ = 'routes'

    route_id = db.Column(db.Integer, primary_key=True)
    route_code = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(100), nullable=False)
    starting_address = db.Column(db.String(255))
    starting_longitude = db.Column(db.Numeric(10, 7))
    starting_latitude = db.Column(db.Numeric(10, 7))
    ending_address = db.Column(db.String(255))
    ending_longitude = db.Column(db.Numeric(10, 7))
    ending_latitude = db.Column(db.Numeric(10, 7))

    def __repr__(self):
        return f'<Route {self.name}>'

    def __init__(self, name, starting_address=None, starting_longitude=None, starting_latitude=None,
                 ending_address=None, ending_longitude=None, ending_latitude=None):
        self.name = name
        self.starting_address = starting_address
        self.starting_longitude = starting_longitude
        self.starting_latitude = starting_latitude
        self.ending_address = ending_address
        self.ending_longitude = ending_longitude
        self.ending_latitude = ending_latitude

    def to_dict(self):
        return {
            'route_id': self.route_id,
            'route_code': self.route_code,
            'name': self.name,
            'starting_address': self.starting_address,
            'starting_longitude': float(self.starting_longitude) if self.starting_longitude else None,
            'starting_latitude': float(self.starting_latitude) if self.starting_latitude else None,
            'ending_address': self.ending_address,
            'ending_longitude': float(self.ending_longitude) if self.ending_longitude else None,
            'ending_latitude': float(self.ending_latitude) if self.ending_latitude else None
        }
    
    # checking if there is an address for the starting and ending address and return the appropriate message
    def check_address(self):
        if ({self.starting_address} == None) and ({self.ending_address} == None):
            return "No starting and ending address"
        elif {self.starting_address} == None:
            return "No starting address"
        elif {self.ending_address} == None:
            return "No ending address"
        else:
            return f"Starting address: {self.starting_address}, Ending address: {self.ending_address}"
        
    
    # checking for starting, ending address or coardinates being the same and return the appropriate message
    def check_route_validity(self):
        if (self.starting_address == self.ending_address) and (self.starting_longitude == self.ending_longitude) and (self.starting_latitude == self.ending_latitude):
            return "Invalid route: Starting and ending points are the same."
        elif((self.starting_longitude == self.ending_longitude) == (self.starting_latitude == self.ending_latitude)):
            return "Invalid route: Starting and ending coordinates are the same."
        return "Valid route."
    
    # checking if the route has valid coordinates and return the appropriate message
    def check_coordinates_validity(self):
        if self.starting_longitude is not None and (self.starting_longitude < -180 or self.starting_longitude > 180):
            return "Invalid starting longitude. Must be between -180 and 180."
        if self.starting_latitude is not None and (self.starting_latitude < -90 or self.starting_latitude > 90):
            return "Invalid starting latitude. Must be between -90 and 90."
        if self.ending_longitude is not None and (self.ending_longitude < -180 or self.ending_longitude > 180):
            return "Invalid ending longitude. Must be between -180 and 180."
        if self.ending_latitude is not None and (self.ending_latitude < -90 or self.ending_latitude > 90):
            return "Invalid ending latitude. Must be between -90 and 90."
        return "Valid coordinates."
    
    # checking if the route has valid name and return the appropriate message
    def check_name_validity(self):
        if not self.name or self.name.strip() == "":
            return "Route name cannot be empty."
        if len(self.name) > 100:
            return "Route name cannot exceed 100 characters."
        return "Valid route name."
    
    # checking if the route has valid data and return the appropriate message
    def is_valid(self):
        name_validity = self.check_name_validity()
        if name_validity != "Valid route name.":
            return name_validity
        
        coordinates_validity = self.check_coordinates_validity()
        if coordinates_validity != "Valid coordinates.":
            return coordinates_validity
        
        route_validity = self.check_route_validity()
        if route_validity != "Valid route.":
            return route_validity
        
        return "Route data is valid."

