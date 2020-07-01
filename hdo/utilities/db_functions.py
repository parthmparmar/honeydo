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

def tasks_by_owner_list_state(current_user, list_id, state):
    tasks = Tasks.query.filter_by(task_owner_id = current_user, list_id = list_id, state = state)
    return tasks

def tasks_by_owner_state(current_user, state):
    tasks = Tasks.query.filter_by(task_owner_id = current_user, state = state).order_by(Tasks.task_completed_date.desc())
    return tasks

def tasks_by_id(task_id):
    tasks = Tasks.query.filter_by(task_id = task_id).first()
    return tasks

'''
#recurrence when none exists yet
def new_recurrence(task_id, recur_method, recur_days):
    if recur_method = "creation":
        new_task = Tasks()
#removing recurrence when it already was enabled

#changing recurrence '''
