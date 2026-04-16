from functools import wraps
from flask_login import current_user, logout_user
from flask import redirect,url_for

def admin_required(f):
    @wraps(f)
    def decorated_function (*args, **kwargs):

        if not current_user.is_authenticated:
            return redirect(url_for('login.login'))
        if not current_user.is_admin:
            logout_user()
            return redirect(url_for('login.login'))
        return f(*args, **kwargs)

    return decorated_function
