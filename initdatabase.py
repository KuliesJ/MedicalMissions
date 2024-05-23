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

def insert_missions(conn):
    """ insert missions into the missions table """
    missions = [
    ('Pamplona Alta - 2018 (video)', '2018-01-01', '2018-12-31', 'Itinerary Placeholder', 0.0, 'Cost Description Placeholder', 'Contact Placeholder'),
    ('Chachapoyas - 2017 (photos)', '2017-01-01', '2017-12-31', 'Itinerary Placeholder', 0.0, 'Cost Description Placeholder', 'Contact Placeholder'),
    ('Ayaviri - 2017 (photos)', '2017-01-01', '2017-12-31', 'Itinerary Placeholder', 0.0, 'Cost Description Placeholder', 'Contact Placeholder'),
    ('Pamplona Alta - 2014 (photos)', '2014-01-01', '2014-12-31', 'Itinerary Placeholder', 0.0, 'Cost Description Placeholder', 'Contact Placeholder'),
    ('Pamplona Alta - 2012 (photos)', '2012-01-01', '2012-12-31', 'Itinerary Placeholder', 0.0, 'Cost Description Placeholder', 'Contact Placeholder'),
    ('Ayaviri - 2012 (video)', '2012-01-01', '2012-12-31', 'Itinerary Placeholder', 0.0, 'Cost Description Placeholder', 'Contact Placeholder'),
    ('Pamplona Alta - 2011 (photos)', '2011-01-01', '2011-12-31', 'Itinerary Placeholder', 0.0, 'Cost Description Placeholder', 'Contact Placeholder'),
    ('Ayaviri - 2011 (photos)', '2011-01-01', '2011-12-31', 'Itinerary Placeholder', 0.0, 'Cost Description Placeholder', 'Contact Placeholder'),
    ('Pamplona Alta - 2010 (video)', '2010-01-01', '2010-12-31', 'Itinerary Placeholder', 0.0, 'Cost Description Placeholder', 'Contact Placeholder'),
    ('Chincha, Ica - 2008 (slide show)', '2008-01-01', '2008-12-31', 'Itinerary Placeholder', 0.0, 'Cost Description Placeholder', 'Contact Placeholder'),
    ('Ayaviri-2023', '2023-09-22', '2023-09-30', 
     '''September 22 - Depart US\n
        September 23 - Arrive Cusco/acclimate/Mandatory group meeting & dinner\n
        September 24 - Day trip as a mission group/get to know each other\n
        September 25 - Transfer to Ayaviri, set up clinic\n
        September 26 - Medical Mission\n
        September 27 - Medical Mission\n
        September 28 - Medical Mission\n
        September 29 - Medical Mission half day/home visits and pack up mission site\n
        September 30 - Depart for home''', 
     925.0, 
     '''All hotel accommodations with breakfast (from September 23rd to 30th), 
        transfer to and from the airport on September 23rd and 30th (Cuzco and Juliaca only), 
        team day trip and dinner in Cuzco, 2 T-shirts, ground transportation (Cuzco – Ayaviri), 
        all meals in Ayaviri, participant contribution for medications, supplies and year around continue care 
        for the population we serve.\n\n
        It doesn't include: Personal expenses, voluntary tips, meals, airfare, nor anything not mentioned above. 
        Current roundtrip air from major cities in the US to Cusco is approximately $2,000.\n\n
        A USD 400.00 deposit is required with your application. 
        The remaining balance is required by August 15th, 2023.''', 
     'Contact: Katy Brant\nMission Coordinator\n(303) 476-1358')
]


    sql = ''' INSERT INTO missions(Name, Date_to_begin, Date_to_end, Itinerary, Cost, mission_cost_description, Contact)
              VALUES(?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.executemany(sql, missions)
    conn.commit()

def insert_admin(conn):
    """ insert an admin user into the users table """
    admin = ('Admin', 'User', '1970-01-01', 'Country Placeholder', 'admin@example.com', 1, 'adminpassword', 1)
    sql = ''' INSERT INTO users(Name, Surname, Birthdate, Country, Email, Approved, Password, is_admin)
              VALUES(?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, admin)
    conn.commit()

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
                                        Password TEXT NOT NULL,
                                        is_admin INTEGER NOT NULL
                                    ); """

    sql_create_missions_table = """ CREATE TABLE IF NOT EXISTS missions (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    Name TEXT NOT NULL,
                                    Date_to_begin DATE,
                                    Date_to_end DATE,
                                    Itinerary TEXT,
                                    Cost FLOAT,
                                    mission_cost_description TEXT,
                                    Contact TEXT
                                );"""

    # create a database connection
    conn = create_connection(database)
    if conn is not None:
        # create users table
        create_table(conn, sql_create_users_table)
        # create missions table
        create_table(conn, sql_create_missions_table)
        # insert missions
        insert_missions(conn)
        # insert admin user
        insert_admin(conn)
        conn.close()
    else:
        print("Error! cannot create the database connection.")

if __name__ == '__main__':
    main()
