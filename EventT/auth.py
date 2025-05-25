import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from EventT.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/signup', methods=('GET', 'POST'))
def signup():
    if request.method == 'POST':
        fullname = request.form['username']
        email = request.form['email']
        password = request.form['password']
        phoneNo = request.form['phone no']
        db = get_db()
        error = None

        if not email:
            error = 'Email is required.'
        elif not password:
            error = 'Password is required.'
        elif not password or not fullname:
            error = 'Field is required'
        if error is None:
            try:
                db.execute(
                    "INSERT INTO Users (Email, PasswordHash, FullName, PhoneNumber) VALUES (?, ?, ?, ?)",
                    (email, generate_password_hash(password), fullname, phoneNo),
                )
                db.commit()
            except db.IntegrityError:
                error = "Account is already registered."
            else:
                return redirect(url_for("auth.login"))
        flash(error)
    return render_template('auth/signup.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM Users WHERE Email = ?', (email,)
        ).fetchone()

        if user is None:
            error = 'Incorrect Email.'
        elif not check_password_hash(user['PasswordHash'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['userid']
            return redirect(url_for('user.index'))

        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM Users WHERE userid = ?', (user_id,)
        ).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('user.index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
