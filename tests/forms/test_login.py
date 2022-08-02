from pydantic import BaseModel, ValidationError, validator
from pypos.models import dao
from werkzeug.security import check_password_hash, generate_password_hash


class LoginForm(BaseModel):
    username: str
    password: str

    @validator("username")
    def username_exist(cls, username):
        user = dao.get_user_by_name(username)
        if not user:
            raise ValueError("Username doesn't exist")
        return username

    @validator("password")
    def password_matches(cls, password, values):
        if values.get("username"):
            user = dao.get_user_by_name(values["username"])
            password_check = user["password"]
            password = generate_password_hash(password)
            if not check_password_hash(password, password_check):
                raise ValueError("Password is incorrect")
        return password


def test_valid_username_valid_password(app):
    with app.app_context():
        login = LoginForm(username="test", password="test")
        assert login
