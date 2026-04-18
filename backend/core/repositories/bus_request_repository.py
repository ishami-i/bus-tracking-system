'''
this is the repository for bus request, which are happening at bus stops,
the passenger can request the bus to stop at the bus stop, 
and the bus operators can see that then decide to let bus go and notify the driver 
that the bus need to stop at the bus stop.

the postgresql entity looks like this:
CREATE TABLE bus_requests (
    request_id SERIAL PRIMARY KEY,
    request_code TEXT GENERATED ALWAYS AS ('request-' || request_id) STORED,
    stop_id INT REFERENCES stops (stop_id) ON DELETE SET NULL,
    trip_id INT REFERENCES trips (trip_id) ON DELETE CASCADE,
    passenger_id INT REFERENCES passengers (passenger_id) ON DELETE CASCADE,
    request_status VARCHAR(50) CHECK (
        request_status IN (
            'pending',
            'picked_up',
            'cancelled'
        )
    ),
    request_time TIMESTAMP NOT NULL DEFAULT NOW()
);
'''

import logging
from typing import Optional, Tuple

logger = logging.getLogger(__name__)

# constants
SELECT_FIELDS = "request_id, request_code, stop_id, trip_id, passenger_id, request_status, request_time"

class BusRequestRepository:
    def __init__(self, db):
        """Initialize repository with database connection."""
        self.db = db

    def create_bus_request(self, stop_id: int, trip_id: int, passenger_id: int, request_status: str) -> Optional[tuple]:
        """Create a new bus request and return the request information.
        
        Args:
            stop_id: The ID of the bus stop where the request is made
            trip_id: The ID of the trip associated with the request
            passenger_id: The ID of the passenger making the request
            request_status: One of 'pending', 'picked_up', 'cancelled'
        returns:
            Tuple of bus request data or None if creation failed
        """
        if request_status not in {'pending', 'picked_up', 'cancelled'}:
            raise ValueError("Invalid request status. Must be 'pending', 'picked_up', or 'cancelled'.")
        
        query = """
            INSERT INTO bus_requests (stop_id, trip_id, passenger_id, request_status)
            VALUES (%s, %s, %s, %s) RETURNING request_id, request_code, stop_id, trip_id, passenger_id, request_status, request_time;
        """
        cursor = None
        try:
            cursor = self.db.cursor()
            cursor.execute(query, (stop_id, trip_id, passenger_id, request_status))
            bus_request = cursor.fetchone()
            self.db.commit()
            return bus_request
        except Exception as e:
            self.db.rollback()
            logger.error(f"Database update failed: {str(e)}")
            raise
        finally:
            if cursor:
                cursor.close()

    def get_bus_request_by_id(self, request_id: int) -> Optional[tuple]:
        """Get bus request information by request ID.
        
        Args:
            request_id: The ID of the bus request to retrieve
        returns:
            Tuple of bus request data or None if not found
        """
        query = f"""
            SELECT {SELECT_FIELDS} FROM bus_requests
            WHERE request_id = %s;
        """
        cursor = None
        try:
            cursor = self.db.cursor()
            cursor.execute(query, (request_id,))
            bus_request = cursor.fetchone()
            return bus_request
        except Exception as e:
            logger.error(f"Database query failed: {str(e)}")
            raise
        finally:
            if cursor:
                cursor.close()

    def get_bus_requests_by_trip_id(self, trip_id: int) -> list:
        """Get a list of bus requests associated with a specific trip ID.
        
        Args:
            trip_id: The ID of the trip to retrieve requests for
        returns:
            List of tuples containing bus request data
        """
        query = f"""
            SELECT {SELECT_FIELDS} FROM bus_requests
            WHERE trip_id = %s;
        """
        cursor = None
        try:
            cursor = self.db.cursor()
            cursor.execute(query, (trip_id,))
            bus_requests = cursor.fetchall()
            return bus_requests
        except Exception as e:
            logger.error(f"Database query failed: {str(e)}")
            raise
        finally:
            if cursor:
                cursor.close()

    def update_bus_request_status(self, request_id: int, new_status: str) -> Optional[tuple]:
        """Update the status of a bus request.
        
        Args:
            request_id: The ID of the bus request to update
            new_status: The new status to set ('pending', 'picked_up', 'cancelled')
        returns:
            Tuple of updated bus request data or None if update failed
        """
        if new_status not in {'pending', 'picked_up', 'cancelled'}:
            raise ValueError("Invalid request status. Must be 'pending', 'picked_up', or 'cancelled'.")
        
        query = """
            UPDATE bus_requests
            SET request_status = %s
            WHERE request_id = %s
            RETURNING request_id, request_code, stop_id, trip_id, passenger_id, request_status, request_time;
        """
        cursor = None
        try:
            cursor = self.db.cursor()
            cursor.execute(query, (new_status, request_id))
            updated_request = cursor.fetchone()
            self.db.commit()
            return updated_request
        except Exception as e:
            self.db.rollback()
            logger.error(f"Database update failed: {str(e)}")
            raise
        finally:
            if cursor:
                cursor.close()

    def auto_cancel_request(self, request_id: int) -> Optional[tuple]:
        """automatically update the request status to cancelled
        when the bus arrives at the stop and the passenger is not picked up.
        and when the passenger_id, on events shows that the passengers event is tap_off at the stop, then the request status will be updated to cancelled.
        """
        query = """
            UPDATE bus_requests
            SET request_status = 'cancelled'
            WHERE request_id = %s
            RETURNING request_id, request_code, stop_id, trip_id, passenger_id, request_status, request_time;
        """
        cursor = None
        try:
            cursor = self.db.cursor()
            cursor.execute(query, (request_id,))
            updated_request = cursor.fetchone()
            self.db.commit()
            return updated_request
        except Exception as e:
            self.db.rollback()
            logger.error(f"Database update failed: {str(e)}")
            raise
        finally:
            if cursor:
                cursor.close()

    def delete_bus_request(self, request_id: int) -> None:
        """Delete a bus request by request ID.
        
        Args:
            request_id: The ID of the bus request to delete
        """
        query = """
            DELETE FROM bus_requests WHERE request_id = %s;
        """
        cursor = None
        try:
            cursor = self.db.cursor()
            cursor.execute(query, (request_id,))
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            logger.error(f"Database update failed: {str(e)}")
            raise
        finally:
            if cursor:
                cursor.close()

    def delete_bus_requests_by_trip_id(self, trip_id: int) -> None:
        """Delete all bus requests associated with a specific trip ID.
        
        Args:
            trip_id: The ID of the trip to delete requests for
        """
        query = """
            DELETE FROM bus_requests WHERE trip_id = %s;
        """
        cursor = None
        try:
            cursor = self.db.cursor()
            cursor.execute(query, (trip_id,))
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            logger.error(f"Database update failed: {str(e)}")
            raise
        finally:
            if cursor:
                cursor.close()

    def delete_bus_requests_by_passenger_id(self, passenger_id: int) -> None:
        """Delete all bus requests associated with a specific passenger ID.
        
        Args:
            passenger_id: The ID of the passenger to delete requests for
        """
        query = """
            DELETE FROM bus_requests WHERE passenger_id = %s;
        """
        cursor = None
        try:
            cursor = self.db.cursor()
            cursor.execute(query, (passenger_id,))
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            logger.error(f"Database update failed: {str(e)}")
            raise
        finally:
            if cursor:
                cursor.close()
    
    def auto_update_based_on_event (self, stop_id: int) -> None:
        """
        Delete all bus request associated with a specific stop id.
        if the bus stop on that bus stop after the request is made, then the request will be deleted.
         example: if the request id made at stop id 1, at 11:00,
         the bus arrives at stop id 1 at 11:05, 
         then the request will be update to picked_up or cancelled,based on the event is tap_on means the 
         passenger is picked up, then the reuest will be update to picked_up, 
         else if nothing on event happened, then the request will be update to cancelled,

         if passenger is anonymous, then the request will be update to picked_up,
         because the passenger is picked up but we cannot track the passenger's event, so we will update the request to picked_up, and
         when the bus arrives at the stop, the bus operator can see that there is a request from anonymous passenger, 
         then the bus operator can decide to let the bus stop at the stop or not.
        """

        if stop_id is None:
            raise ValueError("Invalid stop_id. Must be a valid stop ID.")
        
        # update for anonymous passenger
        query_anonymous = """
            UPDATE bus_requests
            SET request_status = 'picked_up'
            WHERE stop_id = %s AND passenger_id IS NULL AND request_status = 'pending';
        """
        # update for non-anonymous passenger
        query_non_anonymous = """
            UPDATE bus_requests
            SET request_status = CASE
                WHEN EXISTS (
                    SELECT 1 FROM passenger_events
                    WHERE passenger_events.passenger_id = bus_requests.passenger_id
                    AND passenger_events.stop_id = bus_requests.stop_id
                    AND passenger_events.event_type = 'tap_on'
                ) THEN 'picked_up'
                ELSE 'cancelled'
            END
            WHERE stop_id = %s AND passenger_id IS NOT NULL AND request_status = 'pending';
        """
        cursor = None
        try:
            cursor = self.db.cursor()
            cursor.execute(query_anonymous, (stop_id,))
            cursor.execute(query_non_anonymous, (stop_id,))
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            logger.error(f"Database update failed: {str(e)}")
            raise
        finally:
            if cursor:
                cursor.close()