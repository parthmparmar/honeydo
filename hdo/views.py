from flask import Flask, redirect, url_for, render_template
from hdo import app
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
#from flask_bootstrap import Bootstrap
from hdo.forms import LoginForm, RegisterForm
from hdo.models import Users
from hdo import db
import datetime
from werkzeug.security import generate_password_hash, check_password_hash

@app.route('/')
def hello_world():
    #if current_user:
        #return 'Hello ' + current_user.name
    return 'Hello World'

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        #return '<h1>' + form.email.data + ' ' + form.password.data + '</h1>'
        user = Users.query.filter_by(email=form.email.data).first()
        if user:
            if check_password_hash(user.hash_password, form.password.data):#user.hash_password == form.password.data:
                #login_user()
                return render_template('lists.html') #will need to change to redirect when route is set up

        return 'Invalid username or password'

    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = Users(email = form.email.data, name = form.name.data , hash_password = hashed_password, active = 0, last_login = datetime.datetime.now())
        db.session.add(new_user)
        db.session.commit()

        #return 'New user has been created!'
        #return '<h1>' + form.email.data + ' ' + form.password.data + '</h1>'
        return redirect(url_for("login"))


    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return 'You are now logged out'
