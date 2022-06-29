from pprint import pprint
from flask import g, session
import pytest

from pypos.db import get_db
from pypos.models import dao
from pypos.models.transactions_dao import (
    Product,
    RegularPurchase
)

#   ("torta", 15.5, 1),
#   ("Pão de Queijo", 10, 1),
#   ("Prato Feito", 10, 2)


def valid_transaction(payment_method='cash'):
    transaction = RegularPurchase(
        canteen_id=1,
        products=[
            Product(id=1, quantity=2, canteen_id=1),
            Product(id=2, quantity=3, canteen_id=1)
        ],
        payment_method=payment_method
    )
    return transaction


def test_product_model(app):
    with app.app_context():
        product = Product(
            id=2,
            quantity=3,
            canteen_id=1
        )
        assert product
        assert product.price == 10
        assert product.sub_total == 30
        assert product.name == 'Pão de Queijo'


def test_regular_purchase_model(app):
    with app.app_context():
        transaction = valid_transaction()
        assert transaction
        assert transaction.total == 61.0


def test_regular_purchase_get_by_id(app, auth, client):
    """Given an transaciton id, should get a whole purchase record including products given"""
    auth.login()
    with app.app_context(), app.test_request_context(), client:
        client.get('/')

        transaction = valid_transaction()
        transaction_id = transaction.save()

        get_transaction = RegularPurchase.get_by_id(transaction_id)
        assert get_transaction
        assert get_transaction == transaction


def test_regular_purchase_get_all(app, auth, client):
    """Should get all purchase records including products"""
    auth.login()
    with app.app_context(), app.test_request_context(), client:
        client.get('/')

        transaction = valid_transaction()
        transaction2 = RegularPurchase(
            canteen_id=1,
            products=[
                Product(id=2, quantity=4, canteen_id=1)
            ],
            payment_method='cash'
        )
        transaction.save()
        transaction2.save()
        get_transactions = RegularPurchase.get_all()

        assert get_transactions
        assert len(get_transactions) == 2


def test_regular_purchase_insert(app, auth, client):
    auth.login()
    with app.app_context(), app.test_request_context(), client:
        client.get('/')

        transaction = valid_transaction()
        transaction.save()

        canteen_balance = dao.get_canteen_balance_by_id(
            1, cash_or_bank='cash_balance')
        assert transaction
        assert canteen_balance == transaction.total


def test_user_account_purchase_insert(app, auth, client):
    auth.login()
    with app.app_context(), app.test_request_context(), client:
        client.get('/')
        initial_user_balance = dao.get_user_balance_by_id(1)

        transaction = valid_transaction(payment_method='user_account')
        transaction.save()

        user_balance = dao.get_user_balance_by_id(1)
        canteen_balance = dao.get_canteen_balance_by_id(
            1, cash_or_bank='cash_balance')
        assert transaction
        assert user_balance == initial_user_balance - transaction.total
        assert canteen_balance == 0
