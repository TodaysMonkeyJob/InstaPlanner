from flask import Blueprint

alcohol = Blueprint('profile', __name__, url_prefix='/profile',template_folder='templates')

from . import views
