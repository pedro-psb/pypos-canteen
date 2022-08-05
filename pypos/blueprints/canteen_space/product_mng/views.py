import sqlite3

from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from pydantic import ValidationError
from pypos.db import get_db
from pypos.models import dao_products

from .errors import (
    ADD_PRODUCT_GENERIC_ERROR,
    ADD_PRODUCT_INTEGRITY_ERROR,
    REMOVE_PRODUCT_INVALID_PRODUCT_ID,
)
from .models import Product, ProductCategory

bp = Blueprint("product", __name__, url_prefix="/product")


@bp.route("/add_product", methods=["POST"])
def add_product():
    db = get_db()

    product = Product(
        request.form.get("name"),
        request.form.get("price"),
        request.form.get("category"),
    )
    error = product.validate()
    # Database Dependent Validation
    if error is None:
        try:
            dao_products.insert_product(db=db, product=product)
            db.commit()
            return redirect(url_for("page.manage_products"))
        except sqlite3.OperationalError:  # TODO handle this better
            print("some error ocurred")
            error = ADD_PRODUCT_INTEGRITY_ERROR
    flash(error)
    return redirect(url_for("page.manage_products_add_product"))


@bp.route("/remove_product", methods=["POST"])
def remove_product():
    error = None
    id = request.form.get("id")
    db = get_db()
    # sqlite3 doesn't raise error if the id doesn't exit.
    # How do I catch the error here? (without using another query)
    id_exist = db.execute("SELECT id FROM product WHERE id=?", (id,)).fetchall()
    id_exist = len(id_exist)

    if not id_exist:
        error = REMOVE_PRODUCT_INVALID_PRODUCT_ID

    if not error:
        try:
            db.execute("UPDATE product SET active=0 WHERE id=?", (id,))
            db.commit()
            return redirect(url_for("page.manage_products"))
        except:
            print("some error has ocurred")
            error = ADD_PRODUCT_GENERIC_ERROR
    flash(error)
    return redirect(url_for("page.manage_products"))


@bp.route("/add_category", methods=["POST"])
def add_category():
    form_data = request.form
    try:
        category = ProductCategory(
            name=request.form.get("name"),
            description=request.form.get("description"),
        )
        dao_products.insert_category(category)
        flash("Sucefully added product category")
        return redirect(url_for("page.manage_products"))
    except ValidationError as e:
        print(e.errors())
        errors = e.errors()
        return render_template(
            "user/management_products_add_category.html", errors=errors
        )

    # flash(error)
    return redirect(url_for("page.manage_products_add_category"))


@bp.route("/remove_category", methods=["POST"])
def remove_category():
    error = None
    id = request.form.get("id")
    id = int(id)
    db = get_db()
    # sqlite3 doesn't raise error if the id doesn't exit.
    # How do I catch the error here? (without using another query)
    id_exist = db.execute(
        "SELECT id FROM product_category WHERE id=?", (id,)
    ).fetchall()
    id_exist = len(id_exist)
    if not id_exist:
        error = REMOVE_PRODUCT_INVALID_PRODUCT_ID

    if not error:
        try:
            db.execute("UPDATE product_category SET active=0 WHERE id=?", (id,))
            db.execute("UPDATE product SET category=NULL WHERE category=?", (id,))
            db.commit()
            return redirect(url_for("page.manage_products"))
        except:
            print("some error has ocurred")
            error = ADD_PRODUCT_GENERIC_ERROR
    flash(error)
    return redirect(url_for("page.manage_products"))


@bp.route("/update_product", methods=["POST"])
def update_product():
    """Allows updating price, category, name, etc"""
    db = get_db()
    product_id = int(request.form.get("id"))
    product = Product(
        request.form.get("name"),
        request.form.get("price"),
        request.form.get("category"),
        id=product_id,
    )
    error = product.validate()
    # Database Dependent Validation
    if error is None:
        try:
            if product.category != "None":
                query = "UPDATE product SET name=?, price=?, category=? WHERE id=?;"
                db.execute(
                    query, (product.name, product.price, product.category, product.id)
                )
            else:
                query = "UPDATE product SET name=?, price=?, category=NULL WHERE id=?;"
                db.execute(query, (product.name, product.price, product.id))
            db.commit()
            return redirect(url_for("page.manage_products"))
        except:
            print("some error ocurred")
            print(product.id, product.name)
            error = ADD_PRODUCT_INTEGRITY_ERROR
    flash(error)
    return redirect(url_for("page.manage_products_update_product", id=product_id))


@bp.route("/update_category", methods=["POST"])
def update_category():
    """Allows updating name and description"""
    db = get_db()
    category = ProductCategory(
        id=request.form.get("id"),
        name=request.form.get("name"),
        description=request.form.get("description"),
    )
    error = category.validate()
    # Database Dependent Validation
    if error is None:
        try:
            query = """UPDATE product_category SET name=?, description=? WHERE id=?;"""
            db.execute(query, (category.name, category.description, category.id))
            db.commit()
            return redirect(url_for("page.manage_products"))
        except:
            print("some error ocurred")
            error = ADD_PRODUCT_INTEGRITY_ERROR
    flash(error)
    return redirect(url_for("page.manage_products_update_category", id=category.id))
