class Delivery:
    def __init__(self, id, client_id, description, status, fee, deadline):
        self.id = id
        self.client_id = client_id
        self.description = description
        self.status = status
        self.fee = fee
        self.deadline = deadline

    @staticmethod
    def get_all(conn):
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, client_id, description, status, fee,  deadline
            FROM deliveries 
            ORDER BY deadline ASC
        """)
        rows = cursor.fetchall()
        return [Delivery(*row) for row in rows]

    @staticmethod
    def get_by_id(conn, delivery_id):
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, client_id, description, status, fee, deadline
            FROM deliveries
            WHERE id = ?
        """, (delivery_id,))
        row = cursor.fetchone()
        return Delivery(*row) if row else None
    
    def __repr__(self):
        return (f"Delivery(id={self.id}, client_id={self.client_id}, "
                f"description='{self.description}', status='{self.status}', "
                f"fee={self.fee},  deadline='{self.deadline}')")


