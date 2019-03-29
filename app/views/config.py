import json
import logging

from flask.views import MethodView
from flask_login import login_required

from app import app
from app.controllers.config import config_controller


class ConfigView(MethodView):
    decorators = [login_required]

    def get(self):
        logging.info("New GET /config request")
        try:
            resp = config_controller.get_configs()
        except ConnectionError:
            return json.dumps({
                "text": "Google authentication error. Please restart the backend",
                "status": 500
            })
        resp['status'] = 200
        return json.dumps(resp)


app.add_url_rule('/config', view_func=ConfigView.as_view('config'))
