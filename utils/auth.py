from functools import wraps
from flask import session, redirect, url_for

# ⚙️ Identifiants en dur
VALID_CREDENTIALS = {
    "admin": "151015"
}

def check_credentials(username, password):
    return VALID_CREDENTIALS.get(username) == password

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function
