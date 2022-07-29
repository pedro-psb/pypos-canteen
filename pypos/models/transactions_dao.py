import json
from datetime import datetime
from pprint import pprint
from sqlite3 import Connection, Cursor
from typing import List, Optional
from wsgiref.validate import validator

from flask import session
from pydantic import (BaseModel, PositiveFloat, ValidationError, parse_obj_as,
                      root_validator)
from pypos.db import get_db
from pypos.models import dao

payment_options = {
    'cash': 'cash_balance',
    'pix': 'bank_account_balance',
    'debit_card': 'bank_account_balance',
    'credit_card': 'bank_account_balance',
    'DOC/TED': 'bank_account_balance',
}


class NullFieldError(Exception):
    pass


class Product(BaseModel):
    id: int
    canteen_id: Optional[int]
    quantity: int
    name: str = ''
    price: float = 0
    sub_total: float = 0

    @ root_validator
    def load_product_data(cls, values):
        db = get_db()
        data = db.execute("SELECT * FROM product WHERE id=?",
                          (values['id'],)).fetchone()
        values['name'] = data['name']
        values['price'] = data['price']
        values['sub_total'] = values['price'] * values['quantity']
        return values


class UserRecharge(BaseModel):
    # default
    date_time: datetime = datetime.strftime(
        datetime.now(), "%Y-%m-%d %H:%M:%S")
    discount: float = 0
    id: Optional[int]

    # required
    canteen_id: Optional[int]
    user_id: Optional[int]
    payment_method: str
    pending: bool
    total: PositiveFloat
    timestamp_code: Optional[str]

    # calculated
    canteen_account_id: Optional[int]
    user_account_id: Optional[int]
    presentation: Optional[dict]

    @root_validator()
    def set_presentation(cls, values):
        if values.get('pending'):
            values['presentation'] = dao.transaction_type_map['user_recharge_pending']['presentation']
        else:
            values['presentation'] = dao.transaction_type_map['user_recharge']['presentation']
        return values

    # One or the other cases
    @root_validator()
    def canteen_id_or_canteen_account_id_required(cls, values):
        if not values.get('canteen_id') and not values.get('canteen_account_id'):
            raise ValueError("Must provide canteen_id or canteen_account_id")
        if not values.get('canteen_account_id'):
            conn = get_db()
            db = conn.cursor()
            canteen_account_id = db.execute(
                "SELECT id FROM canteen_account WHERE canteen_id=?",
                [values['canteen_id']]).fetchone()[0]
            values['canteen_account_id'] = canteen_account_id
        return values

    @root_validator()
    def user_id_or_user_account_id_required(cls, values):
        if not values.get('user_id') and not values.get('user_account_id'):
            raise ValueError("Must provide user_id or user_account_id")
        if not values.get('user_account_id'):
            conn = get_db()
            db = conn.cursor()
            user_account_id = db.execute(
                "SELECT id FROM user_account WHERE user_id=?",
                (values['user_id'],)).fetchone()[0]
            values['user_account_id'] = user_account_id
        return values

    @root_validator()
    def timestamp_required_on_pending(cls, values):
        if values.get('pending') and not values.get('timestamp_code'):
            raise ValueError(
                'If transaction is pending, timestamp_code must be informed')
        return values

    def get_all(self):
        pass

    def save(self):
        conn = get_db()
        db = conn.cursor()

        # insert generic_transaction

        dao.insert_into_table(
            db, 'generic_transaction',
            date_time=self.date_time,
            canteen_id=self.canteen_id,
            total=self.total
        )
        transaction_id = db.lastrowid

        # add to canteen account or create payment voucher

        if not self.pending:
            dao.add_to_account(
                table_name='canteen_account',
                total=self.total,
                account_id=self.canteen_account_id,
                account_type=payment_options[self.payment_method],
                con=conn
            )
            dao.add_to_account(
                table_name='user_account',
                total=self.total,
                account_id=self.user_account_id,
                account_type='balance',
                con=conn
            )
        else:
            dao.insert_into_table(
                db, 'payment_voucher',
                timestamp_code=self.timestamp_code,
                generic_transaction_id=transaction_id,
            )

        # insert payment_info

        dao.insert_into_table(
            db, 'payment_info',
            discount=self.discount,
            payment_method=self.payment_method,
            pending=self.pending,
            generic_transaction_id=transaction_id
        )

        # insert canteen_account_transaction

        dao.insert_into_table(
            db, 'canteen_account_transaction',
            operation_add=True,
            generic_transaction_id=transaction_id,
            canteen_account_id=self.canteen_account_id
        )

        dao.insert_into_table(
            db, 'user_account_transaction',
            operation_add=True,
            generic_transaction_id=transaction_id,
            user_account_id=self.user_account_id
        )
        conn.commit()
        self.id = transaction_id
        return transaction_id


class RegularPurchase(BaseModel):
    """A purchase paid with cash or card in the POS"""
    presentation: Optional[dict]
    canteen_id: int
    date_time: str = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
    products: List[Product]
    payment_method: str
    discount: float = 0
    total: float = 0

    # calculated
    canteen_account_id: Optional[int]
    user_account_id: Optional[int]

    @root_validator()
    def canteen_id_or_canteen_account_id_required(cls, values):
        if not values.get('canteen_id') and not values.get('canteen_account_id'):
            raise ValueError("Must provide canteen_id or canteen_account_id")
        if not values.get('canteen_account_id'):
            conn = get_db()
            db = conn.cursor()
            canteen_account_id = db.execute(
                "SELECT id FROM canteen_account WHERE canteen_id=?",
                [values['canteen_id']]).fetchone()[0]
            values['canteen_account_id'] = canteen_account_id
        return values

    @root_validator(pre=True)
    def parse_products(cls, values):
        products = values.get('products')
        if not products:
            raise ValueError('Products not informed')
        elif isinstance(products, str):
            values['products'] = []
            products = json.loads(products)
            for p in products:
                p['canteen_id'] = values['canteen_id']
                values['products'].append(p)
        return values

    @root_validator
    def calculate_total(cls, values):
        total = sum(product.sub_total for product in values['products'])
        values['total'] = total
        return values

    @ classmethod
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
        INNER JOIN canteen_account_transaction cat ON cat.generic_transaction_id = gt.id
        LEFT JOIN user_account_transaction uat ON uat.generic_transaction_id = cat.generic_transaction_id
        GROUP BY gt.id HAVING p.canteen_id=? AND uat.generic_transaction_id IS NULL;"""
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
        conn = get_db()
        db = conn.cursor()

        # add to cash/bank balance in canteen account
        canteen_account_id = self.canteen_account_id

        canteen_account_type = payment_options[self.payment_method]
        query = f'UPDATE canteen_account SET {canteen_account_type}={canteen_account_type}+? WHERE id=?;'
        db.execute(query, (self.total, canteen_account_id))

        if db.rowcount < 1:
            raise ValueError(
                "Some error occurred while adding to the canteen account")

        # insert generic_transaction

        dao.insert_into_table(
            db, 'generic_transaction',
            date_time=self.date_time,
            canteen_id=self.canteen_id,
            total=self.total
        )

        # insert payment_info

        transaction_id = db.lastrowid
        dao.insert_into_table(
            db, 'payment_info',
            discount=self.discount,
            payment_method=self.payment_method,
            generic_transaction_id=transaction_id
        )

        # insert canteen_account_transaction

        dao.insert_into_table(
            db, 'canteen_account_transaction',
            operation_add=True,
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


class UserAccountPurchase(BaseModel):
    """A purchase paid with the user account balance in the POS"""
    presentation: Optional[dict]
    date_time: str = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
    products: List[Product]

    canteen_id: Optional[int]
    canteen_account_id: Optional[int]
    client_id: Optional[int]
    client_account_id: Optional[int]

    payment_method: str
    discount: float = 0
    total: float = 0
    pending: bool = False

    @root_validator(pre=True)
    def parse_products(cls, values):
        products = values.get('products')
        if not products:
            raise ValueError('Products not informed')
        elif isinstance(products, str):
            values['products'] = []
            products = json.loads(products)
            for p in products:
                p['canteen_id'] = values['canteen_id']
                values['products'].append(p)
        return values

    @root_validator
    def get_client_and_canteen_account_id(cls, values):
        client_id = values.get('client_id')
        client_account_id = values.get('client_account_id')
        canteen_id = values.get('canteen_id')
        canteen_account_id = values.get('canteen_account_id')
        if not client_account_id:
            if not client_id:
                raise ValueError("Must provide client_id or client_account_id")
            values['client_account_id'] = dao.get_user_account_by_user_id(
                client_id)
        if not canteen_account_id:
            if not canteen_id:
                raise ValueError(
                    "Must provide canteen_id or canteen_account_id")
            values['canteen_account_id'] = dao.get_canteen_account_id_by_canteen_id(
                canteen_id)
        return values

    @root_validator
    def calculate_total(cls, values):
        total = sum(product.sub_total for product in values['products'])
        values['total'] = total
        return values

    @classmethod
    def get_all(cls):
        db = get_db()
        canteen_id = session.get('canteen_id', 1)
        query = """
        SELECT gt.canteen_id, gt.date_time, gt.total,
        pay.payment_method, pay.discount, pay.pending,
        group_concat('{"name":"' || p.name || '","quantity":"' || tpi.quantity ||
        '","price":"' || p.price || '","sub_total":"' || tpi.sub_total ||
        '","id":"' || p.id || '","canteen_id":"' || p.canteen_id || '"}') AS products
        FROM generic_transaction gt
        INNER JOIN transaction_product_item tpi ON gt.id=tpi.generic_transaction_id
        INNER JOIN payment_info pay ON gt.id=pay.generic_transaction_id
        INNER JOIN product p ON p.id = tpi.product_id
        INNER JOIN user_account_transaction uat ON uat.generic_transaction_id = gt.id
        LEFT JOIN canteen_account_transaction cat ON uat.generic_transaction_id = cat.generic_transaction_id
        GROUP BY gt.id HAVING p.canteen_id=? AND cat.generic_transaction_id IS NULL;"""
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
        conn = get_db()
        db = conn.cursor()
        # add to client account

        db.execute("""UPDATE user_account SET balance = balance-:total
                   WHERE id = :acc_id AND balance + negative_limit >= :total; """,
                   {"total": self.total, "acc_id": self.client_account_id})
        if db.rowcount < 1:
            raise ValueError("User don't have enought balance")

        # insert generic_transaction

        dao.insert_into_table(
            db, 'generic_transaction',
            date_time=self.date_time,
            canteen_id=self.canteen_id,
            total=self.total
        )

        # insert payment_info

        transaction_id = db.lastrowid
        dao.insert_into_table(
            db, 'payment_info',
            discount=self.discount,
            payment_method='user_account',
            generic_transaction_id=transaction_id
        )

        # insert user_account_transaction

        dao.insert_into_table(
            db, 'user_account_transaction',
            operation_add=-1,
            generic_transaction_id=transaction_id,
            user_account_id=self.client_account_id
        )

        # insert product_items

        product_item_values = [str((p.id, p.quantity, p.sub_total, transaction_id))
                               for p in self.products]
        product_item_values = ",".join(product_item_values)
        product_item_query = f"""INSERT INTO transaction_product_item(product_id, quantity, sub_total, generic_transaction_id)\
            VALUES {product_item_values}; """
        db.execute(product_item_query)
        conn.commit()

        return transaction_id


class CanteenWithdraw:
    presentation: Optional[dict]
    date_time: datetime = datetime.now()
    canteen_id: int
    amount: float

    def get_all(cls):
        pass

    def save(cls):
        pass

# Utils (can't go to dao module because of circular imports)


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


def accept_pending_transaction(transaction_id):
    # TODO can I use typehints from other modules without doing circular imports?
    con = get_db()
    db = con.cursor()
    transaction = dao.get_user_recharge_transaction_by_id(transaction_id)
    dao.add_to_account(
        table_name='canteen_account',
        total=transaction["total"],
        account_id=transaction["canteen_account_id"],
        account_type=payment_options[transaction["payment_method"]],
        con=con
    )
    dao.add_to_account(
        table_name='user_account',
        total=transaction["total"],
        account_id=transaction["user_account_id"],
        account_type='balance',
        con=con
    )
    db.execute("""UPDATE payment_info SET pending=0
               WHERE generic_transaction_id=?;""", [transaction["id"]])
    con.commit()


def reject_pending_transaction(transaction_id):
    con = get_db()
    db = con.cursor()
    db.execute("""UPDATE payment_info SET pending=0
               WHERE generic_transaction_id=?;""", [transaction_id])
    db.execute("""UPDATE generic_transaction SET active=0
               WHERE id=?;""", [transaction_id])
    con.commit()
