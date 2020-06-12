from flask import Flask, redirect, url_for, render_template, request, flash, Markup
from hdo import app
from flask_login import login_user, login_required, logout_user, current_user
from hdo.models import Users, Lists, Access, Tasks
from hdo import db, mail
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import re
from hdo.utilities.db_functions import is_owner, has_access, list_num_users, random_password
#from sqlalchemy.sql import text
from sqlalchemy import create_engine
from config import *
from flask_mail import Message
from hdo.utilities.email_functions import *

engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])

@app.route('/')
@login_required
def hello_world():
    return redirect(url_for("tasksummary"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login_page.html")

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = Users.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.hash_password, password):
                login_user(user)
                flash("Welcome Back " + user.name, "success")
                return redirect(url_for("tasksummary"))

        flash("email and/or password incorrect, please try again." "warning")
        return redirect(url_for("login"))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        password = request.form["password"]
        pattern = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])(?=.*[^\s])[A-Za-z\d@$!#%*?&]{8,}$")
        if re.match(pattern, password) is None:
            flash("Password does not meet minimum requirement of 8 Characters long, with one capital letter, one lowercase letter, one digit and one special character.", "danger")
            return redirect(url_for("register"))
        email = request.form["email"]
        user = Users.query.filter_by(email=email).first()

        if user:
            flash("Unfortunately, " + user.email + " is already in use.", 'danger')
            return redirect(url_for("register"))
        hashed_password = generate_password_hash(request.form["password"], method='sha256')
        new_user = Users(email = request.form["email"], name = request.form["name"] , hash_password = hashed_password, active = 0, last_login = datetime.now())
        db.session.add(new_user)
        db.session.commit()
        email_new_user(request.form["email"])
        flash("Please login", "success")
        return redirect(url_for("login"))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You are now logged out", "success")
    return redirect(url_for("login"))

@app.route("/lists", methods=["GET"])
@login_required
def dashboard():
    if request.method == "GET":
        user_lists = Access.query.filter_by(user_id=current_user.id).all()
        user_lists = list_num_users(user_lists)
        modal = {"title": "Confirm", "msg": "Are you sure you want to delete the list?"}
        data = {"user_lists": user_lists, "modal": modal, "user": current_user}
        return render_template("lists.html", data = data)

@app.route("/list/<list_id>", methods=["GET"])
@login_required
def list_display(list_id):
    if request.method == "GET":
        list = Lists.query.filter_by(list_id=list_id).first()
        if list:
            if has_access(current_user.id, list_id):
                tasks = Tasks.query.filter_by(list_id=list_id).all()
                task_data = {"tasks": tasks}
                users = Access.query.filter_by(list_id=list_id).all()

                all_tasks = Tasks.query.order_by(Tasks.task_id).filter_by(list_id=list_id).all()
                with engine.connect() as con:
                    complete_tasks = con.execute(
                    """SELECT a.user_id, u.name, SUM (CASE WHEN a.user_id = t.completed_by_id THEN t.points ELSE 0 END) AS points
                    FROM public."Access" a
                    JOIN public."Tasks" t
                    ON a.list_id = t.list_id
                    JOIN public."Users" u
                    ON a.user_id = u.id
                    WHERE a.list_id = %s
                    GROUP BY a.user_id, u.name
                    ORDER BY points desc""", (list_id))
                list = Lists.query.filter_by(list_id=list_id).first()
                list = list_num_users(list)
                task_data = {"tasks": all_tasks}
                scoreboard_data = {"sb_data": complete_tasks}
                modal = {"title": "Confirm", "msg": "Are you sure you want to delete the task?"}
                data = {"all_tasks": all_tasks, "modal": modal}

                return render_template("tasks.html", list = list, task_data = task_data, list_id = list_id, current_user = current_user, users = users, data=data, scoreboard_data=scoreboard_data)
            else:
                flash("You don't have access to this list, please contact owner to get access", "warning")
                return redirect(url_for("dashboard"))
        else:
            return "404 Error" #replace with 404 page

        #return render_template("tasks.html", list = list, task_data = task_data, list_id = list_id, scoreboard_data = scoreboard_data, data=data)

        #list = Lists.query.filter_by(list_id = list_id).first()
        #return list.list_name + " -- " + list.list_owner.email

@app.route("/api/task/<list_id>/add", methods=["POST"])
@login_required
def api_task(list_id):
    if request.method == "POST":
        task_name = request.form["new_task_name"]
        due_date = request.form["new_due_date"] or None
        points = request.form["new_points"] or 0
        new_task = Tasks(list_id=list_id, task_name=task_name, task_owner_id=current_user.id, due_date=due_date, state=0, points=points)
        db.session.add(new_task)
        db.session.commit()
        #flash(task_name + " was added", "success")
        return redirect(url_for("list_display", list_id=list_id))



@app.route("/api/list/<list_id>", methods=["POST", "DELETE", "PUT"])
@login_required
def api_list(list_id):

    if request.method == "POST":
        list_name = request.form["list_name"]
        new_list = Lists(list_name = list_name, list_owner_id = current_user.id)
        db.session.add(new_list)
        db.session.flush()
        db.session.refresh(new_list)
        list_id = new_list.list_id
        new_access = Access(list_id = list_id, user_id = current_user.id)
        db.session.add(new_access)
        db.session.commit()
        flash(list_name + " was added", "success")
        return redirect(url_for("dashboard"))

    if request.method == "DELETE":
        # TODO: check to see if user is the owner of the list
        list = Lists.query.filter_by(list_id = list_id).first()
        list_name = list.list_name
        db.session.delete(list)
        db.session.commit()
        flash(list_name + " was deleted!", "success")
        return "list deleted"

    # update list name
    # AJAX calls
    if request.method == "PUT":
        if is_owner(current_user.id, list_id):
            list = Lists.query.filter_by(list_id = list_id).first()
            list.list_name = request.form["new_name"]
            db.session.commit()
            return "list updated"
        else:
            flash("You are not the owner of the list, please ask the owner to change the name", "danger")
            return "not allowed", 401

@app.route("/api/access/", methods=["GET", "POST", "DELETE"])
@login_required
def api_access():
    list_id = request.args["list_id"]

# Give Access
    if request.method == "POST":
        user_email=request.form["user_email"]
        user = Users.query.filter_by(email=user_email).first()
        if not user:
            flash ("User does not exist, please check email and try again.", "warning")
            return redirect(url_for("list_display", list_id = list_id))

        user_id = user.id
        if is_owner(current_user.id, list_id):
            if has_access(user_id, list_id):
                flash("User already has access to this list", "warning")
                return redirect(url_for("list_display", list_id = list_id))
            else:
                new_access = Access(list_id = list_id, user_id = user_id)
                db.session.add(new_access)
                db.session.commit()
                flash("Access given to " + user.name, "success")
                return redirect(url_for("list_display", list_id = list_id))
        else:
            flash("You are not the owner of this list, please ask ower to give access", "warning")
            return redirect(url_for("list_display", list_id = list_id))

# Access Delete
# AJAX Call
    if request.method == "DELETE":

        user_id = request.args["user_id"]
        list_id = request.args["list_id"]
        access = Access.query.filter_by(user_id = user_id, list_id = list_id).first()

        if access:
            if is_owner(current_user.id, list_id):
                db.session.delete(access)
                db.session.commit()
                flash("User removed for list", "success")
                return "Access Deleted"
            elif int(user_id) == current_user.id:
                db.session.delete(access)
                db.session.commit()
                flash("You were removed for list", "success")
                return "Self Deleted"
            else:
                flash("You are not the owner of the list, please ask owner to delete user." , "danger")
                return "Not Owner of List"
        else:
            return "Access Item Not Found", 404

@app.route("/api/<list_id>/task/<task_id>/delete", methods=["DELETE"])
@login_required
def api_delete_task(list_id, task_id):
    if request.method == "DELETE":
        task_to_delete = Tasks.query.filter_by(task_id=task_id).first()
        task_name = task_to_delete.task_name
        db.session.delete(task_to_delete)
        db.session.commit()
        flash(task_name + " was deleted", "danger")
        return "task deleted"


@app.route("/api/task/<task_id>/update_state/<location>", methods=["PUT"])
@login_required
def api_update_state(task_id, location):
    if request.method == "PUT":
        task_to_update = Tasks.query.filter_by(task_id=task_id).first()
        task_name = task_to_update.task_name
        if task_to_update.state == 1:
            task_to_update.state = 0
            task_to_update.completed_by_id = None
        elif task_to_update.state == 0:
            task_to_update.state = 1
            task_to_update.completed_by_id = current_user.id
            if location == "in_summary":
                flash(task_name + " was marked complete " + Markup('<a href="#" class="toggle_task" data-task_id={}>UNDO</a>'.format(task_id)))
        else:
            task_to_update.state = 0
        db.session.flush()
        db.session.commit()
        return "task updated"

@app.route("/api/<list_id>/task/<task_id>/claim", methods=["PUT"])
@login_required
def api_assign_user(list_id, task_id):
    user_id = current_user.id
    list = Lists.query.filter_by(list_id = list_id).first()
    list = list_num_users(list)
    if list.num_users > 1:
        action = "claimed"
    else:
        action = "prioritized"
    if request.method == "PUT":
        task_to_update = Tasks.query.filter_by(task_id=task_id).first()
        task_name = task_to_update.task_name
        if not task_to_update.assigned_user_id:
            task_to_update.assigned_user_id = user_id
            db.session.commit()
            flash(task_name + " was " + action + " by you", "success")
            return "success"
        elif task_to_update.assigned_user_id == user_id:
            task_to_update.assigned_user_id = None
            db.session.commit()
            flash(task_name + " was un-" + action + " by you", "success")
            return "success"
        elif task_to_update.assign_user_id != user_id:
            if is_owner(current_user.id, list_id):
                task_to_update.assigned_user_id = assigned_user_id
                db.session.commit()
                flash(task_name + " was " + action + " by you", "success")
                return "success"
            else:
                flash("Task has been claimed by someone else, please contact list owner to change", "warning")
                return "not allowed"




@app.route("/api/task/<task_id>/update", methods=["PUT"])
@login_required
def api_update_task(task_id):
    if request.method == "PUT":
        task_to_update = Tasks.query.filter_by(task_id=task_id).first()

        task_name = request.form["task_name"]
        task_to_update.task_name = task_name

        new_points = request.form["points"]
        task_to_update.points = new_points

        new_date = request.form["due_date"] or None
        task_to_update.due_date = new_date

        db.session.flush()
        db.session.commit()
        return "task updated"


@app.route("/tasksummary")
@login_required
def tasksummary():
    if request.method == "GET":
        with engine.connect() as con:
            tasks_due_today = con.execute(
            """SELECT t.*, l.list_name
            FROM public."Tasks" t
            JOIN public."Lists" l
            ON l.list_id = t.list_id
            WHERE t.task_owner_id = %s
            AND t.due_date = CURRENT_DATE
            AND t.state = 0""", (current_user.id))
            tasks_overdue = con.execute(
            """SELECT t.*, l.list_name
            FROM public."Tasks" t
            JOIN public."Lists" l
            ON l.list_id = t.list_id
            WHERE t.task_owner_id= %s
            AND t.due_date < CURRENT_DATE
            AND t.state = 0
            ORDER BY t.due_date ASC""", (current_user.id))
            other_tasks = con.execute(
            """SELECT t.*, l.list_name
            FROM public."Tasks" t
            JOIN public."Lists" l
            ON l.list_id = t.list_id
            WHERE t.task_owner_id = %s
            AND (t.due_date > CURRENT_DATE OR t.due_date IS NULL)
            AND t.state = 0
            ORDER BY t.due_date ASC""", (current_user.id))
        modal = {"title": "Confirm", "msg": "Are you sure you want to delete the list?"}
        data = {"tasks_due_today": tasks_due_today, "tasks_overdue": tasks_overdue, "other_tasks": other_tasks, "modal": modal}
        return render_template("tasks_summary.html", data = data)

@app.route("/reset-password", methods=["GET", "POST"])
@login_required
def reset_password():
    if request.method == "GET":
        return render_template("reset_password.html")
    if request.method == "POST":
        current_password = request.form["current-password"]
        password = request.form["password"]
        pattern = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])(?=.*[^\s])[A-Za-z\d@$!#%*?&]{8,}$")
        if re.match(pattern, password) is None:
            flash("Password does not meet minimum requirement of 8 Characters long, with one capital letter, one lowercase letter, one digit and one special character.", "danger")
            return redirect(url_for("register"))

        hashed_password = generate_password_hash(request.form["password"], method='sha256')

        if check_password_hash(current_user.hash_password, current_password):
            current_user.hash_password = hashed_password
            db.session.commit()
            flash("Password Reset", "success")
            email_reset_password(current_user.email)
            return redirect(url_for("dashboard"))
        else:
            flash("current password incorrect", "warning")
            return redirect(url_for("dashboard"))

@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "GET":
        return render_template("forgot-password.html")
    if request.method == "POST":
        email = request.form["email"]
        user = Users.query.filter_by(email=email).first()

        if user:
            new_password = random_password()
            hashed_password = generate_password_hash(new_password, method='sha256')
            user.hash_password = hashed_password
            db.session.commit()
            email_forgot_password(user.email, new_password)
            flash("Email with new password send to " + user.email, "success")
            return redirect(url_for("login"))

        flash("No user with that email found!" "warning")
        return redirect(url_for("login"))
