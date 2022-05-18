import functools

from unicodedata import category
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from pypos.db import get_db
from pypos.errors import *
from pypos.models import Product

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
    db = get_db()

    product = Product(
        request.form.get("name"),
        request.form.get("price"),
        request.form.get("category")
    )
    error = product.validate()

    # Database Dependent Validation
    if error is None:
        try:
            db.execute(
                "INSERT INTO product(name, price, category) "
                "VALUES (?,?,?);",
                (product.name, product.price, product.category))
        except db.IntegrityError:
            error = ADD_PRODUCT_INTEGRITY_ERROR
        else:
            return redirect(url_for('product.dashboard'))
    flash(error)
    return redirect(url_for('index'))


@bp.route("/remove_product", methods=['POST'])
def remove_product():
    error = None
    product_id = request.form.get('product_id')
    db = get_db()
    # sqlite3 doesn't raise error if the id doesn't exit.
    # How do I catch the error here? (without using another query)
    id_exist = db.execute('SELECT id FROM product WHERE id=?', (product_id,)).fetchall()
    id_exist = len(id_exist)
    if id_exist:
        db.execute('UPDATE product SET active=0 WHERE id=?', (product_id,))
    else:
        error = REMOVE_PRODUCT_INVALID_PRODUCT_ID
    
    flash(error)
    return redirect(url_for('index'))


@bp.route("/add_category", methods=['POST'])
def add_category():
    name = request.form.get('category_name').strip()
    error = ''
    if not name:
        error = 'Category must have a name'

    db = get_db()
    db.execute('INSERT INTO product_category(name) VALUES (?);', (name,))
    flash("Sucefully added product category")
    return redirect(url_for('index'))


@bp.route("/remove_category", methods=['POST'])
def remove_category():
    category_id = request.form.get('category_id').strip()
    error = ''
    if not category_id:
        error = 'Invalid operation'

    db = get_db()
    db.execute('UPDATE product_category SET active=0 WHERE id=?', (category_id,))
    flash("Sucefully deleted product category")
    return redirect(url_for('index'))
