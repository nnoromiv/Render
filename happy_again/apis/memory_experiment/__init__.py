from flask import Blueprint

word_encoding_api = Blueprint('word_encoding_api', __name__)

from happy_again.apis.memory_experiment import api
