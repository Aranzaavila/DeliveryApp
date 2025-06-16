import sqlite3
from models.client import Client
from models.delivery import Delivery


class Database:
    def __init__(self, db_file):
        self.conn= sqlite3.connect(db_file)
        self._tables()
        self._add_completed_date_column()

    def _tables(self):
        cursor = self.conn.cursor()
    

        # client table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        """)

        # freelancers table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS freelancers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        """)

        # delivery table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS deliveries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_id INTEGER NOT NULL,
                description TEXT NOT NULL,
                completed INTEGER DEFAULT 0,
                completed_date TEXT,
                fee REAL NOT NULL,
                deadline TEXT NOT NULL,
                FOREIGN KEY (client_id) REFERENCES clients(id)
            )
        """)

        self.conn.commit()
    
    def _add_completed_date_column(self):
        cursor = self.conn.cursor()
        # Check if column already exists
        cursor.execute("PRAGMA table_info(deliveries)")
        columns = [info[1] for info in cursor.fetchall()]
        if "completed_date" not in columns:
            cursor.execute("""
                ALTER TABLE deliveries 
                ADD COLUMN completed_date TEXT
            """)
            self.conn.commit()



    def insert_client(self, client):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO clients (name) VALUES (?)", (client.name,))  # <-- comma!
        self.conn.commit()
        return cursor.lastrowid

    def insert_freelancer(self, freelancer):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO freelancers (name) VALUES (?)", (freelancer.name,))
        self.conn.commit()
        return cursor.lastrowid
    
    # Add these methods to your Database class

    def count_deliveries(self, completed=None):
        cursor = self.conn.cursor()
        if completed is None:
            cursor.execute("SELECT COUNT(*) FROM deliveries")
        else:
            cursor.execute("SELECT COUNT(*) FROM deliveries WHERE completed=?", (int(completed),))
        return cursor.fetchone()[0]

    def get_all_clients(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, name FROM clients")
        rows = cursor.fetchall()
        return [Client(id=row[0], name=row[1]) for row in rows]

    def add_delivery(self, delivery):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO deliveries (client_id, description, completed, fee, deadline, completed_date)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            delivery.client_id,
            delivery.description,
            delivery.completed,
            delivery.fee,
            delivery.deadline,
            delivery.completed_date
        ))
        self.conn.commit()
        return cursor.lastrowid

    def get_all_deliveries(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, client_id, description, completed, completed_date, fee, deadline FROM deliveries")
        rows = cursor.fetchall()
        return [
            Delivery(
                id=row[0],
                client_id=row[1],
                description=row[2],
                completed=bool(row[3]),
                completed_date=row[4],
                fee=row[5],
                deadline=row[6]
            )
            for row in rows
        ]

    def get_client_by_id(self, client_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, name FROM clients WHERE id=?", (client_id,))
        row = cursor.fetchone()
        if row:
            from models.client import Client
            return Client(id=row[0], name=row[1])
        return None

    def mark_delivery_completed(self, delivery_id):
        import datetime
        cursor = self.conn.cursor()
        completed_date = datetime.datetime.now().strftime("%Y-%m-%d")
        cursor.execute(
            "UPDATE deliveries SET completed=1, completed_date=? WHERE id=?",
            (completed_date, delivery_id)
        )
        self.conn.commit()
