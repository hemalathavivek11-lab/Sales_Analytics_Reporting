import sqlite3

DATABASE = "sales_analytics.db"

connection = sqlite3.connect(DATABASE)
cursor = connection.cursor()

# Customers
customers = [
    (1, "Arun Kumar", "arun@gmail.com", "Chennai", "2026-01-05"),
    (2, "Priya Sharma", "priya@gmail.com", "Madurai", "2026-01-10"),
    (3, "Rahul Raj", "rahul@gmail.com", "Coimbatore", "2026-01-15"),
    (4, "Divya S", "divya@gmail.com", "Trichy", "2026-02-02"),
    (5, "Karthik M", "karthik@gmail.com", "Salem", "2026-02-12"),
    (6, "Meena R", "meena@gmail.com", "Chennai", "2026-03-01"),
    (7, "Vijay Kumar", "vijay@gmail.com", "Madurai", "2026-03-15"),
    (8, "Anitha P", "anitha@gmail.com", "Erode", "2026-04-05")
]

cursor.executemany("""
INSERT OR IGNORE INTO customers
(customer_id, name, email, city, signup_date)
VALUES (?, ?, ?, ?, ?)
""", customers)


# Products
products = [
    (1, "Laptop", "Electronics", 55000, 20),
    (2, "Smartphone", "Electronics", 25000, 35),
    (3, "Headphones", "Accessories", 2500, 50),
    (4, "Keyboard", "Accessories", 1500, 40),
    (5, "Mouse", "Accessories", 800, 60),
    (6, "Monitor", "Electronics", 12000, 25),
    (7, "Printer", "Electronics", 15000, 15),
    (8, "Webcam", "Accessories", 3500, 30)
]

cursor.executemany("""
INSERT OR IGNORE INTO products
(product_id, product_name, category, price, stock)
VALUES (?, ?, ?, ?, ?)
""", products)


# Orders
orders = [
    (1, 1, "2026-01-12", "COMPLETED", 57500),
    (2, 2, "2026-01-20", "COMPLETED", 27500),
    (3, 3, "2026-02-05", "COMPLETED", 12000),
    (4, 4, "2026-02-18", "CANCELLED", 15000),
    (5, 5, "2026-03-02", "COMPLETED", 25800),
    (6, 1, "2026-03-15", "COMPLETED", 15000),
    (7, 6, "2026-04-01", "PENDING", 55000),
    (8, 2, "2026-04-12", "COMPLETED", 5000),
    (9, 7, "2026-05-03", "COMPLETED", 15000),
    (10, 8, "2026-05-18", "COMPLETED", 6300),
    (11, 3, "2026-06-05", "COMPLETED", 25000),
    (12, 5, "2026-06-20", "COMPLETED", 2800)
]

cursor.executemany("""
INSERT OR IGNORE INTO orders
(order_id, customer_id, order_date, status, total_amount)
VALUES (?, ?, ?, ?, ?)
""", orders)


# Order items
order_items = [
    (1, 1, 1, 1, 55000),
    (2, 1, 3, 1, 2500),

    (3, 2, 2, 1, 25000),
    (4, 2, 5, 1, 800),
    (5, 2, 4, 1, 1500),

    (6, 3, 6, 1, 12000),

    (7, 4, 7, 1, 15000),

    (8, 5, 2, 1, 25000),
    (9, 5, 5, 1, 800),

    (10, 6, 7, 1, 15000),

    (11, 7, 1, 1, 55000),

    (12, 8, 8, 1, 3500),
    (13, 8, 4, 1, 1500),

    (14, 9, 7, 1, 15000),

    (15, 10, 6, 1, 5500),
    (16, 10, 5, 1, 800),

    (17, 11, 2, 1, 25000),

    (18, 12, 3, 1, 2500),
    (19, 12, 5, 1, 300)
]

cursor.executemany("""
INSERT OR IGNORE INTO order_items
(order_item_id, order_id, product_id, quantity, unit_price)
VALUES (?, ?, ?, ?, ?)
""", order_items)


# Payments
payments = [
    (1, 1, "2026-01-12", 57500, "PAID"),
    (2, 2, "2026-01-20", 27500, "PAID"),
    (3, 3, "2026-02-05", 12000, "PAID"),
    (4, 4, "2026-02-18", 15000, "REFUNDED"),
    (5, 5, "2026-03-02", 25800, "PAID"),
    (6, 6, "2026-03-15", 15000, "PAID"),
    (7, 7, "2026-04-01", 55000, "PENDING"),
    (8, 8, "2026-04-12", 5000, "PAID"),
    (9, 9, "2026-05-03", 15000, "PAID"),
    (10, 10, "2026-05-18", 6300, "PAID"),
    (11, 11, "2026-06-05", 25000, "PAID"),
    (12, 12, "2026-06-20", 2800, "PAID")
]

cursor.executemany("""
INSERT OR IGNORE INTO payments
(payment_id, order_id, payment_date, amount, payment_status)
VALUES (?, ?, ?, ?, ?)
""", payments)


connection.commit()
connection.close()

print("Sample sales data inserted successfully!")