from flask import Flask
#from models import db
from config import *

def create_app():
    app = Flask(__name__,instance_relative_config=False)
    app.config.from_object('config.DevelopmentConfig')
    # app.run()

    with app.app_context():
        from . import views

    return app
    #db.init_app(app)
