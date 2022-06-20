import pytest
from flask import g, session
from pypos.db import get_db, close_db


def test_register(client, app):
    with app.app_context():
        form_data = {
            'username': 'a',
            'email': 'foo@gmail.com',
            'password': 'a',
            'password_confirm': 'a',
            'canteen_id': '1'
        }
        response = client.post(
            '/auth/register', data=form_data
        )

        db = get_db()
        query = "SELECT * FROM user WHERE username=?"
        user_registered = db.execute(query, ('a')).fetchone()

        assert user_registered is not None


@pytest.mark.parametrize(('username', 'email', 'password', 'password_confirm', 'canteen_id', 'message'), (
    ('', 'foo@gmail.com', 'pass', 'pass', '1', 'Username is required.'),
    ('user', '', 'pass', 'pass', '1', 'Email is required.'),
    ('user', 'foo@gmail.com', '', 'pass', '1', 'Password is required.'),
    ('user', 'foo@gmail.com', '', 'pass', '', 'Canteen ID is required.'),
    ('user', 'foo-gmail.com', 'pass', 'pass', '1', 'Email is invalid'),
    ('user', 'foo@gmail.com', 'pass', 'pass2', '1', "Password doesn't match"),
    ('fake_client', 'foo@gmail.com', 'pass', 'pass', '1', 'User already exist'),
    ('user', 'foo@gmail.com', 'pass', 'pass', '100', 'Canteen ID is Invalid')
))
def test_register_fail(app, client, username, email, password, password_confirm, canteen_id, message):
    with app.app_context():
        form_data = {
            'username': username,
            'email': email,
            'password': password,
            'password_confirm': password_confirm,
            'canteen_id': canteen_id
        }
        db = get_db()
        query = "SELECT count(*) FROM user;"
        user_registered_before = db.execute(query).fetchone()[0]
        
        response = client.post('/auth/register', data=form_data)
        close_db()
        db = get_db()
        user_registered_after = db.execute(query).fetchone()[0]

        assert user_registered_before == user_registered_after
        # assert message in response.data


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
