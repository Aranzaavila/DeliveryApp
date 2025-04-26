import sqlite3 

def connections(db_file):
    conn = sqlite3.connect(db_file)
    return conn

def tables(conn):
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS freelancers (id INTEGER PRIMARY KEY,
                   name TEXT NOT NULL,
                   email YEXY NOT NULL
                   )

   ''' )
    
    cursor.execute(''' 
CREATE TABLE IF NOT EXISTS clients ( id INTEGER PRIMARY KEY,
                   name TEXT NOT NULL,
                   address TEXT NOT NULL
                   )

''' )
    

    cursor.execute('''
CREATE TABLE IF NOT EXISTS deliveries(
                   id INTEGER PRIMARY KEY,
                   client_id INTEGER,
                   pickup_address TEXT,
                   dropoff_address TEXT,
                   status TEXT,
                   fee REAL,
                   FOREIGN KEY (client_id) REFERENCES clients (id),
                   FOREIGN KEY (freelancer_id) REFERENCES freelancers (id)

                   
                   )


''')
    
sqlite3.connect()