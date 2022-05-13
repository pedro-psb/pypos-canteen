import functools

from unicodedata import category
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from pypos.db import get_db
from pypos.errors import *

bp = Blueprint('product', __name__, url_prefix='/product')


@bp.route("/")
def dashboard():
    db = get_db()
    products = db.execute(
        "SELECT product.name, product.price, product.id, product_category.name as category_name "
        "FROM product JOIN product_category "
        "ON product.category = product_category.id;"
    ).fetchall()
    return render_template("product/dashboard.html", products=products)


@bp.route("/add_product", methods=['POST'])
def add_product():
    error = None
    db = get_db()

    name = request.form.get("name")
    price = request.form.get("price")
    category = request.form.get("category")

    # Name
    if not name:
        error = ADD_PRODUCT_NOT_EMPTY_NAME_ERROR
    
    # Price
    if not price:
        error = ADD_PRODUCT_NOT_EMPTY_PRICE_ERROR
    try:
        price = float(price)
    except:
        error = ADD_PRODUCT_INVALID_PRICE_ERROR
    else:
        if price < 0:
            error = ADD_PRODUCT_NOT_POSTIIVE_REAL_ERROR
    
    # Category
    '''
    I don't know if it is best to catch the error in the DB or before sending the query.
    The example in the Flask Tutorial catches the error in the DB with the IntegrityError exception,
    but catching it early can save a query.
    '''
    try:
        category = int(category)
    except ValueError:
        error = ADD_PRODUCT_INVALID_CATEGORY_ERROR
    else:
        if category <= 0:
            error = ADD_PRODUCT_INVALID_CATEGORY_ERROR
    
    # Database Dependent Validation
    if error is None:
        products = {
            "name": name,
            "price": price,
            "category": category
        }
        try:
            db.execute(
                "INSERT INTO product(name, price, category) "
                "VALUES (?,?,?);",
                (tuple([*products.values()])))
        except db.IntegrityError:
            error = ADD_PRODUCT_INTEGRITY_ERROR
        else:
            return redirect(url_for('product.dashboard'))
    flash(error)
    return redirect(url_for('index'))

@bp.route("/remove_product", methods=['POST'])
def remove_product():
    product_id = request.form.get('product_id')
    db = get_db()
    db.execute('UPDATE product SET active=0 WHERE id=?', (product_id,))
    return redirect(url_for('index'))


# @bp.route("/add_category", methods=['POST'])
# def add_category():
#     db = get_db()
#     products = db.execute()
#     return redirect(url_for('product.dashboard'))


# @bp.route("/remove_category", methods=['POST'])
# def remove_category():
#     db = get_db()
#     products = db.execute()
#     return redirect(url_for('product.dashboard'))


# Unknown syntax error with sqlite
# def dump_db(db, table="user"):
#     query = db.execute("SELECT * FROM ?", (table,)).fetchall()
#     for row in query:
#         print(dict(row))
