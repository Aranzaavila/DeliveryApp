"""
Delivery model for the Delivery Management App.
Represents a delivery and provides database helper methods.
"""


class Delivery:
    """
    Represents a delivery with all relevant fields.
    """

    def __init__(
        self, id, client_id, description, completed, fee, deadline, completed_date=None
    ):
        """
        Initialize a Delivery instance.
        :param id: Delivery ID.
        :param client_id: Associated client ID.
        :param description: Description of the delivery.
        :param completed: Completion status (0 or 1).
        :param fee: Delivery fee.
        :param deadline: Deadline date as string.
        :param completed_date: Date when completed (optional).
        """
        self.id = id
        self.client_id = client_id
        self.description = description
        self.completed = completed
        self.fee = fee
        self.deadline = deadline
        self.completed_date = completed_date

    @staticmethod
    def get_all(conn):
        """
        Retrieve all deliveries from the database, ordered by deadline.
        :param conn: Database connection.
        :return: List of Delivery instances.
        """
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, client_id, description, completed, fee, deadline, completed_date
            FROM deliveries 
            ORDER BY deadline ASC
        """
        )
        rows = cursor.fetchall()
        return [Delivery(*row) for row in rows]

    @staticmethod
    def get_by_id(conn, delivery_id):
        """
        Retrieve a delivery by its ID.
        :param conn: Database connection.
        :param delivery_id: ID of the delivery to retrieve.
        :return: Delivery instance or None if not found.
        """
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, client_id, description, completed, fee, deadline, completed_date
            FROM deliveries
            WHERE id = ?
        """,
            (delivery_id,),
        )
        row = cursor.fetchone()
        return Delivery(*row) if row else None

    def __repr__(self):
        """
        String representation for debugging.
        """
        return (
            f"Delivery(id={self.id}, client_id={self.client_id}, "
            f"description='{self.description}', completed={self.completed}, "
            f"fee={self.fee}, deadline='{self.deadline}', "
            f"completed_date='{self.completed_date}')"
        )
