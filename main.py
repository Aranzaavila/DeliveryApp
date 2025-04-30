from models.freelancer import Freelancer 
from models.client import Client
from models.delivery import Delivery
from db.database import connections, tables

def main():
    conn= connections('deliveries.db')
    tables(conn)

    freelancer = Freelancer(user_id=133, name= "Andrea Avila", email= "andrea@example.com", freelancer_id= 1045 )
    client= Client(client_id= 12, name= "John", address= "32 Warschauer St.")
    delivery= Delivery(delivery_id= 222, client=client, freelancer=freelancer, pickup_address="Warehouse A", dropoff= "Client Address", fee= 10.0)

    freelancer.add_delivery(delivery)

    print("=== Deliveries ===")
    freelancer.view_deliveries()

    delivery.update_status("DELIVERED")
    print(f"Total revenue: ${freelancer.calculate_revenue()}")

if __name__ == "__main__":
    main()
