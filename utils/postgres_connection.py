import os
from flask_sqlalchemy import SQLAlchemy

POSTGRES_USERNAME = os.environ["POSTGRES_USERNAME"]
POSTGRES_PASSWORD = os.environ["POSTGRES_PASSWORD"]
POSTGRES_HOST_AND_PORT = os.environ["POSTGRES_HOST_AND_PORT"]
POSTGRES_DBNAME = os.environ["POSTGRES_DBNAME"]

db = SQLAlchemy()
