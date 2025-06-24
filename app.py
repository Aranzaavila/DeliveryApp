"""
Main application file for the Delivery Management App.
Initializes the main window and handles navigation between views.
"""

import customtkinter as ctk
from tkinter import messagebox

from controller import AppController
from views.dashboard_frame import DashboardFrame
from views.create_delivery_frame import CreateDeliveryFrame
from views.view_deliveries_frame import ViewDeliveriesFrame
from views.invoice_frame import InvoiceFrame

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("modern-theme.json")


class DeliveryApp(ctk.CTk):
    """
    Main application class for the Delivery Management App
    Handles navigation, view management, and reminders
    """

    def __init__(self, controller: AppController):
        super().__init__()
        self.controller = controller

        self.title("Delivery Management App")
        self.geometry("1000x600")
        self.minsize(800, 500)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar setup
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="ns")
        self.sidebar.grid_rowconfigure(5, weight=1)

        self.logo_label = ctk.CTkLabel(
            self.sidebar,
            text="DeliveryApp",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.logo_label.grid(row=0, column=0, pady=(20, 10), padx=20)

        self.btn_dashboard = ctk.CTkButton(
            self.sidebar, text="🏠 Dashboard",
            command=self.show_dashboard_view
        )
        self.btn_dashboard.grid(row=1, column=0, sticky="ew", padx=20, pady=10)

        self.btn_create_delivery = ctk.CTkButton(
            self.sidebar, text="➕ Create Delivery",
            command=self.show_create_delivery_view
        )
        self.btn_create_delivery.grid(row=2, column=0, sticky="ew", padx=20, pady=10)

        self.btn_view_deliveries = ctk.CTkButton(
            self.sidebar, text="🚚 Deliveries",
            command=self.show_view_deliveries_view
        )
        self.btn_view_deliveries.grid(row=3, column=0, sticky="ew", padx=20, pady=10)

        self.btn_view_invoices = ctk.CTkButton(
            self.sidebar, text="💸 Invoice",
            command=self.show_invoices_view
        )
        self.btn_view_invoices.grid(row=4, column=0, sticky="ew", padx=20, pady=10)

        self.btn_reminders = ctk.CTkButton(
            self.sidebar, text="🔔 Reminders",
            command=self.check_reminders
        )
        self.btn_reminders.grid(row=5, column=0, sticky="ew", padx=20, pady=10)

        # Main content area for views
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Dictionary to store view instances
        self.frames = {}

        # Instantiate and store each view frame
        for F in (
            DashboardFrame,
            CreateDeliveryFrame,
            ViewDeliveriesFrame,
            InvoiceFrame
        ):
            frame_name = F.__name__
            frame = F(master=self.main_frame, controller=self.controller)
            self.frames[frame_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_dashboard_view()
        self.after(2000, self.check_reminders)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def show_frame(self, frame_name):
        """
        Bring the specified frame to the front.
        Refresh data if the frame supports it.
        """
        frame = self.frames[frame_name]
        if hasattr(frame, "refresh_data"):
            frame.refresh_data()
        frame.tkraise()

    def show_dashboard_view(self):
        """Show the dashboard view."""
        self.show_frame("DashboardFrame")

    def show_create_delivery_view(self):
        """Show the create delivery view."""
        self.show_frame("CreateDeliveryFrame")

    def show_view_deliveries_view(self):
        """Show the deliveries view."""
        self.show_frame("ViewDeliveriesFrame")

    def show_invoices_view(self):
        """Show the invoices view."""
        self.show_frame("InvoiceFrame")

    def check_reminders(self):
        """Check for reminders and display them as a warning if any exist."""
        messages = self.controller.get_reminders()
        if messages:
            messagebox.showwarning("Reminders", messages)

    def on_closing(self):
        """Handle cleanup and close the application."""
        self.destroy()
