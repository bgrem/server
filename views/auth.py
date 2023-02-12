from flask import Blueprint, request
from middlewares.auth import AuthMiddleware
from services.auth import AuthService
from utils.common import CommonUtils
from utils.auth import AuthUtils
from constants.auth import AuthConstants
from middlewares.request_parcer import RequestParcer

auth_view = Blueprint("auth", __name__)


@auth_view.post("/register")
@RequestParcer.validate_request({"user_name":str,"user_email":str,"password":str})
def register():
    request_body = request.get_json()
    user_object = AuthService.register(request_body)
    if user_object:
        jwt_token = AuthUtils.encode_jwt_token({"user_id": user_object.user_id})
        return CommonUtils.get_response(
            "Registered user successfully",
            200,
            {"user_id": user_object.user_id, "jwt_token": jwt_token},
        )
    return CommonUtils.get_response("Register failed", 400)


@auth_view.post("/login")
@RequestParcer.validate_request({"user_email":str,"password":str})
def login():
    request_body = request.get_json()
    user_object = AuthService.login(request_body)
    if user_object:
        jwt_token = AuthUtils.encode_jwt_token({"user_id": user_object.user_id})
        return CommonUtils.get_response(
            "Logged in successfully",
            200,
            {"user_id": user_object.user_id, "jwt_token": jwt_token},
        )
    return CommonUtils.get_response("Login failed", 400)


@auth_view.post("/change_password")
@RequestParcer.validate_request({"user_email":str,"old_password":str,"new_password":str})
def change_password():
    request_body = request.get_json()
    user_object = AuthService.change_password(request_body)
    if user_object:
        return CommonUtils.get_response(
            "Password changed successfully",
            200,
        )
    return CommonUtils.get_response("Password change failed", 400)

@auth_view.post("/add_admin")
@RequestParcer.validate_request({"user_name":str,"user_email":str,"password":str})
@AuthMiddleware.auth(AuthConstants.ADMIN_ROLE)
def add_admin():
    request_body = request.get_json()
    user_object = AuthService.add_admin(request_body)
    if user_object:
        jwt_token = AuthUtils.encode_jwt_token({"user_id": user_object.user_id})
        return CommonUtils.get_response(
            "Registered user successfully",
            200,
            {"user_id": user_object.user_id, "jwt_token": jwt_token},
        )
    return CommonUtils.get_response("Register failed", 400)


@auth_view.get("/check_admin")
@AuthMiddleware.auth(AuthConstants.ADMIN_ROLE)
def check_admin():
    return CommonUtils.get_response("valid",200)


@auth_view.get("/check")
@AuthMiddleware.auth()
def check():
    return CommonUtils.get_response("valid",200)