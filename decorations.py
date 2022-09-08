from flask import g, render_template
import functools


def login_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if hasattr(g, 'user'):
            return f(*args, **kwargs)
        return render_template('404.html'), 404

    return decorated_function
