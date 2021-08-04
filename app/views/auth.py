from flask import render_template, request, Blueprint, flash, redirect, url_for
from flask_login import login_user
from werkzeug.security import check_password_hash

from app import app
import app.models.users as users_model


bp = Blueprint("auth", __name__)


@bp.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "GET":
        return render_template("admin/../templates/login.html")
    else:
        user = users_model.get_by_email(request.form["email"])
        if not user or not check_password_hash(user["password"], request.form["password"]):
            flash("Email or password is incorrect", 'error')
            return render_template("admin/../templates/login.html")
        login_user(users_model.load_user(user["id"]))
        return redirect(url_for("service.admin_services_management"))


@bp.route("/logout")
def logout():
    return "Logout"
