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


@bp.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')

        db = get_db()
        error = None

        # required fields
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif not email:
            error = 'Email is required'

        # validate email
        email_pattern = r"^([\w\.\-]+)@([\w\-]+)((\.(\w){2,3})+)$"
        pattern = re.compile(email_pattern)
        email_is_valid = re.match(pattern, email.strip())
        if not email_is_valid:
            error = "Email is not valid"

        # Password doesnt match
        if password != password_confirm:
            error = "Password doesn't match"

        # User already exist
        check_user_query = "SELECT * FROM user WHERE username=?;"
        user_exist = db.execute(check_user_query, (username,)).fetchone()
        if user_exist:
            print(username, dict(user_exist))
            error = "User already exist"

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, email, password, role_name) VALUES (?,?,?,?)",
                    (username, email, generate_password_hash(password), 'generic'))
                db.commit()
                session.clear()
                return redirect(url_for("page.login"))
            except:
                error = f"Some error with the database ocurred"

        flash(error)
        print('\n', error, '\n')
        return redirect(url_for('page.register'))


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
                'SELECT * FROM user WHERE username = ?', (username,)
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

            # redirect to the right place
            if 'initial_acess' in session['permissions']:
                return redirect(url_for('page.create_or_join_canteen'))
            elif 'acess_client_dashboard' in session['permissions']:
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
