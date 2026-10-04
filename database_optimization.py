import sqlite3

DATABASE = "sales_analytics.db"

connection = sqlite3.connect(DATABASE)
cursor = connection.cursor()

print("\n========== DATABASE OPTIMIZATION ==========\n")


# 1. Create Sales Summary View
print("--- Creating Sales Summary View ---")

cursor.execute("DROP VIEW IF EXISTS sales_summary")

cursor.execute("""
CREATE VIEW sales_summary AS
SELECT
    o.order_id,
    c.name AS customer_name,
    o.order_date,
    o.status,
    o.total_amount
FROM orders o
JOIN customers c
    ON o.customer_id = c.customer_id
""")


# 2. Create Product Sales View
print("--- Creating Product Sales View ---")

cursor.execute("DROP VIEW IF EXISTS product_sales")

cursor.execute("""
CREATE VIEW product_sales AS
SELECT
    p.product_name,
    p.category,
    SUM(oi.quantity) AS units_sold,
    SUM(oi.quantity * oi.unit_price) AS revenue
FROM order_items oi
JOIN products p
    ON oi.product_id = p.product_id
JOIN orders o
    ON oi.order_id = o.order_id
WHERE o.status = 'COMPLETED'
GROUP BY p.product_id, p.product_name, p.category
""")


# 3. Create Indexes
print("--- Creating Indexes ---")

cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_orders_customer
ON orders(customer_id)
""")

cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_orders_date
ON orders(order_date)
""")

cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_order_items_product
ON order_items(product_id)
""")


# 4. Test Sales Summary View
print("\n--- Sales Summary View ---")

cursor.execute("""
SELECT *
FROM sales_summary
LIMIT 10
""")

for row in cursor.fetchall():
    print(row)


# 5. Test Product Sales View
print("\n--- Product Sales View ---")

cursor.execute("""
SELECT *
FROM product_sales
ORDER BY revenue DESC
""")

for row in cursor.fetchall():
    print(row)


# 6. Query Optimization
print("\n--- Query Execution Plan ---")

cursor.execute("""
EXPLAIN QUERY PLAN
SELECT *
FROM orders
WHERE customer_id = 1
""")

for row in cursor.fetchall():
    print(row)


connection.commit()
connection.close()

print("\nDatabase optimization completed successfully!")