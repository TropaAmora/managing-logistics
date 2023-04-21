""" This file imports the app instance from the app directory """
# Flask will look for this file to initialize the application
# Just import the app, and db fil (the last one should not be needed)
# the flask shell context should be initialized herex

from app import app, session
from app.models import User


