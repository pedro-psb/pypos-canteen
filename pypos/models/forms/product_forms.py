from pydantic import BaseModel, PrivateAttr, validator
from pypos.models import dao_products


class AddProductForm(BaseModel):
    name: str
    price: float
    category_id: int

    @validator("name", "price", "category_id")
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
