class Client:
    def __init__(self, name, id=None):
        self.id = id
        self.name = name
        

    @staticmethod
    def get_by_id(conn, client_id):
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM clients WHERE id=?", (client_id,))
        row = cursor.fetchone()
        return Client(row[1], row[0]) if row else None

    @staticmethod
    def get_id_by_name(conn, name):
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM clients WHERE name = ?", (name,))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            cursor.execute("INSERT INTO clients (name) VALUES (?)", (name,))
            conn.commit()
            return cursor.lastrowid
