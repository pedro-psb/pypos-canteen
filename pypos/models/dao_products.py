"""DAO for products and categories"""
from sqlite3 import Cursor
from typing import Dict, List

from pypos.blueprints.canteen_space.product_mng.models import Product, ProductCategory
from pypos.db import get_db
from pypos.models.forms.category_forms import UpdateCategoryForm
from pypos.models.forms.product_forms import AddProductForm, UpdateProductForm


# INSERT
def insert_product(product: AddProductForm) -> int | None:
    """Insert product and return it's id"""
    con = get_db()
    db = con.cursor()
    product_id = _insert_product(db, product)
    con.commit()
    return product_id


def _insert_product(db: Cursor, product: AddProductForm) -> int | None:
    if product.category_id:
        db.execute(
            """INSERT INTO product(name, price, category, filepath)
        VALUES (?,?,?,?);""",
            [product.name, product.price, product.category_id, product.file],
        )
    else:
        db.execute(
            """INSERT INTO product(name, price)
        VALUES (?,?);""",
            [
                product.name,
                product.price,
            ],
        )
    return db.lastrowid


def insert_category(product: ProductCategory):
    con = get_db()
    db = con.cursor()
    _insert_category(db=db, product=product)
    con.commit()


def _insert_category(db: Cursor, product: ProductCategory) -> Cursor:
    query = """INSERT INTO product_category(name, description)
    VALUES (?,?);"""
    db.execute(
        query,
        [product.name, product.description],
    )
    return db


def update_product(product: UpdateProductForm):
    """Updates a product"""
    con = get_db()
    db = con.cursor()
    db.execute(
        """UPDATE product SET name=:name, category=:category_id, price=:price
    WHERE id=:product_id;""",
        product.dict(),
    )
    con.commit()
    return db.lastrowid


def update_category(category: UpdateCategoryForm):
    """Updates a category"""
    con = get_db()
    db = con.cursor()
    db.execute(
        """UPDATE product_category SET name=:name, description=:description
    WHERE id=:category_id;""",
        category.dict(),
    )
    con.commit()
    return db.lastrowid


# GET


def get_product_by_id(product_id: int) -> Dict:
    """Gets a product by it's id"""
    db = get_db()
    query = """SELECT p.id, p.name, p.price, c.name,
    c.id AS category_id
    FROM product p LEFT JOIN product_category c ON
    p.category = c.id WHERE p.id=?"""
    product = db.execute(query, [product_id]).fetchone()
    product = dict(product) if product else None
    return product


def get_product_by_name(product_name: str) -> Dict:
    """Gets a product by it's name"""
    db = get_db()
    query = """SELECT p.id, p.name, p.price, c.name,
    c.id AS category_id
    FROM product p LEFT JOIN product_category c ON
    p.category = c.id WHERE p.name=?"""
    product = db.execute(query, [product_name]).fetchone()
    product = dict(product) if product else None
    return product


def get_product_id_by_name(product_name: str) -> str:
    """Gets a product id by it's name"""
    product = get_product_by_name(product_name)
    return product["id"]


def get_category_by_id(category_id: int) -> Dict:
    """Get a single category from it's id"""
    db = get_db()
    category = db.execute(
        "SELECT * FROM product_category WHERE id=?;", [category_id]
    ).fetchone()
    category = dict(category) if category else {}
    return category


def get_category_by_name(category_name: str) -> Dict:
    """Get a single category from it's name"""
    db = get_db()
    category = db.execute(
        "SELECT * FROM product_category WHERE name=?;", [category_name]
    ).fetchone()
    category = dict(category) if category else {}
    return category


def get_all_categories() -> List[Dict]:
    """Get all categories"""
    db = get_db()
    query = "SELECT * FROM product_category;"
    result = db.execute(query).fetchall()
    result = [dict(item) for item in result] if result else []
    return result


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
