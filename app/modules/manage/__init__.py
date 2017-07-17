from flask import Blueprint
# create a blueprint
async = Blueprint('async', __name__)

from . import views