from hdo import db

class Users(db.Model):  #accessing Model class of SQLAlchemy
	__tablename__ = "Users"
	id=db.Column(db.Integer, primary_key=True)
	email=db.Column(db.String, unique=True)
	name=db.Column(db.String)
	hash_password=db.Column(db.String)
	active=db.Column(db.Integer)
	last_login=db.Column(db.DateTime)

'''	def __init__(self,id,email,name, hash_password,active,last_login):
		self.id=id
		self.email=email
		self.name=name
		self.hash_password=hash_password
		self.active=active
		self.last_login=last_login'''

class Lists(db.Model):  #accessing Model class of SQLAlchemy
	__tablename__ = "Lists"
	list_id=db.Column(db.Integer, primary_key=True)
	list_name=db.Column(db.String)
	list_owner=db.Column(db.String)


	def __init__(self,list_id,list_name,list_owner):
		self.list_id=list_id
		self.list_name=list_name
		self.list_owner=list_owner

class Tasks(db.Model):  #accessing Model class of SQLAlchemy
	__tablename__ = "Tasks"
	task_id=db.Column(db.Integer, primary_key=True)
	list_id=db.Column(db.Integer)
	task_name=db.Column(db.String)
	task_owner=db.Column(db.String)
	due_date=db.Column(db.DateTime)
	reset_time=db.Column(db.DateTime)
	state=db.Column(db.Integer)
	points=db.Column(db.Integer)
	repeat=db.Column(db.Integer)

	def __init__(self,task_id,list_id,task_name,task_owner,due_date,reset_time,state,points,repeat):
		self.task_id=task_id
		self.list_id=list_id
		self.task_name=task_name
		self.task_owner=task_owner
		self.due_date=due_date
		self.reset_time=reset_time
		self.state=state
		self.points=points
		self.repeat=repeat

class Access(db.Model):  #accessing Model class of SQLAlchemy
	__tablename__ = "Access"
	access_id=db.Column(db.Integer, primary_key=True)
	list_id=db.Column(db.Integer)
	user_id=db.Column(db.Integer)
	write=db.Column(db.Integer)


	def __init__(self,access_id,list_id,user_id,write):
		self.access_id=access_id
		self.list_id=list_id
		self.user_id=user_id
		self.write=write
