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

        self.selected_delivery_id = None

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

        self.btn_reminders = ctk.CTkButton(self.sidebar, text="Reminders", command=self.check_notifications)
        self.btn_reminders.grid(row=5, column=0, sticky="ew", padx=20, pady=10)
        
        # Main frame
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        
      
        self.show_dashboard()
        self.after(100, self.check_notifications)  

    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        self.selected_delivery_id = None

    

    def show_dashboard(self):
        self.clear_main_frame()
        dashboard_frame = ctk.CTkFrame(self.main_frame, fg_color="#232323")
        dashboard_frame.pack(fill="both", expand=True, padx=20, pady=20)

        
        title_label = ctk.CTkLabel(dashboard_frame, text="Dashboard Overview", font=ctk.CTkFont(size=22, weight="bold"))
        title_label.pack(pady=(10, 20))

        
        charts_frame = ctk.CTkFrame(dashboard_frame, fg_color="#232323")
        charts_frame.pack(pady=10, padx=10, fill="x")

        # Pie chart 
        completed = self.db.count_deliveries(completed=1)
        pending = self.db.count_deliveries(completed=0)
        sizes = [completed, pending]
        labels = ['Completed', 'Pending']
        colors = ['#00b894', '#636e72']

        fig, ax = plt.subplots(figsize=(3.5, 3.5), dpi=100, facecolor="#232323")
        if sum(sizes) == 0:
            ax.text(0.5, 0.5, "No data", ha='center', va='center', fontsize=14, color='white')
            ax.axis('off')
        else:
            wedges, texts, autotexts = ax.pie(
                sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90,
                textprops={'color': 'white', 'fontsize': 13}, wedgeprops={'edgecolor': 'white', 'linewidth': 1.5}
            )
            for text in texts:
                text.set_color('white')
            for autotext in autotexts:
                autotext.set_color('white')
            ax.set_title('Delivery Status', color='white', fontsize=15)
        fig.patch.set_facecolor('#232323')

        canvas = FigureCanvasTkAgg(fig, master=charts_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, padx=(30, 40), pady=10)  # More horizontal padding
        plt.close(fig)

        # Bar chart 
        earnings = self.db.get_total_earnings_by_month()
        months = list(earnings.keys())
        totals = list(earnings.values())

        fig2, ax2 = plt.subplots(figsize=(4.5, 4), dpi=100, facecolor="#232323")
        if months and totals:
            bars = ax2.bar(months, totals, color='#00cec9', edgecolor='#232323', linewidth=1.5)
            ax2.set_title('Earnings by Month', color='white', fontsize=15)
            ax2.set_xlabel('Month', color='white', fontsize=12)
            ax2.set_ylabel('Total Earnings', color='white', fontsize=12)
            ax2.tick_params(axis='x', colors='white', labelrotation=30, labelsize=10)
            ax2.tick_params(axis='y', colors='white', labelsize=10)
            ax2.spines['bottom'].set_color('white')
            ax2.spines['left'].set_color('white')
            ax2.spines['top'].set_color('#232323')
            ax2.spines['right'].set_color('#232323')
            plt.subplots_adjust(bottom=0.28, left=0.18, right=0.95, top=0.85)  
            for bar in bars:
                height = bar.get_height()
                ax2.annotate(f'{height:.2f}',
                            xy=(bar.get_x() + bar.get_width() / 2, height),
                            xytext=(0, 5),
                            textcoords="offset points",
                            ha='center', va='bottom', color='white', fontsize=9)
        else:
            ax2.text(0.5, 0.5, "No data", ha='center', va='center', fontsize=14, color='white')
            ax2.axis('off')
        fig2.patch.set_facecolor('#232323')

        canvas2 = FigureCanvasTkAgg(fig2, master=charts_frame)
        canvas2.draw()
        canvas2.get_tk_widget().grid(row=0, column=1, padx=(40, 30), pady=10)  
        plt.close(fig2)

    def show_create_delivery(self):
        self.clear_main_frame()
        label = ctk.CTkLabel(self.main_frame, text="Create New Delivery", font=ctk.CTkFont(size=24, weight="bold"))
        label.pack(pady=10)

        form_frame = ctk.CTkFrame(self.main_frame)
        form_frame.pack(pady=10, padx=10, fill="x")

        # Client 
        tk.Label(form_frame, text="Client:", bg="#2b2b2b", fg="white").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.client_entry = ctk.CTkEntry(form_frame, placeholder_text="Client name")
        self.client_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        # Description
        tk.Label(form_frame, text="Description:", bg="#2b2b2b", fg="white").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.desc_entry = ctk.CTkEntry(form_frame, placeholder_text="Description")
        self.desc_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        # Fee 
        tk.Label(form_frame, text="Fee:", bg="#2b2b2b", fg="white").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.fee_entry = ctk.CTkEntry(form_frame, placeholder_text="Amount")
        self.fee_entry.grid(row=2, column=1, sticky="ew", padx=5, pady=5)

        # Deadline
        tk.Label(form_frame, text="Deadline (YYYY-MM-DD):", bg="#2b2b2b", fg="white").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.deadline_entry = DateEntry(form_frame, date_pattern="yyyy-mm-dd")
        self.deadline_entry.grid(row=3, column=1, sticky="ew", padx=5, pady=5)
        form_frame.grid_columnconfigure(1, weight=1)

        btn_create = ctk.CTkButton(self.main_frame, text="Create Delivery", command=self.create_delivery)
        btn_create.pack(pady=10)

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

    

    def show_view_deliveries(self):
        self.clear_main_frame()
        main_frame = ctk.CTkFrame(self.main_frame, fg_color="#232323")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        
        search_frame = ctk.CTkFrame(main_frame, fg_color="#232323")
        search_frame.pack(fill="x", pady=(0, 10))
        search_entry = ctk.CTkEntry(search_frame, placeholder_text="Search by client or description")
        search_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        search_button = ctk.CTkButton(search_frame, text="Search", command=lambda: self.filter_deliveries(search_entry.get()))
        search_button.pack(side="left")
        clear_button = ctk.CTkButton(search_frame, text="Clear", command=self.clear_delivery_search)
        clear_button.pack(side="left", padx=(10, 0))

        label = ctk.CTkLabel(self.main_frame, text="List of Deliveries", font=ctk.CTkFont(size=24, weight="bold"))
        label.pack(pady=10)

        
        deliveries = getattr(self, "filtered_deliveries", None)
        if deliveries is None:
            deliveries = self.db.get_all_deliveries()

        
        list_frame = ctk.CTkScrollableFrame(self.main_frame, height=350)
        list_frame.pack(fill="both", expand=True, padx=10, pady=10)

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

    def clear_delivery_search(self):
        self.filtered_deliveries = None
        self.show_view_deliveries()


    def _show_delivery_details(self, delivery: Delivery):
        
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
        self.show_invoices()

    def show_invoices(self):
        self.clear_main_frame()
        invoices = self.db.get_all_invoices()
        main_frame = ctk.CTkFrame(self.main_frame, fg_color="#232323")  # <-- parent is self.main_frame
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        headers = ["ID", "Delivery ID", "Amount", "Date", "Paid", "Actions"]
        for col, header in enumerate(headers):
            tk.Label(main_frame, text=header, bg="#232323", fg="white", font=("Arial", 11, "bold")).grid(row=0, column=col, padx=8, pady=8)

        for row_idx, invoice in enumerate(invoices, start=1):
            paid_text = "Yes" if invoice.paid else "No"
            tk.Label(main_frame, text=invoice.id, bg="#232323", fg="white").grid(row=row_idx, column=0, padx=5, pady=5)
            tk.Label(main_frame, text=invoice.delivery_id, bg="#232323", fg="white").grid(row=row_idx, column=1, padx=5, pady=5)
            tk.Label(main_frame, text=invoice.amount, bg="#232323", fg="white").grid(row=row_idx, column=2, padx=5, pady=5)
            tk.Label(main_frame, text=invoice.date, bg="#232323", fg="white").grid(row=row_idx, column=3, padx=5, pady=5)
            tk.Label(main_frame, text=paid_text, bg="#232323", fg="white").grid(row=row_idx, column=4, padx=5, pady=5)
            if not invoice.paid:
                btn_pay = ctk.CTkButton(main_frame, text="Mark as Paid", width=100,
                                        command=lambda inv_id=invoice.id: self.mark_invoice_paid(inv_id))
                btn_pay.grid(row=row_idx, column=5, padx=5, pady=5)

    def mark_invoice_paid(self, invoice_id):
        self.db.mark_invoice_paid(invoice_id)
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

        


if __name__ == "__main__":
    app = DeliveryApp()
    app.mainloop()

