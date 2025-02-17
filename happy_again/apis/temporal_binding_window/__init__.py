from flask import Blueprint

temporal_binding_window_api = Blueprint('temporal_binding_window_api', __name__)

from happy_again.apis.temporal_binding_window import api