import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
from models.delivery import Delivery
from db.database import Database
import ctypes
import sys

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")
ctk.deactivate_automatic_dpi_awareness()  # To avoid conflict with Windows auto scaling

if sys.platform == "win32":
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass


class DeliveryApp(ctk.CTk):
    def __init__(self, db_file="my_database.db"):
        super().__init__()

        self.db_file = db_file

        self.title("Delivery Management App")
        self.geometry("1000x600")
        self.minsize(800, 500)

        self.db = Database(self.db_file)

        # Variables to select delivery
        self.selected_delivery_id = None

        # Main grid configuration
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="ns")
        self.sidebar.grid_rowconfigure(5, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar, text="DeliveryApp", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, pady=(20, 10), padx=20)

        # Sidebar buttons
        self.btn_dashboard = ctk.CTkButton(self.sidebar, text="Dashboard", command=self.show_dashboard)
        self.btn_dashboard.grid(row=1, column=0, sticky="ew", padx=20, pady=10)

        self.btn_create_delivery = ctk.CTkButton(self.sidebar, text="Create Delivery", command=self.show_create_delivery)
        self.btn_create_delivery.grid(row=2, column=0, sticky="ew", padx=20, pady=10)

        self.btn_view_deliveries = ctk.CTkButton(self.sidebar, text="Deliveries", command=self.show_view_deliveries)
        self.btn_view_deliveries.grid(row=3, column=0, sticky="ew", padx=20, pady=10)

        self.btn_view_invoices = ctk.CTkButton(self.sidebar, text="Invoice", command=self.show_view_invoices)
        self.btn_view_invoices.grid(row=4, column=0, sticky="ew", padx=20, pady=10)

        # Main content frame
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        # Show dashboard by default
        self.show_dashboard()

    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        self.selected_delivery_id = None

    def show_dashboard(self):
        self.clear_main_frame()

        label = ctk.CTkLabel(self.main_frame, text="Dashboard", font=ctk.CTkFont(size=24, weight="bold"))
        label.pack(pady=10)

        # Basic statistics
        total_deliveries = self.db.count_deliveries()
        completed_deliveries = self.db.count_deliveries(completed=True)
        pending_deliveries = total_deliveries - completed_deliveries

        stats_text = (
            f"Total Deliveries: {total_deliveries}\n"
            f"Completed Deliveries: {completed_deliveries}\n"
            f"Pending Deliveries: {pending_deliveries}"
        )
        stats_label = ctk.CTkLabel(self.main_frame, text=stats_text, font=ctk.CTkFont(size=16))
        stats_label.pack(pady=10)

    def show_create_delivery(self):
        self.clear_main_frame()

        label = ctk.CTkLabel(self.main_frame, text="Create New Delivery", font=ctk.CTkFont(size=24, weight="bold"))
        label.pack(pady=10)

        form_frame = ctk.CTkFrame(self.main_frame)
        form_frame.pack(pady=10, padx=10, fill="x")

        # Client (text entry)
        tk.Label(form_frame, text="Client:", bg="#2b2b2b", fg="white").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.client_entry = ctk.CTkEntry(form_frame, placeholder_text="Client name")
        self.client_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        form_frame.grid_columnconfigure(1, weight=1)

        tk.Label(form_frame, text="Description:", bg="#2b2b2b", fg="white").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.desc_entry = ctk.CTkEntry(form_frame)
        self.desc_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        tk.Label(form_frame, text="Deadline (YYYY-MM-DD):", bg="#2b2b2b", fg="white").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.deadline_entry = ctk.CTkEntry(form_frame)
        self.deadline_entry.grid(row=2, column=1, sticky="ew", padx=5, pady=5)

        btn_create = ctk.CTkButton(self.main_frame, text="Create Delivery", command=self.create_delivery)
        btn_create.pack(pady=10)

    def create_delivery(self):
        client_name = self.client_entry.get().strip()
        description = self.desc_entry.get().strip()
        deadline = self.deadline_entry.get().strip()

        if not client_name:
            messagebox.showerror("Error", "Please enter a client name.")
            return
        if not description:
            messagebox.showerror("Error", "Please enter a description.")
            return
        if not deadline:
            messagebox.showerror("Error", "Please enter a deadline.")
            return

        import datetime
        try:
            datetime.datetime.strptime(deadline, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Use YYYY-MM-DD")
            return

        # Check if client exists, otherwise create it
        clients = self.db.get_all_clients()
        client = next((c for c in clients if c.name == client_name), None)
        if not client:
            from models.client import Client
            client = Client(id=None, name=client_name)
            client.id = self.db.insert_client(client)

        # Create new delivery
        new_delivery = Delivery(
            id=None,
            client_id=client.id,
            description=description,
            completed=0,
            fee=0.0,
            deadline=deadline,
            completed_date=None
        )
        self.db.add_delivery(new_delivery)
        messagebox.showinfo("Success", "Delivery created successfully")

        self.show_view_deliveries()

    def show_view_deliveries(self):
        self.clear_main_frame()

        label = ctk.CTkLabel(self.main_frame, text="List of Deliveries", font=ctk.CTkFont(size=24, weight="bold"))
        label.pack(pady=10)

        # Delivery list with scroll
        list_frame = ctk.CTkScrollableFrame(self.main_frame, height=350)
        list_frame.pack(fill="both", expand=True, padx=10, pady=10)

        deliveries = self.db.get_all_deliveries()
        if not deliveries:
            empty_label = ctk.CTkLabel(list_frame, text="No deliveries")
            empty_label.pack(pady=20)
            return

        for delivery in deliveries:
            item_frame = ctk.CTkFrame(list_frame, height=60)
            item_frame.pack(fill="x", pady=5, padx=5)

            # Status and color
            status_text = "Completed" if delivery.completed else "Pending"
            status_color = "green" if delivery.completed else "red"
            status_label = ctk.CTkLabel(item_frame, text=status_text, text_color=status_color, width=80)
            status_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

            # Description and client
            client = self.db.get_client_by_id(delivery.client_id)
            client_name = client.name if client else "Unknown"
            desc_text = f"{delivery.description} (Client: {client_name})"
            desc_label = ctk.CTkLabel(item_frame, text=desc_text)
            desc_label.grid(row=0, column=1, padx=10, pady=10, sticky="w")

            # Deadline
            deadline_label = ctk.CTkLabel(item_frame, text=f"Deadline: {delivery.deadline}")
            deadline_label.grid(row=1, column=1, padx=10, sticky="w")

            # Details button
            btn_details = ctk.CTkButton(item_frame, text="Details",
                                        command=lambda d=delivery: self._show_delivery_details(d))
            btn_details.grid(row=0, column=2, padx=10, pady=10, sticky="e")

            # Mark as completed button (if not already)
            if not delivery.completed:
                btn_complete = ctk.CTkButton(item_frame, text="Completed",
                                             command=lambda d=delivery: self.mark_as_completed(d))
                btn_complete.grid(row=1, column=2, padx=10, pady=5, sticky="e")

            item_frame.grid_columnconfigure(1, weight=1)

    def _show_delivery_details(self, delivery: Delivery):
        # Popup window with delivery details
        detail_win = ctk.CTkToplevel(self)
        detail_win.title(f"Details Delivery ID {delivery.id}")
        detail_win.geometry("400x300")

        client = self.db.get_client_by_id(delivery.client_id)
        client_name = client.name if client else "Unknown"

        ctk.CTkLabel(detail_win, text=f"ID: {delivery.id}", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=5)
        ctk.CTkLabel(detail_win, text=f"Client: {client_name}").pack(pady=5)
        ctk.CTkLabel(detail_win, text=f"Description: {delivery.description}").pack(pady=5)
        ctk.CTkLabel(detail_win, text=f"Deadline: {delivery.deadline}").pack(pady=5)
        ctk.CTkLabel(detail_win, text=f"Status: {'Completed' if delivery.completed else 'Pending'}").pack(pady=5)
        if delivery.completed_date:
            ctk.CTkLabel(detail_win, text=f"Completed date: {delivery.completed_date}").pack(pady=5)

        btn_close = ctk.CTkButton(detail_win, text="Close", command=detail_win.destroy)
        btn_close.pack(pady=10)

    def mark_as_completed(self, delivery: Delivery):
        if messagebox.askyesno("Confirm", "Mark as completed?"):
            self.db.mark_delivery_completed(delivery.id)
            messagebox.showinfo("Success", "Delivery is completed")
            self.show_view_deliveries()

    def show_view_invoices(self):
        self.clear_main_frame()

        label = ctk.CTkLabel(self.main_frame, text="Invoice", font=ctk.CTkFont(size=24, weight="bold"))
        label.pack(pady=10)

        # Placeholder for invoice feature
        placeholder = ctk.CTkLabel(self.main_frame, text="Invoice feature in development")
        placeholder.pack(pady=20)


if __name__ == "__main__":
    app = DeliveryApp()
    app.mainloop()

