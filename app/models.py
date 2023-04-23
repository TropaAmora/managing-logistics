""" This file contains the several models used in this application """

import datetime
from typing import Optional, List
from sqlalchemy import String, Integer, Float, ForeignKey, create_engine, DateTime, TIMESTAMP
from sqlalchemy import func
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship, sessionmaker

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Base(DeclarativeBase):
    type_annotation_map = {
    datetime.datetime: TIMESTAMP(timezone=True),
    }

class User(UserMixin, Base):
    """ User class """
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(100))
    password_hash: Mapped[str] = mapped_column(String(128))
    fullname: Mapped[Optional[str]]
    email: Mapped[Optional[str]] = mapped_column(String(100))
    #created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    sales: Mapped[List["Sale"]] = relationship(back_populates="user")

    # initializes 
    def __init__(self, username, password_hash, fullname="", email=''):
        self.username = username
        self.password_hash = password_hash
        self.fullname = fullname
        self.email = email

    def __repr__(self) -> str:
        return f'<User {self.username}>'
    

class Client(Base):
    """ Client class """
    __tablename__ = 'client'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    adress: Mapped[str] = mapped_column(String(100))
    email: Mapped[Optional[str]] = mapped_column(String(100))
    description: Mapped[Optional[str]] = mapped_column(String(128))
    #created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    sales: Mapped[List["Sale"]] = relationship(back_populates="client")

    def __init__(self, name, adress, email):
        self.name = name
        self.adress = adress
        self.email = email

    def __repr__(self) -> str:
        return f'<Client {self.name}>'


class Product(Base):
    """ Product class """
    __tablename__ = 'product'
    ref: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    # add a ptype_id to connect with the ptype table
    stock: Mapped[int] = mapped_column(Integer)

    salebatches: Mapped[List["SaleBatch"]] = relationship(back_populates="product")    

    def __init__(self, refference, name, stock):
        self.refference = refference
        self.name = name
        self.stock = stock
    
    def __repr__(self) -> str:
        return f'<Product {self.name} ({self.refference})>'

class Sale(Base):
    """ Sale class """
    __tablename__ = 'sale'

    id: Mapped[int] = mapped_column(primary_key=True)
    #timestamp: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    client_id: Mapped[int] = mapped_column(ForeignKey("client.id"))

    salebatches: Mapped[List["SaleBatch"]] = relationship(back_populates="sale")

    # Create the init method to ensure that this fields are filled and a row may be created
    def __init__(self, user_id, client_id):
        self.user_id = user_id
        self.client_id = client_id

    def __repr__(self):
        return f'<Sale {self.id}>'
    
class SaleBatch(Base):
    """ Sale batch class """
    __tablename__ = 'salebatch'

    id: Mapped[int] = mapped_column(primary_key=True)
    quantity: Mapped[int] = mapped_column(Integer)
    saleprice: Mapped[float] = mapped_column(Float)
    sale_id: Mapped[int] = mapped_column(ForeignKey("sale.id"))
    product_ref: Mapped[int] = mapped_column(ForeignKey("product.ref"))

    def __init__(self, quantity, saleprice, sale_id, product_id):
        self.quantity = quantity
        self.saleprice = saleprice
        self.sale_id = sale_id
        self.product_id = product_id

    def __repr__(self):
        return f'Sale batch {self.id}'


# Engine creation first and the creation of all the tabels that result from this models
engine = create_engine("sqlite:///app.db", echo=True)
Base.metadata.create_all(bind=engine)