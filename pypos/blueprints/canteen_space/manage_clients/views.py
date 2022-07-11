from flask import request, session, url_for, redirect, flash
from pypos.db import get_db
from pypos.models import transactions_dao
from pypos.models.transactions_dao import UserRecharge
from . import bp

@bp.route('/manage-client/user_recharge', methods=['POST'])
def add_user_recharge_from_pos():
    """Make Client Recharge from the manager's Manage Clients page"""
    try:
        form_data = dict(request.form)
        form_data['canteen_id'] = session['canteen_id']
        form_data['pending'] = False
        transaction = UserRecharge(**form_data)
        transaction.save()
    except Exception as e:
        print(e)
        return redirect(url_for('page.manage_clients_recharge', account_id=form_data['user_account_id']))
    return redirect(url_for('page.manage_clients'))
