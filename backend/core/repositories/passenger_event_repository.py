'''
this is the repository for events happening throught the trip by users 
the postgresql entity looks like this:
CREATE TABLE passenger_events (
    event_id SERIAL PRIMARY KEY,
    event_code TEXT GENERATED ALWAYS AS ('event-' || event_id) STORED,
    trip_id INT NOT NULL REFERENCES trips (trip_id) ON DELETE CASCADE,
    passenger_id INT NOT NULL REFERENCES passengers (passenger_id) ON DELETE CASCADE,
    event_type VARCHAR(50) NOT NULL CHECK (
        event_type IN ('tap_on', 'tap_off')
    ),
    event_time TIMESTAMP NOT NULL DEFAULT NOW()
);
'''

import logging
from typing import Optional, Tuple

logger = logging.getLogger(__name__)

# constants
SELECT_FIELDS = "event_id, event_code, trip_id, passenger_id, event_type, event_time"

class PassengerEventRepository:
    def __init__(self, db):
        """Initialize repository with database connection."""
        self.db = db

    def create_passenger_event(self, trip_id: int, passenger_id: int, event_type: str) -> Optional[tuple]:
        """Create a new passenger event and return the event information.
        
        Args:
            trip_id: The ID of the trip associated with the event
            passenger_id: The ID of the passenger associated with the event
            event_type: One of 'tap_on' or 'tap_off'
        returns:
            Tuple of passenger event data or None if creation failed
        """
        if event_type not in {'tap_on', 'tap_off'}:
            raise ValueError("Invalid event type. Must be 'tap_on' or 'tap_off'.")
        
        query = """
            INSERT INTO passenger_events (trip_id, passenger_id, event_type)
            VALUES (%s, %s, %s) RETURNING event_id, event_code, trip_id, passenger_id, event_type, event_time;
        """
        cursor = None
        try:
            cursor = self.db.cursor()
            cursor.execute(query, (trip_id, passenger_id, event_type))
            passenger_event = cursor.fetchone()
            self.db.commit()
            return passenger_event
        except Exception as e:
            self.db.rollback()
            logger.error(f"Database update failed: {str(e)}")
            raise
        finally:
            if cursor:
                cursor.close()

    def get_passenger_event_by_id(self, event_id: int) -> Optional[tuple]:
        """Get passenger event information by event ID.
        
        Args:
            event_id: The ID of the passenger event to retrieve
        returns:
            Tuple of passenger event data or None if not found
        """
        query = f"""
            SELECT {SELECT_FIELDS} FROM passenger_events
            WHERE event_id = %s;
        """
        cursor = None
        try:
            cursor = self.db.cursor()
            cursor.execute(query, (event_id,))
            passenger_event = cursor.fetchone()
            return passenger_event
        except Exception as e:
            logger.error(f"Database query failed: {str(e)}")
            raise
        finally:
            if cursor:
                cursor.close()

    def get_passenger_events_by_trip_id(self, trip_id: int) -> list:
        """Get a list of passenger events associated with a specific trip ID.
        
        Args:
            trip_id: The ID of the trip to retrieve events for
        returns:
            List of tuples, each containing passenger event data
        """
        query = f"""
            SELECT {SELECT_FIELDS} FROM passenger_events
            WHERE trip_id = %s
            ORDER BY event_time ASC;
        """
        cursor = None
        try:
            cursor = self.db.cursor()
            cursor.execute(query, (trip_id,))
            passenger_events = cursor.fetchall()
            return passenger_events
        except Exception as e:
            logger.error(f"Database query failed: {str(e)}")
            raise
        finally:
            if cursor:
                cursor.close()

    def get_passenger_events_by_passenger_id(self, passenger_id: int) -> list:
        """Get a list of passenger events associated with a specific passenger ID.
        
        Args:
            passenger_id: The ID of the passenger to retrieve events for
        returns:
            List of tuples, each containing passenger event data
        """
        query = f"""
            SELECT {SELECT_FIELDS} FROM passenger_events
            WHERE passenger_id = %s
            ORDER BY event_time ASC;
        """
        cursor = None
        try:
            cursor = self.db.cursor()
            cursor.execute(query, (passenger_id,))
            passenger_events = cursor.fetchall()
            return passenger_events
        except Exception as e:
            logger.error(f"Database query failed: {str(e)}")
            raise
        finally:
            if cursor:
                cursor.close()

    def delete_passenger_event(self, event_id: int) -> None:
        """Delete a passenger event from the database by event ID.
        
        Args:
            event_id: The ID of the passenger event to delete
        """
        query = """
            DELETE FROM passenger_events WHERE event_id = %s;
        """
        cursor = None
        try:
            cursor = self.db.cursor()
            cursor.execute(query, (event_id,))
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            logger.error(f"Database update failed: {str(e)}")
            raise
        finally:
            if cursor:
                cursor.close()

    def get_all_passenger_events(self) -> list:
        """Get a list of all passenger events in the database.
        
        returns:
            List of tuples, each containing passenger event data
        """
        query = f"""
            SELECT {SELECT_FIELDS} FROM passenger_events
            ORDER BY event_time ASC;
        """
        cursor = None
        try:
            cursor = self.db.cursor()
            cursor.execute(query)
            passenger_events = cursor.fetchall()
            return passenger_events
        except Exception as e:
            logger.error(f"Database query failed: {str(e)}")
            raise
        finally:
            if cursor:
                cursor.close()
    def delete_passenger_events_by_trip_id(self, trip_id: int) -> None:
        """Delete all passenger events associated with a specific trip ID.
        
        Args:
            trip_id: The ID of the trip to delete events for
        """
        query = """
            DELETE FROM passenger_events WHERE trip_id = %s;
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
    def delete_passenger_events_by_passenger_id(self, passenger_id: int) -> None:
        """Delete all passenger events associated with a specific passenger ID.
        
        Args:
            passenger_id: The ID of the passenger to delete events for
        """
        query = """
            DELETE FROM passenger_events WHERE passenger_id = %s;
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
    
    def delete_passenger_events_by_event_type(self, event_type: str) -> None:
        """Delete all passenger events associated with a specific event type.
        
        Args:
            event_type: The type of event to delete (e.g., 'tap_on' or 'tap_off')
        """
        if event_type not in {'tap_on', 'tap_off'}:
            raise ValueError("Invalid event type. Must be 'tap_on' or 'tap_off'.")
        
        query = """
            DELETE FROM passenger_events WHERE event_type = %s;
        """
        cursor = None
        try:
            cursor = self.db.cursor()
            cursor.execute(query, (event_type,))
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            logger.error(f"Database update failed: {str(e)}")
            raise
        finally:
            if cursor:
                cursor.close()
    def get_passenger_events_by_event_type(self, event_type: str) -> list:
        """Get a list of passenger events associated with a specific event type.
        
        Args:
            event_type: The type of event to retrieve (e.g., 'tap_on' or 'tap_off')
        returns:
            List of tuples, each containing passenger event data
        """
        if event_type not in {'tap_on', 'tap_off'}:
            raise ValueError("Invalid event type. Must be 'tap_on' or 'tap_off'.")
        
        query = f"""
            SELECT {SELECT_FIELDS} FROM passenger_events
            WHERE event_type = %s
            ORDER BY event_time ASC;
        """
        cursor = None
        try:
            cursor = self.db.cursor()
            cursor.execute(query, (event_type,))
            passenger_events = cursor.fetchall()
            return passenger_events
        except Exception as e:
            logger.error(f"Database query failed: {str(e)}")
            raise
        finally:
            if cursor:
                cursor.close()