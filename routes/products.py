from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from database import get_db_connection
from helpers import login_required, export_to_csv, validate_positive_integer, validate_positive_number


products_bp = Blueprint(
    "products",
    __name__,
    url_prefix="/products"
)


@products_bp.route("/")
@login_required
def index():

    conn = get_db_connection()
    cursor = conn.cursor()

    search = request.args.get("search", "").strip()

    if search:

        products = cursor.execute(
            """
            SELECT
                products.*,
                categories.name AS category_name,
                suppliers.name AS supplier_name

            FROM products

            LEFT JOIN categories
                ON products.category_id = categories.id

            LEFT JOIN suppliers
                ON products.supplier_id = suppliers.id

            WHERE products.name LIKE ?

            ORDER BY products.id DESC
            """,
            (f"%{search}%",)
        ).fetchall()

    else:

        products = cursor.execute(
            """
            SELECT
                products.*,
                categories.name AS category_name,
                suppliers.name AS supplier_name

            FROM products

            LEFT JOIN categories
                ON products.category_id = categories.id

            LEFT JOIN suppliers
                ON products.supplier_id = suppliers.id

            ORDER BY products.id DESC
            """
        ).fetchall()


    conn.close()

    return render_template(
        "products/index.html",
        products=products,
        search=search
    )



@products_bp.route("/add", methods=["GET", "POST"])
@login_required
def add():

    conn = get_db_connection()
    cursor = conn.cursor()

    categories = cursor.execute(
        "SELECT * FROM categories ORDER BY name"
    ).fetchall()

    suppliers = cursor.execute(
        "SELECT * FROM suppliers ORDER BY name"
    ).fetchall()


    if request.method == "POST":

        name = request.form.get("name", "").strip()
        category_id = request.form.get("category_id")
        supplier_id = request.form.get("supplier_id")

        quantity = request.form.get("quantity")
        purchase_price = request.form.get("purchase_price")
        selling_price = request.form.get("selling_price")


        if not name:

            conn.close()

            flash(
                "Product name is required.",
                "danger"
            )

            return render_template(
                "products/add.html",
                categories=categories,
                suppliers=suppliers
            )


        if not validate_positive_integer(quantity):

            conn.close()

            flash(
                "Quantity must be a valid positive number.",
                "danger"
            )

            return render_template(
                "products/add.html",
                categories=categories,
                suppliers=suppliers
            )


        if not validate_positive_number(purchase_price) or not validate_positive_number(selling_price):

            conn.close()

            flash(
                "Prices must be valid numbers.",
                "danger"
            )

            return render_template(
                "products/add.html",
                categories=categories,
                suppliers=suppliers
            )


        cursor.execute(
            """
            INSERT INTO products
            (
                name,
                category_id,
                supplier_id,
                quantity,
                purchase_price,
                selling_price
            )

            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                name,
                category_id,
                supplier_id,
                quantity,
                purchase_price,
                selling_price
            )
        )


        conn.commit()
        conn.close()


        flash(
            "Product added successfully.",
            "success"
        )

        return redirect(
            url_for("products.index")
        )


    conn.close()


    return render_template(
        "products/add.html",
        categories=categories,
        suppliers=suppliers
    )



@products_bp.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit(id):

    conn = get_db_connection()
    cursor = conn.cursor()


    product = cursor.execute(
        """
        SELECT *
        FROM products
        WHERE id=?
        """,
        (id,)
    ).fetchone()


    if product is None:

        conn.close()

        flash(
            "Product not found.",
            "danger"
        )

        return redirect(
            url_for("products.index")
        )


    categories = cursor.execute(
        "SELECT * FROM categories ORDER BY name"
    ).fetchall()


    suppliers = cursor.execute(
        "SELECT * FROM suppliers ORDER BY name"
    ).fetchall()



    if request.method == "POST":

        name = request.form.get("name", "").strip()
        category_id = request.form.get("category_id")
        supplier_id = request.form.get("supplier_id")

        quantity = request.form.get("quantity")
        purchase_price = request.form.get("purchase_price")
        selling_price = request.form.get("selling_price")


        cursor.execute(
            """
            UPDATE products

            SET
                name=?,
                category_id=?,
                supplier_id=?,
                quantity=?,
                purchase_price=?,
                selling_price=?

            WHERE id=?
            """,
            (
                name,
                category_id,
                supplier_id,
                quantity,
                purchase_price,
                selling_price,
                id
            )
        )


        conn.commit()
        conn.close()


        flash(
            "Product updated successfully.",
            "success"
        )

        return redirect(
            url_for("products.index")
        )


    conn.close()


    return render_template(
        "products/edit.html",
        product=product,
        categories=categories,
        suppliers=suppliers
    )



@products_bp.route("/delete/<int:id>", methods=["POST"])
@login_required
def delete(id):

    conn = get_db_connection()
    cursor = conn.cursor()


    cursor.execute(
        """
        DELETE FROM products
        WHERE id=?
        """,
        (id,)
    )


    conn.commit()
    conn.close()


    flash(
        "Product deleted successfully.",
        "success"
    )


    return redirect(
        url_for("products.index")
    )



@products_bp.route("/export")
@login_required
def export_csv():

    conn = get_db_connection()


    products = conn.execute(
        """
        SELECT
            products.id,
            products.name,
            categories.name AS category,
            suppliers.name AS supplier,
            products.quantity,
            products.purchase_price,
            products.selling_price

        FROM products

        LEFT JOIN categories
            ON products.category_id = categories.id

        LEFT JOIN suppliers
            ON products.supplier_id = suppliers.id

        ORDER BY products.id
        """
    ).fetchall()


    conn.close()


    headers = [
        "ID",
        "Product",
        "Category",
        "Supplier",
        "Quantity",
        "Purchase Price",
        "Selling Price"
    ]


    rows = [
        (
            p["id"],
            p["name"],
            p["category"],
            p["supplier"],
            p["quantity"],
            p["purchase_price"],
            p["selling_price"]
        )
        for p in products
    ]


    return export_to_csv(
        "products.csv",
        headers,
        rows
    )
