from os import environ
class EnvironmentVariables:
    REFRENCE_IMAGE_URL="REFRENCE_IMAGE_URL"
    JWT_SECRET="JWT_SECRET"
    ADMIN_USER="admin"
    ADMIN_EMAIL="admin@gmail.com"
    ADMIN_PASSWORD="Admin@123"


    def get_environment_variable(name:str):
        return environ[name]