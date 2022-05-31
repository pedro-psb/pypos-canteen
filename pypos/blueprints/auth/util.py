import functools
from flask import g, session, redirect, url_for
from pypos.db import get_db
from . import bp

# TODO - understand this code
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


def login_required(permissions=None):
    def decorator(view):
        @functools.wraps(view)
        def wrapped_view(*args,**kwargs):
            if g.user is None:
                return redirect(url_for('auth.login'))
            user_permissions = session['permissions']
            # breakpoint()
            for required_perm in permissions:
                if required_perm not in user_permissions:
                    return redirect(url_for('auth.login'))
            return view(*args, **kwargs)
        return wrapped_view
    return decorator