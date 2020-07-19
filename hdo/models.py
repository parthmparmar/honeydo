from hdo import db, login
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import datetime

class Users(UserMixin, db.Model):
	__tablename__ = "Users"
	id=db.Column(db.Integer, primary_key=True)
	email=db.Column(db.String, unique=True)
	name=db.Column(db.String)
	hash_password=db.Column(db.String)
	active=db.Column(db.Integer)
	last_login=db.Column(db.DateTime)
	user_created_date=db.Column(db.DateTime)

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
	task_description=db.Column(db.String)
	task_completed_date=db.Column(db.DateTime)
	recur_ind = db.Column(db.Integer)
	recur_days = db.Column(db.Integer)
	parent_task_id = db.Column(db.Integer)

	@property
	def to_dict(self):
		dictionary = {
			"task_id": self.task_id,
			"list_id": self.list_id,
			"task_name":self.task_name,
			"task_owner_id": self.task_owner.id,
			"task_owner_name": self.task_owner.name if self.task_owner else None,
			"due_date": self.due_date,
			"reset_time": self.reset_time,
			"state": self.state,
			"assigned_user_id": self.assigned_user_id,
			"assigned_user_name": self.assigned_user.name if self.assigned_user else None,
			"completed_by_id": self.completed_by_id,
			"completed_by_name": self.completed_by.name if self.completed_by else None,
			"points": self.points,
			"repeat": self.repeat,
			"task_description": self.task_description,
			"task_completed_date": self.task_completed_date
		}
		return dictionary


class Access(db.Model):
	__tablename__ = "Access"
	access_id=db.Column(db.Integer, primary_key=True)
	list_id=db.Column(db.Integer, db.ForeignKey("Lists.list_id"), nullable=False)
	list=db.relationship("Lists", foreign_keys = [list_id], lazy=True)
	user_id=db.Column(db.Integer, db.ForeignKey("Users.id"), nullable=False)
	user=db.relationship("Users", foreign_keys = [user_id], lazy=True)
	write=db.Column(db.Boolean)
