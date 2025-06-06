class Delivery:
    def __init__(self, id, client_id, description, status, fee, delivery_date, delivery_time, deadline):
        self.id = id
        self.client_id = client_id
        self.description = description
        self.status = status
        self.fee = fee
        self.delivery_date = delivery_date
        self.delivery_time = delivery_time
        self.deadline = deadline

    @staticmethod
    def get_all(conn):
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, client_id, description, status, fee, delivery_date, delivery_time, deadline
            FROM deliveries
        """)
        rows = cursor.fetchall()
        return [Delivery(*row) for row in rows]

    @staticmethod
    def get_by_id(conn, delivery_id):
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, client_id, description, status, fee, delivery_date, delivery_time, deadline
            FROM deliveries
            WHERE id = ?
        """, (delivery_id,))
        row = cursor.fetchone()
        return Delivery(*row) if row else None
    
    def __repr__(self):
        return (f"Delivery(id={self.id}, client_id={self.client_id}, "
                f"description='{self.description}', status='{self.status}', "
                f"fee={self.fee}, delivery_date='{self.delivery_date}', "
                f"delivery_time='{self.delivery_time}', deadline='{self.deadline}')")


