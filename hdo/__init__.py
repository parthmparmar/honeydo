from flask import Flask
from config import *
from .extensions import db
from hdo import models
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__,instance_relative_config=False)
app.config.from_object('config.DevelopmentConfig')
db.init_app(app)
#login = LoginManager(app)
Bootstrap(app) #might need to be moved

from hdo import views

with app.app_context():
    db.create_all()
