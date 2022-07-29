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
        assert dao_products.get_product_by_name("Big Meal")
        assert dao_products.get_product_by_name("Pizza Slice")
        assert dao_products.get_product_by_name("Orange Juice")
        assert dao_products.get_category_by_name("Lunch")
        assert dao_products.get_category_by_name("Breakfast")
        assert dao_products.get_category_by_name("Juice")


def test_transactions_setup_works(app):
    with app.app_context():
        # TODO make this test more efficient
        setup.setup_transaction_data()
        regular_purchase = dao.get_generic_transaction_by_id(1)
        user_account_purchase = dao.get_generic_transaction_by_id(1)
        user_recharge = dao.get_generic_transaction_by_id(1)

        assert regular_purchase
        assert user_account_purchase
        assert user_recharge
