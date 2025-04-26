class Delivery:
    def __init__(self, delivery_id, client, freelancer, pickup_address,dropoff, fee):
        self.delivery_id= delivery_id
        self.client= client
        self.freelancer= freelancer
        self.pickup_address= pickup_address
        self.dropoff= dropoff
        self.status = "PENDING"
        self.fee= fee

    def update_status(self, new_status):
        if new_status in ["PENDING", "IN TRANSIT", "DELIVERED", "CANCELLED"]:
            self.status= new_status
        else:
            print("Invallid status")