import customtkinter as ctk
from tkinter import messagebox
from models.freelancer import Freelancer
from models.client import Client
from models.delivery import Delivery
from db.database import connections, tables, insert_freelancer, insert_client, insert_delivery

class DeliveryApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        # Initialize database
        self.conn = connections('deliveries.db')
        tables(self.conn)

        # Current freelancer model (by name)
        self.freelancer = Freelancer('TestUser', 'test@example.com')
        insert_freelancer(self.conn, self.freelancer)

        # Window configuration
        self.title("Delivery Management")
        self.geometry("900x600")
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # Build interface
        self._create_header()
        self._create_tabs()
        self._create_content_area()
        self._switch_tab("Dashboard")

    def _create_header(self):
        header = ctk.CTkFrame(self, height=80, fg_color='white')
        header.pack(fill='x')
        title = ctk.CTkLabel(
            header,
            text="Delivery\nManagement",
            font=ctk.CTkFont(size=24, weight="bold"),
            anchor='w'
        )
        title.pack(side='left', padx=20, pady=10)
        user_lbl = ctk.CTkLabel(
            header,
            text=f"Freelancer: {self.freelancer.name}",
            font=ctk.CTkFont(size=14)
        )
        user_lbl.pack(side='right', padx=20)

    def _create_tabs(self):
        self.tab_frame = ctk.CTkFrame(self, fg_color="white")
        self.tab_frame.pack(fill='x')
        self.tab_buttons = {}
        for tab in ['Dashboard', 'Create Delivery', 'Deliveries', 'Invoice']:
            btn = ctk.CTkButton(
                self.tab_frame,
                text=tab,
                width=120,
                command=lambda t=tab: self._switch_tab(t),
                fg_color="#3B82F6",
                hover_color="#2563EB"
            )
            btn.pack(side='left', padx=10, pady=10)
            self.tab_buttons[tab] = btn

    def _create_content_area(self):
        self.content_frame = ctk.CTkFrame(self, fg_color="#fdfdfd")
        self.content_frame.pack(fill='both', expand=True, padx=20, pady=10)

    def _clear_content(self):
        for w in self.content_frame.winfo_children():
            w.destroy()

    def _switch_tab(self, tab_name):
        self._clear_content()
        if tab_name == 'Dashboard':
            self._show_dashboard()
        elif tab_name == 'Create Delivery':
            self._show_create_delivery()
        elif tab_name == 'Deliveries':
            self._show_deliveries()
        elif tab_name == 'Invoice':
            self._show_invoice()

    def _show_dashboard(self):
        ctk.CTkLabel(
            self.content_frame,
            text=f"Welcome, {self.freelancer.name}!",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=20)

    def _show_create_delivery(self):
        form = ctk.CTkFrame(self.content_frame, fg_color="white")
        form.pack(pady=20, padx=20, fill='x')

        entries = {}
        fields = ["Client Name", "Client Address", "Pickup Address", "Dropoff Address", "Status", "Fee"]
        for field in fields:
            row = ctk.CTkFrame(form, fg_color="white")
            row.pack(fill='x', pady=5)
            lbl = ctk.CTkLabel(row, text=field, width=140, anchor='w')
            lbl.pack(side='left')
            ent = ctk.CTkEntry(row)
            ent.pack(side='right', fill='x', expand=True)
            entries[field] = ent

        def submit():
            vals = {k: e.get().strip() for k,e in entries.items()}
            if not all(vals.values()):
                messagebox.showerror("Error", "All fields are required.")
                return
            try:
                fee = float(vals["Fee"])
            except ValueError:
                messagebox.showerror("Error", "Fee must be a number.")
                return

            client = Client(vals["Client Name"], vals["Client Address"])
            insert_client(self.conn, client)
           
            delivery = Delivery(
                client_name=client.name,
                freelancer_name=self.freelancer.name,
                pickup_address=vals["Pickup Address"],
                dropoff_address=vals["Dropoff Address"],
                status=vals["Status"],
                fee=fee
            )
            insert_delivery(self.conn, delivery)
            self.freelancer.add_delivery(delivery)
            messagebox.showinfo("Success", "Delivery successfully created.")
            self._switch_tab('Deliveries')

        ctk.CTkButton(form, text="Create Delivery", command=submit).pack(pady=10)

    def _show_deliveries(self):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT client_name, pickup_address, dropoff_address, status, fee"
            " FROM deliveries WHERE freelancer_name = ?",
            (self.freelancer.name,)
        )
        rows = cursor.fetchall()
        if not rows:
            ctk.CTkLabel(self.content_frame, text="No deliveries.").pack(pady=20)
            return
        for client_name, pickup, dropoff, status, fee in rows:
            card = ctk.CTkFrame(self.content_frame, fg_color="white")
            card.pack(fill='x', pady=5, padx=5)
            txt = f"Client: {client_name} | Pickup: {pickup} | Dropoff: {dropoff} | Status: {status} | Fee: ${fee}"
            ctk.CTkLabel(card, text=txt).pack(side='left', padx=10)
            def updater(cn=client_name, pu=pickup, st=status, dr=dropoff, fe=fee):
                self._update_status_dialog(cn, pu)
            ctk.CTkButton(card, text="Update Status", width=150,
                          command=updater).pack(side='right', padx=10)

    def _show_invoice(self):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT SUM(fee) FROM deliveries WHERE freelancer_name = ?",
            (self.freelancer.name,)
        )
        total = cursor.fetchone()[0] or 0.0
        ctk.CTkLabel(
            self.content_frame,
            text=f"Total Invoice: ${total:.2f}",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=20)

    def _update_status_dialog(self, client_name, pickup_address):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Update Status")
        dialog.geometry("300x150")
        ctk.CTkLabel(dialog, text=f"Client: {client_name}\nPickup: {pickup_address}").pack(pady=10)
        entry = ctk.CTkEntry(dialog)
        entry.pack(pady=5, fill='x', padx=20)
        def update():
            new_status = entry.get().strip()
            if new_status:
                cursor = self.conn.cursor()
                cursor.execute(
                    "UPDATE deliveries SET status = ? WHERE client_name = ? AND freelancer_name = ? AND pickup_address = ?",
                    (new_status, client_name, self.freelancer.name, pickup_address)
                )
                self.conn.commit()
                dialog.destroy()
                self._switch_tab('Deliveries')
        ctk.CTkButton(dialog, text="Update", command=update).pack(pady=10)

if __name__ == '__main__':
    app = DeliveryApp()
    app.mainloop()
