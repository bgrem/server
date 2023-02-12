from typing import List
from sqlalchemy import ARRAY
from sqlalchemy.sql import func
from utils.postgres_connection import db
from sqlalchemy.dialects.postgresql import TIMESTAMP, VARCHAR


class UserModel(db.Model):
    user_id = db.Column(VARCHAR, nullable=False, primary_key=True)
    user_name = db.Column(VARCHAR, nullable=False, primary_key=False)
    user_email = db.Column(VARCHAR, nullable=False, primary_key=False, unique=True)
    roles = db.Column(ARRAY(VARCHAR), nullable=False, primary_key=False)
    password = db.Column(VARCHAR, nullable=False, primary_key=False)
    created_time = db.Column(TIMESTAMP, server_default=func.now())
    update_time = db.Column(TIMESTAMP, server_default=func.now(), onupdate=func.current_timestamp())

    def __init__(
        self,
        user_name: str,
        user_email: str,
        password: str,
        user_id: str = None,
        roles:List[str] = [],
    ) -> None:
        self.user_id = user_id
        self.user_name = user_name
        self.user_email = user_email
        self.password = password
        self.roles = roles

    def __repr__(self):
        return f"<User {self.user_id}>"
