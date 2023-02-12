from helpers.Image import ImageHelper
from models.ImageModel import ImageModel


class ImageMapper:
    def map_dao_to_object(image_dao: ImageModel) -> ImageHelper:
        return ImageHelper(
            image_id=image_dao.image_id,
            user_id=image_dao.user_id,
            input_image_url=image_dao.input_image_url,
            output_image_url=image_dao.output_image_url
        )

    def map_object_to_dao(image_object: ImageHelper) -> ImageModel:
        return ImageModel(
            image_id=image_object.image_id,
            user_id=image_object.user_id,
            input_image_url=image_object.input_image_url,
            output_image_url=image_object.output_image_url
        )
