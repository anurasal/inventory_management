from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

from database import get_db_connection

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if session.get("user_id"):
        return redirect(url_for("dashboard.dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        confirmation = request.form.get("confirmation", "")

        if not username:
            flash("Username is required.", "danger")
            return render_template("register.html")

        if not password:
            flash("Password is required.", "danger")
            return render_template("register.html")

        if password != confirmation:
            flash("Passwords do not match.", "danger")
            return render_template("register.html")

        conn = get_db_connection()
        cursor = conn.cursor()

        existing = cursor.execute(
            "SELECT id FROM users WHERE username = ?",
            (username,)
        ).fetchone()

        if existing:
            conn.close()
            flash("Username already exists.", "danger")
            return render_template("register.html")

        hashed_password = generate_password_hash(password)

        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hashed_password)
        )

        conn.commit()
        conn.close()

        flash("Registration successful. Please login.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not username:
            flash("Username is required.", "danger")
            return render_template("login.html")

        if not password:
            flash("Password is required.", "danger")
            return render_template("login.html")

        conn = get_db_connection()
        cursor = conn.cursor()

        user = cursor.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        ).fetchone()

        conn.close()

        if user is None or not check_password_hash(user["password"], password):
            flash("Invalid username or password.", "danger")
            return render_template("login.html")

        session["user_id"] = user["id"]
        session["username"] = user["username"]

        flash(f"Welcome, {user['username']}!", "success")
        return redirect(url_for("dashboard.dashboard"))

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))
