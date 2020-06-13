from flask import Flask
from config import *
from .extensions import db
from flask_login import LoginManager #, UserMixin, login_user, login_required, logout_user, current_user
from flask_mail import Mail
import os
from dotenv import load_dotenv

app = Flask(__name__,instance_relative_config=False)

if os.getenv('SECRET_KEY'):
    app.config.from_object('config.ProductionConfig')
else:
    app.config.from_object('config.DevelopmentConfig')

db.init_app(app)
mail = Mail(app)
login = LoginManager()
login.init_app(app)
login.login_view = "login"


from hdo import views

with app.app_context():
    db.create_all()
