""" This file comprises all the functions needed for the project """
from app import session
import calendar

def get_list_id(table, user_id):
    """ Returns a list of objects queried from the db based on the model name """
    names = [(name.id, name.name) for name in session.query(table).filter(table.user_id == user_id).order_by('name')]
    return names

def get_list_ref(table, user_id):
    """ Returns a list of objects queried from the db based on the model name """
    names = [(name.ref, name.name) for name in session.query(table).filter(table.user_id == user_id).order_by('name')]
    return names

def dow_name(dow):
    return calendar.day_name[dow]


