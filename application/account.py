from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required
from .models import User
from . import db
from werkzeug.security import check_password_hash, generate_password_hash

account = Blueprint(name="account", import_name=__name__)

@account.route('/view')
@login_required
def view():
	return render_template('account.html', user=current_user)