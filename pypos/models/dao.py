
from sqlite3 import Connection, Cursor
from typing import List
from pypos.db import get_db


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


def get_all_client_transactions(client_id):
    # get account_id
    # query purchases and recharges
    # transform each row in a ClientPurchase or ClientRecharge
    pass


def get_transaction_pending_state(transaction_id):
    con = get_db()
    db = con.cursor()
    query = """SELECT pay.pending FROM generic_transaction gt
    INNER JOIN payment_info pay ON pay.generic_transaction_id = gt.id
    WHERE gt.id=?;"""
    pending_state = db.execute(query, (transaction_id,)).fetchone()[0]
    return pending_state

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
                   conn: Connection):
    query = f"UPDATE {table_name} SET {account_type}={account_type}+? WHERE id=?;"
    cur = conn.execute(query, (total, account_id))
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
