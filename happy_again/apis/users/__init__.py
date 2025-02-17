from flask import Blueprint

user_api = Blueprint('user_api',__name__)

from happy_again.apis.users import api
