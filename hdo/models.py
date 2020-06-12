from hdo import db, login
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

class Users(UserMixin, db.Model): 
	__tablename__ = "Users"
	id=db.Column(db.Integer, primary_key=True)
	email=db.Column(db.String, unique=True)
	name=db.Column(db.String)
	hash_password=db.Column(db.String)
	active=db.Column(db.Integer)
	last_login=db.Column(db.DateTime)

@login.user_loader
def load_user(id):
	return Users.query.get(int(id))

class Lists(db.Model):

	__tablename__ = "Lists"
	list_id=db.Column(db.Integer, primary_key=True)
	list_name=db.Column(db.String, nullable=False)
	list_description=db.Column(db.String)
	list_owner_id=db.Column(db.Integer, db.ForeignKey("Users.id"), nullable=False)
	list_owner=db.relationship("Users", foreign_keys = [list_owner_id], lazy=True)
	list_access = db.relationship("Access", cascade="all, delete-orphan")
	list_tasks = db.relationship("Tasks", cascade="all, delete-orphan")

class Tasks(db.Model):
	__tablename__ = "Tasks"
	task_id=db.Column(db.Integer, primary_key=True)
	list_id=db.Column(db.Integer, db.ForeignKey("Lists.list_id"), nullable=False)
	list=db.relationship("Lists", foreign_keys = [list_id], lazy=True)
	task_name=db.Column(db.String)
	task_owner_id=db.Column(db.Integer, db.ForeignKey("Users.id"), nullable=False)
	task_owner=db.relationship("Users", foreign_keys = [task_owner_id], lazy=True)
	due_date=db.Column(db.Date)
	reset_time=db.Column(db.DateTime)
	state=db.Column(db.Integer)
	assigned_user_id=db.Column(db.Integer, db.ForeignKey("Users.id"))
	assigned_user = db.relationship("Users", foreign_keys = [assigned_user_id], lazy = True)
	completed_by_id=db.Column(db.Integer, db.ForeignKey("Users.id"))
	completed_by = db.relationship("Users", foreign_keys = [completed_by_id], lazy = True)
	points=db.Column(db.Integer)
	repeat=db.Column(db.Integer)

class Access(db.Model):
	__tablename__ = "Access"
	access_id=db.Column(db.Integer, primary_key=True)
	list_id=db.Column(db.Integer, db.ForeignKey("Lists.list_id"), nullable=False)
	list=db.relationship("Lists", foreign_keys = [list_id], lazy=True)
	user_id=db.Column(db.Integer, db.ForeignKey("Users.id"), nullable=False)
	user=db.relationship("Users", foreign_keys = [user_id], lazy=True)
	write=db.Column(db.Boolean)
