class Invoice:
    def __init__(self, id, delivery_id, amount, date, paid=0):
        self.id = id
        self.delivery_id = delivery_id
        self.amount = amount
        self.date = date
        self.paid = paid