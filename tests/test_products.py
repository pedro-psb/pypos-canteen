import pytest
from flask import g, session, url_for
from pypos.db import get_db
from pypos.errors import *

def test_add_product(client, app):
    # TODO: test validations
    form_data = {
        'name': 'name',
        'price': 10,
        'category': 1,
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
        ('torta', 10, 1, ADD_PRODUCT_INTEGRITY_ERROR),
    )
)
def test_add_product_validation(client, app, name, price, category, message):
    with app.app_context():
        db = get_db()
        product_count_before = db.execute(
            "SELECT COUNT(*) FROM product").fetchone()[0]
        response = client.post(
            '/product/add_product',data={'name': name, 'price': price, 'category': category})
        product_count_after = db.execute(
            "SELECT COUNT(*) FROM product").fetchone()[0]
        
        assert response.status_code == 302
        # TODO: Fix the assert the message is in the page
        #   * Currently, the response is a redirect page
        #   * I can't programatically acess the redirect destination to check it's content
        # assert message in response.text
        assert product_count_after == product_count_before





