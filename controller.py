"""
Controller for the Delivery Management App.
Handles business logic and communication between the database and the views.
"""

import datetime
from collections import defaultdict
from db.database import Database
from models.delivery import Delivery
from models.client import Client


class AppController:
    """
    Controller class for the Delivery Management App.
    """

    def __init__(self, db_file):
        """
        Initialize the controller with a database connection.
        """
        self.db = Database(db_file)

    def create_delivery_with_invoice(self, client_name, description, fee, deadline):
        """
        Create a new delivery and its associated invoice.
        If the client does not exist, create a new client.
        """
        client = self.db.get_client_by_name(client_name)
        if not client:
            new_client = Client(id=None, name=client_name)
            client_id = self.db.insert_client(new_client)
        else:
            client_id = client.id

        new_delivery = Delivery(
            id=None,
            client_id=client_id,
            description=description,
            completed=0,
            fee=float(fee),
            deadline=deadline,
            completed_date=None
        )
        delivery_id = self.db.add_delivery(new_delivery)

        # create an invoice for the new delivery
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        self.db.add_invoice(delivery_id, float(fee), today)
        return delivery_id

    def mark_delivery_as_completed(self, delivery_id):
        """
        Mark a delivery as completed in the database.
        """
        self.db.mark_delivery_completed(delivery_id)
        self.db.add_delivery_history(delivery_id, "Completed")
    
    def mark_invoice_as_paid(self, invoice_id):
        """
        Mark an invoice as paid in the database.
        """
        self.db.mark_invoice_as_paid(invoice_id)

    def filter_deliveries(self, query):
        """
        Filter deliveries by description or client name.
        Returns a list of deliveries matching the query.
        """
        query = query.lower().strip()
        if not query:
            return self.get_all_deliveries_for_view()
        all_deliveries = self.db.get_all_deliveries()
        filtered = []
        for d in all_deliveries:
            client = self.db.get_client_by_id(d.client_id)
            if (query in d.description.lower()) or (client and query in client.name.lower()):
                client_name = client.name if client else "Unknown"
                filtered.append({"delivery": d, "client_name": client_name})
        return filtered

    def get_dashboard_stats(self):
        """
        Get statistics for the dashboard: total, completed, pending deliveries, and earnings.
        """
        stats = {
            "total": self.db.count_all_deliveries(),
            "completed": self.db.count_completed(),
            "pending": self.db.count_pending(),
            "earnings": self.db.total_earnings()
        }
        return stats

    def get_all_deliveries_for_view(self):
        """
        Get all deliveries with their associated client names for display in the view.
        """
        deliveries = self.db.get_all_deliveries()
        data_for_view = []
        for d in deliveries:
            client = self.db.get_client_by_id(d.client_id)
            client_name = client.name if client else "Unknown Client"
            data_for_view.append({
                "delivery": d,
                "client_name": client_name
            })
        return data_for_view

    def get_invoices_for_view(self):
        """
        Get all invoices with their associated client names and delivery descriptions for display.
        """
        invoices = self.db.get_all_invoices()
        data_for_view = []
        for invoice in invoices:
            # get the delivery associated with the invoice
            delivery = self.db.get_delivery_by_id(invoice.delivery_id)
            if delivery:
                client = self.db.get_client_by_id(delivery.client_id)
                client_name = client.name if client else "Unknown Client"
                delivery_desc = delivery.description
            else:
                client_name = "N/A"
                delivery_desc = "Delivery not found"

            data_for_view.append({
                "invoice": invoice,
                "client_name": client_name,
                "delivery_desc": delivery_desc
            })
        return data_for_view

    def get_reminders(self):
        """
        Get reminders for overdue deliveries and unpaid invoices.
        Returns a string with the reminder messages.
        """
        today = datetime.date.today().strftime("%Y-%m-%d")
        overdue = [
            d for d in self.db.get_all_deliveries()
            if not d.completed and d.deadline <= today
        ]
        unpaid = [i for i in self.db.get_all_invoices() if not i.paid]
        messages = []
        if overdue:
            messages.append(f"You have {len(overdue)} delivery(ies) due or overdue.")
        if unpaid:
            messages.append(f"You have {len(unpaid)} unpaid invoice(s).")

        return "\n".join(messages)

    def get_earnings_over_time(self):
        """
        Get earnings grouped by month for completed deliveries.
        Returns two lists: labels (months) and values (earnings).
        """
        earnings_by_month = defaultdict(float)

        # get all completed deliveries with a completion date
        completed_deliveries = [
            d for d in self.db.get_all_deliveries()
            if d.completed and d.completed_date
        ]

        for delivery in completed_deliveries:
            # convert the completion date string to a date object
            completion_date = datetime.datetime.strptime(
                delivery.completed_date, "%Y-%m-%d"
            ).date()
            # create a key in the format "YYYY-MM"
            month_key = completion_date.strftime("%Y-%m")
            earnings_by_month[month_key] += delivery.fee

        sorted_months = sorted(earnings_by_month.keys())
        labels = sorted_months
        values = [earnings_by_month[key] for key in sorted_months]

        return labels, values

    def get_daily_activity_for_current_month(self):
        """
        Get the number of completed deliveries per day for the current month.
        Returns a dictionary with day as key and count as value.
        """
        activity = defaultdict(int)
        today = datetime.date.today()
        # get all completed deliveries with a completion date
        completed_deliveries = [
            d for d in self.db.get_all_deliveries()
            if d.completed and d.completed_date
        ]

        for delivery in completed_deliveries:
            completion_date = datetime.datetime.strptime(
                delivery.completed_date, "%Y-%m-%d"
            ).date()
            # only count deliveries completed in the current month and year
            if (completion_date.month == today.month and
                    completion_date.year == today.year):
                activity[completion_date.day] += 1

        return dict(activity)
    
    def delete_delivery(self, delivery_id):
        """
        Delete a delivery by its ID.
        """
        self.db.delete_delivery(delivery_id)

    def update_delivery(self, delivery_id, description, fee, deadline):
        """
        Update a delivery's details.
        """
        self.db.update_delivery(delivery_id, description, fee, deadline)
        self.db.add_delivery_history(delivery_id, "Edited")
