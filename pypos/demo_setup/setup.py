from pypos.blueprints.canteen_space.product_mng.models import Product, ProductCategory
from pypos.db import get_db
from pypos.models.dao_products import insert_category, insert_product
from pypos.models.dao_users import (
    insert_client_child_no_commit,
    insert_user_account_no_commit,
    insert_user_no_commit,
)
from pypos.models.transactions_dao import (
    RegularPurchase,
    UserAccountPurchase,
    UserRecharge,
)
from pypos.models.user_model import User, UserChildCreateForm

from .sample_product_data import sample_categories, sample_products
from .sample_transaction_data import (
    sample_regular_purchase,
    sample_user_account_purchase,
    sample_user_recharge,
)
from .sample_user_data import sample_client_dependents, sample_clients, sample_employees


def setup_sample_data():
    """Setup sample data for the demo"""
    setup_user_data()
    setup_product_data()
    setup_transaction_data()


def setup_user_data():
    """Setup user data"""
    con = get_db()
    db = con.cursor()
    # Insert Employees
    for employee in sample_employees():
        user = User(**employee)
        insert_user_no_commit(db, user)

    # Insert Clients
    for client in sample_clients():
        user = User(**client)
        db = insert_user_no_commit(db, user)
        user_id: int = db.lastrowid  # type: ignore
        insert_user_account_no_commit(db, user_id)

    # Insert Client Dependents
    for client in sample_client_dependents():
        user = UserChildCreateForm(**client)
        insert_client_child_no_commit(db, user)
    con.commit()


def setup_product_data():
    """Setup product/category data"""
    con = get_db()
    db = con.cursor()

    # Insert Categories
    for category in sample_categories:
        category = ProductCategory(**category)
        insert_category(db, category)

    # Insert Products
    for product in sample_products:
        product = Product(**product)
        insert_product(db, product)
    con.commit()


def setup_transaction_data():
    """Setup random transaction data"""
    # Insert Random User Account Transactions
    for data in sample_user_recharge():
        transaction = UserRecharge(**data)
        transaction.save()

    # Insert Random Regular Transactions
    for data in sample_regular_purchase():
        transaction = RegularPurchase(**data)
        transaction.save()

    # Insert Random Recharges Transactions
    for data in sample_user_account_purchase():
        transaction = UserAccountPurchase(**data)
        transaction.save()
