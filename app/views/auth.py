from flask import render_template, request, Blueprint, flash, redirect, url_for
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash

import app.models.users as users_model


bp = Blueprint("auth", __name__)


@bp.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        user = users_model.get_by_username(request.form["username"])

        if not user or not check_password_hash(
            user["password"], request.form["password"]
        ):
            flash("Username or password is incorrect", "error")
            return render_template("login.html")

        # if ther user check on the "Remember me" box.
        # The "rememberme" key will be incluced in request form
        remember = "rememberme" in request.form
        login_user(users_model.load_user(user["id"]), remember=remember)

        return redirect(url_for("service.admin_services_management"))


@bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
