from flask import Blueprint, render_template, request, redirect, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

from database import db


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            flash("Username required")
            return redirect("/register")

        if not password:
            flash("Password required")
            return redirect("/register")

        if password != confirmation:
            flash("Passwords do not match")
            return redirect("/register")

        existing = db.execute(
            "SELECT * FROM users WHERE username = ?",
            username
        )

        if existing:
            flash("Username already exists")
            return redirect("/register")

        hash_password = generate_password_hash(password)

        db.execute(
            """
            INSERT INTO users(username, hash)
            VALUES(?, ?)
            """,
            username,
            hash_password
        )

        flash("Registration Successful")
        return redirect("/login")

    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    session.clear()

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        if not username:
            flash("Username required")
            return redirect("/login")

        if not password:
            flash("Password required")
            return redirect("/login")

        rows = db.execute(
            "SELECT * FROM users WHERE username = ?",
            username
        )

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            flash("Invalid username or password")
            return redirect("/login")

        session["user_id"] = rows[0]["id"]
        session["username"] = rows[0]["username"]

        return redirect("/")

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():

    session.clear()

    return redirect("/login")
