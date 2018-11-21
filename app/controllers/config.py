import logging

from gspread.exceptions import APIError

from app.constants import CONFIG_SHEET_ID
from app.controllers.google_sheet import gsheets


class ConfigController:

    #  GSpread column starts from 1
    CATEGORY_WORKSHEET_INDEX = 0
    SPENDING_TYPE_WORKSHEET_INDEX = 1
    SPENDING_TYPE_COLUMN = 1
    MONTHLY_CATEGORY_COLUMN = 1
    ANNUAL_CATEGORY_COLUMN = 2
    OCCASSIONAL_CATEGORY_COLUMN = 3

    def __init__(self):
        self.file = gsheets.open_by_key(CONFIG_SHEET_ID)

    def get_configs(self):
        # Trying to get user with user_id
        retry = 5
        is_fetched = False
        annual_category = []
        monthly_category = []
        occassional_category = []
        spending_type = []
        while retry > 0 and not is_fetched:
            retry -= 1
            try:
                category_ws = self.file.get_worksheet(self.CATEGORY_WORKSHEET_INDEX)
                spending_type_ws = self.file.get_worksheet(self.SPENDING_TYPE_WORKSHEET_INDEX)
                spending_type = spending_type_ws.col_values(self.SPENDING_TYPE_COLUMN)[1:]
                monthly_category = category_ws.col_values(self.MONTHLY_CATEGORY_COLUMN)[1:]
                annual_category = category_ws.col_values(self.ANNUAL_CATEGORY_COLUMN)[1:]
                occassional_category = category_ws.col_values(self.OCCASSIONAL_CATEGORY_COLUMN)[1:]
            except APIError:
                logging.error("Authentication error. Re-logging in")
                gsheets.login()
            else:
                is_fetched = True
        if not is_fetched:
            logging.error("Error authenticating to Google Sheet")
            raise ConnectionError("Error authenticating to Google Sheet")
        resp = dict()
        resp['category'] = {
            "monthly": monthly_category,
            "annual": annual_category,
            "occassional": occassional_category,
        }
        resp['spending_type'] = spending_type
        return resp


config_controller = ConfigController()
