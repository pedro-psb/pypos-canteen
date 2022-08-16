from pypos.models.user_model import UserChildCreateForm, UserChildUpdateForm

from ._fake_forms.form_user_child import create_form_valid, update_form_valid


def test_model_user_child_create_valid(app):
    with app.app_context():
        form = UserChildCreateForm(**create_form_valid)
        assert form


def test_model_user_child_update_valid(app):
    with app.app_context():
        form = UserChildUpdateForm(**update_form_valid)
        assert form
