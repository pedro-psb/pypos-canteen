import pytest
from pydantic import ValidationError
from pypos.models.forms.client_forms import LoginForm
from pypos.utils.data_util import parse_errors


@pytest.mark.parametrize(
    "username,password,username_flag,password_flag",
    [
        ("invalid", "not_aplicable", True, True),
        ("test", "invalid", False, True),
        ("test", "test", False, False),
        # ("", "", True, True), #TODO add field required validation error
    ],
)
def test_parse_succeed_all_invalid_fields(
    app, username, password, username_flag, password_flag
):
    """parse_errors should return errors in the format `field.errors`"""
    with app.app_context():
        try:
            LoginForm(username=username, password=password)
        except ValidationError as e:
            errors = parse_errors(errors=e.errors(), model=LoginForm)
            assert bool(errors["username"]) == username_flag
            assert bool(errors["password"]) == password_flag
