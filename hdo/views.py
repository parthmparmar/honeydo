from flask import Flask, redirect, url_for, render_template, request, flash
from hdo import app
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from hdo.models import Users, Lists, Access
from hdo import db
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import json
import re

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
        password = request.form["password"]
        pattern = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])(?=.*[^\s])[A-Za-z\d@$!#%*?&]{8,}$")
        if re.match(pattern, password) is None:
            flash("Password does not meet minimum requirement of 8 Characters long, with one capital letter, one lowercase letter, one digit and one special character.", "danger")
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

@app.route("/dashboard", methods=["GET"])
def dashboard():
    if request.method == "GET":
        user_lists = Access.query.filter_by(user_id=current_user.id).all()
        modal = {"title": "Confirm", "msg": "Are you sure you want to delete the list?"}
        data = {"user_lists": user_lists, "modal": modal}
        return render_template("lists.html", data = data)

@app.route("/list/<list_id>", methods=["GET"])
def list_display(list_id):
    if request.method == "GET":
        list = Lists.query.filter_by(list_id = list_id).first()
        return list.list_name + " -- " + list.list_owner.email

@app.route("/api/list/<list_id>", methods=["POST", "DELETE"])
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
        list = Lists.query.filter_by(list_id = list_id).first()
        list_name = list.list_name
        db.session.delete(list)
        db.session.commit()
        flash(list_name + " was deleted!", "success")
        return "list deleted"
        # todo: Do we also need to delete the task for this list?  How do we want to do that? SQLAlchemy Cascades

@app.route("/api/lists/get", methods=["GET"])
def api_get_lists():
    if request.method == "GET":
        lists = Lists.query.all()
        print(lists)
        for list in lists:
            print(list.list_owner.email)
        return "test"

@app.route("/api/access/<access_id>", methods=["GET", "POST", "DELETE"])
def api_access(access_id):
    if request.method == "DELETE":
        access = Access.query.filter_by(access_id = access_id).first()
        if access:
            db.session.delete(access)
            db.session.commit()
            return "Access Deleted"
        else:
            return "Access Item Not Found", 404
