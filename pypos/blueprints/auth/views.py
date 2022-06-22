import functools
from logging import raiseExceptions
import re

from flask import (
    flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from pypos.db import get_db
from . import bp
from .util import *


@bp.route('/register_client', methods=['POST'])
def register_client():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')
        canteen_id = request.form.get('canteen_id')
        current_url = request.form.get('current_url')
        role = 'client'

        db = get_db()
        error = None

        # required fields
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif not email:
            error = 'Email is required'
        elif not canteen_id:
            error = 'Needs to be related to an existing canteen'
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
        check_canteen_query = "SELECT * FROM canteen WHERE id=?;"
        canteen_exist = db.execute(
            check_canteen_query, (canteen_id,)).fetchone()
        if not canteen_exist:
            error = "Canteen don't exist"

        # User already exist
        check_user_query = "SELECT * FROM user WHERE username=? AND canteen_id=?;"
        user_exist = db.execute(
            check_user_query, (username, canteen_id)).fetchone()
        if user_exist:
            error = "User already exist"

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, email, password, role_name, canteen_id) VALUES (?,?,?,?,?)",
                    (username,
                     email,
                     generate_password_hash(password),
                     role,
                     canteen_id))
                db.commit()
                session.clear()
                return redirect(url_for("page.login"))
            except Exception():
                error = f"Some error with the database ocurred"

        flash(error)
        print('\n', error, '\n')
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
                "INSERT INTO user (username, email, password, role_name, canteen_id) VALUES (?,?,?,?,?)",
                (username,
                 email,
                 generate_password_hash(password),
                 role,
                 canteen_id))
            db.commit()
            session.clear()
            return redirect(url_for("page.login"))
        except Exception():
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
            user = db.execute(
                'SELECT * FROM user WHERE username=?;', (username,)
            ).fetchone()
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

            # redirect to the right place
            if 'acess_client_dashboard' in session['permissions']:
                return redirect(url_for('page.client_index'))
            return redirect(url_for('page.canteen_index'))
        except Exception():
            print(error)
            flash(error)
            return redirect(url_for('page.login'))


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('page.index'))
