from flask import request, url_for, redirect, flash
from pypos.db import get_db
from . import bp
from .models import TransactionProduct


@bp.route('/add_transaction_product', methods=['POST'])
def add_transaction_product():
    transaction_product = TransactionProduct(
        request.form.get('products'),
        request.form.get('discount'),
        request.form.get('payment_method')
    )
    # Create transaction
    db = get_db()
    errors = transaction_product.validate(db)
    if not errors:
        db.execute(
            'INSERT INTO transaction_product'
            '(date, total_value, discount, payment_method) VALUES (?,?,?,?);',
            (transaction_product.date,
             transaction_product.total_value,
             transaction_product.discount,
             transaction_product.payment_method
             ))
        # Get the id of the inserted transaction
        transaction_id = db.execute(
            "SELECT last_insert_rowid() as id;").fetchone()
        transaction_id = int(transaction_id['id'])

        # Create transaction items for each product
        for product in transaction_product.products:
            product_id = product['id']
            quantity = int(product['quantity'])
            db.execute(
                'INSERT INTO transaction_product_item'
                '(product_id, quantity, transaction_product_id) VALUES (?,?,?);',
                (product_id, quantity, transaction_id))

        flash("Sucefully added transaction")
    else:
        flash(errors)
    return redirect(url_for('page.index'))


@bp.route('/remove_transaction_product', methods=['POST'])
def remove_transaction_product():
    '''Soft delete of transaction'''
    errors = None
    transaction_id = request.form.get('transaction_id')
    db = get_db()
    db.execute(
        'UPDATE transaction_product SET active=0 WHERE id=?',
        (transaction_id))

    flash(errors)
    return redirect(url_for('page.index'))
