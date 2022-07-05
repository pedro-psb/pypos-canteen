from . import bp
from flask import redirect, request, session, url_for
from pypos.models.transactions_dao import UserRecharge


@bp.route('/add_user_recharge', methods=['POST'])
def add_user_recharge():
    try:
        form_data = dict(request.form)
        form_data['canteen_id'] = session['canteen_id']
        form_data['user_id'] = session['user_id']
        form_data['pending'] = True
        transaction = UserRecharge(**form_data)
        transaction.save()
    except Exception as e:
        print(e)
        return redirect(url_for('page.client_deposit'))
    return redirect(url_for('page.client_index'))