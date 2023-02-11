from functools import wraps
from models.Error import Error
from utils.auth import AuthUtils
from flask import request
from flask import g as global_flask

class RequestParcer:

    def auth():
        def _auth(f):
            @wraps(f)
            def __auth(*args,**kwargs):
                if not "Authorization" in request.headers:
                    raise Error("Authorization header was not found",401)
                jwt_token:str = request.headers['Authorization']
                jwt_payload:dict = AuthUtils.validate_jwt_token(jwt_token)
                return f(*args,**kwargs)
            return __auth
        return _auth
