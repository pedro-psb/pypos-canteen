import pytest
from pydantic import ValidationError
from pypos.db import get_db
from pypos.models import dao_products
from pypos.models.forms.product_forms import AddProductForm


def test_valid_add_product_form(app):
    with app.app_context():
        form = AddProductForm(
            name="bread",
            price=10,
            category_id=dao_products.get_category_by_name("Lanche").get("id"),  # type: ignore
        )
        assert form


@pytest.mark.parametrize(
    "name,price,category_id",
    [
        ("", "", ""),
        ("", 10, 1),
        ("valid_name", 0, 1),
        ("valid_name", -3, 1),
        ("valid_name", 10, 10),
    ],
)
def test_invalid_add_product_form(app, name, price, category_id):
    with app.app_context():
        with pytest.raises(ValidationError):
            form = AddProductForm(name=name, price=price, category_id=category_id)
            assert form


def test_unique_name_constrain(app):
    with app.app_context():
        product_a = AddProductForm(name="valid_name", price=10, category_id=1)
        dao_products.insert_product(product_a)
        with pytest.raises(ValidationError):
            AddProductForm(name="valid_name", price=10, category_id=1)
