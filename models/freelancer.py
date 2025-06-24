"""
Freelancer model for the Delivery Management App.
Represents a freelancer and manages their deliveries.
"""


class Freelancer:
    """
    Represents a freelancer with an id, name, and a list of deliveries.
    """

    def __init__(self, name, id=None):
        """
        Initialize a Freelancer instance.
        :param name: Name of the freelancer.
        :param id: ID of the freelancer (optional).
        """
        self.id = id
        self.name = name
        self.deliveries = []

    def add_delivery(self, delivery):
        """
        Add a delivery to the freelancer's list of deliveries.
        :param delivery: Delivery instance to add.
        """