from flask import Flask, render_template, jsonify
import sqlite3

app = Flask(__name__, static_folder="statics", static_url_path="/static")

DATABASE = "sales_analytics.db"


def get_db():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/dashboard")
def dashboard():

    connection = get_db()
    cursor = connection.cursor()

    # Summary
    cursor.execute("""
        SELECT COALESCE(SUM(total_amount), 0) AS revenue
        FROM orders
        WHERE status = 'COMPLETED'
    """)
    revenue = cursor.fetchone()["revenue"]

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM orders
    """)
    orders = cursor.fetchone()["total"]

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM customers
    """)
    customers = cursor.fetchone()["total"]

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM products
    """)
    products = cursor.fetchone()["total"]

    # Monthly Sales
    cursor.execute("""
        SELECT
            strftime('%Y-%m', order_date) AS month,
            SUM(total_amount) AS revenue
        FROM orders
        WHERE status = 'COMPLETED'
        GROUP BY month
        ORDER BY month
    """)

    monthly_sales = [dict(row) for row in cursor.fetchall()]

    # Top Products
    cursor.execute("""
        SELECT
            p.product_name,
            SUM(oi.quantity) AS units_sold,
            SUM(oi.quantity * oi.unit_price) AS revenue
        FROM order_items oi
        JOIN products p
            ON oi.product_id = p.product_id
        JOIN orders o
            ON oi.order_id = o.order_id
        WHERE o.status = 'COMPLETED'
        GROUP BY p.product_id, p.product_name
        ORDER BY revenue DESC
        LIMIT 5
    """)

    top_products = [dict(row) for row in cursor.fetchall()]

    # Top Customers
    cursor.execute("""
        SELECT
            c.name,
            COALESCE(SUM(o.total_amount), 0) AS revenue
        FROM customers c
        LEFT JOIN orders o
            ON c.customer_id = o.customer_id
            AND o.status = 'COMPLETED'
        GROUP BY c.customer_id, c.name
        ORDER BY revenue DESC
        LIMIT 5
    """)

    top_customers = [dict(row) for row in cursor.fetchall()]

    # Order Status
    cursor.execute("""
        SELECT status, COUNT(*) AS count
        FROM orders
        GROUP BY status
        ORDER BY count DESC
    """)

    order_status = [dict(row) for row in cursor.fetchall()]

    # Payment Status
    cursor.execute("""
        SELECT payment_status, COUNT(*) AS count
        FROM payments
        GROUP BY payment_status
        ORDER BY count DESC
    """)

    payment_status = [dict(row) for row in cursor.fetchall()]

    # Recent Orders
    cursor.execute("""
        SELECT
            o.order_id,
            c.name AS customer_name,
            o.order_date,
            o.status,
            o.total_amount
        FROM orders o
        JOIN customers c
            ON o.customer_id = c.customer_id
        ORDER BY o.order_id DESC
        LIMIT 10
    """)

    recent_orders = [dict(row) for row in cursor.fetchall()]

    connection.close()

    return jsonify({
        "revenue": revenue,
        "orders": orders,
        "customers": customers,
        "products": products,
        "monthly_sales": monthly_sales,
        "top_products": top_products,
        "top_customers": top_customers,
        "order_status": order_status,
        "payment_status": payment_status,
        "recent_orders": recent_orders
    })


if __name__ == "__main__":
    app.run(debug=True)