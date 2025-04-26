class User:
    def __init__(self, user_id, name, email):
        self.user_id = user_id
        self.name = name
        self.email = email

    def update_info(self, name=None, email=None):
        if name:
            self.name = name
        if email:
            self.email = email
