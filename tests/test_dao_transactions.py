from multiprocessing.sharedctypes import Value
from pprint import pprint
from flask import g, session
import pytest

from pypos.db import get_db
from pypos.models import dao
from pypos.models.transactions_dao import (
    Product,
    RegularPurchase,
    UserAccountPurchase,
    UserRecharge,
    accept_pending_transaction,
    reject_pending_transaction,
    transaction_presentations
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


def valid_recharge_transaction(payment_method='pix',
                               user_id=1,
                               total=20,
                               pending=False,
                               timestamp_code='foo'):
    if not pending:
        transaction = UserRecharge(
            canteen_id=1,
            user_id=user_id,
            total=total,
            payment_method=payment_method,
            pending=pending
        )
    else:
        transaction = UserRecharge(
            canteen_id=1,
            user_id=user_id,
            total=total,
            payment_method=payment_method,
            pending=pending,
            timestamp_code=timestamp_code
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


def test_user_recharge_model(app):
    with app.app_context():
        transaction = valid_recharge_transaction(total=20)
        transaction_pending = valid_recharge_transaction(pending=True)
        assert transaction

        # calculated values
        assert transaction.canteen_account_id == 1
        assert transaction.user_account_id == 1
        assert transaction.presentation == transaction_presentations['user_recharge']
        assert transaction_pending.presentation ==\
            transaction_presentations['user_recharge_pending']

        # test pending-timestamp_code dependency
        with pytest.raises(ValueError):
            transaction_pending = valid_recharge_transaction(
                pending=True,
                timestamp_code=None)


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
        canteen_transaction.save()
        canteen_transaction2.save()

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
        user_acc_transaction.save()
        user_acc_transaction2.save()

        get_transactions = UserAccountPurchase.get_all()
        assert get_transactions
        assert len(get_transactions) == 2


def test_user_recharge_save(app, auth, client):
    auth.login()
    with app.app_context(), app.test_request_context(), client:
        client.get('/')
        initial_user_balance = dao.get_user_balance_by_id(1)
        initial_canteen_balance = dao.get_canteen_balance_by_id(
            1, cash_or_bank='bank_account_balance')

        transaction = valid_recharge_transaction(
            total=10, pending=False)
        transaction.save()

        user_balance = dao.get_user_balance_by_id(1)
        canteen_balance = dao.get_canteen_balance_by_id(
            1, cash_or_bank='bank_account_balance')
        assert transaction
        assert user_balance == initial_user_balance + transaction.total
        assert canteen_balance == initial_canteen_balance + transaction.total


def test_user_recharge_pending_save(app, auth, client):
    auth.login()
    with app.app_context(), app.test_request_context(), client:
        client.get('/')
        initial_user_balance = dao.get_user_balance_by_id(1)
        initial_canteen_balance = dao.get_canteen_balance_by_id(
            1, cash_or_bank='bank_account_balance')

        transaction = valid_recharge_transaction(
            total=10, pending=True)
        transaction_id = transaction.save()
        transaction_pending_state = dao.get_transaction_pending_state(
            transaction_id)

        user_balance = dao.get_user_balance_by_id(1)
        canteen_balance = dao.get_canteen_balance_by_id(
            1, cash_or_bank='bank_account_balance')
        assert transaction
        assert user_balance == initial_user_balance
        assert canteen_balance == initial_canteen_balance
        assert transaction_pending_state == True


def test_user_recharge_pending_accept(app, auth, client):
    auth.login()
    with app.app_context(), app.test_request_context(), client:
        client.get('/')
        initial_user_balance = dao.get_user_balance_by_id(1)
        initial_canteen_balance = dao.get_canteen_balance_by_id(
            1, cash_or_bank='bank_account_balance')

        transaction = valid_recharge_transaction(
            total=10, pending=True)
        transaction_id = transaction.save()
        # accept call
        accept_pending_transaction(transaction)
        is_transaction_pending = dao.is_transaction_pending(transaction_id)

        # after accept balance
        user_balance = dao.get_user_balance_by_id(1)
        canteen_balance = dao.get_canteen_balance_by_id(
            1, cash_or_bank='bank_account_balance')
        assert transaction
        assert user_balance == initial_user_balance + transaction.total
        assert canteen_balance == initial_canteen_balance + transaction.total
        assert is_transaction_pending == False


def test_user_recharge_pending_reject(app, auth, client):
    auth.login()
    with app.app_context(), app.test_request_context(), client:
        client.get('/')
        initial_user_balance = dao.get_user_balance_by_id(1)
        initial_canteen_balance = dao.get_canteen_balance_by_id(
            1, cash_or_bank='bank_account_balance')

        transaction = valid_recharge_transaction(
            total=10, pending=True)
        transaction_id = transaction.save()

        # accept call
        reject_pending_transaction(transaction_id)
        is_transaction_pending = dao.is_transaction_pending(transaction_id)

        # after reject balance
        user_balance = dao.get_user_balance_by_id(1)
        canteen_balance = dao.get_canteen_balance_by_id(
            1, cash_or_bank='bank_account_balance')
        assert transaction
        assert user_balance == initial_user_balance
        assert canteen_balance == initial_canteen_balance
        assert is_transaction_pending == False


def test_user_recharge_get_all(app, auth, client):
    pass
