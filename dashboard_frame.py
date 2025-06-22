import customtkinter as ctk

class DashboardFrame(ctk.CTkFrame):
    def __init__ (self, master, db_contoller):
        super().__init__(master, fg_color="#23272f", corner_radius=20)
        self.db_controller = db_controller