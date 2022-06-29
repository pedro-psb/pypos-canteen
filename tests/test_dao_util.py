# general_dao

from pypos.models import dao


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