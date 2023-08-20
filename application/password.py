from flask import Blueprint, render_template, request, flash, redirect, url_for, send_file
from flask_login import current_user, login_required
from .modules.rsa_key import save_key
from .models import Password, User
from sqlalchemy import or_, and_
from . import db
import base64
import rsa

password = Blueprint(name="password", import_name=__name__)

@password.route('/set-key', methods=["POST"])
@login_required
def set_key():
	try:
		publicKey, privateKey = rsa.newkeys(512)

		User.query.filter_by(email=current_user.email).update(dict(
				public_key = publicKey.save_pkcs1()
			))
		db.session.commit()

		save_key(privateKey, current_user.username)
		flash('Created keys.', category='success')
	except:
		flash('Failed to create keys!', category='error')
		return redirect(url_for('views.index'))
	return redirect(url_for('password.manager'))

@password.route('/manager', methods=["GET", "POST"])
@login_required
def manager():
	if current_user.public_key != None:
		priv_key = rsa.PrivateKey.load_pkcs1(open(f'keys/{current_user.username}.key', 'rb').read())
		passwords = []
		for password in current_user.passwords:
			dec_password = decrypt(password.password, priv_key)
			passwords.append({"id":password.id,
								"url":password.url,
								"username": password.username,
								"email": password.email,
								"password": dec_password})
	else:
		passwords = []
	return render_template('password/manager.html', user=current_user, passwords = passwords)

@password.route('/manager/save', methods=["POST"])
@login_required
def manager_save():
	url = request.form.get("url")
	username = request.form.get("username")
	email = request.form.get("email")
	password = request.form.get("password")

	public_key = rsa.PublicKey.load_pkcs1(current_user.public_key)
	enc_password = encrypt(password, public_key)

	try:
		new_password = Password(url=url, username=username, 
								email=email, password=enc_password, user_id=current_user.id)
		db.session.add(new_password)
		db.session.commit()

		flash('Saved new password.', category="success")
		return redirect(url_for('password.manager'))

	except:
		flash('Could\'nt save password', category="error")
		return redirect(url_for('password.manager'))

@password.route('/manager/edit/<int:id>', methods=["GET", "POST"])
@login_required
def manager_edit(id):
	data = Password.query.filter_by(id=id)

	priv_key = rsa.PrivateKey.load_pkcs1(open(f'keys/{current_user.username}.key', 'rb').read())
	data_first = data.first()
	dec_password = decrypt(data_first.password, priv_key)

	data_ = {"id": data_first.id,
			"url":data_first.url,
			"username": data_first.username,
			"email": data_first.email,
			"password": dec_password}

	if request.method == "POST":
		url = request.form.get("url")
		username = request.form.get("username")
		email = request.form.get("email")
		password = request.form.get("password")

		public_key = rsa.PublicKey.load_pkcs1(current_user.public_key)
		enc_password = encrypt(password, public_key)

		if data.first().user_id == current_user.id:
			try:
				data.update(dict(
					url=url,
					username=username,
					email=email,
					password=enc_password
				))
				db.session.commit()
				flash("Password updated", category="success")
				return redirect(url_for("password.manager"))

			except:
				flash("Could'nt update password", category="error")
				return redirect(url_for("dashboard.manager"))
		else:
			return redirect(url_for("views.index"))

	return render_template('password/manager/edit.html', user = current_user, data=data_)

@password.route('/manager/search', methods=["POST"])
@login_required
def manager_search():
	search_option = int(request.form.get('search-option'))
	search_value = request.form.get('search-value')
	passwords = []
	data = None
	
	priv_key = rsa.PrivateKey.load_pkcs1(open(f'keys/{current_user.username}.key', 'rb').read())
	pub_key = rsa.PublicKey.load_pkcs1(current_user.public_key)

	if search_option == 0:
		data = Password.query.filter(and_(Password.id == int(search_value), Password.user_id == current_user.id)).first()

	elif search_option == 1:
		data = Password.query.filter(and_(Password.url.like(search_value + '%'), Password.user_id == current_user.id)).all()

	elif search_option == 2:
		data = Password.query.filter(and_(Password.username.like(search_value + '%'), Password.user_id == current_user.id)).all()

	elif search_option == 3:
		data = Password.query.filter(and_(Password.email.like(search_value + '%'), Password.user_id == current_user.id)).all()

	elif search_option == 4:
		data = Password.query.filter(and_(or_(Password.url.like(search_value + '%'), Password.username.like(search_value + '%'), Password.email.like(search_value + '%')), Password.user_id == current_user.id)).all()

	if isinstance(data, list):
		for password in data:
			print(password.password)
			dec_password = decrypt(password.password, priv_key)
			passwords.append({"id":password.id,
								"url":password.url,
								"username": password.username,
								"email": password.email,
								"password": dec_password})
	else:
		dec_password = decrypt(data.password, priv_key)
		passwords.append({"id":data.id,
								"url":data.url,
								"username": data.username,
								"email": data.email,
								"password": dec_password})

	return render_template('password/manager/search.html', user = current_user, data = passwords, search_option = search_option, search_value = search_value )

@password.route("/manager/delete/<int:id>", methods=["GET", "POST"])
@login_required
def delete(id):
	password = Password.query.filter_by(id=id).first()

	if password.user_id == current_user.id:

		try:
			db.session.delete(password)
			db.session.commit()
			flash("Password deleted", category="success")
			return redirect(url_for("password.manager"))

		except:
			flash("Couldnt delete password", category="error")
			return redirect(url_for("password.manager"))

	else:
		return redirect("views.index")

@password.route('/generator', methods=["GET", "POST"])
@login_required
def generator():
	if request.method == "POST":
		pass
	return render_template('password/generator.html', user=current_user)

@password.route('/checker', methods=["GET", "POST"])
@login_required
def checker():
	if request.method == "POST":
		pass
	return render_template('password/checker.html', user=current_user)

def encrypt(text, pub_key):
	return base64.b64encode(rsa.encrypt(text.encode(), pub_key)).decode()

def decrypt(text, priv_key):
	return rsa.decrypt(base64.b64decode(text), priv_key).decode()