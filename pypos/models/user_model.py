import re
from typing import Optional
from pydantic import BaseModel, ConstrainedStr, root_validator, validator
from werkzeug.security import generate_password_hash

from pypos.db import get_db


class NotEmptyString(ConstrainedStr):
    min_length = 1


class User(BaseModel):
    # TODO strip all whitespace exepct from password field
    id: Optional[int]
    email: NotEmptyString
    password: NotEmptyString
    phone_number: str = ""
    role_name: Optional[str]
    role_id: Optional[NotEmptyString]
    canteen_name: Optional[str]
    canteen_id: int
    username: NotEmptyString

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
            raise ValueError("The role doesn't exist")

        # Update role_name with accurate value
        if not values['role_name']:
            values['role_name'] = role_name
        return id

    @validator('canteen_id')
    def canteen_id_exist(cls, canteen_id, values):
        query = "SELECT name FROM canteen WHERE id=?;"
        db = get_db()
        canteen_name = db.execute(query, (str(canteen_id),)).fetchone()
        if not canteen_name:
            raise ValueError("Canteen ID is invalid.")
        if not values.get('canteen_name'):
            values['canteen_name'] = canteen_name[0]
        return canteen_id

    @validator('username')
    def username_doesnt_exist(cls, username, values):
        db = get_db()
        query = "SELECT * FROM user WHERE username=?;"
        user_exist = db.execute(query, (username,)).fetchone()
        if user_exist:
            raise ValueError('username already taken')
        return username

    @validator('email')
    def email_isnt_taken(cls, email):
        db = get_db()
        query = "SELECT * FROM user WHERE email=?;"
        email_exist = db.execute(query, (email,)).fetchone()
        if email_exist:
            raise ValueError('email is already taken')
        return email

    class Config:
        anystr_strip_whitespace = True


class UserUpdate(User):
    '''Used only to update'''
    # TODO  refactor this so there is a Config in the User class
    #       which makes all parameters optional.
    id: Optional[int]
    username: Optional[NotEmptyString]
    email: Optional[str]
    password: Optional[NotEmptyString]
    phone_number: Optional[str] = ""
    role_name: Optional[str]
    role_id: Optional[NotEmptyString]
    canteen_id: Optional[int]
    
    @validator('username')
    def username_doesnt_exist(cls, username, values):
        """TODO needs some special validation:
        - if username is already taken (expeting the original username), shouln't pass"""
        # db = get_db()
        # query = "SELECT * FROM user WHERE username=?;"
        # user_exist = db.execute(query, (username,)).fetchone()
        # if not user_exist:
        #     raise ValueError("username doesn't exist")
        return username

    @validator('email')
    def email_must_match_pattern(cls, email):
        return email
    
    @validator('email')
    def email_isnt_taken(cls, email):
        """TODO needs some validation:
        - if email is the same as from same user, should pass
        - if email is the same as from different user, shouldn't pass"""
        return email

class UserClient(User):
    password_confirm: NotEmptyString

    @root_validator(pre=True)
    def password_matches(cls, values):
        if not values['password_confirm'] == values['password']:
            raise ValueError("Passwords doesn't match")
        return values


class UserOwner(User):
    canteen_name: NotEmptyString
    canteen_id: Optional[int]

    @validator('canteen_name')
    def canteen_name_doesnt_exist(cls, canteen_name, values):
        query = "SELECT * FROM canteen WHERE name LIKE ?;"
        db = get_db()
        canteen_exist = db.execute(query, (canteen_name,)).fetchone()
        if canteen_exist:
            raise ValueError("Canteen name already taken.")
        return canteen_name

    @validator('canteen_id')
    def canteen_id_exist(cls, canteen_id):
        print("shouldn't provide canteen_id")
        return canteen_id


class UserChildCreateForm(User):
    role_name = 'client_dependent'
    email: Optional[str]
    age: Optional[int]
    grade: Optional[str]
    user_provider_id: int


class UserChildUpdateForm(UserUpdate):
    age: Optional[int]
    grade: Optional[str]
    


# TODO implement this later


class Canteen(BaseModel):
    name: str
    id: Optional[int]
    description: Optional[str]
