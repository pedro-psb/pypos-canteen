"""DAO for products and categories"""
from sqlite3 import Cursor
from typing import List

from pypos.blueprints.canteen_space.product_mng.models import Product, ProductCategory
from pypos.db import get_db


# INSERT
def insert_product(db: Cursor, product: Product) -> Cursor:
    query = """INSERT INTO product(name, price, category, canteen_id)
    VALUES (?,?,?,1);"""
    db.execute(
        query,
        [
            product.name,
            product.price,
            product.category,
        ],
    )
    return db


def insert_category(db: Cursor, product: ProductCategory) -> Cursor:
    query = """INSERT INTO product_category(name, description)
    VALUES (?,?);"""
    db.execute(
        query,
        [product.name, product.description],
    )
    return db


# GET


def get_product_by_name(product_name: str) -> str:
    """Gets a product by it's name"""
    db = get_db()
    query = """SELECT p.id, p.name, p.price, c.name,
    c.id AS category_id
    FROM product p LEFT JOIN product_category c ON
    p.category = c.id WHERE p.name=?"""
    product = db.execute(query, [product_name]).fetchone()
    product = product[0] if product else ""
    return product


def get_category_by_name(category_name: str) -> str:
    """Gets a category by it's name"""
    db = get_db()
    query = """SELECT * FROM product_category WHERE name=?"""
    product = db.execute(query, [category_name]).fetchone()
    product = product[0] if product else ""
    return product


def get_product_list_by_canteen_id(canteen_id: int) -> List:
    """Gets a client or client_dependent from a canteen"""
    con = get_db()
    db = con.cursor()
    query = """SELECT p.name, p.id, p.price, pc.name as category
    FROM product p LEFT JOIN product_category pc ON p.category = pc.id
    WHERE p.active=1 AND p.canteen_id=?;"""
    product_list = db.execute(query, [canteen_id]).fetchall()
    product_list = [dict(product) for product in product_list]
    return product_list
