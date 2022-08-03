# general_dao

from pprint import pprint
from typing import Dict, List

from pypos.models import dao
from pypos.models.transactions_dao import (
    Product,
    RegularPurchase,
    UserAccountPurchase,
    UserRecharge,
)
from tests.dao.test_dao_transactions import valid_transaction


def test_get_user_balance_by_id(app):
    with app.app_context(), app.test_request_context():
        user_balance = dao.get_user_balance_by_id(1)
        assert user_balance == 100


def test_get_canteen_balance(app):
    with app.app_context(), app.test_request_context():
        canteen_cash_balance = dao.get_canteen_balance()["cash_balance"]
        canteen_bank_account_balance = dao.get_canteen_balance()["bank_account_balance"]
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


def test_get_user_account_purchase(app):
    with app.app_context():
        # setup all types of purchase
        setup_single_transactions()

        # verify the function can select the purchase it
        wrong_transaction1 = dao.get_user_account_purchase_transaction_by_id(1)
        user_purchase = dao.get_user_account_purchase_transaction_by_id(2)
        wrong_transaction2 = dao.get_user_account_purchase_transaction_by_id(3)
        print(wrong_transaction2)
        assert not wrong_transaction1
        assert user_purchase
        assert not wrong_transaction2


def test_get_all_user_account_purchases(app):
    with app.app_context():
        # setup all [types]' of purchase
        # user_child_1 provider account is ('test', id=1)
        setup_single_transactions(
            additional_transactions=[
                UserAccountPurchase(
                    products=[Product(id=1, quantity=1)],
                    client_id=dao.get_user_by_name("user_child_1")["id"],
                    payment_method="user_account",
                )
            ]
        )
        # verify the function can select the purchase it
        all_uat = dao.get_all_user_account_purchases()
        fake_client_uat = filter_dicts_username(dicts=all_uat, filter="fake_client")
        test_client_uat = filter_dicts_username(dicts=all_uat, filter="test")
        assert all_uat
        assert fake_client_uat
        assert test_client_uat
        assert len(all_uat) == 2
        assert len(fake_client_uat) == 1
        assert len(test_client_uat) == 1


def filter_dicts(dicts: List[Dict], dict_key: str, filter: str) -> List[Dict]:
    """Filter a list of dicts by a `dict_key` that matches a `filter` value"""
    # TODO move to dict utils
    filtered_result = [item for item in dicts if item[dict_key] == filter]
    return filtered_result


def filter_dicts_username(dicts: List[Dict], filter: str):
    """Filter a list of dicts by 'username' that matches a `filter` value"""
    # TODO move to dict utils
    return filter_dicts(dicts=dicts, dict_key="username", filter=filter)


def setup_single_transactions(additional_transactions: List = None):
    """Setup the following transactions:
    - RegularPurchase id=1
    - UserAccountPurhcase id=2
    - UserRecharge id=3
    """
    regular_purchase = RegularPurchase(
        payment_method="cash",
        products=[Product(id=2, quantity=1), Product(id=2, quantity=3)],
    )
    user_purchase = UserAccountPurchase(
        payment_method="user_account", products=[Product(id=2, quantity=1)], client_id=5
    )
    user_recharge = UserRecharge(
        payment_method="cash", user_id=5, pending=False, total=9.87
    )
    regular_purchase.save()
    user_purchase.save()
    user_recharge.save()
    if additional_transactions:
        for t in additional_transactions:
            t.save()


def test_get_user_account_id_by_id(app):
    """Get user account id by a user id"""
    with app.app_context(), app.test_request_context():
        user_account = dao.get_user_account_by_user_id(1)
        assert user_account["id"] == 1


def test_get_user_account_by_user_id(app):
    """Should return the same account_id for both provider and child"""
    with app.app_context():
        provider_account_id = dao.get_user_account_by_user_id(1).get("id")
        child_account_id = dao.get_user_account_by_user_id(7).get("id")
        assert provider_account_id == child_account_id
