from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from database import get_db_connection
from helpers import login_required, export_to_csv

categories_bp = Blueprint("categories", __name__, url_prefix="/categories")


@categories_bp.route("/")
@login_required
def index():
    conn = get_db_connection()
    cursor = conn.cursor()

    search = request.args.get("search", "").strip()

    if search:
        categories = cursor.execute(
            """
            SELECT *
            FROM categories
            WHERE name LIKE ?
            ORDER BY id DESC
            """,
            (f"%{search}%",)
        ).fetchall()
    else:
        categories = cursor.execute(
            """
            SELECT *
            FROM categories
            ORDER BY id DESC
            """
        ).fetchall()

    conn.close()

    return render_template(
        "categories/index.html",
        categories=categories,
        search=search
    )


@categories_bp.route("/add", methods=["GET", "POST"])
@login_required
def add():

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()

        if not name:
            flash("Category name is required.", "danger")
            return render_template("categories/add.html")

        conn = get_db_connection()
        cursor = conn.cursor()

        exists = cursor.execute(
            "SELECT id FROM categories WHERE name=?",
            (name,)
        ).fetchone()

        if exists:
            conn.close()
            flash("Category already exists.", "warning")
            return render_template("categories/add.html")

        cursor.execute(
            """
            INSERT INTO categories(name, description)
            VALUES(?, ?)
            """,
            (name, description)
        )

        conn.commit()
        conn.close()

        flash("Category added successfully.", "success")
        return redirect(url_for("categories.index"))

    return render_template("categories/add.html")


@categories_bp.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit(id):

    conn = get_db_connection()
    cursor = conn.cursor()

    category = cursor.execute(
        "SELECT * FROM categories WHERE id=?",
        (id,)
    ).fetchone()

    if category is None:
        conn.close()
        flash("Category not found.", "danger")
        return redirect(url_for("categories.index"))

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()

        if not name:
            conn.close()
            flash("Category name is required.", "danger")
            return render_template(
                "categories/edit.html",
                category=category
            )

        duplicate = cursor.execute(
            """
            SELECT id
            FROM categories
            WHERE name=?
            AND id != ?
            """,
            (name, id)
        ).fetchone()

        if duplicate:
            conn.close()
            flash("Category already exists.", "warning")
            return render_template(
                "categories/edit.html",
                category=category
            )

        cursor.execute(
            """
            UPDATE categories
            SET
                name=?,
                description=?
            WHERE id=?
            """,
            (name, description, id)
        )

        conn.commit()
        conn.close()

        flash("Category updated successfully.", "success")
        return redirect(url_for("categories.index"))

    conn.close()

    return render_template(
        "categories/edit.html",
        category=category
    )


@categories_bp.route("/delete/<int:id>", methods=["POST"])
@login_required
def delete(id):

    conn = get_db_connection()
    cursor = conn.cursor()

    category = cursor.execute(
        "SELECT id FROM categories WHERE id=?",
        (id,)
    ).fetchone()

    if category is None:
        conn.close()
        flash("Category not found.", "danger")
        return redirect(url_for("categories.index"))

    cursor.execute(
        "DELETE FROM categories WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    flash("Category deleted successfully.", "success")
    return redirect(url_for("categories.index"))


@categories_bp.route("/export")
@login_required
def export_csv():

    conn = get_db_connection()

    categories = conn.execute(
        """
        SELECT
            id,
            name,
            description,
            created_at
        FROM categories
        ORDER BY id
        """
    ).fetchall()

    conn.close()

    headers = [
        "ID",
        "Name",
        "Description",
        "Created At"
    ]

    rows = [
        (
            c["id"],
            c["name"],
            c["description"],
            c["created_at"]
        )
        for c in categories
    ]

    return export_to_csv(
        "categories.csv",
        headers,
        rows
    )
