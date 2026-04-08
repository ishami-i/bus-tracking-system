'''
This model python code is their for bus stops in-between routes.
some stops might be shared between routes, and some might be unique to a specific route.
the stop entity contains following attributes:
TABLE stops (
    stop_id SERIAL PRIMARY KEY,
    stop_code TEXT GENERATED ALWAYS AS ('stop-' || id) STORED stop_name VARCHAR(100) NOT NULL,
    location VARCHAR(255),
    longitude DECIMAL(10, 7),
    latitude DECIMAL(10, 7) 
    )
'''

from . import db

class Stop(db.Model):
    __tablename__ = 'stops'

    stop_id = db.Column(db.Integer, primary_key=True)
    stop_code = db.Column(db.String(50), unique=True)
    stop_name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(255))
    longitude = db.Column(db.Numeric(10, 7))
    latitude = db.Column(db.Numeric(10, 7))

    def __repr__(self):
        return f'<Stop {self.stop_name}>'

    def __init__(self, stop_name, location=None, longitude=None, latitude=None):
        self.stop_name = stop_name
        self.location = location
        self.longitude = longitude
        self.latitude = latitude

    def to_dict(self):
        return {
            'stop_id': self.stop_id,
            'stop_code': self.stop_code,
            'stop_name': self.stop_name,
            'location': self.location,
            'longitude': str(self.longitude),
            'latitude': str(self.latitude)
        }
    
    # Check if stop is shared between routes (this would require a relationship to routes, which is not defined here)
    def is_shared_between_routes(self):
        # This is a placeholder implementation. You would need to define the relationship between stops and routes to implement this properly.
        return False
    
    # Check if stop is unique to a specific route (this would also require a relationship to routes)
    def is_unique_to_route(self):
        # This is a placeholder implementation. You would need to define the relationship between stops and routes to implement this properly.
        return False
    
    # check for the validity of the stop name
    def is_valid_stop_name(self):
        if not self.stop_name or len(self.stop_name) > 100:
            return "Invalid stop name. It must be between 1 and 100 characters."
        return True
    
    # check for the validity of the location
    def is_valid_location(self):
        if self.location and len(self.location) > 255:
            return "Invalid location. It must be less than 255 characters."
        return True
    
    # check for the validity of the longitude and latitude
    def is_valid_coordinates(self):
        if self.longitude is not None and (self.longitude < -180 or self.longitude > 180):
            return "Invalid longitude. It must be between -180 and 180."
        if self.latitude is not None and (self.latitude < -90 or self.latitude > 90):
            return "Invalid latitude. It must be between -90 and 90."
        return True
    
    # Validate the stop data
    def is_valid(self):
        name_validation = self.is_valid_stop_name()
        if name_validation is not True:
            return name_validation
        
        location_validation = self.is_valid_location()
        if location_validation is not True:
            return location_validation
        
        coordinates_validation = self.is_valid_coordinates()
        if coordinates_validation is not True:
            return coordinates_validation
        
        return True
    # Get the full stop information as a string
    def get_full_stop_info(self):
        return f"Stop Name: {self.stop_name}, Location: {self.location}, Coordinates: ({self.latitude}, {self.longitude})"
    
    # Update the stop information
    def update_stop_info(self, stop_name=None, location=None, longitude=None, latitude=None):
        if stop_name is not None:
            self.stop_name = stop_name
        if location is not None:
            self.location = location
        if longitude is not None:
            self.longitude = longitude
        if latitude is not None:
            self.latitude = latitude
        return f"Stop {self.stop_name} information has been updated."
    
    # Get the stop's location as a tuple of (latitude, longitude)
    def get_stop_location(self):
        return (self.latitude, self.longitude)

    