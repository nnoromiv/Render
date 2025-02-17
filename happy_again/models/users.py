import uuid
from datetime import datetime
from datetime import timedelta

from passlib.hash import pbkdf2_sha256
from sqlalchemy import Column, String, Integer, DateTime, Enum

from happy_again import db
from happy_again.common.utils import datetime_to_str


class User(db.Model):
    KEY_ID = "id"
    KEY_EMAIL = "email"
    KEY_REGISTERED_AT = "registered_at"
    KEY_CONFIRMED_AT_BY_USER = "confirmed_at_by_user"
    KEY_SESSION_ID = "session_id"
    KEY_BLOCKED = 'blocked'

    __tablename__ = "users"
    __bind_key__ = 'userdb'

    id = Column(String(64), primary_key=True, nullable=False)
    email = Column(String(255), nullable=False)
    password_hash = Column(String(255), nullable=False)
    registered_at = Column(DateTime, nullable=False)
    confirmed_at_by_user = Column(DateTime, default=None)
    blocked = Column(Integer, nullable=False)

    def __init__(self, user_id, email, password):
        print("registering w type's", type(password))
        #self.id = str(uuid.uuid4().hex+"_1")
        self.id= user_id
        self.email = email
        self.hash_password(password)
        self.registered_at = datetime.utcnow()
        self.blocked = 0

    def hash_password(self, password):
        self.password_hash = pbkdf2_sha256.hash(password)

    def verify_password(self, password):
        return pbkdf2_sha256.verify(password, self.password_hash)

    def confirm_email(self):
        self.confirmed_at_by_user = datetime.utcnow()

    def change_password(self, password):
        self.hash_password(password)
        
    def block_user(self):
        self.blocked = 1

    def unblock_user(self):
        self.blocked = 0

    @staticmethod
    def get_user(user_id):
        return db.session.query(User).filter_by(id=user_id).first()

    def to_json(self):
        return {
            self.KEY_ID: self.id,
            self.KEY_EMAIL: self.email,
            self.KEY_REGISTERED_AT: datetime_to_str(self.registered_at),
            self.KEY_CONFIRMED_AT_BY_USER: datetime_to_str(self.confirmed_at_by_user),
        }


class Session(db.Model):
    KEY_ID = "id"
    KEY_START_TIME = "start_time"
    KEY_END_TIME = "end_time"
    KEY_LAST_COMPLETED_TASK = "last_completed_task"
    KEY_BROWSER = "browser"
    KEY_VERSION = "version"
    KEY_OP_SYSTEM = "op_system"
    KEY_SCREEN_RESOLUTION = "screen_resolution"
    KEY_PIXEL_DENSITY_H = "pixel_density_h"
    KEY_PIXEL_DENSITY_W = "pixel_density_w"
    KEY_USER_AGENT = "user_agent"
    KEY_USER_ID = "user_id"

    __tablename__ = "sessions"
    __bind_key__ = 'happyagaindb'

    id = Column(String(32), primary_key=True, nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, default=None)
    las_completed_task = Column(String(32), default=None)
    browser = Column(String(32), default=None)
    version = Column(String(32), default=None)
    op_system = Column(String(32), default=None)
    screen_resolution = Column(String(32), default=None)
    pixel_density_h = Column(String(32), default=None)
    pixel_density_w = Column(String(32), default=None)
    user_agent = Column(String(200), default=None)
    user_id = Column(String(64), nullable=False)

    def __init__(self, user_id):
        self.id = str(uuid.uuid4().hex)
        self.start_time = datetime.utcnow()
        self.user_id = user_id

    def update_session_data(self, browser, version, op_system, screen_resolution,
                            pixel_density_h, pixel_density_w, user_agent, user_id):
        self.las_completed_task = 0
        self.browser = browser
        self.version = version
        self.op_system = op_system
        self.screen_resolution = screen_resolution
        self.pixel_density_h = pixel_density_h
        self.pixel_density_w = pixel_density_w
        self.user_agent = user_agent
        self.user_id = user_id

    def logged_out(self):
        self.end_time = datetime.utcnow()

    def update_last_completed_task(self, las_completed_task):
        self.las_completed_task = las_completed_task

    def to_json(self):
        return {
            self.KEY_ID: self.id,
            self.KEY_START_TIME: datetime_to_str(self.start_time),
            self.KEY_END_TIME: datetime_to_str(self.end_time),
            self.KEY_LAST_COMPLETED_TASK: self.las_completed_task,
            self.KEY_BROWSER: self.browser,
            self.KEY_VERSION: self.version,
            self.KEY_OP_SYSTEM: self.op_system,
            self.KEY_SCREEN_RESOLUTION: self.screen_resolution,
            self.KEY_PIXEL_DENSITY_H: self.pixel_density_h,
            self.KEY_PIXEL_DENSITY_W: self.pixel_density_w,
            self.KEY_USER_AGENT: self.user_agent,
            self.KEY_USER_ID: self.user_id
        }

    @staticmethod
    def get_session(session_id):
        return db.session.query(Session).filter_by(id=session_id).first()


class UserInfo(db.Model):
    KEY_ID = "id"
    KEY_LC_FLAG = "lc_flag"
    KEY_GENDER = "gender"
    KEY_LANGUAGE = "language"
    KEY_CONSENT_DATE = "consent"
    KEY_USER_ID = "user_id"

    GENDER_MALE = "male"
    GENDER_FEMALE = "female"
    GENDER_OTHERS = "others"

    __tablename__ = "users_info"
    __bind_key__ = 'happyagaindb'

    id = Column(String(32), primary_key=True, nullable=False)
    lc_flag = Column(Integer, default=None)
    gender = Column(Enum(GENDER_MALE, GENDER_FEMALE, GENDER_OTHERS), default=None)
    language = Column(String(255), nullable=False)
    consent_date = Column(DateTime, nullable=False)
    user_id = Column(String(64), nullable=False)

    def __init__(self, language, user_id,lc_flag):
        self.id = str(uuid.uuid4().hex)
        self.language = language
        self.consent_date = datetime.utcnow()
        self.user_id = user_id
        self.lc_flag=lc_flag

    def update_user_info(self, age, gender):
        self.age = age
        self.gender = gender

    def to_json(self):
        return {
            self.KEY_ID: self.id,
            self.KEY_LC_FLAG: self.lc_flag,
            self.KEY_GENDER: self.gender,
            self.KEY_LANGUAGE: self.language,
            self.KEY_CONSENT_DATE: datetime_to_str(self.consent_date),
            self.KEY_USER_ID: self.user_id,
        }

class Admin(db.Model):
    EMAIL = "email"
    
    __tablename__ = "admins"
    __bind_key__ = 'userdb'
    
    email = Column(String(255), primary_key=True, nullable=False)
    
    def __init__(self, email):
        self.email = email
        
    def to_json(self):
        return {
            self.EMAIL: self.email
        }

class NotifiedUsers (db.Model):
    EMAIL = "email"
    N_MAIL_SENDED = "n_email_sended"
    TIMESTAMP="timestamp"


    email = Column(String(255), primary_key=True, nullable=False)
    n_mail_sended=Column(Integer, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    
    __table_name = "notified_users"
    __bind_key__ = 'userdb'

    def __init__(self, email, n_mail_sended):
        self.email = email
        self.n_mail_sended = n_mail_sended
        self.timestamp = datetime.utcnow()
        
    def update_info(self,n_mail_sended):
        self.n_mail_sended = n_mail_sended
        self.timestamp = datetime.utcnow()

    def extend_user(self, time):
        # User is blocked when the timestamp is past 4 days
        self.timestamp =  datetime.utcnow() + timedelta(days=int(time)-4) 
        
    def to_json(self):
        return{
            self.EMAIL: self.email,
            self.N_MAIL_SENDED: self.n_mail_sended,
            self.TIMESTAMP: datetime_to_str(self.timestamp)
        }

class CheckedUsers (db.Model):
    EMAIL = "email"
    IS_CHECKED = "is_checked"

    email = Column(String(255), primary_key=True, nullable=False)
    is_checked=Column(Integer, nullable=False)
    
    __table_name = "checked_users"
    __bind_key__ = 'userdb'

    def __init__(self, email, is_checked):
        self.email = email
        self.is_checked = is_checked
        
    def update_checkbox(self):
        if self.is_checked==0:
            self.is_checked = 1
        else:
            self.is_checked = 0
        
    def to_json(self):
        return{
            self.EMAIL: self.email,
            self.IS_CHECKED: self.is_checked,
        }
        
class OtpCodes (db.Model):
    CODE="code"

    code = Column(String(255), primary_key=True, nullable=False)
    
    __table_name = "otp_codes"
    __bind_key__ = 'userdb'

    def __init__(self, code):
        self.code = code
        
    def to_json(self):
        return{
            self.CODE: self.code

        }

class NoVoucher (db.Model):
    EMAIL="email"
    NATION="nation"

    email = Column(String(255), primary_key=True, nullable=False)
    nation = Column(String(255), primary_key=True, nullable=False)
    
    __table_name = "no_voucher"
    __bind_key__ = 'userdb'

    def __init__(self, email,nation):
        self.email=email
        self.nation=nation
        
    def to_json(self):
        return{
            self.EMAIL: self.email,
            self.NATION: self.nation,

        }
    
class SubjectUniqueId (db.Model):
    ID="id"
    EMAIL="email"
    SUBJECT_ID="subject_id"

    id=Column(String(255), primary_key=True, nullable=False)
    email = Column(String(255), primary_key=True, nullable=False)
    subject_id = Column(Integer, primary_key=True, nullable=False)
    
    __table_name = "subject_unique_id"
    __bind_key__ = 'userdb'

    def __init__(self,id, email,subject_id):
        self.id=id
        self.email=email
        self.subject_id=subject_id
        
    def to_json(self):
        return{
            self.ID:self.id,
            self.EMAIL: self.email,
            self.SUBJECT_ID: self.subject_id,
        }