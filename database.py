import sqlite3

DATABASE = "sales_analytics.db"


def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def create_database():
    connection = get_connection()

    with open("schema.sql", "r") as file:
        schema = file.read()

    connection.executescript(schema)
    connection.commit()
    connection.close()

    print("Database created successfully!")


if __name__ == "__main__":
    create_database()