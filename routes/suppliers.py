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

suppliers_bp = Blueprint(
    "suppliers",
    __name__,
    url_prefix="/suppliers"
)


@suppliers_bp.route("/")
@login_required
def index():

    conn = get_db_connection()
    cursor = conn.cursor()

    search = request.args.get("search", "").strip()

    if search:
        suppliers = cursor.execute(
            """
            SELECT *
            FROM suppliers
            WHERE
                name LIKE ?
                OR contact_person LIKE ?
                OR phone LIKE ?
                OR email LIKE ?
            ORDER BY id DESC
            """,
            (
                f"%{search}%",
                f"%{search}%",
                f"%{search}%",
                f"%{search}%"
            )
        ).fetchall()
    else:
        suppliers = cursor.execute(
            """
            SELECT *
            FROM suppliers
            ORDER BY id DESC
            """
        ).fetchall()

    conn.close()

    return render_template(
        "suppliers/index.html",
        suppliers=suppliers,
        search=search
    )


@suppliers_bp.route("/add", methods=["GET", "POST"])
@login_required
def add():

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        contact_person = request.form.get("contact_person", "").strip()
        phone = request.form.get("phone", "").strip()
        email = request.form.get("email", "").strip()
        address = request.form.get("address", "").strip()

        if not name:
            flash("Supplier name is required.", "danger")
            return render_template("suppliers/add.html")

        conn = get_db_connection()
        cursor = conn.cursor()

        exists = cursor.execute(
            "SELECT id FROM suppliers WHERE name=?",
            (name,)
        ).fetchone()

        if exists:
            conn.close()
            flash("Supplier already exists.", "warning")
            return render_template("suppliers/add.html")

        cursor.execute(
            """
            INSERT INTO suppliers
            (
                name,
                contact_person,
                phone,
                email,
                address
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                name,
                contact_person,
                phone,
                email,
                address
            )
        )

        conn.commit()
        conn.close()

        flash("Supplier added successfully.", "success")
        return redirect(url_for("suppliers.index"))

    return render_template("suppliers/add.html")


@suppliers_bp.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit(id):

    conn = get_db_connection()
    cursor = conn.cursor()

    supplier = cursor.execute(
        "SELECT * FROM suppliers WHERE id=?",
        (id,)
    ).fetchone()

    if supplier is None:
        conn.close()
        flash("Supplier not found.", "danger")
        return redirect(url_for("suppliers.index"))

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        contact_person = request.form.get("contact_person", "").strip()
        phone = request.form.get("phone", "").strip()
        email = request.form.get("email", "").strip()
        address = request.form.get("address", "").strip()

        if not name:
            conn.close()
            flash("Supplier name is required.", "danger")
            return render_template(
                "suppliers/edit.html",
                supplier=supplier
            )

        duplicate = cursor.execute(
            """
            SELECT id
            FROM suppliers
            WHERE name=?
            AND id != ?
            """,
            (name, id)
        ).fetchone()

        if duplicate:
            conn.close()
            flash("Supplier already exists.", "warning")
            return render_template(
                "suppliers/edit.html",
                supplier=supplier
            )

        cursor.execute(
            """
            UPDATE suppliers
            SET
                name=?,
                contact_person=?,
                phone=?,
                email=?,
                address=?
            WHERE id=?
            """,
            (
                name,
                contact_person,
                phone,
                email,
                address,
                id
            )
        )

        conn.commit()
        conn.close()

        flash("Supplier updated successfully.", "success")
        return redirect(url_for("suppliers.index"))

    conn.close()

    return render_template(
        "suppliers/edit.html",
        supplier=supplier
    )


@suppliers_bp.route("/delete/<int:id>", methods=["POST"])
@login_required
def delete(id):

    conn = get_db_connection()
    cursor = conn.cursor()

    supplier = cursor.execute(
        "SELECT id FROM suppliers WHERE id=?",
        (id,)
    ).fetchone()

    if supplier is None:
        conn.close()
        flash("Supplier not found.", "danger")
        return redirect(url_for("suppliers.index"))

    cursor.execute(
        "DELETE FROM suppliers WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    flash("Supplier deleted successfully.", "success")
    return redirect(url_for("suppliers.index"))


@suppliers_bp.route("/export")
@login_required
def export_csv():

    conn = get_db_connection()

    suppliers = conn.execute(
        """
        SELECT
            id,
            name,
            contact_person,
            phone,
            email,
            address,
            created_at
        FROM suppliers
        ORDER BY id
        """
    ).fetchall()

    conn.close()

    headers = [
        "ID",
        "Name",
        "Contact Person",
        "Phone",
        "Email",
        "Address",
        "Created At"
    ]

    rows = [
        (
            s["id"],
            s["name"],
            s["contact_person"],
            s["phone"],
            s["email"],
            s["address"],
            s["created_at"]
        )
        for s in suppliers
    ]

    return export_to_csv(
        "suppliers.csv",
        headers,
        rows
    )
