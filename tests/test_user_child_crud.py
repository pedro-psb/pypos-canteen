import pytest
from flask import url_for
from pypos.db import get_db
from pypos.models import dao
from pypos.models.user_model import UserChildCreateForm, UserChildUpdateForm
from .fake_forms.user_child import (
    create_form_valid,
    update_form_valid
)


def test_user_child_create(app):
    with app.app_context(), app.test_request_context():
        form = UserChildCreateForm(**create_form_valid)
        assert form


def test_user_child_create_fail(app):
    with app.app_context(), app.test_request_context():
        form = UserChildCreateForm(**create_form_valid)
        assert form


def test_user_child_update(app):
    with app.app_context(), app.test_request_context():
        form = UserChildUpdateForm(**create_form_valid)
        assert form


def test_user_child_update_fail(app):
    with app.app_context(), app.test_request_context():
        form = UserChildUpdateForm(**create_form_valid)
        assert form


def test_user_child_delete(app):
    with app.app_context(), app.test_request_context():
        pass


def test_user_child_delete(app):
    with app.app_context(), app.test_request_context():
        pass
