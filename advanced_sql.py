import sqlite3

DATABASE = "sales_analytics.db"

connection = sqlite3.connect(DATABASE)
cursor = connection.cursor()

print("\n========== ADVANCED SQL ANALYTICS ==========\n")


# 1. SUBQUERY
print("--- 1. Customers Above Average Sales ---")

cursor.execute("""
SELECT
    c.name,
    SUM(o.total_amount) AS total_sales
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
WHERE o.status = 'COMPLETED'
GROUP BY c.customer_id, c.name
HAVING SUM(o.total_amount) > (
    SELECT AVG(total_amount)
    FROM orders
    WHERE status = 'COMPLETED'
)
ORDER BY total_sales DESC
""")

for row in cursor.fetchall():
    print(row)


# 2. CTE
print("\n--- 2. Customer Sales Using CTE ---")

cursor.execute("""
WITH customer_sales AS (
    SELECT
        customer_id,
        SUM(total_amount) AS total_sales
    FROM orders
    WHERE status = 'COMPLETED'
    GROUP BY customer_id
)
SELECT
    c.name,
    customer_sales.total_sales
FROM customer_sales
JOIN customers c
    ON customer_sales.customer_id = c.customer_id
ORDER BY customer_sales.total_sales DESC
""")

for row in cursor.fetchall():
    print(row)


# 3. CASE
print("\n--- 3. Order Value Classification ---")

cursor.execute("""
SELECT
    order_id,
    total_amount,
    CASE
        WHEN total_amount >= 50000 THEN 'High Value'
        WHEN total_amount >= 20000 THEN 'Medium Value'
        ELSE 'Low Value'
    END AS order_category
FROM orders
ORDER BY total_amount DESC
""")

for row in cursor.fetchall():
    print(row)


# 4. RANKING
print("\n--- 4. Customer Sales Ranking ---")

cursor.execute("""
SELECT
    c.name,
    SUM(o.total_amount) AS total_sales,
    RANK() OVER (
        ORDER BY SUM(o.total_amount) DESC
    ) AS sales_rank
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
WHERE o.status = 'COMPLETED'
GROUP BY c.customer_id, c.name
ORDER BY sales_rank
""")

for row in cursor.fetchall():
    print(row)


# 5. ROW_NUMBER
print("\n--- 5. Order Ranking ---")

cursor.execute("""
SELECT
    order_id,
    total_amount,
    ROW_NUMBER() OVER (
        ORDER BY total_amount DESC
    ) AS order_rank
FROM orders
WHERE status = 'COMPLETED'
ORDER BY order_rank
""")

for row in cursor.fetchall():
    print(row)


# 6. RUNNING TOTAL
print("\n--- 6. Running Sales Total ---")

cursor.execute("""
SELECT
    order_date,
    order_id,
    total_amount,
    SUM(total_amount) OVER (
        ORDER BY order_date, order_id
    ) AS running_total
FROM orders
WHERE status = 'COMPLETED'
ORDER BY order_date, order_id
""")

for row in cursor.fetchall():
    print(row)


# 7. MONTHLY SALES
print("\n--- 7. Monthly Sales ---")

cursor.execute("""
SELECT
    strftime('%Y-%m', order_date) AS month,
    SUM(total_amount) AS monthly_sales
FROM orders
WHERE status = 'COMPLETED'
GROUP BY month
ORDER BY month
""")

for row in cursor.fetchall():
    print(row)


# 8. TOP 3 PRODUCTS
print("\n--- 8. Top 3 Products ---")

cursor.execute("""
SELECT
    p.product_name,
    SUM(oi.quantity * oi.unit_price) AS revenue
FROM order_items oi
JOIN products p
    ON oi.product_id = p.product_id
JOIN orders o
    ON oi.order_id = o.order_id
WHERE o.status = 'COMPLETED'
GROUP BY p.product_id, p.product_name
ORDER BY revenue DESC
LIMIT 3
""")

for row in cursor.fetchall():
    print(row)


connection.close()

print("\nAdvanced SQL analytics completed successfully!")