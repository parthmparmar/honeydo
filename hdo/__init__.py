from flask import Flask
from config import *
from .extensions import db
from hdo import models
from flask_bootstrap import Bootstrap

app = Flask(__name__,instance_relative_config=False)
app.config.from_object('config.DevelopmentConfig')
db.init_app(app)
Bootstrap(app)

from hdo import views

with app.app_context():
    db.create_all()
