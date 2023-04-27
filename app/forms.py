from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length

from app.models import User, Client, Product
from app import session

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remmember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    validation = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = session.query(User).filter(User.username == username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')
        
    def validate_email(self, email):
        user = session.query(User).filter(User.email == email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
        
    
class ClientRegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 40)])
    address = StringField('Address', validators=[DataRequired(), Length(10, 40)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Create Client')

    def validate_client(self, email):
        user = session.query(Client).filter(Client.email == email.data).first()
        if user is not None:
            raise ValidationError('This email is already registered on another existing client')
        

class ProductRegistrationForm(FlaskForm):
    ref = IntegerField('Refference', validators=[DataRequired(), Length(10, 20)])
    name = StringField('Name', validators=[DataRequired(), Length(1, 40)])
    stock = IntegerField('Initial stock', validators=[DataRequired()])
    submit = SubmitField('Add product')

    def validate_ref(self, ref):
        product = session.query(Product).filer(Product.ref == ref).first()
        if product is not None:
            raise ValidationError('The refference is already registered.')
        

class SaleRegistrationForm(FlaskForm):
    pass