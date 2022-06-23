import re
from typing import Optional
from xml.dom import ValidationErr
from pydantic import BaseModel, ConstrainedStr, ValidationError, validator
from werkzeug.security import generate_password_hash

from pypos.db import get_db


class NotEmptyString(ConstrainedStr):
    min_length = 1


class Employee(BaseModel):
    id: Optional[int]
    name: NotEmptyString
    email: NotEmptyString
    password: NotEmptyString
    phone_number: str = ""
    role_name: Optional[str]
    role_id: NotEmptyString
    canteen_id: int

    @validator('name')
    def name_trailling_space(cls, name):
        name = name.strip()
        return name.strip()

    @validator('email')
    def email_must_match_pattern(cls, email):
        email_pattern = r"^([\w\.\-]+)@([\w\-]+)((\.(\w){2,3})+)$"
        pattern = re.compile(email_pattern)
        email_is_valid = re.match(pattern, email.strip())
        if not email_is_valid:
            raise ValueError("Email is not valid")
        return email.strip()

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
        if not values['role_name']:
            values['role_name'] = role_name
        return id
