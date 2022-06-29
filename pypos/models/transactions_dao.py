from datetime import datetime
import json
from multiprocessing.sharedctypes import Value
from pprint import pprint
from sqlite3 import Connection, Cursor
from typing import List
from xxlimited import foo

from flask import session
from pypos.db import get_db
from pydantic import BaseModel, root_validator


class Product(BaseModel):
    id: int
    canteen_id: int
    quantity: int
    name: str = ''
    price: float = 0
    sub_total: float = 0

    @root_validator
    def load_product_data(cls, values):
        db = get_db()
        data = db.execute("SELECT * FROM product WHERE id=?",
                          (values['id'],)).fetchone()
        values['name'] = data['name']
        values['price'] = data['price']
        values['sub_total'] = values['price'] * values['quantity']
        return values


class Recharge:
    date_time: datetime = datetime.now()
    canteen_account_id: int
    user_account_id: int
    total: float
    payment_method_id: int

    def get_all(cls):
        pass

    def do(cls):
        pass


class RegularPurchase(BaseModel):
    """A purchase paid in the POS"""
    date_time: str = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
    products: List[Product]
    canteen_id: int
    payment_method: str
    discount: float = 0
    total: float = 0

    @root_validator
    def calculate_total(cls, values):
        total = sum(product.sub_total for product in values['products'])
        values['total'] = total

        return values

    @classmethod
    def get_by_id(cls, transaction_id):
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

    @classmethod
    def get_all(cls):
        db = get_db()
        canteen_id = session.get('canteen_id', 1)
        query = """
        SELECT gt.canteen_id, gt.date_time, pay.payment_method, pay.discount, gt.total, 
        group_concat('{"name":"' || p.name || '","quantity":"' || tpi.quantity || 
        '","price":"' || p.price || '","sub_total":"' || tpi.sub_total || 
        '","id":"' || p.id || '","canteen_id":"' || p.canteen_id || '"}') AS products 
        FROM generic_transaction gt 
        INNER JOIN transaction_product_item tpi ON gt.id=tpi.generic_transaction_id 
        INNER JOIN payment_info pay ON gt.id=pay.generic_transaction_id 
        INNER JOIN product p ON p.id = tpi.product_id 
        GROUP BY gt.id HAVING p.canteen_id=?;"""
        all_transactions_data = db.execute(query, (canteen_id,)).fetchall()
        all_transactions = []
        for transaction in all_transactions_data:
            transaction = dict(transaction)
            products = f"[{transaction.get('products')}]"
            products = json.loads(products)
            products = [Product(**product) for product in products]
            transaction['products'] = products
            transaction = RegularPurchase(**transaction)
            all_transactions.append(transaction)

        return all_transactions

    def save(self):
        user_id = session.get('user_id')
        canteen_id = session.get('canteen_id')
        if not user_id or not canteen_id:
            raise ValueError('User must be logged in')
        conn = get_db()
        db = conn.cursor()
        canteen_account_id = db.execute(
            "SELECT id FROM canteen_account WHERE canteen_id=?",
            (self.canteen_id,)).fetchone()[0]

        # add to balance canteen_account/user_account

        if self.payment_method == 'user_account':
            db.execute('UPDATE user_account SET balance = balance-? WHERE id=? AND balance>=?;',
                       (self.total, user_id, self.total))
            if db.rowcount < 1:
                raise ValueError("User don't have enought balance")
        elif self.payment_method == 'cash':
            query = 'UPDATE canteen_account SET cash_balance=cash_balance+? WHERE id=?;'
            db.execute(query, (self.total, canteen_account_id))
        elif self.payment_method == 'debit_card':
            query = 'UPDATE canteen_account SET bank_account_balance=bank_account_balance+? WHERE id=?;'
            db.execute(query, (self.total, canteen_account_id))

        if db.rowcount < 1:
            raise ValueError(
                "Some error occurred while adding to the canteen account")

        # insert generic_transaction

        insert_into_table(
            db, 'generic_transaction',
            date_time=self.date_time,
            canteen_id=self.canteen_id,
            total=self.total
        )

        # insert payment_info

        transaction_id = db.lastrowid
        insert_into_table(
            db, 'payment_info',
            discount=self.discount,
            payment_method=self.payment_method,
            generic_transaction_id=transaction_id
        )

        # insert canteen_account_transaction

        insert_into_table(
            db, 'canteen_account_transaction',
            generic_transaction_id=transaction_id,
            canteen_account_id=canteen_account_id
        )

        # insert product_items

        product_item_values = [str((p.id, p.quantity, p.sub_total, transaction_id))
                               for p in self.products]
        product_item_values = ",".join(product_item_values)
        product_item_query = f"""INSERT INTO transaction_product_item\
            (product_id, quantity, sub_total, generic_transaction_id)\
            VALUES {product_item_values};"""
        db.execute(product_item_query)
        conn.commit()

        return transaction_id


class UserAccountPurchase:
    date_time: datetime = datetime.now()
    canteen_id: int
    user_account_id: int
    amount: float
    discount: float
    products: List[Product]

    def get_all(cls):
        pass

    def do(cls):
        pass


class CanteenWithdraw:
    date_time: datetime = datetime.now()
    canteen_id: int
    amount: float

    def get_all(cls):
        pass

    def do(cls):
        pass


# util

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
