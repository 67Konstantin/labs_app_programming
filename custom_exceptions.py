class InvalidUserIdException(Exception):
    
    def __init__(self, user_id, message="Некорректный ID пользователя"):
        self.user_id = user_id
        self.message = f"{message}: {user_id}. ID должен начинаться с '101' и быть числом."
        super().__init__(self.message)


class InvalidEmailException(Exception):
    
    def __init__(self, email, message="Некорректный email адрес"):
        self.email = email
        self.message = f"{message}: {email}. Email должен содержать '@' и домен с точкой."
        super().__init__(self.message)

