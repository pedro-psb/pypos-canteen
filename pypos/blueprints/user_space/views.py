from pypos.models import dao
from pypos.models.user_model import UserChildUpdateForm
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


@bp.route('/user_child_insert', methods=['POST'])
def user_child_insert():
    form_data = dict(request.form)
    user_data = dao.get_user_by_id(form_data['id'])
    if not form_data['password']:
        form_data['password'] = user_data['password']
    user_data.update(form_data)
    user_data = UserChildUpdateForm(**user_data)
    dao.update_user_child(user_data)
    return redirect(url_for('page.client_manage'))


@bp.route('/user_child_update', methods=['POST'])
def user_child_update():
    pass


@bp.route('/user_child_remove', methods=['POST'])
def user_child_remove():
    pass
