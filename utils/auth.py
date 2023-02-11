from jwt import decode
from models.Error import Error

class AuthUtils:
    def validate_jwt_token(jwt_token:str):
        if decode(jwt_token):
            raise Error("Invalid jwt token",401)
        return True