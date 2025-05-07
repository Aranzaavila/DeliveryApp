from models.user import User

class Freelancer(User):
    def __init__(self, user_id, name, email, freelancer_id):
        super().__init__(user_id,name, email)
        self.freelancer_id= freelancer_id
        self.deliveries=[]


    def add_delivery(self, delivery):
        self.deliveries.append(delivery)

    def view_deliveries(self):
        for delivery in self.deliveries:
            print(f"Delivery {delivery.delivery_id}: {delivery.status}")
    
    def calculate_invoice(self):
        return sum(delivery.fee for delivery in self.deliveries if delivery.status == "DELIVERED")