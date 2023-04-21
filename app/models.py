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
    username: Mapped[str] = mapped_column(String(120))
    password_hash: Mapped[str] = mapped_column(String(128))
    fullname: Mapped[Optional[str]]

    # initializes 
    def __init__(self, id, username, password_hash, fullname):
        self.username = username
        self.password_hash = password_hash

    def __repr__(self) -> str:
        return f'<User {self.username}>'
    
engine = create_engine("sqlite:///app.db", echo=True)

Base.metadata.create_all(bind=engine)