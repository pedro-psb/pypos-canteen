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
                return redirect(url_for('page.login'))
            
            if permissions and not isinstance(permissions, list):
                raise Exception("'permissions' must be a list in @login_required(permissions)")

            user_permissions = session['permissions']
            for required_perm in permissions:
                if required_perm not in user_permissions:
                    return redirect(url_for('page.unauthorized'))
            return view(*args, **kwargs)
        return wrapped_view
    return decorator

def public_acess_only(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user:
            return redirect(url_for('page.index'))
        return view(**kwargs)
    return wrapped_view