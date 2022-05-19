import pytest
from flask import g, session, url_for, get_flashed_messages
from pypos.db import get_db
from pypos.blueprints.canteen_space.product_mng.errors import *
from markupsafe import escape

def test_dashboard(client, app):
    with app.app_context(), app.test_request_context():
        response = client.get(url_for('canteen.product.dashboard'))
        assert response.status_code == 200


def test_add_product(client, app):
    # TODO: test validations
    form_data = {
        'name': 'name',
        'price': '10',
        'category': '1',
    }

    with app.app_context(), app.test_request_context():
        db = get_db()
        product_count_before = db.execute(
            "SELECT COUNT(*) FROM product").fetchone()[0]

        response = client.post(
            url_for('canteen.product.add_product'), data=form_data)

        product_count_after = db.execute(
            "SELECT COUNT(*) FROM product").fetchone()[0]

        assert response.status_code == 302
        assert product_count_after == product_count_before + 1


@pytest.mark.parametrize(
    ('name', 'price', 'category', 'message'), (
        ('torta', '10', '1', ADD_PRODUCT_INTEGRITY_ERROR),
        ('', '10', '1', ADD_PRODUCT_NOT_EMPTY_NAME_ERROR),
        ('valido', '', '1', ADD_PRODUCT_NOT_EMPTY_PRICE_ERROR),
        ('valido', None, '1', ADD_PRODUCT_NOT_EMPTY_PRICE_ERROR),
        ('valido', '-1', '1', ADD_PRODUCT_NOT_POSTIIVE_REAL_ERROR),
        ('valido', '10', '1.3', ADD_PRODUCT_INVALID_CATEGORY_ERROR),
        ('valido', '10', '-1', ADD_PRODUCT_INVALID_CATEGORY_ERROR),
    )
)
def test_add_product_validation(client, app, name, price, category, message):
    with app.app_context(), app.test_request_context():
        db = get_db()
        product_count_before = db.execute(
            "SELECT COUNT(*) FROM product").fetchone()[0]
        response = client.post(
            url_for('canteen.product.add_product'),
            data={'name': name, 'price': price, 'category': category})
        product_count_after = db.execute(
            "SELECT COUNT(*) FROM product").fetchone()[0]

        assert response.status_code == 302
        response = client.get(response.location)

        message = bytes(escape(message), encoding='utf-8')
        assert response.status_code == 200
        assert message in response.data
        assert product_count_after == product_count_before


def test_remove_product(client, app):
    with app.app_context(), app.test_request_context():
        db = get_db()
        rows_before = db.execute(
            'SELECT COUNT(*) FROM product WHERE active=1 AND id=1;').fetchone()[0]
        response = client.post(url_for('canteen.product.remove_product'),
                               data={'product_id': 1})
        rows_after = db.execute(
            'SELECT COUNT(*) FROM product WHERE active=1 AND id=1;').fetchone()[0]

        assert response.status_code == 302
        assert rows_after == rows_before - 1


def test_remove_product_validation(client, app):
    with app.app_context(), app.test_request_context():
        db = get_db()
        response = client.post(url_for('canteen.product.remove_product'),
                               data={'product_id': 50})
        assert response.status_code == 302
        response = client.get(response.location)
        assert response.status_code == 200

        message = bytes(
            escape(REMOVE_PRODUCT_INVALID_PRODUCT_ID), encoding='utf-8')
        assert message in response.data


def test_add_product_category(app, client):
    with app.app_context(), app.test_request_context():
        db = get_db()
        rows_before = db.execute(
            'SELECT COUNT(*) FROM product_category;').fetchone()[0]
        response = client.post(url_for('canteen.product.add_category'),
                               data={'category_name': 'Sobremesa'})
        rows_after = db.execute(
            'SELECT COUNT(*) FROM product_category;').fetchone()[0]

        assert response.status_code == 302
        assert rows_after == rows_before + 1


def test_remove_product_category(app, client):
    with app.app_context(), app.test_request_context():
        db = get_db()
        rows_before = db.execute(
            'SELECT COUNT(*) FROM product_category WHERE active=1;').fetchone()[0]
        response = client.post(url_for('canteen.product.remove_category'),
                               data={'category_id': '1'})
        rows_after = db.execute(
            'SELECT COUNT(*) FROM product_category WHERE active=1;').fetchone()[0]

        assert response.status_code == 302
        assert rows_after == rows_before - 1
