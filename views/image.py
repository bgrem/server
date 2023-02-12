from flask import Blueprint, request, send_file
from io import BytesIO
from PIL import Image
from services.image import ImageService
from middlewares.request_parcer import RequestParcer
from werkzeug.datastructures import FileStorage
from models.Error import Error
from middlewares.auth import AuthMiddleware
from helpers.User import UserHelper
from flask import g as global_flask
from helpers.Image import ImageHelper
from constants.auth import AuthConstants
from utils.common import CommonUtils

image_view = Blueprint("image",__name__)

@image_view.post("/remove_background")
@RequestParcer.validate_request({},{"image":None})
@AuthMiddleware.auth()
def remove_background():
    image_file:FileStorage = request.files.get("image")
    if not image_file:
        raise Error(message="Image not provided",status_code=400)
    input_image_bytes = BytesIO()
    image_file.save(input_image_bytes)
    input_image = Image.open(input_image_bytes)
    matte = ImageService.get_matte(input_image)
    print("Generation of matte successful")
    output_image = ImageService.remove_background(input_image,matte)
    print("Generation of foreground successful")
    output_image_bytes = BytesIO()
    output_image.save(output_image_bytes, 'JPEG', quality=70)
    output_image_bytes.seek(0)
    input_res = ImageService.upload_image(input_image_bytes)
    input_image_url = input_res['secure_url']
    print("Uploaded input image:",input_image_url)
    output_res = ImageService.upload_image(output_image_bytes)
    output_image_url = output_res['secure_url']
    print("Uploaded output image:",output_image_url)
    user:UserHelper = global_flask.context['user']
    image = ImageHelper(user_id=user.user_id,input_image_url=input_image_url,output_image_url=output_image_url)
    ImageService.add_image(image=image)
    return send_file(output_image_bytes, mimetype='image/jpeg')


@image_view.get("/")
@AuthMiddleware.auth(AuthConstants.ADMIN_ROLE)
def get_all():
    all_image_helpers = ImageService.get_all_images()
    all_images = []
    for all_image_helper in all_image_helpers:
        all_images.append(all_image_helper.__dict__)
    return CommonUtils.get_response("Successful", 200, {"images":all_images})


@image_view.get("/<user_id>")
@AuthMiddleware.auth()
def get_one(user_id):
    user:UserHelper = global_flask.context['user']
    if user.user_id != user_id and user.roles.count(AuthConstants.ADMIN_ROLE) == 0:
        raise Error("Unauthorized", 402)
    user_image_helpers = ImageService.get_images_of_user(user.user_id)
    user_images = []
    for user_image_helper in user_image_helpers:
        user_images.append(user_image_helper.__dict__)
    return CommonUtils.get_response("Successful", 200, {"images":user_images})