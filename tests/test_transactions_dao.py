from pprint import pprint
from pydantic import ValidationError
import pytest
from pypos.db import get_db
from pypos.models.transactions_dao import (
    Product,
    RegularPurchase,
    get_canteen_transaction,
    get_user_transaction
)

#   ("torta", 15.5, 1),
#   ("Pão de Queijo", 10, 1),
#   ("Prato Feito", 10, 2)


def test_product_model(app):
    with app.app_context():
        product = Product(
            id=2,
            quantity=3,
            canteen_id=1
        )
        assert product
        assert product.price == 10
        assert product.sub_total == 30
        assert product.name == 'Pão de Queijo'


def test_regular_purchase_model(app):
    with app.app_context():
        transaction = RegularPurchase(
            canteen_id=1,
            products=[
                Product(id=1, quantity=2, canteen_id=1),
                Product(id=2, quantity=3, canteen_id=1)
            ],
            payment_method='cash'
        )
        assert transaction
        assert transaction.total == 61.0


def test_regular_purchase_get_by_id(app):
    with app.app_context():
        transaction = RegularPurchase(
            canteen_id=1,
            products=[
                Product(id=1, quantity=2, canteen_id=1),
                Product(id=2, quantity=3, canteen_id=1)
            ],
            payment_method='cash'
        )
        transaction_id = transaction.save()
        get_transaction = RegularPurchase.get_by_id(transaction_id)
        assert get_transaction
        assert get_transaction == transaction

def test_regular_purchase_get_all(app):
    with app.app_context(), app.test_request_context():
        transaction = RegularPurchase(
            canteen_id=1,
            products=[
                Product(id=1, quantity=2, canteen_id=1),
                Product(id=2, quantity=3, canteen_id=1)
            ],
            payment_method='cash'
        )
        transaction2 = RegularPurchase(
            canteen_id=1,
            products=[
                Product(id=2, quantity=4, canteen_id=1)
            ],
            payment_method='cash'
        )
        transaction.save()
        transaction2.save()
        get_transactions = RegularPurchase.get_all()

        assert get_transactions
        assert len(get_transactions) == 2

def test_regular_purchase_insert(app):
    with app.app_context():
        transaction = RegularPurchase(
            canteen_id=1,
            products=[
                Product(id=1, quantity=2, canteen_id=1),
                Product(id=2, quantity=3, canteen_id=1)
            ],
            payment_method='cash'
        )
        transaction.save()
        assert transaction
