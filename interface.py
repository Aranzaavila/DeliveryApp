import customtkinter as ctk
from tkinter import messagebox
import datetime
from models.freelancer import Freelancer
from models.client import Client
from models.delivery import Delivery
from db.database import connections, tables, insert_freelancer, insert_client, insert_delivery

class DeliveryApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.conn = connections('deliveries.db')
        tables(self.conn)

        self.freelancer = Freelancer('TestUser', 'test@example.com')
        insert_freelancer(self.conn, self.freelancer)

        self.title("Delivery Management")
        self.geometry("950x600")
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self._create_header()
        self._create_tabs()
        self._create_content_area()
        self._switch_tab("Dashboard")

    def _create_header(self):
        header = ctk.CTkFrame(self, height=80, fg_color='white')
        header.pack(fill='x', pady=(0, 1))

        title = ctk.CTkLabel(header, text="Delivery\nManagement", font=ctk.CTkFont(size=22, weight="bold"), anchor='w')
        title.pack(side='left', padx=20, pady=10)

        right = ctk.CTkFrame(header, fg_color='white')
        right.pack(side='right', padx=20, pady=10)

        self.theme_toggle = ctk.CTkSwitch(right, text="Dark Mode", command=self._toggle_theme)
        self.theme_toggle.pack(anchor='e')

        user_lbl = ctk.CTkLabel(right, text=f"Freelancer: {self.freelancer.name}", font=ctk.CTkFont(size=14))
        user_lbl.pack(anchor='e')

    def _toggle_theme(self):
        mode = ctk.get_appearance_mode()
        ctk.set_appearance_mode("dark" if mode == "light" else "light")

    def _create_tabs(self):
        self.tab_frame = ctk.CTkFrame(self, fg_color='white')
        self.tab_frame.pack(fill='x')

        self.tab_buttons = {}
        for tab in ['Dashboard', 'Create Delivery', 'Deliveries', 'Invoice']:
            btn = ctk.CTkButton(
                self.tab_frame, text=tab, width=140,
                fg_color='white', text_color='black',
                hover_color="#e0e0e0", corner_radius=0,
                command=lambda t=tab: self._switch_tab(t)
            )
            btn.pack(side='left', padx=(0, 1), pady=5)
            self.tab_buttons[tab] = btn

    def _highlight_tab(self, active):
        for tab, btn in self.tab_buttons.items():
            if tab == active:
                btn.configure(fg_color='#3B82F6', text_color='white')
            else:
                btn.configure(fg_color='white', text_color='black')

    def _create_content_area(self):
        self.content_frame = ctk.CTkFrame(self, fg_color='#fdfdfd')
        self.content_frame.pack(fill='both', expand=True, padx=20, pady=10)

    def _clear_content(self):
        for w in self.content_frame.winfo_children():
            w.destroy()

    def _switch_tab(self, tab_name):
        self._highlight_tab(tab_name)
        self._clear_content()
        if tab_name == 'Dashboard':
            self._show_dashboard()
        elif tab_name == 'Create Delivery':
            self._show_create_delivery()
        elif tab_name == 'Deliveries':
            self._show_deliveries()
        elif tab_name == 'Invoice':
            ctk.CTkLabel(self.content_frame, text="Invoice summary coming soon...").pack(pady=20)

    def _show_dashboard(self):
        ctk.CTkLabel(self.content_frame, text="Dashboard Overview", font=ctk.CTkFont(size=20, weight="bold")).pack(anchor='w', pady=(0, 20))

        stat_row = ctk.CTkFrame(self.content_frame, fg_color='white')
        stat_row.pack(fill='x', padx=10, pady=10)

        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM deliveries WHERE freelancer_name = ?", (self.freelancer.name,))
        total_deliveries = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM deliveries WHERE freelancer_name = ? AND status = 'Completed'", (self.freelancer.name,))
        completed = cursor.fetchone()[0]
        cursor.execute("SELECT SUM(fee) FROM deliveries WHERE freelancer_name = ?", (self.freelancer.name,))
        earnings = cursor.fetchone()[0] or 0

        for label, value in [("Total Deliveries", total_deliveries), ("Completed", completed), ("Earnings ($)", f"{earnings:.2f}")]:
            stat_box = ctk.CTkFrame(stat_row, fg_color="#f0f0f0")
            stat_box.pack(side='left', expand=True, fill='both', padx=10)
            ctk.CTkLabel(stat_box, text=label, font=ctk.CTkFont(size=14)).pack(pady=(10, 0))
            ctk.CTkLabel(stat_box, text=str(value), font=ctk.CTkFont(size=18, weight='bold')).pack(pady=(0, 10))

    def _show_create_delivery(self):
        ctk.CTkLabel(self.content_frame, text="Create New Delivery", font=ctk.CTkFont(size=18, weight="bold")).pack(anchor='w', pady=(0, 20))

        form = ctk.CTkFrame(self.content_frame, fg_color="white")
        form.pack(fill='x', padx=10)

        entries = {}
        fields = ["Client Name", "Pickup Address", "Dropoff Address", "Status", "Fee", "Delivery Date", "Delivery Time"]
        for field in fields:
            row = ctk.CTkFrame(form, fg_color="white")
            row.pack(fill='x', pady=4)
            ctk.CTkLabel(row, text=field, width=130, anchor='w').pack(side='left')
            entry = ctk.CTkEntry(row)
            entry.pack(side='right', fill='x', expand=True)
            entries[field] = entry

        now = datetime.datetime.now()
        entries["Delivery Date"].insert(0, now.strftime('%Y-%m-%d'))
        entries["Delivery Time"].insert(0, now.strftime('%H:%M'))

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

            client = Client(vals["Client Name"], vals["Pickup Address"])
            insert_client(self.conn, client)
            delivery = Delivery(client.name, self.freelancer.name, vals["Pickup Address"], vals["Dropoff Address"], vals["Status"], fee, vals["Delivery Date"], vals["Delivery Time"])
            insert_delivery(self.conn, delivery)
            self.freelancer.add_delivery(delivery)
            messagebox.showinfo("Success", "Delivery successfully created.")
            self._switch_tab("Deliveries")

        ctk.CTkButton(form, text="Create Delivery", command=submit).pack(pady=15)

    def _show_deliveries(self):
        ctk.CTkLabel(self.content_frame, text="Deliveries", font=ctk.CTkFont(size=18, weight="bold")).pack(anchor='w', pady=(0, 10))

        cursor = self.conn.cursor()
        cursor.execute("SELECT id, client_name, pickup_address, dropoff_address, status, fee, delivery_date, delivery_time FROM deliveries WHERE freelancer_name = ?", (self.freelancer.name,))
        rows = cursor.fetchall()

        if not rows:
            ctk.CTkLabel(self.content_frame, text="No deliveries yet.").pack(pady=20)
            return

        for row in rows:
            card = ctk.CTkFrame(self.content_frame, fg_color='white')
            card.pack(fill='x', pady=5, padx=5)
            details = (f"ID: {row[0]} | Client: {row[1]} | Pickup: {row[2]} | Dropoff: {row[3]} | Status: {row[4]} | "
                       f"Fee: ${row[5]} | Date: {row[6]} | Time: {row[7]}")
            ctk.CTkLabel(card, text=details, wraplength=700, justify='left').pack(side='left', padx=10, pady=5)
            ctk.CTkButton(card, text="Update Status", width=120, command=lambda cn=row[1], pu=row[2]: self._update_status_dialog(cn, pu)).pack(side='right', padx=10)

    def _update_status_dialog(self, client_name, pickup_address):
        top = ctk.CTkToplevel(self)
        top.title("Update Delivery Status")
        top.geometry("350x180")

        ctk.CTkLabel(top, text="Update Status", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
        entry = ctk.CTkEntry(top, placeholder_text="New Status (e.g., Completed)")
        entry.pack(pady=10, padx=20)

        def update():
            new_status = entry.get().strip()
            if not new_status:
                messagebox.showerror("Error", "Please enter a status.")
                return
            cursor = self.conn.cursor()
            cursor.execute("UPDATE deliveries SET status = ? WHERE client_name = ? AND pickup_address = ?", (new_status, client_name, pickup_address))
            self.conn.commit()
            messagebox.showinfo("Success", f"Status updated to '{new_status}'")
            top.destroy()
            self._switch_tab("Deliveries")

        ctk.CTkButton(top, text="Update", command=update).pack(pady=10)

if __name__ == "__main__":
    app = DeliveryApp()
    app.mainloop()