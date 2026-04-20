'''
this model contains the stop repository for the handling add, updating, deleting and fetching stop data from the database
the postgresql database looks like this:
CREATE TABLE stops (
    stop_id SERIAL PRIMARY KEY,
    stop_code TEXT GENERATED ALWAYS AS ('stop-' || stop_id) STORED,
    stop_name VARCHAR(100) NOT NULL,
    location VARCHAR(255),
    longitude DECIMAL(10, 7),
    latitude DECIMAL(10, 7)
);
'''

from typing import List, Optional
import psycopg2
from psycopg2 import sql
from core.models.stop import Stop
from core.config import get_db_connection
import logging

class StopRepository:
    def __init__(self):
        self.connection = get_db_connection()
    
    # add new stop to the database
    def add_stop(self, stop: Stop) -> Optional[Stop]:
        try:
            with self.connection.cursor() as cursor:
                insert_query = sql.SQL("""
                    INSERT INTO stops (stop_name, location, longitude, latitude)
                    VALUES (%s, %s, %s, %s) RETURNING stop_id, stop_code
                """)
                cursor.execute(insert_query, (stop.stop_name, stop.location, stop.longitude, stop.latitude))
                result = cursor.fetchone()
                self.connection.commit()
                return Stop(stop_id=result[0], stop_code=result[1], stop_name=stop.stop_name,
                            location=stop.location, longitude=stop.longitude, latitude=stop.latitude)
        except Exception as e:
            logging.error(f"Error adding stop: {e}")
            self.connection.rollback()
            return None
        
    # update the existing stop in database
    def update_stop(self, stop_id: int, stop: Stop) -> Optional[Stop]:
        try:
            with self.connection.cursor() as cursor:
                update_query = sql.SQL("""
                    UPDATE stops
                    SET stop_name = %s, location = %s, longitude = %s, latitude = %s
                    WHERE stop_id = %s RETURNING stop_code
                """)
                cursor.execute(update_query, (stop.stop_name, stop.location, stop.longitude, stop.latitude, stop_id))
                result = cursor.fetchone()
                self.connection.commit()
                if result:
                    return Stop(stop_id=stop_id, stop_code=result[0], stop_name=stop.stop_name,
                                location=stop.location, longitude=stop.longitude, latitude=stop.latitude)
                return None
        except Exception as e:
            logging.error(f"Error updating stop: {e}")
            self.connection.rollback()
            return None
        
    # delete the stop from database
    def delete_stop(self, stop_id: int) -> bool:
        try:
            with self.connection.cursor() as cursor:
                delete_query = sql.SQL("DELETE FROM stops WHERE stop_id = %s")
                cursor.execute(delete_query, (stop_id,))
                self.connection.commit()
                return cursor.rowcount > 0
        except Exception as e:
            logging.error(f"Error deleting stop: {e}")
            self.connection.rollback()
            return False
        
    # fetch the stop from database by id
    def get_stop_by_id(self, stop_id: int) -> Optional[Stop]:
        try:
            with self.connection.cursor() as cursor:
                select_query = sql.SQL("SELECT stop_id, stop_code, stop_name, location, longitude, latitude FROM stops WHERE stop_id = %s")
                cursor.execute(select_query, (stop_id,))
                result = cursor.fetchone()
                if result:
                    return Stop(stop_id=result[0], stop_code=result[1], stop_name=result[2],
                                location=result[3], longitude=result[4], latitude=result[5])
                return None
        except Exception as e:
            logging.error(f"Error fetching stop by id: {e}")
            return None
        
    # fetch all stops from database
    def get_all_stops(self) -> List[Stop]:
        try:
            with self.connection.cursor() as cursor:
                select_query = sql.SQL("SELECT stop_id, stop_code, stop_name, location, longitude, latitude FROM stops")
                cursor.execute(select_query)
                results = cursor.fetchall()
                return [Stop(stop_id=row[0], stop_code=row[1], stop_name=row[2],
                             location=row[3], longitude=row[4], latitude=row[5]) for row in results]
        except Exception as e:
            logging.error(f"Error fetching all stops: {e}")
            return []
        
    # close the database connection when the repository is destroyed
    def __del__(self):
        if self.connection:
            self.connection.close()