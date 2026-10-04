import sqlite3

DATABASE = "sales_analytics.db"


def get_connection():
    return sqlite3.connect(DATABASE)


# CREATE
def add_customer():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO customers
        (name, email, city, signup_date)
        VALUES (?, ?, ?, ?)
    """, (
        "Test Customer",
        "testcustomer@gmail.com",
        "Chennai",
        "2026-10-04"
    ))

    connection.commit()
    connection.close()

    print("Customer added successfully!")


# READ
def view_customers():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT customer_id, name, email, city, signup_date
        FROM customers
        ORDER BY customer_id
    """)

    customers = cursor.fetchall()

    print("\n--- Customers ---")

    for customer in customers:
        print(customer)

    connection.close()


# UPDATE
def update_customer():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE customers
        SET city = ?
        WHERE email = ?
    """, (
        "Madurai",
        "testcustomer@gmail.com"
    ))

    connection.commit()
    connection.close()

    print("Customer updated successfully!")


# DELETE
def delete_customer():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM customers
        WHERE email = ?
    """, (
        "testcustomer@gmail.com",
    ))

    connection.commit()
    connection.close()

    print("Customer deleted successfully!")


if __name__ == "__main__":

    print("===== CRUD OPERATIONS =====")

    add_customer()

    view_customers()

    update_customer()

    view_customers()

    delete_customer()

    view_customers()

    print("\nCRUD operations completed successfully!")