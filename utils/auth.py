import jwt
import os
import bcrypt
from utils.env import EnvironmentVariables

class AuthUtils:
    JWT_ALGORITHM = "HS256"

    def encode_jwt_token(payload: dict) -> str:
        try:
            jwt_token = jwt.encode(payload, EnvironmentVariables.get_environment_variable(EnvironmentVariables.JWT_SECRET), AuthUtils.JWT_ALGORITHM)
            return jwt_token
        except Exception as error:
            return None

    def decode_jwt_token(jwt_token: str) -> dict:
        try:
            payload = jwt.decode(jwt_token, EnvironmentVariables.get_environment_variable(EnvironmentVariables.JWT_SECRET), AuthUtils.JWT_ALGORITHM)
            return payload
        except Exception as error:
            return None

    def hash_string(string: str) -> str:
        byte_string = string.encode("utf-8")
        salt = bcrypt.gensalt()
        hashed_string = bcrypt.hashpw(byte_string, salt)
        return hashed_string.decode("utf-8")

    def validate_hashed_string(string: str, hashed_string: str) -> str:
        string = string.encode("utf-8")
        hashed_string = hashed_string.encode("utf-8")
        try:
            return bcrypt.checkpw(string, hashed_string)
        except Exception as error:
            return False
