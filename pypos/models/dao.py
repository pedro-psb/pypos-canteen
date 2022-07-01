
from sqlite3 import Connection, Cursor
from typing import List
from pypos.db import get_db
from pypos.models.transactions_dao import RegularPurchase, UserRecharge


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
    db = get_db()
    transaction_query = """SELECT gt.date_time, gt.total, gt.canteen_id,
        pay.discount, pay.payment_method FROM generic_transaction gt
        INNER JOIN payment_info pay ON gt.id = pay.generic_transaction_id
        WHERE gt.id=? AND gt.active=1;"""
    products_query = """SELECT p.canteen_id, p.id, p.name, p.price, tpi.quantity, 
        tpi.sub_total FROM product p INNER JOIN transaction_product_item tpi 
        ON p.id = tpi.product_id WHERE tpi.generic_transaction_id=? AND p.active=1;"""

    transaction = dict(db.execute(transaction_query,
                       (transaction_id,)).fetchone())
    products = db.execute(products_query, (transaction_id,)).fetchall()
    products = [dict(p) for p in products]
    transaction['products'] = products
    transaction = RegularPurchase(**transaction)
    return transaction


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


payment_options = {
    'cash': 'cash_balance',
    'pix': 'bank_account_balance',
    'debit_card': 'bank_account_balance',
    'credit_card': 'bank_account_balance',
    'DOC/TED': 'bank_account_balance',
}


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


def reject_pending_transaction(transaction_id):
    con = get_db()
    db = con.cursor()
    db.execute("""UPDATE payment_info SET pending=0
               WHERE generic_transaction_id=?;""", (transaction_id,))


def accept_pending_transaction(transaction: UserRecharge):
    con = get_db()
    db = con.cursor()
    add_to_account(
        table_name='canteen_account',
        total=transaction.total,
        account_id=transaction.canteen_account_id,
        account_type=payment_options[transaction.payment_method],
        conn=con
    )
    add_to_account(
        table_name='user_account',
        total=transaction.total,
        account_id=transaction.user_account_id,
        account_type='balance',
        conn=con
    )
    db.execute("""UPDATE payment_info SET pending=0
               WHERE generic_transaction_id=?;""", (transaction.id,))



def is_transaction_pending(transaction_id):
    con = get_db()
    db = con.cursor()
    query = """
    SELECT pay.pending FROM generic_transaction gt INNER JOIN
    payment_info pay ON gt.id = pay.generic_transaction_id
    WHERE gt.id=?;"""
    is_pending = db.execute(query, (transaction_id,)).fetchone()[0]
    return is_pending
