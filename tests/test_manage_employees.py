import pytest
from flask import url_for
from pypos.db import get_db


def test_add_employee(app, client, auth):
    form_data = {
        'name': 'Lilian',
        'email': 'lilian@gmail.com',
        'password': '123',
        'phone_number': '(31) 9289-3984',
        'role_id': '2'  # manager
    }
    with app.app_context(), app.test_request_context():
        endpoint = url_for('canteen.manage_employee.add')
        db = get_db()
        auth.login()
        query = "SELECT COUNT(*) FROM user;"
        user_count_before = db.execute(query).fetchone()[0]
        response = client.post(endpoint, data=form_data)
        user_count_after = db.execute(query).fetchone()[0]

        print(response.location)
        assert user_count_after == user_count_before + 1,\
            'The user was not added'


@pytest.mark.parametrize(('error', 'form_data'), (
    ('Empty name', {
        'name': '',
        'email': 'lilian@gmail.com',
        'password': '123',
        'phone_number': '(31) 9289-3984',
        'role_id': '2'  # manager
    }),
    ('Empty email', {
        'name': 'Lilian',
        'email': '',
        'password': '123',
        'phone_number': '(31) 9289-3984',
        'role_id': '2'  # manager
    }),
    ('Empty password', {
        'name': 'Lilian',
        'email': 'lilian@gmail.com',
        'password': '',
        'phone_number': '(31) 9289-3984',
        'role_id': '2'  # manager
    }),
    ('Empty role_id', {
        'name': 'Lilian',
        'email': 'lilian@gmail.com',
        'password': '123',
        'phone_number': '(31) 9289-3984',
        'role_id': ''  # manager
    }),
    ('Invalid email format', {
        'name': 'Lilian',
        'email': 'lilian-gmail.com',
        'password': '123',
        'phone_number': '(31) 9289-3984',
        'role_id': '2'  # manager
    }),
    ('Invalid role_name', {
        'name': 'Lilian',
        'email': 'lilian-gmail.com',
        'password': '123',
        'phone_number': '(31) 9289-3984',
        'role_id': '10'  # doesn't exist
    }),
))
def test_add_employee_exceptions(app, client, auth, error, form_data):
    with app.app_context(), app.test_request_context():
        endpoint = url_for('canteen.manage_employee.add')
        db = get_db()
        auth.login()
        query = "SELECT COUNT(*) FROM user;"
        user_count_before = db.execute(query).fetchone()[0]
        client.post(endpoint, data=form_data)
        user_count_after = db.execute(query).fetchone()[0]

        assert user_count_after == user_count_before,\
            "The new user shouldn't be added"


def test_update_employee(app, client, auth):
    form_data = {
        'id': '3',
        'role_id': '3',  # cashier
        'name': 'Lilian',
        'email': 'lilian@gmail.com',
        'password': '123',
        'phone_number': '(31) 9289-3984'
    }
    with app.app_context(), app.test_request_context():
        endpoint = url_for('canteen.manage_employee.update')
        auth.login()
        db = get_db()
        query = 'SELECT role_name FROM user WHERE id=?;'

        role_before = db.execute(query, (form_data['id'])).fetchone()[0]
        client.post(endpoint, data=form_data)
        role_after = db.execute(query, (form_data['id'])).fetchone()[0]

        assert role_before != role_after, "Role of user hasn't been modified"


@pytest.mark.parametrize(('error', 'new_role'), (
    ('Empty role_name', ''),
    ('Invalid role_name', 'Foo'),
))
def test_update_employee_exceptions(app, auth, client, error, new_role):
    form_data = {
        'id': '3',
        'role_name': new_role,
        'name': 'Lilian',
        'email': 'lilian@gmail.com',
        'password': '123',
        'phone_number': '(31) 9289-3984'
    }
    with app.app_context(), app.test_request_context():
        endpoint = url_for('canteen.manage_employee.update')
        auth.login()
        db = get_db()
        query = 'SELECT role_name FROM user WHERE id=?;'

        role_before = db.execute(query, (form_data['id'])).fetchone()[0]
        client.post(endpoint, data=form_data)
        role_after = db.execute(query, (form_data['id'])).fetchone()[0]

        assert role_before == role_after, "Role of user shouldn't been modified"


def test_delete_employee(app, auth, client):
    form_data = {'id': '1'}
    with app.app_context(), app.test_request_context():
        endpoint = url_for('canteen.manage_employee.delete')
        auth.login()
        db = get_db()
        query = 'SELECT active FROM user WHERE id=?;'

        active_state_before = db.execute(query, (form_data['id'],)).fetchone()[0]
        client.post(endpoint, data=form_data)
        active_state_after = db.execute(query, (form_data['id'],)).fetchone()[0]

        assert active_state_before == 1, "Initially, user should be active"
        assert active_state_after == 0, "Later, user should be inactive"


@pytest.mark.parametrize(('error', 'form_data'), (
    ('Empty user_id', {
        'id': ''
    }),
    ('Invalid user_id', {
        'id': '99'
    })
))
def test_delete_employee_exceptions(app, client, auth, error, form_data):
    with app.app_context(), app.test_request_context():
        endpoint = url_for('canteen.manage_employee.delete')
        auth.login()
        db = get_db()
        query = 'SELECT COUNT(*) FROM user WHERE active=1;'

        active_count_before = db.execute(query).fetchone()[0]
        client.post(endpoint, data=form_data)
        active_count_after = db.execute(query).fetchone()[0]

        assert active_count_before == active_count_after,\
            "Active count should be the same. User shouln't be added"
