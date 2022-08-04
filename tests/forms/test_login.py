from pydantic import ValidationError
from pypos.models.forms.client_forms import LoginForm


def test_valid_username_valid_password(app):
    with app.app_context():
        login = LoginForm(username="test", password="test")
        assert login


# TODO parametrize these invalid test with the aid of the error classes
def test_invalid_username(app):
    with app.app_context():
        try:
            login = LoginForm(username="invalid_username", password="test")
            assert not login
        except ValidationError as e:
            # TODO add an error msg enum class for each form
            errors = e.errors()
            assert errors


def test_invalid_password(app):
    with app.app_context():
        try:
            login = LoginForm(username="test", password="invalid_password")
            assert not login
        except ValidationError as e:
            # TODO add an error msg enum class for each form
            errors = e.errors()
            assert errors


def test_empty_username(app):
    with app.app_context():
        try:
            login = LoginForm(username="", password="test")
            assert not login
        except ValidationError as e:
            # TODO add an error msg enum class for each form
            errors = e.errors()
            assert errors


def test_empty_password(app):
    with app.app_context():
        try:
            login = LoginForm(username="insert", password="")
            assert not login
        except ValidationError as e:
            # TODO add an error msg enum class for each form
            errors = e.errors()
            assert errors
