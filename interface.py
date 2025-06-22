import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
from models.delivery import Delivery
from db.database import Database
import ctypes
import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkcalendar import DateEntry
import datetime

ctk.set_appearance_mode("dark")
ctk.deactivate_automatic_dpi_awareness()  
ctk.set_default_color_theme("modern-theme.json")


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
        self.selected_delivery_id = None

        self.grid_columnconfigure(0, weight=0)  
        self.grid_columnconfigure(1, weight=1)  
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="ns")
        self.sidebar.grid_rowconfigure(5, weight=1)

        # Main frame
       
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=1, sticky="nsew")
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)


        self.logo_label = ctk.CTkLabel(self.sidebar, text="DeliveryApp", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, pady=(20, 10), padx=20)

        # Sidebar buttons
        self.btn_dashboard = ctk.CTkButton(self.sidebar, text="🏠 Dashboard", command=self.show_dashboard)
        self.btn_dashboard.grid(row=1, column=0, sticky="ew", padx=20, pady=10)

        self.btn_create_delivery = ctk.CTkButton(self.sidebar, text="➕ Create Delivery", command=self.show_create_delivery)
        self.btn_create_delivery.grid(row=2, column=0, sticky="ew", padx=20, pady=10)

        self.btn_view_deliveries = ctk.CTkButton(self.sidebar, text="🚚 Deliveries", command=self.show_view_deliveries)
        self.btn_view_deliveries.grid(row=3, column=0, sticky="ew", padx=20, pady=10)

        self.btn_view_invoices = ctk.CTkButton(self.sidebar, text="💸 Invoice", command=self.show_view_invoices)
        self.btn_view_invoices.grid(row=4, column=0, sticky="ew", padx=20, pady=10)

        self.btn_reminders = ctk.CTkButton(self.sidebar, text="🔔 Reminders", command=self.check_notifications)
        self.btn_reminders.grid(row=5, column=0, sticky="ew", padx=20, pady=10)
        
        self.show_dashboard()
        self.after(100, self.check_notifications)  
        
    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        self.selected_delivery_id = None

    

    def show_dashboard(self):
        self.clear_main_frame()
        shadow = ctk.CTkFrame(self.main_frame, fg_color="#181a20", corner_radius=22)
        shadow.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.98)

        # Fuentes modernas
        font_title = ctk.CTkFont(family="Segoe UI", size=28, weight="bold")
        font_card = ctk.CTkFont(family="Segoe UI", size=16, weight="bold")

        dashboard_frame = ctk.CTkFrame(self.main_frame, fg_color="#23272f", corner_radius=20)
        dashboard_frame.pack(fill="both", expand=True, padx=30, pady=30)

        # Título principal
        label = ctk.CTkLabel(
            dashboard_frame,
            text="📊 Dashboard Overview",
            font=font_title,
            text_color="#00b894"
        )
        label.pack(pady=(24, 18), padx=16, anchor="center")

        # Tarjetas resumen
        summary_frame = ctk.CTkFrame(dashboard_frame, fg_color="#181a20", corner_radius=14)
        summary_frame.pack(fill="x", padx=16, pady=(0, 24))

        ctk.CTkLabel(summary_frame, text="Total Deliveries", font=font_card, text_color="#00b894").pack(side="left", padx=24, pady=16)
        ctk.CTkLabel(summary_frame, text=str(self.db.count_all_deliveries()), font=font_card, text_color="#ffffff").pack(side="left", padx=24, pady=16)
        ctk.CTkLabel(summary_frame, text="Completed", font=font_card, text_color="#00e676").pack(side="left", padx=24, pady=16)
        ctk.CTkLabel(summary_frame, text=str(self.db.count_completed()), font=font_card, text_color="#ffffff").pack(side="left", padx=24, pady=16)
        ctk.CTkLabel(summary_frame, text="Pending", font=font_card, text_color="#ff1744").pack(side="left", padx=24, pady=16)
        ctk.CTkLabel(summary_frame, text=str(self.db.count_pending()), font=font_card, text_color="#ffffff").pack(side="left", padx=24, pady=16)
        ctk.CTkLabel(summary_frame, text="Earnings", font=font_card, text_color="#00b894").pack(side="left", padx=24, pady=16)
        ctk.CTkLabel(summary_frame, text=f"${self.db.total_earnings():.2f}", font=font_card, text_color="#ffffff").pack(side="left", padx=24, pady=16)

        

         # Ejemplo de datos para el gráfico
        total = self.db.count_all_deliveries()
        completed = self.db.count_completed()
        pending = self.db.count_pending()
        earnings = self.db.total_earnings()
         # Crear figura matplotlib
        fig, axs = plt.subplots(1, 2, figsize=(8, 3), dpi=100)
        # Gráfico de pastel
        axs[0].pie(
            [completed, pending],
            labels=["Completed", "Pending"],
            colors=["#00e676", "#ff1744"],
            autopct="%1.1f%%",
            startangle=90
        )
        axs[0].set_title("Delivery Status")
        # Gráfico de barras
        axs[1].bar(["Earnings"], [earnings], color="#00b894")
        axs[1].set_title("Earnings")
        axs[1].set_ylabel("Total Earnings")

        plt.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=dashboard_frame)
        canvas.get_tk_widget().pack(padx=30, pady=10, fill="both", expand=True)

    def show_create_delivery(self):
        self.clear_main_frame()
        shadow = ctk.CTkFrame(self.main_frame, fg_color="#181a20", corner_radius=22)
        shadow.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.98)

    
        font_title = ctk.CTkFont(family="Segoe UI", size=28, weight="bold")
        font_label = ctk.CTkFont(family="Segoe UI", size=14)
        font_button = ctk.CTkFont(family="Segoe UI", size=12, weight="bold")

        main_frame = ctk.CTkFrame(self.main_frame, fg_color="#23272f", corner_radius=20)
        main_frame.pack(fill="both", expand=True, padx=30, pady=30)

        label = ctk.CTkLabel(
            main_frame,
            text="➕ Create New Delivery",
            font=font_title,
            text_color="#00b894"
        )
        label.grid(row=0, column=0, columnspan=2, pady=(24, 18), padx=16, sticky="w")

        ctk.CTkLabel(main_frame, text="Client:", font=font_label).grid(row=1, column=0, sticky="e", padx=16, pady=10)
        self.client_entry = ctk.CTkEntry(main_frame, font=font_label, fg_color="#3a3f47", text_color="#ffffff")
        self.client_entry.grid(row=1, column=1, sticky="w", padx=16, pady=10)

        ctk.CTkLabel(main_frame, text="Description:", font=font_label).grid(row=2, column=0, sticky="e", padx=16, pady=10)
        self.desc_entry = ctk.CTkEntry(main_frame, font=font_label,fg_color="#3a3f47", text_color="#ffffff")
        self.desc_entry.grid(row=2, column=1, sticky="w", padx=16, pady=10)

        ctk.CTkLabel(main_frame, text="Fee:", font=font_label).grid(row=3, column=0, sticky="e", padx=16, pady=10)
        self.fee_entry = ctk.CTkEntry(main_frame, font=font_label, fg_color="#3a3f47", text_color="#ffffff")
        self.fee_entry.grid(row=3, column=1, sticky="w", padx=16, pady=10)

        ctk.CTkLabel(main_frame, text="Deadline (YYYY-MM-DD):", font=font_label).grid(row=4, column=0, sticky="e", padx=16, pady=10)
        self.deadline_entry = ctk.CTkEntry(main_frame, font=font_label, fg_color="#3a3f47", text_color="#ffffff")
        self.deadline_entry.grid(row=4, column=1, sticky="w", padx=16, pady=10)

        create_btn = ctk.CTkButton(
            main_frame,
            text="Crear Delivery",
            font=font_button,
            fg_color="#00b894",
            hover_color="#0984e3",
            corner_radius=16,
            command=self.create_delivery
        )
        create_btn.grid(row=5, column=0, columnspan=2, pady=24, padx=16)

    def create_delivery(self):
        client_name = self.client_entry.get().strip()
        description = self.desc_entry.get().strip()
        deadline = self.deadline_entry.get_date().strftime("%Y-%m-%d")

        if not client_name:
            messagebox.showerror("Error", "Please enter a client name.")
            return
        if not description:
            messagebox.showerror("Error", "Please enter a description.")
            return
        if not deadline:
            messagebox.showerror("Error", "Please enter a deadline.")
            return


        clients = self.db.get_all_clients()
        client = next((c for c in clients if c.name == client_name), None)
        if not client:
            from models.client import Client
            client = Client(id=None, name=client_name)
            client.id = self.db.insert_client(client)

        fee_text = self.fee_entry.get().strip()
        try:
            fee = float(fee_text)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for the fee.")
            return

      
        new_delivery = Delivery(
            id=None,
            client_id=client.id,
            description=description,
            completed=0,
            fee=fee,
            deadline=deadline,
            completed_date=None
        )
        delivery_id = self.db.add_delivery(new_delivery)

        
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        self.db.add_invoice(delivery_id, fee, today)
        messagebox.showinfo("Success", "Delivery created successfully!")
        self.show_view_deliveries()
    

    def show_view_deliveries(self):
        self.clear_main_frame()
        shadow = ctk.CTkFrame(self.main_frame, fg_color="#181a20", corner_radius=22)
        shadow.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.98)

        # Definir fuentes modernas y consistentes
        font_title = ctk.CTkFont(family="Segoe UI", size=28, weight="bold")
        font_label = ctk.CTkFont(family="Segoe UI", size=14)
        font_button = ctk.CTkFont(family="Segoe UI", size=12, weight="bold")

        # Frame principal
        main_frame = ctk.CTkFrame(self.main_frame, fg_color="#23272f", corner_radius=20)
        main_frame.pack(fill="both", expand=True, padx=30, pady=30)

        # Título arriba, dentro de main_frame
        label = ctk.CTkLabel(
            main_frame,
            text="🚚 List of Deliveries",
            font=font_title,
            text_color="#00b894"
        )
        label.pack(pady=(24, 18), padx=16, anchor="w")

        # search frame
       
        search_frame = ctk.CTkFrame(main_frame, fg_color="#23272f")  
        search_frame.pack(fill="x", padx=16, pady=(0, 16))

        search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Search by client or description",
            fg_color="#3a3f47",  
            text_color="#ffffff"
        )
        search_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        search_button = ctk.CTkButton(search_frame, text="Search", command=lambda: self.filter_deliveries(search_entry.get()))
        search_button.pack(side="left")
        clear_button = ctk.CTkButton(search_frame, text="Clear", command=self.clear_delivery_search)
        clear_button.pack(side="left", padx=(10, 0))


        # Lista de entregas, también dentro de main_frame
        list_frame = ctk.CTkScrollableFrame(main_frame, height=350)
        list_frame.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        # obtain deliveries
        deliveries = getattr(self, "filtered_deliveries", None)
        if deliveries is None:
            deliveries = self.db.get_all_deliveries()

        if not deliveries:
            empty_label = ctk.CTkLabel(list_frame, text="No deliveries", font=font_label)
            empty_label.pack(pady=20)
            return

        for delivery in deliveries:
            item_frame = ctk.CTkFrame(
                list_frame,
                height=70,
                corner_radius=14,
                border_width=2,
                border_color="#00b894",
                fg_color="#23272f"
            )
            item_frame.pack(fill="x", pady=14, padx=16)

            # Status and color
            status_text = "Completed" if delivery.completed else "Pending"
            status_color = "#00e676" if delivery.completed else "#ff1744"
            status_label = ctk.CTkLabel(
                item_frame,
                text=status_text,
                text_color=status_color,
                font=font_label,
                width=100
            )
            status_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

            client = self.db.get_client_by_id(delivery.client_id)
            client_name = client.name if client else "Unknown"
            desc_text = f"{delivery.description} (Client: {client_name})"
            desc_label = ctk.CTkLabel(item_frame, text=desc_text, font=font_label)
            desc_label.grid(row=0, column=1, padx=10, pady=10, sticky="w")

            # Deadline
            deadline_label = ctk.CTkLabel(item_frame, text=f"Deadline: {delivery.deadline}", font=font_label)
            deadline_label.grid(row=1, column=1, padx=10, sticky="w")

            # Mark as completed button (if not already)
            if not delivery.completed:
                btn_complete = ctk.CTkButton(
                    item_frame,
                    text="✔ Completed",
                    fg_color="#00e676",
                    hover_color="#00c853",
                    font=font_button,
                    corner_radius=16
                )
                btn_complete.grid(row=1, column=2, padx=16, pady=8, sticky="e")

            item_frame.grid_columnconfigure(1, weight=1)

    def clear_delivery_search(self):
        self.filtered_deliveries = None
        self.show_view_deliveries()

    def mark_as_completed(self, delivery: Delivery):
        if messagebox.askyesno("Confirm", "Mark as completed?"):
            self.db.mark_delivery_completed(delivery.id)
            messagebox.showinfo("Success", "Delivery is completed")
            self.show_view_deliveries()

    def show_view_invoices(self):
        self.show_invoices()

    def show_invoices(self):
        self.clear_main_frame()
        shadow = ctk.CTkFrame(self.main_frame, fg_color="#181a20", corner_radius=22)
        shadow.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.98)

        font_title = ctk.CTkFont(family="Segoe UI", size=28, weight="bold")
        font_label = ctk.CTkFont(family="Segoe UI", size=14)
        font_header = ctk.CTkFont(family="Segoe UI", size=14, weight="bold")
        font_button = ctk.CTkFont(family="Segoe UI", size=12, weight="bold")

        main_frame = ctk.CTkFrame(self.main_frame, fg_color="#23272f", corner_radius=20)
        main_frame.pack(fill="both", expand=True, padx=30, pady=30)

        # Título
        label = ctk.CTkLabel(
            main_frame,
            text="💸 Invoices",
            font=font_title,
            text_color="#00b894"
        )
        label.pack(pady=(24, 18), padx=16, anchor="w")

        # Encabezados de la tabla
        headers = ["ID", "Delivery ID", "Amount", "Date", "Paid", "Actions"]
        header_frame = ctk.CTkFrame(main_frame, fg_color="#23272f")
        header_frame.pack(fill="x", padx=16, pady=(0, 8))
        for idx, header in enumerate(headers):
            ctk.CTkLabel(
                header_frame,
                text=header,
                font=font_header,
                text_color="#ffffff",
                fg_color="#23272f"
            ).grid(row=0, column=idx, padx=8, pady=4, sticky="w")

        # Lista de facturas
        invoices = self.db.get_all_invoices()
        for i, invoice in enumerate(invoices):
            row_frame = ctk.CTkFrame(main_frame, fg_color="#23272f", corner_radius=10)
            row_frame.pack(fill="x", padx=16, pady=6)

            ctk.CTkLabel(row_frame, text=str(invoice.id), font=font_label, text_color="#ffffff", fg_color="#23272f").grid(row=0, column=0, padx=8, pady=4, sticky="w")
            ctk.CTkLabel(row_frame, text=str(invoice.delivery_id), font=font_label, text_color="#ffffff", fg_color="#23272f").grid(row=0, column=1, padx=8, pady=4, sticky="w")
            ctk.CTkLabel(row_frame, text=str(invoice.amount), font=font_label, text_color="#ffffff", fg_color="#23272f").grid(row=0, column=2, padx=8, pady=4, sticky="w")
            ctk.CTkLabel(row_frame, text=str(invoice.date), font=font_label, text_color="#ffffff", fg_color="#23272f").grid(row=0, column=3, padx=8, pady=4, sticky="w")
            ctk.CTkLabel(row_frame, text="Yes" if invoice.paid else "No", font=font_label, text_color="#00e676" if invoice.paid else "#ff1744", fg_color="#23272f").grid(row=0, column=4, padx=8, pady=4, sticky="w")

            # Botón de acción
            if not invoice.paid:
                ctk.CTkButton(
                    row_frame,
                    text="💸 Mark as Paid",
                    font=font_button,
                    fg_color="#00b894",
                    hover_color="#0984e3",
                    corner_radius=16,
                    command=lambda inv=invoice: self.mark_invoice_as_paid(inv)
                ).grid(row=0, column=5, padx=8, pady=4, sticky="w")

    def mark_invoice_as_paid(self, invoice):
        self.db.mark_invoice_paid(invoice.id)
        messagebox.showinfo("Invoice", "Invoice marked as paid.")
        self.show_invoices()

    def filter_deliveries(self, query):
        query = query.lower().strip()
        all_deliveries = self.db.get_all_deliveries()
        filtered = []
        for d in all_deliveries:
            client = self.db.get_client_by_id(d.client_id)
            if (query in d.description.lower()) or (client and query in client.name.lower()):
                filtered.append(d)
        self.filtered_deliveries = filtered
        self.show_view_deliveries()

    
    def check_notifications(self):
        today = datetime.date.today().strftime("%Y-%m-%d")
        # overdue or due-today deliveries
        overdue = [d for d in self.db.get_all_deliveries() if not d.completed and d.deadline <= today]
        # unpaid invoices
        unpaid = [i for i in self.db.get_all_invoices() if not i.paid]

        messages = []
        if overdue:
            messages.append(f"You have {len(overdue)} delivery(ies) due or overdue.")
        if unpaid:
            messages.append(f"You have {len(unpaid)} unpaid invoice(s).")
        if messages:
            messagebox.showwarning("Reminders", "\n".join(messages))

    def fade_in (self, widget, step=0):
        alpha=step/10
        if alpha > 1:
            widget.attributes('-alpha', alpha)
            widget.after(30,lambda: self.fade_in(widget,step + 1))
    def slide_in(self, frame, start_x, end_x, step=10):
        if start_x < end_x:
            frame.place(x=start_x, y=0)
            self.after(10, lambda: self.slide_in(frame, start_x + step, end_x, step))
        else:
            frame.place(x=end_x, y=0)

if __name__ == "__main__":
        app = DeliveryApp()
        app.mainloop()

