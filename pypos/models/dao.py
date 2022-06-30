
from pypos.db import get_db
from pypos.models.transactions_dao import RegularPurchase


def get_user_balance_by_id(id):
    conn = get_db()
    db = conn.cursor()
    query = "SELECT balance FROM user_account WHERE user_id=?;"
    user_balance = db.execute(query, (id,)).fetchone()[0]
    return user_balance

def get_canteen_balance_by_id(id, cash_or_bank='cash_balance'):
    conn = get_db()
    db = conn.cursor()
    query = f"SELECT {cash_or_bank} FROM canteen_account WHERE canteen_id=?;"
    canteen_balance = db.execute(query, (id,)).fetchone()[0]
    return canteen_balance

def get_generic_transaction_by_id(transaction_id):
        db = get_db()
        transaction_query = """SELECT gt.date_time, gt.total, gt.canteen_id,
        pay.discount, pay.payment_method FROM generic_transaction gt
        INNER JOIN payment_info pay ON gt.id = pay.generic_transaction_id
        WHERE gt.id=? AND gt.active=1;"""
        products_query = """SELECT p.canteen_id, p.id, p.name, p.price, tpi.quantity, 
        tpi.sub_total FROM product p INNER JOIN transaction_product_item tpi 
        ON p.id = tpi.product_id WHERE tpi.generic_transaction_id=? AND p.active=1;"""

        transaction = dict(db.execute(transaction_query,
                           (transaction_id,)).fetchone())
        products = db.execute(products_query, (transaction_id,)).fetchall()
        products = [dict(p) for p in products]
        transaction['products'] = products
        transaction = RegularPurchase(**transaction)
        return transaction
    
def get_all_client_transactions(client_id):
    # get account_id
    # query purchases and recharges
    # transform each row in a ClientPurchase or ClientRecharge
    pass