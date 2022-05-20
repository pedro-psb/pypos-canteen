class TransactionProduct:
    def __init__(self, date, total_value, products) -> None:
        self.date = date
        self.total_value = total_value
        self.products = products

    def __str__(self) -> str:
        return f"{self.date}: {self.total_value}"