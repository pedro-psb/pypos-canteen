import re
from typing import Optional
from pydantic import BaseModel, ConstrainedStr, ValidationError, validator
from flask import request, session, url_for, redirect
from pypos.db import get_db
from . import bp
from .models import Employee


@bp.route('/insert_employee', methods=['POST'])
def add():
    form_data = dict(request.form)
    form_data['canteen_id'] = session.get('canteen_id')
    try:
        employee = Employee(**form_data)
        insert_employee(employee)
        print(employee)
    except ValidationError as e:
        print(e)
        return redirect(url_for('page.manage_employees_add'))
    return redirect(url_for('page.manage_employees'))


@bp.route('/update_employee', methods=['POST'])
def update():
    form_data = dict(request.form)
    form_data['canteen_id'] = session['canteen_id']
    try:
        employee = Employee(**form_data)
        db = get_db()
        query = "UPDATE user SET role_name=? WHERE id=?;"
        db.execute(query, (employee.role_name, employee.id,))
    except ValidationError as e:
        print(e)
        return redirect(url_for('page.manage_employees_update', id=form_data['id']))
    return redirect(url_for('page.manage_employees'))


@bp.route('/delete_employee', methods=['POST'])
def delete():
    return redirect(url_for('page.manage_employees'))


def insert_employee(employee):
    db = get_db()
    query = """INSERT INTO user(username, email, password,\
            phone_number, role_name, canteen_id) VALUES(?,?,?,?,?,?);"""
    db.execute(query, (
        employee.name,
        employee.email,
        employee.password,
        employee.phone_number,
        employee.role_name,
        employee.canteen_id
    ))


def update_role_by_id(id):
    pass


def soft_delete_by_id(id):
    pass
