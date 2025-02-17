from flask import Blueprint

loudness_perception_api = Blueprint('loudness_perception _api', __name__)

from happy_again.apis.loudness_perception import api
