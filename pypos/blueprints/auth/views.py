import functools
from logging import raiseExceptions
import re

from flask import (
    flash, g, redirect, render_template, request, session, url_for
)
from pydantic import ValidationError
from werkzeug.security import check_password_hash, generate_password_hash
from pypos.db import get_db
from pypos.models.user_model import User
from . import bp
from .util import *


@bp.route('/register_client', methods=['POST'])
def register_client():
    if request.method == 'POST':
        # breakpoint()
        form_data = dict(request.form)
        # client TODO put fixed roles in config file
        form_data['role_id'] = '4'

        current_url = request.form.get('current_url')
        if not current_url:
            current_url = url_for('page.index')

        db = get_db()

        try:
            user = User(**form_data)
            db.execute(
                "INSERT INTO user (username, email, password,\
                    role_name, canteen_id) VALUES (?,?,?,?,?)",
                (user.username, user.email, user.password,
                 user.role_name, user.canteen_id))
            db.commit()
            session.clear()
            return redirect(url_for("page.login"))
        except ValidationError() as e:
            print(e)
            return redirect(current_url)


@bp.route('/register_canteen', methods=['POST'])
def register_canteen():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')
        canteen_name = request.form.get('canteen_name')
        current_url = request.form.get('current_url')
        role = 'owner'

        db = get_db()
        error = None

        # required fields
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif not email:
            error = 'Email is required'
        elif not canteen_name:
            error = 'Canteen needs a name'
        if not current_url:
            current_url = url_for('page.index')

        # validate email
        email_pattern = r"^([\w\.\-]+)@([\w\-]+)((\.(\w){2,3})+)$"
        pattern = re.compile(email_pattern)
        email_is_valid = re.match(pattern, email.strip())
        if not email_is_valid:
            error = "Email is not valid"

        # Password doesnt match
        if password != password_confirm:
            error = "Password doesn't match"

        # canteen doesn't exist/ is invalid
        check_canteen_query = "SELECT * FROM canteen WHERE name LIKE ?;"
        canteen_exist = db.execute(
            check_canteen_query, (canteen_name,)).fetchone()
        if canteen_exist:
            error = "Canteen Name already taken"

        # User already exist
        check_user_query = "SELECT * FROM user WHERE username=?;"
        user_exist = db.execute(
            check_user_query, (username,)).fetchone()
        if user_exist:
            error = "User already exist"

    if error is None:
        try:
            # create canteen
            db.execute(
                "INSERT INTO canteen (name) VALUES (?)", (canteen_name,))

            # create user
            last_id_query = "SELECT last_insert_rowid();"
            canteen_id = int(db.execute(last_id_query).fetchone()[0])
            db.execute(
                """INSERT INTO user (username, email, password,\
                role_name, canteen_id) VALUES (?,?,?,?,?)""",
                (username,
                 email,
                 generate_password_hash(password),
                 role,
                 canteen_id))
            db.commit()
            session.clear()
            return redirect(url_for("page.login"))
        except:
            error = f"Some error with the database ocurred"

    flash(error)
    print('\n', error, '\n')
    return redirect(current_url)


@bp.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        try:
            db = get_db()
            error = None

            # get user data from db
            query = '''SELECT u.username, u.id, u.email, u.phone_number, u.password,\
                u.phone_number, u.role_name, u.active, u.canteen_id, c.name as canteen_name\
                FROM user u INNER JOIN canteen c ON u.canteen_id = c.id\
                WHERE u.username=? AND u.active=1;'''
            user = db.execute(query, (username,)).fetchone()
            user = dict(user)
            # Check password
            if user is None:
                error = 'Incorrect username.'
                raiseExceptions()
            elif not check_password_hash(user['password'], password):
                error = 'Incorrect password.'
                raiseExceptions()

            # Check role and save permission to session
            role_name = user.get('role_name')
            if role_name:
                user_permissions = db.execute(
                    'SELECT p.slug FROM permission p INNER JOIN role_permission rp '
                    'ON p.slug = rp.permission_slug WHERE rp.role_name=?;',
                    (role_name,)).fetchall()
                user_permissions = [perm[0] for perm in user_permissions]

            # save session data
            session.clear()
            session['user_id'] = user['id']
            session['permissions'] = user_permissions
            session['canteen_id'] = user['canteen_id']
            session['canteen_name'] = user['canteen_name']

            # redirect to the right place
            if 'acess_client_dashboard' in session['permissions']:
                return redirect(url_for('page.client_index'))
            return redirect(url_for('page.canteen_index'))
        except:
            print(error)
            flash(error)
            return redirect(url_for('page.login'))


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('page.index'))
