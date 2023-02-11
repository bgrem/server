from os import environ
class EnvironmentVariables:
    REFRENCE_IMAGE_URL="REFRENCE_IMAGE_URL"
    JWT_SECRET="JWT_SECRET"

    def get_environment_variable(name:str):
        return environ[name]