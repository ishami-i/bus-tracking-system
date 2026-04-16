'''
this is the repository for the trip model, it contains all the database operations related to the trip model
the trip looks like this:
TABLE trips (
    trip_id SERIAL PRIMARY KEY,
    trip_code TEXT GENERATED ALWAYS AS ('trip-' || id) STORED route_id INT REFERENCES routes (route_id) ON DELETE SET NULL,
    driver_id INT REFERENCES drivers (driver_id) ON DELETE SET NULL,
    event_id INT, -- FK to passenger_events (set after table creation)
    starting_time TIMESTAMP NOT NULL,
    status VARCHAR(50) NOT NULL -- e.g. 'scheduled', 'in_progress', 'completed', 'cancelled'
);

this is what followes after the models in model directory, the trip repository contains all the database operations related to the trip model, 
such as creating a new trip, updating a trip, deleting a trip, and getting a trip by id or by driver id.
'''
class TripRepository:
    def __init__(self, db):
        self.db = db

    # creating a new trip
    def create_trip(self, route_id, driver_id, starting_time, status):
        query = """
        INSERT INTO trips (route_id, driver_id, starting_time, status)
        VALUES (%s, %s, %s, %s)
        RETURNING trip_id;
        """

        try:
            cursor = self.db.cursor()
            cursor.execute(query, (route_id, driver_id, starting_time, status))

            # get generated id
            trip_id = cursor.fetchone()[0]

            # commit transaction
            self.db.commit()

            # fetch full trip
            return self.get_trip_by_id(trip_id)

        except Exception as e:
            self.db.rollback()
            print("Error creating trip:", e)
            return None
        
    # getting a trip by id
    def get_trip_by_id(self, trip_id):
        query = """
        SELECT trip_id, trip_code, route_id, driver_id, event_id, starting_time, status
        FROM trips
        WHERE trip_id = %s;
        """

        try:
            cursor = self.db.cursor()
            cursor.execute(query, (trip_id,))
            row = cursor.fetchone()

            if row:
                return {
                    "trip_id": row[0],
                    "trip_code": row[1],
                    "route_id": row[2],
                    "driver_id": row[3],
                    "event_id": row[4],
                    "starting_time": row[5],
                    "status": row[6]
                }
            else:
                return None

        except Exception as e:
            print("Error fetching trip by id:", e)
            return None
        
    # updating trip data by id
    def update_trip(self, trip_id, route_id=None, driver_id=None, starting_time=None, status=None):
        query = """
        UPDATE trips
        SET route_id = COALESCE(%s, route_id),
            driver_id = COALESCE(%s, driver_id),
            starting_time = COALESCE(%s, starting_time),
            status = COALESCE(%s, status)
        WHERE trip_id = %s
        RETURNING trip_id;
        """

        try:
            cursor = self.db.cursor()
            cursor.execute(query, (route_id, driver_id, starting_time, status, trip_id))

            # get updated id
            updated_trip_id = cursor.fetchone()[0]

            # commit transaction
            self.db.commit()

            # fetch full trip
            return self.get_trip_by_id(updated_trip_id)

        except Exception as e:
            self.db.rollback()
            print("Error updating trip:", e)
            return None
    # deleting a trip by id
    def delete_trip(self, trip_id):
        query = """
        DELETE FROM trips
        WHERE trip_id = %s;
        """

        try:
            cursor = self.db.cursor()
            cursor.execute(query, (trip_id,))

            # commit transaction
            self.db.commit()

            return True

        except Exception as e:
            self.db.rollback()
            print("Error deleting trip:", e)
            return False
        
    # getting all trips by driver id
    def get_trips_by_driver_id(self, driver_id):
        query = """
        SELECT trip_id, trip_code, route_id, driver_id, event_id, starting_time, status
        FROM trips
        WHERE driver_id = %s;
        """

        try:
            cursor = self.db.cursor()
            cursor.execute(query, (driver_id,))
            rows = cursor.fetchall()

            trips = []
            for row in rows:
                trips.append({
                    "trip_id": row[0],
                    "trip_code": row[1],
                    "route_id": row[2],
                    "driver_id": row[3],
                    "event_id": row[4],
                    "starting_time": row[5],
                    "status": row[6]
                })

            return trips

        except Exception as e:
            print("Error fetching trips by driver id:", e)
            return []
    
    # patch on existing trip, only update the fields that are provided
    def patch_trip(self, trip_id, route_id=None, driver_id=None, starting_time=None, status=None):
        query = """
        UPDATE trips
        SET route_id = COALESCE(%s, route_id),
            driver_id = COALESCE(%s, driver_id),
            starting_time = COALESCE(%s, starting_time),
            status = COALESCE(%s, status)
        WHERE trip_id = %s
        RETURNING trip_id;
        """

        try:
            cursor = self.db.cursor()
            cursor.execute(query, (route_id, driver_id, starting_time, status, trip_id))

            # get updated id
            updated_trip_id = cursor.fetchone()[0]

            # commit transaction
            self.db.commit()

            # fetch full trip
            return self.get_trip_by_id(updated_trip_id)

        except Exception as e:
            self.db.rollback()
            print("Error patching trip:", e)
            return None
        
    # getting all trips
    def get_all_trips(self):
        query = """
        SELECT trip_id, trip_code, route_id, driver_id, event_id, starting_time, status
        FROM trips;
        """

        try:
            cursor = self.db.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()

            trips = []
            for row in rows:
                trips.append({
                    "trip_id": row[0],
                    "trip_code": row[1],
                    "route_id": row[2],
                    "driver_id": row[3],
                    "event_id": row[4],
                    "starting_time": row[5],
                    "status": row[6]
                })

            return trips

        except Exception as e:
            print("Error fetching all trips:", e)
            return []
        
    # getting all trips by status
    def get_trips_by_status(self, status):
        query = """
        SELECT trip_id, trip_code, route_id, driver_id, event_id, starting_time, status
        FROM trips
        WHERE status = %s;
        """

        try:
            cursor = self.db.cursor()
            cursor.execute(query, (status,))
            rows = cursor.fetchall()

            trips = []
            for row in rows:
                trips.append({
                    "trip_id": row[0],
                    "trip_code": row[1],
                    "route_id": row[2],
                    "driver_id": row[3],
                    "event_id": row[4],
                    "starting_time": row[5],
                    "status": row[6]
                })

            return trips

        except Exception as e:
            print("Error fetching trips by status:", e)
            return []
        
    # getting all trips by route id
    def get_trips_by_route_id(self, route_id):
        query = """
        SELECT trip_id, trip_code, route_id, driver_id, event_id, starting_time, status
        FROM trips
        WHERE route_id = %s;
        """

        try:
            cursor = self.db.cursor()
            cursor.execute(query, (route_id,))
            rows = cursor.fetchall()

            trips = []
            for row in rows:
                trips.append({
                    "trip_id": row[0],
                    "trip_code": row[1],
                    "route_id": row[2],
                    "driver_id": row[3],
                    "event_id": row[4],
                    "starting_time": row[5],
                    "status": row[6]
                })

            return trips

        except Exception as e:
            print("Error fetching trips by route id:", e)
            return []
        
    # getting all trips by event id
    def get_trips_by_event_id(self, event_id):
        query = """
        SELECT trip_id, trip_code, route_id, driver_id, event_id, starting_time, status
        FROM trips
        WHERE event_id = %s;
        """

        try:
            cursor = self.db.cursor()
            cursor.execute(query, (event_id,))
            rows = cursor.fetchall()

            trips = []
            for row in rows:
                trips.append({
                    "trip_id": row[0],
                    "trip_code": row[1],
                    "route_id": row[2],
                    "driver_id": row[3],
                    "event_id": row[4],
                    "starting_time": row[5],
                    "status": row[6]
                })

            return trips

        except Exception as e:
            print("Error fetching trips by event id:", e)
            return []
        
    # getting all trips by starting time range
    def get_trips_by_starting_time_range(self, start_time, end_time):
        query = """
        SELECT trip_id, trip_code, route_id, driver_id, event_id, starting_time, status
        FROM trips
        WHERE starting_time >= %s AND starting_time <= %s;
        """

        try:
            cursor = self.db.cursor()
            cursor.execute(query, (start_time, end_time))
            rows = cursor.fetchall()

            trips = []
            for row in rows:
                trips.append({
                    "trip_id": row[0],
                    "trip_code": row[1],
                    "route_id": row[2],
                    "driver_id": row[3],
                    "event_id": row[4],
                    "starting_time": row[5],
                    "status": row[6]
                })

            return trips

        except Exception as e:
            print("Error fetching trips by starting time range:", e)
            return []
        
    # getting all trips by driver id and status
    def get_trips_by_driver_id_and_status(self, driver_id, status):
        query = """
        SELECT trip_id, trip_code, route_id, driver_id, event_id, starting_time, status
        FROM trips
        WHERE driver_id = %s AND status = %s;
        """

        try:
            cursor = self.db.cursor()
            cursor.execute(query, (driver_id, status))
            rows = cursor.fetchall()

            trips = []
            for row in rows:
                trips.append({
                    "trip_id": row[0],
                    "trip_code": row[1],
                    "route_id": row[2],
                    "driver_id": row[3],
                    "event_id": row[4],
                    "starting_time": row[5],
                    "status": row[6]
                })

            return trips

        except Exception as e:
            print("Error fetching trips by driver id and status:", e)
            return []
        
    # getting all trips by route id and status
    def get_trips_by_route_id_and_status(self, route_id, status):
        query = """
        SELECT trip_id, trip_code, route_id, driver_id, event_id, starting_time, status
        FROM trips
        WHERE route_id = %s AND status = %s;
        """

        try:
            cursor = self.db.cursor()
            cursor.execute(query, (route_id, status))
            rows = cursor.fetchall()

            trips = []
            for row in rows:
                trips.append({
                    "trip_id": row[0],
                    "trip_code": row[1],
                    "route_id": row[2],
                    "driver_id": row[3],
                    "event_id": row[4],
                    "starting_time": row[5],
                    "status": row[6]
                })

            return trips

        except Exception as e:
            print("Error fetching trips by route id and status:", e)
            return []
        
    # getting all trips by event id and status
    def get_trips_by_event_id_and_status(self, event_id, status):
        query = """
        SELECT trip_id, trip_code, route_id, driver_id, event_id, starting_time, status
        FROM trips
        WHERE event_id = %s AND status = %s;
        """

        try:
            cursor = self.db.cursor()
            cursor.execute(query, (event_id, status))
            rows = cursor.fetchall()

            trips = []
            for row in rows:
                trips.append({
                    "trip_id": row[0],
                    "trip_code": row[1],
                    "route_id": row[2],
                    "driver_id": row[3],
                    "event_id": row[4],
                    "starting_time": row[5],
                    "status": row[6]
                })

            return trips

        except Exception as e:
            print("Error fetching trips by event id and status:", e)
            return []
        
    # getting all trips by starting time range and status
    def get_trips_by_starting_time_range_and_status(self, start_time, end_time, status):
        query = """
        SELECT trip_id, trip_code, route_id, driver_id, event_id, starting_time, status
        FROM trips
        WHERE starting_time >= %s AND starting_time <= %s AND status = %s;
        """

        try:
            cursor = self.db.cursor()
            cursor.execute(query, (start_time, end_time, status))
            rows = cursor.fetchall()

            trips = []
            for row in rows:
                trips.append({
                    "trip_id": row[0],
                    "trip_code": row[1],
                    "route_id": row[2],
                    "driver_id": row[3],
                    "event_id": row[4],
                    "starting_time": row[5],
                    "status": row[6]
                })

            return trips

        except Exception as e:
            print("Error fetching trips by starting time range and status:", e)
            return []