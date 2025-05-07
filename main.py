import tkinter as tk
from tkinter import messagebox, simpledialog
from models.freelancer import Freelancer 
from models.client import Client
from models.delivery import Delivery
from db.database import connections, tables
import sqlite3


def save_to_db(conn, freelancer):
    cursor = conn.cursor()

    clients_saved=set()
    for delivery in freelancer.deliveries:
            cursor.execute(""" INSERT OR REPLACE INTO deliveries (delivery_id, client_id,freelancer_id, pickup_address, dropoff, fee, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (delivery.delivery.id, delivery.client.client.id, delivery.freelancer.freelancer_id,
             delivery.pickup_address, delivery.dropoff, delivery.fee, delivery.status))
    
            if delivery.client.client_id not in clients_saved: 
                cursor.execute(""" INSERT OR REPLACE INTO clients (client_id, name, address) VALUES (?, ?, ?)
        """, (delivery.client.client_id, delivery.client.name, delivery.client.address))

    cursor.execute( """ INSERT OR REPLACE INTO freelancers (freelancer_id, user_id, name, email) VALUES (?, ?, ?, ?)
        """, (freelancer.freelancer_id, freelancer.user_id, freelancer.name, freelancer.email))
    conn.commit()

def load_from_db(conn, freelancer_id):
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM deliveries WHERE freelancer_id =?", (freelancer_id,))
    row= cursor.fetchone()
    if row:
        freelancer= Freelancer(user_id=row[1], name=row[2], email= row[3], freelancer_id=row[0])
        cursor.execute("SELECT * FROM deliverires WHERE freelancer_id = ?", (freelancer_id, ))
        deliveries= cursor.fetchall()
        for d in deliveries:
            cursor.execute("SELECT * FROM clients WHERE client_id = ?", (d[1],))
            c =cursor.fetchone()
            client= Client(client_id=c[0], name=c[1], address= c[2])
            delivery= Delivery(delivery_id=d[0], client=client, freelancer=freelancer, pickup_address=d[3], dropoff=d[4], fee=d[5], status= d[6])
            freelancer.add_delivery(delivery)
        return freelancer
    return None

def create_delivery():
    global freelancer
    client_name= simpledialog.askstring("Client Info", "Client name: ")
    client_address= simpledialog.askstring("Client Info", "Client address: ")
    client_id= simpledialog.askstring("Client Info", "Client ID: ")
    delivery_id= int(simpledialog.askstring("Delivery Info ", "Delivery ID: " ))
    pickup_address= simpledialog.askstring("Delivery Info ", "Pickup address: ")
    dropoff= simpledialog.askstring("Delivery Info", "Dropoff address: ")
    fee= float(simpledialog.askstring("Delivery Info", "Fee: "))

    client= Client(client_id=client_id, name=client_name, address=client_address)
    delivery= Delivery(delivery_id=delivery_id, client=client, freelancer=freelancer,
                        pickup_address=pickup_address, dropoff=dropoff, fee=fee)
    
    freelancer.add_delivery(delivery)
    messagebox.showinfo("Success", "Delivery created. ")

def update_status():
    ids=[str(d.delivery_id) for d in freelancer.deliveries]
    d_id= simpledialog.askstring("Update", f"Delivery ID to update({','.join(ids)}):")
    new_status= simpledialog.askstring("Update", "New status (e.g. DELIVERED):")
    for d in freelancer.deliveries:  
        if str(d.delivery_id)== d_id:
            d.update_status(new_status)
            messagebox.showinfo("Updated", "Delivery status updated")
            return
        messagebox.showerror("Error", "Delivry ID not found")

def view_deliveries():
    output= "\n" .join([f"ID: {d.delivery_id}, Client: {d.client.name}, Status: {d.status}" for d in freelancer.deliveries])
    messagebox.showinfo("Deliveries", output if output else "No deliveriesfound")

def show_invoice():
    invoice= freelancer.calculate_invoice()
    messagebox.showinfo("Invoice", f"Total invoice: ${invoice}")

def exit_app():
    save_to_db(conn, freelancer)
    root.destroy()

def login():
    global freelancer
    fid= simpledialog.askinteger("Login", "Enter Freelancer ID: ")
    user= load_from_db(conn, freelancer_id=fid)
    if user:
        freelancer=user
        login_frame.pack_forget()
        dashboard_frame.pack()
    else:
        name= simpledialog.askstring("New Freelancer", "Name: ")
        email= simpledialog.askstring("New Freelancer", "Email: ")
        freelancer= Freelancer(user_id=100 + fid, name=name, email=email, freelancer_id=fid)
        messagebox.showinfo("Account Created", f"Welcome, {name}!")


conn= connections('deliveries.db')
tables(conn)
freelancer=None

root=tk.Tk()
root.title("Delivery Managment")

login_frame= tk.Frame(root)
tk.Label(login_frame, text= "Welcome! ").pack(pady=10)
tk.Button(login_frame, text= "Login", width=25, command=login).pack(pady=5)
login_frame.pack()


dashboard_frame= tk.Frame(root)
tk.Label(dashboard_frame, text= "Dashboard").pack(pady=5)
tk.Button(dashboard_frame, text="Create Delivery", width=25,command=create_delivery).pack(pady=5)
tk.Button (dashboard_frame, text= "Update Delivery Status", width=25, command=update_status).pack(pady=5)
tk.Button (dashboard_frame, text= "View Deliveries", width= 25, command=view_deliveries).pack(pady=5)
tk.Button (dashboard_frame, text="Show total invoice", width=25, command=show_invoice).pack(pady=5)
tk.Button (dashboard_frame, text= "Save and exit", width=25, command=exit_app).pack(pady=5)


root.mainloop()