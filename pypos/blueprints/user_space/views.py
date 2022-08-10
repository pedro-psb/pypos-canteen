from multiprocessing.sharedctypes import Value

from flask import flash, redirect, render_template, request, session, url_for
from pydantic import ValidationError
from pypos.blueprints.frontend.views import PAYMENT_METHODS_NO_USER
from pypos.models import dao, dao_users
from pypos.models.transactions_dao import UserRecharge
from pypos.models.user_model import UserChildCreateForm, UserChildUpdateForm
from pypos.utils.data_utils import parse_errors

from . import bp


@bp.route("/add_user_recharge", methods=["POST"])
def add_user_recharge():
    try:
        form_data = dict(request.form)
        form_data["canteen_id"] = session["canteen_id"]
        form_data["user_id"] = session["user_id"]
        form_data["pending"] = True
        transaction = UserRecharge(**form_data)
        transaction.save()
        flash("Added deposit request successfully", category="success")
        return redirect(url_for("page.client_index"))
    except ValidationError as e:
        errors = parse_errors(e.errors(), UserRecharge)
        print(e)
        data = {"payment_methods": PAYMENT_METHODS_NO_USER}
        return render_template("user/client_deposit.html", data=data, errors=errors)


@bp.route("/user_child_insert", methods=["POST"])
def user_child_insert():
    try:
        form_data = dict(request.form)
        form_data = remove_empty_fields(form_data)
        form_data["canteen_id"] = session["canteen_id"]
        form_data["user_provider_id"] = session["user_id"]

        user_data = UserChildCreateForm(**form_data)
        dao_users.create_user_child(user_data)
        flash("Created dependent user successfully", category="success")
        return redirect(url_for("page.client_manage"))
    except ValidationError as e:
        errors = parse_errors(e.errors(), UserChildCreateForm)
        print(errors)
        return render_template("user/client_manage_add.html", errors=errors)


def remove_empty_fields(form_data: dict):
    new_form = {}
    for k, v in form_data.items():
        if v:
            new_form[k] = v
    return new_form


@bp.route("/user_child_update", methods=["POST"])
def user_child_update():
    form_data = dict(request.form)
    try:
        user = UserChildUpdateForm(**form_data)
        dao_users.update_user_child(user)
        flash("User Dependent updated successfully", category="success")
        return redirect(url_for("page.client_manage"))
    except ValidationError as e:
        errors = parse_errors(e.errors(), UserChildUpdateForm)
        data = {"user_child": dao.get_user_by_id(form_data["id"])}
        print(errors)
        return render_template(
            "user/client_manage_update.html", data=data, errors=errors
        )


@bp.route("/user_child_remove", methods=["POST"])
def user_child_remove():
    try:
        form_data = request.form
        dao_users.delete_user(form_data["id"])
    except Exception as e:
        print(e)
    return redirect(url_for("page.client_manage"))
