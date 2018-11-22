import logging

from gspread.exceptions import APIError, CellNotFound

from app.constants import EXPENSES_SHEET_ID, DEFAULT_RETRY
from app.controllers.google_sheet import gsheets
from app.models.expenses import Expenses


class ExpensesController:

    #  GSpread column starts from 1
    EXPENSES_WORKSHEET_TITLE = "Expenses"
    USER_ID_COLUMN = 6

    def __init__(self):
        file = gsheets.open_by_key(EXPENSES_SHEET_ID)
        self.worksheet = file.worksheet(self.EXPENSES_WORKSHEET_TITLE)

    def create_expenses(self, expenses):
        values_to_store = expenses.export_as_sheet_list()
        retry = DEFAULT_RETRY
        is_done = False
        while retry > 0 and not is_done:
            retry -= 1
            try:
                self.worksheet.append_row(values_to_store, value_input_option="USER_ENTERED")
            except APIError:
                logging.error("Authentication error. Re-logging in")
                gsheets.login()
            else:
                is_done = True
        if not is_done:
            logging.error("Error authenticating to Google Sheet")
            raise ConnectionError("Error authenticating to Google Sheet")
        return is_done

    def get_all_expenses(self, user_id):
        # Trying to get expenses of user_id
        retry = DEFAULT_RETRY
        is_fetched = False
        cells = []
        while retry > 0 and not is_fetched:
            retry -= 1
            try:
                cells = self.worksheet.findall(user_id)
            except CellNotFound:
                logging.error("User ID {} has no expenses yet".format(user_id))
                return []
            except APIError:
                logging.error("Authentication error. Re-logging in")
                gsheets.login()
            else:
                is_fetched = True
        if not is_fetched:
            logging.error("Error authenticating to Google Sheet")
            raise ConnectionError("Error authenticating to Google Sheet")
        # Getting expenses info
        selected_row_indexes = map(lambda x: x.row, cells)
        selected_row_information = map(lambda x: self.worksheet.row_values(x), selected_row_indexes)
        # Transform it into expenses instance
        expenses = map(lambda x: Expenses(x[5], x[0], x[1], x[2], x[3], x[4]), selected_row_information)
        resp = list(map(lambda x: x.export_as_dict(), expenses))
        return resp


expense_controller = ExpensesController()
