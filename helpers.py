from functools import wraps
from flask import session, redirect, url_for, flash, Response
import csv
import io


def login_required(f):
    """
    Decorator to require login before accessing a route.
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            flash("Please login first.", "warning")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)

    return decorated_function


def format_currency(amount):
    """
    Format number as currency.
    Example:
    1200 -> ₹1,200.00
    """
    try:
        return f"₹{float(amount):,.2f}"
    except (TypeError, ValueError):
        return "₹0.00"


def export_to_csv(filename, headers, rows):
    """
    Generate CSV file for download.

    filename : inventory.csv
    headers  : ["ID", "Name", ...]
    rows     : list of tuples or sqlite rows
    """

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow(headers)

    for row in rows:
        if hasattr(row, "keys"):
            writer.writerow([row[key] for key in row.keys()])
        else:
            writer.writerow(row)

    csv_data = output.getvalue()
    output.close()

    return Response(
        csv_data,
        mimetype="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename={filename}"
        },
    )


def search_query(base_query, keyword, columns):
    """
    Create SQL search query.

    Example:

    search_query(
        "SELECT * FROM products",
        keyword,
        ["name"]
    )

    Returns:
    query, parameters
    """

    if keyword:
        conditions = " OR ".join(
            [f"{column} LIKE ?" for column in columns]
        )

        query = f"{base_query} WHERE {conditions}"
        params = tuple(f"%{keyword}%" for _ in columns)

        return query, params

    return base_query, ()


def calculate_sale_total(quantity, price):
    """
    Calculate total sale amount.
    """

    try:
        return float(quantity) * float(price)
    except (TypeError, ValueError):
        return 0.0


def validate_positive_number(value):
    """
    Check if value is a positive number.
    """

    try:
        return float(value) >= 0
    except (TypeError, ValueError):
        return False


def validate_positive_integer(value):
    """
    Check if value is a positive integer.
    """

    try:
        return int(value) >= 0
    except (TypeError, ValueError):
        return False
