import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Connected to SQLite version: {sqlite3.version}")
    except Error as e:
        print(e)
    return conn

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def main():
    database = "database.db"

    sql_create_users_table = """ CREATE TABLE IF NOT EXISTS users (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        Name TEXT NOT NULL,
                                        Surname TEXT NOT NULL,
                                        Birthdate TEXT NOT NULL,
                                        Country TEXT NOT NULL,
                                        Email TEXT NOT NULL,
                                        Approved INTEGER NOT NULL,
                                        Password TEXT NOT NULL
                                    ); """

    # create a database connection
    conn = create_connection(database)
    if conn is not None:
        # create users table
        create_table(conn, sql_create_users_table)
        conn.close()
    else:
        print("Error! cannot create the database connection.")

if __name__ == '__main__':
    main()
