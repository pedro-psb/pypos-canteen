from datetime import datetime
import json
from pprint import pprint
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
        db = get_db()
        canteen_account_id = db.execute(
            "SELECT id FROM canteen_account WHERE canteen_id=?",
            (self.canteen_id,)).fetchone()[0]

        # insert generic_transaction

        db.execute(*insert_into_table(
            'generic_transaction',
            date_time=self.date_time,
            canteen_id=self.canteen_id,
            total=self.total
        ))

        # insert payment_info

        transaction_id = db.execute(
            "SELECT last_insert_rowid();").fetchone()[0]
        db.execute(*insert_into_table(
            'payment_info',
            discount=self.discount,
            payment_method=self.payment_method,
            generic_transaction_id=transaction_id
        ))

        # insert canteen_account_transaction

        db.execute(*insert_into_table(
            'canteen_account_transaction',
            generic_transaction_id=transaction_id,
            canteen_account_id=canteen_account_id
        ))

        # insert product_items

        product_item_values = [str((p.id, p.quantity, p.sub_total, transaction_id))
                               for p in self.products]
        product_item_values = ",".join(product_item_values)
        product_item_query = f"""INSERT INTO transaction_product_item\
            (product_id, quantity, sub_total, generic_transaction_id)\
            VALUES {product_item_values};"""
        db.execute(product_item_query)
        db.commit()
        return transaction_id


def insert_into_table(table: str, **values):
    """Return a tuple of a insert query with it's values."""
    keys = [n for n in values]
    values_placeholder = ["?"] * len(keys)
    keys = ",".join(keys)
    values_placeholder = ",".join(values_placeholder)

    query = "INSERT INTO {}({}) VALUES({});".format(
        table, keys, values_placeholder)
    values = [n for n in values.values()]
    values = tuple(values)
    return (query, values)


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


# read


def get_canteen_transaction(canteen_transaction_id):
    pass


def get_user_transaction(user_transaction_id):
    pass
