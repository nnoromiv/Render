from flask import Blueprint

spq_covid_api = Blueprint('spq_covid_api', __name__)

from happy_again.apis.questionaire import api