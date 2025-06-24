"""
Frame for displaying and managing invoices in the Delivery Management App.
Shows a list of invoices with status and allows marking as paid.
"""

import customtkinter as ctk
from tkinter import messagebox


class InvoiceFrame(ctk.CTkFrame):
    """
    Frame for the 'Invoices' view.
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
        Create and layout all widgets for the invoices view.
        """
        self.title_label = ctk.CTkLabel(
            self,
            text="💸 Invoices",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#00b894"
        )
        self.title_label.pack(pady=(0, 20), padx=10, anchor="w")

        self.scrollable_frame = ctk.CTkScrollableFrame(
            self, fg_color="transparent"
        )
        self.scrollable_frame.pack(fill="both", expand=True, padx=10, pady=5)

    def refresh_data(self):
        """
        Request fresh data from the controller and redraw the invoice list.
        """
        # Clear previous widgets
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        invoices_data = self.controller.get_invoices_for_view()

        if not invoices_data:
            no_data_label = ctk.CTkLabel(
                self.scrollable_frame,
                text="No invoices found.",
                font=("Segoe UI", 14)
            )
            no_data_label.pack(pady=20)
            return

        # Draw each invoice as a card
        for data in invoices_data:
            invoice = data["invoice"]

            # Card frame for each invoice
            card_frame = ctk.CTkFrame(
                self.scrollable_frame, border_width=2, border_color="#3b3b3b"
            )
            card_frame.pack(fill="x", pady=10, padx=10)
            card_frame.grid_columnconfigure(0, weight=1)

            # Header with invoice ID, amount, and status
            header_frame = ctk.CTkFrame(card_frame, fg_color="transparent")
            header_frame.grid(row=0, column=0, padx=15, pady=(10, 5), sticky="ew")
            header_frame.grid_columnconfigure(1, weight=1)

            id_font = ctk.CTkFont(family="Segoe UI", size=18, weight="bold")
            ctk.CTkLabel(
                header_frame, text=f"Invoice #{invoice.id}", font=id_font
            ).grid(row=0, column=0, sticky="w")

            amount_font = ctk.CTkFont(family="Segoe UI", size=18)
            ctk.CTkLabel(
                header_frame, text=f"${invoice.amount:.2f}", font=amount_font
            ).grid(row=0, column=1, sticky="w", padx=20)

            status_font = ctk.CTkFont(family="Segoe UI", size=14, weight="bold")
            status_text = "Paid" if invoice.paid else "Pending"
            status_color = "#00e676" if invoice.paid else "#ff1744"
            status_label_frame = ctk.CTkFrame(
                header_frame, fg_color=status_color, corner_radius=8
            )
            status_label_frame.grid(row=0, column=2, sticky="e")
            ctk.CTkLabel(
                status_label_frame, text=status_text, font=status_font, padx=10, pady=2
            ).pack()

            # Separator line
            separator = ctk.CTkFrame(card_frame, height=1, fg_color="#3b3b3b")
            separator.grid(row=1, column=0, padx=15, pady=5, sticky="ew")

            # Details: delivery description and client name
            details_font = ctk.CTkFont(family="Segoe UI", size=12)
            ctk.CTkLabel(
                card_frame,
                text=f'For Delivery: "{data["delivery_desc"]}"',
                font=details_font,
                text_color="gray70"
            ).grid(row=2, column=0, padx=15, sticky="w")
            ctk.CTkLabel(
                card_frame,
                text=f"👤 Client: {data['client_name']}",
                font=details_font,
                text_color="gray70"
            ).grid(row=3, column=0, padx=15, pady=(0, 10), sticky="w")

            # Footer with issue date and pay button if not paid
            footer_frame = ctk.CTkFrame(card_frame, fg_color="transparent")
            footer_frame.grid(row=4, column=0, padx=15, pady=10, sticky="ew")
            footer_frame.grid_columnconfigure(0, weight=1)

            ctk.CTkLabel(
                footer_frame,
                text=f"Issued: {invoice.date}",
                font=details_font,
                text_color="gray60"
            ).grid(row=0, column=0, sticky="w")

            if not invoice.paid:
                pay_button = ctk.CTkButton(
                    footer_frame,
                    text="💸 Mark as Paid",
                    width=140,
                    command=lambda inv_id=invoice.id: self.mark_as_paid_action(inv_id)
                )
                pay_button.grid(row=0, column=1, sticky="e")

    def mark_as_paid_action(self, invoice_id):
        """
        Action executed when the 'Mark as Paid' button is pressed.
        """
        if messagebox.askyesno("Confirm", f"Mark invoice ID {invoice_id} as paid?"):
            self.controller.mark_invoice_as_paid(invoice_id)
            messagebox.showinfo("Success", "Invoice marked as paid.")
            self.refresh_data()
