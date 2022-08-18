from pathlib import Path

import pytest
from flask import Flask, url_for
from flask.testing import FlaskClient
from markupsafe import escape
from pydantic import ValidationError
from pypos.blueprints.canteen_space.product_mng.errors import *
from pypos.blueprints.canteen_space.product_mng.models import Product, ProductCategory
from pypos.db import get_db
from pypos.models import dao_products
from pypos.models.forms.product_forms import UpdateProductForm

resources = Path(__file__).parent / "_resources"
valid_product_form = {
    "name": "new_name",
    "price": "10",
    "category_id": "1",
    "file": (resources / "valid_image.jpeg").open("rb"),
}


def test_add_product(client: FlaskClient, app: Flask):
    with app.test_request_context():
        client.post(
            url_for("canteen.product.add_product"),
            data=valid_product_form,
        )

        product_name = valid_product_form["name"]
        assert dao_products.get_product_by_name(product_name)


@pytest.mark.skip(reason="no way of currently testing this")
@pytest.mark.parametrize(
    ("name", "price", "category", "message"),
    (
        ("torta", "10", "1", ADD_PRODUCT_INTEGRITY_ERROR),
        ("", "10", "1", ADD_PRODUCT_NOT_EMPTY_NAME_ERROR),
        ("valido", "", "1", ADD_PRODUCT_NOT_EMPTY_PRICE_ERROR),
        ("valido", None, "1", ADD_PRODUCT_NOT_EMPTY_PRICE_ERROR),
        ("valido", "-1", "1", ADD_PRODUCT_NOT_POSTIIVE_REAL_ERROR),
        ("valido", "10", "1.3", ADD_PRODUCT_INVALID_CATEGORY_ERROR),
        ("valido", "10", "-1", ADD_PRODUCT_INVALID_CATEGORY_ERROR),
    ),
)
def test_add_product_validation(client, app, name, price, category, message):
    with app.app_context(), app.test_request_context():
        db = get_db()
        product_count_before = db.execute("SELECT COUNT(*) FROM product").fetchone()[0]
        response = client.post(
            url_for("canteen.product.add_product"),
            data={"name": name, "price": price, "category": category},
        )
        product_count_after = db.execute("SELECT COUNT(*) FROM product").fetchone()[0]

        assert response.status_code == 302
        response = client.get(response.location)

        message = bytes(escape(message), encoding="utf-8")
        assert response.status_code == 200
        assert message in response.data
        assert product_count_after == product_count_before


def test_remove_product(client, app):
    with app.app_context(), app.test_request_context():
        db = get_db()
        rows_before = db.execute(
            "SELECT COUNT(*) FROM product WHERE active=1 AND id=1;"
        ).fetchone()[0]
        response = client.post(
            url_for("canteen.product.remove_product"), data={"id": 1}
        )
        rows_after = db.execute(
            "SELECT COUNT(*) FROM product WHERE active=1 AND id=1;"
        ).fetchone()[0]
        assert response.status_code == 302
        assert rows_after == rows_before - 1


@pytest.mark.skip(reason="no way of currently testing this")
def test_remove_product_validation(client, app):
    with app.app_context(), app.test_request_context():
        db = get_db()
        response = client.post(
            url_for("canteen.product.remove_product"), data={"id": 50}
        )
        assert response.status_code == 302
        response = client.get(response.location)
        assert response.status_code == 200

        message = bytes(escape(REMOVE_PRODUCT_INVALID_PRODUCT_ID), encoding="utf-8")
        assert message in response.data


def test_add_product_category(app):
    with app.app_context():
        category = ProductCategory(name="new name", description="some description")
        category_count_before = len(dao_products.get_all_categories())
        dao_products.insert_category(category)
        category_count_after = len(dao_products.get_all_categories())
        assert category_count_after == category_count_before + 1


def test_add_product_category_validation_unique_constrain(app):
    with app.app_context():
        # add valid category
        category_a = ProductCategory(name="new name", description="some description")
        dao_products.insert_category(category_a)

        # add category with not unique name
        with pytest.raises(ValidationError):
            category_b = ProductCategory(
                name="new name", description="some description"
            )


def test_remove_product_category(app, client):
    with app.app_context(), app.test_request_context():
        db = get_db()
        rows_before = db.execute(
            "SELECT COUNT(*) FROM product_category WHERE active=1;"
        ).fetchone()[0]
        response = client.post(
            url_for("canteen.product.remove_category"), data={"id": "1"}
        )
        rows_after = db.execute(
            "SELECT COUNT(*) FROM product_category WHERE active=1;"
        ).fetchone()[0]

        assert response.status_code == 302
        assert rows_after == rows_before - 1


# TODO turn category_id=NULL (on sqlite) to '0' for consistency
@pytest.mark.parametrize(
    ("name", "price", "category_id"),
    [
        ("foo", "1.2", "2"),
        ("foo", "1.2", "0"),  # category_id = 0 means No category
        ("torta", "1.2", "0"),  # category_id = 0 means No category
    ],
)
def test_update_product_valid(app, name, price, category_id):
    product_id = 1
    with app.app_context():
        product = UpdateProductForm(
            name=name, price=price, category_id=category_id, product_id=product_id
        )
        dao_products.update_product(product)
        product_after = dao_products.get_product_by_id(product_id)
        assert product_after["name"] == product.name
        assert product_after["price"] == product.price
        assert bool(product_after["category_id"]) == bool(product.category_id)


def test_update_product_unique_name_constrain_invalid(app):
    product_id = 2
    with app.app_context():
        with pytest.raises(ValidationError):
            UpdateProductForm(
                name="torta", price=10, category_id=1, product_id=product_id
            )
