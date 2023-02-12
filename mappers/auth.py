from helpers.User import UserHelper
from models.UserModel import UserModel


class AuthMapper:
    def map_dao_to_object(user_dao: UserModel) -> UserHelper:
        return UserHelper(
            user_name=user_dao.user_name,
            user_email=user_dao.user_email,
            password=user_dao.password,
            user_id=user_dao.user_id,
            roles=user_dao.roles,
        )

    def map_object_to_dao(user_object: UserHelper) -> UserModel:
        return UserModel(
            user_name=user_object.user_name,
            user_email=user_object.user_email,
            password=user_object.password,
            user_id=user_object.user_id,
            roles=user_object.roles,
        )
