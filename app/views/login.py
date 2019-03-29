import json
import logging

from flask.views import MethodView
from flask_login import login_required, logout_user, current_user
from flask import request, redirect

from app import app
from app.controllers.login import login_controller


class LoginView(MethodView):

    def get(self):
        logging.info("New GET /login request")
        if current_user.is_authenticated:
            return json.dumps({
                "status": 200,
                "text": "logged in"
            })
        else:
            logout_user()  # Destroy cookies
            return json.dumps({
                "text": "Not logged in",
                "status": 301}
            )

    def post(self):
        logging.info("New POST /login request")
        data = request.get_json()
        if not data:
            return json.dumps({
                "text": "payload is not found",
                "status": 400
            })
        if not data.get("user_id") or not data.get("password"):
            return json.dumps({
                "text": "payload is not complete",
                "status": 400
            })
        # Try to log in
        user_id = data.get("user_id")
        password = data.get("password")
        try:
            resp = login_controller.login(user_id, password)
        except FileNotFoundError:
            return json.dumps({
                "text": "user is not found",
                "status": 404
            })
        except AssertionError:
            return json.dumps({
                "text": "wrong password",
                "status": 403
            })
        resp['status'] = 200
        return json.dumps(resp)


class LogoutView(MethodView):
    decorators = [login_required]

    def get(self):
        redirect_url = request.args.get("redirect_url")
        logout_user()
        return redirect(redirect_url)


app.add_url_rule('/login', view_func=LoginView.as_view('login'))
app.add_url_rule('/logout', view_func=LogoutView.as_view('logout'))
