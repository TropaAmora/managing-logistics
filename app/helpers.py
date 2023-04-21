""" This file comprises all the functions needed in the project """
from app import session, login_manager
from models import User


@login_manager.user_loader
def load_user(id):
    return session.query(User).filter(id).first()
