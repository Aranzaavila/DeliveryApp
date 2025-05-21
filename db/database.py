import sqlite3

from models.client import Client
from models.delivery import Delivery
from models.freelancer import Freelancer

def connections(db_file):
    conn = sqlite3.connect(db_file)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def tables(conn):
    cursor = conn.cursor()

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
        fee REAL NOT NULL
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
        "INSERT OR REPLACE INTO clients (name, address) VALUES (?, ?)",
        (client.name, client.address)
    )
    conn.commit()


def insert_delivery(conn, delivery):
    cursor = conn.cursor()
   
    cursor.execute("SELECT name FROM freelancers WHERE name = ?", (delivery.freelancer_name,))
    if not cursor.fetchone():
        raise ValueError(f"Freelancer '{delivery.freelancer_name}' no existe.")
    cursor.execute("SELECT name FROM clients WHERE name = ?", (delivery.client_name,))
    if not cursor.fetchone():
        raise ValueError(f"Client '{delivery.client_name}' no existe.")

    cursor.execute(
        "INSERT OR REPLACE INTO deliveries (client_name, freelancer_name, pickup_address, dropoff_address, status, fee) VALUES (?, ?, ?, ?, ?, ?)",
        (delivery.client_name, delivery.freelancer_name, delivery.pickup_address,
         delivery.dropoff_address, delivery.status, delivery.fee)
    )
    conn.commit()
    
def main():
    
    conn = connections('your_database.db')
    tables(conn)

  
    f = Freelancer('Alice', 'alice@example.com')
    insert_freelancer(conn, f)

    c = Client('ClienteX', 'Calle Falsa 123')
    insert_client(conn, c)

    d = Delivery('ClienteX', 'Alice', 'Origen 1', 'Destino 1', 'Pending', 20.0)
    insert_delivery(conn, d)

if __name__ == "__main__":
    main()
