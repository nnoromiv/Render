from flask import Blueprint

tasks_api = Blueprint('tasks_api', __name__)

from happy_again.apis.tasks import api