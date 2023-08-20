from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, login_user, logout_user, current_user
from .models import User
from . import db
from werkzeug.security import check_password_hash, generate_password_hash

auth = Blueprint(name="auth", import_name=__name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
	if request.method == "POST":
		email = request.form.get("email")
		password = request.form.get("password")

		user = User.query.filter_by(email=email).first()

		if user:
			if check_password_hash(user.password, password):
				login_user(user, remember=True)

				flash(
					f"Hello {user.username} !", category="success")
				return redirect(url_for("password.manager"))

			else:
				flash(f"Incorrect password for {user.email}", category="error")
				return redirect(url_for("auth.login"))

		else:
			flash(f"Email does not exists", category="error")
			return redirect(url_for("auth.login"))

	if current_user.is_authenticated:
		flash('You Already Logged in!', category='info')
		return redirect(url_for('views.index'))

	return render_template("login.html", user=current_user)


@auth.route("/register", methods=["GET", "POST"])
def register():
	if request.method == "POST":
		username = request.form.get("username")
		email = request.form.get("email")
		password = request.form.get("password")
		confirm_password = request.form.get("confirm-password")

		user = User.query.filter_by(email=email).first()
		user_ = User.query.filter_by(username=username).first()

		if user:
			flash("Email Already Exists", category="error")
		if user_:
			flash("Username Already Exists", category="error")

		elif len(password) < 8:
			flash("Too short password", category="error")

		elif confirm_password != password:
			flash("Passwords does not match", category="error")

		else:
			entry = User(email=email, username=username, password=generate_password_hash(
				confirm_password, method="sha256"))
			db.session.add(entry)
			db.session.commit()

			user = User.query.filter_by(email=email).first()
			login_user(user, remember=True)

			flash(
				"Account created!",
				category="success"
			)

			return redirect(url_for("password.manager"))

	if current_user.is_authenticated:
		flash('You Already Logged in!', category='info')
		return redirect(url_for('views.index'))

	return render_template("register.html", user=current_user)


@auth.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
	logout_user()
	return redirect(url_for("auth.login"))
