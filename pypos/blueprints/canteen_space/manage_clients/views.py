from flask import flash, redirect, render_template, request, session, url_for
from pydantic import ValidationError
from pypos.db import get_db
from pypos.models import PAYMENT_METHODS_NO_USER, transactions_dao
from pypos.models.transactions_dao import UserRecharge
from pypos.utils.data_util import parse_errors

from . import bp


@bp.route("/manage-client/user_recharge", methods=["POST"])
def add_user_recharge_from_pos():
    """Make Client Recharge from the manager's Manage Clients page"""
    try:
        form_data = dict(request.form)
        form_data["pending"] = False
        transaction = UserRecharge(**form_data)
        transaction.save()
        flash("Recharge was successfull", category="success")
        return redirect(url_for("page.manage_clients"))
    except ValidationError as e:
        errors = parse_errors(e.errors(), UserRecharge)
        print(errors)
        data = {
            "account_id": form_data["user_account_id"],
            "payment_methods": PAYMENT_METHODS_NO_USER,
        }
        return render_template(
            "user/management_clients_recharge.html", data=data, errors=errors
        )
