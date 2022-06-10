import functools
from re import L

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from pypos.db import get_db
from .errors import *
from .models import Product, ProductCategory
from . import bp

bp = Blueprint('product', __name__, url_prefix='/product')


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
            db.commit()
            return redirect(url_for('page.manage_products'))
        except:
            print('some error ocurred')
            error = ADD_PRODUCT_INTEGRITY_ERROR
    flash(error)
    return redirect(url_for('page.manage_products_add_product'))


@bp.route("/remove_product", methods=['POST'])
def remove_product():
    error = None
    id = request.form.get('id')
    db = get_db()
    # sqlite3 doesn't raise error if the id doesn't exit.
    # How do I catch the error here? (without using another query)
    id_exist = db.execute(
        'SELECT id FROM product WHERE id=?', (id,)).fetchall()
    id_exist = len(id_exist)
    
    if not id_exist:
        error = REMOVE_PRODUCT_INVALID_PRODUCT_ID

    if not error:
        try:
            db.execute('UPDATE product SET active=0 WHERE id=?', (id,))
            db.commit()
            return redirect(url_for('page.manage_products'))
        except:
            print('some error has ocurred')
            error = ADD_PRODUCT_GENERIC_ERROR
    flash(error)
    return redirect(url_for('page.manage_products'))


@bp.route("/add_category", methods=['POST'])
def add_category():
    category = ProductCategory(
        request.form.get('name'),
        request.form.get('description')
    )
    error = category.validate()
    if not error:
        try:
            db = get_db()
            db.execute('INSERT INTO product_category(name, description) VALUES (?,?);',
                       (category.name, category.description))
            db.commit()
            flash("Sucefully added product category")
            return redirect(url_for('page.manage_products'))
        except:
            print('some error ocurred')
            error = ADD_PRODUCT_GENERIC_ERROR

    flash(error)
    return redirect(url_for('page.manage_products_add_category'))


@bp.route("/remove_category", methods=['POST'])
def remove_category():
    error = None
    id = request.form.get('id')
    id = int(id)
    db = get_db()
    # sqlite3 doesn't raise error if the id doesn't exit.
    # How do I catch the error here? (without using another query)
    id_exist = db.execute(
        'SELECT id FROM product_category WHERE id=?', (id,)).fetchall()
    id_exist = len(id_exist)
    if not id_exist:
        error = REMOVE_PRODUCT_INVALID_PRODUCT_ID
    
    if not error:
        try:
            db.execute('UPDATE product_category SET active=0 WHERE id=?', (id,))
            db.commit()
            return redirect(url_for('page.manage_products'))
        except:
            print('some error has ocurred')
            error = ADD_PRODUCT_GENERIC_ERROR
    flash(error)
    return redirect(url_for('page.manage_products'))


@bp.route("/update_product")
def update_product():
    '''Allows updating price, category, name, etc'''
    pass
