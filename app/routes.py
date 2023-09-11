from flask import render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user, login_user, logout_user
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from is_safe_url import is_safe_url
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.urls import url_parse

from app import app, session, N
from app.models import User, Client, Product, Sale, SaleBatch
from app.forms import LoginForm, RegistrationForm, ClientRegistrationForm, ProductRegistrationForm, SaleRegistrationForm, SaleBatchRegistrationForm
from app.helpers import get_list_id, get_list_ref

@app.route("/")
@login_required
def index():
    user_id = int(current_user.get_id())
    user = session.query(User).filter(User.id == user_id).first()
    return render_template("index.html", username=user.username)

@app.route("/login", methods=['GET', 'POST'])
def login():
    # Do login as the user got here to login
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if request.method == 'POST':
        # query the database for the username of the form value
        user = session.query(User).filter(User.username == form.username.data).first()
        if user is None or not check_password_hash(user.password_hash, form.password.data):
            flash('Username or password are incorrect.')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)
        flash('Login successful')
        next_page = request.args.get('next')
        
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    else:
        return render_template('login.html', form=form)
        
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        # if the form is validated is similar to the request method being post
        pwd = generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, 
                        password_hash=pwd, 
                        email=form.email.data)
        session.add(new_user)
        session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('index'))
    else:
        return render_template('register.html', form=form)
    
@app.route("/registerclient", methods=['GET', 'POST'])
@login_required
def registerclient():
    form = ClientRegistrationForm()
    if request.method == 'POST':
        # Register the client
        id_user = int(current_user.get_id())
        new_client = Client(form.name.data, 
                            form.address.data, 
                            form.email.data, 
                            form.description.data, 
                            id_user)
        session.add(new_client)
        session.commit()
        flash('Congratulations, you created a new client!')
        return redirect(url_for('index'))
    else:
        return render_template('registerclient.html', form=form)
    
@app.route("/registerproduct", methods=['GET', 'POST'])
@login_required
def registerproduct():
    form = ProductRegistrationForm()
    id_user = int(current_user.get_id())
    if request.method == 'POST':
        # do stuff
        new_product = Product(ref=form.ref.data, 
                              name=form.name.data, 
                              stock=form.stock.data, 
                              user_id=id_user)
        session.add(new_product)
        session.commit()
        flash('Congratulations, you created a new product.')
        return redirect(url_for('index'))
    else:
        return render_template('registerproduct.html', form=form)

    
@app.route("/registersale", methods=['GET', 'POST'])
@login_required
def registersale():
    global N # means: in this scope, use the global name
    id_user = int(current_user.get_id())
    clients_list = get_list_id(Client, id_user)
    form = SaleRegistrationForm()
    form.client.choices = clients_list
    if request.method == 'POST':
        # register sale here
        new_sale = Sale(user_id=id_user, 
                        client_id=form.client.data
                        )
        session.add(new_sale)
        session.commit()
        id_sale = session.query(Sale.id).filter(Sale.user_id == id_user).order_by(Sale.id.desc()).first()
        # using temporary lists to store the values for each sale batch
        sb = {
            'sale_batches-0-product_ref':[], 
            'sale_batches-0-quantity':[], 
            'sale_batches-0-saleprice':[]
            }
        for keys in request.form.keys():
            i = 0
            if keys == 'sale_batches-0-product_ref':
                for value in request.form.getlist(keys):
                    sb['sale_batches-0-product_ref'].append(value)
                    i += 1
            i = 0
            if keys == 'sale_batches-0-quantity':
                for value in request.form.getlist(keys):
                    sb['sale_batches-0-quantity'].append(value)
                    i += 1
            i = 0
            if keys == 'sale_batches-0-saleprice':
                for value in request.form.getlist(keys):
                    sb['sale_batches-0-saleprice'].append(value)
                    i += 1
        for index in range(N):
            new_salebatch = SaleBatch(product_ref=int(sb['sale_batches-0-product_ref'][index]),
                                      quantity=int(sb['sale_batches-0-quantity'][index]), 
                                      saleprice=float(sb['sale_batches-0-saleprice'][index]), 
                                      sale_id=(id_sale[0]), 
                                      )
            product = session.query(Product).filter(Product.ref == new_salebatch.product_ref).first()
            product.stock -= new_salebatch.quantity
            session.add(new_salebatch)
            session.commit()
        flash('Congratulations, you registered a sale.')
        N = 1
        return redirect(url_for('index'))
    else:
        return render_template('registersale.html', form=form, N=N)
        
@app.route("/clients", methods=['GET', 'POST'])
def clients():
    if request.method == 'GET':
        id_user = int(current_user.get_id())
        clients = session.query(Client).filter(Client.user_id == id_user).all()
        return render_template('clients.html', clients=clients)
    else:
        return redirect(url_for('index'))
    
@app.route("/products", methods=['GET', 'POST'])
def products():
    if request.method == 'GET':
        id_user = int(current_user.get_id())
        products = session.query(Product).filter(Product.user_id == id_user).all()
        return render_template('products.html', products=products)
    else:
        return redirect(url_for('index'))
    

@app.route("/sales", methods=['GET', 'POST'])
def sales():
    if request.method == 'GET':
        id_user = int(current_user.get_id())
        sales = session.query(Sale).join(SaleBatch, Sale.id == SaleBatch.sale_id).filter(Sale.user_id == id_user).all()
        return render_template('sales.html', sales=sales)
    else:
        return redirect(url_for('index'))
    
@app.route("/addsalebatch", methods=['GET', 'POST'])
@login_required
def addsalebatch():
    global N
    N += 1
    return redirect(url_for('registersale'))

@app.route("/removesalebatch", methods=['GET', 'POST'])
@login_required
def removesalebatch():
    global N
    if N > 1:
        N -= 1
    return redirect(url_for('registersale'))