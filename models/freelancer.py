class Freelancer:
    def __init__(self, name, email, id=None):
        self.id=id
        self.name = name
        self.email = email
        self.deliveries = []

    def add_delivery(self, delivery):
        self.deliveries.append(delivery)





