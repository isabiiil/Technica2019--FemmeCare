# auth.py

from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from .models import User
from . import db

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
	return render_template('login.html')

@auth.route('/signup')
def signup():
	return render_template('signup.html')

@auth.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('main.index'))	

@auth.route('/account')
@login_required
def account():
	return render_template('account.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
	email = request.form.get('email')
	name = request.form.get('name')
	password = request.form.get('password')
	remember = True if request.form.get('remember') else False

	user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

	if user: # if a user is found, we want to redirect back to signup page so user can try again
		flash('Email address already exists')
		return redirect(url_for('auth.signup'))

	# create new user with the form data. Hash the password so plaintext version isn't saved.
	new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

	# add the new user to the database
	db.session.add(new_user)
	db.session.commit()
	login_user(new_user,remember=remember)
	return redirect(url_for('auth.account'))

@auth.route('/login', methods=['POST'])
def login_post():
	email = request.form.get('email')
	password = request.form.get('password')
	remember = True if request.form.get('remember') else False

	user = User.query.filter_by(email=email).first()

	# check if user actually exists
	# take the user supplied password, hash it, and compare it to the hashed password in database
	if not user or not check_password_hash(user.password, password): 
		flash('Please check your login details and try again.')
		return redirect(url_for('auth.login')) # if user doesn't exist or password is wrong, reload the page

	# if the above check passes, then we know the user has the right credentials
	login_user(user,remember=remember)
	return redirect(url_for('main.profile'))

@auth.route('/account', methods=['POST'])
@login_required
def account_post():
	bank = request.form.get('bank')
	account = request.form.get('accountNumber')
	routing = request.form.get('routingNumber')

	user = current_user
	user.bank = bank
	user.account = account
	user.routing = routing
	user.total = 0

	db.session.commit()

	return redirect(url_for('main.nonprofit'))