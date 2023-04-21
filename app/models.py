from typing import Optional, List
from sqlalchemy import String, Integer, Float, ForeignKey, create_engine
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship, sessionmaker

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Base(DeclarativeBase):
    pass

class User(UserMixin, Base):
    """ User class """
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(100))
    password_hash: Mapped[str] = mapped_column(String(128))
    fullname: Mapped[Optional[str]]
    email: Mapped[Optional[str]] = mapped_column(String(100))

    # initializes 
    def __init__(self, username, password_hash, fullname="", email=''):
        self.username = username
        self.password_hash = password_hash
        self.fullname = fullname
        self.email = email

    def __repr__(self) -> str:
        return f'<User {self.username}>'
    
engine = create_engine("sqlite:///app.db", echo=True)

Base.metadata.create_all(bind=engine)

