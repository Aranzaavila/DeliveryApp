"""
Frame for displaying and managing deliveries in the Delivery Management App.
Shows a list of deliveries as cards and allows marking as completed.
"""

import customtkinter as ctk
from tkinter import messagebox


class ViewDeliveriesFrame(ctk.CTkFrame):
    """
    Frame for the 'Deliveries List' view.
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
        Create and layout all static widgets for the deliveries view.
        """
        self.title_label = ctk.CTkLabel(
            self,
            text="🚚 Deliveries List",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#00b894"
        )
        self.title_label.pack(pady=(0, 20), padx=10, anchor="w")

        # Scrollable frame for the list of deliveries
        self.scrollable_frame = ctk.CTkScrollableFrame(
            self, fg_color="transparent"
        )
        self.scrollable_frame.pack(fill="both", expand=True, padx=10, pady=5)

    def refresh_data(self):
        """
        Request fresh data from the controller and redraw the list as cards.
        """
        # Clear old widgets
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Get new data from the controller
        deliveries_data = self.controller.get_all_deliveries_for_view()

        if not deliveries_data:
            no_data_label = ctk.CTkLabel(
                self.scrollable_frame,
                text="No deliveries found.",
                font=("Segoe UI", 14)
            )
            no_data_label.pack(pady=20)
            return

        # Loop to create each delivery card
        for data in deliveries_data:
            delivery = data["delivery"]
            client_name = data["client_name"]

            # Main card frame for this delivery
            card_frame = ctk.CTkFrame(
                self.scrollable_frame,
                border_width=2,
                border_color="#3b3b3b"
            )
            card_frame.pack(fill="x", pady=10, padx=10)

            # Configure columns inside the card
            card_frame.grid_columnconfigure(0, weight=1)  # Description/details
            card_frame.grid_columnconfigure(1, weight=0)  # Button

            # Row 0: Description
            desc_font = ctk.CTkFont(family="Segoe UI", size=16, weight="bold")
            desc_label = ctk.CTkLabel(
                card_frame,
                text=delivery.description,
                font=desc_font,
                wraplength=500,
                justify="left"
            )
            desc_label.grid(
                row=0, column=0, columnspan=2, padx=15, pady=(10, 5), sticky="w"
            )

            # Row 1: Details (Client, Deadline, Fee)
            details_font = ctk.CTkFont(family="Segoe UI", size=12)
            details_text = (
                f"👤 Client: {client_name}   |   "
                f"📅 Deadline: {delivery.deadline}   |   "
                f"💰 Fee: ${delivery.fee:.2f}"
            )
            details_label = ctk.CTkLabel(
                card_frame,
                text=details_text,
                font=details_font,
                text_color="gray60"
            )
            details_label.grid(
                row=1, column=0, columnspan=2, padx=15, pady=(0, 10), sticky="w"
            )

            # Row 2: Separator, Status, and Action Button
            separator = ctk.CTkFrame(card_frame, height=1, fg_color="#3b3b3b")
            separator.grid(
                row=2, column=0, columnspan=2, padx=15, pady=5, sticky="ew"
            )

            # Status (Pending/Completed)
            status_font = ctk.CTkFont(family="Segoe UI", size=14, weight="bold")
            status_text = "Completed" if delivery.completed else "Pending"
            status_color = "#00e676" if delivery.completed else "#ff1744"
            status_label = ctk.CTkLabel(
                card_frame,
                text=status_text,
                font=status_font,
                text_color=status_color
            )
            status_label.grid(row=3, column=0, padx=15, pady=10, sticky="w")

            # Action button (only if pending)
            if not delivery.completed:
                btn_complete = ctk.CTkButton(
                    card_frame,
                    text="✔ Mark as Completed",
                    width=150,
                    command=lambda d_id=delivery.id: self.mark_as_completed_action(d_id)
                )
                btn_complete.grid(row=3, column=1, padx=15, pady=10, sticky="e")

    def mark_as_completed_action(self, delivery_id):
        """
        Action executed when the 'Mark as Completed' button is pressed.
        """
        if messagebox.askyesno(
            "Confirm", f"Mark delivery ID {delivery_id} as completed?"
        ):
            self.controller.mark_delivery_as_completed(delivery_id)
            messagebox.showinfo("Success", "Delivery marked as completed.")
            self.refresh_data()