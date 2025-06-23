from app import DeliveryApp
from controller import AppController

if __name__== "__main__":
    controller= AppController(db_file="my_database.db")
    app= DeliveryApp(controller)
    app.mainloop()
