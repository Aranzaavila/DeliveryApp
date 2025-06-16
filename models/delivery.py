class Delivery:
    def __init__(self, id, client_id, description, completed, fee, deadline, completed_date=None):
        self.id = id
        self.client_id = client_id
        self.description = description
        self.completed = completed  
        self.fee = fee
        self.deadline = deadline
        self.completed_date = completed_date

    @staticmethod
    def get_all(conn):
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, client_id, description, completed, fee, deadline, completed_date
            FROM deliveries 
            ORDER BY deadline ASC
        """)
        rows = cursor.fetchall()
        return [Delivery(*row) for row in rows]

    @staticmethod
    def get_by_id(conn, delivery_id):
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, client_id, description, completed, fee, deadline, completed_date
            FROM deliveries
            WHERE id = ?
        """, (delivery_id,))
        row = cursor.fetchone()
        return Delivery(*row) if row else None
    
    def __repr__(self):
        return (f"Delivery(id={self.id}, client_id={self.client_id}, "
                f"description='{self.description}', completed={self.completed}, "
                f"fee={self.fee}, deadline='{self.deadline}', completed_date='{self.completed_date}')")
