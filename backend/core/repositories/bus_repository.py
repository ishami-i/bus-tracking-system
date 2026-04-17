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
    def __init__(self, db):
        self.db = db
    
    # create a new bus and return the bus information
    def create_bus(self, bus_capacity, license_number, bus_status, route_id=None):
        query = """
        INSERT INTO buses (bus_capacity, license_number, bus_status, route_id)
        VALUES (%s, %s, %s, %s) RETURNING bus_id;
        """
        cursor = self.db.cursor()
        cursor.execute(query, (bus_capacity, license_number, bus_status, route_id))
        bus_id = cursor.fetchone()[0]
        self.db.commit()
        return self.get_bus_by_id(bus_id)

    # get bus information by bus_id
    def get_bus_by_id(self, bus_id):
        query = "SELECT bus_id, bus_code, bus_capacity, license_number, bus_status, route_id FROM buses WHERE bus_id = %s;"
        cursor = self.db.cursor()
        cursor.execute(query, (bus_id,))
        return cursor.fetchone()

    # get bus information by license number
    def get_bus_by_license_number(self, license_number):
        query = "SELECT bus_id, bus_code, bus_capacity, license_number, bus_status, route_id FROM buses WHERE license_number = %s;"
        cursor = self.db.cursor()
        cursor.execute(query, (license_number,))
        return cursor.fetchone()
    
    # update the bus information by bus_id, only the fields that are not None will be updated
    def update_bus(self, bus_id, bus_capacity=None, license_number=None, bus_status=None, route_id=None):
        fields = []
        values = []
        
        if bus_capacity is not None:
            fields.append("bus_capacity = %s")
            values.append(bus_capacity)
        
        if license_number is not None:
            fields.append("license_number = %s")
            values.append(license_number)
        
        if bus_status is not None:
            fields.append("bus_status = %s")
            values.append(bus_status)
        
        if route_id is not None:
            fields.append("route_id = %s")
            values.append(route_id)

        if not fields:
            return  # No fields to update

        query = f"UPDATE buses SET {', '.join(fields)} WHERE bus_id = %s;"
        values.append(bus_id)

        cursor = self.db.cursor()
        cursor.execute(query, tuple(values))
        self.db.commit()

    # delete the bus by bus_id
    def delete_bus(self, bus_id):
        query = "DELETE FROM buses WHERE bus_id = %s;"
        cursor = self.db.cursor()
        cursor.execute(query, (bus_id,))
        self.db.commit()

    # update bus with the only data provided and leave the rest of the data unchanged
    def update_bus_partial(self, bus_id, data):
        fields = []
        values = []
        
        for key, value in data.items():
            if value is not None:
                fields.append(f"{key} = %s")
                values.append(value)

        if not fields:
            return  # No fields to update

        query = f"UPDATE buses SET {', '.join(fields)} WHERE bus_id = %s;"
        values.append(bus_id)

        cursor = self.db.cursor()
        cursor.execute(query, tuple(values))
        self.db.commit()

    # get all buses information
    def get_all_buses(self):
        query = "SELECT bus_id, bus_code, bus_capacity, license_number, bus_status, route_id FROM buses;"
        cursor = self.db.cursor()
        cursor.execute(query)
        return cursor.fetchall()
    
    # get information of all buses that are active
    def get_active_buses(self):
        query = "SELECT bus_id, bus_code, bus_capacity, license_number, bus_status, route_id FROM buses WHERE bus_status = 'active';"
        cursor = self.db.cursor()
        cursor.execute(query)
        return cursor.fetchall()
    
    # get information of all buses that are in maintenance
    def get_buses_in_maintenance(self):
        query = "SELECT bus_id, bus_code, bus_capacity, license_number, bus_status, route_id FROM buses WHERE bus_status = 'maintenance';"
        cursor = self.db.cursor()
        cursor.execute(query)
        return cursor.fetchall()
    
    # get information of all buses that are decommissioned
    def get_decommissioned_buses(self):
        query = "SELECT bus_id, bus_code, bus_capacity, license_number, bus_status, route_id FROM buses WHERE bus_status = 'decommissioned';"
        cursor = self.db.cursor()
        cursor.execute(query)
        return cursor.fetchall()
    
    # get all buses information by route_id
    def get_buses_by_route_id(self, route_id):
        query = "SELECT bus_id, bus_code, bus_capacity, license_number, bus_status, route_id FROM buses WHERE route_id = %s;"
        cursor = self.db.cursor()
        cursor.execute(query, (route_id,))
        return cursor.fetchall()