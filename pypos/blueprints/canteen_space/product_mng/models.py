from datetime import date
from unicodedata import name
from .errors import *


class ProductCategory:
    def __init__(self, name, id=None) -> None:
        self.id = id
        self.name = name

    def __str__(self) -> str:
        return self.name


class Product:
    def __init__(self, name, price, category=None, id=None):
        self.id = id
        self.name = name
        self.price = price
        self.category = category

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
            self.category = int(self.category)
        except ValueError:
            return ADD_PRODUCT_INVALID_CATEGORY_ERROR
        else:
            if self.category <= 0:
                return ADD_PRODUCT_INVALID_CATEGORY_ERROR

    def __str__(self) -> str:
        return self.name
