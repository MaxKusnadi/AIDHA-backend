import json
import logging

from flask import request
from flask.views import MethodView
from flask_login import current_user, login_required

from app import app
from app.controllers.expenses import expense_controller
from app.models.expenses import Expenses


class ExpenseView(MethodView):
    decorators = [login_required]

    def get(self):
        logging.info("New GET /expense request")
        try:
            expenses = expense_controller.get_all_expenses(current_user.user_id)
        except ConnectionError:
            return json.dumps({
                "text": "Google authentication error. Please restart the backend",
                "status": 500
            })
        resp = {
            "status": 200,
            "result": expenses
        }
        return json.dumps(resp)

    def post(self):
        logging.info("New POST /expense request")
        data = request.get_json()
        if not data:
            return json.dumps({
                "text": "payload is not found",
                "status": 400
            })
        user_id = current_user.user_id
        date = data.get("date")
        description = data.get("description", "No Description")
        spending_type = data.get("spending_type")
        category = data.get("category")
        amount = data.get("amount")
        if not date or not spending_type or not category or not amount:
            return json.dumps({
                "text": "payload is not complete",
                "status": 400
            })

        # Try to create expenses
        expense = Expenses(user_id, date, description, spending_type, category, amount)
        try:
            status = expense_controller.create_expenses(expense)
        except ConnectionError:
            return json.dumps({
                "text": "Google authentication error. Please restart the backend",
                "status": 500
            })
        status_code = 200 if status else 400
        return json.dumps({
            "status": status_code,
            "text": status
        })


app.add_url_rule('/expense', view_func=ExpenseView.as_view('expense'))
