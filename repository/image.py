from helpers.Image import ImageHelper
from models.ImageModel import ImageModel
from mappers.image import ImageMapper
from sqlalchemy.exc import SQLAlchemyError
from utils.postgres_connection import db
from models.Error import Error
from typing import List

class ImageRepository:
    def add_image(image_object: ImageHelper) -> None or ImageHelper:
        image_dao: ImageModel = ImageMapper.map_object_to_dao(image_object)
        try:
            db.session.add(image_dao)
            db.session.commit()
            added_image_dao = ImageRepository.get_image_by_id(image_object.image_id)
        except SQLAlchemyError as e:
            print(e)
            raise Error("Database Error",400)
        if added_image_dao:
            print(added_image_dao.__dict__)
        return added_image_dao

    def get_images_of_user(user_id: str) :
        try:
            image_dao_array: List[ImageModel] = ImageModel.query.all()
        except SQLAlchemyError as e:
            print(e)
            raise Error("Database Error",400)
        images:List[ImageHelper] = []
        for image_dao in image_dao_array:
            if image_dao.user_id == user_id:
                images.append(ImageMapper.map_dao_to_object(image_dao))
        return images

    def get_image_by_id(image_id: str) -> None or ImageHelper:
        try:
            image_dao = ImageModel.query.get(image_id)
            if not image_dao:
                raise Error("Image doesnt exist",400)
            image_object = ImageMapper.map_dao_to_object(image_dao)
        except SQLAlchemyError as e:
            print(e)
            raise Error("Database Error",400)
        if image_object:
            print(image_object.__dict__)
        else:
            raise Error("Image not found",400)
        return image_object

    
    def get_all_images():
        try:
            image_dao_array: List[ImageModel] = ImageModel.query.all()
        except SQLAlchemyError as e:
            print(e)
            raise Error("Database Error",400)
        images:List[ImageHelper] = []
        for image_dao in image_dao_array:
            images.append(ImageMapper.map_dao_to_object(image_dao))
        return images
        
