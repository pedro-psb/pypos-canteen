from flask import Blueprint

bp = Blueprint('point_of_sale', __name__, url_prefix='/point_of_sale')
from .views import *