from datetime import date
from typing import Optional

from pydantic import BaseModel, PrivateAttr, ValidationError, validator
from pypos.db import get_db
from pypos.models import dao_products

from .errors import *


class ProductCategory(BaseModel):
    name: str
    description: Optional[str] = ""
    # TODO find out how to not show private att on the IDE hints
    _id: str = PrivateAttr()

    @validator("name")
    def unique_name(cls, value):
        db = get_db()
        category = db.execute(
            "SELECT * FROM product_category WHERE name=?", [value]
        ).fetchall()
        if category:
            raise ValueError("Category name already taken")
        return value

    class Config:
        anystr_strip_whitespace = True


class Product:
    def __init__(self, name, price, category=None, id=None):
        self.id = id
        self.name = name
        self.price = price
        self.category_id = category

    def validate(self):
        # Name
        if not self.name:
            return ADD_PRODUCT_NOT_EMPTY_NAME_ERROR

        # Price
        if not self.price:
            return ADD_PRODUCT_NOT_EMPTY_PRICE_ERROR
        try:
            self.price = float(self.price)
        except:
            return ADD_PRODUCT_INVALID_PRICE_ERROR
        else:
            if self.price < 0:
                return ADD_PRODUCT_NOT_POSTIIVE_REAL_ERROR

        # Category
        try:
            if self.category_id != "None":
                self.category_id = int(self.category_id)
                if self.category_id <= 0:
                    return ADD_PRODUCT_INVALID_CATEGORY_ERROR
        except ValueError:
            return ADD_PRODUCT_INVALID_CATEGORY_ERROR

    def __str__(self) -> str:
        return self.name
