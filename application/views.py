from flask import render_template, Blueprint
from flask_login import current_user

views = Blueprint(name="views", import_name=__name__)

@views.route('/', methods=["GET"])
def index():
	# return '<a href="https://www.youtube.com/watch?v=sFUmPSyG61c&pp=ygUPcmljayByb2xsIGFuaW1l">Link</a>'
	return render_template("index.html", user=current_user)
