""" This file initializes all the instances needed to run the applications """

from typing import Optional, List
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_login import LoginManager

from app.models import User
from config import Config

import calendar

# Creation of the app instance and apply the config class
app = Flask(__name__)
app.config.from_object(Config)
Session(app)

# instance db
db = SQLAlchemy(app) 

# Apply the LoginManager class to the app instance
login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'login'

# SQLalchemy stuff to start the engine
connection_link = app.config['SQLALCHEMY_DATABASE_URI']
engine = create_engine(connection_link, echo=True)
Session_db = sessionmaker(bind=engine)
session = Session_db()


# user_loader function, dont know where to put it
@login_manager.user_loader
def load_user(id):
    return session.query(User).filter(User.id == int(id)).first()

def dow_name(dow):
    return calendar.day_name[dow]

app.jinja_env.filters['dow'] = dow_name
#u1 = User(username='Anna')
#u1.set_password('123')
#session.add(u1)
#session.commit()

#people = session.query(User).filter(User.username == "Anna")

#for r in people:
#    print(r)

from app import routes, models