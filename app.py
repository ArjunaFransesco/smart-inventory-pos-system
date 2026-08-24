# -*- coding: utf-8 -*-
"""
Smart Inventory & Warehouse Point-of-Sale (POS) Web Application
Author: Arjuna Fransesco (https://github.com/ArjunaFransesco)
"""

import os
import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash

app = Flask(__name__, template_folder="app/templates", static_folder="app/static")
app.secret_key = "smart-inventory-secret-key-2026"

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "inventory_pos.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def dashboard():
    conn = get_db()
    cur = conn.cursor()
    
    total_products = cur.execute("SELECT COUNT(*) FROM products").fetchone()[0]
    total_stock_value = cur.execute("SELECT SUM(cost_price * stock_quantity) FROM products").fetchone()[0] or 0
    total_sales_today = cur.execute("SELECT SUM(total_amount) FROM transactions WHERE date(date) = date('now')").fetchone()[0] or 0
    low_stock_count = cur.execute("SELECT COUNT(*) FROM products WHERE stock_quantity <= min_reorder_level").fetchone()[0]
    
    low_stock_items = cur.execute("""
        SELECT p.*, c.name as category_name, s.name as supplier_name
        FROM products p
        JOIN categories c ON p.category_id = c.id
        JOIN suppliers s ON p.supplier_id = s.id
        WHERE p.stock_quantity <= p.min_reorder_level
        ORDER BY p.stock_quantity ASC
    """).fetchall()

    recent_transactions = cur.execute("""
        SELECT * FROM transactions ORDER BY date DESC LIMIT 5
    """).fetchall()

    conn.close()
    return render_template("dashboard.html", 
                           total_products=total_products,
                           total_stock_value=total_stock_value,
                           total_sales_today=total_sales_today,
                           low_stock_count=low_stock_count,
                           low_stock_items=low_stock_items,
                           recent_transactions=recent_transactions)

@app.route("/inventory")
def inventory():
    conn = get_db()
    cur = conn.cursor()
    products = cur.execute("""
        SELECT p.*, c.name as category_name, s.name as supplier_name
        FROM products p
        JOIN categories c ON p.category_id = c.id
        JOIN suppliers s ON p.supplier_id = s.id
        ORDER BY p.id DESC
    """).fetchall()
    categories = cur.execute("SELECT * FROM categories").fetchall()
    suppliers = cur.execute("SELECT * FROM suppliers").fetchall()
    conn.close()
    return render_template("inventory.html", products=products, categories=categories, suppliers=suppliers)

@app.route("/inventory/add", methods=["POST"])
def add_product():
    sku = request.form["sku"]
    name = request.form["name"]
    category_id = int(request.form["category_id"])
    supplier_id = int(request.form["supplier_id"])
    cost_price = float(request.form["cost_price"])
    selling_price = float(request.form["selling_price"])
    stock = int(request.form["stock_quantity"])
    min_reorder = int(request.form["min_reorder_level"])
    
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO products (sku, name, category_id, supplier_id, cost_price, selling_price, stock_quantity, min_reorder_level)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (sku, name, category_id, supplier_id, cost_price, selling_price, stock, min_reorder))
    conn.commit()
    conn.close()
    flash("Product successfully created!", "success")
    return redirect(url_for("inventory"))

@app.route("/pos")
def pos_terminal():
    conn = get_db()
    cur = conn.cursor()
    products = cur.execute("""
        SELECT p.*, c.name as category_name 
        FROM products p 
        JOIN categories c ON p.category_id = c.id 
        WHERE p.stock_quantity > 0
        ORDER BY p.name ASC
    """).fetchall()
    categories = cur.execute("SELECT * FROM categories").fetchall()
    conn.close()
    return render_template("pos.html", products=products, categories=categories)

@app.route("/api/pos/checkout", methods=["POST"])
def pos_checkout():
    data = request.get_json()
    items = data.get("items", [])
    payment_method = data.get("payment_method", "CASH")
    cashier = data.get("cashier_name", "Arjuna Fransesco")
    
    if not items:
        return jsonify({"success": False, "error": "Cart is empty"}), 400

    conn = get_db()
    cur = conn.cursor()
    total_amount = sum(item["price"] * item["qty"] for item in items)
    invoice_number = f"INV-{datetime.now().strftime('%Y%m%d%H%M%S')}"

    cur.execute("""
        INSERT INTO transactions (invoice_number, total_amount, payment_method, cashier_name)
        VALUES (?, ?, ?, ?)
    """, (invoice_number, total_amount, payment_method, cashier))
    txn_id = cur.lastrowid

    for it in items:
        cur.execute("""
            INSERT INTO transaction_items (transaction_id, product_id, quantity, unit_price, subtotal)
            VALUES (?, ?, ?, ?, ?)
        """, (txn_id, it["id"], it["qty"], it["price"], it["price"] * it["qty"]))
        
        cur.execute("UPDATE products SET stock_quantity = stock_quantity - ? WHERE id = ?", (it["qty"], it["id"]))

    conn.commit()
    conn.close()
    return jsonify({"success": True, "invoice": invoice_number, "total": total_amount})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
