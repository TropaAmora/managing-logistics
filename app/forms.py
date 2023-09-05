from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField, FormField, FieldList, DecimalField, Form
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length, InputRequired

from app.models import User, Client, Product, SaleBatch
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
        product = session.query(Product).filter(Product.ref == ref).first()
        if product is not None:
            raise ValidationError('The refference is already registered.')
        
    def validate_stock(self, stock):
        if stock < 1:
            raise ValidationError('Please insert a valid quantity')
        


class SaleBatchRegistrationForm(Form):
    #product_ref = SelectField('Product name', coerce=int, validators=[InputRequired()])
    product_ref = IntegerField('Product ref', validators=[InputRequired()])
    quantity = IntegerField('Quantity', validators=[InputRequired()])
    saleprice = DecimalField('Price', validators=[InputRequired()])

    # if done with SelectField remove this validation step
    def validate_ref(self, ref):
        product = session.query(Product).filter(Product.ref == ref).first()
        if product is None:
            raise ValidationError('The product ref does not exist.')
        
    def validate_quantity(self, quantity):
        if quantity < 1:
            raise ValidationError('The quantity should be an integer greater or equal to one.')

class SaleRegistrationForm(FlaskForm):
    client = SelectField('Client name', coerce=int, validators=[InputRequired()])
    sale_batches = FieldList(FormField(SaleBatchRegistrationForm), min_entries=1, max_entries=5)

    # probably better to add a validate function for the number of sale_batches