from flask import Flask
from flask_session import Session

from database import init_db

from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.products import products_bp
from routes.categories import categories_bp
from routes.suppliers import suppliers_bp
from routes.sales import sales_bp


app = Flask(__name__)

app.config["SECRET_KEY"] = "inventory-secret-key"

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)

init_db()

app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(products_bp)
app.register_blueprint(categories_bp)
app.register_blueprint(suppliers_bp)
app.register_blueprint(sales_bp)


if __name__ == "__main__":
    app.run(debug=True)
