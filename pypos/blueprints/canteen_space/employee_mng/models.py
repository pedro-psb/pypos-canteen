import re
from typing import Optional
from pydantic import BaseModel, ConstrainedStr, ValidationError, validator
from werkzeug.security import generate_password_hash

from pypos.db import get_db


class NotEmptyString(ConstrainedStr):
    min_length = 1


class Employee(BaseModel):
    # TODO strip all whitespace exepct from password field
    id: Optional[int]
    name: NotEmptyString
    email: NotEmptyString
    password: NotEmptyString
    phone_number: str = ""
    role_name: Optional[str]
    role_id: NotEmptyString
    canteen_id: int

    @validator('email')
    def email_must_match_pattern(cls, email):
        email_pattern = r"^([\w\.\-]+)@([\w\-]+)((\.(\w){2,3})+)$"
        pattern = re.compile(email_pattern)
        email_is_valid = re.match(pattern, email)
        if not email_is_valid:
            raise ValueError("Email is not valid")
        return email

    @validator('password')
    def secure_password(cls, password):
        password = generate_password_hash(password)
        return password

    @validator('role_id')
    def validate_id_exist(cls, id, values):
        db = get_db()
        role_name = db.execute(
            "SELECT name FROM role WHERE id=?;", (id,)).fetchone()[0]
        if not role_name:
            raise ValidationError("The role doesn't exist")
        
        # Update role_name with accurate value
        if not values['role_name']:
            values['role_name'] = role_name
        return id

    class Config:
        anystr_strip_whitespace = True
        max_anystr_length = 100


class EmployeeUpdate(Employee):
    '''Used only to update'''
    # TODO  refactor this so there is a Config in the Employee class
    #       which makes all parameters optional.
    id: Optional[int]
    name: Optional[NotEmptyString]
    email: Optional[NotEmptyString]
    password: Optional[NotEmptyString]
    phone_number: Optional[str] = ""
    role_name: Optional[str]
    role_id: Optional[NotEmptyString]
    canteen_id: Optional[int]
