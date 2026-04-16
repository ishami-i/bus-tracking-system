'''
this is repository for bus model, it contains all the database operations related to bus model
the bus entity looks like this:
TABLE buses (
    bus_id SERIAL PRIMARY KEY,
    bus_code TEXT GENERATED ALWAYS AS ('bus-' || id) STORED bus_plate VARCHAR(20) UNIQUE NOT NULL,
    bus_capacity INT NOT NULL,
    license_number VARCHAR(10) UNIQUE NOT NULL,
    bus_status VARCHAR(50) NOT NULL, -- e.g. 'active', 'maintenance', 'decommissioned'
    route_id INT REFERENCES routes (route_id) ON DELETE SET NULL
);
'''

class BusRepository:
    