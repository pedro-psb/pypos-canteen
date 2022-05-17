from .errors import *

class Product:
    def __init__(self, name, price, category, id=None):
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
        '''
        I don't know if it is best to catch the error in the DB or before sending the query.
        The example in the Flask Tutorial catches the error in the DB with the IntegrityError exception,
        but catching it early can save a query.
        '''
        try:
            self.category = int(self.category)
        except ValueError:
            return ADD_PRODUCT_INVALID_CATEGORY_ERROR
        else:
            if self.category <= 0:
                return ADD_PRODUCT_INVALID_CATEGORY_ERROR
