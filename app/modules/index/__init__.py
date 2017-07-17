from flask import Blueprint
# create a blueprint
index = Blueprint('index', __name__)

from . import views

