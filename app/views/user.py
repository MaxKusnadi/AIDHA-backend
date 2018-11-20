import json
import logging

from flask import request
from flask.views import MethodView
from flask_login import current_user, login_required

from app import app
from app.controllers.user import user_controller


class UserView(MethodView):
    decorators = [login_required]

    def get(self):
        logging.info("New GET /user request")
        resp = dict()
        resp['user_id'] = current_user.user_id
        resp['first_name'] = current_user.first_name
        resp['last_name'] = current_user.last_name
        resp['monthly_income'] = current_user.monthly_income
        return json.dumps(resp)


class UserCreationView(MethodView):

    def post(self):
        logging.info("New POST /user/create request")
        data = request.get_json()
        if not data:
            return json.dumps({
                "text": "payload is not found",
                "status": 400
            })
        user_id = data.get("user_id")
        password = data.get("password")
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        monthly_income = data.get("monthly_income", 1000)
        if not user_id or not password or not first_name or not last_name:
            return json.dumps({
                "text": "payload is not complete",
                "status": 400
            })
        # Try to create user
        try:
            user = user_controller.create_user(user_id,
                                               first_name,
                                               last_name,
                                               monthly_income,
                                               password)
            resp = dict()
            resp['user_id'] = user.user_id
            resp['first_name'] = user.first_name
            resp['last_name'] = user.last_name
            resp['monthly_income'] = user.monthly_income
        except FileExistsError:
            return json.dumps({
                "text": "user already exists",
                "status": 404
            })
        return json.dumps(resp)


app.add_url_rule('/user', view_func=UserView.as_view('user'))
app.add_url_rule('/user/create', view_func=UserCreationView.as_view('user_create'))
