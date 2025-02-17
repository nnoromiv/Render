from flask import Blueprint

movement_perception_api = Blueprint('movement_perception_api', __name__)

from happy_again.apis.movement_perception import api