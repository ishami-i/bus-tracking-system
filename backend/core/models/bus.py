# this is model for the bus, it contains all the information about the bus

from .sql import db

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