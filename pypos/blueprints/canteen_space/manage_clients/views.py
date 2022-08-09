from flask import flash, redirect, request, session, url_for
from pydantic import ValidationError
from pypos.db import get_db
from pypos.models import transactions_dao
from pypos.models.transactions_dao import UserRecharge
from pypos.utils.data_util import parse_errors

from . import bp


@bp.route("/manage-client/user_recharge", methods=["POST"])
def add_user_recharge_from_pos():
    """Make Client Recharge from the manager's Manage Clients page"""
    try:
        form_data = dict(request.form)
        form_data["canteen_id"] = session["canteen_id"]
        form_data["pending"] = False
        transaction = UserRecharge(**form_data)
        transaction.save()
        return redirect(url_for("page.manage_clients"))
    except ValidationError as e:
        errors = parse_errors(e.errors(), UserRecharge)
        return redirect(
            url_for(
                "page.manage_clients_recharge",
                account_id=form_data["user_account_id"],
                errors=errors,
            )
        )
