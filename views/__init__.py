from flask import Blueprint
from views.image import image_view
from views.auth import auth_view

root_view = Blueprint("root",__name__)
root_view.register_blueprint(image_view,url_prefix="/image")
root_view.register_blueprint(auth_view,url_prefix="/auth")