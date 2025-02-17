from flask import Flask
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
mail = Mail()

from happy_again.models import MedicalInfo
from happy_again.models import User
from happy_again.models import UserRoles
from happy_again.models import questionaire
from happy_again.models import word_encoding
from happy_again.models import LoudnessPerception
from happy_again.common.consts import deployment


def create_app():
    app = Flask(__name__)
    app.config.update(dict(
        DEBUG=True,
        MAIL_SERVER='smtp.gmail.com',
        MAIL_PORT=465,
        MAIL_USE_TLS=False,
        MAIL_USE_SSL=True,
        MAIL_USERNAME='happyagainessex',
        MAIL_PASSWORD='bfnlekxmsheslqdu',
        MAIL_DEFAULT_SENDER='happyagainessex@gmail.com',
        MAX_CONTENT_LENGTH=2048 * 2048
    ))

    # File upload setting
    mail.init_app(app)

    # if deployment:
    #     # ACCESS FROM DEPLOYED VERSION
    #     SQLALCHEMY_DATABASE_URI_USER_DB = 'mysql+mysqldb://iacopo:happyagain@127.0.0.1:3306/userdb?charset=utf8mb4'
    #     SQLALCHEMY_DATABASE_URI_HAPPY_AGAIN_DB = 'mysql+mysqldb://iacopo:happyagain@127.0.0.1:3306/happyagaindb?charset=utf8mb4'
    # else:
    # ACCESS FROM LOCAL
    # SQLALCHEMY_DATABASE_URI_USER_DB = 'sqlite:///userdb.db'
    # SQLALCHEMY_DATABASE_URI_HAPPY_AGAIN_DB = 'sqlite:///happyagaindb.db'
    SQLALCHEMY_DATABASE_URI_USER_DB = 'mysql+mysqldb://iacopo:happyagain@cseevito1.essex.ac.uk:3306/userdbdev?charset=utf8mb4'
    SQLALCHEMY_DATABASE_URI_HAPPY_AGAIN_DB = 'mysql+mysqldb://iacopo:happyagain@cseevito1.essex.ac.uk:3306/happyagaindbdev?charset=utf8mb4'

    app.config['SQLALCHEMY_BINDS'] = {
        'userdb': SQLALCHEMY_DATABASE_URI_USER_DB,
        'happyagaindb': SQLALCHEMY_DATABASE_URI_HAPPY_AGAIN_DB
    }

    db.init_app(app)
    app.config["JWT_SECRET_KEY"] = "happyagain"
    jwt = JWTManager(app)
    db.app = app

    from happy_again.apis.users import user_api
    from happy_again.apis.usersRoles import userRoles_api
    from happy_again.apis.temporal_binding_window import temporal_binding_window_api
    from happy_again.apis.questionaire import spq_covid_api
    from happy_again.apis.memory_experiment import word_encoding_api
    from happy_again.apis.loudness_perception import loudness_perception_api
    from happy_again.apis.posner_task import posner_task_api
    from happy_again.apis.movement_perception import movement_perception_api
    from happy_again.apis.tasks import tasks_api

    app.register_blueprint(user_api)
    app.register_blueprint(temporal_binding_window_api)
    app.register_blueprint(userRoles_api)
    app.register_blueprint(spq_covid_api)
    app.register_blueprint(word_encoding_api)
    app.register_blueprint(loudness_perception_api)
    app.register_blueprint(posner_task_api)
    app.register_blueprint(movement_perception_api)
    app.register_blueprint(tasks_api)

    return app
