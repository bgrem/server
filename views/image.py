from flask import Blueprint, request, send_file
from io import BytesIO
from PIL import Image
from services.image import ImageService
from middlewares.request_parcer import RequestParcer
from werkzeug.datastructures import FileStorage
from models.Error import Error

image_view = Blueprint("image",__name__)

@image_view.post("/remove_background")
@RequestParcer.validate_request({},{"image":None})
def remove_background():
    image_file:FileStorage = request.files.get("image")
    if not image_file:
        raise Error(message="Image not provided",status_code=400)
    input_image_bytes = BytesIO()
    image_file.save(input_image_bytes)
    input_image = Image.open(input_image_bytes)
    matte = ImageService.get_matte(input_image)
    output_image = ImageService.remove_background(input_image,matte)
    output_image_bytes = BytesIO()
    output_image.save(output_image_bytes, 'JPEG', quality=70)
    output_image_bytes.seek(0)
    return send_file(output_image_bytes, mimetype='image/jpeg')
