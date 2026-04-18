'''
this repository for passenger model, it will handle all the database operations related to passenger
the postgresql passenger table looks like this:
 TABLE passengers (
    passenger_id SERIAL PRIMARY KEY,
    passenger_code TEXT GENERATED ALWAYS AS ('passenger-' || passenger_id) STORED,
    user_id INT NOT NULL REFERENCES users (user_id) ON DELETE CASCADE,
    tap_go_number VARCHAR(50) UNIQUE
);
'''

import logging
from typing import Optional, Tuple, List, Any

logger = logging.getLogger(__name__)

# constants
SELECT_FIELDS = "bus_id, bus_code, bus_capacity, license_plate, bus_status, route_id"

class PassengerRepository:
    def __init__(self, db):
        """Initialize repository with database connection."""
        self.db = db

    def create_passenger(self, user_id: int, tap_go_number: Optional[str] = None) -> Optional[Tuple]:
        """Create a new passenger and return the passenger information.
        
        Args:
            user_id: The ID of the user associated with the passenger
            tap_go_number: Optional unique tap-go number for the passenger

        Returns:
            Tuple of passenger data or None if creation failed
        """
        cursor = None
        try:
            cursor = self.db.cursor()
            query = """
                INSERT INTO passengers (user_id, tap_go_number)
                VALUES (%s, %s)
                RETURNING passenger_id, passenger_code, user_id, tap_go_number
            """
            cursor.execute(query, (user_id, tap_go_number))
            passenger = cursor.fetchone()
            self.db.commit()
            return passenger
        except Exception as e:
            self.db.rollback()
            logger.error(f"Database insert failed: {str(e)}")
            raise
        finally:
            if cursor:
                cursor.close()

    def get_passenger_by_id(self, passenger_id: int) -> Optional[Tuple]:
        """Retrieve passenger information by passenger ID.
        
        Args:
            passenger_id: The ID of the passenger to retrieve

        Returns:
            Tuple of passenger data or None if not found
        """
        cursor = None
        try:
            cursor = self.db.cursor()
            query = """
                SELECT passenger_id, passenger_code, user_id, tap_go_number
                FROM passengers
                WHERE passenger_id = %s
            """
            cursor.execute(query, (passenger_id,))
            return cursor.fetchone()
        except Exception as e:
            logger.error(f"Database query failed: {str(e)}")
            raise
        finally:
            if cursor:
                cursor.close()

    def get_passenger_by_tap_go_number(self, tap_go_number: str) -> Optional[Tuple]:
        """Retrieve passenger information by tap-go number.
        
        Args:
            tap_go_number: The tap-go number of the passenger to retrieve

        Returns:
            Tuple of passenger data or None if not found
        """
        cursor = None
        try:
            cursor = self.db.cursor()
            query = """
                SELECT passenger_id, passenger_code, user_id, tap_go_number
                FROM passengers
                WHERE tap_go_number = %s
            """
            cursor.execute(query, (tap_go_number,))
            return cursor.fetchone()
        except Exception as e:
            logger.error(f"Database query failed: {str(e)}")
            raise
        finally:
            if cursor:
                cursor.close()

    def update_passenger_tap_go_number(self, passenger_id: int, new_tap_go_number: str) -> Optional[Tuple]:
        """Update the tap-go number for a passenger.
        
        Args:
            passenger_id: The ID of the passenger to update
            new_tap_go_number: The new tap-go number to set
        returns:
            Tuple of updated passenger data or None if update failed
        """
        cursor = None
        try:
            cursor = self.db.cursor()
            query = """
                UPDATE passengers
                SET tap_go_number = %s
                WHERE passenger_id = %s
                RETURNING passenger_id, passenger_code, user_id, tap_go_number
            """
            cursor.execute(query, (new_tap_go_number, passenger_id))
            updated_passenger = cursor.fetchone()
            self.db.commit()
            return updated_passenger
        except Exception as e:
            self.db.rollback()
            logger.error(f"Database update failed: {str(e)}")
            raise
        finally:
            if cursor:
                cursor.close()

    def get_all_passengers(self) -> List[Tuple]:
        """Retrieve all passengers from the database.
        
        Returns:
            List of tuples containing passenger data
        """
        cursor = None
        try:
            cursor = self.db.cursor()
            query = """
                SELECT passenger_id, passenger_code, user_id, tap_go_number
                FROM passengers 
            """
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            logger.error(f"Database query failed: {str(e)}")
            raise
        finally:
            if cursor:
                cursor.close()

    def delete_passenger(self, passenger_id: int) -> None:
        """Delete a passenger from the database.
        
        Args:
            passenger_id: The ID of the passenger to delete
        """
        cursor = None
        try:
            cursor = self.db.cursor()
            query = """
                DELETE FROM passengers
                WHERE passenger_id = %s
            """
            cursor.execute(query, (passenger_id,))
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            logger.error(f"Database delete failed: {str(e)}")
            raise
        finally:
            if cursor:
                cursor.close()