# 🚚 Delivery Management App

Welcome to **DeliveryApp**!  
A modern, user-friendly desktop application for managing deliveries and invoices.  
Built with a clean architecture and a beautiful dark-themed interface, DeliveryApp helps you organize, track, and analyze your delivery business with ease.

---

## 📑 Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)

---

## 🌟 Features

- **MVC Architecture:** Clean separation of logic, UI, and data for maintainability and scalability.
- **Interactive Dashboard:** Real-time KPIs, status charts, and an activity heatmap for quick insights.
- **Delivery Management:** Create, edit, delete, and mark deliveries as completed.
- **Invoicing System:** Automatic invoice generation and management for each delivery.
- **Modern UI:** Built with CustomTkinter for a sleek, dark-themed look.
- **Notifications & Alerts:** Visual alerts for overdue and soon-to-expire deliveries, and unpaid invoices.
- **Change History:** Track edits and completion events for each delivery.
- **Data Export:** Export deliveries and invoices to CSV for external analysis.
- **Search & Filters:** Quickly find deliveries by client, status, or date.
- **Responsive Design:** Card-based layout adapts to different window sizes.

---

## 🛠️ Technologies Used

- **Language:** Python 3.10+
- **GUI Framework:** [CustomTkinter]
- **Charts & Visualizations:** Matplotlib, NumPy
- **Date Picker:** tkcalendar
- **Database:** SQLite 3

---

## 🚀 Getting Started

Follow these steps to run the project locally.

### Prerequisites

- Python 3.10 or higher
- `pip` (Python package manager)

### Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/Aranzaavila/DeliveryApp.git
    cd DeliveryApp
    ```

2. **Create and activate a virtual environment (recommended):**
    ```bash
    python -m venv .venv

    # Activate the environment
    # On Windows:
    .\.venv\Scripts\activate
    # On macOS/Linux:
    source .venv/bin/activate
    ```

3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Run the application:**
    ```bash
    python main.py
    ```

---

## 💡 Usage

After launching the app, use the sidebar to:
- **View Dashboard:** See key statistics, charts, and your activity heatmap.
- **Create Deliveries:** Add new deliveries with client, description, fee, and deadline.
- **Manage Deliveries:** Edit, delete, complete, and view the history of each delivery.
- **Manage Invoices:** Track, mark as paid, and review all invoices.

---

## 🖼️ Screenshots

*Dashboard View with Activity Heatmap:*

![Dashboard Screenshot](screenshots/dashboard.png)

*Create Delivery View:*

![Create Delivery Screenshot](screenshots/create_delivery.png)

*Deliveries List with Card-Based Design:*

![Deliveries List Screenshot](screenshots/deliveries_list.png)

*Invoices List with Card-Based Design:*

![Invoices List Screenshot](screenshots/invoices_list.png)

---

## 🤝 Contributing

Contributions are welcome!  
If you have suggestions or improvements, please open an issue or submit a pull request.

---

## 📄 License

This project is licensed under the MIT License.

---

*Created by Aranza Avila for academic purposes.*


