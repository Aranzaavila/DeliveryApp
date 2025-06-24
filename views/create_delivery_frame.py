import customtkinter as ctk
from tkinter import messagebox
from tkcalendar import DateEntry


class CreateDeliveryFrame(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master, fg_color="transparent")
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        # Este frame es ahora el contenedor, así que usamos 'self'
        font_title = ctk.CTkFont(family="Segoe UI", size=28, weight="bold")
        font_label = ctk.CTkFont(family="Segoe UI", size=14)
        font_button = ctk.CTkFont(family="Segoe UI", size=12, weight="bold")

        label = ctk.CTkLabel(self, text="➕ Create New Delivery", font=font_title, text_color="#00b894")
        label.grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky="w")

        ctk.CTkLabel(self, text="Client:", font=font_label).grid(row=1, column=0, sticky="e", padx=10, pady=10)
        self.client_entry = ctk.CTkEntry(self, font=font_label, fg_color= "#9DEEEE", text_color= "#066B6B",border_color="#00b894",          # Color del borde, igual que tu color principal
                                 placeholder_text="Enter client name...",
                                 placeholder_text_color="#066B6B")
        self.client_entry.grid(row=1, column=1, sticky="ew", padx=10, pady=10)

        ctk.CTkLabel(self, text="Description:", font=font_label).grid(row=2, column=0, sticky="e", padx=10, pady=10)
        self.desc_entry = ctk.CTkEntry(self, font=font_label, fg_color= "#9DEEEE", text_color= "#066B6B", border_color="#00b894",          # Color del borde, igual que tu color principal
                                 placeholder_text="Enter description...",
                                 placeholder_text_color="#066B6B")
        self.desc_entry.grid(row=2, column=1, sticky="ew", padx=10, pady=10)

        ctk.CTkLabel(self, text="Fee:", font=font_label).grid(row=3, column=0, sticky="e", padx=10, pady=10)
        self.fee_entry = ctk.CTkEntry(self, font=font_label, fg_color= "#9DEEEE", text_color= "#066B6B",border_color="#00b894",          # Color del borde, igual que tu color principal
                                 placeholder_text="Enter fee...",
                                 placeholder_text_color="#066B6B")
        self.fee_entry.grid(row=3, column=1, sticky="ew", padx=10, pady=10)

        ctk.CTkLabel(self, text="Deadline:", font=font_label).grid(row=4, column=0, sticky="e", padx=10, pady=10)
        # En views/create_delivery_frame.py, dentro de create_widgets()


        style = {
            'background': '#2b2b2b',          # Fondo del campo de entrada
            'foreground': 'white',            # Texto del campo de entrada
            'borderwidth': 2,
            'headersbackground': '#00b894',    # Fondo de la cabecera (tu color principal)
            'headersforeground': 'white',     # Texto de la cabecera
            'selectbackground': '#008f7a',     # Fondo del día seleccionado (un verde más oscuro)
            'selectforeground': 'white',      # Texto del día seleccionado
            'normalbackground': '#3b3b3b',     # Fondo de los días normales
            'normalforeground': 'white',      # Texto de los días normales
            'othermonthforeground': 'gray50', # Texto de los días de otros meses
            'othermonthbackground': '#2b2b2b'  # Fondo de los días de otros meses
        }

        self.deadline_entry = DateEntry(
            self, 
            date_pattern='y-mm-dd', 
            width=18,
            **style  
        )
        self.deadline_entry.grid(row=4, column=1, sticky="w", padx=10, pady=10)
        
        
        self.grid_columnconfigure(1, weight=1) 

        create_btn = ctk.CTkButton(
            self,
            text="Create Delivery",
            font=font_button,
            command=self.create_delivery_action
        )
        create_btn.grid(row=5, column=0, columnspan=2, pady=20)

    def create_delivery_action(self):
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
            self.controller.create_delivery_with_invoice(client_name, description, fee, deadline)
            messagebox.showinfo("Success", "Delivery created successfully!")
            
            
            self.client_entry.delete(0, 'end')
            self.desc_entry.delete(0, 'end')
            self.fee_entry.delete(0, 'end')
            
        except ValueError:
            messagebox.showerror("Error", "Fee must be a valid number.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")