"""Authentication and registration endpoints"""
from sqlite3 import Cursor
from typing import Dict, List, Optional

from flask import flash, redirect, render_template, request, session, url_for
from pydantic import ValidationError
from pypos.db import get_db
from pypos.models import dao
from pypos.models.dao_users import insert_user, insert_user_account
from pypos.models.forms.client_forms import LoginForm
from pypos.models.user_model import UserClient, UserOwner
from pypos.utils.data_utils import parse_errors

from . import bp


@bp.route("/register_client", methods=["POST"])
def register_client():
    if request.method == "POST":
        form_data = dict(request.form)
        # TODO put fixed roles in config file
        form_data["role_id"] = "4"  # client

        current_url = request.form.get("current_url")
        if not current_url:
            current_url = url_for("page.index")
        try:
            user = UserClient(**form_data)
            user_id = insert_user(user)
            insert_user_account(user_id)
            session.clear()
            return redirect(url_for("page.login"))
        except ValidationError as e:
            errors = parse_errors(e.errors(), UserClient)
            print(errors)
            return render_template("public/register_client.html", errors=errors)


@bp.route("/register_canteen", methods=["POST"])
def register_canteen():
    if request.method == "POST":
        form_data = dict(request.form)
        current_url = request.form.get("current_url")
        if not current_url:
            current_url = url_for("page.index")
        form_data["role_id"] = "1"  # owner

        try:
            user = UserOwner(**form_data)
            db = get_db()

            # create canteen
            db.execute("INSERT INTO canteen (name) VALUES (?)", (user.canteen_name,))

            # create user
            last_id_query = "SELECT last_insert_rowid();"
            canteen_id = db.execute(last_id_query).fetchone()[0]
            canteen_id = int(canteen_id)

            db.execute(
                """INSERT INTO user (username, email, password,\
                role_name, canteen_id) VALUES (?,?,?,?,?)""",
                (user.username, user.email, user.password, user.role_name, canteen_id),
            )
            db.commit()
            session.clear()
            return redirect(url_for("page.login"))
        except:
            error = "Some error with the database ocurred"

        flash(error)
        print("\n", error, "\n")
        return redirect(current_url)


@bp.route("/login", methods=["POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        try:
            user = LoginForm(username=username, password=password)
            user = dao.get_user_by_name(user.username)
            user_permissions = get_permissions_for_role(user["role_name"])
            # save session data
            session.clear()
            session["user_id"] = user["id"]
            session["permissions"] = user_permissions
            session["canteen_id"] = user["canteen_id"]
            session["canteen_name"] = user["canteen_name"]
            # redirect to the right place
            if "acess_client_dashboard" in session["permissions"]:
                return redirect(url_for("page.client_index"))
            return redirect(url_for("page.pos_main"))
        except ValidationError as e:
            # TODO fix typecheck error with BaseModel subclass parameter in `parse_errors`
            errors = parse_errors(e.errors(), LoginForm)
            print(errors)
            return render_template("public/login.html", errors=errors)


def get_permissions_for_role(role_name: str) -> List:
    """Get a list of `permissions` that belong to a `role_name`"""
    # TODO move to a better place
    db = get_db()
    user_permissions = db.execute(
        "SELECT p.slug FROM permission p INNER JOIN role_permission rp "
        "ON p.slug = rp.permission_slug WHERE rp.role_name=?;",
        [role_name],
    ).fetchall()
    user_permissions = [perm[0] for perm in user_permissions]
    return user_permissions


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("page.index"))
