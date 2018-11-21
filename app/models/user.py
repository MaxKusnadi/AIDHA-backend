from flask_login import UserMixin

from app import bcrypt


class User(UserMixin):

    def __init__(self, user_id, first_name, last_name, monthly_income, password=None):
        self.first_name = first_name
        self.last_name = last_name
        self.monthly_income = monthly_income
        self._password = password
        self.user_id = user_id

    def check_password(self, plain_text):
        if self._password:
            return bcrypt.check_password_hash(self._password, plain_text)
        return False

    def set_hashed_password(self, plain_text):
        self._password = bcrypt.generate_password_hash(plain_text)
        return True

    def get_password(self):
        return self._password

    def is_active(self):
        return True

    def get_id(self):
        return self.user_id

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def __repr__(self):
        return "ID: {id} | Name: {first_name} {last_name}".format(id=self.user_id, first_name=self.first_name,
                                                                  last_name=self.last_name)
