from os import environ
from flask import Flask
from views import root_view
from utils.common import CommonUtils
from models.Error import Error
from flask_cors import CORS
from dotenv import load_dotenv
from flask_migrate import Migrate
from utils.postgres_connection import (
    POSTGRES_DBNAME,
    POSTGRES_HOST_AND_PORT,
    POSTGRES_PASSWORD,
    POSTGRES_USERNAME,
    db,
)
from flask import g as global_flask
from repository.auth import AuthRepository
from helpers.User import UserHelper
from utils.env import EnvironmentVariables
from utils.auth import AuthUtils
from constants.auth import AuthConstants
import cloudinary

load_dotenv()

cloudinary.config(
  cloud_name = EnvironmentVariables.get_environment_variable(EnvironmentVariables.CLOUDINARY_CLOUD_NAME), 
  api_key = EnvironmentVariables.get_environment_variable(EnvironmentVariables.CLOUDINARY_CLOUD_API_KEY), 
  api_secret = EnvironmentVariables.get_environment_variable(EnvironmentVariables.CLOUDINARY_CLOUD_API_SECRET),
  secure = True
)

application = Flask(__name__)


CORS(application, resorces={r"/*": {"origins": "*"}}, support_credentials=True)


application.register_blueprint(root_view,url_prefix="/")


application.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"pool_pre_ping": True}
application.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
application.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"postgresql://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_HOST_AND_PORT}/{POSTGRES_DBNAME}"
db.init_app(application)
migrate = Migrate(application, db)


@application.errorhandler(Error)
def handle_error(error:Error):
    print(error)
    return CommonUtils.get_error_response(error)


# @application.errorhandler(Exception)
# def handle_exception(exception:Exception):
#     line_number = exception.__traceback__.tb_lineno
#     file_name = exception.__traceback__.tb_frame.f_code.co_filename
#     print(f'An error occurred at line {line_number} in file {file_name}')
#     print(exception)
#     error = Error("Internel server error", 500)
#     return CommonUtils.get_error_response(error)


@application.after_request
def remove_context(f):
    try:
        global_flask.pop("context")
    except:
        pass
    return f


@application.before_request
def create_context():
    global_flask.context = {}

@application.before_first_request
def add_admin_user():
    try:
        if AuthRepository.get_user_by_email(EnvironmentVariables.get_environment_variable(EnvironmentVariables.ADMIN_EMAIL)):
            print("Exists")
            return
    except:
        pass

    hashed_password = AuthUtils.hash_string(EnvironmentVariables.get_environment_variable(EnvironmentVariables.ADMIN_PASSWORD))
    user:UserHelper = UserHelper(
        EnvironmentVariables.get_environment_variable(EnvironmentVariables.ADMIN_USER),
        EnvironmentVariables.get_environment_variable(EnvironmentVariables.ADMIN_EMAIL),
        hashed_password,
        roles=[ AuthConstants.ADMIN_ROLE ],
    )
    AuthRepository.add_user(user)

@application.get("/")
def home():
    return "Online",200


if __name__ == "__main__":
    application.run(host=environ["HOST"], port=environ["PORT"])