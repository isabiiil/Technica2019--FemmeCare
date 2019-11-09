# main.py

from flask import Blueprint, render_template, redirect, request, url_for
from flask_login import login_required, current_user
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

@main.route('/nonprofit')
@login_required
def nonprofit():
	return render_template('nonprofit.html')

@main.route('/nonprofit', methods=['POST'])
@login_required
def nonprofit_post():
	nonprofit = request.form.get('nonprofit')

	user = current_user
	user.nonprofit = nonprofit
	db.session.commit()

	return redirect(url_for('main.profile'))

