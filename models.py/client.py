class Client:
    def __init__(self, client_id, name, address):
        self.client_id= client_id
        self.name= name
        self.address= address
    
    def update_info(self, name=None, address=None):
        if name:
            self.name= name

        if address:
            self.address= address