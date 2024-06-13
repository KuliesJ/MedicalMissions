import sqlite3
from sqlite3 import Error
import bcrypt

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Connected to SQLite version: {sqlite3.version}")
    except Error as e:
        print(e)
    return conn

def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def insert_admin(conn):
    name = 'Admin'
    surname = 'User'
    birthdate = '1970-01-01'
    country = 'Country Placeholder'
    email = 'admin@example.com'
    password = 'adminpassword'
    is_admin = 1
    
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    admin = (name, surname, birthdate, country, email, hashed_password, is_admin)
    
    sql = ''' INSERT INTO users(Name, Surname, Birthdate, Country, Email, Password, is_admin)
              VALUES(?,?,?,?,?,?,?) '''
    
    cur = conn.cursor()
    cur.execute(sql, admin)
    conn.commit()

def create_posts_table(conn):
    try:
        sql_create_posts_table = """ CREATE TABLE IF NOT EXISTS posts (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        title TEXT,
                                        subtitle TEXT,
                                        content TEXT,
                                        image TEXT,
                                        section TEXT NOT NULL,
                                        `order` INTEGER DEFAULT 0,
                                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                                    ); """
        c = conn.cursor()
        c.execute(sql_create_posts_table)
        
        # Add the order column if it doesn't exist
        c.execute("PRAGMA table_info(posts);")
        columns = [column[1] for column in c.fetchall()]
        if 'order' not in columns:
            c.execute("ALTER TABLE posts ADD COLUMN `order` INTEGER DEFAULT 0;")
        conn.commit()
    except Error as e:
        print(f"Error occurred: {e}")

def main():
    database = "database.db"

    sql_create_users_table = """ CREATE TABLE IF NOT EXISTS users (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    Name TEXT NOT NULL,
                                    Surname TEXT NOT NULL,
                                    Birthdate TEXT,
                                    Country TEXT,
                                    Email TEXT NOT NULL,
                                    Password TEXT NOT NULL,
                                    is_admin INTEGER NOT NULL DEFAULT 0
                                ); """

    conn = create_connection(database)

    if conn is not None:
        create_table(conn, sql_create_users_table)
        insert_admin(conn)
        create_posts_table(conn)
        conn.close()
    else:
        print("Error! Cannot create the database connection.")

if __name__ == '__main__':
    main()
