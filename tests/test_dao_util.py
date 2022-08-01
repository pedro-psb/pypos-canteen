# general_dao

import pytest
from pypos.models import dao

from tests.test_dao_transactions import valid_transaction


def test_get_user_balance_by_id(app):
    with app.app_context(), app.test_request_context():
        user_balance = dao.get_user_balance_by_id(1)
        assert user_balance == 100


def test_get_canteen_balance_by_id(app):
    with app.app_context(), app.test_request_context():
        canteen_cash_balance = dao.get_canteen_balance_by_id(1)
        canteen_bank_account_balance = dao.get_canteen_balance_by_id(
            1, cash_or_bank="bank_account_balance"
        )
        assert canteen_cash_balance == 0
        assert canteen_bank_account_balance == 0


def test_get_generic_transaction_by_id(app, auth, client):
    """Given an transaciton id, should get a generic_transaction row"""
    auth.login()
    with app.app_context(), app.test_request_context(), client:
        client.get("/")

        transaction = valid_transaction()
        transaction_id = transaction.save()

        get_transaction = dao.get_generic_transaction_by_id(transaction_id)
        assert get_transaction
        assert get_transaction["date_time"] == transaction.date_time
        assert get_transaction["total"] == transaction.total


def test_get_user_account_id_by_id(app):
    """Get user account id by a user id"""
    with app.app_context(), app.test_request_context():
        user_account_id = dao.get_user_account_by_user_id(1)
        assert user_account_id == 1


def test_get_user_account_by_user_id(app):
    """Should return the same account_id for both provider and child"""
    with app.app_context():
        provider_account_id = dao.get_user_account_by_user_id(1)
        child_account_id = dao.get_user_account_by_user_id(7)
        assert provider_account_id == child_account_id
