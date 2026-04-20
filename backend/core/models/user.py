'''
this is the model for the user, it contains all the user related information from PostgreSQL database

this entity contains these attributes:
 users (
    user_id SERIAL PRIMARY KEY,
    user_code TEXT GENERATED ALWAYS AS ('user-' || id) STORED name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    telephone VARCHAR(20),
    role VARCHAR(50) NOT NULL -- e.g. 'admin', 'driver', 'passenger'
'''

from . import db
import re

class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    user_code = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    telephone = db.Column(db.String(20))
    role = db.Column(db.String(50), nullable=False)

    def __init__(self, email, telephone=None, role=None, name=None, user_id=None, user_code=None):
        self.user_id = user_id
        self.user_code = user_code
        self.name = name
        self.email = email
        self.telephone = telephone
        self.role = role
    def __repr__(self):
        return f'<User {self.user_code}>'
    
    # This method is used to serialize the user object to a dictionary, which can be easily converted to JSON
    def to_dict(self):
        return {
            'user_id': self.user_id,
            'user_code': self.user_code,
            'name': self.name,
            'email': self.email,
            'telephone': self.telephone,
            'role': self.role
        }
    
    def from_dict(self, data):
        for field in ['name', 'email', 'telephone', 'role']:
            if field in data:
                setattr(self, field, data[field])
            else:
                raise ValueError(f'Missing field: {field}')
    @staticmethod
    # validation of attributes of the user, such as email format and telephone number format
    def validate_email(email):
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_regex, email):
            raise ValueError('Invalid email format')
        else: 
            return True
    @staticmethod
    def validate_telephone(telephone):
        telephone_regex = r'^\+?[\d\s\-]+$'
        if not re.match(telephone_regex, telephone):
            raise ValueError('Invalid telephone format')
        else:
            return True
    @staticmethod
    def validate_role(role):
        valid_roles = ['admin', 'driver', 'passenger', 'sales', 'coordinator']
        if role not in valid_roles:
            raise ValueError(f'Invalid role. Valid roles are: {", ".join(valid_roles)}')
        else:
            return True
        

    # This method is used to validate the user data before creating or updating a user
    @staticmethod
    def validate_user_data(data):
        if 'email' not in data:
            raise ValueError('Missing email field')
        if 'role' not in data:
            raise ValueError('Missing role field')
        
        User.validate_email(data['email'])
        if 'telephone' in data:
            User.validate_telephone(data['telephone'])
        User.validate_role(data['role'])