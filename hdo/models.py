from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class userData(db.usersModel):  #accessing Model class of SQLAlchemy
	__tablename__ = "users"
	userid=db.Column(db.Integer, primary_key=True)
	email=db.Column(db.EmailType)
	name=db.Column(db.String)
	hash_password=db.Column(db.String)
    active=db.Column(db.Boolean)
    last_login.Column(db.DateTime)

	def __init__(self,userid,email,name,hash_password,active,last_login):
		self.userid=userid
		self.email=email
		self.name=name
        self.hash_password=hash_password
        self.active=active
        self.last_login=last_login
