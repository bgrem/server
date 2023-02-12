from typing import List
from sqlalchemy import ARRAY
from sqlalchemy.sql import func
from utils.postgres_connection import db
from sqlalchemy.dialects.postgresql import TIMESTAMP, VARCHAR


class ImageModel(db.Model):
    image_id = db.Column(VARCHAR, nullable=False, primary_key=True)
    user_id = db.Column(VARCHAR, nullable=False, primary_key=False)
    input_image_url = db.Column(VARCHAR, nullable=False, primary_key=False)
    output_image_url = db.Column(VARCHAR, nullable=False, primary_key=False)
    def __init__(
        self,
        image_id:str,
        user_id: str,
        input_image_url:str,
        output_image_url:str,
    ) -> None:
        self.image_id = image_id
        self.user_id = user_id
        self.input_image_url = input_image_url
        self.output_image_url = output_image_url

    def __repr__(self):
        return f"<Image {self.image_id}>"
