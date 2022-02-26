from flask import flash, redirect, url_for, session
from functools import wraps

# Kullanıcı Giriş Decorator'ı
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "loggin_in" in session:
            return f(*args, **kwargs)
        else:
            flash("Lütfen giriş yapınız.", "danger")
            return redirect(url_for('login'))
    return decorated_function