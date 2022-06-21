import pytest
from flask import g, session, url_for, get_flashed_messages
from pypos.db import get_db


def test_products_are_isolated_by_canteen(client, app):
    with app.app_context(), app.test_request_context():
        form_data = {
            'name': 'name',
            'price': '10',
            'category': '1',
        }
        db = get_db()
        response = client.post(
            url_for('canteen.product.add_product'), data=form_data)


def test_categories_are_isolated_by_canteen():
    pass
