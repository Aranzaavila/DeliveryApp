import customtkinter as ctk
from tkinter import messagebox


class InvoiceFrame(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master, fg_color="transparent")
        self.controller = controller
        self.create_widgets()
        

    def create_widgets(self):
            """Crea los elementos de la UI que no cambian, como el título y los encabezados."""
            
            # --- Título de la Vista ---
            title_label = ctk.CTkLabel(self, text="💸 Invoices", font=ctk.CTkFont(size=28, weight="bold"), text_color="#00b894")
            title_label.pack(pady=(0, 20), padx=10, anchor="w")

            # --- Frame para los Encabezados de la Tabla ---
            header_frame = ctk.CTkFrame(self, fg_color="#2b2b2b")
            header_frame.pack(fill="x", padx=10, pady=5)
            
            headers = ["ID", "Delivery ID", "Amount", "Date", "Status", "Actions"]
            font_header = ctk.CTkFont(family="Segoe UI", size=14, weight="bold")
            
            # Usamos grid para alinear las columnas
            header_frame.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)
            for i, header in enumerate(headers):
                header_label = ctk.CTkLabel(header_frame, text=header, font=font_header)
                header_label.grid(row=0, column=i, padx=5, pady=10)

            # --- Área de Scroll para las Filas de Facturas ---
            # Aquí es donde se dibujarán dinámicamente las facturas
            self.scrollable_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
            self.scrollable_frame.pack(fill="both", expand=True, padx=10, pady=5)

    def refresh_data(self):
    
            # 1. Limpiar las filas antiguas antes de dibujar las nuevas.
            #    Esto es MUY importante para no tener datos duplicados.
            for widget in self.scrollable_frame.winfo_children():
                widget.destroy()

            # 2. Pedir la lista de facturas actualizada al controlador.
            invoices = self.controller.get_invoices_for_view()
            font_row = ctk.CTkFont(family="Segoe UI", size=14)

            # 3. Dibujar cada factura en una nueva fila.
            for i, invoice in enumerate(invoices):
                # Creamos un frame para cada fila
                row_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="#2b2b2b" if i % 2 == 0 else "#242424")
                row_frame.pack(fill="x", pady=4)
                row_frame.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)

                # Columna ID
                ctk.CTkLabel(row_frame, text=str(invoice.id), font=font_row).grid(row=0, column=0, pady=5)
                # Columna Delivery ID
                ctk.CTkLabel(row_frame, text=str(invoice.delivery_id), font=font_row).grid(row=0, column=1, pady=5)
                # Columna Amount
                ctk.CTkLabel(row_frame, text=f"${invoice.amount:.2f}", font=font_row).grid(row=0, column=2, pady=5)
                # Columna Date
                ctk.CTkLabel(row_frame, text=invoice.date, font=font_row).grid(row=0, column=3, pady=5)
                
                # Columna Status (con color)
                status_text = "Paid" if invoice.paid else "Pending"
                status_color = "#00e676" if invoice.paid else "#ff1744"
                ctk.CTkLabel(row_frame, text=status_text, font=font_row, text_color=status_color).grid(row=0, column=4, pady=5)

                # --- Columna de Acciones (con el botón condicional) ---
                action_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
                action_frame.grid(row=0, column=5, pady=5)

                if not invoice.paid:
                    # El botón solo se crea si la factura está pendiente.
                    # El truco 'inv_id=invoice.id' en lambda es para asegurar que se pasa el ID correcto.
                    pay_button = ctk.CTkButton(
                        action_frame,
                        text="Mark as Paid",
                        width=120,
                        command=lambda inv_id=invoice.id: self.mark_as_paid_action(inv_id)
                    )
                    pay_button.pack()
        
    def mark_as_paid_action(self, invoice_id):

            if messagebox.askyesno("Confirm", f"Mark invoice ID {invoice_id} as paid?"):
                # 1. Llama al controlador para que haga el trabajo de lógica.
                self.controller.mark_invoice_as_paid(invoice_id)
                
                # 2. Muestra un mensaje de éxito.
                messagebox.showinfo("Success", "Invoice marked as paid.")
                
                # 3. ¡Refresca la vista para que los cambios se vean al instante!
                self.refresh_data()