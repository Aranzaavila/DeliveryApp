"""
Dashboard frame for the Delivery Management App.
Displays summary cards and charts for deliveries and activity.
"""

import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import calendar
import numpy as np
import datetime


class DashboardFrame(ctk.CTkFrame):
    """
    Frame for the dashboard view, showing KPIs and charts.
    """

    def __init__(self, master, controller):
        """
        Initialize the dashboard frame and its widgets.
        """
        super().__init__(master, fg_color="transparent")
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        """
        Create and layout all widgets for the dashboard, including summary cards and charts.
        """
        font_title = ctk.CTkFont(family="Segoe UI", size=28, weight="bold")
        font_card_title = ctk.CTkFont(family="Segoe UI", size=16, weight="bold")
        font_card_value = ctk.CTkFont(family="Segoe UI", size=20, weight="bold")

        # Dashboard title
        label = ctk.CTkLabel(
            self,
            text="📊 Dashboard Overview",
            font=font_title,
            text_color="#00b894"
        )
        label.pack(pady=10, padx=10, anchor="center")

        # Summary cards frame
        summary_frame = ctk.CTkFrame(self)
        summary_frame.pack(fill="x", padx=10, pady=10)

        # Configure columns for summary cards
        summary_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        # Card 1: Total Deliveries
        self.total_label = self.create_summary_card(
            summary_frame, "Total Deliveries", "0", 0
        )

        # Card 2: Completed Deliveries
        self.completed_label = self.create_summary_card(
            summary_frame, "Completed", "0", 1, value_color="#00e676"
        )

        # Card 3: Pending Deliveries
        self.pending_label = self.create_summary_card(
            summary_frame, "Pending", "0", 2, value_color="#ff1744"
        )

        # Card 4: Earnings
        self.earnings_label = self.create_summary_card(
            summary_frame, "Earnings", "$0.00", 3
        )

        # --- Charts Section ---
        # Create Matplotlib figure and axes only once
        self.fig, (self.ax1, self.ax2) = plt.subplots(
            1, 2, figsize=(8, 4), dpi=100
        )
        self.fig.patch.set_facecolor('#242424')  # Set background color
        plt.rcParams['text.color'] = '#FFFFFF'

        # Embed the Matplotlib figure in the Tkinter frame
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(padx=10, pady=10, fill="both", expand=True)

    def create_summary_card(self, parent, title, value, col, value_color="#FFFFFF"):
        """
        Helper function to create a summary card for KPIs.
        """
        card_frame = ctk.CTkFrame(parent, fg_color="#2b2b2b")
        card_frame.grid(row=0, column=col, padx=10, pady=10, sticky="ew")

        title_label = ctk.CTkLabel(
            card_frame, text=title, font=ctk.CTkFont(size=14)
        )
        title_label.pack(pady=(10, 5), padx=20)

        value_label = ctk.CTkLabel(
            card_frame,
            text=value,
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=value_color
        )
        value_label.pack(pady=(0, 10), padx=20)

        return value_label  # Return the value label for later updates

    def refresh_data(self):
        """
        Refresh the dashboard data and update the summary cards and charts.
        """
        stats = self.controller.get_dashboard_stats()

        # Update summary card values
        self.total_label.configure(text=str(stats["total"]))
        self.completed_label.configure(text=str(stats["completed"]))
        self.pending_label.configure(text=str(stats["pending"]))
        self.earnings_label.configure(text=f"${stats['earnings']:.2f}")

        # Clear previous chart data before redrawing
        self.ax1.clear()
        self.ax2.clear()

        # --- Pie Chart: Delivery Status ---
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

        self.ax1.pie(
            pie_data,
            labels=pie_labels,
            colors=pie_colors,
            autopct="%1.1f%%",
            startangle=90
        )
        self.ax1.set_title("Delivery Status", color="#FFFFFF")
        self.ax1.set_facecolor('#242424')

        # --- Heatmap: Daily Activity ---
        activity_data = self.controller.get_daily_activity_for_current_month()
        today = datetime.date.today()

        # Get the calendar matrix for the current month (weeks x days)
        cal_matrix = calendar.monthcalendar(today.year, today.month)

        # Create a matrix of activity counts for the heatmap
        data_matrix = np.zeros((len(cal_matrix), 7))
        for r, week in enumerate(cal_matrix):
            for c, day in enumerate(week):
                if day != 0 and day in activity_data:
                    data_matrix[r, c] = activity_data[day]

        self.ax2.set_title(
            f"Daily Activity - {today.strftime('%B %Y')}", color="#FFFFFF"
        )
        self.ax2.imshow(data_matrix, cmap="Blues", aspect="auto")

        # Set axis labels
        self.ax2.set_xticks(np.arange(7))
        self.ax2.set_xticklabels(
            ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'], color="white"
        )
        self.ax2.set_yticks([])  # Hide week numbers for a cleaner look

        # Add day numbers to each cell
        for r, week in enumerate(cal_matrix):
            for c, day in enumerate(week):
                if day != 0:
                    # Use white text if the cell is dark, black otherwise
                    text_color = (
                        "white" if data_matrix[r, c] > data_matrix.max() / 2 else "black"
                    )
                    self.ax2.text(
                        c, r, day, ha="center", va="center",
                        color=text_color, fontsize=8
                    )

        self.ax2.set_facecolor('#242424')

        # Finalize and redraw the figure
        self.fig.tight_layout(pad=3.0)
        self.canvas.draw()

