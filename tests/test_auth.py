import pytest
from flask import g, session
from pypos.db import get_db


def test_register(client, app):
    response = client.post(
        '/auth/register', data={
            'username': 'a', 'password': 'a', 'role_name': 'owner'}
    )

    with app.app_context():
        user_registered = get_db().execute(
            "SELECT * FROM user WHERE username = 'a'",).fetchone()
        assert user_registered is not None
    
    assert response.headers["Location"] == "/auth/login"


# @pytest.mark.parametrize(('username', 'password', 'message'), (
#     ('', '', b'Username is required.'),
#     ('a', '', b'Password is required.'),
#     ('test', 'test', b'already registered'),
# ))
# def test_register_validate_input(client, username, password, message):
#     response = client.post(
#         '/auth/register',
#         data={'username': username, 'password': password}
#     )
#     assert message in response.data


def test_login(client, auth):
    response = auth.login()

    with client:
        client.get('/')
        # breakpoint()
        assert session.get('user_id') == 1
        assert g.user['username'] == 'test'
        assert g.user['role_name'] == 'owner'


# @pytest.mark.parametrize(('username', 'password', 'message'), (
#     ('a', 'test', b'Incorrect username.'),
#     ('test', 'a', b'Incorrect password.'),
# ))
# def test_login_validate_input(auth, username, password, message):
#     response = auth.login(username, password)
#     assert message in response.data


def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert 'user_id' not in session
