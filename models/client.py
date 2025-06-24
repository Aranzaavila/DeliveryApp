"""
Client model for the Delivery Management App.
Represents a client and provides database helper methods.
"""


class Client:
    """
    Represents a client with an id and name.
    """

    def __init__(self, name, id=None):
        """
        Initialize a Client instance.
        :param name: Name of the client.
        :param id: ID of the client (optional).
        """
        self.id = id
        self.name = name

    @staticmethod
    def get_by_id(conn, client_id):
        """
        Retrieve a client from the database by ID.
        :param conn: Database connection.
        :param client_id: ID of the client to retrieve.
        :return: Client instance or None if not found.
        """
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM clients WHERE id=?", (client_id,))
        row = cursor.fetchone()
        return Client(row[1], row[0]) if row else None

    @staticmethod
    def get_id_by_name(conn, name):
        """
        Retrieve a client's ID by name, or create the client if not found.
        :param conn: Database connection.
        :param name: Name of the client.
        :return: ID of the client.
        """
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM clients WHERE name = ?", (name,))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            cursor.execute("INSERT INTO clients (name) VALUES (?)", (name,))
            conn.commit()
            return cursor.lastrowid
