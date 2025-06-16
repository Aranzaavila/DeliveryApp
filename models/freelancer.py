class Freelancer:
    def __init__(self, name, id=None):
        self.id=id
        self.name = name
        self.deliveries = []

    def add_delivery(self, delivery):
        self.deliveries.append(delivery)





