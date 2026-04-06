# here it is scripts for managaing bus data in the database. 
# It includes functions for creating, retrieving, updating, and deleting bus records.


class BusRepository:
    def __init__(self, db):
        self.db = db

    def create_bus(self, bus_data):
        new_bus = Bus(**bus_data)
        self.db.session.add(new_bus)
        self.db.session.commit()
        return new_bus

    def get_bus(self, bus_id):
        return Bus.query.get(bus_id)

    def update_bus(self, bus_id, bus_data):
        bus = self.get_bus(bus_id)
        if bus:
            for key, value in bus_data.items():
                setattr(bus, key, value)
            self.db.session.commit()
            return bus
        return None

    def delete_bus(self, bus_id):
        bus = self.get_bus(bus_id)
        if bus:
            self.db.session.delete(bus)
            self.db.session.commit()
            return True
        return False