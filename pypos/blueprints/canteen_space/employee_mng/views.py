from flask import redirect, render_template, request, session, url_for
from pydantic import ValidationError
from pypos.db import get_db
from pypos.models import dao, dao_acess_control
from pypos.models.dao_users import insert_user
from pypos.models.user_model import User, UserUpdate
from pypos.utils.data_utils import parse_errors

from . import bp


@bp.route("/insert_employee", methods=["POST"])
def add():
    # TODO validation: check if email is not already taken

    form_data = dict(request.form)
    try:
        employee = User(**form_data)
        insert_user(employee)
    except ValidationError as e:
        errors = parse_errors(e.errors(), User)
        data = {"roles": dao_acess_control.get_all_roles()}
        print(errors)
        return render_template(
            "user/management_employees_add.html", data=data, errors=errors
        )
    return redirect(url_for("page.manage_employees"))


@bp.route("/update_employee", methods=["POST"])
def update():
    form_data = dict(request.form)
    try:
        # create and validate employee data
        employee = UserUpdate(
            canteen_id=session["canteen_id"],
            id=form_data.get("id"),
            role_id=form_data.get("role_id"),
        )  # type: ignore

        # add to database
        db = get_db()
        query = "UPDATE user SET role_name=? WHERE id=?;"
        db.execute(
            query,
            (
                employee.role_name,
                employee.id,
            ),
        )
        db.commit()
    except ValidationError as e:
        print(e)
        return redirect(url_for("page.manage_employees_update", id=form_data["id"]))
    return redirect(url_for("page.manage_employees"))


@bp.route("/delete_employee", methods=["POST"])
def delete():
    db = get_db()
    form_id = request.form.get("id")
    try:
        query = "UPDATE user SET active=0 WHERE id=?;"
        db.execute(query, (form_id,))
        db.commit()
    except Exception("Some error ocurred with the database"):
        print("error deleting user")
    return redirect(url_for("page.manage_employees"))


def update_role_by_id(id):
    pass


def soft_delete_by_id(id):
    pass
