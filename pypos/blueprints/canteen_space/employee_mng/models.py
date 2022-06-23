import re
from pydantic import BaseModel, ConstrainedStr, validator
from werkzeug.security import generate_password_hash


class NotEmptyString(ConstrainedStr):
    min_length = 1


class Employee(BaseModel):
    name: NotEmptyString
    email: NotEmptyString
    password: NotEmptyString
    phone_number: str = ""
    role_name: NotEmptyString
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
