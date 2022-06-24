from datetime import datetime
from .errors import *
import json

class TransactionProduct:    
    def __init__(self, products, discount, payment_method) -> None:
        self.date = datetime.now()
        self.products = json.loads(products)
        self.discount = float(discount)
        self.payment_method = int(payment_method)
        self.total_value = 0
    
    def validate(self, db):
        '''Check if products is a list of valid product id integers'''
        # TODO refactor error handling. Quantity check should be here
        try:
            # check data correctness
            for product in self.products:
                product_quantity = product['quantity']
                product_id = product['id']
            # check product id is in database
            errors = self.sum_total(db)
        except:
            errors = POS_INVALID_TRANSACTION_REQUEST_ERROR
        return errors

    def sum_total(self, db):
        errors = None
        total_sum = 0
        for product in self.products:
            # check if quantity is integer
            try:
                product_quantity = int(product['quantity'])
            except:
                errors = POS_INVALID_PRODUCT_QUANTITY_VALUE_ERROR
                break

            # check if product id is valid
            product_price = db.execute(
                'SELECT price FROM product WHERE id=?;',
                (product['id'],)).fetchone()
            if not product_price:
                errors = POS_INVALID_PRODUCT_ID_ERROR
                break
            
            # sum if everything is ok
            total_sum += product_price[0] * product_quantity
        if not errors:
            self.total_value = total_sum - self.discount
            return None
        return errors
    
    def __repr__(self):
        return "date: {}\npayment: {}\ndiscount: {}\ntotal: {}\nproducts: {}".format(
            self.date, self.payment_method, self.discount, self.total_value, self.products
        )
    
    def __str__(self) -> str:
        return f"{self.date}: {self.total_value}"

