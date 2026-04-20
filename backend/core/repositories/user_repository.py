'''
this the repository for creating, updating, deleting, and fetching the user data from the database. 
it uses the psycopg2 library to connect to the PostgreSQL database and execute SQL queries. the repository provides methods for creating a new user, updating an existing user, deleting a user, fetching a user by id, and fetching all users. it also handles exceptions and logs errors when they occur. finally, it ensures that the database connection is closed when the repository is destroyed.
the postogresql table looks like this:
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    user_code TEXT GENERATED ALWAYS AS ('user-' || user_id) STORED,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    telephone VARCHAR(20),
    role VARCHAR(50) NOT NULL CHECK (
        role IN (
            'admin',
            'driver',
            'passenger',
            'sales',
            'coordinator'
        )
    )
);
'''

from typing import List, Optional
import psycopg2
from psycopg2 import sql
from core.models.user import User
from core.config import get_db_connection
import logging

logger = logging.getLogger(__name__)

class UserRepository:
    def __init__(self):
        self.connection = get_db_connection()
    
    # add new user with one of current roles to the database
    def add_user(self, user: User) -> Optional[User]:
        try:
            with self.connection.cursor() as cursor:
                insert_query = sql.SQL("""
                    INSERT INTO users (name, email, telephone, role)
                    VALUES (%s, %s, %s, %s) RETURNING user_id, user_code
                """)
                cursor.execute(insert_query, (user.name, user.email, user.telephone, user.role))
                result = cursor.fetchone()
                self.connection.commit()
                return User(user_id=result[0], user_code=result[1], name=user.name,
                            email=user.email, telephone=user.telephone, role=user.role)
        except Exception as e:
            logger.error(f"Error adding user: {e}")
            self.connection.rollback()
            return None
        
    # add new user with new role to the database
    def add_user_with_role(self, user: User) -> Optional[User]:
        try:
            with self.connection.cursor() as cursor:
                insert_query = sql.SQL("""
                    INSERT INTO users (name, email, telephone, role)
                    VALUES (%s, %s, %s, %s) RETURNING user_id, user_code
                """)
                cursor.execute(insert_query, (user.name, user.email, user.telephone, user.role))
                result = cursor.fetchone()
                self.connection.commit()
                return User(user_id=result[0], user_code=result[1], name=user.name,
                            email=user.email, telephone=user.telephone, role=user.role)
        except Exception as e:
            logger.error(f"Error adding user with role: {e}")
            self.connection.rollback()
            return None
        
    # update the existing user in database
    def update_user(self, user_id: int, user: User) -> Optional[User]:
        try:
            with self.connection.cursor() as cursor:
                update_query = sql.SQL("""
                    UPDATE users
                    SET name = %s, email = %s, telephone = %s, role = %s
                    WHERE user_id = %s RETURNING user_code
                """)
                cursor.execute(update_query, (user.name, user.email, user.telephone, user.role, user_id))
                result = cursor.fetchone()
                self.connection.commit()
                if result:
                    return User(user_id=user_id, user_code=result[0], name=user.name,
                                email=user.email, telephone=user.telephone, role=user.role)
                return None
        except Exception as e:
            logger.error(f"Error updating user: {e}")
            self.connection.rollback()
            return None
        
    # delete the user from database
    def delete_user(self, user_id: int) -> bool:
        try:
            with self.connection.cursor() as cursor:
                delete_query = sql.SQL("DELETE FROM users WHERE user_id = %s")
                cursor.execute(delete_query, (user_id,))
                self.connection.commit()
                return cursor.rowcount > 0
        except Exception as e:
            logger.error(f"Error deleting user: {e}")
            self.connection.rollback()
            return False
        
    # fetch the user from database by id
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        try:
            with self.connection.cursor() as cursor:
                select_query = sql.SQL("SELECT user_id, user_code, name, email, telephone, role FROM users WHERE user_id = %s")
                cursor.execute(select_query, (user_id,))
                result = cursor.fetchone()
                if result:
                    return User(user_id=result[0], user_code=result[1], name=result[2],
                                email=result[3], telephone=result[4], role=result[5])
                return None
        except Exception as e:
            logger.error(f"Error fetching user by id: {e}")
            return None

    # fetch all users from database
    def get_all_users(self) -> List[User]:
        try:
            with self.connection.cursor() as cursor:
                select_query = sql.SQL("SELECT user_id, user_code, name, email, telephone, role FROM users")
                cursor.execute(select_query)
                results = cursor.fetchall()
                return [User(user_id=row[0], user_code=row[1], name=row[2],
                             email=row[3], telephone=row[4], role=row[5]) for row in results]
        except Exception as e:
            logger.error(f"Error fetching all users: {e}")
            return []
        
    # fetch user by roles from database
    def get_users_by_role(self, role: str) -> List[User]:
        try:
            with self.connection.cursor() as cursor:
                select_query = sql.SQL("SELECT user_id, user_code, name, email, telephone, role FROM users WHERE role = %s")
                cursor.execute(select_query, (role,))
                results = cursor.fetchall()
                return [User(user_id=row[0], user_code=row[1], name=row[2],
                             email=row[3], telephone=row[4], role=row[5]) for row in results]
        except Exception as e:
            logger.error(f"Error fetching users by role: {e}")
            return []
        
    # close the database connection when the repository is destroyed
    def __del__(self):
        if self.connection:
            self.connection.close()