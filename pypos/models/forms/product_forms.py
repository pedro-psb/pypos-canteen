from typing import Dict, Optional

from pydantic import BaseModel, PrivateAttr, root_validator, validator
from pypos.models import dao_products


class AddProductForm(BaseModel):
    name: str
    price: float
    category_id: int

    @validator("name", "price")
    def not_empty_field(cls, value):
        if not value:
            raise ValueError("Enter a valid value")
        return value

    @validator("price")
    def positive_value(cls, value):
        if value < 0:
            raise ValueError("Price must be positive")
        return value

    @validator("category_id")
    def category_exist(cls, value):
        if value:
            category_exist = dao_products.get_category_by_id(value)
            if not category_exist:
                raise ValueError("Sorry, for some reason this category doesn't exist")
        return value

    @validator("name")
    def name_already_taken(cls, value):
        product_exist = dao_products.get_product_by_name(value)
        if product_exist:
            raise ValueError("Product should have a unique name")
        return value

    class Config:
        anystr_strip_whitespace = True


class UpdateProductForm(AddProductForm):
    product_id: int
    _product_data: Dict = PrivateAttr()
    name: str

    @root_validator
    def product_id_exist(cls, values):
        product_data = dao_products.get_product_by_id(values["product_id"])
        if not product_data:
            raise ValueError("Product id is invalid")
        values["_product_data"] = product_data
        return values

    @validator("name")
    def name_already_taken(cls, value):
        return value

    @root_validator
    def name_except_original(cls, values):
        """Overrides name_already_taken() validator to accept update with same name as before"""
        product_exist = dao_products.get_product_by_name(values["name"])
        original_name = values["_product_data"]["name"]
        if product_exist:
            if product_exist["name"] != original_name:
                raise ValueError("Product should have a unique name")
        return values
