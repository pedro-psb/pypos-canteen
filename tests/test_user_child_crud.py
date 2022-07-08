import pytest
from flask import url_for
from pypos.db import get_db
from pypos.models import dao
from pypos.models.user_model import UserChildCreateForm, UserChildUpdateForm
from .fake_forms.form_user_child import (
    create_form_valid,
    update_form_valid
)


def test_user_child_create(app):
    with app.app_context(), app.test_request_context():
        db = get_db()
        users_before = dao.get_user_child_count(1)

        form = UserChildCreateForm(**create_form_valid)
        dao.create_user_child(form)

        users_after = dao.get_user_child_count(1)
        assert form
        assert users_after == users_before + 1


# def test_user_child_create_fail(app):
#     with app.app_context(), app.test_request_context():
#         form = UserChildCreateForm(**create_form_valid)
#         assert form


def test_user_child_update(app):
    with app.app_context(), app.test_request_context():
        # create user before update
        form = UserChildCreateForm(**create_form_valid)
        user_id = dao.create_user_child(form)
        user_before = dao.get_user_by_id(user_id)

        # update user (only age)
        form_data = user_before
        form_data.update(update_form_valid)
        form = UserChildUpdateForm(**form_data)
        dao.update_user_child(form)

        user_after = dao.get_user_by_id(user_id)
        assert form
        assert user_before['username'] == user_after['username']
        assert user_before['age'] != user_after['age']


# def test_user_child_update_fail(app):
#     with app.app_context(), app.test_request_context():
#         form = UserChildUpdateForm(**create_form_valid)
#         assert form


def test_user_child_delete(app):
    with app.app_context(), app.test_request_context():
        # create user before update
        form = UserChildCreateForm(**create_form_valid)
        user_id = dao.create_user_child(form)
        user_active_before = dao.get_user_by_id(user_id)['active']
        
        dao.delete_user(user_id)
        user_active = dao.get_user_by_id(user_id)['active']
        assert user_active_before == 1
        assert user_active == 0
        


# def test_user_child_delete_fail(app):
#     with app.app_context(), app.test_request_context():
#         pass
