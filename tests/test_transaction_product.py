import json
from urllib import response
import pytest
from flask import g, got_request_exception, session, url_for, get_flashed_messages
from pypos.db import get_db, close_db
from pypos.blueprints.canteen_space.point_of_sale.errors import *
from markupsafe import escape


def test_valid_transaction(app, client):
    with app.app_context(), app.test_request_context():
        db = get_db()
        form_data = {
            'products': json.dumps([
                {'id': '1', 'quantity': '1'},
                {'id': '2', 'quantity': '3'},
            ]),
            'discount': '0',
            'payment_method': '1'
        }
        transactions_before = db.execute(
            'SELECT count(*) FROM transaction_product;').fetchone()[0]
        transactions_items_before = db.execute(
            'SELECT count(*) FROM transaction_product_item;').fetchone()[0]

        # Posting JSON!
        # response = client.post(
        #     url_for('canteen.point_of_sale.add_transaction_product'),
        #     json=form_data)
        response = client.post(
            url_for('canteen.point_of_sale.add_transaction_product'),
            data=form_data)

        close_db()
        db = get_db()
        transactions_after = db.execute(
            'SELECT count(*) FROM transaction_product;').fetchone()[0]
        transactions_items_after = db.execute(
            'SELECT count(*) FROM transaction_product_item;').fetchone()[0]

        assert response.status_code == 302
        assert transactions_after == transactions_before + 1
        assert transactions_items_after == transactions_items_before + 2


def test_remove_transaction_product(app, client):
    with app.app_context(), app.test_request_context():
        db = get_db()
        add_form_data = {
            'products': json.dumps([
                {'id': '1', 'quantity': '1'},
                {'id': '2', 'quantity': '3'},
            ]),
            'discount': '0',
            'payment_method': '1'
        }
        remove_form_data = {'transaction_id': '1'}

        # add product
        client.post(
            url_for('canteen.point_of_sale.add_transaction_product'),
            data=add_form_data)

        transactions_before = db.execute(
            'SELECT count(*) FROM transaction_product '
            'WHERE active=1;').fetchone()[0]

        # remove product
        response = client.post(
            url_for('canteen.point_of_sale.remove_transaction_product'),
            data=remove_form_data)

        # restart db to check persistence
        close_db()
        db = get_db()

        transactions_after = db.execute(
            'SELECT count(*) FROM transaction_product '
            'WHERE active=1;').fetchone()[0]

        assert response.status_code == 302
        assert transactions_after == transactions_before - 1


# @ pytest.mark.parametrize(
#     ('products', 'error_msg'), (
#         ([{'product_id': '4', 'quantity': '2'}], POS_INVALID_PRODUCT_ID_ERROR),
#         ([{'product_id': '5.4', 'quantity': '2'}], POS_INVALID_PRODUCT_ID_ERROR),
#         ([{'product_id': '1', 'quantity': '2.3'}],
#          POS_INVALID_PRODUCT_QUANTITY_VALUE_ERROR),
#         ([{'product_id': 'asd', 'quantity': '2'}], POS_INVALID_PRODUCT_ID_ERROR),
#         ([{'product_id': '1', 'quantity': 'asd'}],
#          POS_INVALID_PRODUCT_QUANTITY_VALUE_ERROR),
#         ([{'product_id': '1', 'quantity': '1'},
#          {'product_id': '4', 'quantity': '2'}], POS_INVALID_PRODUCT_ID_ERROR),
#         ([{'invalid_key': '1', 'quantity': 'asd'}],
#          POS_INVALID_TRANSACTION_REQUEST_ERROR),)
# )
# def test_invalid_transactions(app, client, products, error_msg):
#     with app.app_context(), app.test_request_context():
#         db = get_db()
#         transactions_before = db.execute(
#             'SELECT count(*) FROM transaction_product;').fetchone()[0]
#         response = client.post(
#             url_for('canteen.point_of_sale.add_transaction_product'),
#             json=products)
#         transactions_after = db.execute(
#             'SELECT count(*) FROM transaction_product;').fetchone()[0]
#         assert response.status_code == 302
#         response = client.get(response.location)

#         assert transactions_after == transactions_before
#         error_msg = bytes(escape(error_msg), encoding='utf-8')
#         assert error_msg in response.data
