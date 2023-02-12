from functools import wraps
from models.Error import Error
from utils.auth import AuthUtils
from flask import request
from flask import g as global_flask
from repository.auth import AuthRepository

class AuthMiddleware:
    def auth(user_role:str or None = None):
        def _auth(f):
            @wraps(f)
            def __auth(*args,**kwargs):
                if not "Authorization" in request.headers:
                    raise Error("Authorization header was not found",401)
                jwt_token:str = request.headers['Authorization']
                jwt_payload:dict = AuthUtils.decode_jwt_token(jwt_token)
                if not jwt_payload:
                    raise Error("Authorization token invalid",401)
                user_id:str = jwt_payload['user_id']
                print(jwt_payload)
                user = AuthRepository.get_user_by_id(user_id)
                if not user:
                    raise Error("User doesn't exist",401)
                if user_role and user.roles.count(user_role) == 0:
                    raise Error("You are not authorized",402)
                global_flask.context['user'] = user
                return f(*args,**kwargs)
            return __auth
        return _auth
