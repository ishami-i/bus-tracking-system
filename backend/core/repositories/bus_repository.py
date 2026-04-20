# Example: Proper Constants Definition
VALID_ROLES = {'admin', 'driver', 'passenger', 'sales', 'coordinator'}
VALID_BUS_STATUSES = {'active', 'maintenance', 'decommissioned'}
VALID_TRIP_STATUSES = {'scheduled', 'in_progress', 'completed', 'cancelled'}
VALID_EVENT_TYPES = {'tap_on', 'tap_off'}
VALID_REQUEST_STATUSES = {'pending', 'picked_up', 'cancelled'}

# Example: Reusable SELECT Fields
USER_SELECT = "user_id, user_code, name, email, telephone, role"
BUS_SELECT = "bus_id, bus_code, license_plate, bus_capacity, bus_status"
TRIP_SELECT = "trip_id, trip_code, route_id, driver_id, bus_id, starting_time, status"

# Example: Input Validation Pattern
def _validate_input(self, **kwargs):
    """Centralized validation"""
    for field, value in kwargs.items():
        if field == 'role' and value not in VALID_ROLES:
            raise ValueError(f"Invalid role: {value}")
        if field == 'email' and not self._is_valid_email(value):
            raise ValueError(f"Invalid email: {value}")            # Example: Proper Constants Definition
            VALID_ROLES = {'admin', 'driver', 'passenger', 'sales', 'coordinator'}
            VALID_BUS_STATUSES = {'active', 'maintenance', 'decommissioned'}
            VALID_TRIP_STATUSES = {'scheduled', 'in_progress', 'completed', 'cancelled'}
            VALID_EVENT_TYPES = {'tap_on', 'tap_off'}
            VALID_REQUEST_STATUSES = {'pending', 'picked_up', 'cancelled'}
            
            # Example: Reusable SELECT Fields
            USER_SELECT = "user_id, user_code, name, email, telephone, role"
            BUS_SELECT = "bus_id, bus_code, license_plate, bus_capacity, bus_status"
            TRIP_SELECT = "trip_id, trip_code, route_id, driver_id, bus_id, starting_time, status"
            
            # Example: Input Validation Pattern
            def _validate_input(self, **kwargs):
                """Centralized validation"""
                for field, value in kwargs.items():
                    if field == 'role' and value not in VALID_ROLES:
                        raise ValueError(f"Invalid role: {value}")
                    if field == 'email' and not self._is_valid_email(value):
                        raise ValueError(f"Invalid email: {value}")"""
Repository for bus model operations.

Handles all database operations related to the bus entity.
PostgreSQL buses table schema:
    - bus_id: SERIAL PRIMARY KEY
    - bus_code: TEXT GENERATED ALWAYS AS ('bus-' || bus_id) STORED
    - license_plate: VARCHAR(20) UNIQUE NOT NULL
    - bus_capacity: INT NOT NULL (CHECK > 0)
    - bus_status: VARCHAR(50) NOT NULL (IN 'active', 'maintenance', 'decommissioned')
"""

import logging
from typing import Optional, List, Tuple, Any

logger = logging.getLogger(__name__)

# Constants
VALID_BUS_STATUSES = {'active', 'maintenance', 'decommissioned'}
SELECT_FIELDS = "bus_id, bus_code, bus_capacity, license_plate, bus_status, route_id"


class BusRepository:
    """Repository for bus database operations."""

    def __init__(self, db):
        """Initialize repository with database connection."""
        self.db = db

    def _execute_update(self, query: str, params: Tuple = ()) -> None:
        """Execute an INSERT/UPDATE/DELETE query and commit."""
        cursor = None
        try:
            cursor = self.db.cursor()
            cursor.execute(query, params)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            logger.error(f"Database update failed: {str(e)}")
            raise
        finally:
            if cursor:
                cursor.close()

    def create_bus(self, bus_capacity: int, license_plate: str, bus_status: str, route_id: Optional[int] = None) -> Optional[Tuple]:
        """Create a new bus and return the bus information.
        
        Args:
            bus_capacity: Bus passenger capacity
            license_plate: Vehicle license plate
            bus_status: One of 'active', 'maintenance', 'decommissioned'
            route_id: Optional route ID assignment
            
        Returns:
            Tuple of bus data or None if creation failed
            
        Raises:
            ValueError: If bus_status is invalid
        """
        if bus_status not in VALID_BUS_STATUSES:
            raise ValueError(f"Invalid bus_status. Must be one of {VALID_BUS_STATUSES}")

        query = """
            INSERT INTO buses (bus_capacity, license_plate, bus_status, route_id)
            VALUES (%s, %s, %s, %s) RETURNING bus_id;
        """
        cursor = None
        try:
            cursor = self.db.cursor()
            cursor.execute(query, (bus_capacity, license_plate, bus_status, route_id))
            bus_id = cursor.fetchone()[0]
            self.db.commit()
            logger.info(f"Bus created: bus_id={bus_id}, license_plate={license_plate}")
            return self.get_bus_by_id(bus_id)
        except Exception as e:
            self.db.rollback()
            logger.error(f"Failed to create bus: {str(e)}")
            raise
        finally:
            if cursor:
                cursor.close()

    def get_bus_by_id(self, bus_id: int) -> Optional[Tuple]:
        """Get bus information by bus_id."""
        query = f"SELECT {SELECT_FIELDS} FROM buses WHERE bus_id = %s;"
        cursor = None
        try:
            cursor = self.db.cursor()
            cursor.execute(query, (bus_id,))
            return cursor.fetchone()
        except Exception as e:
            logger.error(f"Failed to fetch bus {bus_id}: {str(e)}")
            raise
        finally:
            if cursor:
                cursor.close()

    def get_bus_by_license_plate(self, license_plate: str) -> Optional[Tuple]:
        """Get bus information by license plate."""
        query = f"SELECT {SELECT_FIELDS} FROM buses WHERE license_plate = %s;"
        cursor = None
        try:
            cursor = self.db.cursor()
            cursor.execute(query, (license_plate,))
            return cursor.fetchone()
        except Exception as e:
            logger.error(f"Failed to fetch bus by license_plate {license_plate}: {str(e)}")
            raise
        finally:
            if cursor:
                cursor.close()

    def update_bus(self, bus_id: int, bus_capacity: Optional[int] = None,
                   license_plate: Optional[str] = None, bus_status: Optional[str] = None,
                   route_id: Optional[int] = None) -> None:
        """Update bus information. Only non-None fields are updated."""
        fields = []
        values = []

        if bus_capacity is not None:
            fields.append("bus_capacity = %s")
            values.append(bus_capacity)

        if license_plate is not None:
            fields.append("license_plate = %s")
            values.append(license_plate)

        if bus_status is not None:
            if bus_status not in VALID_BUS_STATUSES:
                raise ValueError(f"Invalid bus_status. Must be one of {VALID_BUS_STATUSES}")
            fields.append("bus_status = %s")
            values.append(bus_status)

        if route_id is not None:
            fields.append("route_id = %s")
            values.append(route_id)

        if not fields:
            logger.debug(f"No fields to update for bus {bus_id}")
            return

        query = f"UPDATE buses SET {', '.join(fields)} WHERE bus_id = %s;"
        values.append(bus_id)

        try:
            self._execute_update(query, tuple(values))
            logger.info(f"Bus {bus_id} updated successfully")
        except Exception as e:
            logger.error(f"Failed to update bus {bus_id}: {str(e)}")
            raise

    def delete_bus(self, bus_id: int) -> None:
        """Delete a bus by bus_id."""
        query = "DELETE FROM buses WHERE bus_id = %s;"
        try:
            self._execute_update(query, (bus_id,))
            logger.info(f"Bus {bus_id} deleted")
        except Exception as e:
            logger.error(f"Failed to delete bus {bus_id}: {str(e)}")
            raise

    def get_all_buses(self) -> List[Tuple]:
        """Get information of all buses."""
        query = f"SELECT {SELECT_FIELDS} FROM buses;"
        cursor = None
        try:
            cursor = self.db.cursor()
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            logger.error(f"Failed to fetch all buses: {str(e)}")
            raise
        finally:
            if cursor:
                cursor.close()

    def get_buses_by_status(self, bus_status: str) -> List[Tuple]:
        """Get all buses with a specific status."""
        if bus_status not in VALID_BUS_STATUSES:
            raise ValueError(f"Invalid bus_status. Must be one of {VALID_BUS_STATUSES}")

        query = f"SELECT {SELECT_FIELDS} FROM buses WHERE bus_status = %s;"
        cursor = None
        try:
            cursor = self.db.cursor()
            cursor.execute(query, (bus_status,))
            return cursor.fetchall()
        except Exception as e:
            logger.error(f"Failed to fetch buses with status {bus_status}: {str(e)}")
            raise
        finally:
            if cursor:
                cursor.close()

    def get_active_buses(self) -> List[Tuple]:
        """Get all active buses."""
        return self.get_buses_by_status('active')

    def get_buses_in_maintenance(self) -> List[Tuple]:
        """Get all buses in maintenance."""
        return self.get_buses_by_status('maintenance')

    def get_decommissioned_buses(self) -> List[Tuple]:
        """Get all decommissioned buses."""
        return self.get_buses_by_status('decommissioned')

    def get_buses_by_route_id(self, route_id: int) -> List[Tuple]:
        """Get all buses assigned to a specific route."""
        query = f"SELECT {SELECT_FIELDS} FROM buses WHERE route_id = %s;"
        cursor = None
        try:
            cursor = self.db.cursor()
            cursor.execute(query, (route_id,))
            return cursor.fetchall()
        except Exception as e:
            logger.error(f"Failed to fetch buses for route {route_id}: {str(e)}")
            raise
        finally:
            if cursor:
                cursor.close()