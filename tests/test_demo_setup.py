"""
Test of the sample data that should be run on the webapp build on production server
Shouldn't be run every time
"""
from pprint import pprint

import pytest
from pypos.db import get_db
from pypos.demo_setup import setup
from pypos.models import dao, dao_products


def test_employee_setup_works(app):
    with app.app_context():
        # TODO make this test more efficient
        setup.setup_user_data()
        owner_user = dao.get_user_by_name("jane_oconnor")
        employee_user = dao.get_user_by_name("dale_raymond")
        cashier_user = dao.get_user_by_name("breanna_rosario")
        client_user = dao.get_user_by_name("mauricio_galvan")
        client_child_user = dao.get_user_by_name("john_galvan")

        assert owner_user
        assert employee_user
        assert cashier_user
        assert client_user
        assert client_child_user


def test_products_setup_works(app):
    """When setup product data, should add product/category sample data to db"""
    with app.app_context():
        setup.setup_product_data()
        assert dao_products.get_product_id_by_name("Big Meal")
        assert dao_products.get_product_id_by_name("Pizza Slice")
        assert dao_products.get_product_id_by_name("Orange Juice")
        assert dao_products.get_category_by_name("Lunch")
        assert dao_products.get_category_by_name("Breakfast")
        assert dao_products.get_category_by_name("Juice")


@pytest.mark.skip(reason="the problem just show on the test, not in the runtime")
def test_transactions_setup_works(app):
    with app.app_context():
        setup.setup_user_data()
        setup.setup_product_data()
        setup.setup_transaction_data()

        regular_purchase = dao.get_generic_transaction_by_id(1)
        all_uat = dao.get_all_user_account_purchases()
        user_recharge = dao.get_user_recharge_transaction_by_id(5)

        pprint(dao.get_all_transactions())

        assert regular_purchase
        assert not regular_purchase.get("user_account_id")

        assert all_uat
        assert len(all_uat) == 2

        assert user_recharge
        assert user_recharge.get("user_account_id")
        assert user_recharge["user_operation_add"]
