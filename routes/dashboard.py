from flask import Blueprint, render_template

from database import get_db_connection
from helpers import login_required

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
@login_required
def dashboard():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Total products
    total_products = cursor.execute(
        "SELECT COUNT(*) FROM products"
    ).fetchone()[0]

    # Total categories
    total_categories = cursor.execute(
        "SELECT COUNT(*) FROM categories"
    ).fetchone()[0]

    # Total suppliers
    total_suppliers = cursor.execute(
        "SELECT COUNT(*) FROM suppliers"
    ).fetchone()[0]

    # Total sales
    total_sales = cursor.execute(
        "SELECT COUNT(*) FROM sales"
    ).fetchone()[0]

    # Total revenue
    revenue = cursor.execute(
        "SELECT COALESCE(SUM(total), 0) FROM sales"
    ).fetchone()[0]

    # Total inventory quantity
    total_stock = cursor.execute(
        "SELECT COALESCE(SUM(quantity), 0) FROM products"
    ).fetchone()[0]

    # Inventory value (purchase price × quantity)
    inventory_value = cursor.execute(
        """
        SELECT COALESCE(
            SUM(quantity * purchase_price),
            0
        )
        FROM products
        """
    ).fetchone()[0]

    # Recent sales
    recent_sales = cursor.execute(
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
        ORDER BY sales.sold_at DESC
        LIMIT 5
        """
    ).fetchall()

    # Low stock products
    low_stock_products = cursor.execute(
        """
        SELECT name, quantity
        FROM products
        WHERE quantity <= 5
        ORDER BY quantity ASC
        """
    ).fetchall()

    conn.close()

    return render_template(
        "dashboard.html",
        total_products=total_products,
        total_categories=total_categories,
        total_suppliers=total_suppliers,
        total_sales=total_sales,
        total_stock=total_stock,
        revenue=revenue,
        inventory_value=inventory_value,
        recent_sales=recent_sales,
        low_stock_products=low_stock_products,
    )
