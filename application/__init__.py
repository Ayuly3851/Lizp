from flask import Flask, redirect, url_for, flash, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
import os

db_name = "lizp.db"
db = SQLAlchemy()

def create_app():
	app = Flask(__name__)
	app.config["SECRET_KEY"] = "wdwdlw wkdwkdn"
	app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_name}"
	
	db.init_app(app=app)
	from .views import views
	from .auth import auth
	from .account import account
	from .password import password
	
	app.register_blueprint(views, url_prefix="/")
	app.register_blueprint(account, url_prefix="/account")
	app.register_blueprint(auth, url_prefix="/")
	app.register_blueprint(password, url_prefix="/password")

	@app.errorhandler(404)
	def not_found(e):
		return render_template('error/404.html', user = current_user)

	from .models import User, Password
	create_db(app=app)

	login_manager = LoginManager()
	login_manager.init_app(app)

	@login_manager.unauthorized_handler
	def to_login():
		flash("Login To Access Feauture", category="warning")
		return redirect(url_for("auth.login"))

	@login_manager.user_loader
	def load_user(id):
		return User.query.get(id)

	return app

def create_db(app):
    if not os.path.exists(os.path.join("instance", db_name)):
        with app.app_context():
            db.create_all()
        print("DB Created Successfully")