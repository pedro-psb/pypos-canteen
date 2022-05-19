from flask import Blueprint

bp = Blueprint('product', __name__, url_prefix='/product_managment')
from .views import *