"""
Frame for creating a new delivery in the Delivery Management App.
Provides a form for user input and handles delivery creation logic.
"""

import customtkinter as ctk
from tkinter import messagebox
from tkcalendar import DateEntry


class CreateDeliveryFrame(ctk.CTkFrame):
    """
    Frame for the 'Create Delivery' view.
    """

    def __init__(self, master, controller):
        """
        Initialize the frame and create widgets.
        """
        super().__init__(master, fg_color="transparent")
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        """
        Create and layout all widgets for the delivery creation form.
        """
        font_title = ctk.CTkFont(family="Segoe UI", size=28, weight="bold")
        font_label = ctk.CTkFont(family="Segoe UI", size=14)
        font_button = ctk.CTkFont(family="Segoe UI", size=12, weight="bold")

        # Title label
        label = ctk.CTkLabel(
            self,
            text="➕ Create New Delivery",
            font=font_title,
            text_color="#00b894"
        )
        label.grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky="w")

        # Client name entry
        ctk.CTkLabel(self, text="Client:", font=font_label).grid(
            row=1, column=0, sticky="e", padx=10, pady=10
        )
        self.client_entry = ctk.CTkEntry(
            self,
            font=font_label,
            fg_color="#9DEEEE",
            text_color="#066B6B",
            border_color="#00b894",
            placeholder_text="Enter client name...",
            placeholder_text_color="#066B6B"
        )
        self.client_entry.grid(row=1, column=1, sticky="ew", padx=10, pady=10)

        # Description entry
        ctk.CTkLabel(self, text="Description:", font=font_label).grid(
            row=2, column=0, sticky="e", padx=10, pady=10
        )
        self.desc_entry = ctk.CTkEntry(
            self,
            font=font_label,
            fg_color="#9DEEEE",
            text_color="#066B6B",
            border_color="#00b894",
            placeholder_text="Enter description...",
            placeholder_text_color="#066B6B"
        )
        self.desc_entry.grid(row=2, column=1, sticky="ew", padx=10, pady=10)

        # Fee entry
        ctk.CTkLabel(self, text="Fee:", font=font_label).grid(
            row=3, column=0, sticky="e", padx=10, pady=10
        )
        self.fee_entry = ctk.CTkEntry(
            self,
            font=font_label,
            fg_color="#9DEEEE",
            text_color="#066B6B",
            border_color="#00b894",
            placeholder_text="Enter fee...",
            placeholder_text_color="#066B6B"
        )
        self.fee_entry.grid(row=3, column=1, sticky="ew", padx=10, pady=10)

        # Deadline date entry
        ctk.CTkLabel(self, text="Deadline:", font=font_label).grid(
            row=4, column=0, sticky="e", padx=10, pady=10
        )

        # Custom style for the DateEntry widget
        style = {
            'background': '#2b2b2b',
            'foreground': 'white',
            'borderwidth': 2,
            'headersbackground': '#00b894',
            'headersforeground': 'white',
            'selectbackground': '#008f7a',
            'selectforeground': 'white',
            'normalbackground': '#3b3b3b',
            'normalforeground': 'white',
            'othermonthforeground': 'gray50',
            'othermonthbackground': '#2b2b2b'
        }

        self.deadline_entry = DateEntry(
            self,
            date_pattern='y-mm-dd',
            width=18,
            **style
        )
        self.deadline_entry.grid(row=4, column=1, sticky="w", padx=10, pady=10)

        # Configure column weight for responsive layout
        self.grid_columnconfigure(1, weight=1)

        # Create Delivery button
        create_btn = ctk.CTkButton(
            self,
            text="Create Delivery",
            font=font_button,
            command=self.create_delivery_action
        )
        create_btn.grid(row=5, column=0, columnspan=2, pady=20)

    def create_delivery_action(self):
        """
        Handle the creation of a new delivery when the button is pressed.
        Validates input and shows appropriate messages.
        """
        client_name = self.client_entry.get().strip()
        description = self.desc_entry.get().strip()
        fee_text = self.fee_entry.get().strip()

        try:
            deadline = self.deadline_entry.get_date().strftime("%Y-%m-%d")
        except AttributeError:
            messagebox.showerror("Error", "Please select a valid date.")
            return

        if not all([client_name, description, fee_text]):
            messagebox.showerror("Error", "All fields must be filled.")
            if not client_name:
                self.client_entry.configure(border_color="red")
            return

        try:
            fee = float(fee_text)
            self.controller.create_delivery_with_invoice(
                client_name, description, fee, deadline
            )
            messagebox.showinfo("Success", "Delivery created successfully!")

            # Clear input fields after successful creation
            self.client_entry.delete(0, 'end')
            self.desc_entry.delete(0, 'end')
            self.fee_entry.delete(0, 'end')

        except ValueError:
            messagebox.showerror("Error", "Fee must be a valid number.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")