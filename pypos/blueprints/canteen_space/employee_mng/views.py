from pydantic import ValidationError
from flask import request, session, url_for, redirect
from pypos.db import get_db
from . import bp
from pypos.models.user_model import User, UserUpdate
from pypos.models.dao_users import insert_user


@bp.route('/insert_employee', methods=['POST'])
def add():
    # TODO validation: check if email is not already taken
    
    form_data = dict(request.form)
    try:
        employee = User(**form_data)
        insert_user(employee)
    except ValidationError as e:
        print(e)
        return redirect(url_for('page.manage_employees_add'))
    return redirect(url_for('page.manage_employees'))


@bp.route('/update_employee', methods=['POST'])
def update():
    form_data = dict(request.form)
    try:
        # create and validate employee data
        employee = UserUpdate(
            canteen_id=session['canteen_id'],
            id=form_data.get('id'),
            role_id=form_data.get('role_id')
        )

        # add to database
        db = get_db()
        query = "UPDATE user SET role_name=? WHERE id=?;"
        db.execute(query, (employee.role_name, employee.id,))
        db.commit()
    except ValidationError as e:
        print(e)
        return redirect(url_for('page.manage_employees_update', id=form_data['id']))
    return redirect(url_for('page.manage_employees'))


@bp.route('/delete_employee', methods=['POST'])
def delete():
    db = get_db()
    form_id = request.form.get('id')
    try:
        query = "UPDATE user SET active=0 WHERE id=?;"
        db.execute(query, (form_id,))
        db.commit()
    except Exception("Some error ocurred with the database"):
        print('error deleting user')
    return redirect(url_for('page.manage_employees'))


def update_role_by_id(id):
    pass


def soft_delete_by_id(id):
    pass

