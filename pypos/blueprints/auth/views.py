import functools

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
        username = request.form['username']
        password = request.form['password']
        role_name = request.form['role_name']

        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        # Check if role is valid
        valid_roles = db.execute('SELECT name FROM role;').fetchall()
        valid_roles = [dict(role)['name'] for role in valid_roles]
        if role_name not in valid_roles:
            error = 'Role is not valid'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password, role_name) VALUES (?,?,?)",
                    (username,
                    generate_password_hash(password),
                    role_name),
                )
                db.commit()
            except:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)
        return redirect(url_for('page.index'))


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()
        role_name = user['role_name']

        user_permissions = db.execute(
            'SELECT * FROM role_permission rp INNER JOIN permission p ON rp.permission_slug = p.slug WHERE rp.role_name = ?',
            (role_name,)).fetchall()
        user_permissions = [perm['permission_slug'] for perm in user_permissions]

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'
        elif not user_permissions:
            error = 'Invalid role'
        
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            session['permissions'] = user_permissions
            return redirect(url_for('page.index'))

        flash(error)

    return render_template('auth/login.html')


@bp.route('/logout')
@login_required(permissions=['bar'])
def logout():
    session.clear()
    return redirect(url_for('page.index'))
