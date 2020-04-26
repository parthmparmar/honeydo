from flask import Flask, redirect, url_for, render_template
from hdo import app
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
#from flask_bootstrap import Bootstrap
from hdo.forms import LoginForm, RegisterForm
from hdo.models import Users
from hdo import db
import datetime

@app.route('/')
def hello_world():
    return 'Hello World'

@app.route('/login')
def login():
    form = LoginForm

    if form.validate_on_submit():
        #return '<h1>' + form.email.data + ' ' + form.password.data + '</h1>'
        user = Users.query.filter_by(email=form.email.data).first()
        if user:
            if user.password == form.password.data:
                return redirect(url_for('lists.html'))

        return 'Invalid username or password'

    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        new_user = Users(email = form.email.data, name = form.name.data , hash_password = form.password.data, active = 0, last_login = datetime.datetime.now())
        db.session.add(new_user)
        db.session.commit()

        #return 'New user has been created!'
        return '<h1>' + form.email.data + ' ' + form.password.data + '</h1>'

    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return 'You are now logged out'
