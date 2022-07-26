from pypos.db import get_db


class ReportSummary:
    """Generate summary report out of transaction data"""
    # TODO refactor: load all items total and compute logic in memory rather than in SQL
    @classmethod
    def get_full_summary(cls):
        most_sales = cls.get_most_sales()
        less_sales = cls.get_less_sales()
        higher_invoice = cls.get_higher_invoice()
        lower_invoice = cls.get_lower_invoice()
        full_summary = {
            'most_sales': {
                'product': most_sales['product'],
                'share': most_sales['share'],
            },
            'less_sales': {
                'product': less_sales['product'],
                'share': less_sales['share'],
            },
            'higher_invoice': {
                'product': higher_invoice['product'],
                'share': higher_invoice['share'],
            },
            'lower_invoice': {
                'product': lower_invoice['product'],
                'share': lower_invoice['share'],
            },
        }
        return full_summary

    @classmethod
    def get_most_sales(cls):
        """Get the most sold not null sold product and share on percentage"""
        db = get_db()
        total_sold = db.execute(
            """SELECT SUM(quantity) FROM transaction_product_item;"""
        ).fetchone()
        most_sold = db.execute(
            """SELECT p.name AS product, SUM(tpi.quantity) AS products_sold FROM product p
            INNER JOIN transaction_product_item tpi
            ON p.id=tpi.product_id GROUP BY p.id ORDER BY products_sold DESC;
            """).fetchall()
        if not total_sold or not most_sold:
            return {
                'product': None,
                'share': 0.00
            }
        total_sold = total_sold[0]
        most_sold = most_sold[0]
        share_percentage = most_sold['products_sold'] / total_sold * 100
        result = {
            'product': most_sold['product'],
            'share': round(share_percentage, 2)
        }
        return result

    @classmethod
    def get_less_sales(cls):
        """Get the most least not null sold product"""
        db = get_db()
        less_sold = db.execute(
            """SELECT p.name AS product, SUM(tpi.quantity) AS products_sold FROM product p
            INNER JOIN transaction_product_item tpi
            ON p.id=tpi.product_id GROUP BY p.id ORDER BY products_sold ASC;
            """).fetchall()
        total_sold = db.execute(
            """SELECT SUM(quantity) FROM transaction_product_item;"""
        ).fetchone()
        if not total_sold or not less_sold:
            return {
                'product': None,
                'share': 0.00
            }
        less_sold = less_sold[0]
        total_sold = total_sold[0]
        share_percentage = less_sold['products_sold'] / total_sold * 100
        result = {
            'product': less_sold['product'],
            'share': round(share_percentage, 2)
        }
        return result

    @classmethod
    def get_higher_invoice(cls):
        """Get the most rentable product and it's percentage share"""
        db = get_db()
        most_rentable = db.execute(
            """SELECT p.name AS product, SUM(tpi.sub_total) AS sub_total_value FROM product p
            INNER JOIN transaction_product_item tpi
            ON p.id=tpi.product_id GROUP BY p.id ORDER BY sub_total_value DESC;
            """).fetchall()
        total_value = db.execute(
            """SELECT SUM(sub_total) FROM transaction_product_item;"""
        ).fetchone()
        if not total_value or not most_rentable:
            return {
                'product': None,
                'share': 0.00
            }
        most_rentable = most_rentable[0]
        total_value = total_value[0]
        share_percentage = most_rentable['sub_total_value'] / total_value * 100
        result = {
            'product': most_rentable['product'],
            'share': round(share_percentage, 2)
        }
        return result

    @classmethod
    def get_lower_invoice(cls):
        """Get the less rentable product and it's percentage share"""
        db = get_db()
        less_rentable = db.execute(
            """SELECT p.name AS product, SUM(tpi.sub_total) AS sub_total_value FROM product p
            INNER JOIN transaction_product_item tpi
            ON p.id=tpi.product_id GROUP BY p.id ORDER BY sub_total_value ASC;
            """).fetchall()
        total_value = db.execute(
            """SELECT SUM(sub_total) FROM transaction_product_item;"""
        ).fetchone()
        if not total_value or not less_rentable:
            return {
                'product': None,
                'share': 0.00
            }
        less_rentable = less_rentable[0]
        total_value = total_value[0]
        share_percentage = less_rentable['sub_total_value'] / total_value * 100
        result = {
            'product': less_rentable['product'],
            'share': round(share_percentage, 2)
        }
        return result
