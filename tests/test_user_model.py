from pydantic import ValidationError
import pytest
from pypos.models.user_model import UserClient, UserOwner

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


# Passwords match?
form_data_mismatch_password = form_data.copy()
form_data_mismatch_password['password_confirm'] = 'abc'


def test_password_validator(app):
    with app.app_context():
        user = UserClient(**form_data)
        assert user


def test_password_validator_fail(app):
    with app.app_context():
        with pytest.raises(ValidationError):
            UserClient(**form_data_mismatch_password)


# Canteen ID is valid?
form_data_invalid_canteen_id = form_data.copy()
form_data_invalid_canteen_id['canteen_id'] = '10'


def test_canteen_exist_validator(app):
    with app.app_context():
        user = UserClient(**form_data)
        assert user


def test_canteen_exist_validator_fail(app):
    with app.app_context():
        with pytest.raises(ValidationError):
            UserClient(**form_data_invalid_canteen_id)


# Username is avaliable?
form_data_username_taken = form_data.copy()
form_data_username_taken['username'] = 'test'


def test_username_avaliable_validator(app):
    with app.app_context():
        user = UserClient(**form_data)
        assert user


def test_username_avaliable_validator_fail(app):
    with app.app_context():
        with pytest.raises(ValidationError):
            UserClient(**form_data_invalid_canteen_id)


# UserOwner: canteen is avaliable?
form_data_canteen_not_taken = form_data.copy()
form_data_canteen_not_taken['canteen_name'] = 'New Canteen'
form_data_canteen_taken = form_data.copy()
form_data_canteen_taken['canteen_name'] = 'Default canteen'


def test_canteen_avaliable_validator(app):
    with app.app_context():
        user = UserOwner(**form_data_canteen_not_taken)
        assert user


def test_canteen_avaliable_validator_fail(app):
    with app.app_context():
        with pytest.raises(ValidationError):
            UserOwner(**form_data_canteen_taken)
