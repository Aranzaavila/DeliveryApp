class Client:
    def __init__(self, client_id, name, address):
        self.client_id= client_id
        self.name= name
        self.address= address
    
    def __str__(self):
        return f'{self.name} - ({self.address})'