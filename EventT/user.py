from flask import *

from EventT.db import get_db
from werkzeug.security import check_password_hash, generate_password_hash
from .auth import login_required

bp = Blueprint('user', __name__)


@bp.route("/")
def index():
    if g.user:
        return render_template("user/home.html")
    return render_template('user/guest.html')


@bp.route("/about us")
def about_us():
    return render_template("user/About us.html")


@bp.route("/contact us")
def contact():
    return render_template("user/Contact us.html")


@bp.route("/Event")
def event():
    db = get_db()
    events = db.execute(
        "SELECT * FROM Events Where OrganizerId = ?", (g.user['userid'],)
    ).fetchall()
    return render_template("user/Events.html", events=events)


@bp.route("/password", methods=["GET", "POST"])
@login_required
def change():
    if request.method == "POST":
        db = get_db()
        password = request.form['password']
        new = request.form['new']
        confirm = request.form['confirm']

        if check_password_hash(g.user['password'], password):
            if new == confirm:
                db.execute(
                    "Update user SET password = ? WHERE id = ?",
                    (generate_password_hash(new), g.user['id'])
                )
                db.commit()
                return redirect(url_for("user.index"))
            else:
                error = "Password and confirm must be the same"
        else:
            error = "Password is incorrect"
        flash(error)
        return render_template('auth/password.html')
    return render_template("auth/password.html")
