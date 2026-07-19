import sqlite3


class Database:
    def __init__(self, database):
        self.database = database

    def execute(self, query, *args):
        conn = sqlite3.connect(self.database)
        conn.row_factory = sqlite3.Row

        cur = conn.cursor()
        cur.execute(query, args)

        conn.commit()

        if query.strip().upper().startswith("SELECT"):
            rows = cur.fetchall()
            conn.close()
            return rows

        lastrowid = cur.lastrowid
        conn.close()
        return lastrowid


db = Database("inventory.db")


def init_db():

    db.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        hash TEXT NOT NULL
    )
    """)

    db.execute("""
    CREATE TABLE IF NOT EXISTS categories(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL
    )
    """)

    db.execute("""
    CREATE TABLE IF NOT EXISTS suppliers(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT,
        email TEXT
    )
    """)

    db.execute("""
    CREATE TABLE IF NOT EXISTS products(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        sku TEXT UNIQUE,
        category_id INTEGER,
        supplier_id INTEGER,
        quantity INTEGER DEFAULT 0,
        buy_price REAL,
        sell_price REAL,
        FOREIGN KEY(category_id) REFERENCES categories(id),
        FOREIGN KEY(supplier_id) REFERENCES suppliers(id)
    )
    """)

    db.execute("""
    CREATE TABLE IF NOT EXISTS sales(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER,
        quantity INTEGER,
        sale_date TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(product_id) REFERENCES products(id)
    )
    """)
