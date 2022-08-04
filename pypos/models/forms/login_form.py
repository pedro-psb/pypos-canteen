from abc import ABC

import werkzeug
from pydantic import BaseModel, validator
from pypos.models import dao
from werkzeug.security import check_password_hash


class LoginForm(BaseModel):
    username: str
    password: str

    @validator("username")
    def username_exist(cls, username):
        user = dao.get_user_by_name(username)
        if not user:
            raise ValueError(f"Username `{username}` doesn't exist")
        return username

    @validator("password")
    def password_matches(cls, password, values):
        if values.get("username"):
            user = dao.get_user_by_name(values["username"])
            password_check = user["password"]
            if not check_password_hash(password_check, password):
                raise ValueError("Password is incorrect")
        else:
            raise ValueError("")
        return password
