from helpers.User import UserHelper
from repository.auth import AuthRepository
from utils.common import CommonUtils
from utils.auth import AuthUtils
from models.Error import Error
from constants.auth import AuthConstants

class AuthService:
    def register(request_body: dict) -> UserHelper:
        user_name: str = request_body["user_name"]
        user_email: str = request_body["user_email"]
        password: str = request_body["password"]
        try:
            AuthRepository.get_user_by_email(user_email)
            raise Error("User email already exists",400)
        except:
            pass
        hashed_password = AuthUtils.hash_string(password)
        user_object: UserHelper = UserHelper(
            user_name=user_name,
            user_email=user_email,
            password=hashed_password,
            roles=[ AuthConstants.USER_ROLE ]
        )
        user_object: UserHelper or None = AuthRepository.add_user(user_object)
        return user_object

    def login(request_body: dict) -> UserHelper:
        user_email: str = request_body["user_email"]
        password: str = request_body["password"]
        user_object = AuthRepository.get_user_by_email(user_email)
        if AuthUtils.validate_hashed_string(password, user_object.password):
            return user_object
        else:
            raise Error("Invalid password",400)

    def change_password(request_body) -> UserHelper:
        user_email: str = request_body["user_email"]
        old_password: str = request_body["old_password"]
        new_password: str = request_body["new_password"]
        user_object = AuthRepository.get_user_by_email(user_email)
        if not AuthUtils.validate_hashed_string(old_password, user_object.password):
            raise Error("Invalid password",400)
        new_hashed_password = AuthUtils.hash_string(new_password)
        user_object.password = new_hashed_password
        new_user_object = AuthRepository.replace_user(user_object)
        return new_user_object
    
    def get_all_users():
        return AuthRepository.get_all_users()

    def add_admin(request_body):
        user_name: str = request_body["user_name"]
        user_email: str = request_body["user_email"]
        password: str = request_body["password"]
        try:
            AuthRepository.get_user_by_email(user_email)
            raise Error("User email already exists",400)
        except:
            pass
        hashed_password = AuthUtils.hash_string(password)
        user_object: UserHelper = UserHelper(
            user_name=user_name,
            user_email=user_email,
            password=hashed_password,
            roles=[ AuthConstants.USER_ROLE, AuthConstants.ADMIN_ROLE ]
        )
        user_object: UserHelper or None = AuthRepository.add_user(user_object)
        return user_object
