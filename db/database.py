import sqlite3
from models.client import Client
from models.delivery import Delivery
from models.freelancer import Freelancer
from datetime import datetime

def connections(db_file):
    conn = sqlite3.connect(db_file)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def tables(conn):
    cursor = conn.cursor()
    
    cursor.execute("DROP TABLE IF EXISTS deliveries")
    cursor.execute("DROP TABLE IF EXISTS clients")
    cursor.execute("DROP TABLE IF EXISTS freelancers")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS freelancers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL
    )
    """)

    cursor.execute("""
CREATE TABLE IF NOT EXISTS clients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    address TEXT NOT NULL
)
""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS deliveries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_name TEXT NOT NULL,
        freelancer_name TEXT NOT NULL,
        pickup_address TEXT NOT NULL,
        dropoff_address TEXT NOT NULL,
        status TEXT NOT NULL,
        fee REAL NOT NULL,
        delivery_date TEXT NOT NULL,   
        delivery_time TEXT NOT NULL    
    )
    """)

    conn.commit()

def insert_freelancer(conn, freelancer):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR REPLACE INTO freelancers (name, email) VALUES (?, ?)",
        (freelancer.name, freelancer.email)
    )
    conn.commit()

def insert_client(conn, client):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO clients (name, address) VALUES (?, ?)",
        (client.name, client.address)
    )
    conn.commit()

def insert_delivery(conn, delivery):
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM freelancers WHERE name = ?", (delivery.freelancer_name,))
    if not cursor.fetchone():
        raise ValueError(f"Freelancer '{delivery.freelancer_name}' does not exist.")

    cursor.execute("SELECT name FROM clients WHERE name = ?", (delivery.client_name,))
    if not cursor.fetchone():
        raise ValueError(f"Client '{delivery.client_name}' does not exist.")

    
    delivery_date = datetime.now().strftime('%Y-%m-%d') 
    delivery_time = datetime.now().strftime('%H:%M')  

    cursor.execute(
        """
        INSERT INTO deliveries (
            client_name, freelancer_name, pickup_address, dropoff_address, status, fee,
            delivery_date, delivery_time
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            delivery.client_name,
            delivery.freelancer_name,
            delivery.pickup_address,
            delivery.dropoff_address,
            delivery.status,
            delivery.fee,
            delivery_date,
            delivery_time
        )
    )
    conn.commit()

def main():
    conn = connections('deliveries.db')
    tables(conn)

   
    f = Freelancer('Alice', 'alice@example.com')
    insert_freelancer(conn, f)

    
    c = Client('ClienteX', 'Fake street 123')
    insert_client(conn, c)

    d = Delivery('ClienteX', 'Alice', 'Origen 1', 'Destino 1', 'Pending', 20.0)
    insert_delivery(conn, d)

    print("Database initialized with sample data.")

if __name__ == "__main__":
    main()
