"""Data Acess Object utilities"""

from sqlite3 import Connection, Cursor
from typing import Dict, List

from pypos.db import get_db


def get_client_list_by_canteen_id(canteen_id: int) -> List[Dict]:
    """Gets all clients or client_dependents data from a canteen"""
    con = get_db()
    db = con.cursor()
    query = """SELECT u.id, u.username, u.phone_number, u.email,u.role_name,
    ua.id AS account_id, ua.balance, "" AS user_provider_name
    FROM user u INNER JOIN user_account ua ON u.id=ua.user_id
    WHERE u.canteen_id=? AND u.active=1 AND
    u.role_name IN ('client')
    UNION
    SELECT u.id, u.username, u.phone_number, u.email, u.role_name,
    ua.id AS account_id, ua.balance, 
    (SELECT username FROM user WHERE id=uc.user_provider_id) AS user_provider_name
    FROM user u INNER JOIN user_child uc ON u.id=uc.user_id
    INNER JOIN user_account ua ON ua.id=uc.user_provider_id;
    """
    user_list = db.execute(query, [canteen_id]).fetchall()
    user_list = [dict(user) for user in user_list]
    return user_list


def get_user_account_by_user_id(user_id: int) -> Dict:
    """Get user account data for regular client or child client"""
    con = get_db()
    db = con.cursor()
    query = """SELECT ua.id, ua.balance,
    ua.negative_limit, ua.user_id FROM user u
    INNER JOIN user_account ua ON u.id=ua.user_id WHERE u.id=?
    UNION
    SELECT ua.id, ua.balance, ua.negative_limit, ua.user_id
    FROM user_account ua WHERE ua.user_id=(
        SELECT uc.user_provider_id FROM user u INNER JOIN user_child uc
        ON u.id=uc.user_id WHERE u.id=?
        );
    """
    user_account = db.execute(query, [user_id, user_id]).fetchone()
    user_account = dict(user_account) if user_account else {}

    return user_account


def get_user_balance_by_id(user_id: int) -> float | None:
    """DEPRECATED. Use get_user_account_by_user_id() instead"""
    user_account = get_user_account_by_user_id(user_id)
    user_balance = user_account.get("balance")
    return user_balance


def get_canteen_account_id_by_canteen_id(canteen_id) -> int:
    con = get_db()
    db = con.cursor()
    query = "SELECT id FROM canteen_account WHERE canteen_id=?;"
    canteen_account_id = db.execute(query, [canteen_id]).fetchone()[0]
    return canteen_account_id


def get_canteen_balance() -> Dict:
    """get cash_balance and bank_account_balance from canteen_account"""
    conn = get_db()
    db = conn.cursor()
    query = "SELECT * FROM canteen_account WHERE canteen_id=1;"
    canteen_balance = db.execute(query).fetchone()
    canteen_balance = dict(canteen_balance) if canteen_balance else {}
    return canteen_balance


def get_generic_transaction_by_id(transaction_id: int) -> dict | None:
    con = get_db()
    db = con.cursor()
    query = "SELECT * FROM generic_transaction WHERE id=?;"
    generic_transaction = db.execute(query, [transaction_id]).fetchone()
    generic_transaction = dict(generic_transaction) if generic_transaction else None
    return generic_transaction


def get_all_user_account_purchases() -> List[Dict]:
    con = get_db()
    db = con.cursor()
    query = """
    SELECT gt.id, gt.total, gt.date_time, pay.payment_method,
    pay.discount, pay.pending, uat.operation_add AS uat_add,
    ua.id AS uat_id, u.id AS user_id, u.username AS username
    FROM generic_transaction gt
    INNER JOIN user_account_transaction uat ON uat.generic_transaction_id=gt.id
    INNER JOIN payment_info pay ON pay.generic_transaction_id=gt.id
    INNER JOIN user_account ua ON ua.user_id=uat.user_account_id
    INNER JOIN user u ON u.id=ua.user_id
    WHERE uat.operation_add=-1;
    """
    transactions = db.execute(query).fetchall()
    transactions = [dict(t) for t in transactions] if transactions else [{}]
    return transactions


def get_user_account_purchase_transaction_by_id(transaction_id) -> Dict:
    con = get_db()
    db = con.cursor()
    query = """SELECT * FROM generic_transaction gt
    INNER JOIN user_account_transaction uat ON uat.generic_transaction_id=gt.id
    INNER JOIN payment_info pay ON pay.generic_transaction_id=gt.id
    WHERE gt.id=? AND uat.operation_add=-1;"""
    transaction = db.execute(query, [transaction_id]).fetchone()
    transaction = dict(transaction) if transaction else {}
    return transaction


def get_user_recharge_transaction_by_id(transaction_id):
    con = get_db()
    db = con.cursor()
    query = """SELECT gt.id, gt.total, gt.date_time,
    pay.payment_method, pay.pending, pay.discount,
    uat.user_account_id, cat.canteen_account_id,
    uat.operation_add AS user_operation_add
    FROM generic_transaction gt
    INNER JOIN payment_info pay ON pay.generic_transaction_id = gt.id
    INNER JOIN user_account_transaction uat ON uat.generic_transaction_id = gt.id
    INNER JOIN canteen_account_transaction cat ON cat.generic_transaction_id = gt.id
    WHERE gt.id=?;"""
    transaction = db.execute(query, [transaction_id]).fetchone()
    transaction = dict(transaction) if transaction else {}
    return transaction


def get_all_transactions(canteen_id=1):
    """Get all transactions and related 1 to 1 entities (except product_item and products)"""
    con = get_db()
    db = con.cursor()
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
                uat_add=transaction["uat_add"], cat_add=transaction["cat_add"]
            )
            row_total_calculator = transaction_type_map["row_total_calculator"]

            row_total = row_total_calculator(row_total, transaction["total"])
            all_transactions[i]["transaction_type"] = transaction_type_map["print_name"]
            all_transactions[i]["row_total"] = row_total

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
                uat_add=transaction["uat_add"],
                cat_add=transaction["cat_add"],
                pending=transaction["pending"],
            )
            row_total_calculator = transaction_type_map["row_total_calculator_user"]

            row_total = row_total_calculator(row_total, transaction["total"])
            all_transactions[i]["presentation"] = transaction_type_map[
                "presentation_user"
            ]
            all_transactions[i]["transaction_type"] = transaction_type_map["print_name"]
            all_transactions[i]["row_total"] = row_total
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


def get_user_children_form_provider(user_id: int):
    con = get_db()
    db = con.cursor()
    query = """SELECT u.username, u.email, u.phone_number, u.id, uc.age, uc.grade FROM user u
    INNER JOIN user_child uc ON u.id = uc.user_id WHERE uc.user_provider_id=? AND u.active=1;"""
    user_child_list = db.execute(query, [user_id]).fetchall()
    user_child_list = [dict(u) for u in user_child_list]
    return user_child_list


def get_user_count(canteen_id=1):
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


def get_user_by_name(user_name: str) -> Dict:
    """Get user and user_child data by `username`. Data as is in the schema"""
    con = get_db()
    db = con.cursor()
    query = """SELECT u.username, u.id, u.email, u.phone_number, u.password,
    u.phone_number, u.role_name, u.active, u.canteen_id, c.name as canteen_name,
    uc.age, uc.grade, uc.user_provider_id
    FROM user u LEFT JOIN user_child uc ON u.id=uc.user_id
    INNER JOIN canteen c ON c.id=u.canteen_id WHERE u.username=?;"""
    user_data = db.execute(query, [user_name]).fetchone()
    user_data: Dict = dict(user_data) if user_data else {}
    return user_data


# Util


def insert_into_table(db: Cursor, table: str, **values):
    """Return a tuple of a insert query with it's values."""
    keys = [n for n in values]
    values_placeholder = ["?"] * len(keys)
    keys = ",".join(keys)
    values_placeholder = ",".join(values_placeholder)

    query = "INSERT INTO {}({}) VALUES({});".format(table, keys, values_placeholder)
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

    query = "UPDATE {} SET ({}) VALUES({});".format(table, keys, values_placeholder)
    values = [n for n in values.values()]
    values = tuple(values)
    db.execute(query, (values))
    return db.lastrowid


# def insert_many_into_table(db: Cursor, table: str, list_of_values: List):
#     """Return a tuple of a insert query with it's values."""
#     keys = [n for n in values]
#     values_placeholder = ["?"] * len(keys)
#     keys = ",".join(keys)
#     values_placeholder = ",".join(values_placeholder)

#     query = "INSERT INTO {}({}) VALUES({});".format(
#         table, keys, values_placeholder)
#     values = [n for n in values.values()]
#     values = tuple(values)

#     db.execute(query, (values))
#     return db.lastrowid


# Transactions


def add_to_account(
    table_name: str, account_id: int, account_type: str, total: float, con: Connection
):
    query = f"UPDATE {table_name} SET {account_type}={account_type}+? WHERE id=?;"
    cur = con.execute(query, (total, account_id))
    if cur.rowcount < 1:
        raise ValueError("Some error occurred while adding to the canteen account")


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
    "regular_purchase": {"name": "purchase", "badge": "bg-danger"},
    "user_account_purchase": {"name": "purchase", "badge": "bg-danger"},
    "user_recharge": {"name": "recharge", "badge": "bg-danger"},
    "user_recharge_pending": {"name": "recharge (pending)", "badge": "bg-warning"},
    "canteen_withdraw": {"name": "purchase", "badge": "bg-danger"},
}


# user_transaction_presentation = {
#     'regular_purchase': {'name': 'purchase', 'badge': 'bg-secondary'},
#     'user_account_purchase': {'name': 'purchase', 'badge': 'bg-danger'},
#     'user_recharge': {'name': 'recharge', 'badge': 'bg-success'},
#     'user_recharge_pending': {'name': 'recharge (pending)', 'badge': 'bg-warning'},
#     'canteen_withdraw': {'name': 'purchase', 'badge': 'bg-danger'},
# }

transaction_type_map = {
    "user_recharge": {
        "print_name": "User Recharge",
        "uat_add": 1,
        "cat_add": None,
        "row_total_calculator": lambda x, y: x + y,
        "row_total_calculator_user": lambda x, y: x + y,
        "presentation": {"name": "recharge", "badge": "bg-danger"},
        "presentation_user": {"name": "recharge", "badge": "bg-success"},
    },
    "user_recharge_pending": {
        "print_name": "User Recharge Pending",
        "uat_add": 1,
        "cat_add": None,
        "row_total_calculator": lambda x, y: x,
        "row_total_calculator_user": lambda x, y: x,
        "presentation": {"name": "recharge (pending)", "badge": "bg-warning"},
        "presentation_user": {"name": "recharge (pending)", "badge": "bg-secondary"},
    },
    "user_account_purchase": {
        "print_name": "User Account Purchase",
        "uat_add": -1,
        "cat_add": None,
        "row_total_calculator": lambda x, y: x,
        "row_total_calculator_user": lambda x, y: x - y,
        "presentation": {"name": "purchase", "badge": "bg-secondary"},
        "presentation_user": {"name": "purchase", "badge": "bg-danger"},
    },
    "regular_purchase": {
        "print_name": "Regular Purchase",
        "uat_add": None,
        "cat_add": 1,
        "row_total_calculator": lambda x, y: x + y,
        "row_total_calculator_user": lambda x, y: x,
        "presentation": {"name": "recharge", "badge": "bg-danger"},
        "presentation_user": {"name": "recharge", "badge": "bg-secondary"},
    },
    "canteen_withdraw": {
        "print_name": "Canteen Withdraw",
        "uat_add": None,
        "cat_add": -1,
        "row_total_calculator": lambda x, y: x - y,
        "row_total_calculator_user": lambda x, y: x,
        "presentation": {"name": "purchase", "badge": "bg-danger"},
        "presentation_user": {"name": "purchase", "badge": "bg-secondary"},
    },
}


def get_transaction_type(uat_add, cat_add, pending=False):
    if uat_add == 1 and cat_add == 1 and not pending:
        transaction_type = "user_recharge"
    elif uat_add == 1 and cat_add == 1 and pending:
        transaction_type = "user_recharge_pending"
    elif uat_add == -1 and not cat_add:
        transaction_type = "user_account_purchase"
    elif not uat_add and cat_add == 1:
        transaction_type = "regular_purchase"
    elif not uat_add and cat_add == -1:
        transaction_type = "canteen_withdraw"
    else:
        raise ValueError("Unknow combination")
    return transaction_type_map[transaction_type]
