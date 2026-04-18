'''
this is the repository for gps log, which is responsible for handling all database operations related to gps log.
the postgreSQL gps_logs table schema:
CREATE TABLE gps_logs (
    log_id SERIAL PRIMARY KEY,
    log_code TEXT GENERATED ALWAYS AS ('gpslog-' || log_id) STORED,
    latitude DECIMAL(10, 7) NOT NULL,
    longitude DECIMAL(10, 7) NOT NULL,
    recorded_at TIMESTAMP NOT NULL DEFAULT NOW(),
    bus_id INT REFERENCES buses (bus_id) ON DELETE SET NULL,
    trip_id INT REFERENCES trips (trip_id) ON DELETE SET NULL
);
'''

import logging
from typing import Optional, Tuple

logger = logging.getLogger(__name__)

# constants
SELECT_FIELDS = "log_id, log_code, latitude, longitude, recorded_at, bus_id, trip_id"

class GPSLogRepository:
    def __init__(self, db):
        """Initialize repository with database connection."""
        self.db = db

    def create_gps_log(self, latitude: float, longitude: float, bus_id: Optional[int] = None, trip_id: Optional[int] = None) -> Optional[tuple]:
        """Create a new GPS log and return the log information.
        
        Args:
            latitude: Latitude of the GPS log
            longitude: Longitude of the GPS log
            bus_id: Optional associated bus ID
            trip_id: Optional associated trip ID
        returns:
            Tuple of GPS log data or None if creation failed
        """
        query = """
            INSERT INTO gps_logs (latitude, longitude, bus_id, trip_id)
            VALUES (%s, %s, %s, %s) RETURNING log_id, log_code, latitude, longitude, recorded_at, bus_id, trip_id;
        """
        cursor = None
        try:
            cursor = self.db.cursor()
            cursor.execute(query, (latitude, longitude, bus_id, trip_id))
            gps_log = cursor.fetchone()
            self.db.commit()
            return gps_log
        except Exception as e:
            self.db.rollback()
            logger.error(f"Database update failed: {str(e)}")
            raise
        finally:
            if cursor:
                cursor.close()

    def get_gps_log_by_id(self, log_id: int) -> Optional[tuple]:
        """Get GPS log information by log ID.
        
        Args:
            log_id: The ID of the GPS log to retrieve
        returns:
            Tuple of GPS log data or None if not found
        """
        query = f"""
            SELECT {SELECT_FIELDS} FROM gps_logs
            WHERE log_id = %s;
        """
        cursor = None
        try:
            cursor = self.db.cursor()
            cursor.execute(query, (log_id,))
            gps_log = cursor.fetchone()
            return gps_log
        except Exception as e:
            logger.error(f"Database query failed: {str(e)}")
            raise
        finally:
            if cursor:
                cursor.close()

    def get_gps_logs_by_bus_id(self, bus_id: int) -> list:
        """Get a list of GPS logs associated with a specific bus ID.
        
        Args:
            bus_id: The ID of the bus to retrieve GPS logs for
        returns:
            List of tuples containing GPS log data
        """
        query = f"""
            SELECT {SELECT_FIELDS} FROM gps_logs
            WHERE bus_id = %s
            ORDER BY recorded_at DESC;
        """
        cursor = None
        try:
            cursor = self.db.cursor()
            cursor.execute(query, (bus_id,))
            gps_logs = cursor.fetchall()
            return gps_logs
        except Exception as e:
            logger.error(f"Database query failed: {str(e)}")
            raise
        finally:
            if cursor:
                cursor.close()

    def get_gps_logs_by_trip_id(self, trip_id: int) -> list:
        """Get a list of GPS logs associated with a specific trip ID.
        
        Args:
            trip_id: The ID of the trip to retrieve GPS logs for
        returns:
            List of tuples containing GPS log data
        """
        query = f"""
            SELECT {SELECT_FIELDS} FROM gps_logs
            WHERE trip_id = %s
            ORDER BY recorded_at DESC;
        """
        cursor = None
        try:
            cursor = self.db.cursor()
            cursor.execute(query, (trip_id,))
            gps_logs = cursor.fetchall()
            return gps_logs
        except Exception as e:
            logger.error(f"Database query failed: {str(e)}")
            raise
        finally:
            if cursor:
                cursor.close()
    def delete_gps_log(self, log_id: int) -> None:
        """Delete a GPS log from the database by log ID.
        
        Args:
            log_id: The ID of the GPS log to delete
        """
        query = """
            DELETE FROM gps_logs WHERE log_id = %s;
        """
        cursor = None
        try:
            cursor = self.db.cursor()
            cursor.execute(query, (log_id,))
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            logger.error(f"Database update failed: {str(e)}")
            raise
        finally:
            if cursor:
                cursor.close()

    def get_all_gps_logs(self) -> list:
        """Get a list of all GPS logs in the database.
        
        returns:
            List of tuples containing GPS log data
        """
        query = f"""
            SELECT {SELECT_FIELDS} FROM gps_logs
            ORDER BY recorded_at DESC;
        """
        cursor = None
        try:
            cursor = self.db.cursor()
            cursor.execute(query)
            gps_logs = cursor.fetchall()
            return gps_logs
        except Exception as e:
            logger.error(f"Database query failed: {str(e)}")
            raise
        finally:
            if cursor:
                cursor.close()

    def delete_gps_logs_by_bus_id(self, bus_id: int) -> None:
        """Delete all GPS logs associated with a specific bus ID.
        
        Args:
            bus_id: The ID of the bus to delete GPS logs for
        """
        query = """
            DELETE FROM gps_logs WHERE bus_id = %s;
        """
        cursor = None
        try:
            cursor = self.db.cursor()
            cursor.execute(query, (bus_id,))
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            logger.error(f"Database update failed: {str(e)}")
            raise
        finally:
            if cursor:
                cursor.close()

    def delete_gps_logs_by_trip_id(self, trip_id: int) -> None:
        """Delete all GPS logs associated with a specific trip ID.
        
        Args:
            trip_id: The ID of the trip to delete GPS logs for
        """
        query = """
            DELETE FROM gps_logs WHERE trip_id = %s;
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
    def delete_gps_logs_by_bus_id_and_trip_id(self, bus_id: int, trip_id: int) -> None:
        """Delete all GPS logs associated with a specific bus ID and trip ID.
        
        Args:
            bus_id: The ID of the bus to delete GPS logs for
            trip_id: The ID of the trip to delete GPS logs for
        """
        query = """
            DELETE FROM gps_logs WHERE bus_id = %s AND trip_id = %s;
        """
        cursor = None
        try:
            cursor = self.db.cursor()
            cursor.execute(query, (bus_id, trip_id))
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            logger.error(f"Database update failed: {str(e)}")
            raise
        finally:
            if cursor:
                cursor.close()