import pytest
from flask import g, session, url_for, get_flashed_messages
from pypos.db import get_db
from pypos.blueprints.frontend.errors import *
from markupsafe import escape

@pytest.mark.parametrize(
    ('page'), (
    ('page.index'),
    ('page.register'),
    ('page.login')
))
def test_pages_dont_require_auth(client, app, page):
    with app.test_request_context():
        response = client.get(url_for(page))
        assert response.status_code == 200

@pytest.mark.parametrize(
    ('page'), (
    ('page.product_management'),
    ('page.pos_interface'),
    ('page.client_dashboard'),
))
def test_pages_require_auth_with_no_login(client, auth, app, page):
    with app.test_request_context():
        response = client.get(url_for(page))
        assert response.status_code != 200


@pytest.mark.parametrize(
    ('page', 'username'), (
    ('page.product_management', 'fake_manager'),
    ('page.pos_interface', 'fake_cashier'),
    ('page.client_dashboard', 'fake_client'),
))
def test_pages_require_auth_witht_right_login(client, auth, app, page, username):
    with app.test_request_context():
        login_response = auth.login(username=username)
        response = client.get(url_for(page))
        assert response.status_code == 200

@pytest.mark.parametrize(
    ('page', 'username'), (
    ('page.product_management', 'fake_client'),
    ('page.pos_interface', 'fake_manager'),
    ('page.client_dashboard', 'fake_cashier'),
))
def test_pages_require_auth_witht_wrong_login(client, auth, app, page, username):
    with app.test_request_context():
        login_response = auth.login(username=username)
        response = client.get(url_for(page))
        assert response.status_code != 200