import gspread
import logging

from oauth2client.service_account import ServiceAccountCredentials

from app.constants import SCOPES, CREDENTIALS_FILE


logging.info("Initializing Google Sheet")
credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, SCOPES)
gsheets = gspread.authorize(credentials)  # To be used by other controllers
