from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from pydantic import ValidationError
from pypos.db import get_db
from pypos.models import dao_products
from pypos.models.forms.category_forms import UpdateCategoryForm
from pypos.models.forms.product_forms import AddProductForm, UpdateProductForm
from pypos.utils.data_utils import parse_errors
from pypos.utils.form_handler import FormWithFileHandler
from pypos.utils.form_handler.exceptions import FormError

from .errors import ADD_PRODUCT_GENERIC_ERROR, REMOVE_PRODUCT_INVALID_PRODUCT_ID
from .models import ProductCategory

bp = Blueprint("product", __name__, url_prefix="/product")


@bp.route("/add_product", methods=["POST"])
def add_product():
    try:
        # TODO make saving the img and saving to db an atomic transaction
        product = FormWithFileHandler(
            FormModel=AddProductForm,
            request=request,
            basepath=current_app.config["PRODUCT_IMG_FOLDER"],
        ).get_valid_form()
        dao_products.insert_product(product=product)
        flash("Product added sucesfully", category="success")
        return redirect(url_for("page.manage_products"))
    except FormError as e:
        errors = e.errors_by_field
        data = {"categories": dao_products.get_all_categories()}
        return render_template(
            "user/management_products_add_product.html", data=data, errors=errors
        )


@bp.route("/remove_product", methods=["POST"])
def remove_product():
    error = None
    product_id = request.form.get("id")
    # sqlite3 doesn't raise error if the id doesn't exit.
    # How do I catch the error here? (without using another query)
    product = dao_products.get_product_by_id(product_id)

    # TODO refactor this
    if not product:
        error = REMOVE_PRODUCT_INVALID_PRODUCT_ID
    else:
        if not error:
            try:
                db = get_db()
                db.execute("UPDATE product SET active=0 WHERE id=?", (product_id,))
                db.commit()
                flash(
                    message=f"Removed {product['name']} succesfuly", category="success"
                )
                return redirect(url_for("page.manage_products"))
            except:
                print("Some error has ocurred")
                error = ADD_PRODUCT_GENERIC_ERROR
    flash("Some error has occurred. Unable to remove product", category="danger")
    return redirect(url_for("page.manage_products"))


@bp.route("/add_category", methods=["POST"])
def add_category():
    form_data = request.form
    try:
        category = ProductCategory(**form_data)
        dao_products.insert_category(category)
        flash("Sucefully added product category", category="success")
        return redirect(url_for("page.manage_products"))
    except ValidationError as e:
        print(e.errors())
        errors = parse_errors(e.errors(), ProductCategory)
        return render_template(
            "user/management_products_add_category.html", errors=errors
        )


@bp.route("/remove_category", methods=["POST"])
def remove_category():
    error = None
    id = request.form.get("id")
    id = int(id)
    category = dao_products.get_category_by_id(id)
    if not category:
        error = REMOVE_PRODUCT_INVALID_PRODUCT_ID
    else:
        db = get_db()
        if not error:
            try:
                db.execute("UPDATE product_category SET active=0 WHERE id=?", (id,))
                db.execute("UPDATE product SET category=NULL WHERE category=?", (id,))
                db.commit()
                flash(
                    message=f"Removed {category['name']} succesfuly", category="success"
                )
                return redirect(url_for("page.manage_products"))
            except:
                print("some error has ocurred")
                error = ADD_PRODUCT_GENERIC_ERROR
        flash(error, category="danger")
    return redirect(url_for("page.manage_products"))


@bp.route("/update_product", methods=["POST"])
def update_product():
    """Allows updating price, category, name, etc"""
    try:
        product = FormWithFileHandler(
            FormModel=UpdateProductForm,
            request=request,
            basepath=current_app.config["PRODUCT_IMG_FOLDER"],
        ).get_valid_form()
        dao_products.update_product(product=product)
        flash("Product updated sucesfully", category="success")
        return redirect(url_for("page.manage_products"))
    except FormError as e:
        errors = e.errors_by_field
        data = {
            "categories": dao_products.get_all_categories(),
            "product": dao_products.get_product_by_id(request.form["product_id"]),
        }
        print(errors)
        return render_template(
            "user/management_products_update_product.html", data=data, errors=errors
        )


@bp.route("/update_category", methods=["POST"])
def update_category():
    """Allows updating name and description"""
    form_data = request.form
    try:
        category = UpdateCategoryForm(**form_data)
        dao_products.update_category(category=category)
        flash("Product updated sucesfully", category="success")
        return redirect(url_for("page.manage_products"))
    except ValidationError as e:
        errors = parse_errors(e.errors(), UpdateCategoryForm)
        data = {
            "category": dao_products.get_category_by_id(form_data["category_id"]),
        }
        print(errors)
        return render_template(
            "user/management_products_update_category.html", data=data, errors=errors
        )
