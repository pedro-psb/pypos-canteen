import pytest
from flask import g, session, url_for
from pypos.db import get_db
from pypos.blueprints.frontend.errors import *
from markupsafe import escape

@pytest.mark.parametrize(
    ('page'), (
    ('page.index'),
    ('page.register_client'),
    ('page.choose_role'),
    ('page.login')
))
def test_pages_dont_require_auth(client, app, page):
    with app.test_request_context():
        response = client.get(url_for(page))
        assert response.status_code == 200

@pytest.mark.parametrize(
    ('page'), (
    ('page.manage_products'),
    ('page.pos_main'),
    ('page.client_index'),
))
def test_pages_require_auth_with_no_login(client, auth, app, page):
    with app.test_request_context():
        response = client.get(url_for(page))
        assert response.status_code != 200


@pytest.mark.parametrize(
    ('page', 'username'), (
    ('page.manage_products', 'fake_owner'),
    ('page.manage_products', 'fake_manager'),
    ('page.pos_main', 'fake_cashier'),
    ('page.client_index', 'fake_client'),
))
def test_pages_require_auth_with_right_login(client, auth, app, page, username):
    with app.test_request_context():
        login_response = auth.login(username=username)
        response = client.get(url_for(page))
        assert response.status_code == 200

@pytest.mark.parametrize(
    ('page', 'username'), (
    ('page.manage_products', 'fake_cashier'),
    ('page.pos_main', 'fake_client'),
    ('page.client_index', 'fake_cashier'),
))
def test_pages_require_auth_witht_wrong_login(client, auth, app, page, username):
    with app.test_request_context():
        login_response = auth.login(username=username)
        response = client.get(url_for(page))
        assert response.status_code != 200