import tkinter as tk
from tkinter import messagebox, simpledialog
from models.freelancer import Freelancer 
from models.client import Client
from models.delivery import Delivery
from db.database import connections, tables


def save_to_db(conn, freelancer):
    if not freelancer:
        messagebox.showerror("Error", "No freelancer data to save.")
        return

    cursor = conn.cursor()
    clients_saved = set()

    
    for delivery in freelancer.deliveries:
        if delivery.client.client_id not in clients_saved:
            cursor.execute(""" 
                INSERT OR REPLACE INTO clients (client_id, name, address)
                VALUES (?, ?, ?)
            """, (delivery.client.client_id, delivery.client.name, delivery.client.address))
            clients_saved.add(delivery.client.client_id)

        cursor.execute(""" 
            INSERT OR REPLACE INTO deliveries (delivery_id, client_id, freelancer_id, pickup_address, dropoff_address, fee, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (delivery.delivery_id, delivery.client.client_id, delivery.freelancer.freelancer_id,
              delivery.pickup_address, delivery.dropoff, delivery.fee, delivery.status))

    
    cursor.execute(""" 
        INSERT OR REPLACE INTO freelancers (freelancer_id, user_id, name, email)
        VALUES (?, ?, ?, ?)
    """, (freelancer.freelancer_id, freelancer.user_id, freelancer.name, freelancer.email))

    conn.commit()

def load_from_db(conn, freelancer_id):
    cursor=conn.cursor()

    cursor.execute("SELECT * FROM freelancers WHERE freelancer_id = ?", (freelancer_id,))
    row= cursor.fetchone()

    if row:
        freelancer= Freelancer(user_id=row[1], name=row[2], email= row[3], freelancer_id=row[0])

        cursor.execute("SELECT * FROM deliveries WHERE freelancer_id = ?", (freelancer_id, ))
        deliveries= cursor.fetchall()

        for d in deliveries:
            cursor.execute("SELECT * FROM clients WHERE client_id = ?", (d[1], ))
            c =cursor.fetchone()
            if c:
                client= Client(client_id=c[0], name=c[1], address= c[2])
                delivery= Delivery(delivery_id=d[0], client=client, freelancer=freelancer, pickup_address=d[3], dropoff=d[4], fee=d[6], status= d[5])
                freelancer.add_delivery(delivery)
        return freelancer
    return None

def create_delivery():
    global freelancer

    client_name = simpledialog.askstring("Client Info", "Client name:")
    if client_name is None:
        return

    client_address = simpledialog.askstring("Client Info", "Client address:")
    if client_address is None:
        return

    client_id = simpledialog.askstring("Client Info", "Client ID:")
    if client_id is None:
        return

    delivery_id_input = simpledialog.askstring("Delivery Info", "Delivery ID:")
    if delivery_id_input is None:
        return
    try:
        delivery_id = int(delivery_id_input)
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid number for the Delivery ID.")
        return

    pickup_address = simpledialog.askstring("Delivery Info", "Pickup address:")
    if pickup_address is None:
        return

    dropoff = simpledialog.askstring("Delivery Info", "Dropoff address:")
    if dropoff is None:
        return

    fee_input = simpledialog.askstring("Delivery Info", "Fee:")
    if fee_input is None:
        return
    try:
        fee = float(fee_input)
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid number for the fee.")
        return

    client = Client(client_id=client_id, name=client_name, address=client_address)
    delivery = Delivery(delivery_id=delivery_id, client=client, freelancer=freelancer,
                        pickup_address=pickup_address, dropoff=dropoff, fee=fee)

    freelancer.add_delivery(delivery)
    messagebox.showinfo("Success", "Delivery created.")

def update_status():
    global freelancer 
    if not freelancer.deliveries:
        messagebox.showinfo("Info", "No deliveries to update")
        return

    ids = [str(d.delivery_id) for d in freelancer.deliveries]
    d_id = simpledialog.askstring("Update", f"Delivery ID to update ({', '.join(ids)}):")
    if d_id is None:
        return

    new_status = simpledialog.askstring("Update", "New status (e.g. DELIVERED):")
    if new_status is None:
        return

    for d in freelancer.deliveries:  
        if str(d.delivery_id) == d_id:
            d.update_status(new_status)
            messagebox.showinfo("Updated", "Delivery status updated")
            return

    messagebox.showerror("Error", "Delivery ID not found")


def view_deliveries():
    global freelancer
    if not freelancer.deliveries:
        messagebox.showinfo("Deliveries", "No deliveries found")
        return
    
    output= "\n" .join([f"ID: {d.delivery_id}, Client: {d.client.name}, Status: {d.status}" for d in freelancer.deliveries])
    messagebox.showinfo("Deliveries", output)



def show_invoice():
    global freelancer
    if not freelancer:
        messagebox.showerror("Error", "No freelancer is logged in.")
        return
    if not freelancer.deliveries:
        messagebox.showinfo("Invoice", "No deliveries to calculate invoice.")
        return
    invoice = freelancer.calculate_invoice()
    messagebox.showinfo("Invoice", f"Total invoice: ${invoice:.2f}")


def exit_app():
    save_to_db(conn, freelancer)
    root.destroy()

def login():
    global freelancer
    fid = simpledialog.askstring("Login", "Enter Freelancer ID:")
    if fid is None:
        return
    try:
        fid = int(fid)
    except ValueError:
        messagebox.showerror("Invalid Input", "Freelancer ID must be a number.")
        return

    user = load_from_db(conn, freelancer_id=fid)
    if user:
        freelancer = user
        login_frame.pack_forget()
        dashboard_frame.pack()
    else:
        name = simpledialog.askstring("New Freelancer", "Name:")
        if name is None:
            return
        email = simpledialog.askstring("New Freelancer", "Email:")
        if email is None:
            return
        freelancer = Freelancer(user_id=100 + fid, name=name, email=email, freelancer_id=fid)
        messagebox.showinfo("Account Created", f"Welcome, {name}!")
        login_frame.pack_forget()
        dashboard_frame.pack()
        


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