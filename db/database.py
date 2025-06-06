import sqlite3

def connections(db_file):
    conn = sqlite3.connect(db_file)
    return conn

def tables(conn):
    cursor = conn.cursor()

    # client table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT
        )
    """)

    # freelancers table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS freelancers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT
        )
    """)

    # delivery table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS deliveries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER NOT NULL,
            description TEXT NOT NULL,
            status TEXT NOT NULL,
            fee REAL NOT NULL,
            delivery_date TEXT NOT NULL,
            delivery_time TEXT NOT NULL,
            deadline TEXT NOT NULL,
            FOREIGN KEY (client_id) REFERENCES clients(id)
        )
    """)

    conn.commit()

def insert_client(conn, client):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO clients (name, email) VALUES (?, ?)", (client.name, client.email))
    conn.commit()
    return cursor.lastrowid

def insert_freelancer(conn, freelancer):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO freelancers (name, email) VALUES (?, ?)", (freelancer.name, freelancer.email))
    conn.commit()
    return cursor.lastrowid

def insert_delivery(conn, delivery):
    cursor = conn.cursor()

    # Validate that the client exists
    cursor.execute("SELECT id FROM clients WHERE id = ?", (delivery.client_id,))
    result = cursor.fetchone()

    if not result:
        raise ValueError(f"Client with id {delivery.client_id} does not exist.")

    cursor.execute("""
        INSERT INTO deliveries (client_id, description, status, fee, delivery_date, delivery_time, deadline)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        delivery.client_id,
        delivery.description,
        delivery.status,
        delivery.fee,
        delivery.delivery_date,
        delivery.delivery_time,
        delivery.deadline
    ))

    conn.commit()
    return cursor.lastrowid

    
