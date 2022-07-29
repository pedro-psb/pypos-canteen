from sqlite3 import Connection

from pypos.db import get_db
from pypos.models.dao_users import (insert_client_child_no_commit, insert_user,
                                    insert_user_account,
                                    insert_user_account_no_commit,
                                    insert_user_no_commit)
from pypos.models.user_model import User, UserChildCreateForm

from .sample_user_data import (sample_client_dependents, sample_clients,
                               sample_employees)


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
    for employee in sample_employees:
        user = User(**employee)
        insert_user_no_commit(db, user)

    # Insert Clients
    for client in sample_clients:
        user = User(**client)
        db = insert_user_no_commit(db, user)
        user_id = db.lastrowid
        insert_user_account_no_commit(db, user_id)

    # Insert Client Dependents
    for client in sample_client_dependents:
        user = UserChildCreateForm(**client)
        insert_client_child_no_commit(db, user)
    con.commit()


def setup_product_data():
    """Setup product/category data"""
    # Insert Categories
    # Insert Products


def setup_transaction_data():
    """Setup random transaction data"""
    # Insert Random Regular Transactions
    # Insert Random Recharges Transactions
    # Insert Random User Account Transactions
