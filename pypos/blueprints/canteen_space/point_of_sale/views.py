from flask import request, session, url_for, redirect, flash
from pypos.db import get_db
from pypos.models import transactions_dao
from pypos.models.transactions_dao import RegularPurchase, UserAccountPurchase
from . import bp


@bp.route('/add_transaction_product', methods=['POST'])
def add_transaction_product():
    try:
        form_data = dict(request.form)
        form_data['canteen_id'] = session['canteen_id']
        if form_data.get('payment_method') != 'user_account':
            transaction = RegularPurchase(**form_data)
        else:
            transaction = UserAccountPurchase(**form_data)
        transaction.save()
    except Exception as e:
        return redirect(url_for('page.pos_main'))
    return redirect(url_for('page.pos_main'))


@bp.route('/accept_pending_recharge', methods=['POST'])
def accept_pending_recharge():
    transaction_id = request.form.get('transaction_id')
    transactions_dao.accept_pending_transaction(transaction_id)
    return redirect(url_for('page.pos_reports'))


@bp.route('/reject_pending_recharge', methods=['POST'])
def reject_pending_recharge():
    transaction_id = request.form.get('transaction_id')
    transactions_dao.reject_pending_transaction(transaction_id)
    return redirect(url_for('page.pos_reports'))


@bp.route('/remove_transaction_product', methods=['POST'])
def remove_transaction_product():
    '''Soft delete of transaction'''
    errors = None
    transaction_id = request.form.get('transaction_id')
    db = get_db()
    db.execute(
        'UPDATE generic_transaction SET active=0 WHERE id=?',
        (transaction_id))
    db.commit()
    flash(errors)
    return redirect(url_for('page.index'))
