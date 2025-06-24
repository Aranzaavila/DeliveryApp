"""
Frame for displaying and managing deliveries in the Delivery Management App.
Shows a list of deliveries as cards and allows marking as completed.
"""

import customtkinter as ctk
from tkinter import messagebox
import datetime


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

            # Calculate card color based on deadline and completion
            deadline_date = datetime.datetime.strptime(delivery.deadline, "%Y-%m-%d").date()
            today = datetime.date.today()
            if not delivery.completed:
                if deadline_date < today:
                    card_color = "#ffcccc"  # Overdue
                elif deadline_date <= today + datetime.timedelta(days=1):
                    card_color = "#fff3cd"  # Due soon
                else:
                    card_color = "#2b2b2b"  # Normal
            else:
                card_color = "#ccffcc"      # Completed

            # Main card frame for this delivery
            card_frame = ctk.CTkFrame(
                self.scrollable_frame,
                border_width=2,
                border_color="#3b3b3b",
                fg_color=card_color
            )
            card_frame.pack(fill="x", pady=10, padx=10)

            # Configure columns inside the card
            card_frame.grid_columnconfigure(0, weight=1)  # Description/details
            for i in range(1, 6):
                card_frame.grid_columnconfigure(1, weight=0)  # Button

            # Row 0: Description
            desc_font = ctk.CTkFont(family="Segoe UI", size=16, weight="bold")
            desc_label = ctk.CTkLabel(
                card_frame,
                text=delivery.description,
                font=desc_font,
                justify="left"
            )
            desc_label.grid(
                row=0, column=0, columnspan=6, padx=15, pady=(10, 5), sticky="ew"
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
                row=1, column=0, columnspan=6, padx=15, pady=(0, 10), sticky="ew"
            )

            # Row 2: Separator
            separator = ctk.CTkFrame(card_frame, height=1, fg_color="#3b3b3b")
            separator.grid(
                row=2, column=0, columnspan=5, padx=15, pady=5, sticky="ew"
            )

            # Row 3: Status
            status_font = ctk.CTkFont(family="Segoe UI", size=14, weight="bold")
            status_text = "Completed" if delivery.completed else "Pending"
            status_color = "#00e676" if delivery.completed else "#ff1744"
            status_label = ctk.CTkLabel(
                card_frame,
                text=status_text,
                font=status_font,
                text_color=status_color,
                anchor="w"
            )
            status_label.grid(row=3, column=0, columnspan=6, padx=25, pady=10, sticky="w")

            # Row 4: Action buttons (start at column=0)
            col = 0
            if not delivery.completed:
                btn_complete = ctk.CTkButton(
                    card_frame,
                    text="✔ Mark as Completed",
                    width=150,
                    command=lambda d_id=delivery.id: self.mark_as_completed_action(d_id)
                )
                btn_complete.grid(row=4, column=col, padx=5, pady=10, sticky="e")
                col += 1

            btn_delete = ctk.CTkButton(
                card_frame,
                text="🗑 Delete",
                fg_color="#ff1744",
                command=lambda d_id=delivery.id: self.delete_delivery_action(d_id)
            )
            btn_delete.grid(row=4, column=col, padx=5, pady=10, sticky="e")
            col += 1

            btn_edit = ctk.CTkButton(
                card_frame,
                text="✏️ Edit",
                fg_color="#00b894",
                command=lambda d=delivery: self.edit_delivery_action(d)
            )
            btn_edit.grid(row=4, column=col, padx=5, pady=10, sticky="e")
            col += 1

            btn_history = ctk.CTkButton(
                card_frame,
                text="📜 History",
                fg_color="#3498db",
                command=lambda d_id=delivery.id: self.show_history_action(d_id)
            )
            btn_history.grid(row=4, column=col, padx=5, pady=10, sticky="e")

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

    def delete_delivery_action(self, delivery_id):
        """
        Action to delete a delivery
        """
        if messagebox.askyesno("Confirm", "Delete this delivery?"):
            self.controller.delete_delivery(delivery_id)
            messagebox.showinfo("Delivery deleted")
            self.refresh_data()

    def edit_delivery_action(self, delivery):
        """
        Open a popup window to edit a delivery's details.
        """
        ctk.set_default_color_theme("blue")
        popup = ctk.CTkToplevel(self)
        popup.title("Edit Delivery")
        popup.grab_set()
        popup.focus_force()
        popup.geometry("350x250")


        # Description
        ctk.CTkLabel(popup, text="Description:").pack(pady=(10, 0))
        desc_entry = ctk.CTkEntry(popup)
        desc_entry.insert(0, delivery.description)
        desc_entry.pack()

        # Fee
        ctk.CTkLabel(popup, text="Fee:").pack(pady=(10, 0))
        fee_entry = ctk.CTkEntry(popup)
        fee_entry.insert(0, str(delivery.fee))
        fee_entry.pack()

        # Deadline
        ctk.CTkLabel(popup, text="Deadline (YYYY-MM-DD):").pack(pady=(10, 0))
        deadline_entry = ctk.CTkEntry(popup)
        deadline_entry.insert(0, delivery.deadline)
        deadline_entry.pack()

        def save_changes():
            new_desc = desc_entry.get().strip()
            try:
                new_fee = float(fee_entry.get().strip())
            except ValueError:
                messagebox.showerror("Error", "Fee must be a number.")
                return
            new_deadline = deadline_entry.get().strip()
            if not (new_desc and new_deadline):
                messagebox.showerror("Error", "All fields are required.")
                return
            self.controller.update_delivery(delivery.id, new_desc, new_fee, new_deadline)
            messagebox.showinfo("Success", "Delivery updated successfully.")
            popup.destroy()
            self.refresh_data()

        save_btn = ctk.CTkButton(popup, text="Save", command=save_changes)
        save_btn.pack(pady=20)

    def show_history_action(self, delivery_id):
        """
        Show a popup window with the change history for a delivery.
        """
        history = self.controller.db.get_delivery_history(delivery_id)
        popup = ctk.CTkToplevel(self)
        popup.title("Change History")
        popup.geometry("350x250")
        popup.grab_set()
        popup.focus_force()
        if not history:
            ctk.CTkLabel(popup, text="No history found.").pack(pady=20)
        else:
            for action, timestamp in history:
                ctk.CTkLabel(popup, text=f"{timestamp}: {action}").pack(anchor="w", padx=10, pady=2)