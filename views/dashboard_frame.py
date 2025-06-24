import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import calendar
import numpy as np
import datetime

class DashboardFrame(ctk.CTkFrame):
    def __init__ (self, master, controller):
        super().__init__(master, fg_color= "transparent")
        self.controller= controller
        self.create_widgets()

    def create_widgets(self):
        font_title = ctk.CTkFont(family="Segoe UI", size=28, weight="bold")
        font_card_title = ctk.CTkFont(family="Segoe UI", size=16, weight="bold")
        font_card_value = ctk.CTkFont(family="Segoe UI", size=20, weight="bold")

        label = ctk.CTkLabel(self, text="📊 Dashboard Overview", font=font_title, text_color="#00b894")
        label.pack(pady=10, padx=10, anchor="center")

        summary_frame = ctk.CTkFrame(self)
        summary_frame.pack(fill="x", padx=10, pady=10)

        # Usaremos grid para alinear mejor las tarjetas
        summary_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        # Tarjeta 1: Total Deliveries
        self.total_label = self.create_summary_card(summary_frame, "Total Deliveries", "0", 0)
        
        # Tarjeta 2: Completed
        self.completed_label = self.create_summary_card(summary_frame, "Completed", "0", 1, value_color="#00e676")
        
        # Tarjeta 3: Pending
        self.pending_label = self.create_summary_card(summary_frame, "Pending", "0", 2, value_color="#ff1744")
        
        # Tarjeta 4: Earnings
        self.earnings_label = self.create_summary_card(summary_frame, "Earnings", "$0.00", 3)

        # --- Gráficos ---
        # Creamos la figura y los ejes de Matplotlib UNA SOLA VEZ.
        # Los guardamos como atributos de la clase para poder actualizarlos después.
        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(8, 4), dpi=100)
        self.fig.patch.set_facecolor('#242424') # Color de fondo de la figura
        plt.rcParams['text.color'] = '#FFFFFF'
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(padx=10, pady=10, fill="both", expand=True)

    def create_summary_card(self, parent, title, value, col, value_color="#FFFFFF"):
        """Función de ayuda para no repetir código al crear las tarjetas."""
        card_frame = ctk.CTkFrame(parent, fg_color="#2b2b2b")
        card_frame.grid(row=0, column=col, padx=10, pady=10, sticky="ew")
        
        title_label = ctk.CTkLabel(card_frame, text=title, font=ctk.CTkFont(size=14))
        title_label.pack(pady=(10, 5), padx=20)
        
        value_label = ctk.CTkLabel(card_frame, text=value, font=ctk.CTkFont(size=22, weight="bold"), text_color=value_color)
        value_label.pack(pady=(0, 10), padx=20)
        
        return value_label # Devolvemos la etiqueta del valor para poder actualizarla

    def refresh_data(self):
        stats = self.controller.get_dashboard_stats()

        # 2. Actualiza las etiquetas de las tarjetas.
        self.total_label.configure(text=str(stats["total"]))
        self.completed_label.configure(text=str(stats["completed"]))
        self.pending_label.configure(text=str(stats["pending"]))
        self.earnings_label.configure(text=f"${stats['earnings']:.2f}")

        # 3. Actualiza los gráficos.
        # Limpiamos los ejes antes de volver a dibujar para no sobreponer gráficos.
        self.ax1.clear()
        self.ax2.clear()

        # Gráfico de pastel
        completed = stats["completed"]
        pending = stats["pending"]
        if completed == 0 and pending == 0:
            pie_data = [1]
            pie_labels = ["No Data"]
            pie_colors = ["#424242"]
        else:
            pie_data = [completed, pending]
            pie_labels = ["Completed", "Pending"]
            pie_colors = ['#00b894', "#034744"]

        self.ax1.pie(pie_data, labels=pie_labels, colors=pie_colors, autopct="%1.1f%%", startangle=90)
        self.ax1.set_title("Delivery Status", color="#FFFFFF")
        self.ax1.set_facecolor('#242424')
            
        activity_data = self.controller.get_daily_activity_for_current_month()
        today = datetime.date.today()

        # Obtener el calendario del mes actual como una matriz (semanas x días)
        cal_matrix = calendar.monthcalendar(today.year, today.month)

        # Crear una matriz de datos con los conteos de actividad
        data_matrix = np.zeros((len(cal_matrix), 7))
        for r, week in enumerate(cal_matrix):
            for c, day in enumerate(week):
                if day != 0 and day in activity_data:
                    data_matrix[r, c] = activity_data[day]

        # Dibujar el heatmap
        self.ax2.set_title(f"Daily Activity - {today.strftime('%B %Y')}", color="#FFFFFF")
        self.ax2.imshow(data_matrix, cmap="Blues", aspect="auto")
        
        # Configurar las etiquetas de los ejes
        self.ax2.set_xticks(np.arange(7))
        self.ax2.set_xticklabels(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'], color="white")
        self.ax2.set_yticks([]) # Ocultamos los números de semana para un look más limpio

        # Añadir el número del día en cada celda
        for r, week in enumerate(cal_matrix):
            for c, day in enumerate(week):
                if day != 0:
                    # El color del texto cambia a blanco si el fondo es muy oscuro
                    text_color = "white" if data_matrix[r, c] > data_matrix.max() / 2 else "black"
                    self.ax2.text(c, r, day, ha="center", va="center", color=text_color, fontsize=8)

        self.ax2.set_facecolor('#242424')

        # 3. Finalizar y dibujar
        self.fig.tight_layout(pad=3.0)
        self.canvas.draw()

            