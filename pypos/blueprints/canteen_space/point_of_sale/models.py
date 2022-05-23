from datetime import datetime


class TransactionProduct:    
    def __init__(self, products) -> None:
        self.date = datetime.now()
        self.products = products
        self.total_value = 0

    
    def validate(self):
        '''Check if products is a list of valid product id integers'''
        return True

    def __str__(self) -> str:
        return f"{self.date}: {self.total_value}"
