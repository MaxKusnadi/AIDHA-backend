import logging

from flask import Flask
from flask_login import LoginManager
from flask_cors import CORS
from flask_bcrypt import Bcrypt

# CREATING LOGGER
logging.basicConfig(level=logging.INFO,
                    format='[%(filename)s:%(lineno)s | %(funcName)s() | %(asctime)s | %(levelname)s] %(message)s')
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)
app.config.from_object('config')
CORS(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

# Initializing views
from app.views.login import *
from app.views.user import *
from app.views.config import *
