# general_dao

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
            1, cash_or_bank='bank_account_balance')
        assert canteen_cash_balance == 0
        assert canteen_bank_account_balance == 0

def test_get_generic_transaction_by_id(app, auth, client):
    """Given an transaciton id, should get a whole purchase record including products given"""
    auth.login()
    with app.app_context(), app.test_request_context(), client:
        client.get('/')

        transaction = valid_transaction()
        transaction_id = transaction.save()

        get_transaction = get_generic_transaction_by_id(transaction_id)
        assert get_transaction
        assert get_transaction == transaction