from functools import wraps
from flask import current_app
from flask import request
from flask_jwt_extended import get_jwt_identity
import jwt
from happy_again import db

from happy_again.models import Session, User, UserRoles, Admin
from happy_again.apis.utils import Helper

def authenticate_user(func):
    """Validate token."""

    @wraps(func)
    def authenticate_and_call(*args, **kwargs):

        token = Session.get_session(get_jwt_identity())
        if not token:
            return Helper.create_error_response(401, "Unauthorized")
        user = User.get_user(token.user_id)
        if not user:
            return Helper.create_error_response(401, "Unauthorized")
        if not kwargs.get('user_id'):
            kwargs['user_id'] = user.id
        if kwargs.get('user_id') != user.id:
            current_app.logger.info("Token mismatch user_id {}".format(kwargs.get('user_id')))
            return Helper.create_error_response(401, "Unauthorized")

        kwargs['user'] = user
        return func(*args, **kwargs)

    return authenticate_and_call


def authenticate(func):
    """Validate token."""
    @wraps(func)
    def authenticate_and_call(*args, **kwargs):
        auth_header = request.headers.get('Authorization', type=str)
        if not auth_header:
            return Helper.create_error_response(401, "Unauthorized")

        split_auth_header = auth_header.split(" ")
        if not len(split_auth_header) == 2:
            return Helper.create_error_response(401, "Invalid Authorization")

        token = split_auth_header[1]
        decode_token = jwt.decode(token, "secret", algorithms=["HS256"])
        if not decode_token:
            return Helper.create_error_response(401, "Unauthorized")
        user = User.get_user(decode_token['user_id'])
        if not user:
            return Helper.create_error_response(401, "Unauthorized")
        if not kwargs.get('user_id'):
            kwargs['user_id'] = user.id
        if kwargs.get('user_id') != user.id:
            current_app.logger.info("Token mismatch user_id {}".format(kwargs.get('user_id')))
            return Helper.create_error_response(401, "Unauthorized")
        kwargs['user'] = user.to_json()
        kwargs['user_id'] = user.to_json()['id']
        return func(*args, **kwargs)
    
    return authenticate_and_call

def authenticateAdmin(func):
    """Validate token."""

    @wraps(func)
    def authenticate_and_call(*args, **kwargs):
        auth_header = request.headers.get('Authorization', type=str)
        if not auth_header:
            return Helper.create_error_response(401, "Unauthorized")

        split_auth_header = auth_header.split(" ")
        if not len(split_auth_header) == 2:
            return Helper.create_error_response(401, "Invalid Authorization")

        token = split_auth_header[1]
        decode_token = jwt.decode(token, "secret", algorithms=["HS256"])
        if not decode_token:
            return Helper.create_error_response(401, "Unauthorized")
        user = UserRoles.get_user(decode_token['id'])
        if not user:
            return Helper.create_error_response(401, "Unauthorized")
        # if not kwargs.get('user_id'):
        #     kwargs['user_id'] = user.id
        # if kwargs.get('user_id') != user.id:
        #     current_app.logger.info("Token mismatch user_id {}".format(kwargs.get('user_id')))
        #     return Helper.create_error_response(401, "Unauthorized")
        #kwargs['user'] = user.to_json()
        #kwargs['user_id'] = user.to_json()['id']
        return func(*args, **kwargs)

    return authenticate_and_call


def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):

        # Get all the Admin records from the database
        admins = db.session.query(Admin).all()
        admin_emails = list(map(lambda a: a.email, admins))
        #print("Admin emails:\n" + "\n".join(admin_emails))

        # Get the current user
        auth_header = request.headers.get('Authorization', type=str)
        split_auth_header = auth_header.split(" ")
        token = split_auth_header[1]
        decode_token = jwt.decode(token, "secret", algorithms=["HS256"])
        current_user_id = decode_token['user_id']
        current_user = db.session.query(User).filter_by(id=current_user_id).first()

        #print("Current user email:", current_user.email)
        #print("Is the current user also an admin?:",current_user.email in admin_emails)

        if current_user.email in admin_emails:
            #print("Congrats uagliò, you're an admin")
            return func(*args, **kwargs)
        else:
            return Helper.create_error_response(401, "Unauthorized")

    return decorated_view
