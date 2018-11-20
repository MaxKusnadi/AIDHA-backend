import logging

from flask_login import login_user

from app.controllers.user import user_controller
from app import login_manager


@login_manager.user_loader
def load_user(user_id):
    return user_controller.get_user(user_id)


class LoginController:

    def login(self, user_id, password):
        user = user_controller.get_user(user_id)
        if not user:
            logging.error("User {} is not found".format(user_id))
            raise FileNotFoundError("User is not found")
        # Check if user password is correct
        if not user.check_password(password):
            logging.error("Wrong password for user {}".format(user_id))
            raise AssertionError("Wrong password")
        login_user(user)
        # Preparing user payload
        resp = dict()
        resp['user_id'] = user.user_id
        resp['first_name'] = user.first_name
        resp['last_name'] = user.last_name
        resp['monthly_income'] = user.monthly_income
        return resp


login_controller = LoginController()
