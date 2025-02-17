from datetime import datetime, timedelta

from flask import request, current_app
from flask_jwt_extended import create_access_token, create_refresh_token
import jwt

from happy_again import db as coviddb
from happy_again.apis.usersRoles import userRoles_api
from happy_again.apis.usersRoles.consts import *
from happy_again.common.consts import *
from happy_again.models import UserRoles, Token
from happy_again.common.utils import send_email
from happy_again.apis.utils import Helper

from flask_cors import CORS

CORS(userRoles_api)


# User Registration api
@userRoles_api.route('/usersRoles', methods=['POST'])
def user_register():
    data = request.get_json(force=True)
    email = data['email']
    role = data['role']
    
    if not email or not role:
        return Helper.create_error_response(400, INCOMPLETE_BODY_PARAMETER)
    
    if not Helper.email_validator(email):
        return Helper.create_error_response(400, "Invalid email format.")

    user = coviddb.session.query(UserRoles).filter_by(email=email).first()
    
    if user:
        current_app.logger.info("{} -> already registered.".format(user.email))
        # return Response(status=409)
        return Helper.create_error_response(409, USER_ALREADY_REGISTERED.format(user.email))

    user = UserRoles(email, role)
    token = create_access_token(user.email, expires_delta=timedelta(days=USER_CONFIRMATION_TOKEN_EXPIRY_DELTA))
    
    #confirm_url = "{site}/users/verify/{token}".format(site=SITE_URL, token=token)
    confirm_url = "{site}/uni/register/complete/{token}".format(site=SITE_URL, token=token)

    if role not in [UserRoles.ROLE_ADMIN, UserRoles.ROLE_LAB_ASSISTANT, UserRoles.ROLE_RESEARCHER]:
        return Helper.create_error_response(409, INVALID_ROLE)
        
    user.confirmed_at_by_admin = datetime.utcnow()

    send_email(
        to=[user.email], 
        subject=SUBJECT_USER_CONFIRMATION_EMAIL,
        msg_html="<div><div><h1>CONSENT FORM</h1><p><b>1.</b> I agree to participate in the research project “Neurological integrity and cognitive functioning test battery” being carried out by the above named researchers.  </p><p><b>2.</b> This agreement has been given voluntarily and without coercion.</p><p><b>3.</b> I have been given full information about the study and contact details of the researcher(s).</p> <p><b>4.</b> I have read and understood the information provided above. </p> <p><b>5.</b> I agree to have my anonymised data shared on publicly accessible repositories.  </p> <p><b>6.</b> I agree to be contacted in the future by the researchers.</p> <p><b>7.</b> I have had the opportunity to ask questions about the research and my participation in it. </p><p><b>8.</b> I am 18 years old or older.</p></div><div><p>To confirm your account, please go to the following link:</p><b>{url}</b></div></div>".format(url=confirm_url)
    )

    coviddb.session.add(user)
    coviddb.session.commit()
    current_app.logger.info("'{}' registered.".format(user.email))
    
    data = {
        **user.to_json(),
        "token": token
    }
    
    # return Response(json.dumps(user.to_json()), mimetype='application/json')
    return Helper.create_success_response("", data)


# User Confirmation api
@userRoles_api.route('/usersRoles/verify/<token>', methods=['POST'])
def confirm_email(token):
    
    user = Helper.validate_jwt_token(token)
    
    if isinstance(user, dict):
        email = user.get("sub")
    else:
        return user
    
    data = request.get_json(force=True)
    password = data["password"]
    
    if not email or not password:
        return Helper.create_error_response(400, INCOMPLETE_BODY_PARAMETER)
    

    user = coviddb.session.query(UserRoles).filter_by(email=email).first()

    if not user:
        current_app.logger.info(INVALID_USER)
        return Helper.create_error_response(404, INVALID_USER)

    if user.confirmed_at_by_user:
        current_app.logger.info(ALREADY_CONFIRMED)
        # return Response(status=409)
        return Helper.create_error_response(409, ALREADY_CONFIRMED)

    user.confirm_email()
    user.hash_password(password)
    coviddb.session.commit()
    
    # TODO: Insert Email into userdb.admin
    
    # return Response(status=200)
    return Helper.create_success_response(USER_CONFIRMED)


@userRoles_api.route('/usersRoles/login', methods=['POST'])
def generate_login_token():
    data = request.get_json(force=True)
    
    email = data["email"]
    password = data["password"]
    
    if not email or not password:
        return Helper.create_error_response(400, INCOMPLETE_BODY_PARAMETER)
    
    if not Helper.email_validator(email):
        return Helper.create_error_response(400, "Invalid email format.")

    user = coviddb.session.query(UserRoles).filter_by(email=email).first()
    
    if not user or not user.verify_password(password):
        current_app.logger.info(INVALID_USER)
        # return Response(status=404)
        return Helper.create_error_response(404, INVALID_USER)
    
    # if not user.verify_password(password):
    #     current_app.logger.info(INVALID_PASSWORD)
    #     # return Response(status=401)
    #     return Helper.create_error_response(401, INVALID_PASSWORD)

    if not user.confirmed_at_by_user:
        current_app.logger.info(EMAIL_NOT_CONFIRMED)
        # return Response(EMAIL_NOT_CONFIRMED, status=403)
        return Helper.create_error_response(403, EMAIL_NOT_CONFIRMED)

    if not user.confirmed_at_by_admin:
        current_app.logger.info(ACCOUNT_NOT_APPROVED_BY_ADMIN)
        # return Response(ACCOUNT_NOT_APPROVED_BY_ADMIN, status=403)
        return Helper.create_error_response(403, ACCOUNT_NOT_APPROVED_BY_ADMIN)

    token = Token(user.id, user.role)
 
    userData = user.to_json()
        
    access_token = jwt.encode(userData, "secret", algorithm="HS256")
    #access_token = create_access_token(identity=token.id, admin=True)
    refresh_token = create_refresh_token(identity=token.id)
    
    user_json = user.to_json()
    strToken = str(access_token)[2:len(str(access_token))-1]
    
    user_json["token"] = {
        "access_token": strToken, 
        "refresh_token": refresh_token
    }
    
    user_json["is_trusted"] = True
    current_app.logger.info(USER_LOGGED_IN)
    
    # return Response(json.dumps(user_json), mimetype='application/json')
    return Helper.create_success_response(USER_LOGGED_IN, user_json)


# @userRoles_api.route('/users/login/verify', methods=['GET'])
# @authenticateAdmin
# def get_user(user_id, user):
#     return Response('this is logged in', mimetype='application/json')


# @userRoles_api.route('/users/verify', methods=['GET'])
# @authenticate_user
# def verify_user(user_id, user):
#     return Response(json.dumps(user.to_json()), mimetype='application/json')