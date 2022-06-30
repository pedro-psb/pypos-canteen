from pprint import pprint
from flask import g, session
import pytest

from pypos.db import get_db
from pypos.models import dao
from pypos.models.transactions_dao import (
    Product,
    RegularPurchase,
    UserAccountPurchase
)

#   ("torta", 15.5, 1),
#   ("Pão de Queijo", 10, 1),
#   ("Prato Feito", 10, 2)


def valid_transaction(Transaction=RegularPurchase,
                      payment_method='cash',
                      client_account_id=None
                      ):
    transaction = Transaction(
        canteen_id=1,
        client_account_id=client_account_id,
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


def test_regular_purchase_get_all(app, auth, client):
    """Should get all purchase records including products"""
    auth.login()
    with app.app_context(), app.test_request_context(), client:
        client.get('/')

        canteen_transaction = valid_transaction()
        canteen_transaction2 = RegularPurchase(
            canteen_id=1,
            products=[
                Product(id=2, quantity=4, canteen_id=1)
            ],
            payment_method='cash'
        )
        user_acc_transaction = valid_transaction(
            Transaction=UserAccountPurchase,
            payment_method='user_account',
            client_account_id=1
        )
        canteen_transaction.save()
        canteen_transaction2.save()
        user_acc_transaction.save()

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

        transaction = valid_transaction(
            Transaction=UserAccountPurchase,
            payment_method='user_account',
            client_account_id=1
        )
        print(transaction.total)
        transaction.save()

        user_balance = dao.get_user_balance_by_id(1)
        canteen_balance = dao.get_canteen_balance_by_id(
            1, cash_or_bank='cash_balance')
        assert transaction
        assert user_balance == initial_user_balance - transaction.total
        assert canteen_balance == 0


def test_user_account_purchase_get_all(app, auth, client):
    """Should get all purchase records including products"""
    auth.login()
    with app.app_context(), app.test_request_context(), client:
        client.get('/')

        user_acc_transaction = valid_transaction(
            Transaction=UserAccountPurchase,
            payment_method='user_account',
            client_account_id=1
        )
        user_acc_transaction2 = UserAccountPurchase(
            canteen_id=1,
            client_account_id=1,
            products=[
                Product(id=2, quantity=4, canteen_id=1)
            ],
            payment_method='user_account'
        )
        canteen_transaction = valid_transaction()
        user_acc_transaction.save()
        user_acc_transaction2.save()
        canteen_transaction.save()

        get_transactions = UserAccountPurchase.get_all()
        assert get_transactions
        assert len(get_transactions) == 2
