import json
import pytest
from flask import g, session, url_for
from pypos.db import get_db


def test_add_employee(app, client, auth):
    form_data = {
        'name': 'Lilian',
        'email': 'lilian@gmail.com',
        'password': '123',
        'phone_number': '(31) 9289-3984',
        'role_name': 'Manager'
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
