''''
this is the driver repository module for the bus tracking system.
it provides functions to interact with the driver data in the database, including creating, reading, updating
and deleting driver records.
this repository interacts with the postegreSQL database using cursor, and it defines the necessary queries and operations to manage driver data effectively.
the postgresql driver entiry looks like this:

CREATE TABLE drivers (
    driver_id SERIAL PRIMARY KEY,
    driver_code TEXT GENERATED ALWAYS AS ('driver-' || driver_id) STORED,
    user_id INT NOT NULL REFERENCES users (user_id) ON DELETE CASCADE
);
'''

import logging
from typing import Optional, List

logger = logging.getLogger(__name__)

# constants
SELECT_FIELDS = "driver_id, driver_code, user_id"

class DriverRepository:
    def __init__(self, db):
        """Initialize repository with database connection."""
        self.db = db

    def create_driver(self, user_id: int) -> Optional[tuple]:
        """Create a new driver and return the driver information.
        
        Args:
            user_id: The user ID associated with the driver
        returns:
            Tuple of driver data or None if creation failed
        """
        query = """
            INSERT INTO drivers (user_id)
            VALUES (%s) RETURNING driver_id, driver_code, user_id;
        """
        cursor = None
        try:
            cursor = self.db.cursor()
            cursor.execute(query, (user_id,))
            driver = cursor.fetchone()
            self.db.commit()
            return driver
        except Exception as e:
            self.db.rollback()
            logger.error(f"Database update failed: {str(e)}")
            raise
        finally:
            if cursor:
                cursor.close()

    def get_driver_by_id(self, driver_id: int) -> Optional[tuple]:
        """Get driver information by driver ID.
        
        Args:
            driver_id: The ID of the driver to retrieve
        returns:
            Tuple of driver data or None if not found
        """
        query = f"""
            SELECT {SELECT_FIELDS} FROM drivers
            WHERE driver_id = %s;
        """
        cursor = None
        try:
            cursor = self.db.cursor()
            cursor.execute(query, (driver_id,))
            return cursor.fetchone()
        except Exception as e:
            logger.error(f"Database query failed: {str(e)}")
            raise
        finally:
            if cursor:
                cursor.close()

    def get_all_drivers(self) -> List[tuple]:
        """Get a list of all drivers in the database.
        
        returns:
            List of tuples, each containing driver data
        """
        query = f"""
            SELECT {SELECT_FIELDS} FROM drivers;
        """
        cursor = None
        try:
            cursor = self.db.cursor()
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            logger.error(f"Database query failed: {str(e)}")
            raise
        finally:
            if cursor:
                cursor.close()

    def delete_driver(self, driver_id: int) -> None:
        """Delete a driver from the database by driver ID.
        
        Args:
            driver_id: The ID of the driver to delete
        """
        query = """
            DELETE FROM drivers WHERE driver_id = %s;
        """
        cursor = None
        try:
            cursor = self.db.cursor()
            cursor.execute(query, (driver_id,))
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            logger.error(f"Database update failed: {str(e)}")
            raise
        finally:
            if cursor:
                cursor.close()

    def get_drivers_by_user_id(self, user_id: int) -> List[tuple]:
        """Get a list of drivers associated with a specific user ID.
        
        Args:
            user_id: The user ID to filter drivers by
        returns:
            List of tuples, each containing driver data for the specified user ID
        """
        query = f"""
            SELECT {SELECT_FIELDS} FROM drivers
            WHERE user_id = %s;
        """
        cursor = None
        try:
            cursor = self.db.cursor()
            cursor.execute(query, (user_id,))
            return cursor.fetchall()
        except Exception as e:
            logger.error(f"Database query failed: {str(e)}")
            raise
        finally:
            if cursor:
                cursor.close()