from flask import Blueprint
from views.image import image_view


root_view = Blueprint("root",__name__)
root_view.register_blueprint(image_view,url_prefix="/image")