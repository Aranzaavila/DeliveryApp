# views/view_deliveries_frame.py

import customtkinter as ctk
from tkinter import messagebox

class ViewDeliveriesFrame(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master, fg_color="transparent")
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        """Crea los elementos estáticos de la UI."""
        self.title_label = ctk.CTkLabel(self, text="🚚 Deliveries List", font=ctk.CTkFont(size=28, weight="bold"), text_color="#00b894")
        self.title_label.pack(pady=(0, 20), padx=10, anchor="w")

        # Aquí irá la lista de entregas
        self.scrollable_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scrollable_frame.pack(fill="both", expand=True, padx=10, pady=5)

    # En: views/view_deliveries_frame.py

# ... (el __init__ y create_widgets se quedan igual) ...

    def refresh_data(self):
        """Pide datos frescos al controller y redibuja la lista con el nuevo diseño de tarjetas."""
        # Limpiar filas antiguas
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Pedir datos nuevos al controller
        deliveries_data = self.controller.get_all_deliveries_for_view()

        if not deliveries_data:
            no_data_label = ctk.CTkLabel(self.scrollable_frame, text="No deliveries found.", font=("Segoe UI", 14))
            no_data_label.pack(pady=20)
            return

        # --- Bucle para crear cada TARJETA de entrega ---
        for data in deliveries_data:
            delivery = data["delivery"]
            client_name = data["client_name"]

            # 1. Creamos la tarjeta principal para esta entrega
            card_frame = ctk.CTkFrame(self.scrollable_frame, border_width=2, border_color="#3b3b3b")
            card_frame.pack(fill="x", pady=10, padx=10)

            # Configuramos las columnas dentro de la tarjeta
            card_frame.grid_columnconfigure(0, weight=1) # Columna para descripción y detalles
            card_frame.grid_columnconfigure(1, weight=0) # Columna para el botón

            # --- Fila 0: Descripción ---
            desc_font = ctk.CTkFont(family="Segoe UI", size=16, weight="bold")
            desc_label = ctk.CTkLabel(card_frame, text=delivery.description, font=desc_font, wraplength=500, justify="left")
            desc_label.grid(row=0, column=0, columnspan=2, padx=15, pady=(10, 5), sticky="w")

            # --- Fila 1: Detalles (Cliente, Deadline, Fee) ---
            details_font = ctk.CTkFont(family="Segoe UI", size=12)
            details_text = f"👤 Client: {client_name}   |   📅 Deadline: {delivery.deadline}   |   💰 Fee: ${delivery.fee:.2f}"
            details_label = ctk.CTkLabel(card_frame, text=details_text, font=details_font, text_color="gray60")
            details_label.grid(row=1, column=0, columnspan=2, padx=15, pady=(0, 10), sticky="w")
            
            # --- Fila 2: Separador, Estado y Botón de Acción ---
            separator = ctk.CTkFrame(card_frame, height=1, fg_color="#3b3b3b")
            separator.grid(row=2, column=0, columnspan=2, padx=15, pady=5, sticky="ew")

            # Estado (Pending/Completed)
            status_font = ctk.CTkFont(family="Segoe UI", size=14, weight="bold")
            status_text = "Completed" if delivery.completed else "Pending"
            status_color = "#00e676" if delivery.completed else "#ff1744"
            status_label = ctk.CTkLabel(card_frame, text=status_text, font=status_font, text_color=status_color)
            status_label.grid(row=3, column=0, padx=15, pady=10, sticky="w")
            
            # Botón de acción (solo si está pendiente)
            if not delivery.completed:
                btn_complete = ctk.CTkButton(
                    card_frame,
                    text="✔ Mark as Completed",
                    width=150,
                    command=lambda d_id=delivery.id: self.mark_as_completed_action(d_id)
                )
                btn_complete.grid(row=3, column=1, padx=15, pady=10, sticky="e")

    def mark_as_completed_action(self, delivery_id):
        if messagebox.askyesno("Confirm", f"Mark delivery ID {delivery_id} as completed?"):
            self.controller.mark_delivery_as_completed(delivery_id)
            messagebox.showinfo("Success", "Delivery marked as completed.")
            self.refresh_data()