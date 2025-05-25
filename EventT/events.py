from flask import *
from EventT.db import get_db
from .auth import login_required

bp = Blueprint('event', __name__, url_prefix="/event")


@bp.route("/create", methods=('GET', 'POST'))
@login_required
def create():
	if request.method == "POST":
		event_name = request.form["EventName"]
		description = request.form["Description"]
		Start = request.form["Start_date"]
		End = request.form["End_date"]
		Location = request.form["LocationName"]
		db = get_db()
		error = None
		if not event_name or not description or not Start or not End or not Location:
			error = "field required"
		if error is None:
			try:
				db.execute(
					"INSERT INTO Events (EventName, Description, Start_date, End_date, LocationName, OrganizerId, "
					"Status) VALUES (?, ?, ?, ?, ?, ?, ?)",
					(event_name, description, Start, End, Location, g.user['userid'], "Scheduled"),
				)
				db.commit()
			except:
				error = "Problem creating event"
			else:
				return redirect(url_for("user.event"))
		flash(error)
	return render_template("Events/add.html")


@bp.route("/update/<int:id>", methods=('GET', 'POST'))
@login_required
def update(id):
	db = get_db()
	value = db.execute(
		"SELECT * FROM Events WHERE EventId = ?", (id,)
	).fetchone()
	if request.method == "POST":
		event_name = request.form["EventName"]
		description = request.form["Description"]
		Start = request.form["Start_date"]
		End = request.form["End_date"]
		Location = request.form["LocationName"]
		Status = request.form["Status"]
		db = get_db()
		error = None
		if not event_name or not description or not Start or not End or not Location:
			error = "field required"
		if error is None:
			try:
				db.execute(
					"UPDATE Events SET EventName = ?, Description = ?, Start_date = ?, End_date = ?, LocationName = ?, "
					"Status = ? WHERE OrganizerId = ?",
					(event_name, description, Start, End, Location, Status, g.user['userid']),
				)
				db.commit()
			except:
				error = "Problem creating event"
			else:
				return redirect(url_for("user.event"))
		flash(error)
	return render_template("Events/Update.html", value=value)


@bp.route("/delete/<int:id>")
@login_required
def delete(id):
	db = get_db()
	db.execute(
		"DELETE FROM Events WHERE EventId = ?", (id,)
	)
	db.commit()
	return redirect(url_for("user.event"))


@bp.route("/manage/<int:event_id>")
@login_required
def manage(event_id):
	db = get_db()
	events = db.execute(
		"SELECT * FROM Events WHERE EventId  = ?", (event_id,)
	).fetchone()
	tasks = db.execute(
		"SELECT * FROM Tasks WHERE EventId = ?", (event_id,)
	).fetchall()
	budget = db.execute(
		"SELECT * FROM Budgets WHERE EventID = ?", (event_id,)
	).fetchall()
	attendance = db.execute(
		"SELECT * FROM Attendees WHERE EventId = ?", (event_id,)
	).fetchall()
	cost = 0
	total = 0
	for money in budget:
		cost += money['TotalBudget']
		total += money['AmountSpent']
	return render_template("Events/manage.html", events=events, tasks=tasks, budget=budget, attendance=attendance, cost=cost, total=total)


@bp.route("/task", methods=('POST', 'Get'))
@login_required
def task():
	if request.method == "POST":
		name = request.form["TaskName"]
		e_id = request.form["EventId"]
		db = get_db()
		db.execute(
			"INSERT INTO Tasks(EventId, TaskName) VALUES (?, ?)", (e_id, name,)
		)
		db.commit()
		return redirect(url_for("event.manage", event_id=e_id))
	return redirect(url_for("user.index"))


@bp.route("/task_d/<int:id>")
@login_required
def deleteTask(id):
	db = get_db()
	e_id = db.execute(
		"Select * FROM Tasks WHERE TaskId= ?", (id,)
	).fetchone()
	db.execute(
		"DELETE FROM Tasks WHERE TaskId = ?", (id,)
	)
	db.commit()
	return redirect(url_for("event.manage", event_id=e_id['EventID']))


@bp.route("/budget", methods=('POST', 'Get'))
@login_required
def budget():
	if request.method == "POST":
		category = request.form["Category"]
		plan = request.form["TotalBudget"]
		cost = request.form["AmountSpent"]
		e_id = request.form["EventId"]
		db = get_db()
		db.execute(
			"INSERT INTO Budgets (EventId, Category, TotalBudget, AmountSpent) VALUES (?, ?, ?, ?)", (e_id, category, plan, cost,)
		)
		db.commit()
		return redirect(url_for("event.manage", event_id=e_id))
	return redirect(url_for("user.index"))


@bp.route("/budget_d/<int:id>")
@login_required
def deleteBudget(id):
	db = get_db()
	e_id = db.execute(
		"Select * FROM Budgets WHERE BudgetId= ?", (id,)
	).fetchone()
	db.execute(
		"DELETE FROM Budgets WHERE BudgetId = ?", (id,)
	)
	db.commit()
	return redirect(url_for("event.manage", event_id=e_id['EventID']))


@bp.route("/attend", methods=('POST', 'Get'))
@login_required
def attend():
	if request.method == "POST":
		name = request.form["Name"]
		email = request.form["Email"]
		e_id = request.form["EventId"]
		db = get_db()
		db.execute(
			"INSERT INTO Attendees(EventId, Name, email) VALUES (?, ?, ?)", (e_id, name, email,)
		)
		db.commit()
		return redirect(url_for("event.manage", event_id=e_id))
	return redirect(url_for("user.index"))


@bp.route("/attend_d/<int:id>")
@login_required
def deleteAttend(id):
	db = get_db()
	e_id = db.execute(
		"Select * FROM Attendees WHERE AttendeeId= ?", (id,)
	).fetchone()
	db.execute(
		"DELETE FROM Attendees WHERE AttendeeId = ?", (id,)
	)
	db.commit()
	return redirect(url_for("event.manage", event_id=e_id['EventID']))
