from pydantic import ValidationError
import pytest
from pypos.models.user_model import UserClient

form_data = {
    'id': '3',
    'role_id': '1',
    'canteen_id': '1',
    'username': 'Lilian',
    'email': 'lilian@gmail.com',
    'password': '123',
    'password_confirm': '123',
    'phone_number': '(31) 9289-3984'
}

form_data_mismatch_password = form_data.copy()
form_data_mismatch_password['password_confirm'] = 'abc'
form_data_invalid_canteen_id = form_data.copy()
form_data_invalid_canteen_id['canteen_id'] = '10'
form_data_username_taken = form_data.copy()
form_data_username_taken['username'] = 'test'

# Passwords match?


def test_password_validator(app):
    with app.app_context():
        user = UserClient(**form_data)
        assert user


def test_password_validator_fail(app):
    with app.app_context():
        with pytest.raises(ValidationError):
            UserClient(**form_data_mismatch_password)

# Canteen ID is valid?


def test_canteen_exist_validator(app):
    with app.app_context():
        user = UserClient(**form_data)
        assert user


def test_canteen_exist_validator_fail(app):
    with app.app_context():
        with pytest.raises(ValidationError):
            UserClient(**form_data_invalid_canteen_id)

# Username is avaliable?


def test_username_avaliable_validator(app):
    with app.app_context():
        user = UserClient(**form_data)
        assert user


def test_username_avaliable_validator_fail(app):
    with app.app_context():
        with pytest.raises(ValidationError):
            UserClient(**form_data_invalid_canteen_id)
