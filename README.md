# Inventory Management System

#### Video Demo:


#### GitHub Repository:
https://github.com/anurasal/inventory_management

#### Description:

Inventory Management System is a web-based application built using Flask and SQLite.

The purpose of this project is to help small businesses manage their inventory, products, suppliers, categories, and sales records from a single dashboard.

The application provides authentication, CRUD operations, stock tracking, search functionality, and CSV export features.

I created this project because many small businesses still manage inventory manually, which can lead to stock errors and difficulty tracking sales. This application provides a simple digital solution for managing daily inventory operations.

---

## Features

### User Authentication

- User registration
- User login
- User logout
- Session-based authentication

### Dashboard

- Total products count
- Total categories count
- Total suppliers count
- Total sales count
- Total stock overview
- Revenue summary
- Recent sales display
- Low stock product alerts
- Sales overview chart

### Product Management

- Add products
- View products
- Edit products
- Delete products
- Search products
- Export products as CSV

Each product contains:

- Product name
- Category
- Supplier
- Quantity
- Purchase price
- Selling price

### Category Management

- Add categories
- View categories
- Edit categories
- Delete categories
- Search categories
- Export categories as CSV

### Supplier Management

- Add suppliers
- View suppliers
- Edit suppliers
- Delete suppliers
- Search suppliers
- Export suppliers as CSV

Supplier details include:

- Supplier name
- Contact person
- Phone number
- Email
- Address

### Sales Management

- Record sales
- Automatically update stock quantity
- View sales history
- Delete sales
- Restore stock after deleting sales
- Export sales as CSV

---

# Technologies Used

- Python
- Flask
- SQLite
- HTML
- CSS
- JavaScript
- Bootstrap 5
- Jinja2 Templates

---

# Project Structure

```text
inventory_management/

├── app.py
├── database.py
├── helpers.py
├── requirements.txt
├── README.md

├── routes/
│   ├── auth.py
│   ├── dashboard.py
│   ├── categories.py
│   ├── suppliers.py
│   ├── products.py
│   └── sales.py

├── templates/
│   ├── layout.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   │
│   ├── categories/
│   │   ├── index.html
│   │   ├── add.html
│   │   └── edit.html
│   │
│   ├── suppliers/
│   │   ├── index.html
│   │   ├── add.html
│   │   └── edit.html
│   │
│   ├── products/
│   │   ├── index.html
│   │   ├── add.html
│   │   └── edit.html
│   │
│   └── sales/
│       ├── index.html
│       └── add.html

└── static/
    ├── css/
    │   └── style.css
    │
    └── js/
        └── script.js
```

---

# Installation

Clone the repository:

```bash
git clone https://github.com/anurasal/inventory_management.git
```

Go inside the project folder:

```bash
cd inventory_management
```

Install required packages:

```bash
pip install -r requirements.txt
```

---

# Running the Application

Start Flask server:

```bash
flask run
```

Open your browser and visit:

```
http://127.0.0.1:5000
```

---

# Database

The project uses SQLite database.

Database tables:

## users

Stores registered user accounts.

## products

Stores inventory product information.

Includes:

- Product name
- Category
- Supplier
- Quantity
- Purchase price
- Selling price

## categories

Stores product categories.

## suppliers

Stores supplier information.

Includes:

- Supplier name
- Contact person
- Phone
- Email
- Address

## sales

Stores sales transactions.

Includes:

- Product sold
- Quantity
- Selling price
- Total amount
- Sale date

---

# Design Decisions

Blueprints were used to organize the Flask application into separate modules.

SQLite was selected because it is lightweight, easy to manage, and suitable for a small inventory management application.

The application automatically updates product stock when sales are recorded to maintain accurate inventory information.

---

# Validation

The application validates:

- Required form fields
- Duplicate category names
- Duplicate supplier names
- Product quantities
- Product prices
- Available stock before completing sales

---

# Future Improvements

Possible improvements:

- User roles (Admin/Employee)
- Product images
- Low-stock notifications
- Advanced sales analytics
- Barcode scanning
- Cloud database support
- Invoice generation

---

# Author

Anushka Rasal

CS50 Final Project
