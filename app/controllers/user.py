import logging

from gspread.exceptions import CellNotFound

from app.constants import USER_SHEET_ID
from app.controllers.google_sheet import gsheets
from app.models.user import User


class UserController:

    def __init__(self):
        worksheet = gsheets.open_by_key(USER_SHEET_ID)
        self.worksheet = worksheet.get_worksheet(0)

    def create_user(self, user_id, first_name, last_name, monthly_income, password):
        # Check if user exists
        user = self.get_user(user_id)
        if user:
            logging.error("User {} already exists".format(user_id))
            raise FileExistsError("User {} already exists".format(user_id))
        user = User(user_id,
                    first_name,
                    last_name,
                    monthly_income)
        user.set_hashed_password(password)
        self._store_user(user)
        return user

    def get_user(self, user_id):
        # Trying to get user with user_id
        try:
            cell = self.worksheet.find(user_id)
        except CellNotFound:
            logging.error("User ID {} is not found".format(user_id))
            return None

        # Get user information if cell is found
        cell_row = cell.row
        user_info = self.worksheet.row_values(cell_row)
        user = User(user_id=user_id,
                    first_name=user_info[1],
                    last_name=user_info[2],
                    monthly_income=user_info[3],
                    password=user_info[4].encode())
        return user

    def _store_user(self, user):
        values = [user.user_id, user.first_name, user.last_name, user.monthly_income, user.get_password().decode()]
        self.worksheet.append_row(values)
        return True


user_controller = UserController()
