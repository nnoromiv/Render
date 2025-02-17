from datetime import timedelta

from flask import request, current_app, Response
from flask_jwt_extended import create_access_token, create_refresh_token
import jwt
import json

from happy_again.apis.utils import Helper
from happy_again.apis.users.utils import UsersUtils

from happy_again import db
from happy_again.apis.users import user_api
from happy_again.apis.users.consts import *
from happy_again.auth import authenticate, admin_required
from happy_again.common.consts import *
from happy_again.common.utils import send_email_with_attachments, send_email
from happy_again.models import User, Session, UserInfo, CheckedUsers, NotifiedUsers, OtpCodes, NoVoucher, \
    SubjectUniqueId, FactorAnalysisData, ComponentScoreCoefficient, CompletedTasks
from happy_again.common.consts import deployment
from happy_again.models.users import Admin

# emails in different languages
# from happy_again.apis.users.email_languages.en import en
# from happy_again.apis.users.email_languages.it import it

from flask_cors import CORS
from datetime import datetime
import numpy as np
import pandas as pd
import math
import uuid

CORS(user_api)


# email language selection moved to utils

# def select_lan(lan):
#     if lan == 'en':
#         return en
#     elif lan == 'it':
#         return it


# def select_pdf(lan):
#     if lan == 'en':
#         return 'Info_Sheet_ENG.pdf'
#     elif lan == 'it':
#         return 'Info_Sheet_ITA.pdf'

# 1.User Registration api

@user_api.route('/users', methods=['POST'])
def user_register(): 
    data = request.get_json(force=True)
    
    email = data['email']
    password = data['password']
    language = data['language']

    if not email or not password:
        return Helper.create_error_response(400, "The 'email' and 'password' fields are required.")

    if not Helper.email_validator(email):
        return Helper.create_error_response(400, "Invalid email format.")
    
    user = db.session.query(User).filter_by(email=email).order_by(User.registered_at.desc()).first()
    
    if user:
        current_app.logger.info(USER_ALREADY_REGISTERED.format(user.email))
        # return Response(USER_ALREADY_REGISTERED.format(user.email), status=409)
        return Helper.create_error_response(409, USER_ALREADY_REGISTERED.format(user.email))
    else:
        userid = str(uuid.uuid4().hex + "_1")
        # current_app.logger.info(USER_ALREADY_REGISTERED.format(user.email))
        # return Response(USER_ALREADY_REGISTERED.format(user.email), status=409)

    user = User(userid, email, password)
    user_info = UserInfo(language=language, user_id=user.id, lc_flag=None)

    token = create_access_token(user.id, expires_delta=timedelta(days=USER_CONFIRMATION_TOKEN_EXPIRY_DELTA))

    confirm_url = CONFIRMATION_URL.format(site=SITE_URL, token=token)

    send_email_with_attachments(
        to=[user.email], 
        subject=SUBJECT_USER_CONFIRMATION_EMAIL.format(lan=UsersUtils.select_lan(language)),
        msg_html=HTML_MESSAGE_REGISTER.format(lan=UsersUtils.select_lan(language), url=confirm_url),
        pdfname=UsersUtils.select_pdf(language)
    )

    db.session.add(user)
    db.session.add(user_info)
    db.session.commit()
    # current_app.logger.info(USER_REGISTERED.format(user.email))
        
    data = {
        **user.to_json(),
        "token": token
    }
    return Helper.create_success_response("", data)
    # return Response(json.dumps(user.to_json()), status=200, mimetype='application/json')


# 2.User Resend Confirmation Link api
@user_api.route('/users/resend-confirmation/<user_email>', methods=['GET'])
def user_resend_confirmation(user_email):
    lan = request.args.get('language')

    user = db.session.query(User).filter_by(email=user_email).first()
    
    if not Helper.email_validator(user_email):
        return Helper.create_error_response(400, "Invalid email format.")
    
    if not user:
        current_app.logger.info(USER_NOT_REGISTERED.format(user_email))
        # return Response(USER_NOT_REGISTERED.format(user_email), status=404)
        return Helper.create_error_response(404, USER_NOT_REGISTERED.format(user_email))
    if user.confirmed_at_by_user:
        # return Response(ALREADY_CONFIRMED, status=409)
        return Helper.create_error_response(409, ALREADY_CONFIRMED)

    token = create_access_token(user.id, expires_delta=timedelta(days=USER_CONFIRMATION_TOKEN_EXPIRY_DELTA))
    confirm_url = CONFIRMATION_URL.format(site=SITE_URL, token=token)

    send_email_with_attachments(
        to=[user.email], 
        subject=SUBJECT_USER_CONFIRMATION_EMAIL.format(lan=UsersUtils.select_lan(lan)),
        msg_html=HTML_MESSAGE_REGISTER.format(lan=UsersUtils.select_lan(lan), url=confirm_url),
        pdfname=UsersUtils.select_pdf(lan)
    )
    
    data = {
        **user.to_json(),
        "token": token
    }

    return Helper.create_success_response("Email Sent", data)
    # return Response(json.dumps(user.to_json()), '200', mimetype='application/json')


# 3.User Confirmation by user api
@user_api.route('/users/verify/<token>', methods=['GET'])
def confirm_email(token):

    user = Helper.validate_jwt_token(token)

    """
        user, {
            'iat': 1614970302, 
            'nbf': 1614970302, 
            'jti': '2d4c9007-1dee-41e8-a644-58927de6345b', 
            'exp': 1615143102,
            'identity': '43037787de214a0fbd4b9bcb16b8c81b', 
            'fresh': False, 
            'type': 'access', 
            'user_claims': {}
            }
    """
    
    if isinstance(user, dict):
        if deployment:
            user_id = user.get("identity")  # DEPLOYED
        else:
            user_id = user.get("sub")  # LOCAL
    else:
        return user

    if not user_id:
        current_app.logger.info(INVALID_TOKEN)
        # return Response(INVALID_TOKEN, status=400)
        return Helper.create_error_response(400, INVALID_TOKEN)

    user = db.session.query(User).filter_by(id=user_id).first()
    if not user:
        current_app.logger.info(INVALID_USER)
        # return Response(INVALID_USER, status=404)
        return Helper.create_error_response(404, INVALID_USER)

    if user.confirmed_at_by_user:
        current_app.logger.info(ALREADY_CONFIRMED)
        # return Response(ALREADY_CONFIRMED, status=409)
        return Helper.create_error_response(409, ALREADY_CONFIRMED)

    user.confirm_email()
    db.session.commit()
    current_app.logger.info(USER_CONFIRMED)
    # return Response(USER_CONFIRMED, status=200)
    return Helper.create_success_response(USER_CONFIRMED, {})


# 4.User Login api
@user_api.route('/users/login', methods=['POST'])
def generate_login_token():
    data = request.get_json(force=True)
    email = data['email']
    password = data["password"]
    
    if not Helper.email_validator(email):
        return Helper.create_error_response(400, "Invalid email format.")

    user = db.session.query(User).filter_by(email=email).order_by(User.registered_at.desc()).first()

    if not user or not user.verify_password(password):
        current_app.logger.info(INVALID_USER)
        # return Response(INVALID_USER, status=404)
        return Helper.create_error_response(404, INVALID_USER)

    if not user.confirmed_at_by_user:
        current_app.logger.info(EMAIL_NOT_CONFIRMED)
        # return Response(EMAIL_NOT_CONFIRMED, status=403)
        return Helper.create_error_response(403, EMAIL_NOT_CONFIRMED)
    if user.blocked == 1:
        current_app.logger.info(USER_BLOCKED)
        # return Response(USER_BLOCKED, status=405)
        return Helper.create_error_response(405, USER_BLOCKED)


    session_info = Session(user.id)
    db.session.add(session_info)
    db.session.commit()

    if deployment:
        access_token = jwt.encode(session_info.to_json(), "secret", algorithm="HS256").decode("utf-8")
    else:
        access_token = jwt.encode(session_info.to_json(), "secret", algorithm="HS256")

    refresh_token = create_refresh_token(identity=session_info.id)
    strToken = str(access_token)[0:len(str(access_token))]

    user_json = user.to_json()
    user_json["token"] = {
        "access_token": strToken, 
        "refresh_token": refresh_token
    }
    user_json["is_trusted"] = True
    user_json["session_id"] = session_info.id
    
    current_app.logger.info(USER_LOGGED_IN)
    # return Response(json.dumps(user_json), status=200, mimetype='application/json')
    return Helper.create_success_response(USER_LOGGED_IN, user_json)


# user block api
@user_api.route('/users/block', methods=['PUT'])
@authenticate
def block_user(user_id, user):
    user = db.session.query(User).filter_by(id=user_id).first()
    user.block_user()
    db.session.commit()

    # return Response(USER_BLOCKED, status=200)
    return Helper.create_success_response(USER_BLOCKED)


@user_api.route('/users/unblock/<user_id>', methods=['PUT'])
def unblock_user(user_id):
    user = db.session.query(User).filter_by(id=user_id).first()
    
    if not user:
        return Helper.create_error_response(401, "User not found")
    
    user.unblock_user()
    db.session.commit()

    # return Response(status=200)
    return Helper.create_success_response(USER_UNBLOCKED)


@user_api.route('/users/extend/<user_email>/<time>', methods=['PUT'])
def extend_user(user_email, time):
    user = db.session.query(NotifiedUsers).filter_by(email=user_email).first()
        
    if not user:
        return Helper.create_error_response(401, "User not found")
    
    if not Helper.email_validator(user_email):
        return Helper.create_error_response(400, "Invalid email format.")
    
    user.extend_user(time)
    db.session.commit()

    # return Response(status=200)
    return Helper.create_success_response(EXTEND_TIME)


# 5.User Session Information update api
@user_api.route('/users/session/<session_id>', methods=['PUT'])
@authenticate
def session_info_add(user_id, user, session_id):
    data = request.get_json(force=True)
    
    browser=data['browser'], 
    version=data['version'], 
    op_system=data['op_system'], 
    screen_resolution=data['screen_resolution'],
    pixel_density_h=data['pixel_density_h'],
    pixel_density_w=data['pixel_density_w'], 
    user_agent=data['user_agent'],
        
    user = db.session.query(User).filter_by(id=user_id).first()
    if not user:
        current_app.logger.info(INVALID_USER)
        # return Response(INVALID_USER, status=404)
        return Helper.create_error_response(404, INVALID_USER)

    session_info = db.session.query(Session).filter_by(
        id=session_id, user_id=user_id).first()

    if not session_info:
        current_app.logger.info(INVALID_SESSION)
        # return Response(INVALID_SESSION, status=404)
        return Helper.create_error_response(404, INVALID_SESSION)

    if session_info.end_time:
        current_app.logger.info(INVALID_SESSION)
        # return Response(USER_ALREADY_LOGGED_OFF, status=409)
        return Helper.create_error_response(409, USER_ALREADY_LOGGED_OFF)
    
    session_info.update_session_data(browser, version, op_system, screen_resolution, pixel_density_h, pixel_density_w, user_agent, user_id)
    
    db.session.commit()

    current_app.logger.info(SESSION_INFORMATION_UPDATED)
    # return Response(json.dumps(session_info.to_json()), status=200, mimetype='application/json')
    return Helper.create_success_response(SESSION_INFORMATION_UPDATED, session_info.to_json())

# 6.User Logged off update api
@user_api.route('/users/logoff/<session_id>', methods=['PUT'])
@authenticate
def logoff_update(user_id, user, session_id):
    user = db.session.query(User).filter_by(id=user_id).first()
    if not user:
        current_app.logger.info(INVALID_USER)
        # return Response(INVALID_USER, status=404)
        return Helper.create_error_response(404, INVALID_USER)

    session_info = db.session.query(Session).filter_by(id=session_id, user_id=user_id).first()

    if not session_info:
        current_app.logger.info(INVALID_SESSION)
        # return Response(INVALID_SESSION, status=404)
        return Helper.create_error_response(404, INVALID_SESSION)

    if session_info.end_time:
        current_app.logger.info(INVALID_SESSION)
        # return Response(USER_ALREADY_LOGGED_OFF, status=409)
        return Helper.create_error_response(409, USER_ALREADY_LOGGED_OFF)

    session_info.logged_out()
    db.session.commit()

    current_app.logger.info(USER_LOGGED_OFF)
    # return Response(USER_LOGGED_OFF, status=200, mimetype='application/json')
    return Helper.create_success_response(USER_LOGGED_OFF)


# 7.User Info Update api
@user_api.route('/users/info/<session_id>', methods=['PUT'])
@authenticate
def users_info_update(user_id, user, session_id):
    data = request.get_json(force=True)
    
    age=data['age']
    gender=data['gender']
    
    if not age or not gender:
        return Helper.create_error_response(400, INCOMPLETE_BODY_PARAMETER)

    user = db.session.query(User).filter_by(id=user_id).first()
    if not user:
        current_app.logger.info(INVALID_USER)
        # return Response(INVALID_USER, status=404)
        return Helper.create_error_response(404, INVALID_USER)

    session_info = db.session.query(Session).filter_by(id=session_id, user_id=user_id).first()

    if not session_info:
        current_app.logger.info(INVALID_SESSION)
        # return Response(INVALID_SESSION, status=404)
        return Helper.create_error_response(404, INVALID_SESSION)

    if session_info.end_time:
        current_app.logger.info(INVALID_SESSION)
        # return Response(USER_ALREADY_LOGGED_OFF, status=409)
        return Helper.create_error_response(409, USER_ALREADY_LOGGED_OFF)

    user_info = db.session.query(UserInfo).filter_by(user_id=user_id).first()

    if not user_info:
        current_app.logger.info(INVALID_USER_INFO)
        # return Response(INVALID_USER_INFO, status=404)
        return Helper.create_error_response(404, INVALID_USER_INFO)

    user_info.update_user_info(age, gender)
    db.session.commit()

    current_app.logger.info(USER_LOGGED_IN)
    # return Response(json.dumps(user_info.to_json()), status=200, mimetype='application/json')
    return Helper.create_success_response(USER_LOGGED_IN, user_info.to_json())

# 8.Forgot Password api
@user_api.route('/users/forgot-password', methods=['POST'])
def user_forgot_password():
    data = request.get_json(force=True)
    
    email = data['email']
    language = data['language']
        
    if not email:
        return Helper.create_error_response(400, EMAIL_IS_REQUIRED)

    user = db.session.query(User).filter_by(email=email).order_by(User.registered_at.desc()).first()

    if not user:
        # return Response(USER_NOT_REGISTERED.format(data['email']), status=404)
        return Helper.create_error_response(404, USER_NOT_REGISTERED.format(email))

    token = create_access_token(user.id, expires_delta=timedelta(days=USER_CONFIRMATION_TOKEN_EXPIRY_DELTA))

    reset_password_url = RESET_PASSWORD_URL.format(site=SITE_URL, token=token)
    send_email(
        to=[user.email],
        subject=SUBJECT_USER_RESET_PASSWORD.format(
        lan=UsersUtils.select_lan(language)),
        msg_html=HTML_MESSAGE_RESET_PASSWORD.format(lan=UsersUtils.select_lan(language),url=reset_password_url)
    )

    # return Response(USER_RESET_PASSWORD_LINK_SENT, status='200', mimetype='application/json')
    return Helper.create_success_response(USER_RESET_PASSWORD_LINK_SENT, { "token": token })


# 9.User Reset Password api
@user_api.route('/users/reset-password', methods=['POST'])
def user_reset_password():
    data = request.get_json(force=True)
    
    token = data["token"]
    password = data['password']
    
    if not token or not password:
        return Helper.create_error_response(400, INCOMPLETE_BODY_PARAMETER)
    
    user = Helper.validate_jwt_token(token)

    """
        user, {
            'iat': 1614970302, 
            'nbf': 1614970302, 
            'jti': '2d4c9007-1dee-41e8-a644-58927de6345b', 
            'exp': 1615143102,
            'identity': '43037787de214a0fbd4b9bcb16b8c81b', 
            'fresh': False, 
            'type': 'access', 
            'user_claims': {}
        }
    """
    
    if isinstance(user, dict):
        if deployment:
            user_id = user.get("identity")  # DEPLOYED
        else:
            user_id = user.get("sub")  # LOCAL
    else:
        return user

    if not user_id:
        current_app.logger.info(INVALID_TOKEN)
        # return Response(INVALID_TOKEN, status=400)
        return Helper.create_error_response(400, INVALID_TOKEN)

    user = db.session.query(User).filter_by(id=user_id).first()
    if not user:
        current_app.logger.info(INVALID_USER)
        # return Response(INVALID_USER, status=404)
        return Helper.create_error_response(404, INVALID_USER)

    user.change_password(password)
    db.session.commit()

    current_app.logger.info(USER_PASSWORD_RESET)
    # return Response(USER_PASSWORD_RESET, status=200)
    return Helper.create_success_response(USER_PASSWORD_RESET)


@user_api.route('/users/login/verify', methods=['GET'])
@authenticate
def get_user(user_id, user):
    current_app.logger.info(USER_LOGGED_IN)
    # return Response(USER_LOGGED_IN, mimetype='application/json')
    return Helper.create_success_response(USER_LOGGED_IN)


# @user_api.route('/users/verify', methods=['GET'])
# @authenticate_user
# def verify_user(user_id, user):
#     # return Response(json.dumps(user.to_json()), status=200, mimetype='application/json')
#     return Helper.create_success_response("", user.to_json())


@user_api.route('/users/checkAdmin', methods=['GET'])
@authenticate
def checkAdmin(user_id, user):
    email = user["email"]
    
    if not email:
        return Helper.create_error_response(400, EMAIL_IS_REQUIRED)
    
    admin = db.session.query(Admin).filter_by(email=email).first()
    
    if admin == None:
        data = {'isAdmin': False}
        return Helper.create_success_response("", data)
    
    # else:
    #     data = {'isAdmin': True}
    # return Response(json.dumps(data), mimetype='application/json')
    return Helper.create_success_response("", {'isAdmin': True})

@user_api.route('/users/admin', methods=['GET'])
def get_admins():
    users = db.session.query(Admin).all()
    data = []
    for user in users:
        data.append(user.to_json())
        
    # return Response(json.dumps(data), mimetype='application/json')
    return Helper.create_success_response("", { "data": data })


@user_api.route('/users/checkvoucher/<user_email>', methods=['PUT'])
def update_check_voucher(user_email):
    user = db.session.query(CheckedUsers).filter_by(email=user_email).first()
    
    if not user:
        return Helper.create_error_response(400, INVALID_USER)
    
    if not Helper.email_validator(user_email):
        return Helper.create_error_response(400, "Invalid email format.")
    
    user.update_checkbox()
    db.session.commit()

    # return Response(json.dumps(user_email), status=200, mimetype='application/json')
    return Helper.create_success_response("", { "email": user_email })


@user_api.route('/users/checkedUsers', methods=['GET'])
def get_checked_users():
    users = db.session.query(CheckedUsers).all()
    data = []
    for user in users:
        data.append(user.to_json())
        
    # return Response(json.dumps(data), mimetype='application/json')
    return Helper.create_success_response("", { "data": data })


@user_api.route('/users/notifiedUsers', methods=['GET'])
def getNotifiedUsers():
    users = db.session.query(NotifiedUsers).all()
    data = []
    for user in users:
        data.append(user.to_json())
        
    # return Response(json.dumps(data), mimetype='application/json')
    return Helper.create_success_response("", { "data": data })


@user_api.route('/users/otp-codes', methods=['GET'])
def getAllCodes():
    codes = db.session.query(OtpCodes).all()
    data = []
    for code in codes:
        data.append(code.to_json())
        
    # return Response(json.dumps(data), mimetype='application/json')
    return Helper.create_success_response("", { "data": data })


@user_api.route('/users/deleteCode/<otpcode>', methods=['DELETE'])
def deleteCode(otpcode):
    code = db.session.query(OtpCodes).filter_by(code=otpcode).first()

    if code:
        db.session.delete(code)
        db.session.commit()
        # return Response("Code deleted successfully", status=200)
        return Helper.create_success_response("Code deleted successfully")
    else:
        # return Response("Code not found", status=404)
        return Helper.create_error_response(404, "Code not found")


@user_api.route('/no_voucher', methods=['POST'])
def no_voucher_insert():
    data = request.get_json(force=True)
    email = data['email']
    nation = data['nation']
    
    if not email or not nation:
        return Helper.create_error_response(400, INCOMPLETE_BODY_PARAMETER)
        
    if not Helper.email_validator(email):
        return Helper.create_error_response(400, "Invalid email format.")
    
    user = NoVoucher(email, nation)

    db.session.add(user)
    db.session.commit()

    # return Response(json.dumps(user.to_json()), status=200, mimetype='application/json')
    return Helper.create_success_response("", user.to_json())


@user_api.route('/users/noVoucherUsers', methods=['GET'])
@admin_required
def get_no_voucher_users():
    users = db.session.query(NoVoucher).all()
    data = []
    for user in users:
        data.append(user.to_json())
        
    # return Response(json.dumps(data), mimetype='application/json')
    return Helper.create_success_response("", { "data": data })


@user_api.route('/users/blockedUsers', methods=['GET'])
@admin_required
def get_blocked_users():
    users = db.session.query(User).filter_by(blocked='1').all()
    data = []
    for user in users:
        data.append(user.to_json())
        
    # return Response(json.dumps(data), mimetype='application/json')
    return Helper.create_success_response("", { "data": data })


@user_api.route('/users/subjectId', methods=['GET'])
def get_subject_id():
    users = db.session.query(SubjectUniqueId).all()
    data = []
    for user in users:
        data.append(user.to_json())
        
    # return Response(json.dumps(data), mimetype='application/json')
    return Helper.create_success_response("", { "data": data })

# TODO: IGNORE
# Get all the data to apply factor analysis
@user_api.route('/users/faData', methods=['GET'])
def get_factor_analysis_data():
    helper = Helper()
    
    result = (
        db.session.query(FactorAnalysisData, UserInfo)
        .outerjoin(UserInfo, FactorAnalysisData.user_id == UserInfo.user_id)
        .filter(FactorAnalysisData.user_id == UserInfo.user_id)
        .all()
    )
    
    users = helper.merged_record(result)
    
    coefficient = db.session.query(ComponentScoreCoefficient).all()
    coefficients = []
    temp = []
    for c in coefficient:
        c_json = c.to_json()
                
        c_json = [i for i in [c_json] if i['index'] not in [39, 40, 41, 43,44, 45, 46, 58, 59, 60, 62, 63, 64, 65]]
        temp.append(c_json)
                
    coefficients = [item for sublist in temp for item in sublist]

    admins = db.session.query(Admin).all()
    admin_email = [i.email for i in admins]
    admin_datas = db.session.query(User).filter(User.email.in_(admin_email)).all()

    noValid = db.session.query(NoVoucher).filter_by(nation="EN").all()
    noValid_email = [i.email for i in noValid]
    noValid_datas = db.session.query(User).filter(User.email.in_(noValid_email)).all()

    datasForFactorNew = []
    for user in users:
        if UsersUtils.is_user_valid(user, admin_datas, noValid_datas) == 1:
            datasForFactorNew.append(user)
            
    keys_to_delete = [
        'covidq11_diarrhea', 
        'covidq11_stomach_aches', 
        'covidq11_loss_of_appetite',
        
        'covidq11_cough',
        'covidq11_headaches',
        'covidq11_sore_throat',
        'covidq11_changes_to_sense_of_smell_or_taste',
        
        'covidq13_diarrhea', 
        'covidq13_stomach_aches', 
        'covidq13_loss_of_appetite',
        
        'covidq13_cough',
        'covidq13_headaches',
        'covidq13_sore_throat',
        'covidq13_changes_to_sense_of_smell_or_taste',
    ]
            
    for item in datasForFactorNew:
        for key in keys_to_delete:
            if key in item:
                del item[key]

    df = pd.DataFrame(datasForFactorNew)
    
    df = df.rename(columns={'covidq11_feeling_sick': 'covidq11_sick_dia_stomach_appetite'})
    df = df.rename(columns={'covidq11_high_temperature': 'covidq11_highT_cough_head_throat_smell_taste'})

    df = df.rename(columns={'covidq13_feeling_sick': 'covidq13_sick_dia_stomach_appetite'})    # Convert the condensed distance matrix into a complete matrix
    df = df.rename(columns={'covidq13_high_temperature': 'covidq13_highT_cough_head_throat_smell_taste'})    # Convert the condensed distance matrix into a complete matrix

    df_dict_list = df.to_dict(orient="records")
    datasForFactorNew.clear()
    datasForFactorNew.append(df_dict_list[0])

    # Set 'uid' as the index
    df.set_index('user_id', inplace=True)

    # Select only the numeric columns (excluding 'uid')
    numeric_columns = df.select_dtypes(include=[np.number]).columns

    # Merge the data with 'uid'
    original_df = df[numeric_columns]

    # Print the normalized data
    original_data = original_df.reset_index().to_dict(orient='records')

    # Print the normalized data
    datassss = original_df.reset_index().to_dict(orient='records')

    for d in original_data:
        for key, value in d.items():
            if isinstance(value, float) and math.isnan(value):
                d[key] = 'NaN'

    factor = []
    uniques = []
    uniqueid = db.session.query(SubjectUniqueId).all()
    for i in uniqueid:
        uniques.append(i.to_json())

    for _ in range(len(uniques)):
        factor.append([])

    question_column_names = [column for column in coefficients[0].keys() if column not in ('index', 'question')]
    user_column_names = [column for column in datassss[0].keys() if column not in 'user_id']
    question_matrix = np.array([[question[column_name] for column_name in question_column_names] for question in coefficients])
    user_matrix = np.array([[user[column_name] for column_name in user_column_names] for user in datassss])

    column_means = np.nanmean(user_matrix, axis=0)

    # Find the indices of 'NaN' values in the user_matrix
    nan_indices = np.isnan(user_matrix)

    # Replace 'NaN' values with the mean of the corresponding columns
    user_matrix[nan_indices] = np.take(column_means, np.where(nan_indices)[1])
    
    # Pad question_matrix with a row of 1s to match the shape (84, 21)
    padding = np.ones((1, question_matrix.shape[1]))  # Create a row of 1s with the same number of columns
    question_matrix_padded = np.vstack([question_matrix, padding])  # Stack the padding to the original matrix

    factors = np.dot(user_matrix, question_matrix_padded)
    user_ids = [user['user_id'] for user in datassss]
    lc_flags = [user['lc_flag'] for user in datassss]
    result_matrix = np.column_stack((user_ids, factors, lc_flags))
    
    result = []
    for i in result_matrix:
        # Create a dictionary for each row
        result.append({
            'user_id': i[0], 
            **{str(j): i[j-1] for j in range(1, 22)},  # Create keys '1' to '21' dynamically
            'lc_flag': i[22]  # Add 'lc_flag' explicitly
        })
    
    for d in datasForFactorNew:
        for key, value in d.items():
            if isinstance(value, float) and math.isnan(value):
                d[key] = 0

    data_without_user_id = pd.DataFrame(datassss).drop(columns=['user_id'])
    data_without_user_id = data_without_user_id.fillna(data_without_user_id.mean())
    
    num_samples = data_without_user_id.shape[1]  # We use shape[1] for the number of column
    distance_matrix = np.zeros((num_samples, num_samples))
        
    # for idx, col in enumerate(data_without_user_id.columns):
    #     print(f"{idx}: {col}")

    for i in range(num_samples):
        for j in range(i + 1, num_samples):
            u = data_without_user_id.iloc[:, i]  # Select the colum i
            v = data_without_user_id.iloc[:, j]  # Select the colum j
            distance = np.linalg.norm(u - v)  # Euclidean distance
            distance_matrix[i, j] = distance
            distance_matrix[j, i] = distance
             
    distance = []
    column_names = data_without_user_id.columns.to_list()
    for index, i in enumerate(distance_matrix):
        if index < len(datassss):  
            distance.append({col: i[idx] for idx, col in enumerate(column_names)})
            distance[-1]['lc_flag'] = datassss[index]['lc_flag']  # Add lc_flag separately
        else:
            pass
        
    # for index, i in enumerate(distance_matrix):
    #     if index < len(datassss):
    #         distance.append({
    #             'age': i[0],
    #             'covidq1': i[1],
    #             'covidq2': i[2],
    #             'covidq3': i[3],
    #             'covidq4_dry_continuous_cough': i[4],
    #             'covidq4_sore_throat': i[5],
    #             'covidq4_runny_nose_nasal_congestion': i[6],
    #             'covidq4_loss_of_taste_smell': i[7],
    #             'covidq4_loss_of_appetite': i[8],
    #             'covidq4_fever': i[9],
    #             'covidq4_chills': i[10],
    #             'covidq4_headache': i[11],
    #             'covidq4_body_aches': i[12],
    #             'covidq4_fatigue': i[13],
    #             'covidq4_shortness_breath': i[14],
    #             'covidq4_nausea_and_or_vomiting': i[15],
    #             'covidq4_diarrhea': i[16],
    #             'covidq4_other': i[17],
    #             'covidq4_total': i[18],
    #             'covidq6': i[19],
    #             'covidq7': i[20],
    #             'covidq8': i[21],
    #             'covidq9': i[22],
    #             'covidq10': i[23],
    #             'covidq11_extreme_tiredness_fatigue': i[24],
    #             'covidq11_shortness_of_breath': i[25],
    #             'covidq11_chest_pain_or_tightness': i[26],
    #             'covidq11_problems_with_memory': i[27],
    #             'covidq11_problems_with_concentration': i[28],
    #             'covidq11_difficulties_sleeping_insomnia': i[29],
    #             'covidq11_difficulties_heart_palpitations': i[30],
    #             'covidq11_dizziness': i[31],
    #             'covidq11_pins_and_needles': i[32],
    #             'covidq11_joint_pain': i[33],
    #             'covidq11_depression': i[34],
    #             'covidq11_anxiety': i[35],
    #             'covidq11_tinnitus': i[36],
    #             'covidq11_earache': i[37],
    #             'covidq11_feeling_sick': i[38],
    #             # 'covidq11_diarrhea': i[39],
    #             # 'covidq11_stomach_aches': i[40],
    #             # 'covidq11_loss_of_appetite': i[41],
    #             'covidq11_high_temperature': i[39],
    #             # 'covidq11_cough': i[43],
    #             # 'covidq11_headaches': i[44],
    #             # 'covidq11_sore_throat': i[45],
    #             # 'covidq11_changes_to_sense_of_smell_or_taste': i[46],
    #             'covidq11_rashes': i[40],
    #             'covidq11_other': i[41],
    #             'covidq11_total': i[42],
    #             'covidq13_extreme_tiredness_fatigue': i[43],
    #             'covidq13_shortness_of_breath': i[44],
    #             'covidq13_chest_pain_or_tightness': i[45],
    #             'covidq13_problems_with_memory': i[46],
    #             'covidq13_problems_with_concentration': i[47],
    #             'covidq13_difficulties_sleeping_insomnia': i[48],
    #             'covidq13_difficulties_heart_palpitations': i[49],
    #             'covidq13_dizziness': i[50],
    #             'covidq13_pins_and_needles': i[51],
    #             'covidq13_joint_pain': i[52],
    #             'covidq13_depression': i[53],
    #             'covidq13_anxiety': i[54],
    #             'covidq13_tinnitus': i[55],
    #             'covidq13_earache': i[56],
    
    #             'covidq13_feeling_sick': i[57],
    #             'covidq13_diarrhea': i[58],
    #             'covidq13_stomach_aches': i[59],
    #             'covidq13_loss_of_appetite': i[60],
    
    #             'covidq13_high_temperature': i[61],
    #             'covidq13_cough': i[62],
    #             'covidq13_headaches': i[63],
    #             'covidq13_sore_throat': i[64],
    #             'covidq13_changes_to_sense_of_smell_or_taste': i[65],
    
    #             'covidq13_rashes': i[66],
    #             'covidq13_other': i[67],
    #             'covidq13_total': i[68],
    #             'covidq15': i[69],
    #             'qol_total_score': i[70],
    #             'qol11': i[71],
    #             'qol16': i[72],
    #             'fatigue_total_score': i[73],
    #             'fatigue8': i[74],
    #             'fatigue11': i[75],
    #             'lc_flag': datassss[index]['lc_flag']
    #         })
    #     else:
    #         pass
        
    data = [datasForFactorNew, result, original_data, distance]

    # return Response(json.dumps(data), mimetype='application/json')
    return Helper.create_success_response("", { "data": data })


@user_api.route('/subjectIdAdd', methods=['POST'])
def add_subject_id():
    data = request.get_json(force=True)
    id = data['id']
    email = data['email']
    subject_id = data['subject_id']
    
    if not id or not email or not subject_id:
        return Helper.create_error_response(400, INCOMPLETE_BODY_PARAMETER)
    
    if not Helper.email_validator(email):
        return Helper.create_error_response(400, "Invalid email format.")
    
    if not isinstance(subject_id, int):
        return Helper.create_error_response(400, "Subject ID must be Integer")
    
    user = SubjectUniqueId(id, email, int(subject_id))

    db.session.add(user)
    db.session.commit()

    # current_app.logger.info(USER_REGISTERED.format(user.email))
    # return Response(json.dumps(user.to_json()), status=200, mimetype='application/json')
    return Helper.create_success_response("", user.to_json())


@user_api.route('/users/usGet', methods=['GET'])
def get_us_get():
    users = db.session.query(User).all()
    data = []
    for user in users:
        data.append(user.to_json())
        
    # return Response(json.dumps(data), mimetype='application/json')
    return Helper.create_success_response("", { "data": data })


@user_api.route('/users/list-attempts/<search>', methods=['GET'])
@admin_required
def list_attempts(search):
    users = db.session.query(User).filter(User.email.like(f'%{search}%')).all()
    data = {}

    for user in users:
        user_id = user.id.split("_")[0]
        attempt = int(user.id.split("_")[1])

        completed_tasks = CompletedTasks.query.with_entities(CompletedTasks.task_completed).filter(
            CompletedTasks.user_id.like(f'{user_id}%')).all()

        unique_special_tasks = set()
        completed_tasks_count = 0

        for task in completed_tasks:
            task_name = task[0]
            if task_name in ["Covid", "Quality", "Fatigue"]:
                if task_name not in unique_special_tasks:
                    unique_special_tasks.add(task_name)
                    completed_tasks_count += 1
            else:
                completed_tasks_count += 1

        current_attempt_completed_tasks = CompletedTasks.query.with_entities(CompletedTasks.task_completed).filter_by(user_id=user.id).all()

        if attempt > 1:
            completed_tasks_joined = ', '.join([task[0] for task in current_attempt_completed_tasks if task[0] not in ["Covid", "Fatigue", "Quality"]])
        else:
            completed_tasks_joined = ', '.join([task[0] for task in current_attempt_completed_tasks])

        if user_id in data:
            if attempt > data[user_id]['attempt']:
                data[user_id]['user_id'] = user.id
                data[user_id]['attempt'] = attempt
                data[user_id]['current_attempt_completed_tasks'] = completed_tasks_joined
        else:
            data[user_id] = {
                'user_id': user.id,
                'email': user.email,
                'attempt': attempt,
                'completed_tasks': completed_tasks_count,
                'current_attempt_completed_tasks': completed_tasks_joined
            }

    response_data = list(data.values())
    # return Response(json.dumps(response_data), mimetype='application/json')
    return Helper.create_success_response("", { "data": response_data })


@user_api.route('/users/create-new-attempt/<user_id>', methods=['POST'])
@admin_required
def create_new_attempt(user_id):
    user = db.session.query(User).filter_by(id=user_id).first()
    
    if user:
        completed_tasks = CompletedTasks.query.with_entities(CompletedTasks.task_completed).filter_by(user_id=user.id).all()
        completed_tasks_count = len(completed_tasks)

        if completed_tasks_count >= 10 or int(user_id[-1]) >= 1:
            last_ch = user.id[-1]
            new_last_ch = str(int(last_ch) + 1)
            userid = user.id[:-1] + new_last_ch

            new_completed_task1 = CompletedTasks(
                user_id=userid,
                task_completed="Covid",
                timestamp=datetime.now()
            )
            new_completed_task2 = CompletedTasks(
                user_id=userid,
                task_completed="Fatigue",
                timestamp=datetime.now()
            )
            new_completed_task3 = CompletedTasks(
                user_id=userid,
                task_completed="Quality",
                timestamp=datetime.now()
            )
            db.session.add(new_completed_task1)
            db.session.add(new_completed_task2)
            db.session.add(new_completed_task3)
            db.session.commit()

            user = User(userid, user.email, user.password_hash)
            old_user_info = db.session.query(UserInfo).filter_by(user_id=user_id).first()
            
            if old_user_info == None:
                user_info = UserInfo(language='en', user_id=user.id, lc_flag=None)
            else:            
                user_info = UserInfo(language=old_user_info.language, user_id=user.id, lc_flag=None)

            db.session.add(user)
            db.session.add(user_info)

            user = db.session.query(User).filter_by(id=userid).first()
            user.confirm_email()

            db.session.commit()

            # return Response("New attempt created", status=200)
            return Helper.create_success_response("New attempt created")

    else:
        return Helper.create_error_response(400, INVALID_USER)
    
    # return Response(TASK_NOT_COMPLETED.format(user.email), status=422)
    return Helper.create_error_response(201, TASK_NOT_COMPLETED.format(user.email))
