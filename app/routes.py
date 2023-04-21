from flask import render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user, login_user, logout_user
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from is_safe_url import is_safe_url
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.urls import url_parse

from app import app, session
from app.models import User
from app.forms import LoginForm, RegistrationForm

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
            flash('Username or password are uncorrect.')
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
    form = RegistrationForm()
    if request.method == 'POST':
        # do stuff
        
    else:
        return render_template('register', form=form)