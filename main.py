from os import environ
from flask import Flask
from views import root_view
from utils.common import CommonUtils
from models.Error import Error

application = Flask(__name__)

application.register_blueprint(root_view,url_prefix="/")


@application.errorhandler(Error)
def handle_error(error:Error):
    print(error)
    return CommonUtils.get_error_response(error)


@application.errorhandler(Exception)
def handle_error(exception:Exception):
    line_number = exception.__traceback__.tb_lineno
    file_name = exception.__traceback__.tb_frame.f_code.co_filename
    print(f'An error occurred at line {line_number} in file {file_name}')
    print(exception)
    error = Error("Internel server error", 500)
    return CommonUtils.get_error_response(error)


@application.get("/")
def home():
    return "Online",200


if __name__ == "__main__":
    application.run(host=environ["HOST"], port=environ["PORT"])