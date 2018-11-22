import logging

from gspread.exceptions import APIError

from app.constants import CONFIG_SHEET_ID, DEFAULT_RETRY
from app.controllers.google_sheet import gsheets


class ConfigController:

    #  GSpread column starts from 1
    CONFIG_WORKSHEET_TITLE = "Configs"
    MONTHLY_CATEGORY_COLUMN = 1
    ANNUAL_CATEGORY_COLUMN = 2
    OCCASSIONAL_CATEGORY_COLUMN = 3
    SPENDING_TYPE_COLUMN = 4

    def __init__(self):
        self.file = gsheets.open_by_key(CONFIG_SHEET_ID)

    def get_configs(self):
        # Trying to get all configs
        retry = DEFAULT_RETRY
        is_fetched = False
        annual_category = []
        monthly_category = []
        occassional_category = []
        spending_type = []
        while retry > 0 and not is_fetched:
            retry -= 1
            try:
                config_ws = self.file.worksheet(self.CONFIG_WORKSHEET_TITLE)
                spending_type = config_ws.col_values(self.SPENDING_TYPE_COLUMN)[1:]
                monthly_category = config_ws.col_values(self.MONTHLY_CATEGORY_COLUMN)[1:]
                annual_category = config_ws.col_values(self.ANNUAL_CATEGORY_COLUMN)[1:]
                occassional_category = config_ws.col_values(self.OCCASSIONAL_CATEGORY_COLUMN)[1:]
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
