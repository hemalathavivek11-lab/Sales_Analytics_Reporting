import sqlite3

DATABASE = "sales_analytics.db"

connection = sqlite3.connect(DATABASE)
cursor = connection.cursor()

print("\n========== SALES ANALYTICS ==========\n")

# 1. Total Revenue
cursor.execute("""
SELECT COALESCE(SUM(total_amount), 0)
FROM orders
WHERE status = 'COMPLETED'
""")

print("Total Revenue:", cursor.fetchone()[0])


# 2. Total Orders
cursor.execute("""
SELECT COUNT(*)
FROM orders
""")

print("Total Orders:", cursor.fetchone()[0])


# 3. Average Order Value
cursor.execute("""
SELECT ROUND(AVG(total_amount), 2)
FROM orders
WHERE status = 'COMPLETED'
""")

print("Average Order Value:", cursor.fetchone()[0])


# 4. Sales by Customer
print("\n--- Sales by Customer ---")

cursor.execute("""
SELECT
    c.name,
    COUNT(o.order_id) AS orders,
    COALESCE(SUM(o.total_amount), 0) AS revenue
FROM customers c
LEFT JOIN orders o
    ON c.customer_id = o.customer_id
    AND o.status = 'COMPLETED'
GROUP BY c.customer_id, c.name
ORDER BY revenue DESC
""")

for row in cursor.fetchall():
    print(row)


# 5. Top Products
print("\n--- Top Products ---")

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

for row in cursor.fetchall():
    print(row)


# 6. Sales by Category
print("\n--- Sales by Category ---")

cursor.execute("""
SELECT
    p.category,
    SUM(oi.quantity * oi.unit_price) AS revenue
FROM order_items oi
JOIN products p
    ON oi.product_id = p.product_id
JOIN orders o
    ON oi.order_id = o.order_id
WHERE o.status = 'COMPLETED'
GROUP BY p.category
ORDER BY revenue DESC
""")

for row in cursor.fetchall():
    print(row)


# 7. Monthly Sales
print("\n--- Monthly Sales ---")

cursor.execute("""
SELECT
    strftime('%Y-%m', order_date) AS month,
    SUM(total_amount) AS revenue
FROM orders
WHERE status = 'COMPLETED'
GROUP BY month
ORDER BY month
""")

for row in cursor.fetchall():
    print(row)


# 8. Order Status
print("\n--- Order Status ---")

cursor.execute("""
SELECT status, COUNT(*)
FROM orders
GROUP BY status
ORDER BY COUNT(*) DESC
""")

for row in cursor.fetchall():
    print(row)


# 9. Payment Status
print("\n--- Payment Status ---")

cursor.execute("""
SELECT payment_status, COUNT(*)
FROM payments
GROUP BY payment_status
ORDER BY COUNT(*) DESC
""")

for row in cursor.fetchall():
    print(row)


# 10. Customers with sales above 30000
print("\n--- High Value Customers ---")

cursor.execute("""
SELECT
    c.name,
    SUM(o.total_amount) AS revenue
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
WHERE o.status = 'COMPLETED'
GROUP BY c.customer_id, c.name
HAVING SUM(o.total_amount) > 30000
ORDER BY revenue DESC
""")

for row in cursor.fetchall():
    print(row)


# 11. Repeat Customers
print("\n--- Repeat Customers ---")

cursor.execute("""
SELECT
    c.name,
    COUNT(o.order_id) AS order_count
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
WHERE o.status = 'COMPLETED'
GROUP BY c.customer_id, c.name
HAVING COUNT(o.order_id) > 1
ORDER BY order_count DESC
""")

for row in cursor.fetchall():
    print(row)


connection.close()

print("\nAnalytics completed successfully!")