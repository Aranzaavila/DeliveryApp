import sqlite3 

def connections(db_file):
    conn = sqlite3.connect(db_file)
    return conn

def tables(conn):
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS freelancers (
        freelancer_id INTEGER PRIMARY KEY,
        user_id INTEGER,
        name TEXT ,
        email TEXT 
        )

    ''' )
    
    cursor.execute(''' 
    CREATE TABLE IF NOT EXISTS clients (
     CLIENT_id INTEGER PRIMARY KEY,
    name TEXT,
    address TEXT 
    )

    ''' )
    

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS deliveries(
        delivery_id INTEGER PRIMARY KEY,
        client_id TEXT,
        freelancer_id INTEGER,
        pickup_address TEXT,
        dropoff_address TEXT,
        status TEXT,
        fee REAL,
        FOREIGN KEY (client_id) REFERENCES clients (client_id),
        FOREIGN KEY (freelancer_id) REFERENCES freelancers (freelancer_id)

                   
    )


    ''')
    
def main():
    conn= connections('your_database.db')
    tables(conn)
    conn.close()

if __name__=="__main__":
    main()
    
