from hdo.models import Users, Lists, Access, Tasks
from hdo import db

def is_owner(user_id, list_id):
    list = Lists.query.filter_by(list_id = list_id).first()

    if list.list_owner_id == user_id:
        return True
    else:
        return False

def has_access(user_id, list_id):
    access = Access.query.filter_by(list_id = list_id, user_id = user_id).first()
    if access:
        return True
    else:
        return False
