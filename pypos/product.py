import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from pypos.db import get_db

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
    products = db.execute()
    return redirect(url_for('product.dashboard'))


@bp.route("/remove_product", methods=['POST'])
def remove_product():
    db = get_db()
    products = db.execute()
    return redirect(url_for('product.dashboard'))


@bp.route("/add_category", methods=['POST'])
def add_category():
    db = get_db()
    products = db.execute()
    return redirect(url_for('product.dashboard'))


@bp.route("/remove_category", methods=['POST'])
def remove_category():
    db = get_db()
    products = db.execute()
    return redirect(url_for('product.dashboard'))
