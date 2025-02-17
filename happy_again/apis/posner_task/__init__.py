from flask import Blueprint

posner_task_api = Blueprint('posner_task_api', __name__)

from happy_again.apis.posner_task import api