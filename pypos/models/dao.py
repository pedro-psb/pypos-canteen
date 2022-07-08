
from sqlite3 import Connection, Cursor, DatabaseError, OperationalError
from typing import List, Optional
from wsgiref.validate import validator

from pydantic import BaseModel
from pypos.db import get_db
from pypos.models.user_model import User, UserChildCreateForm, UserChildUpdateForm


def get_client_list_by_canteen_id(canteen_id: int) -> int:
    """Gets a client or client_dependent from a canteen"""
    con = get_db()
    db = con.cursor()
    query = """SELECT u.id, u.username AS name, ua.balance FROM user u
    INNER JOIN user_account ua ON u.id=ua.user_id
    WHERE u.canteen_id=? AND u.active=1 AND
    u.role_name IN ('client', 'client_dependent');"""
    user_list = db.execute(query, [canteen_id]).fetchall()
    user_list = [dict(user) for user in user_list]
    return user_list


def get_product_list_by_canteen_id(canteen_id: int) -> int:
    """Gets a client or client_dependent from a canteen"""
    con = get_db()
    db = con.cursor()
    query = """SELECT p.name, p.id, p.price, pc.name as category
    FROM product p LEFT JOIN product_category pc ON p.category = pc.id
    WHERE p.active=1 AND p.canteen_id=?;"""
    product_list = db.execute(query, [canteen_id]).fetchall()
    product_list = [dict(product) for product in product_list]
    return product_list


def get_user_account_by_user_id(user_id) -> int:
    con = get_db()
    db = con.cursor()
    query = "SELECT id FROM user_account WHERE user_id=?;"
    user_account_id = db.execute(query, [user_id]).fetchone()[0]
    return user_account_id


def get_canteen_account_id_by_canteen_id(canteen_id) -> int:
    con = get_db()
    db = con.cursor()
    query = "SELECT id FROM canteen_account WHERE canteen_id=?;"
    canteen_account_id = db.execute(query, [canteen_id]).fetchone()[0]
    return canteen_account_id


def get_user_balance_by_id(id):
    conn = get_db()
    db = conn.cursor()
    query = "SELECT balance FROM user_account WHERE user_id=?;"
    user_balance = db.execute(query, (id,)).fetchone()[0]
    return user_balance


def get_canteen_balance_by_id(id, cash_or_bank='cash_balance'):
    conn = get_db()
    db = conn.cursor()
    query = f"SELECT {cash_or_bank} FROM canteen_account WHERE canteen_id=?;"
    canteen_balance = db.execute(query, (id,)).fetchone()[0]
    return canteen_balance


def get_generic_transaction_by_id(transaction_id):
    con = get_db()
    db = con.cursor()
    query = f"SELECT * FROM generic_transaction WHERE id=?;"
    generic_transaction = db.execute(query, [transaction_id]).fetchone()
    return dict(generic_transaction)


def get_user_recharge_transaction_by_id(transaction_id):
    con = get_db()
    db = con.cursor()
    query = """SELECT gt.id, gt.total, gt.date_time,
    pay.payment_method, pay.pending, pay.discount,
    uat.user_account_id, cat.canteen_account_id
    FROM generic_transaction gt
    INNER JOIN payment_info pay ON pay.generic_transaction_id = gt.id
    INNER JOIN user_account_transaction uat ON uat.generic_transaction_id = gt.id
    INNER JOIN canteen_account_transaction cat ON cat.generic_transaction_id = gt.id
    WHERE gt.id=?;"""
    generic_transaction = db.execute(query, [transaction_id]).fetchone()
    return dict(generic_transaction)


def get_all_transactions_by_canteen_id(canteen_id):
    con = get_db()
    db = con.cursor()
    """Get all transactions and related 1 to 1 entities (except product_item and products)"""
    query = """
        SELECT gt.id, gt.total, gt.date_time, pay.payment_method, pay.discount, pay.pending,
        uat.operation_add AS uat_add, cat.operation_add AS cat_add,
        ua.id AS uat_id, u.id AS user_id, u.username AS user_name,
        payv.timestamp_code
        FROM generic_transaction gt
        LEFT JOIN payment_info pay ON gt.id = pay.generic_transaction_id
        LEFT JOIN payment_voucher payv ON payv.generic_transaction_id = gt.id
        LEFT JOIN user_account_transaction uat ON uat.generic_transaction_id=gt.id
        LEFT JOIN canteen_account_transaction cat ON cat.generic_transaction_id=gt.id
        LEFT JOIN user_account ua  ON uat.user_account_id=ua.id
        LEFT JOIN user u  ON ua.user_id = u.id
        WHERE gt.canteen_id=? AND gt.active=1;
    """
    all_transactions = db.execute(query, [canteen_id]).fetchall()
    row_total = 0
    if all_transactions:
        for i, transaction in enumerate(all_transactions):
            all_transactions[i] = dict(transaction)

            # get transaction_type_data based on user account and canteen acount operations
            transaction_type_map = get_transaction_type(
                uat_add=transaction['uat_add'], cat_add=transaction['cat_add'])
            row_total_calculator = transaction_type_map['row_total_calculator']

            row_total = row_total_calculator(row_total, transaction['total'])
            all_transactions[i]['transaction_type'] = transaction_type_map['print_name']
            all_transactions[i]['row_total'] = row_total

    return all_transactions


def get_all_transactions_by_user_id(user_id):
    """Get all user transactions data (except product_item and products)"""
    con = get_db()
    db = con.cursor()
    query = """
        SELECT gt.id, gt.total, gt.date_time, pay.payment_method, pay.discount, pay.pending,
        uat.operation_add AS uat_add, cat.operation_add AS cat_add,
        ua.id AS uat_id, u.id AS user_id, u.username AS user_name,
        payv.timestamp_code
        FROM generic_transaction gt
        INNER JOIN user_account_transaction uat ON uat.generic_transaction_id=gt.id
        LEFT JOIN payment_info pay ON gt.id = pay.generic_transaction_id
        LEFT JOIN payment_voucher payv ON payv.generic_transaction_id = gt.id
        LEFT JOIN canteen_account_transaction cat ON cat.generic_transaction_id=gt.id
        LEFT JOIN user_account ua  ON uat.user_account_id=ua.id
        LEFT JOIN user u  ON ua.user_id = u.id
        WHERE ua.user_id=? AND gt.active=1;
    """
    all_transactions = db.execute(query, [user_id]).fetchall()
    row_total = 0
    if all_transactions:
        for i, transaction in enumerate(all_transactions):
            all_transactions[i] = dict(transaction)

            # get transaction_type_data based on user account and canteen acount operations
            transaction_type_map = get_transaction_type(
                uat_add=transaction['uat_add'],
                cat_add=transaction['cat_add'],
                pending=transaction['pending'])
            row_total_calculator = transaction_type_map['row_total_calculator_user']

            row_total = row_total_calculator(row_total, transaction['total'])
            all_transactions[i]['presentation'] = transaction_type_map['presentation_user']
            all_transactions[i]['transaction_type'] = transaction_type_map['print_name']
            all_transactions[i]['row_total'] = row_total
    return all_transactions


def get_payment_voucher_code_by_transaction_id(transaction_id):
    con = get_db()
    db = con.cursor()
    query = """SELECT timestamp_code FROM payment_voucher
    WHERE generic_transaction_id=?;"""
    payment_voucher_code = db.execute(query, [transaction_id]).fetchone()[0]
    return payment_voucher_code


def get_transaction_pending_state(transaction_id):
    con = get_db()
    db = con.cursor()
    query = """SELECT pay.pending FROM generic_transaction gt
    INNER JOIN payment_info pay ON pay.generic_transaction_id = gt.id
    WHERE gt.id=? AND active=1;"""
    pending_state = db.execute(query, (transaction_id,)).fetchone()[0]
    return pending_state


def get_user_child_count(canteen_id):
    con = get_db()
    db = con.cursor()
    query = """SELECT count(*) FROM user u INNER JOIN user_child uc
    ON u.id = uc.user_id WHERE canteen_id=? AND u.active=1;"""
    user_child_count = db.execute(query, [canteen_id]).fetchone()[0]
    return user_child_count


def get_user_child_list(canteen_id):
    con = get_db()
    db = con.cursor()
    query = """SELECT u.username, u.email, u.phone_number, u.id, uc.age, uc.grade FROM user u
    INNER JOIN user_child uc ON u.id = uc.user_id WHERE canteen_id=? AND u.active=1;"""
    user_child_list = db.execute(query, [canteen_id]).fetchall()
    user_child_list = [dict(u) for u in user_child_list]
    return user_child_list


def get_user_count(canteen_id):
    con = get_db()
    db = con.cursor()
    query = """SELECT count(*) FROM user WHERE canteen_id=?;"""
    user_count = db.execute(query, [canteen_id]).fetchone()[0]
    return user_count


def get_user_by_id(user_id):
    con = get_db()
    db = con.cursor()
    query = """SELECT * FROM user u INNER JOIN user_child uc ON u.id=uc.user_id
    WHERE u.id=?;"""
    user_data = db.execute(query, [user_id]).fetchone()
    user_data = dict(user_data)
    return user_data
# Create


def create_user_child(form_data: UserChildCreateForm):
    con = get_db()
    db = con.cursor()

    # Insert regular user
    query = """INSERT INTO user (username, password, email, phone_number,
    role_name, canteen_id) VALUES (?,?,?,?,?,?);"""
    db.execute(query, [
        form_data.username, form_data.password, form_data.email,
        form_data.phone_number, form_data.role_name, form_data.canteen_id
    ])
    user_id = db.lastrowid

    # Insert user_child extension
    query = """INSERT INTO user_child (age, grade, user_provider_id, user_id)
    VALUES (?,?,?,?);"""
    db.execute(query, [
        form_data.age, form_data.grade,
        form_data.user_provider_id, user_id
    ])
    if db.rowcount < 1:
        raise ValueError('Some error ocurred with the database insert funcion')
    # Suceed
    con.commit()
    return user_id


def update_user_child(form_data: UserChildUpdateForm):
    con = get_db()
    db = con.cursor()

    # update regular user
    query = """UPDATE user SET username=:username, password=:password, email=:email,
    phone_number=:phone_number, role_name=:role_name
    WHERE id=:id;"""
    db.execute(query, form_data.dict())

    # update user_child extension
    query = """UPDATE user_child SET age=:age, grade=:grade WHERE user_id=:id;"""
    db.execute(query, form_data.dict())
    # Suceed
    con.commit()


def delete_user(user_id):
    con = get_db()
    db = con.cursor()

    # update regular user
    query = """UPDATE user SET active=0 WHERE id=?"""
    db.execute(query, [user_id])
    con.commit()

# Util


def insert_into_table(db: Cursor, table: str, **values):
    """Return a tuple of a insert query with it's values."""
    keys = [n for n in values]
    values_placeholder = ["?"] * len(keys)
    keys = ",".join(keys)
    values_placeholder = ",".join(values_placeholder)

    query = "INSERT INTO {}({}) VALUES({});".format(
        table, keys, values_placeholder)
    values = [n for n in values.values()]
    values = tuple(values)
    db.execute(query, (values))
    return db.lastrowid


def update_table(db: Cursor, table: str, **values):
    """Return a tuple of a update query with it's values.
    NOT WORKING
    """
    keys = [n for n in values]
    values_placeholder = ["?"] * len(keys)
    keys = ",".join(keys)
    values_placeholder = ",".join(values_placeholder)

    query = "UPDATE {} SET ({}) VALUES({});".format(
        table, keys, values_placeholder)
    values = [n for n in values.values()]
    values = tuple(values)
    db.execute(query, (values))
    return db.lastrowid


def insert_many_into_table(db: Cursor, table: str, list_of_values: List):
    """Return a tuple of a insert query with it's values."""
    keys = [n for n in values]
    values_placeholder = ["?"] * len(keys)
    keys = ",".join(keys)
    values_placeholder = ",".join(values_placeholder)

    query = "INSERT INTO {}({}) VALUES({});".format(
        table, keys, values_placeholder)
    values = [n for n in values.values()]
    values = tuple(values)

    db.execute(query, (values))
    return db.lastrowid


# Transactions


def add_to_account(table_name: str,
                   account_id: int,
                   account_type: str,
                   total: float,
                   con: Connection):
    query = f"UPDATE {table_name} SET {account_type}={account_type}+? WHERE id=?;"
    cur = con.execute(query, (total, account_id))
    if cur.rowcount < 1:
        raise ValueError(
            "Some error occurred while adding to the canteen account")


def is_transaction_pending(transaction_id):
    con = get_db()
    db = con.cursor()
    query = """
    SELECT pay.pending FROM generic_transaction gt INNER JOIN
    payment_info pay ON gt.id = pay.generic_transaction_id
    WHERE gt.id=?;"""
    is_pending = db.execute(query, (transaction_id,)).fetchone()[0]
    return is_pending


# TODO implement this map over the ifs. Or don't
canteen_transaction_presentation = {
    'regular_purchase': {'name': 'purchase', 'badge': 'bg-danger'},
    'user_account_purchase': {'name': 'purchase', 'badge': 'bg-danger'},
    'user_recharge': {'name': 'recharge', 'badge': 'bg-danger'},
    'user_recharge_pending': {'name': 'recharge (pending)', 'badge': 'bg-warning'},
    'canteen_withdraw': {'name': 'purchase', 'badge': 'bg-danger'},
}


# user_transaction_presentation = {
#     'regular_purchase': {'name': 'purchase', 'badge': 'bg-secondary'},
#     'user_account_purchase': {'name': 'purchase', 'badge': 'bg-danger'},
#     'user_recharge': {'name': 'recharge', 'badge': 'bg-success'},
#     'user_recharge_pending': {'name': 'recharge (pending)', 'badge': 'bg-warning'},
#     'canteen_withdraw': {'name': 'purchase', 'badge': 'bg-danger'},
# }

transaction_type_map = {
    'user_recharge': {
        'print_name': 'User Recharge',
        'uat_add': 1,
        'cat_add': None,
        'row_total_calculator': lambda x, y: x + y,
        'row_total_calculator_user': lambda x, y: x + y,
        'presentation': {'name': 'recharge', 'badge': 'bg-danger'},
        'presentation_user': {'name': 'recharge', 'badge': 'bg-success'}
    },
    'user_recharge_pending': {
        'print_name': 'User Recharge Pending',
        'uat_add': 1,
        'cat_add': None,
        'row_total_calculator': lambda x, y: x,
        'row_total_calculator_user': lambda x, y: x,
        'presentation': {'name': 'recharge (pending)', 'badge': 'bg-warning'},
        'presentation_user': {'name': 'recharge (pending)', 'badge': 'bg-secondary'}
    },
    'user_account_purchase': {
        'print_name': 'User Account Purchase',
        'uat_add': -1,
        'cat_add': None,
        'row_total_calculator': lambda x, y: x,
        'row_total_calculator_user': lambda x, y: x - y,
        'presentation': {'name': 'purchase', 'badge': 'bg-secondary'},
        'presentation_user': {'name': 'purchase', 'badge': 'bg-danger'}
    },
    'regular_purchase': {
        'print_name': 'Regular Purchase',
        'uat_add': None,
        'cat_add': 1,
        'row_total_calculator': lambda x, y: x + y,
        'row_total_calculator_user': lambda x, y: x,
        'presentation': {'name': 'recharge', 'badge': 'bg-danger'},
        'presentation_user': {'name': 'recharge', 'badge': 'bg-secondary'}
    },
    'canteen_withdraw': {
        'print_name': 'Canteen Withdraw',
        'uat_add': None,
        'cat_add': -1,
        'row_total_calculator': lambda x, y: x - y,
        'row_total_calculator_user': lambda x, y: x,
        'presentation': {'name': 'purchase', 'badge': 'bg-danger'},
        'presentation_user': {'name': 'purchase', 'badge': 'bg-secondary'}
    },
}


def get_transaction_type(uat_add, cat_add, pending=False):
    if uat_add == 1 and cat_add == 1 and not pending:
        transaction_type = 'user_recharge'
    elif uat_add == 1 and cat_add == 1 and pending:
        transaction_type = 'user_recharge_pending'
    elif uat_add == -1 and not cat_add:
        transaction_type = 'user_account_purchase'
    elif not uat_add and cat_add == 1:
        transaction_type = 'regular_purchase'
    elif not uat_add and cat_add == -1:
        transaction_type = 'canteen_withdraw'
    else:
        raise ValueError('Unknow combination')
    return transaction_type_map[transaction_type]
