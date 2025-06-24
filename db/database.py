import sqlite3
from models.client import Client
from models.delivery import Delivery
from models.invoice import Invoice
import datetime


class Database:
    """
    Database class for the Delivery Management App.
    Handles all database operations and table management.
    """

    def __init__(self, db_file):
        """
        Initialize the database connection and create tables if needed.
        """
        self.conn = sqlite3.connect(db_file)
        self._create_tables()
        self._add_completed_date_column()

    def _create_tables(self):
        """
        Create all necessary tables if they do not exist.
        """
        cursor = self.conn.cursor()

        # Clients table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        """)

        # Freelancers table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS freelancers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        """)

        # Deliveries table
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

        # Invoices table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS invoices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                delivery_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                date TEXT NOT NULL,
                paid INTEGER DEFAULT 0,
                FOREIGN KEY (delivery_id) REFERENCES deliveries(id)
            )
        """)
         # history table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS delivery_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            delivery_id INTEGER NOT NULL,
            action TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            FOREIGN KEY (delivery_id) REFERENCES deliveries(id)
        )
    """)
        self.conn.commit()

    def _add_completed_date_column(self):
        """
        Add the completed_date column to deliveries if it does not exist.
        """
        cursor = self.conn.cursor()
        cursor.execute("PRAGMA table_info(deliveries)")
        columns = [info[1] for info in cursor.fetchall()]
        if "completed_date" not in columns:
            cursor.execute("""
                ALTER TABLE deliveries 
                ADD COLUMN completed_date TEXT
            """)
            self.conn.commit()

    def insert_client(self, client):
        """
        Insert a new client into the database.
        :param client: Client instance.
        :return: ID of the inserted client.
        """
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO clients (name) VALUES (?)", (client.name,))
        self.conn.commit()
        return cursor.lastrowid

    def insert_freelancer(self, freelancer):
        """
        Insert a new freelancer into the database.
        :param freelancer: Freelancer instance.
        :return: ID of the inserted freelancer.
        """
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO freelancers (name) VALUES (?)", (freelancer.name,))
        self.conn.commit()
        return cursor.lastrowid

    def count_deliveries(self, completed=None):
        """
        Count deliveries, optionally filtered by completion status.
        :param completed: None for all, True for completed, False for pending.
        :return: Number of deliveries.
        """
        cursor = self.conn.cursor()
        if completed is None:
            cursor.execute("SELECT COUNT(*) FROM deliveries")
        else:
            cursor.execute(
                "SELECT COUNT(*) FROM deliveries WHERE completed=?",
                (int(completed),)
            )
        return cursor.fetchone()[0]

    def get_all_clients(self):
        """
        Retrieve all clients from the database.
        :return: List of Client instances.
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, name FROM clients")
        rows = cursor.fetchall()
        return [Client(id=row[0], name=row[1]) for row in rows]

    def add_delivery(self, delivery):
        """
        Add a new delivery to the database.
        :param delivery: Delivery instance.
        :return: ID of the inserted delivery.
        """
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
        """
        Retrieve all deliveries from the database.
        :return: List of Delivery instances.
        """
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT id, client_id, description, completed, completed_date, fee, deadline FROM deliveries"
        )
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
        """
        Retrieve a client by their ID.
        :param client_id: ID of the client.
        :return: Client instance or None.
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, name FROM clients WHERE id=?", (client_id,))
        row = cursor.fetchone()
        if row:
            return Client(id=row[0], name=row[1])
        return None

    def get_client_by_name(self, client_name):
        """
        Retrieve a client by their name.
        :param client_name: Name of the client.
        :return: Client instance or None.
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, name FROM clients WHERE name = ?", (client_name,))
        row = cursor.fetchone()
        if row:
            return Client(id=row[0], name=row[1])
        return None

    def mark_delivery_completed(self, delivery_id):
        """
        Mark a delivery as completed and set the completed_date.
        :param delivery_id: ID of the delivery to mark as completed.
        """
        
        cursor = self.conn.cursor()
        completed_date = datetime.datetime.now().strftime("%Y-%m-%d")
        cursor.execute(
            "UPDATE deliveries SET completed=1, completed_date=? WHERE id=?",
            (completed_date, delivery_id)
        )
        self.conn.commit()

    def add_invoice(self, delivery_id, amount, date):
        """
        Add a new invoice to the database.
        :param delivery_id: Associated delivery ID.
        :param amount: Invoice amount.
        :param date: Invoice date.
        :return: ID of the inserted invoice.
        """
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO invoices (delivery_id, amount, date, paid) VALUES (?, ?, ?, 0)",
            (delivery_id, amount, date)
        )
        self.conn.commit()
        return cursor.lastrowid

    def get_all_invoices(self):
        """
        Retrieve all invoices from the database.
        :return: List of Invoice instances.
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, delivery_id, amount, date, paid FROM invoices")
        rows = cursor.fetchall()
        return [Invoice(*row) for row in rows]

    def mark_invoice_as_paid(self, invoice_id):
        """
        Mark an invoice as paid.
        """
        cursor = self.conn.cursor()
        cursor.execute("UPDATE invoices SET paid=1 WHERE id=?", (invoice_id,))
        self.conn.commit()

    def get_total_earnings_by_month(self):
        """
        Get total earnings grouped by month.
        :return: Dictionary with month as key and total earnings as value.
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT strftime('%Y-%m', deadline) as month, SUM(fee)
            FROM deliveries
            GROUP BY month
            ORDER BY month
        """)
        rows = cursor.fetchall()
        return {row[0]: row[1] for row in rows}

    def count_all_deliveries(self):
        """Return the total number of deliveries directly from the DB."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(id) FROM deliveries")
        return cursor.fetchone()[0]

    def count_completed(self):
        """Return the total number of completed deliveries directly from the DB."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(id) FROM deliveries WHERE completed = 1")
        return cursor.fetchone()[0]

    def count_pending(self):
        """Return the total number of pending deliveries directly from the DB."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(id) FROM deliveries WHERE completed = 0")
        return cursor.fetchone()[0]

    def total_earnings(self):
        """Return the sum of fees for completed deliveries directly from the DB."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT COALESCE(SUM(fee), 0) FROM deliveries WHERE completed = 1")
        return cursor.fetchone()[0]

    def get_delivery_by_id(self, delivery_id):
        """
        Retrieve a delivery by its ID.
        :param delivery_id: ID of the delivery.
        :return: Delivery instance or None.
        """
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT id, client_id, description, completed, completed_date, fee, deadline FROM deliveries WHERE id=?",
            (delivery_id,)
        )
        row = cursor.fetchone()
        if row:
            return Delivery(
                id=row[0], client_id=row[1], description=row[2],
                completed=bool(row[3]), completed_date=row[4],
                fee=row[5], deadline=row[6]
            )
        return None

    def delete_delivery(self, delivery_id):
        """
        Delete a delivery from the database by its ID.
        """
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM invoices WHERE delivery_id=?", (delivery_id,))
        cursor.execute("DELETE FROM deliveries WHERE id=?", (delivery_id,))
        self.conn.commit()

    def update_delivery(self, delivery_id, description, fee, deadline):
        """
        Update the details of a delivery.
        """
        cursor = self.conn.cursor()
        cursor.execute(
            "UPDATE deliveries SET description=?, fee=?, deadline=? WHERE id=?",
            (description, fee, deadline, delivery_id)
        )
        self.conn.commit()
    def add_delivery_history(self, delivery_id, action):
        """
        Add a record to the delivery's change history.
        """
        
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO delivery_history (delivery_id, action, timestamp) VALUES (?, ?, ?)",
            (delivery_id, action, timestamp)
        )
        self.conn.commit()

    def get_delivery_history(self, delivery_id):
        """
        Get the change history for a delivery.
        """
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT action, timestamp FROM delivery_history WHERE delivery_id=? ORDER BY timestamp DESC",
            (delivery_id,)
        )
        return cursor.fetchall()
