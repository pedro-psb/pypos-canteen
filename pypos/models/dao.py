
from pypos.db import get_db


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
