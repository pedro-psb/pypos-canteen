import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from pypos.db import get_db

bp = Blueprint('product', __name__, url_prefix='/product')

@bp.route("/")
def index():
    db = get_db()
    products = db.execute(
        "SELECT product.name, product.price, product.id, product_category.name as category_name "
        "FROM product JOIN product_category "
        "ON product.category = product_category.id;"
        ).fetchall()
    return render_template("product/index.html", products=products)