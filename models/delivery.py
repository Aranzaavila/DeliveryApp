class Delivery:
    def __init__(self, client_name, freelancer_name, pickup_address, dropoff_address, status, fee, delivery_date, delivery_time):
        self.client_name = client_name
        self.freelancer_name = freelancer_name
        self.pickup_address = pickup_address
        self.dropoff_address = dropoff_address
        self.status = status
        self.fee = fee
        self.delivery_date = delivery_date  
        self.delivery_time = delivery_time  

    def __repr__(self):
        return (f"Delivery({self.client_name}, {self.freelancer_name}, {self.pickup_address}, "
                f"{self.dropoff_address}, {self.status}, {self.fee}, {self.delivery_date}, {self.delivery_time})")


