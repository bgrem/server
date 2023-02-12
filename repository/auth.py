from typing import List
from helpers.User import UserHelper
from mappers.auth import AuthMapper
from models.UserModel import UserModel
from sqlalchemy.exc import SQLAlchemyError
from utils.postgres_connection import db
from typing import List
from models.UserModel import UserModel
from sqlalchemy.exc import SQLAlchemyError
from utils.postgres_connection import db
from models.Error import Error


class AuthRepository:
    def replace_user(user_object: UserHelper) -> None or UserHelper:
        try:
            user_dao: UserModel = UserModel.query.get(user_object.user_id)
            if not user_dao:
                raise Error("User doesnt exist",400)
            new_user_dao = AuthMapper.map_object_to_dao(user_object)
            user_dao.user_name = new_user_dao.user_name
            user_dao.user_email = new_user_dao.user_email
            user_dao.password = new_user_dao.password
            db.session.commit()
            replaced_user_dao = AuthRepository.get_user_by_id(user_dao.user_id)
        except SQLAlchemyError as e:
            print(e)
            raise Error("Database Error",400)
        if replaced_user_dao:
            print(replaced_user_dao.__dict__)
        return user_dao

    def add_user(user_object: UserHelper) -> None or UserHelper:
        user_dao: UserModel = AuthMapper.map_object_to_dao(user_object)
        try:
            db.session.add(user_dao)
            db.session.commit()
            added_user_dao = AuthRepository.get_user_by_id(user_object.user_id)
        except SQLAlchemyError as e:
            print(e)
            raise Error("Database Error",400)
        if added_user_dao:
            print(added_user_dao.__dict__)
        return added_user_dao

    def get_user_by_id(user_id: str) -> None or UserHelper:
        try:
            user_dao = UserModel.query.get(user_id)
            if not user_dao:
                raise Error("User doesnt exist",400)
            user_object = AuthMapper.map_dao_to_object(user_dao)
        except SQLAlchemyError as e:
            print(e)
            raise Error("Database Error",400)
        if user_object:
            print(user_object.__dict__)
        else:
            raise Error("User not found",400)
        return user_object

    def get_user_by_email(user_email: str) -> None or UserHelper:
        try:
            user_dao_array: List[UserModel] = UserModel.query.all()
            user_object = None
        except SQLAlchemyError as e:
            print(e)
            raise Error("Database Error",400)
        for user_dao in user_dao_array:
            if user_dao.user_email == user_email:
                user_object = AuthMapper.map_dao_to_object(user_dao)
        if user_object:
            print(user_object.__dict__)
        else:
            raise Error("User not found",400)
        return user_object

    def get_user_by_name(user_name: str) -> None or UserHelper:
        try:
            user_dao_array: List[UserModel] = UserModel.query.all()
            user_object = None
        except SQLAlchemyError as e:
            print(e)
            raise Error("Database Error",400)
        for user_dao in user_dao_array:
            if user_dao.user_name == user_name:
                user_object = AuthMapper.map_dao_to_object(user_dao)
        if user_object:
            print(user_object.__dict__)
        else:
            raise Error("User not found",400)
        return user_object

    def get_all_users() -> List[UserHelper]:
        try:
            user_dao_array = UserModel.query.all()
            users:List[UserHelper] = []
            for user_dao in user_dao_array:
                users.append(AuthMapper.map_dao_to_object(user_dao))
            return users
        except SQLAlchemyError as e:
            print(e)
            raise Error("Database Error",400)
