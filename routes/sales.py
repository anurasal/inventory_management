from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from database import get_db_connection
from helpers import login_required, export_to_csv, calculate_sale_total


sales_bp = Blueprint(
    "sales",
    __name__,
    url_prefix="/sales"
)


@sales_bp.route("/")
@login_required
def index():

    conn = get_db_connection()
    cursor = conn.cursor()

    search = request.args.get("search", "").strip()


    if search:

        sales = cursor.execute(
            """
            SELECT
                sales.id,
                products.name AS product_name,
                sales.quantity,
                sales.selling_price,
                sales.total,
                sales.sold_at

            FROM sales

            JOIN products
                ON sales.product_id = products.id

            WHERE products.name LIKE ?

            ORDER BY sales.id DESC
            """,
            (f"%{search}%",)
        ).fetchall()


    else:

        sales = cursor.execute(
            """
            SELECT
                sales.id,
                products.name AS product_name,
                sales.quantity,
                sales.selling_price,
                sales.total,
                sales.sold_at

            FROM sales

            JOIN products
                ON sales.product_id = products.id

            ORDER BY sales.id DESC
            """
        ).fetchall()


    conn.close()


    return render_template(
        "sales/index.html",
        sales=sales,
        search=search
    )



@sales_bp.route("/add", methods=["GET", "POST"])
@login_required
def add():

    conn = get_db_connection()
    cursor = conn.cursor()


    products = cursor.execute(
        """
        SELECT *
        FROM products
        WHERE quantity > 0
        ORDER BY name
        """
    ).fetchall()



    if request.method == "POST":


        product_id = request.form.get("product_id")
        quantity = request.form.get("quantity")


        if not product_id or not quantity:

            conn.close()

            flash(
                "Product and quantity are required.",
                "danger"
            )

            return render_template(
                "sales/add.html",
                products=products
            )


        product = cursor.execute(
            """
            SELECT *
            FROM products
            WHERE id=?
            """,
            (product_id,)
        ).fetchone()



        if product is None:

            conn.close()

            flash(
                "Product not found.",
                "danger"
            )

            return redirect(
                url_for("sales.add")
            )



        quantity = int(quantity)



        if quantity <= 0:

            conn.close()

            flash(
                "Quantity must be greater than zero.",
                "danger"
            )

            return redirect(
                url_for("sales.add")
            )



        if quantity > product["quantity"]:

            conn.close()

            flash(
                "Not enough stock available.",
                "danger"
            )

            return redirect(
                url_for("sales.add")
            )



        total = calculate_sale_total(
            quantity,
            product["selling_price"]
        )



        cursor.execute(
            """
            INSERT INTO sales
            (
                product_id,
                quantity,
                selling_price,
                total
            )

            VALUES (?, ?, ?, ?)
            """,
            (
                product_id,
                quantity,
                product["selling_price"],
                total
            )
        )



        cursor.execute(
            """
            UPDATE products

            SET quantity = quantity - ?

            WHERE id=?
            """,
            (
                quantity,
                product_id
            )
        )



        conn.commit()
        conn.close()



        flash(
            "Sale recorded successfully.",
            "success"
        )


        return redirect(
            url_for("sales.index")
        )



    conn.close()


    return render_template(
        "sales/add.html",
        products=products
    )



@sales_bp.route("/delete/<int:id>", methods=["POST"])
@login_required
def delete(id):

    conn = get_db_connection()
    cursor = conn.cursor()



    sale = cursor.execute(
        """
        SELECT *
        FROM sales
        WHERE id=?
        """,
        (id,)
    ).fetchone()



    if sale is None:

        conn.close()

        flash(
            "Sale not found.",
            "danger"
        )

        return redirect(
            url_for("sales.index")
        )



    cursor.execute(
        """
        UPDATE products

        SET quantity = quantity + ?

        WHERE id=?
        """,
        (
            sale["quantity"],
            sale["product_id"]
        )
    )



    cursor.execute(
        """
        DELETE FROM sales
        WHERE id=?
        """,
        (id,)
    )



    conn.commit()
    conn.close()



    flash(
        "Sale deleted and stock restored.",
        "success"
    )


    return redirect(
        url_for("sales.index")
    )



@sales_bp.route("/export")
@login_required
def export_csv():

    conn = get_db_connection()


    sales = conn.execute(
        """
        SELECT

            sales.id,
            products.name AS product,
            sales.quantity,
            sales.selling_price,
            sales.total,
            sales.sold_at

        FROM sales

        JOIN products
            ON sales.product_id = products.id

        ORDER BY sales.id

        """
    ).fetchall()


    conn.close()



    headers = [
        "ID",
        "Product",
        "Quantity",
        "Selling Price",
        "Total",
        "Date"
    ]



    rows = [

        (
            s["id"],
            s["product"],
            s["quantity"],
            s["selling_price"],
            s["total"],
            s["sold_at"]
        )

        for s in sales

    ]



    return export_to_csv(
        "sales.csv",
        headers,
        rows
    )
