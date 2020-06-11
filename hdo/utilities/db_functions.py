from hdo.models import Users, Lists, Access, Tasks
from hdo import db
import string
from random import *


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

def list_num_users(lists):
    if type(lists) is list:
        for list_item in lists:
            access = Access.query.filter_by(list_id = list_item.list_id).all()
            list_item.num_users = len(access)

    else:
        access = Access.query.filter_by(list_id = lists.list_id).all()
        lists.num_users = len(access)
    return lists

def random_password():
    characters = string.ascii_letters + string.digits
    password =  "".join(choice(characters) for x in range(randint(8, 16)))
    return password
