from flask import Flask, redirect, url_for, render_template, request, flash
from hdo import app
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from hdo.models import Users, Lists, Access, Tasks
from hdo import db
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import json

@app.route('/')
def hello_world():
    try:
        return "Hello " + current_user.name
    except:
        return 'Hello World'

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
                return redirect(url_for("dashboard"))

        return "Invalid Username or Password"


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     form = LoginForm()
#
#     if form.validate_on_submit():
#         #return '<h1>' + form.email.data + ' ' + form.password.data + '</h1>'
#         user = Users.query.filter_by(email=form.email.data).first()
#         if user:
#             if check_password_hash(user.hash_password, form.password.data):#user.hash_password == form.password.data:
#                 login_user(user)
#                 return render_template('lists.html') #will need to change to redirect when route is set up
#
#         return 'Invalid username or password'
#
#     return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        email = request.form["email"]
        user = Users.query.filter_by(email=email).first()

        if user:
            flash("Unfortunately, " + user.email + " is already in use.", 'danger') #need to change to a red message
            return redirect(url_for("register"))
        hashed_password = generate_password_hash(request.form["password"], method='sha256')
        new_user = Users(email = request.form["email"], name = request.form["name"] , hash_password = hashed_password, active = 0, last_login = datetime.datetime.now())
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("login"))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return 'You are now logged out'

@app.route("/lists", methods=["GET"])
def dashboard():
    if request.method == "GET":
        user_lists = Access.query.filter_by(user_id=current_user.id).all()
        data = {"user_lists": user_lists}
        return render_template("lists.html", data = data)

@app.route("/list/<list_id>", methods=["GET"])
def list_display(list_id):
    if request.method == "GET":
        tasks = Tasks.query.filter_by(list_id=list_id).all()
        list = Lists.query.filter_by(list_id=list_id).first()
        task_data = {"tasks": tasks}
        return render_template("tasks.html", list = list, task_data = task_data, list_id = list_id,)

        #list = Lists.query.filter_by(list_id = list_id).first()
        #return list.list_name + " -- " + list.list_owner.email

@app.route("/api/task/<list_id>/add", methods=["POST"])
def api_task(list_id):
    if request.method == "POST":
        task_name = request.form["task_name"]
        due_date = request.form["due_date"]
        points = request.form["points"]
        new_task = Tasks(list_id = list_id, task_name = task_name, task_owner_id = current_user.id, due_date = due_date, state = 1, points=points)
        db.session.add(new_task)
        db.session.commit()
        flash(task_name + " was added", "success")
        return redirect(url_for("list_display", list_id = list_id))



@app.route("/api/list/add", methods=["POST"])
def api_list():
    if request.method == "POST":
        list_name = request.form["list_name"]
        new_list = Lists(list_name = list_name, list_owner_id= current_user.id)
        db.session.add(new_list)
        db.session.flush()
        db.session.refresh(new_list)
        list_id = new_list.list_id
        new_access = Access(list_id = list_id, user_id = current_user.id)
        db.session.add(new_access)
        db.session.commit()
        flash(list_name + " was added", "success")
        return redirect(url_for("dashboard"))

@app.route("/api/lists/get", methods=["GET"])
def api_get_lists():
    if request.method == "GET":
        lists = Lists.query.all()
        print(lists)
        for list in lists:
            print(list.list_owner.email)
        return "test"

@app.route("/api/<list_id>/task/<task_id>/delete", methods=["POST"])
def api_delete_task(list_id, task_id):
    if request.method == "POST":
        task_to_delete = Tasks.query.filter_by(task_id=task_id).first()
        task_name = task_to_delete.task_name
        db.session.delete(task_to_delete)
        db.session.flush()
        db.session.commit()
        flash(task_name + " was deleted", "success")
        return redirect(url_for("list_display", list_id = list_id))

@app.route("/api/<list_id>/task/<task_id>/update_state", methods=["POST"])
def api_update_state(list_id, task_id):
    if request.method == "POST":

        task_to_update = Tasks.query.filter_by(task_id=task_id).first()
        task_name = task_to_update.task_name
        task_to_update.state = 0
        #db.session.update(task_to_update) #wrong method
        db.session.flush()
        db.session.commit()
        flash(task_name + " was updated", "success")
        return redirect(url_for("list_display", list_id = list_id))
