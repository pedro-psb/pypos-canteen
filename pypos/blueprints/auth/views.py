"""Authentication and registration endpoints"""
from typing import Optional

from flask import flash, redirect, request, session, url_for
from pydantic import BaseModel, Field, ValidationError, validator
from pypos.db import get_db
from pypos.models import dao
from pypos.models.dao_users import insert_user
from pypos.models.user_model import UserClient, UserOwner
from werkzeug.security import check_password_hash, generate_password_hash

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
            insert_user(user)
            session.clear()
            return redirect(url_for("page.login"))
        except ValidationError as e:
            print(e)
            return redirect(current_url)


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
            db = get_db()
            error = None

            # get user data from db
            query = """SELECT u.username, u.id, u.email, u.phone_number, u.password,\
                u.phone_number, u.role_name, u.active, u.canteen_id, c.name as canteen_name\
                FROM user u INNER JOIN canteen c ON u.canteen_id = c.id\
                WHERE u.username=? AND u.active=1;"""
            user = db.execute(query, (username,)).fetchone()
            user = dict(user)
            # Check password
            if user is None:
                error = "Incorrect username."
                raise Exception()
            elif not check_password_hash(user["password"], password):
                error = "Incorrect password."
                raise Exception()

            # Check role and save permission to session
            role_name = user.get("role_name")
            if role_name:
                user_permissions = db.execute(
                    "SELECT p.slug FROM permission p INNER JOIN role_permission rp "
                    "ON p.slug = rp.permission_slug WHERE rp.role_name=?;",
                    (role_name,),
                ).fetchall()
                user_permissions = [perm[0] for perm in user_permissions]

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
        except:
            return redirect(url_for("page.login"))


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("page.index"))
