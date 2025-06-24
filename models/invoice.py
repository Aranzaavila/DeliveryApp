"""
Invoice model for the Delivery Management App.
Represents an invoice associated with a delivery.
"""


class Invoice:
    """
    Represents an invoice with id, delivery_id, amount, date, and paid status.
    """

    def __init__(self, id, delivery_id, amount, date, paid=0):
        """
        Initialize an Invoice instance.
        :param id: Invoice ID.
        :param delivery_id: Associated delivery ID.
        :param amount: Invoice amount.
        :param date: Invoice date.
        :param paid: Paid status (0 or 1).
        """
        self.id = id
        self.delivery_id = delivery_id
        self.amount = amount
        self.date = date
        self.paid = paid