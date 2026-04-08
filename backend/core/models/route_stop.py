'''
this is model for connecting routes with stops, since one stop can have multiple routes 
and ano route can have multiple stops, we need a many-to-many relationship between routes and stops, this model will be used to connect the two tables in the database.

this entity contains these attributes:
TABLE route_stops (
    route_stop_id SERIAL PRIMARY KEY,
    stop_id INT NOT NULL REFERENCES stops (stop_id) ON DELETE CASCADE,
    route_id INT NOT NULL REFERENCES routes (route_id) ON DELETE CASCADE,
    stop_order INT NOT NULL
);
'''

from . import db

class RouteStop(db.Model):
    __tablename__ = 'route_stops'

    route_stop_id = db.Column(db.Integer, primary_key=True)
    stop_id = db.Column(db.Integer, db.ForeignKey('stops.stop_id', ondelete='CASCADE'), nullable=False)
    route_id = db.Column(db.Integer, db.ForeignKey('routes.route_id', ondelete='CASCADE'), nullable=False)
    stop_order = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<RouteStop Route ID: {self.route_id}, Stop ID: {self.stop_id}, Order: {self.stop_order}>'
    
    def to_dict(self):
        return {
            'route_stop_id': self.route_stop_id,
            'stop_id': self.stop_id,
            'route_id': self.route_id,
            'stop_order': self.stop_order
        }
    
    # Check if the stop is the first stop in the route
    def is_first_stop(self):
        return self.stop_order == 1
    
    # check for how many routes this stop is shared
    def shared_routes_count(self):
        return RouteStop.query.filter_by(stop_id=self.stop_id).count()
    
    # check if the stop is shared between multiple routes
    def is_shared_between_routes(self):
        return self.shared_routes_count() > 1
    
    # check if the stop is unique to a specific route
    def is_unique_to_route(self):
        return self.shared_routes_count() == 1
    
    # check for the validity of the stop order
    def is_valid_stop_order(self):
        if self.stop_order < 1:
            return "Invalid stop order. It must be a positive integer."
        return True
    
    # check if the stop order is unique within the route
    def is_unique_stop_order_within_route(self):
        existing_stop = RouteStop.query.filter_by(route_id=self.route_id, stop_order=self.stop_order).first()
        if existing_stop and existing_stop.route_stop_id != self.route_stop_id:
            return "Invalid stop order. It must be unique within the route."
        return True
    
    # check if the stop order is sequential within the route (this would require additional logic to check the existing stop orders for the route)
    def is_sequential_stop_order_within_route(self):
        existing_stops = RouteStop.query.filter_by(route_id=self.route_id).order_by(RouteStop.stop_order).all()
        expected_order = 1
        for stop in existing_stops:
            if stop.stop_order != expected_order:
                return "Invalid stop order. It must be sequential within the route."
            expected_order += 1
        return True
    # check if the stop order is valid within the route (this would require checking both the validity of the stop order and its uniqueness/sequentiality within the route)
    def is_valid_stop_order_within_route(self):
        valid_order = self.is_valid_stop_order()
        if valid_order is not True:
            return valid_order
        
        unique_order = self.is_unique_stop_order_within_route()
        if unique_order is not True:
            return unique_order
        
        sequential_order = self.is_sequential_stop_order_within_route()
        if sequential_order is not True:
            return sequential_order
        
        return True
    
    # check if the route stop is valid (this would require checking the validity of the stop order and its uniqueness/sequentiality within the route)
    def is_valid(self):
        valid_stop_order = self.is_valid_stop_order()
        if valid_stop_order is not True:
            return valid_stop_order
        
        unique_stop_order = self.is_unique_stop_order_within_route()
        if unique_stop_order is not True:
            return unique_stop_order
        
        sequential_stop_order = self.is_sequential_stop_order_within_route()
        if sequential_stop_order is not True:
            return sequential_stop_order
        
        return True
    
    # check if the route stop is shared between multiple routes (this would require checking if the stop is shared between multiple routes and if the stop order is valid within each route)
    def is_shared_between_multiple_routes(self):
        if not self.is_shared_between_routes():
            return False
        
        existing_stops = RouteStop.query.filter_by(stop_id=self.stop_id).all()
        for stop in existing_stops:
            if stop.route_id != self.route_id:
                valid_stop_order = stop.is_valid_stop_order_within_route()
                if valid_stop_order is not True:
                    return False
        
        return True
    
    # check if the route stop is unique to a specific route (this would require checking if the stop is unique to a specific route and if the stop order is valid within that route)
    def is_unique_to_specific_route(self):
        if not self.is_unique_to_route():
            return False
        
        valid_stop_order = self.is_valid_stop_order_within_route()
        if valid_stop_order is not True:
            return False
        
        return True
    
    # check if the route stop is valid for a specific route (this would require checking if the stop is valid within the route and if the stop order is valid within the route)
    def is_valid_for_specific_route(self):
        valid_stop_order = self.is_valid_stop_order_within_route()
        if valid_stop_order is not True:
            return False
        
        return True
    
    # check if the route stop is valid for multiple routes (this would require checking if the stop is valid within each route and if the stop order is valid within each route)
    def is_valid_for_multiple_routes(self):
        existing_stops = RouteStop.query.filter_by(stop_id=self.stop_id).all()
        for stop in existing_stops:
            valid_stop_order = stop.is_valid_stop_order_within_route()
            if valid_stop_order is not True:
                return False
        
        return True