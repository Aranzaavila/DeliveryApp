import customtkinter as ctk
from tkinter import messagebox
import datetime
from models.freelancer import Freelancer
from models.client import Client
from models.delivery import Delivery
from db.database import connections, tables, insert_client, insert_delivery, insert_freelancer


class DeliveryApp(ctk.CTk):
    def __init__(self, freelancer, conn):
        super().__init__()
        self.conn = conn
        self.freelancer = freelancer

        self.title("Delivery Manager")
        self.geometry("1000x600")
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.sidebar = ctk.CTkFrame(self, width=150)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.pack(side="right", fill="both", expand=True)

        ctk.CTkButton(self.sidebar, text="Dashboard", command=self._show_dashboard).pack(pady=10)
        ctk.CTkButton(self.sidebar, text="Create Delivery", command=self._show_create_delivery).pack(pady=10)
        ctk.CTkButton(self.sidebar, text="Deliveries", command=self._show_deliveries).pack(pady=10)

        self._show_dashboard()

    def _switch_tab(self, tab):
        if tab == "Dashboard":
            self._show_dashboard()
        elif tab == "Create":
            self._show_create_delivery()
        elif tab == "Deliveries":
            self._show_deliveries()

    def _show_dashboard(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        title = ctk.CTkLabel(self.content_frame, text="📊 Delivery Dashboard", font=("Arial", 20, "bold"))
        title.pack(pady=10)

        scroll_frame = ctk.CTkScrollableFrame(self.content_frame, width=800, height=500)
        scroll_frame.pack(padx=20, pady=10, fill="both", expand=True)

        deliveries = Delivery.get_all(self.conn)
        for delivery in deliveries:
            client = Client.get_by_id(self.conn, delivery.client_id)

            card = ctk.CTkFrame(scroll_frame, corner_radius=12)
            card.pack(pady=10, padx=10, fill="x")

            title_label = ctk.CTkLabel(card, text=f"📦 {delivery.description}", font=("Arial", 14, "bold"))
            title_label.pack(anchor="w", padx=10, pady=5)

            client_label = ctk.CTkLabel(card, text=f"👤 Client: {client.name}")
            client_label.pack(anchor="w", padx=10)

            date_label = ctk.CTkLabel(card, text=f"📅 Deadline: {delivery.deadline}")
            date_label.pack(anchor="w", padx=10)

            status_color = "#32CD32" if delivery.status.lower() == "completed" else "#FFA500"
            status_label = ctk.CTkLabel(card, text=f"🔶 Status: {delivery.status}", text_color=status_color)
            status_label.pack(anchor="w", padx=10, pady=(0, 5))

            mark_completed_button = ctk.CTkButton(card, text="Mark as Completed", width=150, command=lambda d=delivery: self._mark_completed(d.id))
            mark_completed_button.pack(anchor="e", padx=10, pady=5)

    def show_delivery_detail_popup(self, delivery):
        client = Client.get_by_id(self.conn, delivery.client_id)

        popup = ctk.CTkToplevel(self)
        popup.title("Delivery Details")
        popup.geometry("400x300")

        ctk.CTkLabel(popup, text="📦 Delivery Details", font=("Arial", 16, "bold")).pack(pady=10)

        ctk.CTkLabel(popup, text=f"Description: {delivery.description}").pack(anchor="w", padx=20, pady=5)
        ctk.CTkLabel(popup, text=f"Client: {client.name}").pack(anchor="w", padx=20, pady=5)
        ctk.CTkLabel(popup, text=f"Deadline: {delivery.deadline}").pack(anchor="w", padx=20, pady=5)
        ctk.CTkLabel(popup, text=f"Status: {delivery.status}").pack(anchor="w", padx=20, pady=5)

        ctk.CTkButton(popup, text="Close", command=popup.destroy).pack(pady=15)

    def clear_tab(self, tab):
        for widget in tab.winfo_children():
            widget.destroy()

    def _show_create_delivery(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.content_frame, text="Create New Delivery", font=ctk.CTkFont(size=18, weight="bold")).pack(anchor='w', pady=(10, 20), padx=30)

        form = ctk.CTkFrame(self.content_frame, fg_color="#444444")
        form.pack(fill='x', padx=10)

        entries = {}
        fields = ["Client Name", "Description", "Status", "Fee", "Deadline"]
        for field in fields:
            row = ctk.CTkFrame(form, fg_color="#444444")
            row.pack(fill='x', pady=7)
            ctk.CTkLabel(row, text=field, text_color="white", width=180, anchor='w').pack(side='left')
            entry = ctk.CTkEntry(row)
            entry.pack(side='right', fill='x', expand=True)
            entries[field] = entry

        now = datetime.datetime.now()
        entries["Deadline"].insert(0, now.strftime('%Y-%m-%d %H:%M'))

        def submit():
            vals = {k: e.get().strip() for k, e in entries.items()}
            if not all(vals.values()):
                messagebox.showerror("Error", "All fields are required.")
                return
            try:
                fee = float(vals["Fee"])
            except ValueError:
                messagebox.showerror("Error", "Fee must be a number.")
                return

            try:
                datetime.datetime.strptime(vals["Deadline"], "%Y-%m-%d %H:%M")
            except ValueError:
                messagebox.showerror("Error", "Deadline format must be YYYY-MM-DD HH:MM.")
                return

            client = Client(vals["Client Name"], "")
            insert_client(self.conn, client)
            client_id = Client.get_id_by_name(self.conn, client.name)

            delivery = Delivery(
                None,
                client_id,
                vals["Description"],
                vals["Status"],
                fee,
                vals["Deadline"]
            )

            insert_delivery(self.conn, delivery)
            messagebox.showinfo("Success", "Delivery successfully created.")
            self._switch_tab("Deliveries")

        ctk.CTkButton(self.content_frame, text="Create Delivery", command=submit).pack(pady=20)

    def _show_deliveries(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.content_frame, text="My Deliveries", font=("Helvetica", 20, "bold")).pack(pady=10)

        table_frame = ctk.CTkScrollableFrame(self.content_frame, corner_radius=10)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        headers = ["Client", "Description", "Status", "Fee", "Deadline"]
        for col, text in enumerate(headers):
            label = ctk.CTkLabel(table_frame, text=text, font=("Helvetica", 14, "bold"),
                                 text_color="white", fg_color="#3b3b3b", corner_radius=6, padx=10, pady=5)
            label.grid(row=0, column=col, padx=5, pady=5, sticky="nsew")

        cursor = self.conn.cursor()
        cursor.execute("SELECT id, client_id, description, status, fee,  deadline FROM deliveries ORDER BY deadline ASC")
        deliveries = cursor.fetchall()

        now= datetime.datetime.now()

        for i, delivery in enumerate(deliveries, start=1):
            delivery_id, client_id, description, status, fee, deadline_str = delivery
            client = Client.get_by_id(self.conn, client_id)
            client_name = client.name if client else "Unknown"

            deadline_dt= datetime.datetime.strptime(deadline_str, "%Y-%m-%d %H:%M")
            time_diff= deadline_dt - now
            urgency_icon= "🔥" if time_diff.total_seconds() < 86400 else ""

            if time_diff.total_seconds() < 86400:
                bg_color= "#F04040" #urgent
            elif time_diff.total_seconds() < 3 * 86400:
                bg_color= "#ECD928" #moderate
            else:
                bg_color= "#1FF331" #there is still time

            data = [client_name, description, status, f"${fee:.2f}", f"{deadline_str} {urgency_icon}"]
            
            for j, value in enumerate(data):
                label = ctk.CTkLabel(table_frame, text=str(value), font=("Helvetica", 12),
                                     fg_color=bg_color, text_color="#000000", corner_radius=4, padx=8, pady=4)
                label.grid(row=i, column=j, padx=4, pady=2, sticky="nsew")

            action_btn = ctk.CTkButton(table_frame, text="Mark Completed",
                                       command=lambda d_id=delivery_id: self._mark_completed(d_id),
                                       width=120, height=28)
            action_btn.grid(row=i, column=len(data), padx=5, pady=5)

        for col in range(len(headers)):
            table_frame.grid_columnconfigure(col, weight=1)

    def _mark_completed(self, delivery_id):
        cursor = self.conn.cursor()
        cursor.execute("UPDATE deliveries SET status = 'COMPLETED' WHERE id = ?", (delivery_id,))
        self.conn.commit()
        messagebox.showinfo("Updated", "Delivery marked as completed.")
        self._show_deliveries()


if __name__ == "__main__":
    conn = connections("deliveries.db")
    tables(conn)
    f = Freelancer("TestUser", "test@example.com")
    app = DeliveryApp(f, conn)
    app.mainloop()
