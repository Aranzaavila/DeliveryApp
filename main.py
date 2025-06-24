"""
Entry point for the Delivery Management App.
Initializes the controller and launches the main application window.
"""
from app import DeliveryApp
from controller import AppController

if __name__== "__main__":
    # Create the controller with the database file
    controller= AppController(db_file="my_database.db")
    # Initialize and run the main application
    app= DeliveryApp(controller)
    app.mainloop()
