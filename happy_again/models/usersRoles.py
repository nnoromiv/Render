import uuid
from datetime import datetime

from passlib.hash import pbkdf2_sha256
from sqlalchemy import Column, String, Integer, DateTime, Enum, ForeignKey

from happy_again import db
from happy_again.common.utils import datetime_to_str

from sqlalchemy.orm import relationship


class UserRoles(db.Model):
    KEY_ID = 'id'
    KEY_USERNAME = 'username'
    KEY_NAME = 'name'
    KEY_EMAIL = 'email'
    KEY_ROLE = 'role'

    ROLE_ADMIN = 'admin'
    ROLE_LAB_ASSISTANT = 'lab_assistant'
    ROLE_RESEARCHER = 'researcher'

    __tablename__ = 'usersRoles'
    __bind_key__ = 'happyagaindb'

    id = Column(String(32), primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=True)
    role = Column(Enum(ROLE_ADMIN, ROLE_LAB_ASSISTANT, ROLE_RESEARCHER), nullable=False)
    confirmed_at_by_user = Column(DateTime, default=None)
    confirmed_at_by_admin = Column(DateTime, default=None)
    last_logged_in_at = Column(DateTime, default=None)
    registered_at = Column(DateTime, default=None)

    tokens = relationship('Token', backref='userRoles', cascade="all, delete-orphan", lazy='dynamic')

    def __init__(self, email, role):
        self.id = str(uuid.uuid4().hex)
        self.email = email
        self.role = role
        self.registered_at = datetime.utcnow()

    def hash_password(self, password):
        self.password_hash = pbkdf2_sha256.hash(password)

    def verify_password(self, password):
        return pbkdf2_sha256.verify(password, self.password_hash)

    def confirm_email(self):
        self.confirmed_at_by_user = datetime.utcnow()

    @staticmethod
    def get_user(user_id):
        return db.session.query(UserRoles).filter_by(id=user_id).first()

    def to_json(self):
        return {
            self.KEY_ID: self.id,
            self.KEY_EMAIL: self.email,
            self.KEY_ROLE: self.role,
        }


class Token(db.Model):
    KEY_ID = "id"
    KEY_ISSUED_AT = "issued_at"
    ROLE_ADMIN = 'admin'
    ROLE_LAB_ASSISTANT = 'lab_assistant'
    ROLE_RESEARCHER = 'researcher'

    __tablename__ = 'tokens'

    id = Column(String(32), primary_key=True)
    issued_at = Column(DateTime, nullable=False)
    user_id = Column(String(32), ForeignKey('usersRoles.id'), nullable=False)
    role = Column(Enum(ROLE_ADMIN, ROLE_LAB_ASSISTANT, ROLE_RESEARCHER), nullable=False)


    def __init__(self, user_id, role):
        self.id = str(uuid.uuid4().hex)
        self.user_id = user_id
        self.issued_at = datetime.utcnow()
        self.role = role

    def to_json(self):
        return {
            self.KEY_ID: self.id,
            self.KEY_ISSUED_AT: self.issued_at.isoformat()
        }

    @staticmethod
    def get_token(token_id):
        return db.session.query(Token).filter_by(id=token_id).first()