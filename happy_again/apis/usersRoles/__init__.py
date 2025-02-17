from flask import Blueprint

userRoles_api = Blueprint('userRoles_api',__name__)

from happy_again.apis.usersRoles import api
