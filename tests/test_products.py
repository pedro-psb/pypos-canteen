import pytest
from flask import g, session, url_for, get_flashed_messages
from pypos.db import get_db
from pypos.errors import *
from markupsafe import escape


def test_add_product(client, app):
    # TODO: test validations
    form_data = {
        'name': 'name',
        'price': '10',
        'category': '1',
    }

    with app.app_context():
        db = get_db()
        product_count_before = db.execute(
            "SELECT COUNT(*) FROM product").fetchone()[0]

        response = client.post('/product/add_product', data=form_data)

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
    message = bytes(message, encoding='utf-8')
    with app.app_context():
        db = get_db()
        product_count_before = db.execute(
            "SELECT COUNT(*) FROM product").fetchone()[0]
        response = client.post(
            '/product/add_product', data={'name': name, 'price': price, 'category': category})
        product_count_after = db.execute(
            "SELECT COUNT(*) FROM product").fetchone()[0]

        assert response.status_code == 302
        response = client.get(response.location)

        message = bytes(escape(message), encoding='utf-8')
        assert response.status_code == 200
        # assert message in response.data
        assert product_count_after == product_count_before


def test_remove_product(client, app):
    with app.app_context():
        db = get_db()
        is_active_before = db.execute(
            'SELECT active FROM product WHERE id=1').fetchone()[0]
        response = client.post('/product/remove_product',
                               data={'product_id': 1})
        is_active_after = db.execute(
            'SELECT active FROM product WHERE id=1').fetchone()[0]

        assert response.status_code == 302
        assert is_active_before
        assert not is_active_after


def test_add_product_category(app, client):
    with app.app_context():
        db = get_db()
        rows_before = db.execute(
            'SELECT COUNT(*) FROM product_category;').fetchone()[0]
        response = client.post('/product/add_category',
                               data={'category_name': 'Sobremesa'})
        rows_after = db.execute(
            'SELECT COUNT(*) FROM product_category;').fetchone()[0]

        assert response.status_code == 302
        assert rows_after == rows_before + 1


def test_remove_product_category(app, client):
    with app.app_context():
        db = get_db()
        rows_before = db.execute(
            'SELECT COUNT(*) FROM product_category;').fetchone()[0]
        response = client.post('/product/remove_category',
                               data={'category_id': '1'})
        rows_after = db.execute(
            'SELECT COUNT(*) FROM product_category;').fetchone()[0]

        assert response.status_code == 302
        assert rows_after == rows_before - 1

